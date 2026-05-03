I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **Measuring Massive Multitask Language Understanding** is valid for use in **South Asian Agricultural and Environmental Science — Mymensingh–Telangana–Andhra Pradesh Deployment**.

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
- **Domain**: General LLM evaluation — academic and professional knowledge across 57 subjects
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology (Test Case Categories)
MMLU covers 57 subjects across STEM, humanities, social sciences, and "other areas that are
important for some people to learn" [Q18], ranging from elementary to advanced professional
level [Q9]. The taxonomy is organized around US and Western academic disciplines. STEM
subjects include physics, computer science, and mathematics [Q33]; humanities include law,
philosophy, and history [Q25]; and social sciences include economics, sociology, politics,
geography, and psychology [Q29]. Additional subjects include security studies [Q31],
professional medicine [Q166], public relations [Q168], virology [Q172], and world religions
[Q173]. History questions are described as covering "a wide range of time periods and
geographical locations" [Q28], and some social science tasks gesture toward international
content [Q135], but these are framed through US and Western academic lenses (e.g., US
Foreign Policy [Q171], US History [Q151], US law [Q163, Q164]).

Critically, no subject in the 57-task taxonomy addresses agro-ecology, delta hydrology,
flood-plain farming, haor wetland systems, aquaculture, dry-land Deccan cropping, or any
South Asian regional agricultural subdomain [Q117]. The benchmark's stated goal of measuring
"extensive world knowledge" [Q2] is operationalized exclusively through US standardized
examination content [Q19], making the input ontology a poor fit for depth-level knowledge
of boro/aman/aus rice cultivation cycles, Brahmaputra-Jamuna char-land agriculture, or
Telugu dry-land cropping systems in Telangana and Andhra Pradesh. The breadth claim of
57 tasks [Q11, Q83] does not translate into regional agro-ecological coverage.

### Input Content (Data Sources and Instances)
Questions were "manually collected by graduate and undergraduate students from freely
available sources online," drawing from GRE and USMLE practice materials, undergraduate
course content, and Oxford University Press books [Q19]. This sourcing strategy is
explicitly US- and Anglophone-institution-centric. The benchmark assumes models acquire
relevant knowledge from "educational books and websites" encountered during pretraining
on "vast quantities of diverse text from the Internet" [Q63, Q16]. Professional Law
examples were supplemented with approximately 1.6 million legal case summaries from
Harvard's Law Library case law corpus [Q77], and history questions reference English
primary sources such as the English Parliament's Act of Supremacy [Q140, Q141]. Most
questions came from "PDFs or websites where questions and answers are on separate pages"
[Q110], reducing memorization risk but not broadening geographic or cultural coverage.

There is no evidence that any data was sourced from South Asian agricultural extension
services, BRRI (Bangladesh Rice Research Institute) publications, Telugu-medium agronomic
resources, or Bangladeshi university curricula. The authorship team is based entirely at
US research institutions (UC Berkeley, Columbia, UChicago, UIUC) [Q10], and funding
is from US-based sources [Q87, Q88], further anchoring the benchmark's content provenance
in Anglophone academic traditions. Dialect-specific agricultural terminology from
Mymensingh/Bangladeshi contexts (local crop names, haor/beel wetland terms, char-land
farming vocabulary) is absent by construction.

### Input Form (Data Format and Modality)
MMLU is an exclusively text-based, English-language benchmark administered in zero-shot
or few-shot multiple-choice format [Q8]. The full dataset comprises 15,908 questions across
development, validation, and test splits [Q21]. GPT-3 receives prompts of the form "The
following are multiple choice questions (with answers) about [subject]," with up to five
demonstration examples, and the model assigns probability to tokens "A," "B," "C," and "D"
[Q45, Q46]. UnifiedQA uses a normalized, lowercased input format with a special
end-of-sequence token; removing this token causes accuracy to decline by several percentage
points [Q101, Q102], demonstrating sensitivity to input formatting conventions.

For the deployment context, the English-only input format is a direct and confirmed
mismatch. The benchmark provides no mechanism for multilingual querying in Bangladeshi
Bengali (Mymensingh dialect), standard Bengali (Indian or Bangladeshi variants), or Telugu
[elicitation Q4]. The text-only format also excludes multimodal content that may be
relevant to agro-ecological assessments, as the authors themselves acknowledge: "many
important concepts are conveyed mainly through other modalities, such as images, audio,
and physical interaction" [Q64]. Input form validity for South Asian multilingual
deployment is essentially zero.

### Output Ontology (Label Schema and Output Categories)
MMLU applies a uniform four-class multiple-choice label schema (A, B, C, D) across all
57 tasks [Q23]. Some tasks are further differentiated by difficulty level — for example,
psychology appears at "Elementary," "High School," "College," or "Professional" levels
[Q20]. The benchmark measures classification accuracy across all examples and tasks [Q35],
with an expert-level ceiling of approximately 89.8% estimated from 95th-percentile US
standardized test performance [Q22].

This output ontology is entirely generic and does not encode region-specific decision
boundaries or culturally contingent correct answers. For the deployment context, the
four-choice forced-selection schema is particularly problematic for questions where the
correct answer legitimately differs by national or regional context — for instance,
water-sharing policy between Bangladesh and India, or optimal cropping practices under
delta flood regimes versus Deccan dry-land conditions. The label schema provides no
mechanism for capturing legitimate regional divergence. Additionally, models perform
especially poorly on "socially important subjects such as morality and law" [Q6, Q86],
and have difficulty with procedural and calculation-heavy tasks [Q14, Q72], which are
directly relevant to agricultural applications (fertilizer dosing, yield estimation,
flood-cycle planning).

### Output Content (Annotation Process and Label Validity)
NOT DOCUMENTED: The paper is entirely silent on annotator demographics, selection criteria
for the graduate and undergraduate students who collected questions, their regional or
disciplinary backgrounds, inter-annotator agreement statistics, or any quality-assurance
process beyond implicit validation through dataset construction [Q19]. The only documented
human baseline is derived from Amazon Mechanical Turk workers (34.5% accuracy) [Q22],
which provides no information about South Asian agronomic expertise or regional knowledge
standards.

Given that all data sources are US/Western-institution-centric [Q19, Q75, Q77] and the
authorship team is entirely based at US universities [Q10], it is a reasonable inference —
though not documented — that annotators had no representation from Bangladeshi, Indian,
or South Asian agricultural science communities. The user confirms that cross-border
water/agricultural agreement questions could yield divergent correct answers depending
on national perspective, and that practice differences between regions are not reflected
in answer keys [elicitation A3]. There is no basis for assuming that ground-truth labels
for any subject reflect Bangladeshi environmental science standards or Telugu-speaking
agrarian community knowledge.

### Output Form (Evaluation Metrics and Modality)
MMLU evaluates text-based classification outputs only, measuring accuracy of predicted
letter tokens [Q35, Q23]. The paper reports accuracy by broad subject grouping and
per-task [Q52, Q92], evaluates calibration via RMS calibration error and accuracy-confidence
gap [Q62], and finds GPT-3 showing up to 24% miscalibration in zero-shot settings [Q61].
Few-shot calibration improves substantially (r = 0.81 vs. r = 0.63 zero-shot) [Q106].
The benchmark does not evaluate open-ended generation, does not penalize language
mismatches (e.g., model responding in English to a Bengali prompt), and does not support
regional-language or regional-script outputs.

