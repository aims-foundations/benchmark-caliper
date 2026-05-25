I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **Grade School Math 8.5K (GSM8K)** is valid for use in **US K–8 Edtech: CCSS-Aligned Math Assessment Item Generation**.

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

- **Name**: gsm8k
- **Full Name**: Grade School Math 8.5K (GSM8K)
- **Domain**: Mathematical reasoning / grade school math word problems
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
GSM8K is organized around a single, undifferentiated task type: grade school math
word problems requiring multi-step arithmetic reasoning. The benchmark provides no
subdivision by mathematical domain, skill cluster, curriculum standard, or topic area
[Q1, Q11]. The paper explicitly frames the benchmark as probing "informal reasoning
ability" of language models [Q12] and contrasts it with harder benchmarks such as
MATH [Q20], but neither comparison introduces any finer-grained taxonomy. The
two methodological variants explored — finetuning versus verification, and token-level
versus solution-level verifiers [Q27, Q28, Q30, Q72, Q73] — both operate over the
same undifferentiated problem pool. Qualitative examples in the paper (books-by-weight
and dog food portions problems [Q128–Q136]) illustrate the general character of items
but confirm the total absence of curriculum-alignment tagging. For the deployment
context — generating items aligned to specific Common Core State Standards (CCSS) at
the standard-cluster level — this taxonomy represents a fundamental and consequential
ontological mismatch. There is no documented evidence that benchmark performance
correlates with ability to correctly operationalize a named standard such as 4.NF.A.2
or 6.RP.A.3.

### Input Content
GSM8K problems were authored by freelance contractors hired via Upwork and subsequently
scaled through Surge AI, an NLP data labeling platform [Q103, Q104]. Linguistic
diversity across problem phrasings was an explicit design goal [Q9], and contractors
were instructed to avoid reusing problem templates, with pairwise similarity scores
used as a quality-feedback mechanism [Q112, Q113]. Seed questions were auto-generated
from a few-shot prompted 175B GPT-3 model to assist contractors [Q110], introducing
an additional layer of culturally and stylistically shaped influence that is not
further characterized. The paper does not document the demographic composition,
geographic backgrounds, educational training, or linguistic profiles of the contractor
workforce. No cultural audit, inclusivity review, or equity guidelines are mentioned.
For the deployment context — which requires problems accessible across urban, suburban,
and rural US settings, inclusive of multilingual learners and students from diverse
socioeconomic backgrounds — the absence of documented cultural design guidelines in
the sourcing pipeline is a material validity gap. The requirement for low-idiom
language, avoidance of culturally narrow references, and sensitive treatment of
money-related contexts is entirely undocumented as a constraint in GSM8K's collection.

### Input Form
GSM8K problems and solutions are presented exclusively as English natural language
text [Q32, Q33]. The design preference for natural language solutions over pure
mathematical expressions was deliberate, intended to foster verbal analytical skills
and produce human-interpretable outputs [Q32, Q33]. The input modality is text-only,
with no audio, image, or other modality component. Calculator annotations are injected
into training solutions as additional tokens [Q40, Q119], but these are still
represented in text. For the deployment context, which is likewise text-based English,
there is no modality or script mismatch — this is the lowest-risk validity dimension.

### Output Ontology
GSM8K's output ontology is binary: solutions are labeled correct or incorrect based
solely on whether they reach the correct final numeric answer [Q60]. The verifier is
trained to output a scalar probability of solution correctness [Q59], and the
token-level variant extends this to a per-token value function [Q31, Q67, Q72, Q73].
At test time, performance is assessed by sampling a single solution and checking the
final answer [Q29, Q46], or by ranking multiple candidates via the verifier [Q3, Q68].
This output schema provides no taxonomic coverage of pedagogical dimensions —
distractor plausibility grounded in student misconceptions, CCSS standard alignment,
or grade-level language appropriateness are entirely absent from the label set.
For the deployment context, this is a critical and multidimensional mismatch: the
deployment's "correct" construct is a fully classroom-ready MCQ item package, and
GSM8K's binary numeric-answer label captures only a hard prerequisite (mathematical
accuracy) while leaving the large majority of the deployment's evaluation construct
completely unmeasured.

### Output Content
After initial problem writing, Surge AI contractors re-solved all problems (no worker
re-solving problems they originally authored), with disagreements triggering repair
or discard [Q105, Q106]. A second agreement check on a subset found a 1.7%
disagreement rate, interpreted as the fraction of problems containing breaking errors
or ambiguities [Q107, Q108], with the possibility of a higher rate of subtle errors
acknowledged [Q109]. Calculator annotations embedded in solutions were not produced
by human contractors but were auto-generated via hard-coded logic and a finetuned
language model [Q117], and the annotation logic is acknowledged as imperfect [Q118].
The paper does not document the demographic composition, geographic location,
educational background, or native language(s) of the annotators who labeled solution
correctness, nor does it report any stratified agreement analysis across annotator
subgroups. For the deployment context, the binary numeric-answer labels — even if
internally consistent — provide no information about distractor quality, misconception
grounding, or standard fidelity, so large portions of the deployment's output construct
are entirely unlabeled regardless of annotator quality.

