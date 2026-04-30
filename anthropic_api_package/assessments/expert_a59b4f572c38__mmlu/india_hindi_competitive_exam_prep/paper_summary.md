# Validity Extraction: Measuring Massive Multitask Language Understanding
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: Measuring Massive Multitask Language Understanding
- **Authors**: Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, Jacob Steinhardt
- **Venue/Year**: Not explicitly stated in registry (ICLR 2021 based on known publication record)
- **Total Pages**: 27
- **Quotes Extracted**: 160

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

The benchmark covers 57 tasks spanning STEM, humanities, social sciences, and other areas, ranging from elementary to advanced professional difficulty [Q1, Q8]. The taxonomy is explicitly designed to require "extensive world knowledge and problem solving ability" rather than narrow linguistic or commonsense skills [Q2], and the breadth is intended to comprehensively evaluate both the depth and breadth of text understanding across topics that humans are motivated to learn [Q15, Q76]. Within the humanities cluster, subjects include law, philosophy, history, and moral reasoning — with philosophy tasks drawing on logical fallacies, formal logic, and normative ethics [Q24, Q26], and history questions covering wide time periods and geographic locations [Q27]. Social science tasks cover economics (micro, macro, econometrics), sociology, politics, geography, and psychology [Q28, Q29, Q31], including more esoteric topics like security studies [Q30], while STEM subjects include physics, computer science, and mathematics at multiple difficulty levels [Q32].

From a deployment-validity perspective, the subject distribution is heavily US-centric. Exemplar questions illustrated across the appendix include US Foreign Policy [Q49], US History [Q140], US Government and Politics [Q133], US Medical Licensing content [Q154], and questions built explicitly from "Advanced Placement" and "Graduate Record Examination" conventions [Q17, Q18]. There is no coverage of Indian Polity & Constitution, Indian History, Hindi language proficiency, Current Affairs relevant to India, or Mathematics/Reasoning formats aligned to UPSC, SSC, or banking exam syllabi. The task taxonomy therefore exhibits a fundamental Input Ontology gap relative to the deployment's priority subjects for Hindi-speaking graduate students preparing for central-level Indian competitive examinations. While the benchmark's broad disciplinary structure (GK, history, reasoning, social science) superficially parallels some central-exam subject areas, the actual instantiation of these categories reflects US and Western academic conventions throughout [Q104, Q105–Q160].

---

### 2. Data Sources and Collection

Questions were manually collected by graduate and undergraduate students from freely available online sources, including practice materials for the GRE, USMLE, undergraduate courses, and Oxford University Press books [Q17]. Crucially, most questions came from PDFs or websites where questions and answers were on separate pages [Q101], which reduces the likelihood of trivial answer leakage during scraping but still situates the entire question pool within English-language, US/Western academic assessment ecosystems. For the Professional Law task specifically, approximately 2,000 additional training examples were collected separately [Q69], and further pretraining used Harvard's Law Library case law corpus [Q71] — both exclusively US legal sources.

A key design distinction is that the benchmark deliberately does not require large training sets, instead assuming that relevant knowledge was acquired during model pretraining on vast internet text [Q60]. This design assumption has direct implications for the deployment context: a model pretrained predominantly on English internet text may have absorbed very limited knowledge about North Indian regional history, administrative structures, or Hindi-language competitive exam content, meaning the benchmark's implicit knowledge acquisition pathway does not map onto what the deployment's target student population would know or need.

---

### 3. Data Format and Preprocessing

The benchmark is designed exclusively for zero-shot and few-shot evaluation, measuring knowledge acquired during pretraining rather than task-specific fine-tuning [Q7]. The dataset contains 15,908 questions in total, split into a 5-question-per-subject few-shot development set, a 1,540-question validation set, and a 14,079-question test set [Q19], with each subject containing at least 100 test examples [Q20]. GPT-3 is prompted with a subject-labeled preamble followed by up to five demonstration examples and a question, with the model's token probabilities for "A," "B," "C," and "D" determining the prediction [Q44]. UnifiedQA uses a different normalized, lowercased input format with a special end-of-sequence token [Q91], and removing that token causes meaningful accuracy drops [Q92] — indicating format sensitivity that is relevant when assessing deployment robustness. Question length is not inherently a difficulty indicator: for questions exceeding 280 characters, the correlation between length and label confidence is slightly positive [Q94].

For the deployment context, the input format is text-only in English — there is no Hindi-language input pathway, no Devanagari script support documented, and no accommodation for the code-mixed Hindi–English phrasing that might characterize the target population's reading environment. This is the benchmark's most fundamental input-form constraint relative to the deployment.

---

### 4. Label Categories and Output Types

The benchmark's output schema is a four-class multiple-choice classification: models predict one of four options (A, B, C, D) for each question [Q83]. Ground truth labels are the correct answers from the original source examinations, and evaluation reduces entirely to classification accuracy across these four classes [Q23, Q34]. There is no secondary label layer for explanatory rationale, confidence tiers, or pedagogical feedback.

This label ontology represents a **critical Output Ontology mismatch** with the deployment context, which requires not only a correct/incorrect verdict but also a substantive Hindi-language explanation of why an answer is right or wrong [Elicitation Q3]. The benchmark provides no framework, annotation, or scoring mechanism for evaluating the quality, accuracy, or fluency of open-ended explanatory outputs — the benchmark's entire ground-truth schema is exhausted by the single correct MCQ option. Downstream validity of model-generated Hindi rationales cannot be assessed using this benchmark's label structure at all.