The MCQ accuracy metric partially aligns with the deployment's need for simple cross-model
comparison, but cannot capture the nuanced, open-ended agronomic reasoning that South Asian
environmental science applications may require. The authors acknowledge that current models
fall below expert-level accuracy on every single task [Q4], and that "data may become a
bottleneck" for esoteric knowledge domains [Q81] — a concern amplified for regional South
Asian agricultural knowledge underrepresented in English-language pretraining corpora.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We propose a new test to measure a text model's multitask accuracy. The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more." |
| Q2 | 1 | input_ontology | "To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability." |
| Q3 | 1 | output_form | "We find that while most recent models have near random-chance accuracy, the very largest GPT-3 model improves over random chance by almost 20 percentage points on average." |
| Q4 | 1 | output_form | "However, on every one of the 57 tasks, the best models still need substantial improvements before they can reach expert-level accuracy." |
| Q5 | 1 | output_form | "Models also have lopsided performance and frequently do not know when they are wrong." |
| Q6 | 1 | output_ontology | "Worse, they still have near-random accuracy on some socially important subjects such as morality and law." |
| Q7 | 1 | output_form | "By comprehensively evaluating the breadth and depth of a model's academic and professional understanding, our test can be used to analyze models across many tasks and to identify important shortcomings." |
| Q8 | 1 | input_form | "We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings." |
| Q9 | 1 | input_ontology | "The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability." |
| Q10 | 1 | output_content | "Dan Hendrycks, UC Berkeley; Collin Burns, Columbia University; Steven Basart, UChicago; Andy Zou, UC Berkeley; Mantas Mazeika, UIUC; Dawn Song, UC Berkeley; Jacob Steinhardt, UC Berkeley" |
| Q11 | 2 | input_ontology | "Since our test consists in 57 tasks, it can be used to analyze aggregate properties of models across tasks and to track important shortcomings." |
| Q12 | 2 | output_form | "few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy" |
| Q13 | 2 | output_form | "unlike human professionals GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects." |
| Q14 | 2 | output_ontology | "The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality." |
| Q15 | 2 | output_form | "GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy." |
| Q16 | 2 | input_content | "The dominant paradigm in NLP is to pretrain large models on massive text corpora including educational books and websites." |
| Q17 | 2 | input_ontology | "Many recent benchmarks aim to assess a model's general world knowledge and basic reasoning ability by testing its "commonsense."" |
| Q18 | 3 | input_ontology | "We create a massive multitask test consisting of multiple-choice questions from various branches of knowledge. The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn. There are 57 tasks in total, which is also the number of Atari games (Bellemare et al., 2013), all of which are listed in Appendix B." |
| Q19 | 3 | input_content | "The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online. These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination. It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books." |
| Q20 | 3 | output_ontology | "Some tasks cover a subject, like psychology, but at a specific level of difficulty, such as "Elementary," "High School," "College," or "Professional."" |
| Q21 | 3 | input_form | "We collected 15908 questions in total, which we split into a few-shot development set, a validation set, and a test set. The few-shot development set has 5 questions per subject, the validation set may be used for selecting hyperparameters and is made of 1540 questions, and the test set has 14079 questions. Each subject contains 100 test examples at the minimum, which is longer than most exams designed to assess people." |
| Q22 | 3 | output_content | "Human-level accuracy on this test varies. Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test. Meanwhile, expert-level performance can be far higher. For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations, and these questions make up our "Professional Medicine" task. If we take the 95th percentile human test-taker accuracy for exams that build up our test, and if we make an educated guess when such information is unavailable, we then estimate that expert-level accuracy is approximately 89.8%." |
| Q23 | 3 | output_ontology | "we instead create a simple-to-evaluate test that measures classification accuracy on multiple choice questions." |
| Q24 | 3 | input_ontology | "Since our test aggregates different subjects and several levels of difficulty, we measure more than straightforward commonsense or narrow linguistic understanding." |
| Q25 | 4 | input_ontology | "The humanities is a group of disciplines that make use of qualitative analysis and analytic methods rather than scientific empirical methods. Branches of the humanities include law, philosophy, history, and so on (Appendix B)." |
| Q26 | 4 | input_ontology | "Mastering these subjects requires a variety of skills. For example, legal understanding requires knowledge of how to apply rules and standards to complex scenarios, and also provide answers with stipulations and explanations." |
| Q27 | 4 | input_ontology | "For philosophy, our questions cover concepts like logical fallacies, formal logic, and famous philosophical arguments. It also covers moral scenarios, including questions from the ETHICS dataset (Hendrycks et al., 2020) that test a model's understanding of normative statements through predicting widespread moral intuitions about diverse everyday scenarios." |
| Q28 | 4 | input_ontology | "Finally, our history questions cover a wide range of time periods and geographical locations, including prehistory and other advanced subjects." |
| Q29 | 4 | input_ontology | "Social science includes branches of knowledge that examine human behavior and society. Subject areas include economics, sociology, politics, geography, psychology, and so on." |
| Q30 | 4 | input_ontology | "Our economics questions include microeconomics, macroeconomics, and econometrics, and cover different types of problems, including questions that require a mixture of world knowledge, qualitative reasoning, or quantitative reasoning." |
| Q31 | 4 | input_ontology | "We also include important but more esoteric topics such as security studies in order to test the boundaries of what is experienced and learned during pretraining." |
| Q32 | 4 | input_ontology | "Social science also includes psychology, a field that may be especially important for attaining a nuanced understanding of humans." |
| Q33 | 4 | input_ontology | "STEM subjects include physics, computer science, mathematics, and more." |
| Q34 | 4 | input_ontology | "Conceptual physics tests understanding of simple physics principles and may be thought" |
| Q35 | 5 | output_form | "To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks." |
| Q36 | 5 | output_form | "We evaluate GPT-3 (Brown et al., 2020) and UnifiedQA (Khashabi et al., 2020)." |
| Q37 | 5 | output_form | "For GPT-3 we use the OpenAI API, which provides access to four model variants, "Ada," "Babbage," "Curie," and "Davinci," which we refer to as "Small" (2.7 billion parameters), "Medium" (6.7 billion), "Large" (13 billion) and "X-Large" (175 billion)." |
| Q38 | 5 | output_form | "UnifiedQA uses the T5 (Raffel et al., 2019) text-to-text backbone and is fine-tuned on previously proposed question answering datasets (Lai et al., 2017), where the prediction is the class with the highest token overlap with UnifiedQA's text output." |
| Q39 | 5 | output_form | "Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy." |
| Q40 | 5 | output_form | "We also fine-tune RoBERTa-base, ALBERT-xxlarge, and GPT-2 on UnifiedQA training data and our dev+val set." |
| Q41 | 5 | output_form | "We primarily focus on UnifiedQA and GPT-3 in the rest of this document, but additional discussion of RoBERTa, ALBERT, and GPT-2 is in Appendix A." |
| Q42 | 5 | output_form | "All values are percentages." |
| Q43 | 5 | output_form | "Some models proposed in the past few months can move several percent points beyond random chance." |
| Q44 | 5 | output_form | "GPT-3 uses few-shot learning and UnifiedQA is tested under distribution shift." |
| Q45 | 6 | input_form | "We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]." For zero-shot evaluation, we append the question to the prompt. For few-shot evaluation, we add up to 5 demonstration examples with answers to the prompt before appending the question. All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction." |
| Q46 | 6 | input_form | "For consistent evaluation, we create a dev set with 5 fixed few-shot examples for each subject." |
| Q47 | 6 | output_form | "We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%." |
| Q48 | 6 | output_form | "While the smaller models have around 25% zero-shot accuracy, Figure 10 in Appendix A shows that the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7%." |
| Q49 | 6 | output_form | "The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy." |
| Q50 | 6 | output_form | "We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy." |
| Q51 | 6 | output_form | "These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps." |
| Q52 | 6 | output_form | "Figure 6 shows the accuracy of GPT-3 (few-shot) and UnifiedQA for all 57 tasks. It shows the both models are below expert-level performance for all tasks, with GPT-3's accuracy ranging from 69% for US Foreign Policy to 26% for College Chemistry." |
| Q53 | 6 | output_form | "UnifiedQA does best on marketing, with an accuracy of 82.5%." |
| Q54 | 6 | output_ontology | "Overall, models do poorly on highly procedural problems. Figure 6 shows that calculation-heavy STEM subjects tend to have low accuracy compared to verbal subjects." |
| Q55 | 6 | output_ontology | "For GPT-3, 9 out of the 10 lowest-accuracy tasks are STEM subjects that emphasize mathematics or calculations. We speculate that is in part because GPT-3 acquires declarative knowledge more readily than procedural knowledge." |
| Q56 | 7 | input_ontology | "For example, many questions in Elementary Mathematics require applying the order of operations for arithmetic, which is described by the acronym PEMDAS (Parentheses Exponents Multiplication Division Addition Subtraction)." |
| Q57 | 7 | output_ontology | "We confirm that GPT-3 is aware of the acronym PEMDAS. However, it does not consistently apply PEMDAS to actual problems." |
| Q58 | 7 | output_ontology | "We find that some verbal tasks such as Moral Scenarios from Hendrycks et al. (2020) and Professional Law also have especially low accuracy." |
| Q59 | 7 | output_ontology | "GPT-3 does better on College Medicine (47.4%) and College Mathematics (35.0%) than calculation-heavy Elementary Mathematics (29.9%)." |
| Q60 | 7 | output_form | "We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject." |
| Q61 | 7 | output_form | "GPT-3 is uncalibrated. In fact, its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects." |
| Q62 | 7 | output_form | "Another calibration measure is the Root Mean Squared (RMS) calibration error (Hendrycks et al., 2019a; Kumar et al., 2019). Many tasks have miscalibrated predictions, such as Elementary Mathematics which has a zero-shot RMS calibration error of 19.4%." |
| Q63 | 7 | input_content | "A major distinction between our benchmark and previous multitask NLP benchmarks is that we do not require large training sets. Instead, we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet." |
| Q64 | 7 | input_form | "While text is capable of conveying an enormous number of concepts about the world, many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020). Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format." |
| Q65 | 8 | input_ontology | "This motivates us to propose a methodological change so that models are trained more like how humans learn." |
| Q66 | 8 | output_form | "For this reason we assess pretrained models in a zero-shot, few-shot, or transfer setting and we provide a dev, val, and test set for each task." |
| Q67 | 8 | output_form | "The dev set is used for few-shot prompts, the val set could be used for hyperparameter tuning, and the test set is used to compute the final accuracy." |
| Q68 | 8 | input_form | "Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining." |
| Q69 | 8 | output_content | "This has the benefit of obviating concerns about spurious training set annotation artifacts (Geirhos et al., 2020; Hendrycks et al., 2019b) and is in stark contrast to the previous paradigm of identically distributed training and test sets." |
| Q70 | 8 | output_form | "We find that current large-scale Transformers have wide room for improvement." |
| Q71 | 8 | output_ontology | "They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks." |
| Q72 | 8 | output_ontology | "Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics and many other STEM subjects with "plug and chug" problems." |
| Q73 | 8 | output_form | "Additionally, they do not match expert-level performance (90%) on any subject, so for all subjects it is subhuman." |
| Q74 | 8 | output_form | "On average, models are only now starting to move beyond random-chance accuracy levels." |
| Q75 | 8 | input_content | "We collected approximately 2,000 additional Professional Law training examples." |
| Q76 | 8 | output_form | "After fine-tuning a RoBERTa-base model (Liu et al., 2019) using this custom training set, our model attained 32.8% test accuracy." |
| Q77 | 8 | input_content | "We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law, but after fine-tuning it only attained 36.1% accuracy." |
| Q78 | 8 | output_form | "This suggests that while additional pretraining on relevant high quality text can help, it may not be enough to substantially increase the performance of current models." |
| Q79 | 8 | output_form | "It is unclear whether simply scaling up existing language models will solve the test." |
| Q80 | 8 | output_form | "Current understanding indicates that a 10× increase in model size must be accompanied by an approximate 5× increase in data (Kaplan et al., 2020)." |
| Q81 | 8 | input_content | "Data may also become a bottleneck, as there is far less written about esoteric branches of knowledge than about everyday situations." |
| Q82 | 8 | input_ontology | "We introduced a new test that measures how well text models can learn and apply knowledge encountered during pretraining." |
| Q83 | 8 | input_ontology | "By covering 57 subjects at varying levels of difficulty, the test assesses language understanding in greater breadth and depth than previous benchmarks." |
| Q84 | 8 | output_form | "We found that it has recently become possible for models to make meaningful progress on the test, but that state-of-the-art models have lopsided performance and rarely excel at any individual task." |
| Q85 | 8 | output_form | "We also showed that current models are uncalibrated and have difficulty with tasks that require calculations." |
| Q86 | 8 | output_ontology | "Worryingly, models also perform especially poorly on socially relevant subjects including morality and law." |
| Q87 | 9 | output_content | "DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship." |
| Q88 | 9 | output_content | "This research was also supported by the NSF Frontier Award 1804794." |
| Q89 | 11 | input_ontology | "This appendix includes figures with sorted results (Figure 9), few-shot examples vs. accuracy (Figure 10), and few-shot calibration (Figure 11). It also includes sections on fine-tuning, error analysis, and format sensitivity." |
| Q90 | 11 | output_form | "We primarily analyzed models with more than 10 billion parameters in the main body of the paper." |
| Q91 | 11 | input_ontology | "For this section, we analyze smaller models including RoBERTa-base (125 million parameters) (Liu" |
| Q92 | 11 | output_form | "On the left are GPT-3 few shot accuracies for all of the 57 tasks. On the right are UnifiedQA transfer accuracies for all of the 57 tasks. For both models, capabilities are lopsided." |
| Q93 | 12 | output_form | "Models are fine-tuned to predict one of four classes using the UnifiedQA MCQ questions and using our dev+val set. We test on our multitask test set." |
| Q94 | 12 | output_form | "RoBERTa-base attains an overall accuracy of 27.9%, with 27.9% accuracy for the humanities, 28.8% for social sciences, 27.0% for STEM, and 27.7% for other." |
| Q95 | 12 | output_form | "ALBERT-xxlarge attains an accuracy of 27.1%, with 27.2% accuracy for the humanities, 25.7% for the social sciences, 27.7% for STEM, and 27.9% for other." |
| Q96 | 12 | output_form | "GPT-2 attains an accuracy of 32.4%, with 32.8% accuracy for the humanities, 33.3% for the social sciences, 30.2% for STEM, and 33.1% for other." |
| Q97 | 12 | output_form | "Compare this to UnifiedQA's smallest variant, which has just 60 million parameters and approximately 29.3% accuracy. It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters." |
| Q98 | 12 | output_form | "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy." |
| Q99 | 12 | output_content | "We qualitatively analyze when GPT-3 makes high confidence mistakes. We find that while many of these mistakes were clearly wrong, many were mistakes that a human might make." |
| Q100 | 12 | input_form | "While different question formatting choices often lead to similar GPT-3 accuracies, we find that UnifiedQA is more sensitive." |
| Q101 | 12 | input_form | "UnifiedQA's input format is of the form QUESTION1 \\n (A) CHOICE1 (B) CHOICE2 (C) CHOICE3 (D) CHOICE4</s> where questions and choices are normalized and made lowercase." |
| Q102 | 12 | input_form | "If we remove the </s> from the input, accuracy declines by several percentage points." |
| Q103 | 13 | input_ontology | "We provide analysis of question length and difficulty in Figure 12. We list all tasks and the topics they test in Table 2. We also provide an example for each task starting with Figure 14." |
| Q104 | 13 | output_content | "Since language models train on vast text corpora, there is some chance that they have seen the exact question and answer during pretraining. If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. Likewise, a question's entropy would be especially low if it were memorized. Memorized questions and answers should have low entropy and" |
| Q105 | 13 | input_form | "For questions longer than a tweet (280 characters), the correlation between question length and true label confidence is slightly positive. This shows that longer questions are not necessarily harder." |
| Q106 | 13 | output_form | "While models are more calibrated in a few-shot setting than a zero-shot setting, they are still miscalibrated, with gap between accuracy and confidence reaching up to 14%. Here the correlation between confidence and accuracy is r = 0.81, compared to r = 0.63 in the zero-shot setting." |
| Q107 | 14 | output_content | "However, in Figure 13, we see that accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers." |
| Q108 | 14 | output_content | "This suggests that our exact questions were not memorized." |
| Q109 | 14 | input_content | "However, during pretraining models encountered text related to our questions through processing Wikipedia." |
| Q110 | 14 | input_content | "We also note that most of our questions came from PDFs or websites where questions and answers are on separate pages." |
| Q111 | 14 | output_content | "See Brown et al. (2020) for a previous discussion of contamination showing that the phenomena hardly affects performance." |
| Q112 | 14 | output_content | "To reduce the probability that future models encounter exact questions during test-time, we will provide a list of question sources." |
| Q113 | 14 | output_form | "The average log probability of the question (without answer) is not strongly positively correlated with accuracy, all else equal." |
| Q114 | 14 | output_form | "Each point corresponds to a task." |
| Q115 | 14 | output_form | "Higher log probability indicates higher compression, and especially high log probability would suggest memorization." |
| Q116 | 14 | output_form | "In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56." |
| Q117 | 15 | input_ontology | "Table 2: Summary of all 57 tasks." |
| Q118 | 16 | input_ontology | "Find all c in Z₃ such that Z₃[x]/(x² + c) is a field." |
| Q119 | 16 | input_ontology | "What is the embryological origin of the hyoid bone?" |
| Q120 | 16 | input_ontology | "Why isn't there a planet where the asteroid belt is located?" |
| Q121 | 16 | input_ontology | "Three contrasting tactics that CSO's can engage in to meet their aims are which typically involves research and communication, , which may involve physically attacking a company's operations or , often involving some form of ." |
| Q122 | 16 | input_ontology | "How many attempts should you make to cannulate a patient before passing the job on to a senior colleague?" |
| Q123 | 16 | input_ontology | "In a given population, 1 out of every 400 people has a cancer caused by a completely recessive allele, b. Assuming the population is in Hardy-Weinberg equilibrium, which of the following is the expected proportion of individuals who carry the b allele but are not expected to develop the cancer?" |
| Q124 | 16 | input_ontology | "Which of the following statements about the lanthanide elements is NOT true?" |
| Q125 | 17 | input_ontology | "Consider a computer design in which multiple processors, each with a private cache memory, share global memory using a single bus. This bus is the critical system resource. Each processor can execute one instruction every 500 nanoseconds as long as memory references are satisfied by its local cache. When a cache miss occurs, the processor is delayed for an additional 2,000 nanoseconds. During half of this additional delay, the bus is dedicated to serving the cache miss. During the other half, the processor cannot continue, but the bus is free to service requests from other processors. On average, each instruction requires 2 memory references. On average, cache misses occur on 1 percent of references. What proportion of the capacity of the bus would a single processor consume, ignoring delays due to competition from other processors?" |
| Q126 | 17 | input_ontology | "Let A be a real 2 × 2 matrix. Which of the following statements must be true? I. All of the entries of A2are nonnegative. II. The determinant of A2is nonnegative. III. If A has two distinct eigenvalues, then A2 has two distinct eigenvalues." |
| Q127 | 17 | input_ontology | "In a genetic test of a newborn, a rare genetic disorder is found that has X-linked recessive transmission. Which of the following statements is likely true regarding the pedigree of this disorder?" |
| Q128 | 17 | input_ontology | "One end of a Nichrome wire of length 2L and cross-sectional area A is attached to an end of another Nichrome wire of length L and cross- sectional area 2A. If the free end of the longer wire is at an electric potential of 8.0 volts, and the free end of the shorter wire is at an electric potential of 1.0 volt, the potential at the junction of the two wires is most nearly equal to" |
| Q129 | 17 | input_ontology | "Why is it that anti-virus scanners would not have found an exploitation of Heartbleed?" |
| Q130 | 17 | input_ontology | "A model airplane flies slower when flying into the wind and faster with wind at its back. When launched at right angles to the wind, a cross wind, its groundspeed compared with flying in still air is" |
| Q131 | 18 | input_ontology | "Consider the following AR(1) model with the disturbances having zero mean and unit variance yt = 0.2 + 0.4yt−1 + ut The (unconditional) mean of y will be given by (A) 0.2 (B) 0.4 (C) 0.5 (D) 0.33" |
| Q132 | 18 | input_ontology | "A point pole has a strength of 4π × 10−4 weber. The force in newtons on a point pole of 4π × 1.5 × 10−4 weber placed at a distance of 10 cm from it will be (A) 15 N. (B) 20 N. (C) 7.5 N. (D) 3.75 N." |
| Q133 | 18 | input_ontology | "A total of 30 players will play basketball at a park. There will be exactly 5 players on each team. Which statement correctly explains how to find the number of teams needed? (A) Add 5 to 30 to find 35 teams. (B) Divide 30 by 5 to find 6 teams. (C) Multiply 30 and 5 to find 150 teams. (D) Subtract 5 from 30 to find 25 teams." |
| Q134 | 18 | input_ontology | "Determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. E ⊃ (F · E) and ∼ E · F (A) Logically equivalent (B) Contradictory (C) Neither logically equivalent nor contradictory, but consistent (D) Inconsistent" |
| Q135 | 18 | input_content | "As of 2017, how many of the world's 1-year-old children today have been vaccinated against some disease? (A) 80% (B) 60% (C) 40% (D) 20%" |
| Q136 | 18 | input_ontology | "Homologous structures are often cited as evidence for the process of natural selection. All of the following are examples of homologous structures EXCEPT (A) the wings of a bird and the wings of a bat (B) the flippers of a whale and the arms of a man (C) the pectoral fins of a porpoise and the flippers of a seal (D) the forelegs of an insect and the forelimbs of a dog" |
| Q137 | 18 | input_ontology | "From the solubility rules, which of the following is true? (A) All chlorides, bromides, and iodides are soluble (B) All sulfates are soluble (C) All hydroxides are soluble (D) All ammonium-containing compounds are soluble" |
| Q138 | 19 | input_ontology | "A list of numbers has n elements, indexed from 1 to n. The following algorithm is intended to display the number of elements in the list that have a value greater than 100. The algorithm uses the variables count and position. Steps 3 and 4 are missing." |
| Q139 | 19 | input_ontology | "Which of the following could be used to replace steps 3 and 4 so that the algorithm works as intended?" |
| Q140 | 19 | input_content | "This question refers to the following information." |
| Q141 | 19 | input_content | "English Parliament, Act of Supremacy, 1534" |
| Q142 | 19 | input_ontology | "From the passage, one may infer that the English Parliament wished to argue that the Act of Supremacy would" |
| Q143 | 19 | input_ontology | "During the third stage of the demographic transition model, which of the following is true?" |
| Q144 | 20 | input_ontology | "Figure 37: A High School Government and Politics example." |
| Q145 | 20 | input_ontology | "Figure 38: A High School Macroeconomics example." |
| Q146 | 20 | input_ontology | "Figure 39: A High School Mathematics example." |
| Q147 | 20 | input_ontology | "Figure 40: A High School Microeconomics example." |
| Q148 | 20 | input_ontology | "Figure 41: A High School Physics example." |
| Q149 | 20 | input_ontology | "Figure 42: A High School Psychology example." |
| Q150 | 21 | input_ontology | "Figure 43: A High School Statistics example." |
| Q151 | 21 | input_content | "Figure 44: A High School US History example." |
| Q152 | 21 | input_ontology | "Figure 45: A High School World History example." |
| Q153 | 21 | input_ontology | "Figure 46: A Human Aging example." |
| Q154 | 22 | input_ontology | "Morning sickness is typically a problem: (A) during the first trimester (B) during the second trimester (C) during the third trimester (D) all through the pregnancy" |
| Q155 | 22 | input_ontology | "Would a reservation to the definition of torture in the ICCPR be acceptable in contemporary practice? (A) This is an acceptable reservation if the reserving country's legislation employs a different definition (B) This is an unacceptable reservation because it contravenes the object and purpose of the ICCPR (C) This is an unacceptable reservation because the definition of torture in the ICCPR is consistent with customary international law (D) This is an acceptable reservation because under general international law States have the right to enter reservations to treaties" |
| Q156 | 22 | input_ontology | "Which position does Rawls claim is the least likely to be adopted by the POP (people in the original position)? (A) The POP would choose equality above liberty. (B) The POP would opt for the 'maximin' strategy. (C) The POP would opt for the 'difference principle.' (D) The POP would reject the 'system of natural liberty.'" |
| Q157 | 22 | input_ontology | "John Stuart Mill: Each person's happiness is a good to that person, and the general happiness, therefore, a good to the aggregate of all persons. (A) Fallacy of Composition (B) Fallacy of Division (C) Gambler's Fallacy (D) Equivocation" |
| Q158 | 22 | input_ontology | "A 6-sided die is rolled 15 times and the results are: side 1 comes up 0 times; side 2: 1 time; side 3: 2 times; side 4: 3 times; side 5: 4 times; side 6: 5 times. Based on these results, what is the probability of side 3 coming up when using Add-1 Smoothing? (A) 2/15 (B) 1/7 (C) 3/16 (D) 1/5" |
| Q159 | 22 | input_ontology | "According to Lewin, Lippet and White's 1939 experiment, which form of leadership produced the most work from participants? (A) Laissez-faire (B) Democratic (C) Authoritarian (D) A mix of laissez-faire and democratic" |
| Q160 | 23 | input_form | "Figure 57: A Moral Scenarios example. The formatting of this task hinders UnifiedQA performance substantially." |
| Q161 | 24 | input_ontology | "According to Moore's "ideal utilitarianism," the right action is the one that brings about the greatest amount of: (A) pleasure. (B) happiness. (C) good. (D) virtue." |
| Q162 | 24 | input_ontology | "Researchers now believe that the decline of the Maya was caused chiefly by: (A) a cataclysm of some kind, such as an earthquake, volcano, or tsunami. (B) ecological degradation resulting from slash-and-burn farming techniques. (C) endless wars between neighboring Mayan city-states. (D) practices of interbreeding that led to a steep rise in congenital disorders." |
| Q163 | 24 | input_content | "Krete is an unmarried taxpayer with income exclusively from wages. By December 31, year 1, Krete's employer has withheld $16,000 in federal income taxes and Krete has made no estimated tax payments. On April 15, year 2, Krete timely filed for an extension request to file her individual tax return, and paid $300 of additional taxes. Krete's year 1 tax liability was $16,500 when she timely filed her return on April 30, year 2, and paid the remaining tax liability balance. What amount would be subject to the penalty for underpayment of estimated taxes? (A) $0 (B) $500 (C) $1,650 (D) $16,500" |
| Q164 | 24 | input_content | "The night before his bar examination, the examinee's next-door neighbor was having a party. The music from the neighbor's home was so loud that the examinee couldn't fall asleep. The examinee called the neighbor and asked her to please keep the noise down. The neighbor then abruptly hung up. Angered, the examinee went into his closet and got a gun. He went outside and fired a bullet through the neighbor's living room window. Not intending to shoot anyone, the examinee fired his gun at such an angle that the bullet would hit the ceiling. He merely wanted to cause some damage to the neighbor's home to relieve his angry rage. The bullet, however, ricocheted off the ceiling and struck a partygoer in the back, killing him. The jurisdiction makes it a misdemeanor to discharge a firearm in public. The examinee will most likely be found guilty for which of the following crimes in connection to the death of the partygoer? (A) Murder. (B) Involuntary manslaughter. (C) Voluntary manslaughter. (D) Discharge of a firearm in public." |
| Q165 | 25 | output_content | "Published as a conference paper at ICLR 2021" |
| Q166 | 25 | input_ontology | "Figure 63: A Professional Medicine example." |
| Q167 | 25 | input_ontology | "Figure 64: A Professional Psychology example." |
| Q168 | 25 | input_ontology | "Figure 65: A Public Relations example." |
| Q169 | 26 | input_ontology | "Figure 66: A Security Studies example." |
| Q170 | 26 | input_ontology | "Figure 67: A Sociology example." |
| Q171 | 26 | input_content | "Figure 68: A US Foreign Policy example." |
| Q172 | 26 | input_ontology | "Figure 69: A Virology example." |
| Q173 | 27 | input_ontology | "Figure 70: A World Religions example." |