### Output Form
GSM8K evaluates free-form natural language solution generation, with final performance
assessed by whether the sampled output's terminal numeric answer matches the ground
truth [Q3, Q29, Q46]. Additional evaluation metrics include test@N (percentage of
problems solved correctly at least once across N guesses) [Q52, Q53, Q54], majority
voting among top verifier-ranked solutions [Q85, Q87, Q88], and token-level verifier
confidence visualizations [Q147, Q148, Q149]. All metrics converge on a single scalar
signal — solution correctness as determined by final numeric answer — and no metric
captures structured output quality. For the deployment context, this output modality
is categorically misaligned: the deployment requires a structured MCQ item package
(problem stem, verified correct answer, misconception-grounded distractor choices),
and distractor quality is explicitly identified as the hardest and most critical
evaluation challenge. None of GSM8K's metrics provide any signal about whether
generated distractors reflect specific, predictable student errors or whether they
are plausible enough to function as effective assessment foils.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems." |
| Q2 | 1 | output_ontology | "To increase performance, we propose training verifiers to judge the correctness of model completions." |
| Q3 | 1 | output_form | "At test time, we generate many candidate solutions and select the one ranked highest by the verifier." |
| Q4 | 1 | output_form | "We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline." |
| Q5 | 1 | output_ontology | "One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes (Shen et al., 2021a)." |
| Q6 | 1 | output_ontology | "When generating a solution, autoregressive models have no mechanism to correct their own errors." |
| Q7 | 1 | input_content | "Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman, OpenAI" |
| Q8 | 2 | input_ontology | "We are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level." |
| Q9 | 2 | input_content | "We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts." |
| Q10 | 2 | input_ontology | "State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems." |
| Q11 | 2 | input_ontology | "At the same time, GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal." |
| Q12 | 2 | input_ontology | "We present a curated dataset of 8.5K grade school math questions and natural language solutions, useful for probing the informal reasoning ability of large language models." |
| Q13 | 2 | output_form | "We show that, compared to a finetuning baseline, the use of verifiers results in approximately the same performance boost as a 30x model size increase, and that verifiers scale significantly better with increased data." |
| Q14 | 2 | output_form | "We show that dropout acts as a strong regularizer, significantly improving performance for both finetuning and verification." |
| Q15 | 3 | input_content | "Early math word problem datasets (Kushman et al., 2014; Roy and Roth, 2015) are relatively small and are not well suited for testing the limits of modern language models." |
| Q16 | 3 | input_content | "Dolphin18K (Huang et al., 2016) is a larger dataset containing" |
| Q17 | 4 | input_content | "The recently developed ASDiv dataset (Miao et al., 2021), which contains 2.3K math word problems, addresses common flaws in prior datasets by ensuring problems have both high diversity and high quality." |
| Q18 | 4 | input_ontology | "We share those design principles in the creation of GSM8K." |
| Q19 | 4 | input_form | "However, we note that GSM8K is larger, provides natural language solutions, and consists of problems that on average require more steps to solve." |
| Q20 | 4 | input_ontology | "The MATH dataset (Hendrycks et al., 2021) is larger and significantly more complex than GSM8K, but the high difficulty makes it challenging to accurately measure progress given the current capabilities of state-of-the-art language models." |
| Q21 | 4 | input_content | "Similar to CommonsenseQA, GSM8K includes questions that require basic background knowledge, like the number of days in a week." |
| Q22 | 4 | input_ontology | "Similar to LogiQA, which requires a mix of reading comprehension and logical reasoning, GSM8K's main difficulty lies in both properly interpreting a question and reasoning through the steps to solve it." |
| Q23 | 4 | output_form | "Previous work has attempted to solve classic math word problem benchmarks with recurrent seq2seq models (Sutskever et al., 2014) and closely related variants (Wang et al., 2017; Huang et al., 2018)." |
| Q24 | 4 | output_form | "More recent work has improved performance by designing specialized encoder-decoder architectures (Amini et al., 2019; Chiang and Chen, 2018; Xie and Sun, 2019; Chen et al., 2020; Li et al., 2020), with the strongest results often relying on large pretrained encoders from the BERT family (Chen et al., 2019; Kim et al., 2020; Liang et al., 2021)." |
| Q25 | 4 | input_content | "Hendrycks et al. (2021) propose pretraining models on a new AMPS corpus, derived from Khan Academy problems and Mathematica scripts." |
| Q26 | 4 | input_content | "Similarly, Shen et al. (2021b) propose a pretrained a corpus of pre-K to college level curricula extracted from the internet, and Peng et al. (2021) propose pretraining by predicting masked subexpressions from expression trees." |
| Q27 | 5 | input_ontology | "We investigate two methods to solve problems in GSM8K: finetuning and verification." |
| Q28 | 5 | input_ontology | "Finetuning, our baseline method, uses the same language modeling objective as the generative pretraining in GPT-3 (Brown et al., 2020)." |
| Q29 | 5 | output_form | "At test time, we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct." |
| Q30 | 5 | input_ontology | "In contrast, verification consists of sampling multiple high temperature solutions, assigning each solution a score, and outputting the highest ranked solution." |
| Q31 | 5 | output_ontology | "Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer." |
| Q32 | 5 | input_form | "First, we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions." |
| Q33 | 5 | input_form | "Moreover, this choice enables our models to develop verbal analytical skills and to produce solutions that are more readily interpretable by humans." |
| Q34 | 5 | output_ontology | "Finally, we use separate generator and verifier networks, in order to prevent the generator from overfitting." |
| Q35 | 6 | input_content | "For both methods, we use models from the GPT-3 family as our initialization, primarily focusing on the 175B and 6B model sizes." |
| Q36 | 6 | input_ontology | "The 175B model is the largest and produces the most impressive results, while the 6B model is significantly more convenient for research purposes." |
| Q37 | 6 | input_form | "We discuss hyperparameter choices in Appendix B." |
| Q38 | 6 | output_ontology | "Our models frequently fail to accurately perform calculations." |
| Q39 | 6 | output_ontology | "Although larger models make fewer arithmetic mistakes than smaller models, this remains a common source of errors." |
| Q40 | 6 | input_form | "To mitigate this issue, we train all models to use a calculator by injecting calculation annotations into the training set." |
| Q41 | 6 | output_form | "At test time, a calculator will override sampling when the model chooses to use these annotations." |
| Q42 | 6 | input_form | "Details can be found in Appendix C." |
| Q43 | 6 | input_form | "We perform finetuning by updating model parameters to minimize the cross-entropy loss over all training tokens." |
| Q44 | 6 | input_ontology | "Figure 2 shows test performance after finetuning on training sets of varying sizes for 20 epochs." |
| Q45 | 6 | output_form | "We visualize the same data both as a function of training set size and as a function of model size." |
| Q46 | 6 | output_form | "Test performance is determined by a single low temperature (T = 0) sample for each test problem." |
| Q47 | 6 | input_ontology | "Unsurprisingly, we see that the 175B model significantly outperforms the smaller models." |
| Q48 | 6 | output_form | "Assuming a log-linear trend, we can naively extrapolate these results to estimate that a model with 10^16 parameters would be required to reach an 80% solve rate, when using the full GSM8K training set." |
| Q49 | 6 | output_form | "It is even harder to extrapolate along the data dimension, since performance does not appear to follow a log-linear trend." |
| Q50 | 6 | output_form | "Nevertheless, it appears likely that the 175B model would require at least two additional orders of magnitude of training data to reach an 80% solve rate." |
| Q51 | 6 | output_form | "In Figure 3, we show how 6B test performance varies over the course of 100" |
| Q52 | 7 | output_form | "We use test@N to denote the percentage of problems solved correctly at least once when allowing the model to make N separate guesses for each problem." |
| Q53 | 7 | output_form | "We use a low temperature (T = 0) to generate test@1 samples and we use a higher temperature (T = 0.7) to generate test@100 samples." |
| Q54 | 7 | output_form | "Both temperature values were chosen empirically to produce the best results." |
| Q55 | 7 | input_content | "For this reason, we use models trained for 2 epochs to generate samples for training verifiers." |
| Q56 | 7 | input_form | "We also note that it is important to allow the model to generate the full natural language solution before outputting a final answer." |
| Q57 | 7 | output_form | "If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%." |
| Q58 | 7 | input_ontology | "To improve upon the finetuning baseline, we train verifiers to judge the correctness of model-generated solutions and search against these verifiers at test time." |
| Q59 | 7 | output_ontology | "Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct." |
| Q60 | 7 | output_ontology | "Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer." |
| Q61 | 7 | output_content | "In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives." |
| Q62 | 8 | input_form | "As shown in Figure 4, we train the verifier as follows: 1. Finetune a model (the "generator") for 2 epochs on the training set. 2. Sample 100 completions from the generator for each training problem and label each solution as correct or incorrect. 3. Train a verifier for a single epoch on this dataset." |
| Q63 | 8 | input_ontology | "Training for 2 epochs is enough for the generator to learn basic skills in this domain." |
| Q64 | 8 | output_content | "We choose not to train for longer, since the diversity of generated solutions begins to collapse after this point, as shown in Figure 3." |
| Q65 | 8 | input_form | "We train separate generator and verifier models to limit the generator's training and prevent overfitting, but in principle, it should be possible to combine these models." |
| Q66 | 8 | input_form | "Unless otherwise specified, we use the same model size for the generator and the verifier." |
| Q67 | 8 | output_ontology | "In addition to predicting solution correctness, we also train the verifier with the same language modeling objective as the generator." |
| Q68 | 8 | output_form | "At test time, we sample 100 completions to each test problem, rank them with the verifier, and then return the one with the highest verifier score." |
| Q69 | 8 | output_form | "We find that it is not beneficial to use verification at low dataset sizes." |
| Q70 | 8 | output_content | "We believe this is due to the pressure to overfit to the correct answer: with small datasets, overfitting to the correct answer happens faster than learning more generalizable properties of correct reasoning." |
| Q71 | 8 | output_form | "However, once we use a sufficiently large dataset, we see a strong boost from verifiers." |
| Q72 | 9 | output_ontology | "We can either train verifiers to make a single scalar prediction conditioned on the entire generated solution, or to make a scalar prediction after each token in the solution." |
| Q73 | 9 | output_ontology | "By default, we choose the latter, training verifiers to make predictions after each token." |
| Q74 | 9 | output_ontology | "This can be viewed as a token-level value function." |
| Q75 | 9 | output_ontology | "Predicting the value function at every token is a more challenging and noisier task than judging only the full completion." |
| Q76 | 9 | output_form | "However, despite the initially slower training, the token-level verifier ultimately outperforms the solution-level verifier." |
| Q77 | 9 | output_content | "Moreover, the token-level verifier is still improving late in training, whereas the solution-level verifier quickly shows signs of overfitting." |
| Q78 | 9 | output_ontology | "We hypothesize that the full value function provides a useful auxiliary signal that encourages the model to judge the reasoning throughout solutions, rather than merely memorizing the correct final answer." |
| Q79 | 9 | output_ontology | "As discussed in Section 4.2, we can optionally include a language modeling objective alongside the verification objective." |
| Q80 | 9 | output_form | "Although both are reasonable choices, including the language modeling objective is a strict improvement." |
| Q81 | 10 | output_form | "At test time, we can choose to generate arbitrarily many solutions to be judged by the verifier before selecting the highest ranked completion." |
| Q82 | 10 | output_form | "At this scale, performance improves as we increase the number of completions up to 400." |
| Q83 | 10 | output_content | "Beyond this point, performance start to decrease. This suggests that the benefits of search are eventually outweighed by the risk of finding adversarial solutions that fool the verifier." |
| Q84 | 10 | output_form | "In general, we evaluate verifier test performance using 100 completions, since this captures most of the benefits of verification with a relatively modest compute cost." |
| Q85 | 10 | output_form | "To further increase performance, we can take a majority vote among the top verifier-ranked solutions instead of selecting only the single top solution." |
| Q86 | 10 | output_content | "This suggests that the verifier may often be relying on relatively coarse heuristics to discriminate between solutions from a given generator, rather than attempting a more thorough form of verification." |
| Q87 | 11 | output_form | "This voting process considers only the final answer reached by the individual solutions: the final answer selected is the one with the most votes." |
| Q88 | 11 | output_form | "When we have only 100 samples, it is optimal to allow only the top 3-5 samples to cast a vote. When we have 3200 samples, it is approximately optimal to allow the top 30 to cast a vote." |
| Q89 | 11 | output_form | "We find that both finetuning and verification strongly benefit from the use of dropout as a regularizer." |
| Q90 | 11 | input_form | "Specifically, we apply residual dropout (Vaswani et al., 2017) along the residual paths of each layer in the network." |
| Q91 | 11 | input_form | "We use 20% dropout for all dropout experiments, chosen based on the results of a hyperparameters sweep." |
| Q92 | 11 | input_form | "We note that GPT-3 models are not pretrained with dropout. For experiments involving dropout, we therefore perform additional pretraining with dropout before subsequently finetuning the models. This mitigates the distribution shift the model experiences during finetuning." |
| Q93 | 11 | output_form | "Figure 8a shows that dropout leads to a significant improvement over baseline." |
| Q94 | 11 | output_form | "In Figure 8b, we see that dropout significantly improves solution-level verifiers, mitigating the overfitting that occurs in the unregularized baseline." |
| Q95 | 11 | output_form | "Notably, using dropout with solution-level verifiers reaches a similar level of performance as token-level verifiers." |
| Q96 | 11 | output_form | "In Figure 8c, we apply dropout to token-level verifiers. Since token-level verifiers are already less susceptible to overfitting, it is no surprise that the impact of dropout is less significant." |
| Q97 | 11 | input_form | "Note that we increase the batch size for token-level verifiers by a factor of 4, to better handle the more difficult objective and the noise from dropout." |
| Q98 | 12 | output_form | "We have seen that verification provides a significant performance boost relative to a finetuning baseline." |
| Q99 | 12 | output_form | "On the full dataset, 6B verification slightly outperforms a finetuned 175B model, thereby offering a boost approximately equivalent to a 30x model size increase." |
| Q100 | 12 | output_form | "We have also seen that token-level verifiers are less prone to overfitting than solution-level verifiers, and that all methods benefit from regularization with residual dropout." |
| Q101 | 12 | input_ontology | "We expect verification to scale well to problem distributions that require more complex mathematical reasoning, and we hope GSM8K supports the development of new methods that scale even better." |
| Q102 | 12 | input_content | "We thank Dan Hendrycks, Leo Gao, Alec Radford, and Giambattista Parascandolo for their valuable feedback on this paper; Harri Edwards, Yura Burda, Michael Wu, and Nick Ryder for many insightful conversations; Michael Petrov, Alethea Power, and Jacob Jackson for their technical assistance; the OpenAI Supercomputing team for the infrastructure that made these experiments possible; and the team at Surge AI for performing the GSM8K data collection." |
| Q103 | 15 | input_content | "We initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork (upwork.com)." |
| Q104 | 15 | input_content | "We then worked with Surge AI (surgehq.ai), an NLP data labeling platform, to scale up our data collection." |
| Q105 | 15 | output_content | "After collecting the full dataset, we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote." |
| Q106 | 15 | output_content | "We checked whether their final answers agreed with the original solutions, and any problems that produced disagreements were either repaired or discarded." |
| Q107 | 15 | output_content | "We then performed another round of agreement checks on a smaller subset of problems, finding that 1.7% of problems still produce disagreements among contractors." |
| Q108 | 15 | output_content | "We estimate this to be the fraction of problems that contain breaking errors or ambiguities." |
| Q109 | 15 | output_content | "It is possible that a larger percentage of problems contain subtle errors." |
| Q110 | 15 | input_content | "To assist contractors with writing questions, we provided seed questions automatically generated from a few-shot prompted 175B GPT-3 model." |
| Q111 | 15 | output_content | "Contractors were allowed to use those seed questions directly, to use them as inspiration and make modifications, or to come up with their own questions entirely." |
| Q112 | 15 | input_content | "We instructed contractors to be as descriptive as possible in their solutions, and to not re-use problem settings or templates between different questions." |
| Q113 | 15 | input_content | "To ensure contractors were not re-using problem templates, we computed pairwise similarity scores between problems and used this to provide feedback to contractors." |
| Q114 | 16 | output_form | "We performed sweeps of the learning rate and batch size by an order of magnitude in both directions from the values in the table and were unable to find any significant improvements." |
| Q115 | 16 | output_form | "Other reasonable choices for both the verifier temperature (eg: 1.0 instead of 0.7) and objective (cross-entropy instead of mean squared error) also had negligible effect in our ablations." |
| Q116 | 16 | output_form | "Hyperparameters used for all experiments, unless explicitly said otherwise. Notable exceptions include Figure 8c, which uses 4x more tokens per batch and 300 completions at both training and test time. All dropout experiments in Figure 8 use 20% dropout. Figure 7a uses verifiers trained on 100 completions, but searching over more completions at test time." |
| Q117 | 17 | output_content | "The calculator annotations were not provided by human contractors: they were generated by a combination of hard-coded logic and a finetuned language model." |
| Q118 | 17 | output_content | "The logic for auto-generating calculator annotations is imperfect. It is highly unlikely to generate any incorrect annotations, but it is not uncommon for it to ignore some lines that could be annotated." |
| Q119 | 17 | input_form | "During training, there is no special distinction between the annotated tokens and the rest of the solution: they are all just tokens." |
| Q120 | 17 | output_form | "During testing, we override model sampling when a well-formatted annotation exists, specifically overwriting the token(s) directly following "=" and within <<. . . >>." |
| Q121 | 17 | output_form | "To simulate the calculator, we simply use the python eval function to evaluate the tokens in the expression (Figure 9)." |
| Q122 | 17 | output_form | "Evaluations that time out or throw an error result in the annotations being skipped and the model being sampled from as usual." |
| Q123 | 17 | output_content | "We note that the original version of our calculator, used for all results in this paper, had some minor implementation bugs." |
| Q124 | 17 | output_content | "Our reported test performance is therefore a slight underestimate, though the magnitude of this discrepancy is less than 1% in most experiments." |
| Q125 | 17 | output_content | "Fixing the calculator improves verification test performance by about 1% when using the full GSM8K training set." |
| Q126 | 18 | input_ontology | "We showcase a handful of samples comparing finetuning and verification at both 6B and 175B scale." |
| Q127 | 18 | input_content | "Samples were slightly cherry-picked for diversity." |
| Q128 | 19 | input_content | "The meat and context books weigh 2 pounds each, the French book weighs 3 pounds and the English book weighs 1 pound, and the total weight book sit in is for English task, if today is a nice day, what is the total weight of all the books?" |
| Q129 | 19 | output_content | "The meat and context books weigh 2 pounds each so they weigh 2*2 = 4=2=6=8 pounds together, the French book weighs 3 pounds and so the total weight of the English book is 6+3 = 10, so if you add up all of the books together, the total weight is 4+3+4 = 11" |
| Q130 | 19 | output_content | "Our generated responses weigh books weigh 2 pounds each to a total of 2*2 = or2=4 pounds, use French book weigh 4 pounds and the English book weighs 3 pounds, to a total of 4+3 = or4+3=7 pounds, if so if you add up all of the books, the total weight of the English book, to a total of 3+3 = or2=4=8 pounds" |
| Q131 | 19 | output_content | "The English book weight 3 pounds, So all of our books weigh 2 + 4 + 3 = 9=10 =9=10=9=10 pounds." |
| Q132 | 19 | output_content | "The total weight of books read at science books is 2*2=or2=4=6=8 pounds total weight of all the books is 4+3=or2=4+3=7 pounds." |
| Q133 | 19 | input_content | "The German Shepherd dog contains 1.5 + = or1+1=1.5=1 diggrams of dog food per day the dog also contains 2.5 +3=or2=5.5 diggrams of dog food per day, During a week, the total is 2.5 + or2+1=3=1+1.5=1 diggrams of dog food is a week." |
| Q134 | 19 | output_content | "Our data 1000=or1=1.5=1.5 diggrams per day for the German Shepherd, if the dog weighs 3.2 + or3+1.7=or3=1.9=1.5 diggrams of dog food per week." |
| Q135 | 19 | output_content | "The German Shepherd's total consumption is 1.5 + =or1=1.5=1.5 diggrams, the dog also and consumption total food per meal is 3.2 + = or3=2.5=1.5=1.5 diggrams." |
| Q136 | 19 | input_content | "The 2 German Shepherd dogs consumes 1.5 + =or1+1=1.5=1.5 diggrams of food per day, the 2 bulldogs consumes 2.3 + =or2=2.5=2.5=1.5 diggrams of food per day." |
| Q137 | 20 | output_ontology | "As noted in section 4.2, we train verifiers with a joint objective where the model learns to label a model completion as correct or incorrect, in addition to the original language modeling objective." |
| Q138 | 20 | output_form | "Architecturally, this means our verifiers are language models, with a small scalar head that outputs predictions on a per-token basis." |
| Q139 | 20 | output_form | "We implement this scalar head as a single bias parameter and single gain parameter that operate on the logits outputted by the language model's final unembedding layer." |
| Q140 | 20 | output_form | "We can choose to initialize the verifier from the same pretrained language model the generator was finetuned from, or from the generator itself." |
| Q141 | 20 | output_form | "In our ablations the latter performed slightly better; we suspect this is because better understanding the language distribution that the generator learned should only aid the verifier in scoring samples from that distribution." |
| Q142 | 20 | output_form | "Unless otherwise explicitly stated, we initialize our verifiers from their corresponding generators in all experiments." |
| Q143 | 20 | input_content | "When training verifiers with the joint objective, we use an equal mix of language data and verifier data." |
| Q144 | 20 | input_content | "Because we sample 100 completions for each original training example to generate the verifier data, using an equal mix means we effectively upsample the original language data by a factor of 100." |
| Q145 | 20 | output_form | "To form the joint objective, we simply add the verifier loss and language modeling loss unweighted, and define an epoch of this joint objective as having seen each verifier example once." |
| Q146 | 20 | input_form | "With both objectives, we mask out tokens in the question and only train on tokens in the solutions, as visualized in Figure 12." |
| Q147 | 21 | output_form | "One benefit of the token-level verifiers is that these models become immediately interpretable: we can visualize the predicted value for each token and better understand how the verifier makes decisions on judging samples." |
| Q148 | 21 | output_form | "Above we present a visualization of the predicted values for five different cherry-picked questions and model completions, verified by a 175B token-level verifier that was trained on the full training set." |
| Q149 | 21 | output_form | "In the visualization, the background color of the text corresponds to the verifier score for that token, where red is low value (predicted incorrect) and green" |
| Q150 | 22 | output_form | "The second column of the table summarizes the verifier's prediction, and the third column indicates whether the generated model completion was actually correct or incorrect." |
| Q151 | 22 | output_form | "Any disagreement between the second and third columns indicates that the verifier made an error." |
| Q152 | 22 | output_content | "Note that the model is initially unsure about whether the solution is correct and gradually gains certainty as the solution progresses: this is likely a property of the verifier training procedure, where it trains on a large fraction of incorrect model-generated samples." |
| Q153 | 22 | output_content | "The second row contains a problem where the solution is correct, but the verifier has rated it as incorrect. This is potentially due to the ambiguity between the "4 times" and the "4 potatoes" in the problem description." |
| Q154 | 22 | output_content | "The third row consists of another false negative example. However, unlike the previous example, here the model completion contains some faulty reasoning. As such, even though the final answer in the model completion was correct, the natural language explanation was incorrect, and so the verifier correctly assigned a low score." |
| Q155 | 22 | output_content | "The final row contains a false positive, where the model makes a mistake on the second step, where it subtracts 400 from the price of a diamond jewel instead of a gold one. Verifiers occasionally make mistakes with performing this variable binding of quantities to their relationships." |