---

### 5. Annotation Process

NOT DOCUMENTED: The paper is entirely silent on annotator demographics, annotation protocols, inter-annotator agreement, or quality assurance procedures for the question collection process. The only stated mechanism for ensuring question quality is that graduate and undergraduate students manually collected questions from existing standardized test materials [Q17], implying that the ground-truth labels are inherited from the original exam answer keys rather than independently annotated. This absence is itself a validity-relevant finding: without knowing who collected the questions, what linguistic or cultural backgrounds they brought, or how conflicts were resolved, it is impossible to assess whether the question set was calibrated for any particular student population — let alone Hindi-medium graduate students in North India. The reliance on existing standardized test answer keys may mitigate some label-noise risk but does nothing to address cultural or linguistic representativeness.

---

### 6. Evaluation Metrics and Output Modality

The primary evaluation metric is classification accuracy — the proportion of questions for which the model selects the correct MCQ option across all tasks [Q34]. Human baselines are reported at two levels: unspecialized Amazon Mechanical Turk workers achieve 34.5% accuracy, while expert-level performance (estimated at the 95th percentile of real-world test takers) is approximately 89.8% [Q21]. Benchmark results show that smaller GPT-3 models perform near random chance (~25%), while the 175B parameter GPT-3 reaches 43.9% [Q11, Q45], and the largest UnifiedQA model achieves 48.9% [Q47]. The paper also evaluates calibration, finding that GPT-3's confidence diverges from actual accuracy by up to 24% in zero-shot settings and up to 14% in few-shot settings [Q57, Q96], with RMS calibration error reaching 19.4% for some subjects [Q58]. Few-shot accuracy monotonically improves with more demonstration examples, though zero-shot performance is only modestly lower than 5-shot [Q97].

For the deployment context, accuracy on four-class MCQ items is an incomplete and potentially misleading validity signal. The deployed system must produce open-ended Hindi-language explanations [Elicitation Q3], and MCQ accuracy does not validate whether a model can generate accurate, coherent, or pedagogically appropriate rationales in Hindi. The benchmark's output modality (a discrete label) fundamentally diverges from the deployment's output modality (a natural-language explanation) — meaning high benchmark accuracy could coexist with poor explanation quality, and the benchmark score provides no direct evidence about the Output Form dimension critical to this deployment.

---

### 7. Stated Limitations

The authors identify several important limitations. First, models fail to reach expert-level accuracy on any of the 57 tasks [Q4, Q67], and performance is lopsided — GPT-3 reaches ~70% on its best subject but near-random performance on several others [Q12, Q54]. Subjects most relevant to the deployment's concern about human-values reasoning — specifically law and morality — show near-random accuracy [Q6, Q13, Q65], a direct warning for any deployment requiring judgment about correct answers in ethics- or policy-adjacent domains.

Second, the benchmark is explicitly text-only, and the authors acknowledge that many important concepts are conveyed through other modalities (images, audio, physical interaction) that are excluded by design [Q59]. Third, GPT-3 is poorly calibrated: its confidence is only weakly correlated with actual accuracy in zero-shot settings, with gaps reaching 24% [Q14, Q57], and even in few-shot settings calibration errors persist [Q96]. The authors note that high-confidence mistakes are common [Q89], which is especially concerning for a deployment that presents model outputs as authoritative feedback to students. Fourth, the authors flag a potential memorization concern — questions sourced from online PDFs may have appeared in pretraining data [Q95, Q100] — though entropy analysis suggests exact question memorization is unlikely [Q98, Q99], and the authors propose publishing source lists to mitigate future contamination [Q102]. Fifth, it is unclear whether simply scaling model size will resolve benchmark performance gaps [Q73, Q74], and additional domain-specific pretraining showed only modest gains in the law domain [Q72]. Format sensitivity is also noted, particularly for UnifiedQA [Q90, Q92, Q149], and the benchmark's evaluation format is not identical to the format in which pretraining knowledge was acquired [Q62, Q63].

From the deployment perspective, the most consequential limitation not acknowledged by the authors is the benchmark's exclusive US/Western cultural and linguistic framing. None of the stated limitations address the absence of Hindi-language content, Indian regional knowledge, or competitive exam formats relevant to UPSC/SSC/banking aspirants — gaps that are entirely invisible within the paper's own scope.

---

### 8. Authors and Affiliations