---

## Regional Context

```yaml
name: South Asian Agricultural and Environmental Science — Mymensingh–Telangana–Andhra
  Pradesh Deployment
abbreviation: SA-AGRI-MYM
assessment_slug: mmlu/sa-agri-mym
scope_note: 'This region document is scoped to the specific deployment population
  described in the elicitation summary: an environmental scientist based in Mymensingh,
  Bangladesh, evaluating LLM agricultural and environmental science knowledge across
  three sub-regional agrarian contexts — the Brahmaputra-Jamuna delta near Mymensingh,
  dry-land cropping zones in Telangana, and coastal aquaculture in Andhra Pradesh.
  It is not a general South Asia or Bangladesh region document.'
primary_anchor:
  country: Bangladesh
  district: Mymensingh
  agro_ecological_zone: Brahmaputra-Jamuna floodplain / Old Brahmaputra floodplain
    (AEZ 9/10, Bangladesh classification)
  user_role: Environmental scientist and researcher; downstream population includes
    farmers and agronomists in Mymensingh district and Telugu-speaking agrarian communities
    in Telangana and Andhra Pradesh
secondary_contexts:
- state: Telangana
  country: India
  agro_ecological_focus: Deccan Plateau dry-land cropping; Rabi and Kharif systems
    on red and black cotton soils
  language_community: Telugu-speaking agrarian communities
- state: Andhra Pradesh
  country: India
  agro_ecological_focus: Coastal aquaculture; Krishna and Godavari delta coastal zones;
    saline-tolerant agriculture
  language_community: Telugu-speaking coastal farming and fishing communities
geopolitical_sensitivity:
  cross_border_issues:
  - Bangladesh–India water-sharing agreements (Ganges/Farakka Barrage, Teesta River)
  - Joint Rivers Commission (Bangladesh–India) — treaty status and current negotiations
  - Shared river basin management for the Brahmaputra-Jamuna system
  - Comparative farming policy divergence between Bangladesh and West Bengal
  note: Questions touching on shared river systems, water allocation, or comparative
    agricultural policy may have legitimately divergent correct answers depending
    on national or institutional perspective. Ground-truth labels derived from a single
    national context will not be authoritative for both sides of this deployment.
  active_treaties_and_agreements: 'Ganges Water Treaty (1996) remains in force; the
    current treaty expires December 2026, and both countries have agreed in principle
    to renew it, with formal negotiations pending the next elected Bangladeshi government
    (Source: TBS News, January 2026 — [WEB-1]).
    The Teesta water-sharing agreement has NO formal treaty as of May 2026: a 2011
    draft proposing 37.5% to Bangladesh and 42.5% to India was blocked by West Bengal''s
    Chief Minister and remains unsigned. Bangladesh''s interim government (led by
    Muhammad Yunus, since August 2024) has prioritised resuming Teesta talks, and
    Bangladesh is simultaneously pursuing a ~$1 billion Teesta river management project
    with China (POWERCHINA), with the Teesta Master Plan deadline extended to December
    2026 (Sources: Wikipedia — [WEB-2];
    South Asian Futures Fellowship — [WEB-3];
    TBS News — [WEB-4]).
    The Joint Rivers Commission remains active (met four times in 2024–2025 in Dhaka,
    Delhi, and Kolkata). This high geopolitical fluidity makes benchmark questions
    touching on Bangladesh–India water rights especially liable to produce nationally
    divergent correct answers.'
languages:
  primary_evaluation_languages:
  - Bangladeshi Bengali (Mymensingh dialect)
  - Standard Bangladeshi Bengali (written/formal)
  - Standard Indian Bengali (West Bengal variant)
  - Telugu
  - English (query/evaluation medium)
  dialect_notes:
    mymensingh_bengali: Mymensingh dialect (উত্তরবঙ্গীয়/ময়মনসিংহ আঞ্চলিক) has distinct
      phonological patterns and agricultural vocabulary absent from standard Bengali
      benchmarks. Local crop names, wetland terms, and land-tenure vocabulary differ
      from Dhaka-standard or Kolkata-standard Bengali.
    bengali_variant_divergence: Indian Bengali (West Bengal) and Bangladeshi Bengali
      share a script but diverge in register, vocabulary, and implicit cultural framing;
      benchmarks sourced from Indian materials may carry West Bengal stylistic defaults.
    telugu: Telugu is a Dravidian language with a distinct script (Telugu script);
      agricultural terminology for Deccan dry-land farming and coastal aquaculture
      is largely absent from English-language benchmarks.
  scripts:
  - Bengali script (বাংলা) — used for both Bangladeshi and Indian Bengali
  - Telugu script (తెలుగు)
  - Latin script (English evaluation medium)
  script_notes: Bengali and Telugu scripts require right-proper Unicode handling;
    neither has uppercase/lowercase distinctions in the Latin sense. MMLU's English-only
    ASCII/Unicode Latin input is a zero-compatibility baseline for both scripts.
  benchmark_language_mismatch: MMLU accepts English-only input. All regional-language
    evaluation (Bengali, Telugu) is entirely unsupported by the benchmark as designed.
  llm_bengali_evaluation_evidence: 'A 2025 arXiv paper (arXiv:2507.23248) evaluating
    LLMs'' multilingual capabilities for Bengali found that LLM accuracy in Bengali
    is generally lower than in English, with smaller models underperforming especially
    in Bengali. This confirms that even for standard Bengali (not Mymensingh dialect),
    current LLMs are meaningfully degraded relative to English baselines. No study
    specifically targeting Mymensingh-dialect Bengali or agricultural-domain Bengali
    was found. Source: arXiv 2507.23248 — [WEB-5]'
agro_ecological_zones:
  mymensingh_bangladesh:
    zone_classification: '[NEEDS VERIFICATION — deferred: below search budget; the
      BARC AEZ classification for Mymensingh district requires direct consultation
      of Bangladesh Agricultural Research Council AEZ maps or SRDI (Soil Resources
      Development Institute) documents, which were not returned by searches. The scaffold
      note of AEZ 9 Old Brahmaputra Floodplain or AEZ 21 Haor and Flood Basin remains
      the best available non-verified estimate.]'
    key_systems:
    - Boro rice cultivation (irrigated dry-season paddy, December–May)
    - Aman rice cultivation (monsoon-fed transplanted paddy, June–November)
    - Aus rice cultivation (pre-monsoon broadcast or transplanted)
    - Haor wetland seasonal flooding cycles
    - Char-land (riverine island) agriculture — highly dynamic, flood-prone
    - Beel (permanent wetland) fisheries and aquaculture
    soils: '[NEEDS VERIFICATION — deferred: below search budget; likely silty clay
      loam fluvial deposits based on general AEZ 9 descriptions, but specific Mymensingh
      district soil series require SRDI or FAO soil map consultation.]'
    flood_regime: '[NEEDS VERIFICATION — deferred: likely unsearchable at required
      sub-district precision; requires BWDB hydrological station data for the Old
      Brahmaputra floodplain near Mymensingh.]'
    key_institutions:
    - Bangladesh Rice Research Institute (BRRI) — Gazipur (near Mymensingh corridor)
    - Bangladesh Agricultural University (BAU) — Mymensingh
    - Bangladesh Agricultural Research Institute (BARI)
    - Department of Agricultural Extension (DAE), Mymensingh region
  telangana_india:
    zone_classification: '[NEEDS VERIFICATION — deferred: below search budget; ICAR
      agro-climatic zone classification for Telangana (likely Zone VI Semi-Arid Tropics/Deccan
      Plateau) requires direct ICAR document consultation.]'
    key_systems:
    - Rabi dry-land cropping (sorghum, chickpea, sunflower on black cotton soils)
    - Kharif cropping (cotton, soybean, maize, red gram)
    - Tank-fed irrigation systems (traditional cheruvu tanks)
    - Dryland horticulture (mango, banana in irrigated pockets)
    soils: '[NEEDS VERIFICATION — deferred: below search budget; Vertisols (black
      cotton soils) and Alfisols (red soils) are well-documented in the literature
      for the Deccan Plateau but district-specific Telangana data was not retrieved.]'
    rainfall_regime: '[NEEDS VERIFICATION — deferred: below search budget; average
      annual rainfall for Telangana dry-land zones typically cited as 700–1000 mm
      with unimodal distribution; sub-district variation requires ICAR-CRIDA or IMD
      data.]'
    key_institutions:
    - Professor Jayashankar Telangana State Agricultural University (PJTSAU)
    - ICRISAT — Patancheru, Hyderabad (semi-arid tropics research)
    - ICAR-Central Research Institute for Dryland Agriculture (CRIDA)
  andhra_pradesh_coastal_india:
    zone_classification: '[NEEDS VERIFICATION — deferred: below search budget; ICAR
      agro-climatic zone for coastal AP (Krishna-Godavari deltaic zone) requires direct
      ICAR document consultation.]'
    key_systems:
    - Brackishwater shrimp aquaculture (Penaeus vannamei, Penaeus monodon)
    - Freshwater fish culture (catla, rohu, mrigal — major carps)
    - Coastal saline agriculture and salt-tolerant rice varieties
    - Delta paddy cultivation (Krishna, Godavari deltas)
    soils: '[NEEDS VERIFICATION — deferred: below search budget; coastal alluvial
      and saline soil characterisation for AP aquaculture zones requires NBSS&LUP
      or ICAR-CIBA publications.]'
    key_institutions:
    - Central Institute of Brackishwater Aquaculture (CIBA) — Chennai (regional mandate)
    - ICAR-Central Marine Fisheries Research Institute (CMFRI)
    - Acharya NG Ranga Agricultural University (ANGRAU)
key_agricultural_terminology:
  bangladeshi_bengali_mymensingh_specific:
    wetland_terms:
    - হাওর (haor) — large bowl-shaped floodplain basin, seasonally inundated
    - বিল (beel) — permanent or semi-permanent freshwater wetland
    - চর (char) — riverine silt island, highly transient landform
    - বাঁওড় (baor) — oxbow lake
    rice_cultivation_terms:
    - বোরো (boro) — dry-season irrigated rice, winter-spring crop
    - আমন (aman) — wet-season transplanted or broadcast rice
    - আউশ (aus) — pre-monsoon rain-fed rice
    land_tenure_and_management:
    - জলমহাল (jalmohol) — government-leased water body for fisheries
    - খাস জমি (khas jomi) — government-owned fallow or vested land
    - বর্গাচাষ (borga chash) — sharecropping arrangement
    note: 'These terms are largely absent from standard Bengali NLP corpora and entirely
      absent from MMLU. Mymensingh dialect variants of these terms may differ from
      Dhaka-standard usage. [NEEDS VERIFICATION — deferred: likely unsearchable (lived
      practice); dialect-specific phonological or lexical variants for the Mymensingh
      region vs. standard Bangladeshi Bengali agricultural registers require in-region
      linguist or BAU faculty elicitation, not web search.]'
  telugu_agricultural_terms:
    note: 'A 2024/2025 study (Rajesh, Gupta, Immadisetty — ICICC 2024, published in
      Springer LNNS vol. 1039) explicitly documents that the agricultural domain ''has
      a lack of readily available resources, especially in regional languages'' and
      evaluates perplexity of language models on Telugu agricultural corpora, confirming
      sparse coverage. No publicly available Telugu-medium agricultural knowledge
      benchmark was found for Telangana or Andhra Pradesh-specific dry-land or aquaculture
      domains. Standard Telugu agricultural terminology for Kharif/Rabi dry-land crops
      and tank irrigation (cheruvu) in NLP corpora remains verified-scarce. Source:
      Springer — [WEB-6]'
literacy_and_education:
  bangladesh_national_literacy_rate: '77.9% (citizens aged 7 and above, 2024 BBS Bangladesh
    Economic Survey figure; up from 76.8% in 2023). The functional literacy rate (7+)
    as measured by BBS Literacy Assessment Survey 2023 is lower at 62.92%, with adult
    functional literacy (15+) at 60.77%. Caution: Bangladesh''s national literacy
    definition (ability to read, write, and do simple arithmetic) diverges from the
    international standard; researchers note the true rate may be lower under international
    criteria. Source: BBS Bangladesh Economic Survey 2024 (Observer BD — [WEB-7]);
    BBS Literacy Assessment Survey 2023 (Prothom Alo — [WEB-8])'
  mymensingh_district_literacy_rate: '[NOT FOUND — searched BBS publications and district-level
    reports; BBS publishes district-level data in Population and Housing Census volumes
    but the 2022 census data was not publicly indexed in retrievable form during this
    search. The national rural functional literacy rate (11–45 years) of 70.54% (BBS
    LAS 2023) is the closest available proxy for rural Mymensingh; actual district
    figure requires BBS district census tables. Source for proxy: Prothom Alo — [WEB-8]]'
  telangana_literacy_rate: '66.54% (2011 Census, the most recent full census available;
    male 74.95%, female 57.92%); NSO 2017–18 survey estimate is approximately 72.8%.
    Caveat: India has not conducted a national census since 2011; the 2021 census
    was delayed and remains unpublished as of May 2026, so no post-2018 official figure
    exists for Telangana. Sources: Government of Telangana Socio-Economic Outlook
    2018 cited in Testbook — [WEB-9];
    NSO 2017–18 data cited in SAARJ/Academicia 2022 — [WEB-10]'
  andhra_pradesh_literacy_rate: '67.02% (Census 2011); NSO 2017–18 estimate 66.4%
    (lowest among all Indian states; male 73.4%, female 59.5%). Same census caveat
    applies — no post-2021 official figure available. Sources: Census 2011 cited at
    census2011.co.in — [WEB-11];
    NSO 2017–18 in findeasy.in — [WEB-12]'
  agricultural_university_presence:
    bangladesh: Bangladesh Agricultural University (BAU), Mymensingh — primary higher
      education anchor for the deployment population
    telangana: 'PJTSAU — [NEEDS VERIFICATION — deferred: below search budget; campus
      locations and extension reach require PJTSAU official website consultation.]'
    andhra_pradesh: 'ANGRAU — [NEEDS VERIFICATION — deferred: below search budget;
      campus locations and extension reach require ANGRAU official website consultation.]'
  note: The primary user (environmental scientist) is university-educated; downstream
    farmer/agronomist population has variable formal education. Agricultural extension
    literacy in local languages is the operative threshold for that sub-population.
    Both Andhra Pradesh and Telangana have among India's lowest state literacy rates,
    sharpening concerns about the downstream farmer population's digital and print
    literacy for any LLM-assisted extension application.
infrastructure_notes:
  bangladesh_internet_penetration: '44.5% of total population (77.36 million users)
    at start of 2024 per DataReportal/Kepios analysis; the Bangladesh Telecommunication
    Regulatory Commission (BTRC) reported a higher mobile-subscription-based figure
    peaking at 80.6% in August 2024 (using a different denominator — mobile internet
    subscriptions relative to population, not unique users), declining to ~78.6% by
    October 2024. Wikipedia/Internet Live Stats puts 2025 internet users at ~82.8
    million (47%). These figures diverge due to methodological differences; the DataReportal/Kepios
    figure (unique users, 44.5%) is generally considered more conservative and reliable.
    Sources: DataReportal Digital 2024 Bangladesh — [WEB-13];
    New Age BD (BTRC data) — [WEB-14]'
  bangladesh_mobile_internet_penetration: 'Mobile internet dominates: approximately
    119.29 million mobile internet subscriptions as of 2025 (exceeds total population
    due to multi-SIM usage). Rural internet access increased from 28% in 2020 to an
    estimated 49% in 2025 per Wikipedia, though significant rural–urban gaps persist
    (urban ~78%). BBS Sample Vital Statistics 2023 reported 50.1% of persons aged
    15+ used the internet in 2023 (up from 45.5% in 2022). Mobile-first access is
    the dominant mode. Sources: Wikipedia Internet in Bangladesh — [WEB-15];
    BBS Sample Vital Statistics 2023 (BSS News) — [WEB-16]'
  india_telangana_andhra_internet_penetration: '[NEEDS VERIFICATION — deferred: below
    search budget; state-level figures for Telangana and Andhra Pradesh internet penetration
    were not returned by Bangladesh-focused searches. TRAI and NSSO data would be
    the authoritative sources. India''s national internet penetration is approximately
    50–55% as of 2023–2024 (ITU/World Bank), with rural–urban divides similar to Bangladesh
    patterns.]'
  device_profile: 'Mobile-first usage expected for farmer/agronomist population; researcher
    population likely has laptop/desktop access. Smartphone penetration in rural Bangladesh
    and rural Telangana differs substantially. Rural Bangladesh internet access approximately
    49% (2025 estimate) vs. urban 78%. [NEEDS VERIFICATION — deferred: below search
    budget; rural smartphone penetration rates specifically for Mymensingh district
    and Telangana agrarian districts require BTRC/TRAI sub-national data.]'
  connectivity_constraints: 'Low-bandwidth environments relevant for farmer-facing
    applications; not a primary constraint for the environmental scientist user but
    relevant to downstream deployment validity. Median mobile internet speed in Bangladesh:
    23.00 Mbps (January 2024, Ookla data). Source: DataReportal Digital 2024 Bangladesh
    — [WEB-13]'
  nlp_infrastructure_notes: 'AI4Bharat IndicBERT v1 (ALBERT-based) covers 12 Indian
    languages including Bengali and Telugu, pretrained on 9B tokens (120GB corpus);
    Telugu has good monolingual corpus representation. IndicBERT v2 (ACL 2023) covers
    20+ languages via the IndicXTREME benchmark (9 tasks across sentence classification,
    QA, NER, and retrieval). IndicTrans2 (2023, TMLR) provides machine translation
    for all 22 scheduled Indian languages including Telugu; its ILCI training data
    includes agriculture domain sentences across 16 languages. Bengali NLP: IndicBERT
    covers Indian Bengali; Bangladeshi Bengali and Mymensingh dialect are not explicitly
    covered by any of these frameworks. None of the above benchmarks include agricultural
    domain knowledge evaluation (agronomy, crop science, aquaculture) for Telugu or
    Bengali — they cover general NLU tasks. Sources: AI4Bharat IndicBERT GitHub —
    [WEB-17]; IndicTrans2 OpenReview — [WEB-18];
    AI4Bharat IndicNLP Resources — [WEB-19]'
cultural_and_institutional_norms:
  bangladesh: Agricultural knowledge in Bangladesh is institutionally anchored in
    BRRI, BARI, and BAU extension networks. Farmer practice is shaped by seasonal
    flood calendars, not Western-academic agronomy defaults. Community-level water
    management (khals, sluice gates) involves collective decision-making. Government
    agricultural extension (DAE) is a primary knowledge channel. Islamic calendar
    influences cropping scheduling in some communities.
  telangana_andhra: Deccan dry-land farming communities have centuries-old tank irrigation
    traditions (cheruvu system) that differ from canal-irrigation assumptions in national-level
    Indian agricultural policy. Telugu-medium extension communication is standard;
    Hindi or English-medium content faces uptake barriers in rural contexts. Farmer
    Producer Organizations (FPOs) and ICRISAT-linked programs are key knowledge intermediaries.
  cross_border_sensitivity: Hydrological and agricultural policy questions that span
    the Bangladesh–India border (Teesta, Ganges, Brahmaputra basin management) carry
    geopolitical charge. Responses calibrated to Indian government policy positions
    may be received as politically biased by Bangladeshi scientists and vice versa.
    Benchmark ground-truth labels that embed one national perspective without flagging
    this are validity risks. The political context has intensified since August 2024
    (fall of Sheikh Hasina government) and Bangladesh's pivot toward China on Teesta
    management adds further geopolitical complexity to any cross-border agricultural
    water-sharing questions.
regulatory_and_policy_context:
  bangladesh:
    primary_agricultural_policy: '[NEEDS VERIFICATION — deferred: below search budget;
      current Bangladesh National Agriculture Policy and active 5-year plan provisions
      for flood-plain farming require Ministry of Agriculture official portal consultation.]'
    water_management_framework: '[NEEDS VERIFICATION — deferred: below search budget;
      Bangladesh Water Act and BWDB regulatory mandate for haor and floodplain zones
      require official legal text consultation.]'
    seeds_and_varieties_regulation: '[NEEDS VERIFICATION — deferred: below search
      budget; BADC and BRRI variety release process and protected variety status require
      institutional publication review.]'
  india_telangana_andhra:
    agricultural_policy: '[NEEDS VERIFICATION — deferred: below search budget; Telangana
      and Andhra Pradesh state agricultural policy frameworks and PM-KISAN provisions
      require state government portal consultation.]'
    aquaculture_regulation: '[NEEDS VERIFICATION — deferred: below search budget;
      Coastal Aquaculture Authority (CAA) Act provisions for AP shrimp farming and
      EIA requirements require Ministry of Fisheries/CAA official text.]'
    water_rights: '[NEEDS VERIFICATION — deferred: below search budget; Andhra Pradesh
      and Telangana water allocation post-bifurcation and Krishna/Godavari River Management
      Board mandates require tribunal order and ministry report consultation.]'
  cross_border:
    ganges_water_treaty: '1996 Ganges Water Sharing Treaty remains active; current
      treaty expires December 2026. Joint River Commission sources confirm both countries
      have agreed in principle to renew; formal negotiations pending elected Bangladeshi
      government. Engineers from both countries are currently monitoring flows at
      Farakka (Bangladesh engineers) and Hardinge Bridge (Indian engineers) per the
      treaty''s joint monitoring provisions. Source: TBS News, January 2026 — [WEB-1]'
    teesta_agreement: 'No formal treaty exists. The 2011 draft (37.5% Bangladesh /
      42.5% India) was blocked by West Bengal CM Mamata Banerjee and remains unsigned.
      Bangladesh''s Yunus-led interim government (since August 2024) has expressed
      commitment to restarting talks. Bangladesh is simultaneously pursuing a Chinese-financed
      Teesta River Comprehensive Management and Restoration Project (~$1B, POWERCHINA);
      the Teesta Master Plan deadline is extended to December 2026. West Bengal CM
      (as of June 2025) has reiterated opposition to any Teesta sharing deal without
      state government involvement. This remains one of the most active and unresolved
      cross-border water disputes in South Asia. Sources: Wikipedia — [WEB-2];
      TBS News (Teesta Master Plan) — [WEB-4];
      PMF IAS — [WEB-20]'
    joint_rivers_commission: 'Bangladesh–India Joint Rivers Commission (JRC) constituted
      in 1972. Remained active through 2024–2025 political turbulence; held meetings
      in Dhaka (×2), Delhi, and Kolkata in 2024–2025. The 2022 Kushiyara River Agreement
      (signed at the 38th JRC meeting) is the most recent bilateral water agreement,
      allowing Bangladesh to withdraw 153 cusecs via Rahimpur Canal for Sylhet irrigation.
      Source: TBS News — [WEB-1];
      Water Diplomat — [WEB-21]'
benchmark_validity_summary:
  benchmark: mmlu
  overall_fitness: Very low for this deployment. MMLU is English-only, US/Western-institution-anchored,
    and contains no agro-ecological, delta-ecology, or South Asian regional agricultural
    content. Multilingual input (Bengali, Telugu) is entirely unsupported. Ground-truth
    labels have no South Asian agronomic validation. The benchmark may serve only
    as a weak general-science baseline for cross-model comparison.
  dimension_fitness:
    input_ontology: Very low — 57-subject taxonomy contains no haor ecology, delta
      farming, dry-land Deccan cropping, or South Asian agro-ecology subjects.
    input_content: Very low — all content sourced from US standardized exams and Anglophone
      university materials; no BRRI, BARI, ICAR, or Telugu-medium agricultural content.
    input_form: Zero — English-only text input; Bengali and Telugu scripts unsupported.
    output_ontology: Low — four-option MCQ schema cannot encode regionally contingent
      correct answers or cross-border policy divergence.
    output_content: Very low — no South Asian annotators documented; US MTurk worker
      baseline irrelevant to agronomic knowledge standards.
    output_form: Partial — MCQ accuracy metric is usable for baseline cross-model
      comparison but cannot capture open-ended agronomic reasoning.
flagged_gaps_for_web_search:
- gap_id: 1
  topic: Mymensingh dialect Bengali agricultural NLP corpora
  search_target: Mymensingh Bengali dialect NLP corpus agricultural terminology haor
    boro aman Bangladeshi Bengali language model benchmark evaluation BNLP BanglaLM
  search_result_summary: '[NOT FOUND — no NLP corpus or benchmark specifically targeting
    Mymensingh-dialect Bengali agricultural terminology was identified. The IndicBERT/IndicGLUE
    ecosystem covers Indian Bengali but not Bangladeshi Bengali dialect variants.
    The BNLP toolkit (referenced in AI4Bharat NLP catalog — [WEB-22])
    provides general Bangladeshi Bengali NLP tools but no agricultural domain or dialect-specific
    corpus. This null result confirms a genuine documentation gap.]'
- gap_id: 2
  topic: Telugu-medium agricultural and environmental science benchmarks
  search_target: Telugu language agricultural benchmark LLM evaluation AI4Bharat IndicGLUE
    IndicBERT Telangana Andhra Pradesh dry-land farming aquaculture Dravidian NLP
    agri domain
  search_result_summary: No Telugu-specific agricultural or environmental science
    LLM benchmark was found. A 2024 conference paper (ICICC 2024, Springer LNNS vol.
    1039 — [WEB-6]) explicitly identifies
    the lack of agricultural domain resources for Telugu and compares language model
    perplexity on Telugu agricultural corpora, but does not produce a reusable benchmark.
    AI4Bharat's IndicGLUE and IndicXTREME benchmarks cover Telugu for general NLU
    tasks (QA, sentiment, NER) but contain no agricultural domain evaluation. This
    is a confirmed gap.
- gap_id: 3
  topic: Haor and floodplain ecology subject coverage in existing benchmarks
  search_target: haor wetland Bangladesh LLM benchmark floodplain ecology South Asian
    agricultural NLP evaluation boro rice char-land farming BRRI BAU dataset
  search_result_summary: '[NOT FOUND — no LLM benchmark or NLP evaluation dataset
    covering haor wetlands, boro rice systems, char-land farming, or Brahmaputra-Jamuna
    floodplain ecology was identified. The AgriPriceBD dataset (arXiv 2604.06227 —
    [WEB-23]) is the only Bangladesh-specific agricultural
    ML dataset found; it covers commodity price forecasting (garlic, chickpea, green
    chilli, cucumber, sweet pumpkin) and does not address agro-ecological or production-system
    knowledge. This confirms the assessment that haor/floodplain ecology is entirely
    absent from the LLM benchmark landscape.]'
- gap_id: 4
  topic: Cross-border Bangladesh–India agri-policy answer divergence in benchmarks
  search_target: Bangladesh India water sharing Ganges Teesta Farakka benchmark annotation
    LLM evaluation cross-border agricultural policy regional answer divergence geopolitical
    NLP
  search_result_summary: '[NOT FOUND — no LLM benchmark or NLP annotation methodology
    was found that explicitly handles cross-border Bangladesh–India water-sharing
    or agricultural policy questions with nationally divergent correct answers. The
    geopolitical validity risk documented in this region document (competing correct
    answers depending on national perspective) is unaddressed in any known benchmark.
    Searches confirmed the Teesta dispute is actively unresolved as of 2025, heightening
    this risk.]'
- gap_id: 5
  topic: Sub-national India agro-climatic zone granularity in LLM benchmarks
  search_target: India sub-national state-level agricultural benchmark LLM Telangana
    Andhra Pradesh agro-climatic zone ICAR IndicNLU regional knowledge evaluation
  search_result_summary: '[NOT FOUND — IndicGLUE, IndicXTREME, and BharatBench (Krutrim,
    2024) evaluate general NLU capabilities for Indian languages but contain no sub-national
    state-level or agro-climatic zone-specific agricultural knowledge tasks. BharatBench
    references the Indic QA Benchmark (multilingual QA for Indic languages) but no
    agricultural domain or state-specific content was documented. Source consulted:
    BharatBench report — [WEB-24]]'
- gap_id: 6
  topic: Region-specific LLM evaluation infrastructure for Bangladeshi Bengali and
    South Indian languages
  search_target: BanglaLM Mukherjee Bengali LLM agricultural domain evaluation IndicBERT
    South Indian language model benchmark comparison frontier vs regional models Bangladesh
  search_result_summary: AI4Bharat IndicBERT v2 (ACL 2023 — [WEB-25])
    is the leading multilingual Indic NLU model, covering 20+ languages including
    Bengali and Telugu via IndicXTREME. A 2025 arXiv paper (arXiv:2507.23248 — [WEB-5])
    benchmarks multiple LLMs on Bengali NLU tasks and finds consistent Bengali performance
    degradation relative to English. No agricultural-domain-specific Bengali or Telugu
    LLM evaluation infrastructure was found. The IndicTrans2 system (TMLR 2023 — [WEB-18])
    includes agriculture-domain sentences from ILCI data in its MT training, but this
    is a translation system, not a knowledge evaluation benchmark.
- gap_id: 7
  topic: Existing South Asian agricultural knowledge evaluation datasets
  search_target: South Asian agricultural NLP dataset knowledge assessment Bangladesh
    India crop soil climate LLM evaluation agronomy environmental science benchmark
    2022 2023 2024
  search_result_summary: 'Two relevant resources found: (1) AgriPriceBD (arXiv 2604.06227,
    March 2026 — [WEB-23]): first publicly available daily
    multi-commodity retail price dataset for Bangladesh (5 commodities, 2020–2025);
    addresses price forecasting, not agricultural knowledge evaluation. (2) A 2025
    arXiv paper (arXiv:2507.16974 — [WEB-26]) creates
    synthetic agricultural QA pairs (60,130 pairs) in English, Hindi, and Punjabi
    using IndicTrans2, with human evaluation; explicitly notes that ''agriculture-specific
    QA datasets are only for high-resource languages such as English, German and Chinese,''
    confirming no Telugu or Bangladeshi Bengali agricultural QA dataset exists. Both
    papers reinforce the absence of domain-specific South Asian agricultural NLP evaluation
    resources.'
- gap_id: 8
  topic: Bangladesh Rice Research Institute (BRRI) and BARI publication corpora availability
    for LLM evaluation
  search_target: BRRI BARI Bangladesh Rice Research Institute publication corpus Bengali
    NLP pretraining LLM agricultural domain knowledge dataset availability
  search_result_summary: '[NOT FOUND — no publicly accessible BRRI or BARI publication
    corpus suitable for NLP pretraining or LLM evaluation was identified through web
    search. BRRI and BARI publish technical bulletins and variety release documents
    in Bengali and English, but these do not appear to be available as structured
    NLP-ready datasets. This is a confirmed documentation gap that would require direct
    institutional collaboration with BRRI/BARI to address.]'
net_new_fields:
  teesta_river_agricultural_significance: 'The Teesta River irrigates approximately
    14% of Bangladesh''s total cropped area and is vital for cultivating Boro rice
    (Bangladesh''s largest crop), with the Teesta Barrage Project irrigating 540,000
    hectares across seven districts. Water shortages from India''s upstream withdrawals
    at Gazoldoba cost Bangladesh approximately 1.5 million tons of rice annually (IFPRI
    estimate). This makes Teesta water allocation directly load-bearing for boro rice
    yield estimation questions — a core agro-ecological topic for the deployment.
    Source: Social Science Journal 2025 — [WEB-27];
    Wikipedia Teesta Water Dispute — [WEB-2]'
  agriprice_bd_dataset: 'AgriPriceBD (arXiv 2604.06227, March 2026) is the first publicly
    available daily multi-commodity retail price dataset for Bangladesh, covering
    five commodities over 2020–2025, constructed via LLM-assisted parsing of government
    market monitoring PDFs. While not an agricultural knowledge benchmark, it confirms
    that LLM-assisted pipelines can successfully process Bengali-language government
    agricultural reports — a methodological precedent for future BRRI/BARI corpus
    digitisation. It also documents that existing forecasting architectures (Informer,
    Prophet) fail on Bangladeshi agricultural price data, underscoring data-scarcity
    and domain-mismatch challenges. Source: arXiv — [WEB-23]'
  synthetic_agri_qa_hindi_punjabi: 'A 2025 paper (arXiv:2507.16974) demonstrates that
    synthetic agricultural QA datasets can be generated at scale (60,130 pairs) for
    Indian languages using IndicTrans2, with human evaluation finding that LLM-as-judge
    metrics are inadequate for domain- and country-specific agricultural QA evaluation.
    The method covers Hindi and Punjabi but not Telugu or Bengali, and explicitly
    notes the absence of agricultural QA datasets for regional Indian languages —
    directly relevant to the deployment''s gap analysis. Source: arXiv — [WEB-26]'
  indic_nlp_general_benchmark_note: 'AI4Bharat''s IndicXTREME (ACL 2023) is the most
    comprehensive multilingual Indic NLU benchmark, covering 9 tasks across 20 languages
    including Bengali and Telugu (IndicQA, IndicSentiment, IndicCOPA, etc.). It does
    not include agricultural domain evaluation. IndicBERT v2 achieves state-of-the-art
    results on these tasks but its Bengali coverage is weighted toward Indian Bengali
    (West Bengal) rather than Bangladeshi Bengali; the Mymensingh dialect is unrepresented.
    Source: ACL Anthology — [WEB-25]'
  kushiyara_river_agreement_2022: 'The 2022 Kushiyara River Agreement (signed at the
    38th JRC meeting) is the most recent Bangladesh–India bilateral water agreement;
    it allows Bangladesh to withdraw 153 cusecs via Rahimpur Canal for Sylhet agriculture
    during the lean season. This incremental agreement is cited as a possible model
    for Teesta governance. Its existence confirms that Bangladesh–India river agreements
    are alive and evolving, meaning benchmark questions about bilateral water agreements
    will require up-to-date factual grounding. Source: Water Diplomat — [WEB-21]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.tbsnews.net/foreign-policy/bangladeshi-indian-engineers-monitor-water-flows-under-ganges-water-sharing-treaty |
| WEB-2 | https://en.wikipedia.org/wiki/Teesta_Water_Dispute |
| WEB-3 | https://www.southasianfuturesfellowship.org/analysis-2/the-future-of-the-teesta-river-project-amidst-new-developments-in-bangladesh:-a-geopolitical-quagmire |
| WEB-4 | https://www.tbsnews.net/features/panorama/teesta-master-plan-and-longstanding-bangladesh-india-water-politics-1072696 |
| WEB-5 | https://arxiv.org/pdf/2507.23248 |
| WEB-6 | https://doi.org/10.1007/978-981-97-4152-6_38 |
| WEB-7 | https://www.observerbd.com/news/542998 |
| WEB-8 | https://en.prothomalo.com/bangladesh/c7axno0vhh |
| WEB-9 | https://testbook.com/question-answer/what-is-the-literacy-rate-of-telangana--5efeb788fbc9b00d102b5fda |
| WEB-10 | https://saarj.com/wp-content/uploads/paper/ACADEMICIA/2022/FULL-PDF/ACADEMICIA-AUGUST-2022/8.15,%20Khritish%20Swargiary.pdf |
| WEB-11 | https://www.census2011.co.in/census/state/andhra+pradesh.html |
| WEB-12 | https://www.findeasy.in/indian-states-by-literacy-rate/ |
| WEB-13 | https://datareportal.com/reports/digital-2024-bangladesh |
| WEB-14 | https://www.newagebd.net/post/telecom/252740/internet-penetration-rate-declines |
| WEB-15 | https://en.wikipedia.org/wiki/Internet_in_Bangladesh |
| WEB-16 | https://www.bssnews.net/news/180472 |
| WEB-17 | https://github.com/AI4Bharat/IndicBERT |
| WEB-18 | https://openreview.net/forum?id=vfT4YuzAYA |
| WEB-19 | https://indicnlp.ai4bharat.org/pages/indicnlp-resources/ |
| WEB-20 | https://www.pmfias.com/teesta-water-sharing-with-bangladesh/ |
| WEB-21 | https://www.waterdiplomat.org/story/2025/08/teesta-river-politics-and-benefit-sharing-getting-yes-without-grand-bargain |
| WEB-22 | https://ai4bharat.github.io/indicnlp_catalog/ |
| WEB-23 | https://arxiv.org/abs/2604.06227 |
| WEB-24 | https://ai-labs.olakrutrim.com/static/Bharatbench-report-4thfeb.pdf |
| WEB-25 | https://aclanthology.org/2023.acl-long.693 |
| WEB-26 | https://arxiv.org/html/2507.16974v2 |
| WEB-27 | https://www.socialsciencejournal.in/assets/archives/2025/vol11issue2/11026.pdf |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Your deployment targets agricultural and environmental science knowledge across South Asian regions — including flood-plain farming in the Brahmaputra-Jamuna delta near Mymensingh, dry-land cropping in Telangana, or coastal aquaculture in Andhra Pradesh. Does the benchmark's subject coverage adequately represent the agro-ecological, soil, crop, and climate-specific knowledge your scientist actually needs, or are those agricultural subdomains largely absent from the benchmark's subject taxonomy?
A1: The benchmark contains only surface-level agricultural knowledge about parts of India; depth-level subject knowledge for the specific agro-ecological subdomains (delta flood-plain farming, haor wetland ecology, dry-land Telugu region cropping) is largely absent from MMLU's subject taxonomy.

Q2 [IC]: Your deployment involves Bengali as spoken in Mymensingh — a dialect with distinct vocabulary and phonological patterns. Would benchmark content reflect standard or Indian-leaning Bengali rather than Bangladeshi/Mymensingh variants? Would dialect-specific agricultural terminology (local crop names, land-tenure terms, irrigation vocabulary) be represented?
A2: The benchmark content defaults to fairly standard Bengali wording with possible implicit Indian Bengali stylistic leanings; dialect-specific agricultural terminology from the Mymensingh/Bangladeshi context is absent, and including it would make the benchmark more robust.

Q3 [OC]: For agricultural and environmental science questions relevant to Bangladesh — haor wetland ecology, boro rice cultivation cycles, flood management under Bangladesh's river systems — would answer keys derived from a non-Bangladeshi annotation context be considered authoritative by Mymensingh-based scientists? Are there cases where the correct answer for a Bangladeshi context would differ from the benchmark's marked answer?
A3: There is potential for divergent correct answers, particularly around cross-border water-sharing agreements and associated geopolitical sentiment between Bangladesh and India — those differing perspectives should be captured gracefully. Indian-exam-derived answers would be considered authoritative in some limited cases, but the core concern is that agricultural and practice differences between regions are not adequately captured or differentiated in ground-truth labels.

Q4 [IF]: Will LLMs being evaluated receive queries in regional South Asian languages, in English, or a mix? Is the Mymensingh scientist expected to query in standard Bengali script, colloquial Bangladeshi Bengali, or English?
A4: Queries should include Indian regional languages (notably Telugu) as well as Bengali in both its Indian and Bangladeshi varieties — the evaluation is explicitly multilingual and not English-only, which is a direct mismatch with MMLU's English-only input design.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MMLU's 57-subject taxonomy has no dedicated agro-ecological or South Asian regional agricultural subdomains; depth-level coverage of delta farming, haor ecology, or Telugu dry-land cropping is confirmed absent by the user. |
| IC | HIGH | Benchmark content carries US/Western defaults and lacks Bangladeshi or Telugu regional agricultural terminology, crop names, land-tenure vocabulary, and delta-specific environmental concepts confirmed missing by the user. |
| IF | HIGH | The deployment explicitly requires multilingual queries (Telugu, Bangladeshi Bengali, Indian Bengali) whereas MMLU is English-only text input — a direct modality/language mismatch confirmed by the user. |
| OO | HIGH | MMLU's output taxonomy (MCQ label selection across generic subjects) does not map onto region-specific agricultural knowledge assessment; legitimate pluralism exists in cross-border agronomic and water-management practice interpretations. |
| OC | HIGH | Ground-truth labels were not validated by South Asian or Bangladeshi agronomists; the user confirms that cross-border water/agricultural agreement questions could yield divergent correct answers depending on national perspective, and that practice differences are not reflected in answer keys. |
| OF | MODERATE | MMLU's MCQ label output format partially aligns with evaluation needs, but the deployment may benefit from open-ended generation to capture nuanced agricultural practice differences; the user did not specifically flag output form as a primary concern. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** cais/mmlu (57 subject configurations)
**Analysis date:** 2025-07-29
**Examples reviewed:** ~175 examples across 37 configs sampled (approximately 5 per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | cais/mmlu | moral_scenarios Ex1 | A | "For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**?" | Question explicitly frames moral standards as US-specific, 2020 vintage | OC |
| D2 | cais/mmlu | high_school_us_history Ex1 | A | "The song, and the movement that it was connected to, highlight which of the following developments in the broader society in the late 1800s?" (re: "The Hayseed", US Populist movement) | US-specific historical content with no South Asian relevance | IO, IC |
| D3 | cais/mmlu | high_school_government_and_politics Ex1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | Entirely US constitutional law content | IO, IC |
| D4 | cais/mmlu | high_school_government_and_politics Ex4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president." | US-specific legislative history | IO |
| D5 | cais/mmlu | us_foreign_policy Ex4 | D | "In American government, the power to declare war rests with Congress." | US government structure; no relevance to South Asian governance or environmental policy | IO |
| D6 | cais/mmlu | us_foreign_policy Ex3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy?" | US Cold War policy — no South Asian agro-ecological relevance | IO |
| D7 | cais/mmlu | professional_law Ex1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs. The logs were being sold by a lumber company… the girl was struck by the tractor-trailer and was seriously injured." | US tort law scenario — US legal context | IO, IC |
| D8 | cais/mmlu | professional_law Ex2 | B | "An avid baseball fan learned that a local professional baseball club was conducting a baseball camp… forwarded the club a $50 registration deposit" | US contract law — US sports/cultural context | IC |
| D9 | cais/mmlu | human_aging Ex3 | C | "The age at which one can receive full benefits from social security" with answer "Has been increasing" | US Social Security system — entirely US institutional context | IC, OC |
| D10 | cais/mmlu | human_sexuality Ex1 | A | "Which of the following is the most common method of birth control for married couples in the **U.S.**" | Explicitly US demographic data | IC, OC |
| D11 | cais/mmlu | human_sexuality Ex5 | A | "From 1988 to 1990 among heterosexuals in the **US**, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" | US-specific behavioral survey data | IC, OC |
| D12 | cais/mmlu | moral_scenarios Ex2–5 | B/C/D/A | "For which of these two scenarios does the main character … do something clearly morally wrong, according to ordinary moral standards in the US as of 2020?" (repeated framing across all 5 examples) | Every moral_scenarios question frames correctness relative to US 2020 norms | OC, OO |
| D13 | cais/mmlu | global_facts Ex2 | B | "As of 2017, what fraction of the population in **India** used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%" | South Asia-referenced factual question, but static 2017 statistic | IC |
| D14 | cais/mmlu | global_facts Ex1 | A | "About what percentage of survey respondents from **China** report having paid a bribe in the last year to access public services … as of 2017?" | Global factual question but no South Asian agricultural content | IC |
| D15 | cais/mmlu | business_ethics Ex5 | A | "in many other countries, such as **Russia** and **China** civil society is far less developed than in, for instance, **Britain**" | Western-normative framing of civil society development | IC |
| D16 | cais/mmlu | high_school_european_history Ex1 | A | "The Scribbling-Machines have thrown thousands of your petitioners out of employ… Leeds Woolen Workers Petition, 1786" | Entirely European industrial history — no South Asian relevance | IO |
| D17 | cais/mmlu | high_school_european_history Ex2 | B | "What is tolerance?… Of all religions, the Christian ought doubtless to inspire the most tolerance… Voltaire, Letters on the English Nation, 1733" | European Enlightenment philosophy — no South Asian agricultural relevance | IO, IC |
| D18 | cais/mmlu | high_school_world_history Ex2 | B | "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters… British journalist William Howard Russell, My Indian Mutiny Diary, 1860" | British colonial framing of Indian history | IC, OC |
| D19 | cais/mmlu | high_school_geography Ex3 | C | "The way of life based on breeding and herding of animals that is used as a source of food, shelter, and clothing is called pastorialism" | Generic geography — no delta/wetland/aquaculture content | IO |
| D20 | cais/mmlu | high_school_geography Ex5 | A | "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric **zone model of urban form**?" | US urban planning model (Burgess model, Chicago School) | IC |
| D21 | cais/mmlu | nutrition Ex1–5 | various | "Which of the following inborn errors of metabolism gives rise to zinc deficiency?"; "What characteristic is not representative of a type IIb muscle fibre?" | Clinical/biochemical nutrition — no South Asian food system or crop nutrition content | IO |
| D22 | cais/mmlu | college_biology Ex1 | A | "In fungi, cell walls are reinforced by which of the following? (A) Chitin (B) Silica (C) Lignin (D) Collagen fibers" | General biology — not agricultural/agro-ecological | IO |
| D23 | cais/mmlu | high_school_biology Ex4 | D | "Which describes an African butterfly species that exists in two strikingly different color patterns?" | Biology question with African species reference — no South Asian agricultural relevance | IO |
| D24 | cais/mmlu | security_studies Ex1 | A | "In what ways do theories of conventional and critical social constructivism differ?" | Western IR theory — no South Asian environmental/agricultural policy content | IO |
| D25 | cais/mmlu | jurisprudence Ex1 | A | "Bill purchased a can of Sipep from the Ajax Minimart. After he finished drinking the Sipep, Bill noticed that the can contained dead insects stuck on the inside bottom of the can. In a strict product liability tort action against Ajax, Bill must prove…" | US-style product liability tort — US legal culture | IO, IC |
| D26 | cais/mmlu | sociology Ex3 | C | "Smith & Tomlinson argued that school character far outweighed ethnic background in determining educational success" | UK-centric sociological research | IC |
| D27 | cais/mmlu | international_law Ex4 | D | "Cultural relativism posits that local culture should validate the existence and practice of all human rights" | International law question — some nominal global relevance, but no South Asian agricultural law content | IO |
| D28 | cais/mmlu | high_school_macroeconomics Ex1–5 | various | "If firms that make a particular product expect its price will be lower in the future, this will cause the supply of the product to increase right now." | Generic macroeconomics — no South Asian agricultural market or agri-policy content | IO |
| D29 | cais/mmlu | elementary_mathematics Ex1 | A | "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" | US units (miles per hour) — not metric; minor cultural assumption | IC |
| D30 | cais/mmlu | high_school_statistics Ex1 | A | "The Department of Health plans to test the lead level in a specific park. Because a high lead level is harmful to children, the park will be closed if the lead level exceeds the allowed limit." | Environmental testing question, but no South Asian or agricultural context | IO |
| D31 | cais/mmlu | professional_medicine Ex2 | B | "A 31-year-old man with a 5-year history of HIV infection comes to the office because of anal pain… He says he and his partner engage in anal-receptive intercourse." | US clinical medicine scenario — Western clinical context | IC |
| D32 | cais/mmlu | college_chemistry Ex5 | A | "A substance that is NOT generally considered to be a toxic pollutant in water is (A) carbonic acid (B) a halogenated hydrocarbon (C) lead (D) mercury" | Closest approach to environmental science — but generic water chemistry, not delta/haor/saline intrusion relevant | IO |
| D33 | cais/mmlu | high_school_geography Ex1 | A | "What is the most rapidly growing religion in the United States today?" | US-centric cultural geography | IC |
| D34 | cais/mmlu | auxiliary_train Ex1 | B | "Jim watched a liquor store furtively for some time, planning to hold it up. He bought a realistic-looking toy gun for the job… On a charge of burglary, Jim's best defense would be that the liquor store was open to the public." | US criminal law scenario — US legal context, no South Asian relevance | IO, IC |
| D35 | cais/mmlu | miscellaneous Ex1 | A | "A flashing red traffic light signifies that a driver should do what? (A) stop" | US traffic law assumption (red = stop is near-universal but framed as US rule) | IC |
| D36 | cais/mmlu | world_religions Ex2 | B | "In Jainism, what is the cycle that one must liberate oneself from? (A) Punya (B) Samsara" | South Asian religion reference (Jainism) — one of very few South Asian cultural anchors in the dataset | IC |
| D37 | cais/mmlu | prehistory Ex2 | B | "The origins of Chinese civilization can be traced to: chiefdoms and states in numerous regions throughout China." | East Asian prehistory — no South Asian relevance | IO |
| D38 | cais/mmlu | high_school_world_history Ex4 | D | "Which of the following most inspired the national plan advanced by Nkrumah? … Socialism" | African postcolonial history — no South Asian agricultural relevance | IO |
| D39 | cais/mmlu | college_medicine Ex4 | D | "When preparing for the **MCAT exam**, a student begins studying electrochemical cells." | MCAT (US Medical College Admissions Test) reference — US academic system assumed | IC |
| D40 | cais/mmlu | global_facts Ex5 | A | "At the time of independence, there were already hundreds of thousands of university graduates in **India**, but hardly any at all in **Congo**." | India referenced but as a factual datapoint about independence-era education, not agro-ecological | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Universal STEM reasoning tasks provide a language-independent cross-model baseline
- **Dimension(s):** IO, OF
- **Observation:** A substantial portion of MMLU items test mathematical, logical, and physical reasoning that does not depend on cultural or geographic knowledge. Examples include abstract algebra (ring theory, group theory), college mathematics (optimization, real analysis), formal logic (predicate logic translation), and physics (electromagnetic, thermodynamic calculations). These items can serve as a culture-neutral baseline for comparing frontier vs. smaller regional models.
- **Deployment relevance:** The environmental scientist's stated goal includes cross-model comparison between frontier LLMs and smaller regional models. STEM reasoning items provide a stable substrate for this comparison even when domain-specific agricultural content is absent.
- **Datapoint citations:**
  - [D1 context] abstract_algebra Ex1 (cais/mmlu, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — Pure abstract mathematics with no cultural loading; valid cross-model comparison point.
  - [D1 context] college_mathematics Ex2 (cais/mmlu, split=test, label=B): "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" — Geometry/optimization; culturally neutral.
  - [D1 context] college_physics Ex3 (cais/mmlu, split=test, label=C): "White light is normally incident on a puddle of water (index of refraction 1.33). A thin (500 nm) layer of oil (index of refraction 1.5) floats on the surface of the puddle. Of the following, the most strongly reflected wavelength is" — Physical optics; no cultural dependency.

#### Strength 2: Some globally-framed factual items reference South Asia tangentially
- **Dimension(s):** IC
- **Observation:** A small number of items in the `global_facts` and `prehistory` configs reference India or broader South Asia, providing a minimal foothold of non-exclusively-Western content. These are sparse but confirm MMLU is not entirely US-only in geographic reference.
- **Deployment relevance:** These items are too few and too shallow to support agricultural knowledge evaluation, but they confirm that some fraction of MMLU questions touch South Asian contexts — marginally relevant for baseline comparison.
- **Datapoint citations:**
  - [D13] global_facts Ex2 (cais/mmlu, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%." — India-referenced factual question; dated (2017) and not agricultural.
  - [D40] global_facts Ex5 (cais/mmlu, split=test, label=A): "At the time of independence, there were already hundreds of thousands of university graduates in India, but hardly any at all in Congo." — India referenced as a comparative datapoint.
  - [D36] world_religions Ex2 (cais/mmlu, split=test, label=B): "In Jainism, what is the cycle that one must liberate oneself from? (A) Punya (B) Samsara" — South Asian religious tradition (Jainism) represented; one of very few South Asian cultural anchors observed across all 175+ reviewed examples.

#### Strength 3: Statistical and scientific reasoning items are moderately transferable
- **Dimension(s):** IO, OF
- **Observation:** High_school_statistics and related items test general inferential reasoning (hypothesis testing, confidence intervals, Type I/II error, sampling) at a level that is conceptually relevant to environmental science methodology universally, including for South Asian researchers. These items test skills the environmental scientist would use regardless of regional context.
- **Deployment relevance:** An environmental scientist evaluating LLMs for agricultural applications would benefit from knowing whether a model understands statistical inference, even if the specific application domains differ.
- **Datapoint citations:**
  - [D30] high_school_statistics Ex1 (cais/mmlu, split=test, label=A): "The Department of Health plans to test the lead level in a specific park. Because a high lead level is harmful to children, the park will be closed if the lead level exceeds the allowed limit… Which of the following decisions would result from the type I error?" — Environmental monitoring framing of Type I error; the content domain is health/environment, though not South Asian specific.
  - [D1 context] high_school_statistics Ex2 (cais/mmlu, split=test, label=B): "In a high school of 1650 students, 132 have personal investments in the stock market. To estimate the total stock investment… Plan I would sample 30 students at random…" — Sampling methodology reasoning, transferable.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Zero subject coverage of South Asian agro-ecology, delta farming, or wetland ecology
- **Dimension(s):** IO
- **Observation:** Across all 57 subject configurations, not a single subject in the MMLU taxonomy addresses haor wetland ecology, boro/aman/aus rice cultivation, char-land agriculture, Brahmaputra-Jamuna floodplain systems, delta hydrology, dry-land Deccan cropping (Rabi/Kharif on black/red soils), coastal aquaculture in Andhra Pradesh, or any South Asian agro-ecological subdomain. The reviewed examples confirm this: the closest environmental content observed is generic water chemistry (D32) and a lead-level park test (D30), neither of which relates to South Asian farming systems. High_school_geography items reference Burgess's Chicago-school urban zone model (D20) and US religion demographics (D33), not Asian agricultural geography.
- **Deployment relevance:** This is a complete structural gap. The deployment's primary purpose — assessing LLM knowledge of South Asian agricultural and environmental science — finds zero targeted test items in MMLU's entire 57-subject taxonomy. The benchmark cannot measure what it does not test.
- **Datapoint citations:**
  - [D19] high_school_geography Ex3 (cais/mmlu, split=test, label=C): "The way of life based on breeding and herding of animals that are used as a source of food, shelter, and clothing is called pastorialism." — Most geographically relevant agriculture item observed; covers generic pastoral farming, not South Asian systems.
  - [D32] college_chemistry Ex5 (cais/mmlu, split=test, label=A): "A substance that is NOT generally considered to be a toxic pollutant in water is (A) carbonic acid (B) a halogenated hydrocarbon (C) lead (D) mercury." — Nearest environmental science content; generic water chemistry with no connection to saline intrusion, haor ecology, or delta hydrology.
  - [D22] college_biology Ex1 (cais/mmlu, split=test, label=A): "In fungi, cell walls are reinforced by which of the following? (A) Chitin (B) Silica (C) Lignin (D) Collagen fibers." — Exemplary of biology coverage: cellular/molecular, not agro-ecological.
  - [D21] nutrition Ex1 (cais/mmlu, split=test, label=A): "Which of the following inborn errors of metabolism gives rise to zinc deficiency? (A) Acrodermatitis enteropathica." — Nutrition content is clinical biochemistry, not crop nutrition or soil science.

#### Concern 2: English-only input format directly contradicts multilingual deployment requirement
- **Dimension(s):** IF
- **Observation:** Every single example reviewed across all 37 configs is in English only. The HF metadata explicitly tags the dataset as `monolingual` with `language: en`. The schema requires English-language question strings. The deployment requires Telugu, Bangladeshi Bengali (Mymensingh dialect), and Indian Bengali as query languages. There is no mechanism within MMLU's format to accept, process, or evaluate non-English input.
- **Deployment relevance:** The elicitation confirms queries will include Telugu and Bengali in both varieties — a direct and absolute format mismatch. No workaround within MMLU's design can address this.
- **Datapoint citations:**
  - [D2] high_school_us_history Ex1 (cais/mmlu, split=test, label=A): "The song, and the movement that it was connected to, highlight which of the following developments in the broader society in the late 1800s?" — Typical English-only question format; no provision for Bengali or Telugu input.
  - [D29] elementary_mathematics Ex1 (cais/mmlu, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" — Even the most basic numeric reasoning items are framed entirely in English with US measurement units.

#### Concern 3: Moral scenarios explicitly anchor correctness in US 2020 norms — irreconcilable with South Asian OC validity
- **Dimension(s):** OC, OO
- **Observation:** The entire `moral_scenarios` config (500 test items) uses a fixed framing: "according to ordinary moral standards in the US as of 2020." This is not incidental phrasing — it is the operative definition of the correct answer for every question in this large subtask. Cultural divergence between Bangladeshi, Bangladeshi-Bengali, and US moral standards (e.g., around family hierarchy, religious obligation, land-use decisions) would produce legitimately different correct answers that this framing cannot accommodate.
- **Deployment relevance:** If the deployment includes any assessment of socially-situated reasoning — relevant for extension workers advising farmers on land use, water management, or community decisions — the US-anchored moral_scenarios labels would be actively misleading as a validity measure.
- **Datapoint citations:**
  - [D1] moral_scenarios Ex1 (cais/mmlu, split=test, label=A): "For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." — US normative framing is explicit and constitutive of the label.
  - [D12] moral_scenarios Ex2–5 (cais/mmlu, split=test): "For which of these two scenarios does the main character … do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**?" — The US normative anchor appears identically in all five reviewed moral_scenarios examples, confirming it is structural, not incidental.

#### Concern 4: Ground-truth labels for human_sexuality, human_aging carry US-specific factual claims as correct answers
- **Dimension(s):** OC, IC
- **Observation:** Several items frame US-specific empirical facts (US birth control statistics, US social security eligibility age, US behavioral survey data 1988–1990) as universally correct answers. A South Asian researcher or LLM optimized for South Asian contexts would reasonably disagree with or be penalized for correctly knowing that these facts differ regionally.
- **Deployment relevance:** While these specific tasks are peripheral to agricultural science, they illustrate a systematic pattern: MMLU's "correct" answers embed US institutional and demographic facts that have no transfer validity to South Asian contexts.
- **Datapoint citations:**
  - [D10] human_sexuality Ex1 (cais/mmlu, split=test, label=A): "Which of the following is the most common method of birth control for married couples in the **U.S.**: (A) Sterilization." — Correct answer is US-specific; would differ for Bangladesh or India.
  - [D11] human_sexuality Ex5 (cais/mmlu, split=test, label=A): "From 1988 to 1990 among heterosexuals in the **US**, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women." — US-specific survey finding from 35+ years ago, embedded as a correct answer.
  - [D9] human_aging Ex3 (cais/mmlu, split=test, label=C): "The age at which one can receive full benefits from social security: (A) Is 62 (B) Is 65 (C) Has been increasing (D) Will never change." — Answer presupposes the US Social Security system.

---

#### MAJOR

#### Concern 5: US legal, political, and historical content dominates multiple large subject categories
- **Dimension(s):** IO, IC
- **Observation:** Multiple high-item-count subjects (professional_law, high_school_us_history, high_school_government_and_politics, us_foreign_policy, jurisprudence) are predominantly or exclusively US-centric. The reviewed professional_law items all involve US tort, contract, and evidence law. High_school_government_and_politics items assume US constitutional structure (First Amendment, War Powers Act, Articles of Confederation). These subjects represent a substantial portion of MMLU's total item count.
- **Deployment relevance:** These subjects are irrelevant to the South Asian agricultural deployment. An LLM performing well on US law or US government questions provides no signal about its knowledge of Bangladesh water law, Indian agricultural extension policy, or Andhra Pradesh coastal aquaculture regulation.
- **Datapoint citations:**
  - [D3] high_school_government_and_politics Ex1 (cais/mmlu, split=test, label=A): "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment." — Entirely US-specific constitutional content.
  - [D4] high_school_government_and_politics Ex4 (cais/mmlu, split=test, label=D): "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president." — US legislative history; no cross-regional transfer.
  - [D7] professional_law Ex1 (cais/mmlu, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs… the girl was struck by the tractor-trailer and was seriously injured. The girl's parents … assert a claim against the lumber company…" — US personal injury/tort law scenario.
  - [D5] us_foreign_policy Ex4 (cais/mmlu, split=test, label=D): "In American government, the power to declare war rests with Congress." — US constitutional structure.

#### Concern 6: World history and European history items frame non-Western events through colonial/Western lenses
- **Dimension(s):** IC, OC
- **Observation:** The `high_school_world_history` config includes South Asian content — specifically the 1857 Indian Uprising (Cawnpore/Kanpur massacres) — but presents it through a British colonial journalist's perspective as primary source, followed by a postcolonial historian's reframing. The correct answer (D18, label=B) is adjudicated by the benchmark. This framing of South Asian history through colonial sources, with labels set by a US academic team, represents a potential OC validity risk where Bangladeshi or Indian stakeholders may assess the "correct" answer differently.
- **Deployment relevance:** If any historical or geopolitical framing questions arise in the deployment context (e.g., framing of Bangladesh-India water disputes), this pattern of colonial-origin primary sources with US-adjudicated correctness is concerning.
- **Datapoint citations:**
  - [D18] high_school_world_history Ex2 (cais/mmlu, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters… British journalist William Howard Russell, My Indian Mutiny Diary, 1860." — Indian history presented through British colonial journalism; label set by US academic team.

#### Concern 7: Global_facts items are temporally stale (2017–2019) for a South Asian deployment context
- **Dimension(s):** IC, OC
- **Observation:** The `global_facts` config contains questions about India and other countries anchored to 2017–2019 data (internet penetration, demographic statistics). For a South Asian deployment in 2025, these figures are significantly outdated. An LLM that correctly knows 2024 India internet penetration figures would be penalized for not knowing the 2017 benchmark answer.
- **Deployment relevance:** The Mymensingh scientist is evaluating LLMs for current-context agricultural and environmental knowledge. Benchmarking against 2017 data for South Asia-relevant questions produces systematically misleading signals about contemporary model knowledge.
- **Datapoint citations:**
  - [D13] global_facts Ex2 (cais/mmlu, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%." — The 2017 figure (26%) is the correct answer; a model knowing the 2025 figure (~55%) would be penalized.
  - [D14] global_facts Ex1 (cais/mmlu, split=test, label=A): "About what percentage of survey respondents from China report having paid a bribe in the last year to access public services … as of 2017?" — Year-anchored question; staleness applies across all global_facts items.

#### Concern 8: No annotator demographic information documented; US MTurk baseline is the only human reference
- **Dimension(s):** OC
- **Observation:** The HF card tags the dataset as `annotations_creators: no-annotation`, and the paper documents only a US MTurk baseline (34.5% accuracy). No South Asian domain experts, agronomists, or environmental scientists were involved in item creation or answer validation, based on all available documentation. The graduate/undergraduate students who collected items are entirely from US institutions.
- **Deployment relevance:** For any questions that could have regionally contingent correct answers (cross-border water policy, comparative agricultural practice), the labels carry no authority for the South Asian deployment context. The user explicitly confirmed this risk for Bangladesh–India water-sharing questions.
- **Datapoint citations:**
  - [D9] human_aging Ex3 (cais/mmlu, split=test, label=C): "The age at which one can receive full benefits from social security … Has been increasing." — Illustrates how US institutional facts are treated as universally correct without regional annotation review.
  - [D12] moral_scenarios, all five reviewed examples — US 2020 normative framing repeated across the entire config without any annotation for cross-cultural validity.

---

#### MINOR

#### Concern 9: US customary units in elementary mathematics assume US educational context
- **Dimension(s):** IC
- **Observation:** Elementary mathematics items use miles per hour (D29) rather than metric units. While this is a minor issue for mathematical reasoning evaluation, it introduces an unnecessary US-centric cultural assumption into what should be culturally neutral content.
- **Deployment relevance:** Minor; the mathematical reasoning being tested is metric-neutral, but the unit choice reflects the US educational sourcing of items.
- **Datapoint citations:**
  - [D29] elementary_mathematics Ex1 (cais/mmlu, split=test, label=A): "If a freight train travels at a speed of **20 miles per hour** for 6 hours, how far will it travel?" — US customary units in an otherwise neutral math problem.

#### Concern 10: College_medicine MCAT reference assumes US higher education system
- **Dimension(s):** IC
- **Observation:** A college_medicine item references the MCAT (US Medical College Admissions Test) as a natural reference point for a study scenario, embedding US higher education assumptions into what purports to be general medical knowledge.
- **Deployment relevance:** Minor; the actual content (elaborative rehearsal psychology) is not US-specific, but the MCAT framing signals the US academic origin of the item and would be unfamiliar to South Asian medical students.
- **Datapoint citations:**
  - [D39] college_medicine Ex4 (cais/mmlu, split=test, label=D): "When preparing for the **MCAT exam**, a student begins studying electrochemical cells… The student's process is best characterized as: (D) Elaborative rehearsal." — MCAT reference embeds US academic context in a psychology-of-learning question.

#### Concern 11: High_school_geography and sociology items carry Western-normative theoretical frameworks
- **Dimension(s):** IC
- **Observation:** Geography questions use Burgess's concentric zone model (Chicago, 1920s) as the reference urban geography theory; sociology questions use UK-origin research (Smith & Tomlinson, Bowlby, Chodorow) as authoritative references. These frameworks were developed in US/UK contexts and may not describe South Asian urban or social patterns.
- **Deployment relevance:** Minor for the primary agricultural deployment; more relevant if the deployment expands to social science evaluation.
- **Datapoint citations:**
  - [D20] high_school_geography Ex5 (cais/mmlu, split=test, label=A): "Which zone contains low-income slums, ethnic ghettos, and general deterioration in **Burgess's concentric zone model of urban form**?" — Chicago School urban theory presented as authoritative geography.
  - [D26] sociology Ex3 (cais/mmlu, split=test, label=C): "Smith & Tomlinson argued that **school character** far outweighed ethnic background in determining educational success." — UK-based educational sociology as the reference frame.

---

### Content Coverage Summary

The 175+ examples reviewed span all 37 sampled configurations and confirm the documented structure: MMLU is an English-only, US/Western-institution-anchored multiple-choice benchmark. The subject matter is dominated by US academic and professional preparation content — US law (professional_law, jurisprudence), US government (high_school_government_and_politics, us_foreign_policy), US history, Western European philosophy and history, and US clinical medicine. General STEM subjects (physics, mathematics, chemistry, computer science, biology) are culturally lighter but still framed through US/Anglophone university materials.

The dataset contains no items addressing boro/aman/aus rice cultivation cycles, haor or beel wetland ecology, char-land agriculture, Brahmaputra-Jamuna floodplain dynamics, Deccan dry-land Rabi/Kharif cropping, brackishwater shrimp aquaculture, or any Bengal/Telugu-specific agro-ecological subdomain. The closest environmental science content observed is generic water chemistry and a Type I error example set in a lead-level park-testing scenario. South Asia is referenced tangentially in two global_facts items (India internet statistics 2017; India vs. Congo university graduates at independence) and one world_religions item (Jainism/samsara). The 1857 Indian Uprising appears in world_history but is framed through British colonial primary sources.

The moral_scenarios config (500 items) explicitly anchors correctness in "ordinary moral standards in the US as of 2020" — a framing that is constitutive, not incidental, and that produces direct OC invalidity for South Asian deployment. Human_sexuality and human_aging items embed US-specific demographic facts as correct answers. The auxiliary_train split contains US bar-exam-style criminal and property law questions with no non-US legal content detected.

Register throughout is formal academic English, consistent with US standardized test preparation. No dialect variation, no Bengali or Telugu script, and no colloquial register is present in any reviewed example.

---

### Limitations

1. **Sample size per config:** Only 5–6 examples were reviewed per configuration. With 100+ items per test split, subject-level coverage patterns within each config cannot be fully characterized from the sample.

2. **Unreviewed configs:** Approximately 20 of the 57 configs were not directly sampled (e.g., formal_logic, prehistory, human_sexuality, and others were sampled but some configs such as prehistory were reviewed with fewer examples). Agricultural or South Asian-adjacent outlier items within those configs cannot be ruled out from the sample alone, though the taxonomy analysis makes their presence extremely unlikely.

3. **No Telugu or Bengali text to inspect:** Because MMLU is English-only, there is no non-English text to assess for dialect, script, or register quality. The language mismatch concern is absolute and visible at the metadata level, but its practical effect on specific model evaluation cannot be further characterized from dataset content alone.

4. **Temporal staleness of global_facts:** The global_facts items are dated (2017–2019); whether any items have been updated in the HuggingFace distribution cannot be confirmed from the sample.

5. **Auxiliary_train split:** The auxiliary_train split contains structured training data in a nested format (`train` column containing a dict). The full content scope of this split was sampled but only 5 examples inspected; it appears to contain US bar-exam-style law questions, but comprehensive characterization requires larger sampling.

6. **Cross-config agricultural content:** It is theoretically possible that a small number of items in the `miscellaneous` config (500 items) or `global_facts` config address South Asian agricultural topics not represented in the 5-example sample. The sample is insufficient to rule out rare outliers, though the documented sourcing from US standardized exams makes such items structurally improbable.

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
  "region": "South Asian Agricultural and Environmental Science — Mymensingh–Telangana–Andhra Pradesh Deployment",
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