---

## Regional Context

```yaml
name: 'US K–8 Edtech: CCSS-Aligned Math Assessment Item Generation'
abbreviation: US_K8_CCSS_MCQ
deployment_context:
  country: United States
  sector: K–12 education technology
  deployment_type: LLM-powered math assessment item generation tool
  primary_users: K–8 classroom teachers in US public and private schools, spanning
    urban, suburban, and rural settings
  secondary_users: K–8 students (grades K–8) whose formative assessments are built
    from generated content
  geographic_scope: National (no sub-national restriction); content must be inclusive
    across all US regional and demographic contexts
  use_case_summary: Teachers specify a CCSS standard (e.g., 4.NF.A.2), grade level,
    and difficulty; the system generates a complete multiple-choice assessment item
    with a verified correct answer and misconception-grounded distractor choices for
    use in targeted formative assessment.
target_population_profile:
  teacher_characteristics:
    grade_bands_served:
    - K–2
    - 3–5
    - 6–8
    settings:
    - urban
    - suburban
    - rural
    student_populations_served:
    - General education students
    - English Language Learners (ELL/multilingual learners)
    - Students from lower-income households
    - Students from diverse racial and ethnic backgrounds
    pedagogical_role: Formative assessment design; teachers use generated items for
      targeted skill diagnosis, not summative grading
    assumed_content_knowledge: Grade-level math content familiarity; not assumed to
      have psychometric or item-writing expertise
  student_characteristics:
    age_range_approx: 5–14 years
    grade_range: K–8
    linguistic_diversity: Significant ELL population; low-idiom, plain-language problem
      stems required
    socioeconomic_diversity: Includes students from lower-income households; money-related
      problem contexts require sensitivity
    cultural_diversity: Broad US demographic diversity; regionally neutral, culturally
      inclusive contexts required
curriculum_framework:
  primary_standard: Common Core State Standards for Mathematics (CCSS-M)
  standard_adoption_status: '41 states, DC, four territories, and the Department of
    Defense Education Activity (DoDEA) have adopted CCSS as of 2025. Four states never
    adopted CCSS at all: Alaska, Nebraska, Texas, and Virginia. States that formally
    repealed and replaced CCSS include Florida (adopted Florida''s B.E.S.T. Standards),
    Indiana (Indiana Academic Standards), Oklahoma, South Carolina, and Tennessee
    (Tennessee Academic Standards). Many other states adopted CCSS but subsequently
    renamed or modestly revised their standards while retaining the core framework.
    Source: Common Core State Standards Initiative — [WEB-1];
    LegalClarity state-by-state analysis (Dec 2025) — [WEB-2].

    CAVEAT: For a national deployment, this means CCSS-tagged items will not directly
    align to the official standards documents in Texas, Virginia, Alaska, Nebraska,
    Florida, Indiana, Oklahoma, South Carolina, and Tennessee. Parallel coverage or
    explicit mapping to Texas TEKS and Virginia SOL is required for full national
    reach (see alternative_frameworks_in_scope).'
  relevant_domains_by_grade_band:
    K–2:
    - Counting & Cardinality (CC)
    - Operations & Algebraic Thinking (OA)
    - Number & Operations in Base Ten (NBT)
    - Measurement & Data (MD)
    - Geometry (G)
    3–5:
    - Operations & Algebraic Thinking (OA)
    - Number & Operations in Base Ten (NBT)
    - Number & Operations—Fractions (NF)
    - Measurement & Data (MD)
    - Geometry (G)
    6–8:
    - Ratios & Proportional Relationships (RP)
    - The Number System (NS)
    - Expressions & Equations (EE)
    - Functions (F)
    - Statistics & Probability (SP)
    - Geometry (G)
  example_target_standards:
  - 4.NF.A.2
  - 6.RP.A.3
  - 3.OA.A.1
  - 5.NF.B.4
  standard_granularity_required: Standard-cluster level (e.g., 4.NF.A.2), not domain-level
  ccss_alignment_in_gsm8k: NOT PRESENT — GSM8K contains no CCSS tagging at domain,
    cluster, or standard level; this is a fundamental ontological gap
  alternative_frameworks_in_scope: 'Texas uses the Texas Essential Knowledge and Skills
    (TEKS) for mathematics, and Virginia uses the Virginia Standards of Learning (SOL)
    — both of which are entirely distinct frameworks from CCSS-M and were never aligned
    to it. Alaska, Nebraska, Oklahoma, South Carolina, Indiana, Florida, and Tennessee
    also use state-specific frameworks that, while sometimes CCSS-derived, are officially
    separate documents. For a national K–8 deployment, the tool should either (a)
    restrict its marketing scope to CCSS-adopting states or (b) implement parallel
    standard-tagging pipelines for TEKS and Virginia SOL at minimum, as Texas and
    Virginia together represent a large share of total US K–8 enrollment. Source:
    LegalClarity state standards map (Dec 2025) — [WEB-2].'
languages:
  primary: English (American English)
  register_requirements: Low-idiom, plain-language register for ELL accessibility;
    lexical complexity norms for math word problems targeting multilingual learners
  ell_frameworks_relevant:
  - 'WIDA English Language Development Standards Framework, 2020 Edition (current
    version — released December 2020 by the WIDA Consortium; being implemented across
    36 states, DC, and four territories as of 2024; supersedes 2012 Edition). Source:
    WIDA official release — [WEB-3];
    WIDA implementation study May 2024 — [WEB-4]'
  - CCSS-ELL language standards
  - 'WIDA 2020 Edition organizes ELD standards around six grade bands (K–1, 2–3, 4–5,
    6–8, 9–10, 11–12) with grade-band-specific Language Expectations and Proficiency
    Level Descriptors — directly relevant to K–8 grade-band differentiation requirements
    of this deployment. Source: WIDA ELD Standards Framework 2020 — [WEB-3]'
  script: Latin alphabet
  modality: Text-only; no audio, image, or symbol-only modality required
  gsm8k_language_match: Full match on language and modality — lowest-risk validity
    dimension
output_format_requirements:
  item_package_components:
  - Problem stem (grade-appropriate language, culturally inclusive context)
  - Verified correct answer (mathematically accurate, clearly labeled)
  - Distractor choices (typically 3, grounded in specific documented student misconceptions)
  - 'Optional: worked solution explanation (step-level, grade-appropriate reasoning
    chain)'
  distractor_design_standard: Distractors must reflect specific, predictable student
    errors (e.g., adding numerators and denominators independently when adding fractions
    for 4.NF.A.2); arbitrary wrong numbers are not acceptable
  item_format: Multiple-choice (MCQ)
  gsm8k_output_format_match: CATEGORICAL MISMATCH — GSM8K evaluates free-form natural
    language solution generation scored by final numeric answer only; structured MCQ
    output (stem + answer + misconception-grounded distractors) is entirely outside
    GSM8K's evaluation scope
  misconception_research_sources: 'Multiple active NLP research efforts address automated
    math MCQ distractor generation grounded in student misconceptions, but no single
    authoritative database covers all CCSS standards.

    - DiVERT (arXiv 2406.19356, 2024): distractor generation using variational error
    representations for math MCQs — [WEB-5]

    - Overgenerate-and-rank (arXiv 2405.05144, 2024): ranks generated distractors
    by predicted student selection likelihood; human-authored distractors still outperform
    generated ones — [WEB-6]

    - ACL 2025 paper on plausible distractor generation via student-choice prediction
    — [WEB-7]

    - ASSISTments platform contains grade-level math MCQ items with student response
    data usable for misconception modeling but is not a public benchmark with CCSS-level
    distractor annotations.

    The research consensus is that crafting misconception-grounded distractors remains
    a labor-intensive, hard-to-automate task; LLM-generated distractors are systematically
    rated lower than human-authored ones by teachers. Source: Overgenerate-and-rank
    study — [WEB-6]'
evaluation_rubric:
  dimension_hierarchy:
  - rank: 1
    dimension: Mathematical solution accuracy
    description: Hard prerequisite; items with incorrect solutions are discarded
    gsm8k_coverage: Direct — GSM8K measures this dimension via final numeric answer
      correctness
    priority: HARD GATE
  - rank: 2
    dimension: Distractor plausibility and misconception grounding
    description: Each distractor must reflect a specific, documented student error;
      implausible or accidentally correct distractors fail the item
    gsm8k_coverage: NOT COVERED — no metric or label in GSM8K addresses MCQ distractor
      quality
    priority: HIGH
  - rank: 3
    dimension: CCSS standard alignment
    description: Generated item must genuinely target the specified standard's specific
      skill, not merely grade-level math broadly
    gsm8k_coverage: NOT COVERED — GSM8K has no CCSS taxonomy
    priority: HIGH
  - rank: 4
    dimension: Grade-level language appropriateness
    description: Problem stem vocabulary, sentence complexity, and context must be
      appropriate for the specified grade band
    gsm8k_coverage: NOT COVERED — GSM8K provides no grade-level tagging or age-appropriate
      language validation
    priority: HIGH
  - rank: 5
    dimension: Cultural inclusivity
    description: Contexts must be accessible across urban/suburban/rural settings,
      low-idiom for ELL students, diverse names, no income-stigmatizing money contexts
    gsm8k_coverage: NOT COVERED — GSM8K has no documented inclusivity guidelines or
      cultural audit
    priority: HIGH
  classroom_readiness_definition: 'An item is ''correct'' only if the entire MCQ package
    is classroom-ready: mathematically accurate, CCSS-aligned, grade-appropriate language,
    plausible misconception-grounded distractors, and culturally inclusive context'
  gsm8k_construct_coverage: GSM8K captures only the hard-gate prerequisite dimension
    (mathematical accuracy); the large majority of the deployment's evaluation construct
    is entirely unmeasured by the benchmark
cultural_inclusivity_requirements:
  required: true
  guidelines:
  - Contexts must be accessible across urban, suburban, and rural US settings
  - 'Avoid culturally narrow references: assumed family structures, regionally specific
    foods, particular sports with uneven US cultural distribution'
  - Use low-idiom language to support multilingual learners
  - Include diverse names in problem scenarios
  - Handle money contexts sensitively to avoid stigmatizing students from lower-income
    households
  - Avoid references that presuppose particular household income levels or material
    circumstances
  relevant_equity_frameworks:
  - NCTM Principles to Actions equity framework (2014)
  - 'NCTM Catalyzing Change series: Catalyzing Change in High School Mathematics (2018);
    Catalyzing Change in Middle School Mathematics (2020); Catalyzing Change in Early
    Childhood and Elementary Mathematics (2020). The series provides equity-centered
    guidance on instructional practices, equitable structures, and positive mathematical
    identity development. Source: NCTM official series page — [WEB-8];
    NCTM Early Childhood volume — [WEB-9]'
  - 'NEEDS VERIFICATION — deferred: below search budget — confirm whether any NCTM
    publication specifically addresses word problem design guidelines for cultural
    inclusivity (vs. broader equity in instruction); likely requires direct examination
    of NCTM publications or expert elicitation'
  - WIDA English Language Development Standards, 2020 Edition (for ELL accessibility)
    — [WEB-3]
  - 'No published cultural audit of K–8 math word problem datasets was found in searches.
    The EDUMATH project (arXiv 2510.06965) includes an ''Educational Appropriateness''
    criterion evaluated by teachers, which is the closest analogue identified, but
    does not constitute a systematic cultural bias audit. Source: EDUMATH paper —
    [WEB-10]'
  gsm8k_inclusivity_coverage: NOT DOCUMENTED — GSM8K contractor guidelines addressed
    template reuse and solution descriptiveness but contain no documented inclusivity
    constraints; GPT-3-seeded problem generation introduces uncharacterized cultural
    influence
grade_band_infrastructure:
  grade_bands:
  - K–2
  - 3–5
  - 6–8
  grade_level_tagging_in_gsm8k: NOT PRESENT — GSM8K treats all problems as undifferentiated
    'grade school math' with no grade-level or grade-band annotation
  readability_standards_relevant:
  - 'NEEDS VERIFICATION — deferred: below search budget — Flesch-Kincaid or Lexile
    grade-band targets for K–2, 3–5, 6–8 math word problems; these targets exist in
    readability literature but no single authoritative source specifically for math
    word problem stems was identified in searches'
  - 'WIDA 2020 Edition provides grade-band-specific Proficiency Level Descriptors
    organized around six grade bands (K–1, 2–3, 4–5, 6–8, 9–10, 11–12) for mathematics
    contexts, directly applicable to lexical complexity calibration by grade band
    for multilingual learners. Source: WIDA ELD Standards 2020 — [WEB-3]'
  difficulty_calibration: Teachers specify difficulty at item-generation time; system
    must honor grade-band-appropriate difficulty, not just broad 'grade school' difficulty
    range
  existing_grade_tagged_item_banks: 'Multiple CCSS-aligned, grade-tagged item banks
    exist and are usable as evaluation references:

    - Smarter Balanced Assessment Consortium: maintains an open interim item bank
    (grade 3–8 and high school) aligned to CCSS, publicly accessible; items are grade-tagged
    and CCSS-standard-tagged. Source: Smarter Balanced resources — [WEB-11];
    California Dept of Education Smarter Balanced resources — [WEB-12]

    - PARCC/New Meridian item bank: 10,000+ grade-level, CCSS-tagged items (grades
    3–11); managed by New Meridian since 2017; states may license items. Released
    PARCC items include scoring rubrics, answer keys, and standards alignment metadata.
    Source: EdWeek PARCC/Smarter Balanced explainer — [WEB-13];
    released items archive — [WEB-14]

    - EDUMATH dataset (arXiv 2510.06965, Oct 2024): first teacher-annotated dataset
    specifically for standards-aligned educational MWP generation, including a Standards
    Alignment annotation criterion; directly relevant as an evaluation reference for
    this deployment. Source — [WEB-10]

    CAVEAT: Smarter Balanced and PARCC banks are designed for summative assessment
    and may not include the misconception-grounded distractor documentation required
    for formative assessment use in this deployment.'
benchmark_validity_summary:
  benchmark: GSM8K
  overall_validity_assessment: LOW — GSM8K measures only the hard-gate prerequisite
    (multi-step arithmetic accuracy) of a five-dimension evaluation construct; four
    of five dimensions (CCSS alignment, distractor quality, grade-level language,
    cultural inclusivity) are entirely outside the benchmark's scope
  dimensions_covered:
  - Mathematical solution accuracy (partial — numeric answer only, no step-level quality)
  dimensions_not_covered:
  - CCSS standard-level alignment
  - Distractor plausibility and misconception grounding
  - Grade-level language appropriateness (K–2 vs. 3–5 vs. 6–8)
  - Cultural inclusivity and ELL accessibility
  - Structured MCQ output format quality
  priority_gaps:
  - gap: CCSS standard-level coverage mapping
    priority: HIGH
    web_search_target: CCSS-aligned math word problem benchmark standard-level tagging
      4.NF.A.2 6.RP.A.3 evaluation MATH MathBench state item banks
    search_finding: 'No existing LLM benchmark provides CCSS standard-cluster-level
      tagging. The closest identified resource is EDUMATH (arXiv 2510.06965, Oct 2024),
      which is the first teacher-annotated dataset for standards-aligned educational
      MWP generation and introduces a Standards Alignment evaluation criterion assessed
      by real teachers. Smarter Balanced and PARCC released item banks provide CCSS-tagged
      items at the standard level and can serve as evaluation reference corpora, though
      they were not designed as LLM benchmarks. Source: EDUMATH — [WEB-10]'
  - gap: Distractor-quality evaluation criteria grounded in student misconceptions
    priority: HIGH
    web_search_target: MCQ distractor quality evaluation rubric student misconceptions
      math formative assessment benchmark ASSISTments Khan Academy item banks
    search_finding: 'Active NLP research area as of 2024–2025 but no standardized
      benchmark or rubric is established. Key papers: DiVERT (arXiv 2406.19356) models
      distractor generation via variational error representations; overgenerate-and-rank
      (arXiv 2405.05144) trains a ranking model on student response data and confirms
      human-authored distractors still outperform LLM-generated ones; ACL 2025 (aclanthology.org/2025.acl-long.1154)
      proposes a pairwise rubric assessing conceptual misunderstanding targeting,
      similarity to correct answer, and intuitive appeal. None of these constitute
      a deployed benchmark. Sources: [WEB-6]; [WEB-5];
      [WEB-7]'
  - gap: Multilingual learner (ELL) linguistic accessibility standards for math word
      problems
    priority: HIGH
    web_search_target: readability lexical complexity math word problems ELL multilingual
      learners WIDA CCSS-ELL grade band benchmark
    search_finding: 'WIDA 2020 Edition (current framework) provides grade-band-specific
      Proficiency Level Descriptors and Language Expectations for mathematics contexts
      across six grade bands including the K–8 bands relevant to this deployment.
      These constitute the authoritative US standard for ELL language calibration.
      However, no published benchmark or dataset for math word problems specifically
      validated against WIDA Proficiency Level Descriptors was identified. Source:
      WIDA ELD Standards 2020 — [WEB-3]'
  - gap: Culturally inclusive math context audit and design guidelines
    priority: HIGH
    web_search_target: culturally inclusive math word problems cultural audit bias
      review NCTM equity guidelines grade school benchmark design
    search_finding: 'No published cultural audit of K–8 math word problem datasets
      was found. EDUMATH (arXiv 2510.06965) evaluates ''Educational Appropriateness''
      via teacher annotation, which partially addresses this gap, but is not a systematic
      cultural inclusivity audit. NCTM Catalyzing Change series (2018–2020) provides
      equity-centered instructional guidance but does not publish a word-problem-specific
      design checklist. This gap appears to require stakeholder/expert elicitation
      rather than a searchable resource. Source: EDUMATH — [WEB-10];
      NCTM Catalyzing Change — [WEB-8]'
  - gap: Grade-band granularity tagging for grade-level-appropriate item generation
    priority: HIGH
    web_search_target: math word problem dataset grade-level tagging K-8 grade band
      Smarter Balanced PARCC item bank difficulty annotation
    search_finding: 'Smarter Balanced and PARCC item banks provide grade-level-tagged,
      CCSS-aligned items (grades 3–8) and are publicly accessible or licensable. Smarter
      Balanced''s open interim item bank is built to the same specifications as the
      summative assessment and is explicitly grade-tagged. These are the highest-quality
      available reference corpora for grade-band validation. EDUMATH (2024) also annotates
      MWPs by grade level. No purpose-built LLM benchmark with K–8 grade-band tagging
      exists. Sources: Smarter Balanced — [WEB-11]; PARCC/New
      Meridian released items — [WEB-14];
      EDUMATH — [WEB-10]'
  - gap: Pedagogical accuracy of solution explanations (step-level quality beyond
      final answer)
    priority: MEDIUM
    web_search_target: math solution explanation quality evaluation step-level correctness
      benchmark pedagogical reasoning chain scoring grade school
    search_finding: 'NEEDS VERIFICATION — deferred: below search budget. The EDUMATH
      paper evaluates ''Solvability'' and ''Accuracy'' as separate criteria (adapted
      from Christ et al. 2024), which partially addresses step-level quality, but
      full pedagogical quality of solution explanations (grade-appropriate reasoning
      chains) was not the focus of any identified benchmark.'
regulatory_and_policy_context:
  data_privacy: 'FERPA, COPPA (Children''s Online Privacy Protection Act, applicable
    given K–8 student ages), and state Student Online Personal Information Protection
    Act (SOPIPA)-type statutes are all potentially applicable. A 2025 Oregon Department
    of Education guidance document explicitly identifies FERPA, COPPA, and state-equivalent
    statutes as governing AI tools processing student data, noting that AI systems
    trained on student data containing PII may have difficulty complying with FERPA''s
    de-identification standard. Deployments generating assessment content involving
    student interaction data should conduct a privacy impact assessment under FERPA/COPPA
    before launch. Source: Oregon DOE AI Guidance (March 2025) — [WEB-15]

    CAVEAT: Whether the item-generation tool itself (as distinct from student response
    collection) triggers FERPA/COPPA depends on whether personally identifiable student
    information is processed; this requires legal review specific to the deployment
    architecture.'
  accessibility_requirements: 'NEEDS VERIFICATION — deferred: below search budget
    — confirm whether WCAG 2.1 AA or Section 508 applies to the edtech platform deploying
    this tool in school contexts. Section 508 applies to federal agencies and federally
    funded programs; whether it directly binds a private edtech vendor in school contexts
    depends on the funding structure of the school district. This requires legal review.'
  ccss_adoption_map: '41 states, DC, four territories, and DoDEA have adopted CCSS-M.
    Four states (Alaska, Nebraska, Texas, Virginia) never adopted CCSS. States that
    formally repealed and replaced CCSS include Florida (B.E.S.T. Standards), Indiana
    (Indiana Academic Standards), Oklahoma, South Carolina, and Tennessee (Tennessee
    Academic Standards). Many additional states renamed or revised their standards
    while retaining the CCSS core framework. For national deployment, the tool''s
    CCSS branding will not match official state framework names in approximately 9
    states, representing a meaningful share of national K–8 enrollment. Sources: CCSS
    Initiative state map — [WEB-1];
    Wikipedia CCSS by state (Jan 2026) — [WEB-16];
    LegalClarity (Dec 2025) — [WEB-2]'
  ai_in_education_policy: 'The US Department of Education issued a Dear Colleague
    Letter (DCL) on July 22, 2025 providing guidance on responsible AI integration
    in education and confirming that existing formula and discretionary federal education
    grant funds may be used to support AI initiatives complying with applicable statutory
    frameworks. This follows the March 2025 Executive Order on ''Advancing Artificial
    Intelligence Education for American Youth.'' The guidance permits AI tutoring
    systems and AI-generated instructional materials but does not establish specific
    disclosure requirements or validity standards for AI-generated formative assessment
    items. No federal standard specifically governing AI-generated assessment content
    validity was identified. State-level AI guidance is proliferating rapidly (e.g.,
    Alabama June 2024, New Mexico May 2025, Missouri 2025–26) but focuses on responsible
    use principles rather than psychometric validity standards for AI-generated items.
    Source: US DOE Dear Colleague Letter July 2025 — [WEB-17];
    state AI guidance inventory — [WEB-18]'
infrastructure_notes: Deployment is a web-based or integrated edtech platform accessed
  by classroom teachers on school-issued or personal devices. No modality mismatch
  with GSM8K (both text-only English). Infrastructure risk is low for the benchmark
  validity assessment; primary validity concerns are pedagogical and curricular, not
  infrastructural.
domain_specific_notes: '- CCSS-M is the authoritative curriculum framework; standard-level
  alignment (not domain-level) is non-negotiable for the deployment use case.

  - Formative assessment item design is a specialized psychometric sub-domain; distractor
  construction grounded in misconception research (e.g., fraction arithmetic errors,
  place-value confusion) is distinct from general math problem generation.

  - ELL accessibility is a legal and ethical requirement in US public schools under
  Title III of ESEA/ESSA; low-idiom language is not merely a preference.

  - Cultural responsiveness in math contexts is supported by NCTM equity frameworks
  and is increasingly a district-level procurement requirement.

  - Grade-band differentiation (K–2, 3–5, 6–8) reflects real developmental differences
  in reading level, abstract reasoning, and CCSS domain progression that a single
  ''grade school math'' benchmark cannot capture.

  - Money-related problem contexts are pervasive in grade school math word problems;
  sensitivity guidelines are needed to avoid reinforcing income-related stigma for
  students from lower-income households.

  '
net_new_fields:
  closest_analogous_benchmark_identified:
    name: 'EDUMATH: Generating Standards-aligned Educational Math Word Problems'
    arxiv_id: '2410.06965'
    url: '[WEB-10]'
    year: 2024
    relevance: 'EDUMATH is the closest identified benchmark/dataset to this deployment''s
      evaluation construct. It is the first teacher-annotated dataset for standards-aligned
      K–12 educational MWP generation, evaluating LLMs on four criteria: Solvability,
      Accuracy, Educational Appropriateness, and Standards Alignment (a new criterion
      introduced by this work). It uses a joint human expert-LLM judge approach to
      evaluate over 11,000 generated MWPs and includes an in-classroom student study.
      Critically, EDUMATH explicitly finds a performance gap between open and closed
      LLMs on the standards-alignment criterion, directly informing the ontological
      gap identified in this assessment.'
    key_limitation: EDUMATH does not evaluate MCQ distractor quality or misconception
      grounding — it targets MWP generation, not full MCQ item package generation.
      It also does not specifically target K–2 grade-band language calibration.
  automated_distractor_generation_research_landscape:
    summary: 'As of 2024–2025, automated math MCQ distractor generation is an active
      NLP research area but has no established benchmark. Three key 2024 papers (DiVERT
      arXiv 2406.19356, overgenerate-and-rank arXiv 2405.05144, and a concept-map
      approach arXiv 2505.02850) collectively establish that: (1) human-authored distractors
      consistently outperform LLM-generated ones in teacher evaluations; (2) effective
      distractors require deep knowledge of common student errors that LLMs do not
      reliably encode; and (3) the most promising approaches use student response
      data to rank generated distractors by predicted selection likelihood.'
    implication_for_assessment: 'The absence of a benchmark and the consistent finding
      that LLM-generated distractors lag behind human-authored ones is itself a high-impact
      finding for this deployment''s validity assessment. It implies that the distractor-quality
      dimension (ranked #2 in the deployment''s evaluation hierarchy) cannot be reliably
      measured by any existing automated benchmark and will require human teacher
      evaluation as the gold standard. Sources: [WEB-6];
      [WEB-5]; [WEB-19]'
  wida_2020_grade_band_relevance:
    summary: The current WIDA ELD Standards Framework (2020 Edition, released December
      2020, in implementation across 36 states and DC as of 2024) organizes language
      development expectations around six grade bands including K–1, 2–3, 4–5, and
      6–8 — directly corresponding to the K–2, 3–5, and 6–8 bands used in this deployment.
      The framework provides Language Expectations specific to mathematics content
      areas at each grade band, making it the most directly applicable US standard
      for calibrating ELL-accessible language in generated math word problems by grade
      band.
    source: WIDA ELD Standards Framework 2020 — [WEB-3];
      WIDA implementation study (May 2024) — [WEB-4]
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.thecorestandards.org/standards-in-your-state/ |
| WEB-2 | https://legalclarity.org/what-states-use-common-core-state-standards/ |
| WEB-3 | https://wida.wisc.edu/resources/wida-english-language-development-standards-framework-2020-edition |
| WEB-4 | https://wida.wisc.edu/resources/examination-current-implementation-status-wida-english-language-development-standards |
| WEB-5 | https://arxiv.org/abs/2406.19356 |
| WEB-6 | https://arxiv.org/abs/2405.05144 |
| WEB-7 | https://aclanthology.org/2025.acl-long.1154.pdf |
| WEB-8 | https://www.nctm.org/change/ |
| WEB-9 | https://www.amazon.com/Catalyzing-Change-Childhood-Elementary-Mathematics/dp/1680540424 |
| WEB-10 | https://arxiv.org/abs/2510.06965 |
| WEB-11 | https://smarterbalanced.org/ |
| WEB-12 | https://www.cde.ca.gov/ta/tg/sa/smarterbalresources.asp |
| WEB-13 | https://www.edweek.org/teaching-learning/big-things-you-need-to-know-now-about-the-parcc-and-smarter-balanced-tests/2019/01 |
| WEB-14 | https://gotestprep.com/parcc-released-items/ |
| WEB-15 | https://www.oregon.gov/ode/educator-resources/teachingcontent/Documents/Developing%20Policy%20and%20Protocols%20for%20the%20use%20of%20Generative%20AI%20in%20K-12%20Classrooms_March%202025.pdf |
| WEB-16 | https://en.wikipedia.org/wiki/Common_Core_implementation_by_state |
| WEB-17 | https://www.ed.gov/about/news/press-release/us-department-of-education-issues-guidance-artificial-intelligence-use-schools-proposes-additional-supplemental-priority |
| WEB-18 | https://www.aiforeducation.io/ai-resources/state-ai-guidance |
| WEB-19 | https://arxiv.org/abs/2505.02850 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: GSM8K covers grade school math word problems broadly, but your teachers need to generate items aligned to specific Common Core domains (e.g., Operations & Algebraic Thinking, Number & Operations—Fractions, Ratios & Proportional Relationships). Does your system need to be evaluated on its ability to generate problems that map to specific Common Core standards or clusters, or is general grade-level math accuracy sufficient?
A1: Common Core alignment is essential and non-negotiable. Teachers select specific standards at the standard-cluster level (e.g., 4.NF.A.2, 6.RP.A.3), and generated items must genuinely target that standard's specific skill. General grade-level accuracy is insufficient; the system must be evaluated on whether outputs correctly operationalize the requested CCSS standard, since teachers use these items for targeted formative assessment.

Q2 [OO]: GSM8K scores answers as correct or incorrect based on a single numeric answer. Your deployment requires evaluating generated problems on multiple pedagogical dimensions — mathematical accuracy of the solution, appropriateness of distractors, alignment to a specified grade level, and Common Core standard coverage. Which of these dimensions matter most for your evaluation, and does 'correct' mean something beyond arithmetic accuracy in your context?
A2: All four dimensions matter, with a clear hierarchy. Mathematical solution accuracy is a hard prerequisite — a failing item is simply discarded. Distractor plausibility (grounded in specific, predictable student misconceptions) and CCSS standard alignment are the primary differentiators of pedagogical value. Grade-level appropriateness of language and context is also critical. "Correct" means the entire item package is classroom-ready, not merely that the arithmetic answer is accurate.

Q3 [IC]: GSM8K word problems use real-world contexts drawn from US everyday life, but your teachers may serve students from diverse communities across the US — urban, rural, multilingual learners, or specific demographic groups. Are there contexts or cultural references that would be inappropriate or inaccessible for your target student populations, or requirements that problems reflect inclusive, culturally responsive scenarios?
A3: Cultural inclusivity is a real requirement. Problems must use contexts accessible across urban, rural, and suburban settings, avoid culturally narrow references (assumed family structures, regionally specific foods, particular sports), use low-idiom language to support multilingual learners, and include diverse names in scenarios. Content involving money must be handled sensitively to avoid stigmatizing students from lower-income households.

Q4 [OF]: GSM8K benchmarks free-form solution generation, but your deployment requires a structured output package: a problem stem, a verified correct answer, and plausible distractor choices. Does your evaluation need to assess the quality of the full multiple-choice item (including distractor design and plausibility), or only whether the underlying math is solved correctly?
A4: Evaluation must cover the full multiple-choice item package. Distractor quality is identified as the hardest and most critical component — valid distractors must reflect specific, predictable student errors (e.g., adding numerators and denominators independently when adding fractions) rather than arbitrary wrong numbers. An item with implausible distractors or accidentally correct distractors fails regardless of the accuracy of the solution. GSM8K's free-form, numeric-answer scoring does not capture this dimension at all.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | GSM8K's problem categories are not organized by CCSS standards or clusters, and the deployment requires evaluating coverage of specific, named standards (e.g., 4.NF.A.2); the ontological mismatch is direct and consequential. |
| IC | HIGH | Teachers require culturally inclusive, low-idiom, regionally neutral problem contexts accessible to multilingual learners and students from diverse socioeconomic backgrounds — dimensions GSM8K was not designed to ensure. |
| IF | LOWER | Both benchmark and deployment are text-only in English, with no modality mismatch. |
| OO | HIGH | GSM8K's single binary correct/incorrect scoring against a numeric answer is categorically misaligned with the deployment's multi-dimensional output rubric (solution accuracy, distractor plausibility, standard alignment, grade-level language appropriateness). |
| OC | HIGH | GSM8K ground-truth labels cover only final numeric answers; there are no labels for distractor quality, misconception grounding, or CCSS standard fidelity — meaning large portions of the deployment's "correct" construct are entirely unlabeled. |
| OF | HIGH | GSM8K evaluates free-form solution generation; the deployment requires structured MCQ output (stem + verified answer + misconception-grounded distractors), and distractor quality is explicitly identified as the hardest unsolved evaluation challenge. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** openai/gsm8k (configs: `main`, `socratic`)
**Analysis date:** 2025-01-27
**Examples reviewed:** 47 from `main` train split; 33 from `socratic` train split (80 total)
**Columns shown:** question, answer
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | main | Ex. 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | Multi-step arithmetic across sequential days — illustrates benchmark's multi-step reasoning requirement | IO |
| D2 | main | Ex. 6 | 54 | "Nancy is filling an aquarium for her fish. She fills it halfway and goes to answer the door. While she's gone, her cat knocks the aquarium over and spills half the water in it. Then Nancy comes back and triples the amount of water in the aquarium." | Proportional reasoning (fractions of volume), multi-step — relevant to grade 3–5 CCSS domains, but not tagged | IO |
| D3 | main | Ex. 7 | 90 | "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle. How many more days are left until all the food runs out?" | Rate/proportion inverse problem — not labeled by CCSS standard or grade band | IO |
| D4 | main | Ex. 23 | 220 | "Jim collects model cars, and he has 301 models total. Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys." | Algebraic system of equations — more consistent with 6–8 CCSS (6.EE, 7.EE) but not tagged | IO |
| D5 | main | Ex. 43 | 720 | "Ariella has $200 more in her son's saving account than Daniella has in her son's savings account. Ariella's account earns her simple interest at the rate of 10% per annum." | Simple interest calculation — consistent with 7th grade CCSS (7.RP) but no tagging | IO |
| D6 | main | Ex. 38 | 90 | "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys, how many will she remain with?" | Ratio and fractions — consistent with 6.RP CCSS domain, but untagged | IO |
| D7 | main | Ex. 2 | 9 | "Anna baked 60 cupcakes. She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes." | Fraction of a whole — resembles 4.NF or 5.NF CCSS, but no standard tag exists | IO |
| D8 | main | Ex. 3 | 99 | "It's Ava's birthday party. Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats. They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." | Party/consumer context with brand-name US candy; culturally narrow | IC |
| D9 | main | Ex. 18 | 72 | "James joins a football team and becomes the star. He scores 4 touchdowns per game and each touchdown is worth 6 points. There are 15 games in the season." | American football context — sport with uneven US cultural distribution; not globally universal | IC |
| D10 | main | Ex. 34 | 500 | "Rachel and Sara want to attend a beauty and modeling contest. They both want to buy new pairs of shoes and dresses. Sara buys a pair of shoes which costs $50 and a dress which costs $200." | Beauty/modeling contest context; gender-stereotyped; culturally specific | IC |
| D11 | main | Ex. 30 | 7200 | "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples because she was at fault in an accident." | Adult household finance context with rent, car insurance — age-inappropriate for K–8; presupposes middle-class expenses | IC |
| D12 | main | Ex. 35 | 333200 | "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" | Real estate pricing — adult financial context, likely inaccessible to lower grades; $333,200 property presupposes affluent ownership | IC |
| D13 | main | Ex. 44 | 11000 | "James decides to replace his car. He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value." | Car purchasing/depreciation — adult consumer context, not grade-appropriate for K–5 | IC |
| D14 | main | Ex. 13 | 1825 | "Sally and Bob have made plans to go on a trip at the end of the year. They both decide to work as babysitters and save half of what they've earned for their trip. If Sally makes $6 per day and Bob makes $4 per day, how much money will they both have saved for their trip after a year?" | Daily earnings context — money-saving scenario; relatively accessible but income figures quite low in adult framing | IC |
| D15 | main | Ex. 22 | 80 | "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change." | Consumer purchase with tax — contextually generic, accessible, but requires understanding of sales tax | IC |
| D16 | main | Ex. 41 | 347 | "Monika went out for the day and spent some money. She went to the mall and spent $250. Then, she went to the movies and watched 3 movies back to back that each cost $24." | Mall spending $250, back-to-back movies — middle/upper-income leisure context | IC |
| D17 | main | Ex. 1 | 32 | "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards. On Thursday Buddy buys 15/3 = <<15/3=5>>5 baseball cards." | Step-by-step natural language solution with calculator annotations; each step shown | IF/OF |
| D18 | socratic | Ex. 1 | 32 | "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. How many cards does Buddy have on Wednesday? ** On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." | Socratic config breaks solution into sub-questions — scaffolded reasoning format | IF |
| D19 | main | Ex. 19 | 54 | "In the first year, Bobby will acquire 16 * .5 = <<16*.5=8>>8 new cars. After the first year, he will have a total of 16 + 8 = <<16+8=24>>24 cars." | Percentage/growth calculation — multi-step, linguistically accessible, no cultural specificity | IC |
| D20 | main | Ex. 9 | 28 | "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms. The second person lost 7 kilograms less than the first person." | Weight loss framing — potentially sensitive body-image context for K–8 students | IC |
| D21 | main | Ex. 37 | 80 | "Calvin has been saving his hair clippings after each haircut to make a wig for his dog. He is 80% there because (8 / 10) x 100 = 80" | Percentage of goal — whimsical context; linguistically accessible | IC |
| D22 | main | Ex. 45 | 120 | "Let N be the original price each friend was going to pay. 10N=6(N+8), 10N=6N+48, 4N=48, N=<<12=12>>12" | Algebraic equation solving — consistent with 6–8 grade CCSS (6.EE.B.7, 7.EE) but untagged | IO |
| D23 | main | Ex. 12 | 78 | "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." | Repeated doubling/exponential growth — multi-step, no grade tag | IO |
| D24 | main | Ex. 11 | 35 | "If Kimiko is 28, Omi is 2 * 28 years = <<28*2=56>>56 years old. Arlette is 3/4 * 28 years = <<3/4*28=21>>21 years old." | Age relationships with fractions — names include Omi, Kimiko, Arlette (diverse naming) | IC |
| D25 | main | Ex. 10 | 22 | "Kantana loves chocolate. Every Saturday she goes to the candy store and buys 2 chocolates for herself and 1 for her sister." | Weekly purchasing routine — linguistically simple, accessible context | IC |
| D26 | main | Ex. 27 | 9 | "Caleb picked a handful of dandelion puffs. He gave 3 to his mom, another 3 to his sister, 5 to his grandmother, and 2 to his dog." | Nature/sharing context — family-friendly, low-idiom, accessible across demographics | IC |
| D27 | main | Ex. 36 | 1080 | "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest, how many beetles are eaten each day?" | Ecological chain problem — neutral context, no cultural specificity, accessible | IC |
| D28 | main | Ex. 8 | 80 | "Five coaster vans are used to transport students for their field trip. Each van carries 28 students, 60 of which are boys." | School field-trip context — classroom-relevant scenario | IC |
| D29 | main | Ex. 46 | 24 | "Janice's office is on the third floor, and she has to walk up 3 flights of stairs to get to her office. In a single day, she goes up the three flights of stairs 5 times, down the three flights of stairs 3 times." | Adult workplace context (office building) — age-inappropriate for lower grades | IC |
| D30 | main | Ex. 15 | 9 | "Kat decides she wants to start a boxing career. She gets a gym membership and spends 1 hour in the gym 3 times a week doing strength training. She also trained at the boxing gym 4 times a week for 1.5 hours." | Boxing/adult fitness career context — arguably age-inappropriate for younger grades | IC |
| D31 | main | Ex. 24 | 180 | "In a northwestern town, it rained 4 inches per day during the first 15 days of November. For the remainder of the month, the average daily rainfall was twice the amount observed during the first 15 days." | Weather/measurement context — neutral, accessible, no cultural specificity | IC |
| D32 | main | Ex. 4 | 21 | "George bought some food for his trip: a bottle of juice, a sandwich, and a bottle of milk. The sandwich was for $4, and the juice was two times more expensive." | Food/travel context — simple, accessible, no cultural specificity | IC |
| D33 | main | Ex. 42 | 96 | "If Maude's age is 8 by the time Anne's age is four times Emile's age, Emile will be six times as old as Maude, which totals 6*8 = 48 years. If Emile's age is 48 years old by the time Anne's age is twice her number, Anne will be 2*48 = <<48*2=96>>96 years." | Age problem involving very large ages (96 years) derived from abstract conditions — possible internal inconsistency in problem framing | OC |
| D34 | main | Ex. 43 | 720 | "Ariella has $200 more in her son's saving account than Daniella has in her son's savings account. Ariella's account earns her simple interest at the rate of 10% per annum." | Simple interest (non-compound); presupposes annual percentage rate concept | IC |
| D35 | main | Ex. 32 | 2290 | "Daniel has a collection of 346 video games. 80 of them, Daniel bought for $12 each. Of the rest, 50% were bought for $7. All others had a price of $3 each." | Consumer math with large collection — accessible but involves higher dollar totals | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-step arithmetic reasoning is consistently represented
- **Dimension(s):** IO, IF
- **Observation:** All sampled problems require sequential multi-step reasoning, with solutions showing each step explicitly. The benchmark reliably probes the core prerequisite the deployment identifies as a "hard gate" — mathematical accuracy before pedagogical packaging. Problems range from 2-step to 6+ step solutions.
- **Deployment relevance:** Mathematical solution accuracy is the first and non-negotiable filter in the deployment's evaluation hierarchy. GSM8K directly measures this dimension. Any system that fails on GSM8K is likely to generate mathematically inaccurate items, so the benchmark provides a meaningful, if partial, signal.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards. On Thursday Buddy buys 15/3 = <<15/3=5>>5 baseball cards." — Demonstrates 4-step sequential arithmetic with calculator annotations.
  - [D2] Example 6 (main, train, label=54): "First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft. Then figure out what proportion of the aquarium is full after the cat knocks it over: 1/2 * 1/2 = 1/4" — 4-step problem combining volume and proportional reasoning.
  - [D23] Example 12 (main, train, label=78): "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds. It doubled in weight again at 3 months old to reach a weight of 12*2=<<12*2=24>>24 pounds." — Repeated operations requiring sequential tracking across time points.

#### Strength 2: Natural language solutions with embedded step annotations support worked-example evaluation
- **Dimension(s):** IF, OF
- **Observation:** All solutions are expressed as natural language prose with embedded calculator annotations (e.g., `<<30/2=15>>`), providing interpretable reasoning chains. The `socratic` config additionally structures solutions as explicit sub-question/answer pairs, offering a scaffolded format closer to pedagogical worked examples.
- **Deployment relevance:** The deployment requires "verified solutions" and "step-level reasoning chains." While GSM8K only scores the final numeric answer, the natural language solution format means that models tested on this benchmark produce (and are at least partially trained on) the kind of step-by-step explanations the deployment needs. The socratic config's sub-question format is particularly close to the pedagogical scaffolding needed for K–8 formative assessment.
- **Datapoint citations:**
  - [D17] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Natural language with embedded calculation annotations throughout.
  - [D18] Example 1 (socratic, train, label=32): "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. How many cards does Buddy have on Wednesday? ** On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Socratic format with explicit sub-question scaffolding.

#### Strength 3: Some cultural diversity in names and accessible low-complexity contexts
- **Dimension(s):** IC
- **Observation:** Several problems use non-Western names (Kantana, Kimiko, Omi, Arlette, Sab, Dane, Keiko, Amalie, Elsa), and some problem contexts are culturally neutral (weather, animals, plants, basic counting). This provides a partial, undesigned counterweight to the culturally narrow concerns documented elsewhere.
- **Deployment relevance:** The deployment requires diverse names and inclusive contexts. While the name diversity is not systematic or documented as intentional, it does appear in the sampled data. Some problems are genuinely low-idiom and use contexts (dandelion puffs, oranges, rainfall) accessible across demographic groups.
- **Datapoint citations:**
  - [D24] Example 11 (main, train, label=35): "If Kimiko is 28, Omi is 2 * 28 years = <<28*2=56>>56 years old. Arlette is 3/4 * 28 years = <<3/4*28=21>>21 years old." — Three non-Western-European names used naturally in an age-relationships problem.
  - [D26] Example 27 (main, train, label=9): "Caleb picked a handful of dandelion puffs. He gave 3 to his mom, another 3 to his sister, 5 to his grandmother, and 2 to his dog." — Nature-based, family-sharing context with simple language; low cultural specificity.
  - [D27] Example 36 (main, train, label=1080): "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest, how many beetles are eaten each day?" — Ecological context with no cultural referents.

#### Strength 4: Variety of arithmetic skill types represented
- **Dimension(s):** IO
- **Observation:** The sampled problems span a range of mathematical operations: basic four-function arithmetic (Ex. 8, 29), fractions (Ex. 2, 7, 11, 38), percentages (Ex. 14, 19, 28, 37), ratios (Ex. 38), rates (Ex. 26), proportional reasoning (Ex. 7), simple algebra (Ex. 23, 45), and interest calculations (Ex. 43). While unlabeled by CCSS standard, this variety means the benchmark probes a broad set of grade-school arithmetic competencies.
- **Deployment relevance:** Even without CCSS tagging, the breadth confirms that a model performing well on GSM8K has demonstrated multi-domain arithmetic competence — a necessary but not sufficient condition for generating CCSS-aligned items. The diversity reduces the risk that strong GSM8K performance reflects only narrow computational ability.
- **Datapoint citations:**
  - [D7] Example 2 (main, train, label=9): "Anna baked 60 cupcakes. She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes." — Fraction of a whole; consistent with NF domain.
  - [D6] Example 38 (main, train, label=90): "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys, how many will she remain with?" — Ratio and fraction problem; consistent with 6.RP.
  - [D22] Example 45 (main, train, label=120): "Let N be the original price each friend was going to pay. 10N=6(N+8), 10N=6N+48, 4N=48, N=<<12=12>>12" — Algebraic equation solving; consistent with 6–8 EE domain.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: No CCSS standard or grade-level tagging — fundamental ontological mismatch
- **Dimension(s):** IO
- **Observation:** Not a single problem in the 80 sampled examples carries any CCSS domain, cluster, or standard label, nor any grade-level or grade-band annotation. Problems that clearly map to different CCSS domains (fractions at 4.NF, ratios at 6.RP, algebraic equations at 6–7 EE, simple interest at 7.RP) appear without distinction in the same undifferentiated pool.
- **Deployment relevance:** The deployment's core requirement is that teachers specify a CCSS standard at the cluster level (e.g., 4.NF.A.2, 6.RP.A.3) and the system generates an item genuinely targeting that standard. GSM8K cannot validate whether a model correctly operationalizes a named standard because the benchmark contains no standard-level ground truth. This gap is confirmed in every sampled example — it is not a sampling artifact. As the web search findings confirm, this is a full gap with no partial mitigation within the benchmark itself.
- **Datapoint citations:**
  - [D4] Example 23 (main, train, label=220): "Jim collects model cars, and he has 301 models total. Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys." — Algebraic system; could map to 6.EE.B or 7.EE.B, but no tag exists.
  - [D5] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum." — Maps to 7.RP.A.3 (percent problems), but no tag exists; indistinguishable in the dataset from a 3rd-grade addition problem.
  - [D3] Example 7 (main, train, label=90): "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle." — Inverse proportion; maps to 6–7 RP but is unlabeled.

#### Concern 2: No structured MCQ output — categorical output format mismatch
- **Dimension(s):** OO, OF
- **Observation:** Every sampled example is structured as a free-form word problem with a natural language solution and a single numeric final answer. There are no multiple-choice answer options, no distractor choices, and no misconception annotations in any example. The output schema is exclusively `question` (string) + `answer` (string ending in `#### [number]`).
- **Deployment relevance:** The deployment requires evaluating the quality of a complete MCQ package: problem stem + verified correct answer + 3 misconception-grounded distractor choices. GSM8K's output schema provides zero signal about distractor plausibility, and this gap is confirmed across every sampled item. As the web search findings note, automated distractor generation is an unsolved research problem; GSM8K does not even establish a baseline for this dimension.
- **Datapoint citations:**
  - [D17] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards...#### 32" — Output is a natural language solution terminating in a single number; no MCQ structure present.
  - [D7] Example 2 (main, train, label=9): "After giving away 4/5 of the cupcakes, Anna has 60 / 5 = <<60/5=12>>12 cupcakes...#### 9" — No distractor choices, no misconception annotations; typical of entire dataset.