The seven authors are affiliated with four US universities: Dan Hendrycks, Andy Zou, Dawn Song, and Jacob Steinhardt at UC Berkeley; Collin Burns at Columbia University; Steven Basart at the University of Chicago; and Mantas Mazeika at the University of Illinois Urbana-Champaign [Q9]. Funding sources include the NSF Graduate Research Fellowship Program, an Open Philanthropy Project Fellowship, and NSF Frontier Award 1804794 [Q78, Q79]. Acknowledgments reference colleagues at AI research organizations including OpenAI and DeepMind [Q77]. The entirely US-based institutional origin of the benchmark strongly signals that its design assumptions, question sources, cultural frames, and subject priorities reflect US academic and professional assessment conventions — providing no institutional grounding in Indian educational systems, Hindi-language assessment traditions, or the competitive examination ecosystem that defines the deployment context.

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "We propose a new test to measure a text model's multitask accuracy. The test covers 57 tasks including elementary mathematics, US history, computer science, law, and more." |
| Q2 | 1 | task_taxonomy | "To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability." |
| Q3 | 1 | evaluation_metrics | "We find that while most recent models have near random-chance accuracy, the very largest GPT-3 model improves over random chance by almost 20 percentage points on average." |
| Q4 | 1 | stated_limitations | "However, on every one of the 57 tasks, the best models still need substantial improvements before they can reach expert-level accuracy." |
| Q5 | 1 | stated_limitations | "Models also have lopsided performance and frequently do not know when they are wrong." |
| Q6 | 1 | stated_limitations | "Worse, they still have near-random accuracy on some socially important subjects such as morality and law." |
| Q7 | 1 | data_format | "We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings." |
| Q8 | 1 | task_taxonomy | "The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability." |
| Q9 | 1 | authors_affiliations | "Dan Hendrycks UC Berkeley, Collin Burns Columbia University, Steven Basart UChicago, Andy Zou UC Berkeley, Mantas Mazeika UIUC, Dawn Song UC Berkeley, Jacob Steinhardt UC Berkeley" |
| Q10 | 2 | task_taxonomy | "Since our test consists in 57 tasks, it can be used to analyze aggregate properties of models across tasks and to track important shortcomings." |
| Q11 | 2 | evaluation_metrics | "We find that meaningful progress on our benchmark has only become possible in recent months. In particular, few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy (see Figure 1b)." |
| Q12 | 2 | stated_limitations | "On the other hand, unlike human professionals GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects." |
| Q13 | 2 | stated_limitations | "Our results indicate that while recent advances have been impressive, state-of-the-art models still struggle at learning and applying knowledge from pretraining. The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality." |
| Q14 | 2 | stated_limitations | "Worryingly, we also find that GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy." |
| Q15 | 2 | task_taxonomy | "We comprehensively evaluate the breadth and depth of a model's text understanding by covering numerous topics that humans are incentivized to learn." |
| Q16 | 3 | task_taxonomy | "We create a massive multitask test consisting of multiple-choice questions from various branches of knowledge. The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn. There are 57 tasks in total, which is also the number of Atari games (Bellemare et al., 2013), all of which are listed in Appendix B." |
| Q17 | 3 | data_sources | "The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online. These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination. It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books." |
| Q18 | 3 | task_taxonomy | "Some tasks cover a subject, like psychology, but at a specific level of difficulty, such as "Elementary," "High School," "College," or "Professional." For example, the "Professional Psychology" task draws on questions from freely available practice questions for the Examination for Professional Practice in Psychology, while the "High School Psychology" task has questions like those from Advanced Placement Psychology examinations." |
| Q19 | 3 | data_format | "We collected 15908 questions in total, which we split into a few-shot development set, a validation set, and a test set. The few-shot development set has 5 questions per subject, the validation set may be used for selecting hyperparameters and is made of 1540 questions, and the test set has 14079 questions." |
| Q20 | 3 | data_format | "Each subject contains 100 test examples at the minimum, which is longer than most exams designed to assess people." |
| Q21 | 3 | evaluation_metrics | "Human-level accuracy on this test varies. Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test. Meanwhile, expert-level performance can be far higher. For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations, and these questions make up our "Professional Medicine" task. If we take the 95th percentile human test-taker accuracy for exams that build up our test, and if we make an educated guess when such information is unavailable, we then estimate that expert-level accuracy is approximately 89.8%." |
| Q22 | 3 | evaluation_metrics | "Since our test aggregates different subjects and several levels of difficulty, we measure more than straightforward commonsense or narrow linguistic understanding. Instead, we measure arbitrary" |
| Q23 | 3 | evaluation_metrics | "Consequently, we instead create a simple-to-evaluate test that measures classification accuracy on multiple choice questions." |
| Q24 | 4 | task_taxonomy | "The humanities is a group of disciplines that make use of qualitative analysis and analytic methods rather than scientific empirical methods. Branches of the humanities include law, philosophy, history, and so on (Appendix B)." |
| Q25 | 4 | task_taxonomy | "Mastering these subjects requires a variety of skills. For example, legal understanding requires knowledge of how to apply rules and standards to complex scenarios, and also provide answers with stipulations and explanations." |
| Q26 | 4 | task_taxonomy | "For philosophy, our questions cover concepts like logical fallacies, formal logic, and famous philosophical arguments. It also covers moral scenarios, including questions from the ETHICS dataset (Hendrycks et al., 2020) that test a model's understanding of normative statements through predicting widespread moral intuitions about diverse everyday scenarios." |
| Q27 | 4 | task_taxonomy | "Finally, our history questions cover a wide range of time periods and geographical locations, including prehistory and other advanced subjects." |
| Q28 | 4 | task_taxonomy | "Social science includes branches of knowledge that examine human behavior and society. Subject areas include economics, sociology, politics, geography, psychology, and so on." |
| Q29 | 4 | task_taxonomy | "Our economics questions include microeconomics, macroeconomics, and econometrics, and cover different types of problems, including questions that require a mixture of world knowledge, qualitative reasoning, or quantitative reasoning." |
| Q30 | 4 | task_taxonomy | "We also include important but more esoteric topics such as security studies in order to test the boundaries of what is experienced and learned during pretraining." |
| Q31 | 4 | task_taxonomy | "Social science also includes psychology, a field that may be especially important for attaining a nuanced understanding of humans." |
| Q32 | 4 | task_taxonomy | "STEM subjects include physics, computer science, mathematics, and more." |
| Q33 | 4 | task_taxonomy | "Conceptual physics tests understanding of simple physics principles and may be thought" |
| Q34 | 5 | evaluation_metrics | "To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks." |
| Q35 | 5 | evaluation_metrics | "We evaluate GPT-3 (Brown et al., 2020) and UnifiedQA (Khashabi et al., 2020)." |
| Q36 | 5 | evaluation_metrics | "For GPT-3 we use the OpenAI API, which provides access to four model variants, "Ada," "Babbage," "Curie," and "Davinci," which we refer to as "Small" (2.7 billion parameters), "Medium" (6.7 billion), "Large" (13 billion) and "X-Large" (175 billion)." |
| Q37 | 5 | evaluation_metrics | "UnifiedQA uses the T5 (Raffel et al., 2019) text-to-text backbone and is fine-tuned on previously proposed question answering datasets (Lai et al., 2017), where the prediction is the class with the highest token overlap with UnifiedQA's text output." |
| Q38 | 5 | evaluation_metrics | "Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy." |
| Q39 | 5 | evaluation_metrics | "We also fine-tune RoBERTa-base, ALBERT-xxlarge, and GPT-2 on UnifiedQA training data and our dev+val set." |
| Q40 | 5 | evaluation_metrics | "We primarily focus on UnifiedQA and GPT-3 in the rest of this document, but additional discussion of RoBERTa, ALBERT, and GPT-2 is in Appendix A." |
| Q41 | 5 | evaluation_metrics | "All values are percentages." |
| Q42 | 5 | stated_limitations | "Some models proposed in the past few months can move several percent points beyond random chance." |
| Q43 | 5 | evaluation_metrics | "GPT-3 uses few-shot learning and UnifiedQA is tested under distribution shift." |
| Q44 | 6 | data_format | "We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]." For zero-shot evaluation, we append the question to the prompt. For few-shot evaluation, we add up to 5 demonstration examples with answers to the prompt before appending the question. All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction. For consistent evaluation, we create a dev set with 5 fixed few-shot examples for each subject." |
| Q45 | 6 | evaluation_metrics | "We compare the few-shot accuracy of each GPT-3 size in Table 1. We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%." |
| Q46 | 6 | evaluation_metrics | "While the smaller models have around 25% zero-shot accuracy, Figure 10 in Appendix A shows that the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7%." |
| Q47 | 6 | evaluation_metrics | "The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy. This performs better than the few-shot GPT-3 X-Large model, despite UnifiedQA have an order of magnitude fewer parameters." |
| Q48 | 6 | evaluation_metrics | "We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy. These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps." |
| Q49 | 6 | task_taxonomy | "Figure 6 shows the accuracy of GPT-3 (few-shot) and UnifiedQA for all 57 tasks. It shows the both models are below expert-level performance for all tasks, with GPT-3's accuracy ranging from 69% for US Foreign Policy to 26% for College Chemistry. UnifiedQA does best on marketing, with an accuracy of 82.5%." |
| Q50 | 6 | stated_limitations | "Overall, models do poorly on highly procedural problems. Figure 6 shows that calculation-heavy STEM subjects tend to have low accuracy compared to verbal subjects. The lowest-accuracy tasks are STEM subjects that emphasize mathematics or calculations. We speculate that is in part because GPT-3 acquires declarative knowledge more readily than procedural knowledge." |
| Q51 | 7 | task_taxonomy | "For example, many questions in Elementary Mathematics require applying the order of operations for arithmetic, which is described by the acronym PEMDAS (Parentheses Exponents Multiplication Division Addition Subtraction)." |
| Q52 | 7 | stated_limitations | "GPT-3 is aware of the acronym PEMDAS. However, it does not consistently apply PEMDAS to actual problems." |
| Q53 | 7 | stated_limitations | "GPT-3 learns about topics in a pedagogically unusual order. GPT-3 does better on College Medicine (47.4%) and College Mathematics (35.0%) than calculation-heavy Elementary Mathematics (29.9%)." |
| Q54 | 7 | stated_limitations | "GPT-3 demonstrates unusual breadth, but it does not master a single subject. Meanwhile we suspect humans have mastery in several subjects but not as much breadth. In this way, our test shows that GPT-3 has many knowledge blindspots and has capabilities that are lopsided." |
| Q55 | 7 | evaluation_metrics | "We should not trust a model's prediction unless the model is calibrated, meaning that its confidence is a good estimate of the actual probability the prediction is correct." |
| Q56 | 7 | evaluation_metrics | "We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject." |
| Q57 | 7 | stated_limitations | "GPT-3 is uncalibrated. In fact, its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects." |
| Q58 | 7 | evaluation_metrics | "Another calibration measure is the Root Mean Squared (RMS) calibration error (Hendrycks et al., 2019a; Kumar et al., 2019). Many tasks have miscalibrated predictions, such as Elementary Mathematics which has a zero-shot RMS calibration error of 19.4%." |
| Q59 | 7 | stated_limitations | "While text is capable of conveying an enormous number of concepts about the world, many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020). Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format." |
| Q60 | 7 | data_sources | "A major distinction between our benchmark and previous multitask NLP benchmarks is that we do not require large training sets. Instead, we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet. For this reason we assess pretrained models in a zero-shot, few-shot, or transfer setting and we provide a dev, val, and test set for each task." |
| Q61 | 8 | evaluation_metrics | "The dev set is used for few-shot prompts, the val set could be used for hyperparameter tuning, and the test set is used to compute the final accuracy." |
| Q62 | 8 | evaluation_metrics | "Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining." |
| Q63 | 8 | stated_limitations | "This has the benefit of obviating concerns about spurious training set annotation artifacts (Geirhos et al., 2020; Hendrycks et al., 2019b) and is in stark contrast to the previous paradigm of identically distributed training and test sets." |
| Q64 | 8 | stated_limitations | "We find that current large-scale Transformers have wide room for improvement." |
| Q65 | 8 | stated_limitations | "They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks." |
| Q66 | 8 | stated_limitations | "Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics and many other STEM subjects with "plug and chug" problems." |
| Q67 | 8 | stated_limitations | "Additionally, they do not match expert-level performance (90%) on any subject, so for all subjects it is subhuman." |
| Q68 | 8 | stated_limitations | "On average, models are only now starting to move beyond random-chance accuracy levels." |
| Q69 | 8 | data_sources | "We collected approximately 2,000 additional Professional Law training examples." |
| Q70 | 8 | evaluation_metrics | "After fine-tuning a RoBERTa-base model (Liu et al., 2019) using this custom training set, our model attained 32.8% test accuracy." |
| Q71 | 8 | data_sources | "We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law, but after fine-tuning it only attained 36.1% accuracy." |
| Q72 | 8 | stated_limitations | "This suggests that while additional pretraining on relevant high quality text can help, it may not be enough to substantially increase the performance of current models." |
| Q73 | 8 | stated_limitations | "It is unclear whether simply scaling up existing language models will solve the test." |
| Q74 | 8 | stated_limitations | "Current understanding indicates that a 10× increase in model size must be accompanied by an approximate 5× increase in data (Kaplan et al., 2020)." |
| Q75 | 8 | task_taxonomy | "We introduced a new test that measures how well text models can learn and apply knowledge encountered during pretraining." |
| Q76 | 8 | task_taxonomy | "By covering 57 subjects at varying levels of difficulty, the test assesses language understanding in greater breadth and depth than previous benchmarks." |
| Q77 | 9 | authors_affiliations | "We would like to thank the following for their helpful comments: Oyvind Tafjord, Jan Leike, David Krueger, Alex Tamkin, Girish Sastry, and Henry Zhu." |
| Q78 | 9 | authors_affiliations | "DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship." |
| Q79 | 9 | authors_affiliations | "This research was also supported by the NSF Frontier Award 1804794." |
| Q80 | 11 | task_taxonomy | "This appendix includes figures with sorted results (Figure 9), few-shot examples vs. accuracy (Figure 10), and few-shot calibration (Figure 11). It also includes sections on fine-tuning, error analysis, and format sensitivity." |
| Q81 | 11 | evaluation_metrics | "We primarily analyzed models with more than 10 billion parameters in the main body of the paper. For this section, we analyze smaller models including RoBERTa-base (125 million parameters) (Liu" |
| Q82 | 11 | task_taxonomy | "On the left are GPT-3 few shot accuracies for all of the 57 tasks. On the right are UnifiedQA transfer accuracies for all of the 57 tasks. For both models, capabilities are lopsided." |
| Q83 | 12 | label_categories | "Models are fine-tuned to predict one of four classes using the UnifiedQA MCQ questions and using our dev+val set. We test on our multitask test set." |
| Q84 | 12 | evaluation_metrics | "RoBERTa-base attains an overall accuracy of 27.9%, with 27.9% accuracy for the humanities, 28.8% for social sciences, 27.0% for STEM, and 27.7% for other." |
| Q85 | 12 | evaluation_metrics | "ALBERT-xxlarge attains an accuracy of 27.1%, with 27.2% accuracy for the humanities, 25.7% for the social sciences, 27.7% for STEM, and 27.9% for other." |
| Q86 | 12 | evaluation_metrics | "GPT-2 attains an accuracy of 32.4%, with 32.8% accuracy for the humanities, 33.3% for the social sciences, 30.2% for STEM, and 33.1% for other." |
| Q87 | 12 | stated_limitations | "UnifiedQA's smallest variant, which has just 60 million parameters and approximately 29.3% accuracy. It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters. This suggests that its larger pretraining dataset enables higher accuracy." |
| Q88 | 12 | evaluation_metrics | "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy. This again suggests that T5's larger pretraining dataset size (and therefore UnifiedQA's pretraining dataset size) can increase accuracy." |
| Q89 | 12 | stated_limitations | "We qualitatively analyze when GPT-3 makes high confidence mistakes. We find that while many of these mistakes were clearly wrong, many were mistakes that a human might make." |
| Q90 | 12 | stated_limitations | "While different question formatting choices often lead to similar GPT-3 accuracies, we find that UnifiedQA is more sensitive." |
| Q91 | 12 | data_format | "UnifiedQA's input format is of the form QUESTION1 \n (A) CHOICE1 (B) CHOICE2 (C) CHOICE3 (D) CHOICE4</s> where questions and choices are normalized and made lowercase." |
| Q92 | 12 | stated_limitations | "If we remove the </s> from the input, accuracy declines by several percentage points." |
| Q93 | 13 | task_taxonomy | "We provide analysis of question length and difficulty in Figure 12. We list all tasks and the topics they test in Table 2. We also provide an example for each task starting with Figure 14." |
| Q94 | 13 | data_format | "For questions longer than a tweet (280 characters), the correlation between question length and true label confidence is slightly positive. This shows that longer questions are not necessarily harder." |
| Q95 | 13 | stated_limitations | "Since language models train on vast text corpora, there is some chance that they have seen the exact question and answer during pretraining. If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. Likewise, a question's entropy would be especially low if it were memorized. Memorized questions and answers should have low entropy and" |
| Q96 | 13 | evaluation_metrics | "While models are more calibrated in a few-shot setting than a zero-shot setting, they are still miscalibrated, with gap between accuracy and confidence reaching up to 14%. Here the correlation between confidence and accuracy is r = 0.81, compared to r = 0.63 in the zero-shot setting." |
| Q97 | 13 | evaluation_metrics | "As the number of few-shot instruction examples increases, the accuracy monotonically increases. Notably, zero-shot performance is only somewhat lower than 5-shot accuracy." |
| Q98 | 14 | stated_limitations | "However, in Figure 13, we see that accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers." |
| Q99 | 14 | stated_limitations | "This suggests that our exact questions were not memorized." |
| Q100 | 14 | stated_limitations | "However, during pretraining models encountered text related to our questions through processing Wikipedia." |
| Q101 | 14 | data_sources | "We also note that most of our questions came from PDFs or websites where questions and answers are on separate pages." |
| Q102 | 14 | stated_limitations | "To reduce the probability that future models encounter exact questions during test-time, we will provide a list of question sources." |
| Q103 | 14 | evaluation_metrics | "In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56." |
| Q104 | 15 | task_taxonomy | "Table 2: Summary of all 57 tasks." |
| Q105 | 16 | task_taxonomy | "Find all c in Z₃ such that Z₃[x]/(x² + c) is a field." |
| Q106 | 16 | task_taxonomy | "What is the embryological origin of the hyoid bone?" |
| Q107 | 16 | task_taxonomy | "Why isn't there a planet where the asteroid belt is located?" |
| Q108 | 16 | task_taxonomy | "Three contrasting tactics that CSO's can engage in to meet their aims are which typically involves research and communication, , which may involve physically attacking a company's operations or , often involving some form of ." |
| Q109 | 16 | task_taxonomy | "How many attempts should you make to cannulate a patient before passing the job on to a senior colleague?" |
| Q110 | 16 | task_taxonomy | "In a given population, 1 out of every 400 people has a cancer caused by a completely recessive allele, b. Assuming the population is in Hardy-Weinberg equilibrium, which of the following is the expected proportion of individuals who carry the b allele but are not expected to develop the cancer?" |
| Q111 | 16 | task_taxonomy | "Which of the following statements about the lanthanide elements is NOT true?" |
| Q112 | 17 | task_taxonomy | "Consider a computer design in which multiple processors, each with a private cache memory, share global memory using a single bus." |
| Q113 | 17 | task_taxonomy | "Let A be a real 2 × 2 matrix. Which of the following statements must be true?" |
| Q114 | 17 | task_taxonomy | "In a genetic test of a newborn, a rare genetic disorder is found that has X-linked recessive transmission." |
| Q115 | 17 | task_taxonomy | "One end of a Nichrome wire of length 2L and cross-sectional area A is attached to an end of another Nichrome wire of length L and cross- sectional area 2A." |
| Q116 | 17 | task_taxonomy | "Why is it that anti-virus scanners would not have found an exploitation of Heartbleed?" |
| Q117 | 17 | task_taxonomy | "A model airplane flies slower when flying into the wind and faster with wind at its back." |
| Q118 | 18 | task_taxonomy | "Consider the following AR(1) model with the disturbances having zero mean and unit variance yt = 0.2 + 0.4yt−1 + ut The (unconditional) mean of y will be given by (A) 0.2 (B) 0.4 (C) 0.5 (D) 0.33" |
| Q119 | 18 | task_taxonomy | "A point pole has a strength of 4π × 10−4 weber. The force in newtons on a point pole of 4π × 1.5 × 10−4 weber placed at a distance of 10 cm from it will be (A) 15 N. (B) 20 N. (C) 7.5 N. (D) 3.75 N." |
| Q120 | 18 | task_taxonomy | "A total of 30 players will play basketball at a park. There will be exactly 5 players on each team. Which statement correctly explains how to find the number of teams needed? (A) Add 5 to 30 to find 35 teams. (B) Divide 30 by 5 to find 6 teams. (C) Multiply 30 and 5 to find 150 teams. (D) Subtract 5 from 30 to find 25 teams." |
| Q121 | 18 | task_taxonomy | "Determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. E ⊃ (F · E) and ∼ E · F (A) Logically equivalent (B) Contradictory (C) Neither logically equivalent nor contradictory, but consistent (D) Inconsistent" |
| Q122 | 18 | task_taxonomy | "As of 2017, how many of the world's 1-year-old children today have been vaccinated against some disease? (A) 80% (B) 60% (C) 40% (D) 20%" |
| Q123 | 18 | task_taxonomy | "Homologous structures are often cited as evidence for the process of natural selection. All of the following are examples of homologous structures EXCEPT (A) the wings of a bird and the wings of a bat (B) the flippers of a whale and the arms of a man (C) the pectoral fins of a porpoise and the flippers of a seal (D) the forelegs of an insect and the forelimbs of a dog" |
| Q124 | 18 | task_taxonomy | "From the solubility rules, which of the following is true? (A) All chlorides, bromides, and iodides are soluble (B) All sulfates are soluble (C) All hydroxides are soluble (D) All ammonium-containing compounds are soluble" |
| Q125 | 19 | task_taxonomy | "A list of numbers has n elements, indexed from 1 to n. The following algorithm is intended to display the number of elements in the list that have a value greater than 100. The algorithm uses the variables count and position. Steps 3 and 4 are missing." |
| Q126 | 19 | task_taxonomy | "Which of the following could be used to replace steps 3 and 4 so that the algorithm works as intended?" |
| Q127 | 19 | task_taxonomy | "Figure 34: A High School Computer Science example." |
| Q128 | 19 | task_taxonomy | "This question refers to the following information." |
| Q129 | 19 | task_taxonomy | "From the passage, one may infer that the English Parliament wished to argue that the Act of Supremacy would" |
| Q130 | 19 | task_taxonomy | "Figure 35: A High School European History example." |
| Q131 | 19 | task_taxonomy | "During the third stage of the demographic transition model, which of the following is true?" |
| Q132 | 19 | task_taxonomy | "Figure 36: A High School Geography example." |
| Q133 | 20 | task_taxonomy | "Figure 37: A High School Government and Politics example." |
| Q134 | 20 | task_taxonomy | "Figure 38: A High School Macroeconomics example." |
| Q135 | 20 | task_taxonomy | "Figure 39: A High School Mathematics example." |
| Q136 | 20 | task_taxonomy | "Figure 40: A High School Microeconomics example." |
| Q137 | 20 | task_taxonomy | "Figure 41: A High School Physics example." |
| Q138 | 20 | task_taxonomy | "Figure 42: A High School Psychology example." |
| Q139 | 21 | task_taxonomy | "Figure 43: A High School Statistics example." |
| Q140 | 21 | task_taxonomy | "Figure 44: A High School US History example." |
| Q141 | 21 | task_taxonomy | "Figure 45: A High School World History example." |
| Q142 | 21 | task_taxonomy | "Figure 46: A Human Aging example." |
| Q143 | 22 | task_taxonomy | "Morning sickness is typically a problem: (A) during the first trimester (B) during the second trimester (C) during the third trimester (D) all through the pregnancy" |
| Q144 | 22 | task_taxonomy | "Would a reservation to the definition of torture in the ICCPR be acceptable in contemporary practice? (A) This is an acceptable reservation if the reserving country's legislation employs a different definition (B) This is an unacceptable reservation because it contravenes the object and purpose of the ICCPR (C) This is an unacceptable reservation because the definition of torture in the ICCPR is consistent with customary international law (D) This is an acceptable reservation because under general international law States have the right to enter reservations to treaties" |
| Q145 | 22 | task_taxonomy | "Which position does Rawls claim is the least likely to be adopted by the POP (people in the original position)? (A) The POP would choose equality above liberty. (B) The POP would opt for the 'maximin' strategy. (C) The POP would opt for the 'difference principle.' (D) The POP would reject the 'system of natural liberty.'" |
| Q146 | 22 | task_taxonomy | "John Stuart Mill: Each person's happiness is a good to that person, and the general happiness, therefore, a good to the aggregate of all persons. (A) Fallacy of Composition (B) Fallacy of Division (C) Gambler's Fallacy (D) Equivocation" |
| Q147 | 22 | task_taxonomy | "A 6-sided die is rolled 15 times and the results are: side 1 comes up 0 times; side 2: 1 time; side 3: 2 times; side 4: 3 times; side 5: 4 times; side 6: 5 times. Based on these results, what is the probability of side 3 coming up when using Add-1 Smoothing? (A) 2/15 (B) 1/7 (C) 3/16 (D) 1/5" |
| Q148 | 22 | task_taxonomy | "According to Lewin, Lippet and White's 1939 experiment, which form of leadership produced the most work from participants? (A) Laissez-faire (B) Democratic (C) Authoritarian (D) A mix of laissez-faire and democratic" |
| Q149 | 23 | stated_limitations | "The formatting of this task hinders UnifiedQA performance substantially." |
| Q150 | 24 | task_taxonomy | "According to Moore's "ideal utilitarianism," the right action is the one that brings about the greatest amount of: (A) pleasure. (B) happiness. (C) good. (D) virtue." |
| Q151 | 24 | task_taxonomy | "Researchers now believe that the decline of the Maya was caused chiefly by: (A) a cataclysm of some kind, such as an earthquake, volcano, or tsunami. (B) ecological degradation resulting from slash-and-burn farming techniques. (C) endless wars between neighboring Mayan city-states. (D) practices of interbreeding that led to a steep rise in congenital disorders." |
| Q152 | 24 | task_taxonomy | "Krete is an unmarried taxpayer with income exclusively from wages. By December 31, year 1, Krete's employer has withheld $16,000 in federal income taxes and Krete has made no estimated tax payments. On April 15, year 2, Krete timely filed for an extension request to file her individual tax return, and paid $300 of additional taxes. Krete's year 1 tax liability was $16,500 when she timely filed her return on April 30, year 2, and paid the remaining tax liability balance. What amount would be subject to the penalty for underpayment of estimated taxes? (A) $0 (B) $500 (C) $1,650 (D) $16,500" |
| Q153 | 24 | task_taxonomy | "The night before his bar examination, the examinee's next-door neighbor was having a party. The music from the neighbor's home was so loud that the examinee couldn't fall asleep. The examinee called the neighbor and asked her to please keep the noise down. The neighbor then abruptly hung up. Angered, the examinee went into his closet and got a gun. He went outside and fired a bullet through the neighbor's living room window. Not intending to shoot anyone, the examinee fired his gun at such an angle that the bullet would hit the ceiling. He merely wanted to cause some damage to the neighbor's home to relieve his angry rage. The bullet, however, ricocheted off the ceiling and struck a partygoer in the back, killing him. The jurisdiction makes it a misdemeanor to discharge a firearm in public. The examinee will most likely be found guilty for which of the following crimes in connection to the death of the partygoer? (A) Murder. (B) Involuntary manslaughter. (C) Voluntary manslaughter. (D) Discharge of a firearm in public." |
| Q154 | 25 | task_taxonomy | "A 63-year-old man is brought to the emergency department because of a 4-day history of increasingly severe left leg pain and swelling of his left calf. He also has a 1-month history of increasingly severe upper midthoracic back pain. During this time, he has had a 9-kg (20-lb) weight loss despite no change in appetite. He has no history of major medical illness. His only medications is ibuprofen. He is 180 cm (5 ft 11 in) tall and weighs 82 kg (180 lb); BMI is 25 kg/m2. His vital signs are within normal limits. On examination, lower extremity pulses are palpable bilaterally. The remainder of the physical examination shows no abnormalities. An x-ray of the thoracic spine shows no abnormalities. A CT scan of the abdomen shows a 3-cm mass in the body of the pancreas; there are liver metastases and encasement of the superior mesenteric artery. Ultrasonography of the left lower extremity shows a femoropopliteal venous clot. Which of the following is the most likely cause of this patient's symptoms?" |
| Q155 | 25 | task_taxonomy | "The technique that is most likely to produce an immediate improvement in the behavior of a child who hits others and rips up schoolbooks is" |
| Q156 | 25 | task_taxonomy | "You work for a utility company that is building a biomass plant in the community. Your employer asks you to give a series of community talks about the plant and future operations. You visit the plant several hours before you are due to give a speech that has been prepared by your immediate supervisor. During the tour of the plant, you discover several claims in the speech are not true. What do you do?" |
| Q157 | 26 | task_taxonomy | "Which of the following statements most closely corresponds with differential association theory?" |
| Q158 | 26 | task_taxonomy | "Why did Congress oppose Wilson's proposal for the League of Nations?" |
| Q159 | 26 | task_taxonomy | "An observational study in diabetics assesses the role of an increased plasma fibrinogen level on the risk of cardiac events. 130 diabetic patients are followed for 5 years to assess the development of acute coronary syndrome. In the group of 60 patients with a normal baseline plasma fibrinogen level, 20 develop acute coronary syndrome and 40 do not. In the group of 70 patients with a high baseline plasma fibrinogen level, 40 develop acute coronary syndrome and 30 do not. Which of the following is the best estimate of relative risk in patients with a high baseline plasma fibrinogen level compared to patients with a normal baseline plasma fibrinogen level?" |
| Q160 | 27 | task_taxonomy | "Figure 70: A World Religions example." |

