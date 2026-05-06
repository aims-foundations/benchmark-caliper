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
| Q7 | 1 | evaluation_metrics | "By comprehensively evaluating the breadth and depth of a model's academic and professional understanding, our test can be used to analyze models across many tasks and to identify important shortcomings." |
| Q8 | 1 | data_format | "We design the benchmark to measure knowledge acquired during pretraining by evaluating models exclusively in zero-shot and few-shot settings." |
| Q9 | 1 | task_taxonomy | "The benchmark covers 57 subjects across STEM, the humanities, the social sciences, and more. It ranges in difficulty from an elementary level to an advanced professional level, and it tests both world knowledge and problem solving ability." |
| Q10 | 1 | authors_affiliations | "Dan Hendrycks, UC Berkeley; Collin Burns, Columbia University; Steven Basart, UChicago; Andy Zou, UC Berkeley; Mantas Mazeika, UIUC; Dawn Song, UC Berkeley; Jacob Steinhardt, UC Berkeley" |
| Q11 | 2 | task_taxonomy | "Since our test consists in 57 tasks, it can be used to analyze aggregate properties of models across tasks and to track important shortcomings." |
| Q12 | 2 | evaluation_metrics | "few-shot models up to 13 billion parameters (Brown et al., 2020) achieve random chance performance of 25% accuracy, but the 175 billion parameter GPT-3 model reaches a much higher 43.9% accuracy" |
| Q13 | 2 | stated_limitations | "unlike human professionals GPT-3 does not excel at any single subject. Instead, we find that performance is lopsided, with GPT-3 having almost 70% accuracy for its best subject but near-random performance for several other subjects." |
| Q14 | 2 | stated_limitations | "The tasks with near-random accuracy include calculation-heavy subjects such as physics and mathematics and subjects related to human values such as law and morality." |
| Q15 | 2 | stated_limitations | "GPT-3 does not have an accurate sense of what it does or does not know since its average confidence can be up to 24% off from its actual accuracy." |
| Q16 | 2 | data_sources | "The dominant paradigm in NLP is to pretrain large models on massive text corpora including educational books and websites." |
| Q17 | 2 | task_taxonomy | "Many recent benchmarks aim to assess a model's general world knowledge and basic reasoning ability by testing its "commonsense."" |
| Q18 | 3 | task_taxonomy | "We create a massive multitask test consisting of multiple-choice questions from various branches of knowledge. The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn. There are 57 tasks in total, which is also the number of Atari games (Bellemare et al., 2013), all of which are listed in Appendix B." |
| Q19 | 3 | data_sources | "The questions in the dataset were manually collected by graduate and undergraduate students from freely available sources online. These include practice questions for tests such as the Graduate Record Examination and the United States Medical Licensing Examination. It also includes questions designed for undergraduate courses and questions designed for readers of Oxford University Press books." |
| Q20 | 3 | label_categories | "Some tasks cover a subject, like psychology, but at a specific level of difficulty, such as "Elementary," "High School," "College," or "Professional."" |
| Q21 | 3 | data_format | "We collected 15908 questions in total, which we split into a few-shot development set, a validation set, and a test set. The few-shot development set has 5 questions per subject, the validation set may be used for selecting hyperparameters and is made of 1540 questions, and the test set has 14079 questions. Each subject contains 100 test examples at the minimum, which is longer than most exams designed to assess people." |
| Q22 | 3 | evaluation_metrics | "Human-level accuracy on this test varies. Unspecialized humans from Amazon Mechanical Turk obtain 34.5% accuracy on this test. Meanwhile, expert-level performance can be far higher. For example, real-world test-taker human accuracy at the 95th percentile is around 87% for US Medical Licensing Examinations, and these questions make up our "Professional Medicine" task. If we take the 95th percentile human test-taker accuracy for exams that build up our test, and if we make an educated guess when such information is unavailable, we then estimate that expert-level accuracy is approximately 89.8%." |
| Q23 | 3 | evaluation_metrics | "we instead create a simple-to-evaluate test that measures classification accuracy on multiple choice questions." |
| Q24 | 3 | stated_limitations | "Since our test aggregates different subjects and several levels of difficulty, we measure more than straightforward commonsense or narrow linguistic understanding." |
| Q25 | 4 | task_taxonomy | "The humanities is a group of disciplines that make use of qualitative analysis and analytic methods rather than scientific empirical methods. Branches of the humanities include law, philosophy, history, and so on (Appendix B)." |
| Q26 | 4 | task_taxonomy | "Mastering these subjects requires a variety of skills. For example, legal understanding requires knowledge of how to apply rules and standards to complex scenarios, and also provide answers with stipulations and explanations." |
| Q27 | 4 | task_taxonomy | "For philosophy, our questions cover concepts like logical fallacies, formal logic, and famous philosophical arguments. It also covers moral scenarios, including questions from the ETHICS dataset (Hendrycks et al., 2020) that test a model's understanding of normative statements through predicting widespread moral intuitions about diverse everyday scenarios." |
| Q28 | 4 | task_taxonomy | "Finally, our history questions cover a wide range of time periods and geographical locations, including prehistory and other advanced subjects." |
| Q29 | 4 | task_taxonomy | "Social science includes branches of knowledge that examine human behavior and society. Subject areas include economics, sociology, politics, geography, psychology, and so on." |
| Q30 | 4 | task_taxonomy | "Our economics questions include microeconomics, macroeconomics, and econometrics, and cover different types of problems, including questions that require a mixture of world knowledge, qualitative reasoning, or quantitative reasoning." |
| Q31 | 4 | task_taxonomy | "We also include important but more esoteric topics such as security studies in order to test the boundaries of what is experienced and learned during pretraining." |
| Q32 | 4 | task_taxonomy | "Social science also includes psychology, a field that may be especially important for attaining a nuanced understanding of humans." |
| Q33 | 4 | task_taxonomy | "STEM subjects include physics, computer science, mathematics, and more." |
| Q34 | 4 | task_taxonomy | "Conceptual physics tests understanding of simple physics principles and may be thought" |
| Q35 | 5 | evaluation_metrics | "To measure performance on our multitask test, we compute the classification accuracy across all examples and tasks." |
| Q36 | 5 | authors_affiliations | "We evaluate GPT-3 (Brown et al., 2020) and UnifiedQA (Khashabi et al., 2020)." |
| Q37 | 5 | evaluation_metrics | "For GPT-3 we use the OpenAI API, which provides access to four model variants, "Ada," "Babbage," "Curie," and "Davinci," which we refer to as "Small" (2.7 billion parameters), "Medium" (6.7 billion), "Large" (13 billion) and "X-Large" (175 billion)." |
| Q38 | 5 | evaluation_metrics | "UnifiedQA uses the T5 (Raffel et al., 2019) text-to-text backbone and is fine-tuned on previously proposed question answering datasets (Lai et al., 2017), where the prediction is the class with the highest token overlap with UnifiedQA's text output." |
| Q39 | 5 | evaluation_metrics | "Since UnifiedQA is fine-tuned on other datasets, we evaluate it without any further tuning to assess its transfer accuracy." |
| Q40 | 5 | evaluation_metrics | "We also fine-tune RoBERTa-base, ALBERT-xxlarge, and GPT-2 on UnifiedQA training data and our dev+val set." |
| Q41 | 5 | evaluation_metrics | "We primarily focus on UnifiedQA and GPT-3 in the rest of this document, but additional discussion of RoBERTa, ALBERT, and GPT-2 is in Appendix A." |
| Q42 | 5 | evaluation_metrics | "All values are percentages." |
| Q43 | 5 | stated_limitations | "Some models proposed in the past few months can move several percent points beyond random chance." |
| Q44 | 5 | evaluation_metrics | "GPT-3 uses few-shot learning and UnifiedQA is tested under distribution shift." |
| Q45 | 6 | data_format | "We feed GPT-3 prompts like that shown in Figure 1a. We begin each prompt with "The following are multiple choice questions (with answers) about [subject]." For zero-shot evaluation, we append the question to the prompt. For few-shot evaluation, we add up to 5 demonstration examples with answers to the prompt before appending the question. All prompts end with "Answer: ". The model then produces probabilities for the tokens "A," "B," "C," and "D," and we treat the highest probability option as the prediction." |
| Q46 | 6 | data_format | "For consistent evaluation, we create a dev set with 5 fixed few-shot examples for each subject." |
| Q47 | 6 | evaluation_metrics | "We find that the three smaller GPT-3 models have near random accuracy (around 25%). In contrast, we find that the X-Large 175 billion parameter GPT-3 model performs substantially better than random, with an accuracy of 43.9%." |
| Q48 | 6 | evaluation_metrics | "While the smaller models have around 25% zero-shot accuracy, Figure 10 in Appendix A shows that the largest GPT-3 model has a much higher zero-shot accuracy of about 37.7%." |
| Q49 | 6 | evaluation_metrics | "The largest UnifiedQA model we test has 11 billion parameters, which is slightly smaller than GPT-3 Large. Nevertheless, we show in Table 1 that it attains 48.9% accuracy." |
| Q50 | 6 | evaluation_metrics | "We also find that even the smallest UnifiedQA variant, with just 60 million parameters, has approximately 29.3% accuracy." |
| Q51 | 6 | stated_limitations | "These results suggest that while model size is a key component for achieving strong performance, fine-tuning also helps." |
| Q52 | 6 | evaluation_metrics | "Figure 6 shows the accuracy of GPT-3 (few-shot) and UnifiedQA for all 57 tasks. It shows the both models are below expert-level performance for all tasks, with GPT-3's accuracy ranging from 69% for US Foreign Policy to 26% for College Chemistry." |
| Q53 | 6 | evaluation_metrics | "UnifiedQA does best on marketing, with an accuracy of 82.5%." |
| Q54 | 6 | stated_limitations | "Overall, models do poorly on highly procedural problems. Figure 6 shows that calculation-heavy STEM subjects tend to have low accuracy compared to verbal subjects." |
| Q55 | 6 | evaluation_metrics | "For GPT-3, 9 out of the 10 lowest-accuracy tasks are STEM subjects that emphasize mathematics or calculations. We speculate that is in part because GPT-3 acquires declarative knowledge more readily than procedural knowledge." |
| Q56 | 7 | task_taxonomy | "For example, many questions in Elementary Mathematics require applying the order of operations for arithmetic, which is described by the acronym PEMDAS (Parentheses Exponents Multiplication Division Addition Subtraction)." |
| Q57 | 7 | stated_limitations | "We confirm that GPT-3 is aware of the acronym PEMDAS. However, it does not consistently apply PEMDAS to actual problems." |
| Q58 | 7 | task_taxonomy | "We find that some verbal tasks such as Moral Scenarios from Hendrycks et al. (2020) and Professional Law also have especially low accuracy." |
| Q59 | 7 | stated_limitations | "GPT-3 does better on College Medicine (47.4%) and College Mathematics (35.0%) than calculation-heavy Elementary Mathematics (29.9%)." |
| Q60 | 7 | evaluation_metrics | "We evaluate the calibration of GPT-3 by testing how well its average confidence estimates its actual accuracy for each subject." |
| Q61 | 7 | stated_limitations | "GPT-3 is uncalibrated. In fact, its confidence is only weakly related to its actual accuracy in the zero-shot setting, with the difference between its accuracy and confidence reaching up to 24% for some subjects." |
| Q62 | 7 | evaluation_metrics | "Another calibration measure is the Root Mean Squared (RMS) calibration error (Hendrycks et al., 2019a; Kumar et al., 2019). Many tasks have miscalibrated predictions, such as Elementary Mathematics which has a zero-shot RMS calibration error of 19.4%." |
| Q63 | 7 | data_sources | "A major distinction between our benchmark and previous multitask NLP benchmarks is that we do not require large training sets. Instead, we assume that models have acquired the requisite knowledge from reading vast quantities of diverse text from the Internet." |
| Q64 | 7 | stated_limitations | "While text is capable of conveying an enormous number of concepts about the world, many important concepts are conveyed mainly through other modalities, such as images, audio, and physical interaction (Bisk et al., 2020). Existing large-scale NLP models, such as GPT-3, do not incorporate multimodal information, so we design our benchmark to capture a diverse array of tasks in a text-only format." |
| Q65 | 8 | task_taxonomy | "This motivates us to propose a methodological change so that models are trained more like how humans learn." |
| Q66 | 8 | evaluation_metrics | "For this reason we assess pretrained models in a zero-shot, few-shot, or transfer setting and we provide a dev, val, and test set for each task." |
| Q67 | 8 | evaluation_metrics | "The dev set is used for few-shot prompts, the val set could be used for hyperparameter tuning, and the test set is used to compute the final accuracy." |
| Q68 | 8 | evaluation_metrics | "Importantly, the format of our evaluation is not identical to the format in which information is acquired during pretraining." |
| Q69 | 8 | stated_limitations | "This has the benefit of obviating concerns about spurious training set annotation artifacts (Geirhos et al., 2020; Hendrycks et al., 2019b) and is in stark contrast to the previous paradigm of identically distributed training and test sets." |
| Q70 | 8 | stated_limitations | "We find that current large-scale Transformers have wide room for improvement." |
| Q71 | 8 | stated_limitations | "They are notably poor at modeling human (dis)approval, as evident by the low performance on the Professional Law and Moral Scenarios tasks." |
| Q72 | 8 | stated_limitations | "Models also have difficulty performing calculations, so much so that they exhibit poor performance on Elementary Mathematics and many other STEM subjects with "plug and chug" problems." |
| Q73 | 8 | stated_limitations | "Additionally, they do not match expert-level performance (90%) on any subject, so for all subjects it is subhuman." |
| Q74 | 8 | stated_limitations | "On average, models are only now starting to move beyond random-chance accuracy levels." |
| Q75 | 8 | data_sources | "We collected approximately 2,000 additional Professional Law training examples." |
| Q76 | 8 | evaluation_metrics | "After fine-tuning a RoBERTa-base model (Liu et al., 2019) using this custom training set, our model attained 32.8% test accuracy." |
| Q77 | 8 | data_sources | "We also had RoBERTa continue pretraining on approximately 1.6 million legal case summaries using Harvard's Law Library case law corpus case.law, but after fine-tuning it only attained 36.1% accuracy." |
| Q78 | 8 | stated_limitations | "This suggests that while additional pretraining on relevant high quality text can help, it may not be enough to substantially increase the performance of current models." |
| Q79 | 8 | stated_limitations | "It is unclear whether simply scaling up existing language models will solve the test." |
| Q80 | 8 | stated_limitations | "Current understanding indicates that a 10× increase in model size must be accompanied by an approximate 5× increase in data (Kaplan et al., 2020)." |
| Q81 | 8 | stated_limitations | "Data may also become a bottleneck, as there is far less written about esoteric branches of knowledge than about everyday situations." |
| Q82 | 8 | task_taxonomy | "We introduced a new test that measures how well text models can learn and apply knowledge encountered during pretraining." |
| Q83 | 8 | task_taxonomy | "By covering 57 subjects at varying levels of difficulty, the test assesses language understanding in greater breadth and depth than previous benchmarks." |
| Q84 | 8 | stated_limitations | "We found that it has recently become possible for models to make meaningful progress on the test, but that state-of-the-art models have lopsided performance and rarely excel at any individual task." |
| Q85 | 8 | stated_limitations | "We also showed that current models are uncalibrated and have difficulty with tasks that require calculations." |
| Q86 | 8 | stated_limitations | "Worryingly, models also perform especially poorly on socially relevant subjects including morality and law." |
| Q87 | 9 | authors_affiliations | "DH is supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship." |
| Q88 | 9 | authors_affiliations | "This research was also supported by the NSF Frontier Award 1804794." |
| Q89 | 11 | task_taxonomy | "This appendix includes figures with sorted results (Figure 9), few-shot examples vs. accuracy (Figure 10), and few-shot calibration (Figure 11). It also includes sections on fine-tuning, error analysis, and format sensitivity." |
| Q90 | 11 | stated_limitations | "We primarily analyzed models with more than 10 billion parameters in the main body of the paper." |
| Q91 | 11 | task_taxonomy | "For this section, we analyze smaller models including RoBERTa-base (125 million parameters) (Liu" |
| Q92 | 11 | evaluation_metrics | "On the left are GPT-3 few shot accuracies for all of the 57 tasks. On the right are UnifiedQA transfer accuracies for all of the 57 tasks. For both models, capabilities are lopsided." |
| Q93 | 12 | evaluation_metrics | "Models are fine-tuned to predict one of four classes using the UnifiedQA MCQ questions and using our dev+val set. We test on our multitask test set." |
| Q94 | 12 | evaluation_metrics | "RoBERTa-base attains an overall accuracy of 27.9%, with 27.9% accuracy for the humanities, 28.8% for social sciences, 27.0% for STEM, and 27.7% for other." |
| Q95 | 12 | evaluation_metrics | "ALBERT-xxlarge attains an accuracy of 27.1%, with 27.2% accuracy for the humanities, 25.7% for the social sciences, 27.7% for STEM, and 27.9% for other." |
| Q96 | 12 | evaluation_metrics | "GPT-2 attains an accuracy of 32.4%, with 32.8% accuracy for the humanities, 33.3% for the social sciences, 30.2% for STEM, and 33.1% for other." |
| Q97 | 12 | evaluation_metrics | "Compare this to UnifiedQA's smallest variant, which has just 60 million parameters and approximately 29.3% accuracy. It obtains higher accuracy than RoBERTa and ALBERT, even though it has fewer parameters." |
| Q98 | 12 | evaluation_metrics | "UnifiedQA with 3 billion parameters attains 43.7%, while the similarly sized GPT-2 model with 1.5 billion parameters attains 32.4% accuracy." |
| Q99 | 12 | stated_limitations | "We qualitatively analyze when GPT-3 makes high confidence mistakes. We find that while many of these mistakes were clearly wrong, many were mistakes that a human might make." |
| Q100 | 12 | stated_limitations | "While different question formatting choices often lead to similar GPT-3 accuracies, we find that UnifiedQA is more sensitive." |
| Q101 | 12 | data_format | "UnifiedQA's input format is of the form QUESTION1 \\n (A) CHOICE1 (B) CHOICE2 (C) CHOICE3 (D) CHOICE4</s> where questions and choices are normalized and made lowercase." |
| Q102 | 12 | stated_limitations | "If we remove the </s> from the input, accuracy declines by several percentage points." |
| Q103 | 13 | task_taxonomy | "We provide analysis of question length and difficulty in Figure 12. We list all tasks and the topics they test in Table 2. We also provide an example for each task starting with Figure 14." |
| Q104 | 13 | stated_limitations | "Since language models train on vast text corpora, there is some chance that they have seen the exact question and answer during pretraining. If they memorized the exact question and answer, then they would attain higher accuracy than their true ability. Likewise, a question's entropy would be especially low if it were memorized. Memorized questions and answers should have low entropy and" |
| Q105 | 13 | data_format | "For questions longer than a tweet (280 characters), the correlation between question length and true label confidence is slightly positive. This shows that longer questions are not necessarily harder." |
| Q106 | 13 | evaluation_metrics | "While models are more calibrated in a few-shot setting than a zero-shot setting, they are still miscalibrated, with gap between accuracy and confidence reaching up to 14%. Here the correlation between confidence and accuracy is r = 0.81, compared to r = 0.63 in the zero-shot setting." |
| Q107 | 14 | stated_limitations | "However, in Figure 13, we see that accuracy and question entropy are not positively correlated, suggesting that the test's low-entropy questions do not correspond to memorized (and thereby correctly predicted) answers." |
| Q108 | 14 | stated_limitations | "This suggests that our exact questions were not memorized." |
| Q109 | 14 | stated_limitations | "However, during pretraining models encountered text related to our questions through processing Wikipedia." |
| Q110 | 14 | data_sources | "We also note that most of our questions came from PDFs or websites where questions and answers are on separate pages." |
| Q111 | 14 | stated_limitations | "See Brown et al. (2020) for a previous discussion of contamination showing that the phenomena hardly affects performance." |
| Q112 | 14 | stated_limitations | "To reduce the probability that future models encounter exact questions during test-time, we will provide a list of question sources." |
| Q113 | 14 | evaluation_metrics | "The average log probability of the question (without answer) is not strongly positively correlated with accuracy, all else equal." |
| Q114 | 14 | evaluation_metrics | "Each point corresponds to a task." |
| Q115 | 14 | evaluation_metrics | "Higher log probability indicates higher compression, and especially high log probability would suggest memorization." |
| Q116 | 14 | evaluation_metrics | "In the zero-shot question prompt, the correlation between average log probability and accuracy is r = −0.43, and for the few-shot setting the correlation is r = −0.56." |
| Q117 | 15 | task_taxonomy | "Table 2: Summary of all 57 tasks." |
| Q118 | 16 | task_taxonomy | "Find all c in Z₃ such that Z₃[x]/(x² + c) is a field." |
| Q119 | 16 | task_taxonomy | "What is the embryological origin of the hyoid bone?" |
| Q120 | 16 | task_taxonomy | "Why isn't there a planet where the asteroid belt is located?" |
| Q121 | 16 | task_taxonomy | "Three contrasting tactics that CSO's can engage in to meet their aims are which typically involves research and communication, , which may involve physically attacking a company's operations or , often involving some form of ." |
| Q122 | 16 | task_taxonomy | "How many attempts should you make to cannulate a patient before passing the job on to a senior colleague?" |
| Q123 | 16 | task_taxonomy | "In a given population, 1 out of every 400 people has a cancer caused by a completely recessive allele, b. Assuming the population is in Hardy-Weinberg equilibrium, which of the following is the expected proportion of individuals who carry the b allele but are not expected to develop the cancer?" |
| Q124 | 16 | task_taxonomy | "Which of the following statements about the lanthanide elements is NOT true?" |
| Q125 | 17 | task_taxonomy | "Consider a computer design in which multiple processors, each with a private cache memory, share global memory using a single bus. This bus is the critical system resource. Each processor can execute one instruction every 500 nanoseconds as long as memory references are satisfied by its local cache. When a cache miss occurs, the processor is delayed for an additional 2,000 nanoseconds. During half of this additional delay, the bus is dedicated to serving the cache miss. During the other half, the processor cannot continue, but the bus is free to service requests from other processors. On average, each instruction requires 2 memory references. On average, cache misses occur on 1 percent of references. What proportion of the capacity of the bus would a single processor consume, ignoring delays due to competition from other processors?" |
| Q126 | 17 | task_taxonomy | "Let A be a real 2 × 2 matrix. Which of the following statements must be true? I. All of the entries of A2are nonnegative. II. The determinant of A2is nonnegative. III. If A has two distinct eigenvalues, then A2 has two distinct eigenvalues." |
| Q127 | 17 | task_taxonomy | "In a genetic test of a newborn, a rare genetic disorder is found that has X-linked recessive transmission. Which of the following statements is likely true regarding the pedigree of this disorder?" |
| Q128 | 17 | task_taxonomy | "One end of a Nichrome wire of length 2L and cross-sectional area A is attached to an end of another Nichrome wire of length L and cross- sectional area 2A. If the free end of the longer wire is at an electric potential of 8.0 volts, and the free end of the shorter wire is at an electric potential of 1.0 volt, the potential at the junction of the two wires is most nearly equal to" |
| Q129 | 17 | task_taxonomy | "Why is it that anti-virus scanners would not have found an exploitation of Heartbleed?" |
| Q130 | 17 | task_taxonomy | "A model airplane flies slower when flying into the wind and faster with wind at its back. When launched at right angles to the wind, a cross wind, its groundspeed compared with flying in still air is" |
| Q131 | 18 | task_taxonomy | "Consider the following AR(1) model with the disturbances having zero mean and unit variance yt = 0.2 + 0.4yt−1 + ut The (unconditional) mean of y will be given by (A) 0.2 (B) 0.4 (C) 0.5 (D) 0.33" |
| Q132 | 18 | task_taxonomy | "A point pole has a strength of 4π × 10−4 weber. The force in newtons on a point pole of 4π × 1.5 × 10−4 weber placed at a distance of 10 cm from it will be (A) 15 N. (B) 20 N. (C) 7.5 N. (D) 3.75 N." |
| Q133 | 18 | task_taxonomy | "A total of 30 players will play basketball at a park. There will be exactly 5 players on each team. Which statement correctly explains how to find the number of teams needed? (A) Add 5 to 30 to find 35 teams. (B) Divide 30 by 5 to find 6 teams. (C) Multiply 30 and 5 to find 150 teams. (D) Subtract 5 from 30 to find 25 teams." |
| Q134 | 18 | task_taxonomy | "Determine whether the statements are logically equivalent or contradictory. If neither, determine whether they are consistent or inconsistent. E ⊃ (F · E) and ∼ E · F (A) Logically equivalent (B) Contradictory (C) Neither logically equivalent nor contradictory, but consistent (D) Inconsistent" |
| Q135 | 18 | task_taxonomy | "As of 2017, how many of the world's 1-year-old children today have been vaccinated against some disease? (A) 80% (B) 60% (C) 40% (D) 20%" |
| Q136 | 18 | task_taxonomy | "Homologous structures are often cited as evidence for the process of natural selection. All of the following are examples of homologous structures EXCEPT (A) the wings of a bird and the wings of a bat (B) the flippers of a whale and the arms of a man (C) the pectoral fins of a porpoise and the flippers of a seal (D) the forelegs of an insect and the forelimbs of a dog" |
| Q137 | 18 | task_taxonomy | "From the solubility rules, which of the following is true? (A) All chlorides, bromides, and iodides are soluble (B) All sulfates are soluble (C) All hydroxides are soluble (D) All ammonium-containing compounds are soluble" |
| Q138 | 19 | task_taxonomy | "A list of numbers has n elements, indexed from 1 to n. The following algorithm is intended to display the number of elements in the list that have a value greater than 100. The algorithm uses the variables count and position. Steps 3 and 4 are missing." |
| Q139 | 19 | task_taxonomy | "Which of the following could be used to replace steps 3 and 4 so that the algorithm works as intended?" |
| Q140 | 19 | data_sources | "This question refers to the following information." |
| Q141 | 19 | data_sources | "English Parliament, Act of Supremacy, 1534" |
| Q142 | 19 | task_taxonomy | "From the passage, one may infer that the English Parliament wished to argue that the Act of Supremacy would" |
| Q143 | 19 | task_taxonomy | "During the third stage of the demographic transition model, which of the following is true?" |
| Q144 | 20 | task_taxonomy | "Figure 37: A High School Government and Politics example." |
| Q145 | 20 | task_taxonomy | "Figure 38: A High School Macroeconomics example." |
| Q146 | 20 | task_taxonomy | "Figure 39: A High School Mathematics example." |
| Q147 | 20 | task_taxonomy | "Figure 40: A High School Microeconomics example." |
| Q148 | 20 | task_taxonomy | "Figure 41: A High School Physics example." |
| Q149 | 20 | task_taxonomy | "Figure 42: A High School Psychology example." |
| Q150 | 21 | task_taxonomy | "Figure 43: A High School Statistics example." |
| Q151 | 21 | task_taxonomy | "Figure 44: A High School US History example." |
| Q152 | 21 | task_taxonomy | "Figure 45: A High School World History example." |
| Q153 | 21 | task_taxonomy | "Figure 46: A Human Aging example." |
| Q154 | 22 | task_taxonomy | "Morning sickness is typically a problem: (A) during the first trimester (B) during the second trimester (C) during the third trimester (D) all through the pregnancy" |
| Q155 | 22 | task_taxonomy | "Would a reservation to the definition of torture in the ICCPR be acceptable in contemporary practice? (A) This is an acceptable reservation if the reserving country's legislation employs a different definition (B) This is an unacceptable reservation because it contravenes the object and purpose of the ICCPR (C) This is an unacceptable reservation because the definition of torture in the ICCPR is consistent with customary international law (D) This is an acceptable reservation because under general international law States have the right to enter reservations to treaties" |
| Q156 | 22 | task_taxonomy | "Which position does Rawls claim is the least likely to be adopted by the POP (people in the original position)? (A) The POP would choose equality above liberty. (B) The POP would opt for the 'maximin' strategy. (C) The POP would opt for the 'difference principle.' (D) The POP would reject the 'system of natural liberty.'" |
| Q157 | 22 | task_taxonomy | "John Stuart Mill: Each person's happiness is a good to that person, and the general happiness, therefore, a good to the aggregate of all persons. (A) Fallacy of Composition (B) Fallacy of Division (C) Gambler's Fallacy (D) Equivocation" |
| Q158 | 22 | task_taxonomy | "A 6-sided die is rolled 15 times and the results are: side 1 comes up 0 times; side 2: 1 time; side 3: 2 times; side 4: 3 times; side 5: 4 times; side 6: 5 times. Based on these results, what is the probability of side 3 coming up when using Add-1 Smoothing? (A) 2/15 (B) 1/7 (C) 3/16 (D) 1/5" |
| Q159 | 22 | task_taxonomy | "According to Lewin, Lippet and White's 1939 experiment, which form of leadership produced the most work from participants? (A) Laissez-faire (B) Democratic (C) Authoritarian (D) A mix of laissez-faire and democratic" |
| Q160 | 23 | stated_limitations | "Figure 57: A Moral Scenarios example. The formatting of this task hinders UnifiedQA performance substantially." |
| Q161 | 24 | task_taxonomy | "According to Moore's "ideal utilitarianism," the right action is the one that brings about the greatest amount of: (A) pleasure. (B) happiness. (C) good. (D) virtue." |
| Q162 | 24 | task_taxonomy | "Researchers now believe that the decline of the Maya was caused chiefly by: (A) a cataclysm of some kind, such as an earthquake, volcano, or tsunami. (B) ecological degradation resulting from slash-and-burn farming techniques. (C) endless wars between neighboring Mayan city-states. (D) practices of interbreeding that led to a steep rise in congenital disorders." |
| Q163 | 24 | task_taxonomy | "Krete is an unmarried taxpayer with income exclusively from wages. By December 31, year 1, Krete's employer has withheld $16,000 in federal income taxes and Krete has made no estimated tax payments. On April 15, year 2, Krete timely filed for an extension request to file her individual tax return, and paid $300 of additional taxes. Krete's year 1 tax liability was $16,500 when she timely filed her return on April 30, year 2, and paid the remaining tax liability balance. What amount would be subject to the penalty for underpayment of estimated taxes? (A) $0 (B) $500 (C) $1,650 (D) $16,500" |
| Q164 | 24 | task_taxonomy | "The night before his bar examination, the examinee's next-door neighbor was having a party. The music from the neighbor's home was so loud that the examinee couldn't fall asleep. The examinee called the neighbor and asked her to please keep the noise down. The neighbor then abruptly hung up. Angered, the examinee went into his closet and got a gun. He went outside and fired a bullet through the neighbor's living room window. Not intending to shoot anyone, the examinee fired his gun at such an angle that the bullet would hit the ceiling. He merely wanted to cause some damage to the neighbor's home to relieve his angry rage. The bullet, however, ricocheted off the ceiling and struck a partygoer in the back, killing him. The jurisdiction makes it a misdemeanor to discharge a firearm in public. The examinee will most likely be found guilty for which of the following crimes in connection to the death of the partygoer? (A) Murder. (B) Involuntary manslaughter. (C) Voluntary manslaughter. (D) Discharge of a firearm in public." |
| Q165 | 25 | authors_affiliations | "Published as a conference paper at ICLR 2021" |
| Q166 | 25 | task_taxonomy | "Figure 63: A Professional Medicine example." |
| Q167 | 25 | task_taxonomy | "Figure 64: A Professional Psychology example." |
| Q168 | 25 | task_taxonomy | "Figure 65: A Public Relations example." |
| Q169 | 26 | task_taxonomy | "Figure 66: A Security Studies example." |
| Q170 | 26 | task_taxonomy | "Figure 67: A Sociology example." |
| Q171 | 26 | task_taxonomy | "Figure 68: A US Foreign Policy example." |
| Q172 | 26 | task_taxonomy | "Figure 69: A Virology example." |
| Q173 | 27 | task_taxonomy | "Figure 70: A World Religions example." |