#### Concern 3: Ground-truth labels cover only final numeric answer — all pedagogical output dimensions unlabeled
- **Dimension(s):** OC
- **Observation:** Every solution in the sample is labeled solely by its final numeric answer (the `#### N` convention). There are no labels for: CCSS standard alignment, grade-level language appropriateness, distractor plausibility, step-level reasoning correctness independent of the final answer, or cultural inclusivity. The annotation process documented in the paper (and confirmed by the data structure) checked only arithmetic agreement.
- **Deployment relevance:** The deployment's evaluation hierarchy ranks mathematical accuracy as a "hard gate" (rank 1) but identifies distractor plausibility and CCSS alignment as the primary differentiators of pedagogical value (ranks 2–3). GSM8K labels cover only rank 1. For the deployment's core purpose, this means the large majority of the "correct" construct is entirely unmeasured by any available label in the dataset.
- **Datapoint citations:**
  - [D33] Example 42 (main, train, label=96): "If Maude's age is 8 by the time Anne's age is four times Emile's age, Emile will be six times as old as Maude, which totals 6*8 = 48 years." — The label is only `96`; no information about grade appropriateness, standard alignment, or whether the problem reasoning is pedagogically sound. (Additionally, the question states "two times as old" but the solution uses "four times" — a potential internal inconsistency that the numeric answer label does not flag.)
  - [D1] Example 1 (main, train, label=32): Full multi-step solution labeled only as `#### 32` — pedagogical quality of explanation, grade-level appropriateness, and standard alignment entirely absent from the label.