### Category Index
- **task_taxonomy**: Q1, Q2, Q8, Q10, Q15, Q16, Q18, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q49, Q51, Q75, Q76, Q80, Q82, Q93, Q104, Q105, Q106, Q107, Q108, Q109, Q110, Q111, Q112, Q113, Q114, Q115, Q116, Q117, Q118, Q119, Q120, Q121, Q122, Q123, Q124, Q125, Q126, Q127, Q128, Q129, Q130, Q131, Q132, Q133, Q134, Q135, Q136, Q137, Q138, Q139, Q140, Q141, Q142, Q143, Q144, Q145, Q146, Q147, Q148, Q150, Q151, Q152, Q153, Q154, Q155, Q156, Q157, Q158, Q159, Q160
- **data_sources**: Q17, Q60, Q69, Q71, Q101
- **data_format**: Q7, Q19, Q20, Q44, Q91, Q94
- **label_categories**: Q83
- **annotation_process**: NO QUOTES — paper is silent
- **evaluation_metrics**: Q3, Q11, Q21, Q22, Q23, Q34, Q35, Q36, Q37, Q38, Q39, Q40, Q41, Q43, Q45, Q46, Q47, Q48, Q55, Q56, Q58, Q61, Q62, Q70, Q81, Q84, Q85, Q86, Q88, Q96, Q97, Q103
- **stated_limitations**: Q4, Q5, Q6, Q12, Q13, Q14, Q42, Q50, Q52, Q53, Q54, Q57, Q59, Q63, Q64, Q65, Q66, Q67, Q68, Q72, Q73, Q74, Q87, Q89, Q90, Q92, Q95, Q98, Q99, Q100, Q102, Q149
- **authors_affiliations**: Q9, Q77, Q78, Q79