### Category Index
- **task_taxonomy**: Q1, Q2, Q9, Q11, Q17, Q18, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q56, Q58, Q65, Q82, Q83, Q89, Q91, Q103, Q117, Q118, Q119, Q120, Q121, Q122, Q123, Q124, Q125, Q126, Q127, Q128, Q129, Q130, Q131, Q132, Q133, Q134, Q135, Q136, Q137, Q138, Q139, Q142, Q143, Q144, Q145, Q146, Q147, Q148, Q149, Q150, Q151, Q152, Q153, Q154, Q155, Q156, Q157, Q158, Q159, Q161, Q162, Q163, Q164, Q166, Q167, Q168, Q169, Q170, Q171, Q172, Q173
- **data_sources**: Q16, Q19, Q63, Q75, Q77, Q110, Q140, Q141
- **data_format**: Q8, Q21, Q45, Q46, Q101, Q105
- **label_categories**: Q20
- **annotation_process**: NO QUOTES — paper is silent
- **evaluation_metrics**: Q3, Q7, Q12, Q22, Q23, Q35, Q37, Q38, Q39, Q40, Q41, Q42, Q44, Q47, Q48, Q49, Q50, Q52, Q53, Q55, Q60, Q62, Q66, Q67, Q68, Q76, Q92, Q93, Q94, Q95, Q96, Q97, Q98, Q106, Q113, Q114, Q115, Q116
- **stated_limitations**: Q4, Q5, Q6, Q13, Q14, Q15, Q24, Q43, Q51, Q54, Q57, Q59, Q61, Q64, Q69, Q70, Q71, Q72, Q73, Q74, Q78, Q79, Q80, Q81, Q84, Q85, Q86, Q90, Q99, Q100, Q102, Q104, Q107, Q108, Q109, Q111, Q112, Q160
- **authors_affiliations**: Q10, Q36, Q87, Q88, Q165