---

#### MAJOR

#### Concern 4: Pervasive adult financial and consumer contexts inappropriate for lower grade bands
- **Dimension(s):** IC
- **Observation:** A substantial proportion of sampled problems — at least 12 of 47 in the main config — are set in adult financial contexts: paying rent ($1,000/month), buying and selling cars ($20,000–$30,000), real estate pricing ($333,200), beauty contests, car insurance, mall spending ($250), back-to-back movies. These contexts presuppose adult circumstances and middle/upper-income material conditions entirely foreign to K–2 and 3–5 students.
- **Deployment relevance:** The deployment requires grade-level-appropriate language and contexts for K–8, including K–2 (ages 5–7). Adult financial problem contexts (rent, car depreciation, property pricing) are categorically age-inappropriate for lower grades. They also risk stigmatizing students from lower-income households by centering affluent spending contexts. No grade-level filter exists in the benchmark to separate these from child-appropriate problems.
- **Datapoint citations:**
  - [D11] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month." — Adult household budget problem; entirely inappropriate for K–5.
  - [D12] Example 35 (main, train, label=333200): "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" — Property valuation at $333,200 — adult real estate context with no K–8 relevance.
  - [D13] Example 44 (main, train, label=11000): "James decides to replace his car. He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value." — Car resale/negotiation — adult consumer context.
  - [D16] Example 41 (main, train, label=347): "Monika went out for the day and spent some money. She went to the mall and spent $250. Then, she went to the movies and watched 3 movies back to back that each cost $24." — Affluent leisure spending context, 3 movies back-to-back.

#### Concern 5: Culturally narrow US-specific contexts present without inclusivity screening
- **Dimension(s):** IC
- **Observation:** Several problems embed US-specific cultural contexts that would be inaccessible or exclusionary for multilingual learners or students from non-mainstream backgrounds: American football scoring rules (touchdowns and 2-point conversions), brand-name US candy (Reese's, Snickers, Skittles), a beauty and modeling contest (gender-stereotyped), and workplace/adult scenarios (office building, boxing career, fountain in a mall).
- **Deployment relevance:** The deployment explicitly requires avoiding "culturally narrow references (assumed family structures, regionally specific foods, particular sports with uneven US cultural distribution)" and "low-idiom language to support multilingual learners." American football rules (touchdown values, 2-point conversions) require specific sports cultural knowledge that many ELL students and students from non-sports-oriented households will not have. Brand-name candy references are US-specific consumer culture. These contexts confirm the absence of any inclusivity screening in the benchmark's design.
- **Datapoint citations:**
  - [D9] Example 18 (main, train, label=72): "James joins a football team and becomes the star. He scores 4 touchdowns per game and each touchdown is worth 6 points...He also manages to score 2 point conversions 6 times during the season." — Requires knowledge of American football scoring rules (touchdown = 6 points, 2-point conversion) — culturally exclusionary for ELL students.
  - [D8] Example 3 (main, train, label=99): "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." — US brand-name candy that may be unfamiliar to recent immigrant families or ELL students.
  - [D10] Example 34 (main, train, label=500): "Rachel and Sara want to attend a beauty and modeling contest. They both want to buy new pairs of shoes and dresses. Sara buys a pair of shoes which costs $50 and a dress which costs $200." — Gender-stereotyped beauty/modeling context; not culturally inclusive.

#### Concern 6: No grade-band differentiation — problems span K–8 implicitly without labeling
- **Dimension(s):** IO, IC
- **Observation:** Problems in the sample range from what appears to be 2nd-grade level (simple addition/subtraction, e.g., Ex. 8 or Ex. 27) to what appears to be 7th–8th-grade level (algebraic systems, Ex. 23; simple interest, Ex. 43; ratio problems, Ex. 38). However, no grade-level or grade-band label exists for any problem. A model performing at a given GSM8K accuracy level could be strong on 6–8 grade problems and weak on K–2 problems, or vice versa, with no way to detect this from the benchmark.
- **Deployment relevance:** Teachers specify grade level at generation time (K–2, 3–5, 6–8 bands). GSM8K cannot validate grade-differentiated generation capability. A model could ace GSM8K by being excellent at 7th-grade algebra while completely failing to generate appropriate K–2 items — and this failure would be invisible in the benchmark score.
- **Datapoint citations:**
  - [D28] Example 8 (main, train, label=80): "Five coaster vans are used to transport students for their field trip. Each van carries 28 students, 60 of which are boys." — Simple 2-step arithmetic; consistent with 2nd–3rd grade level.
  - [D4] Example 23 (main, train, label=220): "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys...11x+15=301, 11x=286, x=26" — Multi-variable algebraic system; 7th–8th grade level.
  - [D5] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum." — Simple interest rate; 7th grade CCSS (7.RP.A.3) — same dataset pool as the 2nd-grade-level Ex. 8.

#### Concern 7: Body weight/weight loss contexts — potentially sensitive for K–8 populations
- **Dimension(s):** IC
- **Observation:** At least one problem (Ex. 9) centers on weight loss as its primary context: "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms." This framing normalizes weight loss as a mathematical context in a way that may be developmentally inappropriate and potentially harmful for K–8 students, particularly in higher-grade bands where body image concerns are prevalent.
- **Deployment relevance:** The deployment requires culturally sensitive content that avoids stigmatizing contexts. While weight loss is not explicitly named in the deployment's list of sensitive contexts, it aligns with the broader sensitivity requirement. For a teacher generating formative assessment items for 6th–8th graders, weight loss as a problem context is a notable cultural sensitivity concern.
- **Datapoint citations:**
  - [D20] Example 9 (main, train, label=28): "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms. The second person lost 7 kilograms less than the first person." — Weight loss framing as primary context; potentially sensitive for K–8 students.

---

#### MINOR

#### Concern 8: Some problems contain adult workplace and leisure contexts of limited K–8 relevance
- **Dimension(s):** IC
- **Observation:** Beyond the major financial concerns, several problems center on adult workplace contexts (Janice's office building, Ex. 46; a company's commuting patterns, Ex. 28) or adult leisure/career contexts (Kat's boxing career, Ex. 15). These are not culturally harmful but are contextually misaligned with K–8 classroom experiences.
- **Deployment relevance:** Grade-level appropriateness of context is a deployment requirement. Office buildings, adult career decisions, and commuting patterns are not contexts that K–8 students experience, reducing the ecological validity of problems that might otherwise be mathematically suitable.
- **Datapoint citations:**
  - [D29] Example 46 (main, train, label=24): "Janice's office is on the third floor, and she has to walk up 3 flights of stairs to get to her office. In a single day, she goes up the three flights of stairs 5 times." — Adult office workplace context.
  - [D30] Example 15 (main, train, label=9): "Kat decides she wants to start a boxing career. She gets a gym membership and spends 1 hour in the gym 3 times a week doing strength training. She also trained at the boxing gym 4 times a week for 1.5 hours." — Adult career/fitness context.

#### Concern 9: Potential internal reasoning error in at least one sampled problem
- **Dimension(s):** OC
- **Observation:** Example 42 (main, label=96) has a notable internal inconsistency: the question states "By the time Anne is two times as old as Emile" but the solution treats this as "four times" in the first sentence ("If Maude's age is 8 by the time Anne's age is four times Emile's age"). The numeric answer (96) follows from the solution's logic but may not follow from the question as written.
- **Deployment relevance:** The benchmark's 1.7% documented breaking-error rate is consistent with some errors appearing in the sample. For the deployment, this is a minor concern: the benchmark is not being used for training data directly, but it does confirm that subtle errors exist in the label set, slightly reducing confidence in the benchmark as an accuracy ground truth.
- **Datapoint citations:**
  - [D33] Example 42 (main, train, label=96): "By the time Anne is two times as old as Emile...If Maude's age is 8 by the time Anne's age is four times Emile's age, Emile will be six times as old as Maude, which totals 6*8 = 48 years." — Question says "two times" but solution uses "four times"; label of 96 follows solution logic, not necessarily question logic.

#### Concern 10: Calculator annotations (`<<...>>`) in solutions may create form noise for some downstream uses
- **Dimension(s):** IF
- **Observation:** All solutions contain embedded calculator annotation tokens in the format `<<expr=result>>` (e.g., `<<30/2=15>>`). These are training artifacts not present in natural classroom-ready worked examples.
- **Deployment relevance:** If GSM8K solutions are used as reference examples for what a "good worked solution" looks like, the calculator annotation format would need to be stripped. This is a minor preprocessing concern rather than a fundamental validity issue, since the deployment's evaluation need is primarily about final correctness and reasoning quality, not the annotation format.
- **Datapoint citations:**
  - [D17] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Calculator annotations present throughout all solutions; not present in natural instructional text.

---

### Content Coverage Summary

The 80 sampled examples confirm the benchmark's character as described in documentation: an undifferentiated pool of grade-school math word problems requiring multi-step arithmetic, presented in natural language with step-by-step solutions. Mathematical operations across the sample span basic four-function arithmetic, fractions, percentages, ratios, rates, proportional reasoning, and introductory algebra — a broad spread that confirms the benchmark probes generalizable arithmetic competence.

Problem contexts are predominantly US everyday life, with a notable tilt toward adult financial and consumer scenarios (rent, car purchase, property pricing, mall spending), American-sports-specific contexts (football scoring), and brand-name consumer products (Reese's, Snickers, Skittles). Approximately 25–30% of the sampled problems embed adult-world contexts that would be inappropriate for lower grade bands (K–2, 3–5). The deployment's specific concerns about culturally narrow references are confirmed by direct observation in the data. Conversely, approximately 30–35% of problems use genuinely neutral, accessible contexts (nature, animals, basic school scenarios, weather) that would translate well across demographic groups, and name diversity (Kantana, Kimiko, Omi, Keiko, Amalie) is present though not systematic.

The socratic config (33 examples) is identical in question content to the main config but structures solutions as explicit sub-question/answer pairs — a format moderately closer to scaffolded instructional design, though still entirely lacking CCSS tags, grade-level labels, or MCQ structure.

The benchmark's two-column schema (question, answer) with numeric final-answer labels confirms that every dimension of the deployment's evaluation construct beyond arithmetic accuracy — CCSS standard alignment, distractor plausibility, grade-level language appropriateness, cultural inclusivity — is entirely absent from the data structure. This is not a gap that could be addressed by additional data sampling from the same benchmark; it is a structural property of what the benchmark measures.

---

### Limitations

1. **Sample size:** 80 examples from a dataset of 8,792 (train + test across both configs) represent approximately 0.9% of the total. Cultural context patterns observed (prevalence of adult financial scenarios, sports references) may not hold at the same rate across the full dataset, though the documented design process provides no reason to expect systematic improvement.

2. **Grade-level inferences are analyst estimates, not dataset labels:** Observations about which problems map to K–2 vs. 6–8 CCSS domains are based on analyst judgment about mathematical content, not any ground-truth annotation. The dataset contains no grade-level labels.

3. **CCSS mapping inferences are analyst estimates:** Observations linking specific problems to CCSS domains (e.g., "consistent with 6.RP") reflect analyst judgment. No automated or human-verified CCSS alignment has been performed on the dataset.

4. **Cultural inclusivity assessment is qualitative:** The observation that certain contexts (football, brand-name candy, beauty contests) are culturally narrow reflects judgment based on the deployment's stated requirements. No quantitative cultural audit methodology was applied.

5. **Socratic config not independently sampled:** The socratic examples reviewed are identical questions to the main config examples, with only solution format differing. No novel problem content was reviewed from the socratic config.

6. **Error detection is opportunistic:** The internal inconsistency identified in Example 42 was noticed during review but a systematic error audit was not performed. The benchmark's 1.7% documented error rate implies roughly 1–2 errors would be expected in an 80-example sample; finding one is consistent with, not a comprehensive audit of, the documented quality level.

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
  "benchmark": "gsm8k",
  "region": "US K–8 Edtech: CCSS-Aligned Math Assessment Item Generation",
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
