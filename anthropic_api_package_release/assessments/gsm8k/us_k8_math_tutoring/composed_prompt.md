I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **Grade School Math 8K (GSM8K)** is valid for use in **US K-8 Math Tutoring Platform — Homework Checker Deployment**.

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
- **Full Name**: Grade School Math 8K (GSM8K)
- **Domain**: Math word problem solving (grade school arithmetic reasoning)
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
GSM8K's primary task category is multi-step arithmetic word problem solving. The
paper frames this as requiring both reading comprehension and logical reasoning [Q22],
with solutions depending "only on elementary concepts" to keep high performance
tractable [Q11]. The benchmark supports two evaluation paradigms — a finetuning
baseline generating a single solution and a verification approach that samples
multiple candidates and ranks them [Q27, Q30] — with further subdivision into
solution-level and token-level verifier designs [Q72, Q73, Q74]. Optional dropout
regularization is explored as an auxiliary technique for both paradigms [Q89].

The paper emphasizes "high diversity among problems" as a core design goal [Q10]
and explicitly notes that GSM8K provides natural language solutions and on average
requires more steps to solve than comparable datasets like ASDiv [Q19]. However,
the paper does not enumerate specific arithmetic subtopics covered (e.g., fractions,
measurement conversions, basic statistics, area/perimeter). The qualitative samples
shown in the paper illustrate weight-based and food-quantity word problems [Q128,
Q133, Q136], suggesting everyday arithmetic contexts, but do not demonstrate
coverage of statistics or geometry sub-skills. There is no documented taxonomy
confirming that US customary unit conversions, mean/median problems, or
area/perimeter word problems are systematically represented.

The paper also acknowledges that state-of-the-art models struggle on GSM8K
"primarily due to the high diversity among problems" [Q10], and naive extrapolation
suggests reaching 80% solve rate would require a model with 10^16 parameters [Q48],
indicating the benchmark is calibrated for upper-elementary and above difficulty
levels rather than K-2 single-step arithmetic.

### Input Content
GSM8K consists of 8,500 problems written by freelance contractors hired through
Upwork and subsequently scaled through Surge AI [Q103, Q104]. Problems were designed
to have "high linguistic diversity while relying on relatively simple grade school
math concepts" [Q9]. Seed questions automatically generated by a few-shot prompted
175B GPT-3 model were provided to contractors as optional starting points [Q110];
contractors could use seeds directly, modify them, or write original problems [Q111].
Contractors were instructed to be descriptive in solutions and to avoid reusing
problem templates [Q112], with pairwise similarity scoring used to enforce diversity
[Q113].

Critically, the paper does not specify the nationality, geographic distribution, or
demographic background of the Upwork or Surge AI contractors. All authors are
affiliated with OpenAI, a US-based organization [Q7, Q102], and the primary region
label is United States, but there is no documented assurance that problems were
written by US-based workers or that problems were explicitly calibrated to US Common
Core standards, US customary units (feet/inches, cups/gallons, pounds/ounces), or
US dollar/cent denominations. The benchmark also draws on comparisons to ASDiv and
prior math word problem datasets [Q15, Q17, Q25, Q26], which may carry diverse
cultural conventions from their own collection processes.

### Input Form
All inputs are natural language text in English [Q9, Q32]. Problems are written in
prose form and require the model to parse natural language before performing
arithmetic reasoning. The paper notes that "it is important to allow the model to
generate the full natural language solution before outputting a final answer" [Q56],
confirming that problems are presented as complete prose word problems rather than
symbolic or structured mathematical expressions. No audio, image, or structured
database formats are involved.

Calculator annotations were injected into the training set using hard-coded logic
and a finetuned language model [Q117], enabling models to invoke a Python-based
calculator during inference [Q40, Q120, Q121] — a text-level preprocessing
convention that is transparent to the input representation. The paper discusses
model architecture using GPT-3 family models at 6B and 175B parameter scales [Q35],
with residual dropout applied during training [Q90, Q91]; these are infrastructure
details that do not alter the text-input character of the benchmark.

### Output Ontology
Ground-truth labels are final numerical answers to word problems. Verifiers are
trained to output a binary correct/incorrect judgment conditioned on whether a
candidate solution reached the correct final answer [Q31, Q59, Q60]. The output
taxonomy is therefore a single binary correctness label mapped to a scalar
probability [Q59], with the highest-scoring completion selected at test time [Q3,
Q68]. An optional majority-voting extension allows top-K verifier-ranked solutions
to cast votes based solely on their final numerical answers [Q85, Q87].

The output ontology is narrow and objective: correctness is determined solely by
whether the final numerical answer matches the ground truth, regardless of the
quality or validity of intermediate reasoning [Q60]. This creates a well-documented
false positive risk — some solutions reach the correct final answer via flawed
reasoning [Q61] — but does not introduce culturally variable decision boundaries.
The binary correct/incorrect schema does not depend on cultural norms or regional
value frameworks.

### Output Content
Ground-truth answers are final numerical values for arithmetic problems, verified
by having a second set of contractors re-solve all problems (no worker re-solved
problems they originally wrote) and comparing final answers to the originals [Q105,
Q106]. A subsequent agreement check on a subset found a 1.7% disagreement rate,
which the authors estimate represents problems with breaking errors or ambiguities
[Q107, Q108], with an acknowledgment that a larger percentage may contain subtle
errors [Q109].

Calculator annotations were not human-generated but produced by automated logic and
a finetuned model [Q117]; this annotation layer has a documented imperfection where
the logic may miss some annotatable lines [Q118]. The paper acknowledges minor
implementation bugs in the calculator that cause the reported test performance to
be a slight underestimate, with the discrepancy less than 1% in most experiments
[Q123, Q124, Q125].

NOT DOCUMENTED: The paper does not report the geographic location, native language,
or demographic characteristics of the Upwork or Surge AI contractors who wrote or
re-solved problems. This means there is no documented assurance that ground-truth
labels were validated by workers familiar with US Common Core conventions, which is
relevant if problems carry ambiguous unit conventions. Annotator agreement metrics
were obtained from contractor re-solving rather than independent cultural expert
review.

### Output Form
The primary evaluation metric is solution accuracy: the percentage of test problems
for which the model produces the correct final numerical answer [Q29, Q46]. The
paper introduces the test@N metric — the percentage of problems solved correctly at
least once across N guesses [Q52] — using T=0 for test@1 and T=0.7 for test@100
[Q53, Q54], with both values chosen empirically [Q54]. Verification performance is
evaluated by sampling 100 completions per test problem and selecting the
highest-ranked by the verifier [Q68, Q84], with experiments showing performance
improves up to 400 completions before degrading [Q82, Q83].

Token-level verifiers produce a per-token scalar value visualizable as a heat map
[Q147, Q148, Q149, Q150, Q151], enabling interpretability beyond a final binary
label. The paper demonstrates that token-level verifiers outperform solution-level
verifiers [Q76] and that including the language modeling objective is a strict
improvement [Q80]. The output modality is text — final numerical answer strings —
and the evaluation metric is exact-match correctness of those numerical answers,
with no partial credit or step-scoring component.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems." |
| Q2 | 1 | output_ontology | "To increase performance, we propose training verifiers to judge the correctness of model completions." |
| Q3 | 1 | output_form | "At test time, we generate many candidate solutions and select the one ranked highest by the verifier." |
| Q4 | 1 | output_form | "We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline." |
| Q5 | 1 | input_ontology | "One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes (Shen et al., 2021a)." |
| Q6 | 1 | input_ontology | "When generating a solution, autoregressive models have no mechanism to correct their own errors." |
| Q7 | 1 | input_content | "Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman, OpenAI" |
| Q8 | 2 | input_content | "We are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level." |
| Q9 | 2 | input_form | "We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts." |
| Q10 | 2 | input_ontology | "State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems." |
| Q11 | 2 | input_ontology | "At the same time, GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal." |
| Q12 | 2 | input_content | "We present a curated dataset of 8.5K grade school math questions and natural language solutions, useful for probing the informal reasoning ability of large language models." |
| Q13 | 2 | output_form | "We show that, compared to a finetuning baseline, the use of verifiers results in approximately the same performance boost as a 30x model size increase, and that verifiers scale significantly better with increased data." |
| Q14 | 2 | output_form | "We show that dropout acts as a strong regularizer, significantly improving performance for both finetuning and verification." |
| Q15 | 3 | input_content | "Early math word problem datasets (Kushman et al., 2014; Roy and Roth, 2015) are relatively small and are not well suited for testing the limits of modern language models." |
| Q16 | 3 | input_content | "Dolphin18K (Huang et al., 2016) is a larger dataset containing" |
| Q17 | 4 | input_content | "The recently developed ASDiv dataset (Miao et al., 2021), which contains 2.3K math word problems, addresses common flaws in prior datasets by ensuring problems have both high diversity and high quality." |
| Q18 | 4 | input_content | "We share those design principles in the creation of GSM8K." |
| Q19 | 4 | input_ontology | "However, we note that GSM8K is larger, provides natural language solutions, and consists of problems that on average require more steps to solve." |
| Q20 | 4 | input_ontology | "The MATH dataset (Hendrycks et al., 2021) is larger and significantly more complex than GSM8K, but the high difficulty makes it challenging to accurately measure progress given the current capabilities of state-of-the-art language models." |
| Q21 | 4 | input_ontology | "Similar to CommonsenseQA, GSM8K includes questions that require basic background knowledge, like the number of days in a week." |
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
| Q35 | 6 | input_form | "For both methods, we use models from the GPT-3 family as our initialization, primarily focusing on the 175B and 6B model sizes." |
| Q36 | 6 | input_ontology | "The 175B model is the largest and produces the most impressive results, while the 6B model is significantly more convenient for research purposes." |
| Q37 | 6 | input_form | "We discuss hyperparameter choices in Appendix B." |
| Q38 | 6 | output_content | "Our models frequently fail to accurately perform calculations." |
| Q39 | 6 | output_content | "Although larger models make fewer arithmetic mistakes than smaller models, this remains a common source of errors." |
| Q40 | 6 | input_form | "To mitigate this issue, we train all models to use a calculator by injecting calculation annotations into the training set." |
| Q41 | 6 | output_form | "At test time, a calculator will override sampling when the model chooses to use these annotations." |
| Q42 | 6 | input_form | "Details can be found in Appendix C." |
| Q43 | 6 | input_form | "We perform finetuning by updating model parameters to minimize the cross-entropy loss over all training tokens." |
| Q44 | 6 | input_ontology | "Figure 2 shows test performance after finetuning on training sets of varying sizes for 20 epochs." |
| Q45 | 6 | output_form | "We visualize the same data both as a function of training set size and as a function of model size." |
| Q46 | 6 | output_form | "Test performance is determined by a single low temperature (T = 0) sample for each test problem." |
| Q47 | 6 | input_ontology | "Unsurprisingly, we see that the 175B model significantly outperforms the smaller models." |
| Q48 | 6 | input_ontology | "Assuming a log-linear trend, we can naively extrapolate these results to estimate that a model with 10^16 parameters would be required to reach an 80% solve rate, when using the full GSM8K training set." |
| Q49 | 6 | input_ontology | "It is even harder to extrapolate along the data dimension, since performance does not appear to follow a log-linear trend." |
| Q50 | 6 | input_ontology | "Nevertheless, it appears likely that the 175B model would require at least two additional orders of magnitude of training data to reach an 80% solve rate." |
| Q51 | 6 | output_form | "In Figure 3, we show how 6B test performance varies over the course of 100" |
| Q52 | 7 | output_form | "We use test@N to denote the percentage of problems solved correctly at least once when allowing the model to make N separate guesses for each problem." |
| Q53 | 7 | output_form | "We use a low temperature (T = 0) to generate test@1 samples and we use a higher temperature (T = 0.7) to generate test@100 samples." |
| Q54 | 7 | output_form | "Both temperature values were chosen empirically to produce the best results." |
| Q55 | 7 | input_content | "For this reason, we use models trained for 2 epochs to generate samples for training verifiers." |
| Q56 | 7 | input_form | "We also note that it is important to allow the model to generate the full natural language solution before outputting a final answer." |
| Q57 | 7 | output_form | "If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%." |
| Q58 | 7 | output_ontology | "To improve upon the finetuning baseline, we train verifiers to judge the correctness of model-generated solutions and search against these verifiers at test time." |
| Q59 | 7 | output_ontology | "Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct." |
| Q60 | 7 | output_ontology | "Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer." |
| Q61 | 7 | output_content | "In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives." |
| Q62 | 8 | input_form | "As shown in Figure 4, we train the verifier as follows: 1. Finetune a model (the "generator") for 2 epochs on the training set. 2. Sample 100 completions from the generator for each training problem and label each solution as correct or incorrect. 3. Train a verifier for a single epoch on this dataset." |
| Q63 | 8 | input_ontology | "Training for 2 epochs is enough for the generator to learn basic skills in this domain." |
| Q64 | 8 | input_content | "We choose not to train for longer, since the diversity of generated solutions begins to collapse after this point, as shown in Figure 3." |
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
| Q89 | 11 | input_ontology | "We find that both finetuning and verification strongly benefit from the use of dropout as a regularizer." |
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
| Q111 | 15 | input_content | "Contractors were allowed to use those seed questions directly, to use them as inspiration and make modifications, or to come up with their own questions entirely." |
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
| Q128 | 19 | input_ontology | "The meat and context books weigh 2 pounds each, the French book weighs 3 pounds and the English book weighs 1 pound, and the total weight book sit in is for English task, if today is a nice day, what is the total weight of all the books?" |
| Q129 | 19 | input_ontology | "The meat and context books weigh 2 pounds each so they weigh 2*2 = 4=2=6=8 pounds together, the French book weighs 3 pounds and so the total weight of the English book is 6+3 = 10, so if you add up all of the books together, the total weight is 4+3+4 = 11" |
| Q130 | 19 | input_ontology | "Our generated responses weigh books weigh 2 pounds each to a total of 2*2 = or2=4 pounds, use French book weigh 4 pounds and the English book weighs 3 pounds, to a total of 4+3 = or4+3=7 pounds, if so if you add up all of the books, the total weight of the English book, to a total of 3+3 = or2=4=8 pounds" |
| Q131 | 19 | input_ontology | "The English book weight 3 pounds, So all of our books weigh 2 + 4 + 3 = 9=10 =9=10=9=10 pounds." |
| Q132 | 19 | input_ontology | "The total weight of books read at science books is 2*2=or2=4=6=8 pounds total weight of all the books is 4+3=or2=4+3=7 pounds." |
| Q133 | 19 | input_ontology | "The German Shepherd dog contains 1.5 + = or1+1=1.5=1 diggrams of dog food per day the dog also contains 2.5 +3=or2=5.5 diggrams of dog food per day, During a week, the total is 2.5 + or2+1=3=1+1.5=1 diggrams of dog food is a week." |
| Q134 | 19 | input_ontology | "Our data 1000=or1=1.5=1.5 diggrams per day for the German Shepherd, if the dog weighs 3.2 + or3+1.7=or3=1.9=1.5 diggrams of dog food per week." |
| Q135 | 19 | input_ontology | "The German Shepherd's total consumption is 1.5 + =or1=1.5=1.5 diggrams, the dog also and consumption total food per meal is 3.2 + = or3=2.5=1.5=1.5 diggrams." |
| Q136 | 19 | input_ontology | "The 2 German Shepherd dogs consumes 1.5 + =or1+1=1.5=1.5 diggrams of food per day, the 2 bulldogs consumes 2.3 + =or2=2.5=2.5=1.5 diggrams of food per day." |
| Q137 | 20 | output_ontology | "As noted in section 4.2, we train verifiers with a joint objective where the model learns to label a model completion as correct or incorrect, in addition to the original language modeling objective." |
| Q138 | 20 | output_ontology | "Architecturally, this means our verifiers are language models, with a small scalar head that outputs predictions on a per-token basis." |
| Q139 | 20 | output_ontology | "We implement this scalar head as a single bias parameter and single gain parameter that operate on the logits outputted by the language model's final unembedding layer." |
| Q140 | 20 | input_form | "We can choose to initialize the verifier from the same pretrained language model the generator was finetuned from, or from the generator itself." |
| Q141 | 20 | output_form | "In our ablations the latter performed slightly better; we suspect this is because better understanding the language distribution that the generator learned should only aid the verifier in scoring samples from that distribution." |
| Q142 | 20 | input_form | "Unless otherwise explicitly stated, we initialize our verifiers from their corresponding generators in all experiments." |
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
name: US K-8 Math Tutoring Platform — Homework Checker Deployment
abbreviation: US-K8-MATH
deployment_description: An LLM-powered homework-checker embedded in a US K-8 math
  tutoring platform. The system receives arithmetic word problems as plain English
  text and performs a binary correct/incorrect judgment on a student's submitted final
  numerical answer. No partial credit, intermediate-step scoring, or written-reasoning
  evaluation is required.
target_population:
  description: American elementary and middle school students in grades K-8, with
    the highest-volume cohort in grades 3-6. Students access the platform nationwide
    with no sub-national geographic targeting specified. Problems are authored to
    US Common Core State Standards for Mathematics (CCSS-M) and use US customary units,
    US dollar/cent currency, and culturally familiar American settings.
  geography: United States (nationwide; no sub-national targeting)
  grade_range: K-8 (grades K-2 present but lower volume; grades 3-6 highest volume;
    grades 6-8 included for fractions, decimals, percentages, ratios)
  age_band_approximate: Ages 5-14
  institutional_context: Consumer-facing tutoring platform; not a single school district
    or state system
languages:
  instruction_language: English (US)
  other_languages_supported: None — platform is English-only
  script: Latin alphabet
curriculum_standards:
  primary_standard: US Common Core State Standards for Mathematics (CCSS-M)
  standard_body: National Governors Association / Council of Chief State School Officers
  adoption_status: '41 states plus DC have currently adopted CCSS-M; 46 states initially
    adopted but several have since repealed or replaced (Indiana, Arizona, Oklahoma,
    South Carolina, Florida, Idaho among those that withdrew or renamed). Four states
    never adopted at all: Texas, Virginia, Alaska, and Nebraska; Minnesota adopted
    ELA only, not math. Several other states renamed or revised the standards while
    retaining substantial alignment. For a nationwide consumer platform, the great
    majority of students are in CCSS-M or CCSS-M-aligned states, but students in the
    ~9 non-adopting/withdrawn states may encounter platform problems calibrated to
    standards their state does not officially use. Sources: CCSS Initiative adoption
    map — [WEB-1]; World Population
    Review 2026 — [WEB-2];
    Wikipedia CCSS implementation by state — [WEB-3]'
  grade_band_topics:
    K-2: Single-step whole-number arithmetic, counting, basic measurement concepts
    3-4: Multi-step problems with four operations on multi-digit numbers, introduction
      to fractions, US customary measurement
    '5': Multi-step fractions, decimals, volume, continued measurement conversion
    6-8: Ratios, percentages, proportional reasoning, basic statistics (mean/median
      from small datasets), area and perimeter word problems, introduction to metric
      exposure per CCSS-M
problem_type_inventory:
  core_operation_types:
  - Addition, subtraction, multiplication, division on multi-digit whole numbers
  - Multi-step combinations of the four operations
  - Fraction arithmetic (addition, subtraction, multiplication, division)
  - Decimal arithmetic
  - Percentage calculations
  - Ratio and proportion
  measurement_and_geometry:
  - US customary unit conversion (feet↔inches, cups↔gallons, pounds↔ounces, miles,
    quarts, etc.)
  - Area and perimeter word problems (rectangles, composite shapes)
  - Basic volume word problems
  - Metric unit exposure (limited, upper-grade CCSS-M mandated)
  data_and_statistics:
  - Mean calculation from small datasets
  - Median calculation from small datasets
  excluded_types:
  - Formal geometry proofs
  - Algebraic symbol manipulation beyond arithmetic reasoning
  - Trigonometry or advanced statistics
cultural_and_contextual_norms:
  currency: 'US dollars and cents exclusively (symbol: $; denominations: pennies,
    nickels, dimes, quarters, dollars)'
  unit_system: US customary as primary; metric appears only where explicitly required
    by upper-grade CCSS-M
  cultural_settings_in_problems: 'American everyday contexts: school cafeterias, sports
    practice, shopping, birthday parties, home improvement, US holidays, American
    sports'
  language_register: Plain American English appropriate for elementary/middle school
    reading level
  sensitivity_considerations: No politically sensitive content expected; student-age-appropriate
    problem framing required; no religious or partisan content
evaluation_task_structure:
  input_format: Natural language arithmetic word problem presented as plain English
    text
  output_requirement: Binary correct/incorrect judgment on submitted final numerical
    answer only
  partial_credit: false
  intermediate_step_evaluation: false
  written_reasoning_evaluation: false
  answer_format: Single numerical value (integer, decimal, or fraction as appropriate
    to grade level)
  scoring_convention: An unconventional solution method yielding the correct numerical
    answer is scored as correct
benchmark_alignment_summary:
  benchmark: GSM8K (Grade School Math 8K, 2021)
  primary_region_label: United States
  language_match: Full — both deployment and benchmark are English-only
  modality_match: Full — both are plain text word problems
  output_schema_match: High — GSM8K uses binary correct/incorrect final-answer grading
    identical to deployment requirement
  curriculum_alignment_status: Partial — GSM8K targets grade school multi-step arithmetic
    broadly but was not explicitly designed to CCSS-M; no documented taxonomy of subtopic
    coverage
  benchmark_saturation_note: 'As of 2025-2026, leading models achieve ~95%+ on GSM8K
    (e.g., Gemini-2.5-Pro at 95.22%), indicating the benchmark may no longer reliably
    differentiate strong from very strong LLMs for this deployment''s upper-grade
    problems. Downstream scorers should note that near-ceiling performance does not
    guarantee generalization to platform-specific subtopics (measurement conversion,
    statistics, area/perimeter) absent from GSM8K. Source: GSM8K-V paper — [WEB-4]'
dimension_priority_weights:
  IO:
    priority: MODERATE
    rationale: GSM8K covers core multi-step arithmetic well, but measurement conversions,
      basic statistics (mean/median), and area/perimeter problems are not documented
      as systematically represented and may be underrepresented.
  IC:
    priority: MODERATE
    rationale: Platform uses US dollars, US customary units, and American cultural
      settings exclusively. GSM8K carries a 'transferred from different cultural context'
      metadata flag despite a US primary region label; contractor demographics and
      nationality are undocumented, introducing non-trivial risk of non-US unit or
      currency conventions in some problems.
  IF:
    priority: LOWER
    rationale: Both benchmark and deployment are text-only English; no modality, script,
      or language mismatch.
  OO:
    priority: LOWER
    rationale: Deployment requires binary correct/incorrect final-answer checking;
      GSM8K's verifier training signal is defined identically. Direct structural alignment.
  OC:
    priority: LOWER
    rationale: Ground-truth labels are arithmetically verifiable numerical answers;
      correctness is objective and not subject to cultural interpretation.
  OF:
    priority: LOWER
    rationale: GSM8K produces a final numerical answer label mapping directly onto
      the platform's binary answer-checking output; no format mismatch.
flagged_gaps:
- id: GAP-1
  label: US customary unit conversion problems
  description: US customary unit conversion problems (feet↔inches, cups↔gallons, pounds↔ounces)
    appear regularly on the platform and are CCSS-M-aligned. GSM8K's paper does not
    enumerate unit systems used, and contractor nationality is undocumented.
  gap_type: partial
  web_search_target: 'Multiple independent sources confirm GSM8K does include basic
    measurement conversions as a content type (listed among ''percentages, fractions,
    ratios, work rates, and basic measurement conversions''), and the standard version
    is described as US-centric using ''names, currencies, and scenarios typical of
    Western grade-school curricula.'' However, no systematic enumeration of how frequently
    US customary unit conversion problems appear (vs. generic measurement) has been
    published; the gap in documented frequency remains. Sources: Emergent Mind GSM8K
    topic summary — [WEB-5]'
- id: GAP-2
  label: Basic statistics problems (mean/median)
  description: Mean and median calculations from small datasets are part of the platform's
    grades 6-8 problem set per CCSS-M. GSM8K does not document coverage of data/statistics
    word problems; sample problems shown in the paper are all arithmetic-only.
  gap_type: full
  web_search_target: 'Confirmed full gap. Multiple independent sources consistently
    characterize GSM8K''s mathematical content as ''elementary arithmetic (+, −, ×,
    ÷)'' with no statistics component. One source explicitly lists GSM8K content as
    ''percentages, fractions, ratios, work rates, and basic measurement conversions''
    — mean/median are absent from all enumerations. Another source confirms ''no advanced
    mathematics (no geometry, quadratics, combinatorics)'' with no statistics mentioned.
    The HuggingFace official card states ''solutions primarily involve performing
    a sequence of elementary calculations using basic arithmetic operations.'' No
    source contradicts this: GSM8K has no documented statistics (mean/median) problems.
    Sources: Emergent Mind GSM8K dataset — [WEB-5];
    HuggingFace openai/gsm8k — [WEB-6]; Brenndoerfer
    GSM8K analysis — [WEB-7]'
- id: GAP-3
  label: Area and perimeter word problems
  description: The platform includes area and perimeter word problems regularly. GSM8K
    does not enumerate geometry sub-skills; no paper evidence that area/perimeter
    problems are systematically present.
  gap_type: full
  web_search_target: 'Confirmed full gap. Two independent sources explicitly state
    GSM8K contains ''no advanced mathematics (no geometry, quadratics, combinatorics)''
    and that ''success on this benchmark does not imply capability in algebra, geometry,
    calculus, or advanced mathematical reasoning.'' The computational vocabulary is
    described as ''addition, subtraction, multiplication, and division over natural
    numbers.'' Area and perimeter are not mentioned in any enumeration of GSM8K subtopics.
    Sources: Emergent Mind GSM8K dataset — [WEB-5];
    Brenndoerfer GSM8K analysis — [WEB-7]'
- id: GAP-4
  label: US cultural context fidelity (currency, settings)
  description: Despite US primary region label, GSM8K carries a 'transferred from
    different cultural context' metadata flag. Contractor nationality is undocumented;
    GPT-3 seed problems may carry non-US conventions. No explicit confirmation of
    US dollar/cent usage or American cultural settings throughout the dataset.
  gap_type: partial
  web_search_target: 'Partially resolved. Multiple sources confirm that ''the standard
    version is US-centric, using names, currencies, and scenarios typical of Western
    grade-school curricula,'' and that GPT-3 seeds instructed workers to ''vary scenarios
    (such as objects, activities, and measuring units).'' This supports a primarily
    US-conventional framing. However, contractor nationality remains undocumented
    in the original paper, and the ''transferred from different cultural context''
    metadata flag is not contradicted. Recent cultural adaptation work (Tomar et al.,
    2025) that created China/India/Japan/Korea/Africa variants confirms the original
    is implicitly US/Western-anchored — but does not confirm strict US-dollar or US-customary-unit
    usage throughout. The gap in documented systematic enforcement of US conventions
    remains partial. Sources: Emergent Mind GSM8K dataset — [WEB-5]'
- id: GAP-5
  label: K-2 and early-grade arithmetic coverage
  description: GSM8K's difficulty calibration emphasizes multi-step problems; the
    paper estimates 80% solve rate would require ~10^16 parameters, indicating the
    benchmark skews toward upper-elementary difficulty and likely underrepresents
    K-2 single-step arithmetic.
  gap_type: partial
  web_search_target: 'Confirmed and sharpened. All independent sources consistently
    report that GSM8K problems require between 2 and 8 steps to solve, with the lower
    bound (2-step) described as ''direct arithmetic exercises where the challenge
    is primarily parsing the linguistic description.'' Problems are described as solvable
    by ''a bright middle school student'' and designed for ''moderate difficulty.''
    A difficulty segmentation study found approximately equal subdivisions into easy
    (<3 operations), medium (=3 operations), and hard (>3 operations) — meaning even
    the easiest third of GSM8K requires at least 2 arithmetic operations. True K-2
    single-step single-operation problems (e.g., ''5 + 3 = ?'') are absent by design.
    Sources: HuggingFace openai/gsm8k — [WEB-6];
    Emergent Mind GSM8K dataset — [WEB-5];
    Brenndoerfer GSM8K analysis — [WEB-7]'
- id: GAP-6
  label: Grade-band difficulty distribution across K-8 span
  description: 'GSM8K does not document the distribution of problems across grade-level
    difficulty bands. Whether simpler (K-2) or more advanced (grades 6-8: ratios,
    percentages, fractions) problems are proportionally represented relative to the
    platform''s usage distribution is unknown.'
  gap_type: partial
  web_search_target: 'Partially resolved. One study (Li et al., 2023, cited in Emergent
    Mind) provides a difficulty segmentation by operation count: approximately equal
    thirds split into easy (<3 operations), medium (=3 operations), and hard (>3 operations).
    This confirms a roughly uniform distribution across multi-step difficulty levels
    within GSM8K''s range, but the range itself (2–8 steps) does not cover K-2 single-step
    work. No source provides a mapping of GSM8K items to specific CCSS-M grade bands
    (K-2, 3-4, 5, 6-8). The grade-band distribution gap therefore remains partially
    unresolved at the CCSS-M granularity the platform uses. Sources: Emergent Mind
    GSM8K dataset — [WEB-5]'
infrastructure_notes:
  deployment_modality: Text-based web/mobile platform; LLM receives word problem text
    and student-submitted answer via API
  input_channel: Text string (word problem prose) submitted programmatically
  output_channel: Binary correct/incorrect label returned to platform UI
  latency_requirements: '[NEEDS VERIFICATION — deferred: below search budget; low
    impact for benchmark validity scoring — platform SLA is an operational requirement
    not affecting benchmark fitness assessment]'
  device_access_patterns: '[NEEDS VERIFICATION — deferred: below search budget; likely
    unsearchable (platform-specific operational data); low impact for benchmark validity
    scoring]'
  internet_access_assumption: Students assumed to have reliable internet access to
    use the platform; no offline-mode requirement documented
regulatory_and_privacy_notes:
  applicable_federal_law: 'COPPA (Children''s Online Privacy Protection Act) — platform
    serves children under 13. COPPA applies to for-profit operators of online services
    that direct services to children under 13 or knowingly collect personal information
    from them, following a notice-and-consent model. Source: McDermott Law EdTech
    Privacy overview — [WEB-8]'
  applicable_state_laws: 'As of 2024, more than 40 states have passed student data
    privacy laws imposing additional compliance requirements beyond federal law. California''s
    SOPIPA (Student Online Personal Information Protection Act, effective 2016) is
    the most widely copied model: it prohibits edtech companies from using K-12 student
    data for commercial purposes, targeted advertising, or profiling, and applies
    regardless of whether a formal school contract exists. At least 13 states have
    passed SOPIPA-modeled laws (Illinois SOPPA, Colorado data-deletion mandate, etc.).
    A nationwide consumer platform must track this patchwork across all states where
    it serves students. Source: StudentDPA 2024 — [WEB-9];
    McDermott Law 2024 — [WEB-8];
    Public Interest Privacy Center — [WEB-10]'
  ferpa_applicability: 'FERPA applies directly to educational institutions receiving
    federal funding, and indirectly to edtech vendors acting as ''school officials''
    under a school contract. For a direct-to-consumer platform with no school contract,
    FERPA''s school official exception does not apply and the platform is not directly
    FERPA-liable; however, if schools recommend or mandate use, the US Department
    of Education has clarified that such use must still comply with FERPA under the
    school official exception. The platform''s consumer-facing mode means COPPA and
    state student privacy laws (especially SOPIPA-type statutes) are the primary regulatory
    obligations rather than FERPA directly. Source: iKeepSafe FERPA 101 — [WEB-11];
    Student Privacy Compass PTAC letter — [WEB-12];
    McDermott Law — [WEB-8]'
  coppa_2_0_note: 'COPPA 2.0 passed the US Senate in July 2024 and would expand protections
    to cover children up to age 16 (vs. current under-13 threshold) and strengthen
    consent requirements. If enacted, it would broaden the platform''s compliance
    obligations to cover the full K-8 student age range. This is pending as of May
    2026. Source: McDermott Law EdTech Privacy overview — [WEB-8]'
  data_handling_considerations: Student age population (under 13 cohort in K-5) triggers
    heightened data protection obligations; benchmark evaluation data itself does
    not involve student PII but deployment context requires COPPA-compliant data handling
annotator_and_label_quality_notes:
  gsm8k_label_error_rate: 1.7% documented disagreement rate among contractor re-solvers;
    authors acknowledge possibly larger fraction of subtle errors
  contractor_demographics: '[NEEDS VERIFICATION — deferred: likely unsearchable (platform-specific
    internal data); Upwork and Surge AI contractor nationality, native language, and
    familiarity with US Common Core are undocumented in the GSM8K paper and no external
    source has surfaced this information]'
  ccss_m_calibration: '[NEEDS VERIFICATION — deferred: likely unsearchable (no published
    CCSS-M alignment audit of GSM8K exists); no documented assurance that GSM8K problems
    were written to CCSS-M grade-level standards; alignment is incidental rather than
    designed]'
net_new_fields:
  gsm8k_content_scope_confirmed:
    value: 'GSM8K''s confirmed mathematical content scope is: percentages, fractions,
      ratios, work rates, and basic measurement conversions — all within elementary
      arithmetic (+, −, ×, ÷). Explicitly absent: geometry (including area/perimeter),
      statistics (mean/median), quadratics, and combinatorics. This is confirmed by
      multiple independent sources and is directly relevant to the validity assessment
      for this deployment''s grades 6-8 geometry and statistics subtopics.'
    source: Emergent Mind GSM8K dataset page — [WEB-5];
      Brenndoerfer interactive GSM8K analysis — [WEB-7]
  gsm8k_difficulty_step_distribution:
    value: All GSM8K problems require 2–8 solution steps, with a difficulty segmentation
      study finding approximately equal thirds in easy (<3 operations), medium (=3),
      and hard (>3) categories. The minimum floor of 2 steps excludes true K-2 single-step
      problems by design. The benchmark was designed for 'a bright middle school student,'
      confirming the difficulty floor sits above K-2 CCSS-M level.
    source: Li et al. 2023, cited in Emergent Mind GSM8K dataset — [WEB-5];
      HuggingFace openai/gsm8k — [WEB-6]
  gsm8k_benchmark_saturation_2025:
    value: As of late 2025, leading LLMs have reached near-ceiling performance on
      GSM8K (e.g., Gemini-2.5-Pro at 95.22% on text GSM8K). This saturation means
      GSM8K is less discriminative at the high end of model capability for standard
      arithmetic tasks, but the benchmark's value for this deployment context is in
      confirming baseline competence on multi-step arithmetic — not frontier differentiation.
      Saturation does not invalidate the benchmark for its intended deployment purpose
      here.
    source: GSM8K-V paper (arXiv 2509.25160) — [WEB-4]
  gsm8k_cultural_adaptation_work:
    value: Recent work (Tomar et al., July 2025) created culturally adapted GSM8K
      variants for China, India, Japan, Korea, and pan-Africa by replacing names,
      currencies, foods, and activities while preserving identical numeric/logical
      structure. This work confirms the original GSM8K is implicitly US/Western-anchored
      (the 'default' from which other cultures are adaptations), supporting the IC
      dimension assessment that GSM8K's cultural framing aligns with US deployment
      context. However, this work does not audit whether all original problems use
      strictly US dollar/cent or US customary units.
    source: Emergent Mind GSM8K benchmark page — [WEB-5]
  ccss_m_non_adopting_states:
    value: 'Four states never adopted CCSS-M mathematics: Texas, Virginia, Alaska,
      and Nebraska. Minnesota adopted ELA only, not mathematics. Several additional
      states (Indiana, Arizona, Oklahoma, South Carolina, Florida, Idaho, New York)
      have formally withdrawn or replaced CCSS-M, though many replacements are closely
      aligned. For a nationwide platform, this means a non-trivial minority of students
      (particularly in Texas, the second-largest state by student population) are
      in states where CCSS-M is not the official standard. The platform''s CCSS-M
      alignment may create a systematic curriculum mismatch for students in non-adopting
      states, most significantly Texas.'
    source: Wikipedia Common Core implementation by state — [WEB-3];
      World Population Review Common Core States 2026 — [WEB-2];
      CCSS Initiative — [WEB-1]
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.thecorestandards.org/standards-in-your-state/ |
| WEB-2 | https://worldpopulationreview.com/state-rankings/common-core-states |
| WEB-3 | https://en.wikipedia.org/wiki/Common_Core_implementation_by_state |
| WEB-4 | https://arxiv.org/pdf/2509.25160 |
| WEB-5 | https://www.emergentmind.com/topics/gsm8k-dataset-95a37205-4213-4591-900f-09ce82d0a123 |
| WEB-6 | https://huggingface.co/datasets/openai/gsm8k |
| WEB-7 | https://mbrenndoerfer.com/writing/gsm8k-evaluating-mathematical-reasoning-language-models |
| WEB-8 | https://www.mcdermottlaw.com/insights/edtech-and-privacy-navigating-a-shifting-regulatory-landscape/ |
| WEB-9 | https://studentdpa.com/blog/understanding-ferpa-coppa-state-privacy-laws-03202025 |
| WEB-10 | https://publicinterestprivacy.org/resources/state-student-privacy/ |
| WEB-11 | https://ikeepsafe.org/content/uploads/2017/01/FERPA-101-for-EdTech-iKeepSafe.pdf |
| WEB-12 | https://studentprivacycompass.org/ptac1/ |

---

## Expert Elicitation

## Elicitation Responses
Q1 [IO]: Which operation types and complexity levels are most critical for your K-8 students, and do your word problems include Common Core-aligned topics like measurement, geometry, or data/statistics that might not appear in a general grade school benchmark?
A1: The core volume is grades 3-6: multi-step problems with four operations on multi-digit numbers, followed by fractions (grades 4-5) and decimals/percentages/ratios (grades 6-8). The platform also regularly includes US customary measurement conversion problems and basic data/statistics problems (mean/median from small datasets). Area/perimeter word problems appear frequently; formal geometry proofs do not.

Q2 [IC]: Do your platform's word problems use US-specific contexts (dollars, customary units, American settings), and would a mismatch in benchmark context affect evaluation representativeness?
A2: Yes — problems are written for US students and consistently use dollars/cents, US customary units, and American settings. Metric appears only where Common Core mandates some exposure in upper grades. A benchmark with non-US currency or heavy metric usage would be a meaningful mismatch for context fidelity, though for pure arithmetic the numerical skills being tested remain the same.

Q3 [OO]: Does your system need to evaluate only the final numerical answer, or also partial credit, intermediate steps, or written reasoning?
A3: The system performs a binary correct/incorrect check on the final numerical answer only. Intermediate steps and written reasoning are not evaluated. An unconventional solution method that yields the correct number is scored as correct.

## Dimension Priority Weights
| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | GSM8K is US-sourced grade school math and covers the core operation types well, but the user confirmed that measurement conversions, basic statistics (mean/median), and area/perimeter problems appear regularly and may be underrepresented in GSM8K's general problem set. |
| IC | MODERATE | The platform uses US dollars, US customary units, and American cultural settings consistently; GSM8K is US-primary but flagged as "transferred from different cultural context," creating a non-trivial risk that some benchmark problems carry non-US unit or currency conventions that reduce representativeness for this deployment. |
| IF | LOWER | Both the benchmark and deployment are text-only in English; no modality or script mismatch exists. |
| OO | LOWER | The deployment requires only binary correct/incorrect judgment on a final numerical answer, which aligns directly with GSM8K's answer-verification structure; no culturally variable output categories are involved. |
| OC | LOWER | Ground-truth labels are objective numerical answers to arithmetic problems; correctness is verifiable and not subject to annotator subjectivity or cultural interpretation. |
| OF | LOWER | The benchmark produces a final numerical label that maps directly onto the platform's binary answer-checking output; no format mismatch. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** openai/gsm8k (configs: `main`, `socratic`)
**Analysis date:** 2025-01-31
**Examples reviewed:** 47 (`main` train), 33 (`socratic` train) = 80 total
**Columns shown:** question, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | main | 3 | 99 | "Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats. They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." | US dollar pricing, brand-name American candy — strongly US cultural context | IC |
| D2 | main | 17 | 11 | "Linda bought two coloring books at $4 each, 4 packs of peanuts at $1.50 each pack, and one stuffed animal. She gave the cashier $25 and got no change." | USD transactions with decimal cents; cashier context | IC |
| D3 | main | 22 | 80 | "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change." | USD with tax — American retail context including sales tax | IC |
| D4 | main | 18 | 72 | "James joins a football team and becomes the star. He scores 4 touchdowns per game and each touchdown is worth 6 points. There are 15 games in the season. He also manages to score 2 point conversions 6 times during the season." | American football scoring system — distinctly US cultural setting | IC |
| D5 | main | 6 | 54 | "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" | US customary units (feet), volume calculation — matches deployment's unit system | IC, IO |
| D6 | main | 12 | 78 | "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9… the dog reached its final adult weight by adding another 30 pounds" | US customary weight (pounds) throughout | IC |
| D7 | main | 25 | 16 | "he poured into the box enough jelly beans to bring the weight to 2 pounds… he added enough brownies to cause the weight to triple… he added another 2 pounds of jelly beans" | US customary weight (pounds) used consistently | IC |
| D8 | main | 9 | 28 | "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms." | Metric weight (kilograms) — not US customary | IC |
| D9 | main | 24 | 180 | "it rained 4 inches per day during the first 15 days of November… the average daily rainfall was twice the amount observed during the first 15 days" | Rainfall in inches (US customary), no conversion required | IC |
| D10 | main | 11 | 35 | "calculate the average age of the three?" — solved as "105 years / 3 people = <<105/3=35>>35 years/person" | Mean/average calculation embedded in a word problem — statistical reasoning present | IO |
| D11 | main | 6 | 54 | "4 feet long, 6 feet wide, and 3 feet high… 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft… 72 cubic ft * 3/4 = <<72*3/4=54>>54 cubic ft" | Volume calculation using length × width × height — geometry-adjacent area/volume | IO |
| D12 | main | 35 | 333200 | "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" | Area (sq ft) applied to pricing — geometry-adjacent; uses sq ft (US customary) | IO, IC |
| D13 | main | 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | Multi-step four-operations problem across sequential days | IO |
| D14 | main | 7 | 90 | "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle. How many more days are left until all the food runs out?" | Multi-step proportional reasoning (rates/ratios) — castle setting, not US-specific | IC |
| D15 | main | 38 | 90 | "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys" | Ratio problem with non-US names; no currency denomination specified | IC |
| D16 | main | 23 | 220 | "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys" | Algebraic reasoning with US car brands — requires variable setup | IO |
| D17 | main | 4 | 21 | "The bottle of milk cost was 75% of the total cost of the sandwich and juice" — "75/100 * 12 = $<<75/100*12=9>>9" | Percentage calculation embedded in word problem | IO |
| D18 | main | 30 | 7200 | "her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples" | Multi-step percentage increase problem with monthly/annual scaling | IO |
| D19 | main | 43 | 720 | "Ariella's account earns her simple interest at the rate of 10% per annum. If Daniella has $400, how much money will Arialla have after two years?" | Simple interest calculation — financial math, USD | IO, IC |
| D20 | main | 19 | 54 | "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" | Repeated percentage growth — compound-style reasoning over years | IO |
| D21 | main | 2 | 9 | "She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes." | Fraction operations on a whole — grades 4-5 fraction content | IO |
| D22 | main | 45 | 120 | "Ten friends decide to get an end-of-year gift for their teacher… four of the group drop out. The remaining friends split the cost equally… each share is now $8 more" | Algebraic reasoning with cost-splitting | IO |
| D23 | main | 31 | 10 | "Dan owns an ice cream shop and every sixth customer gets a free ice cream cone. Cones cost $2 each. If he sold $100 worth of cones, how many free ones did he give away?" | Division with a logical twist — note: answer logic has arithmetic error in solution (50/5=10, but every 6th, not 5th) | OC |
| D24 | main | 36 | 1080 | "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest" | Multi-step chained multiplication — nature/ecology context | IO |
| D25 | main | 13 | 1825 | "If Sally makes $6 per day and Bob makes $4 per day, how much money will they both have saved for their trip after a year?" | USD daily earnings, year-long accumulation — simple interest-like structure | IC |
| D26 | main | 37 | 80 | "He has gotten 8 haircuts and knows that he needs 2 more to reach his goal. What percentage towards his goal is he?" | Percentage of goal completion — straightforward percentage | IO |
| D27 | main | 39 | 20 | "Ian won $100 in the lottery. He decided to use the money to pay off debts. He paid $20 to Colin." | USD lottery/debt context — British names (Colin, Helen, Benedict) suggest possible non-US authorship | IC |
| D28 | main | 41 | 347 | "She went to the mall and spent $250. Then, she went to the movies and watched 3 movies back to back that each cost $24. Then she stopped by the farmer's market on her way home and got 20 bags of beans at $1.25/bag." | USD across multiple retail settings; farmer's market — culturally American context | IC |
| D29 | main | 44 | 11000 | "He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value." | Large-dollar USD transactions, car-buying in American context | IC |
| D30 | socratic | 6 | 54 | "How many cubic feet are in the aquarium? ** First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" | Socratic decomposition explicitly scaffolds volume step — same problem as D11 | IO |
| D31 | main | 47 | 72 | "Larry spends half an hour twice a day walking and playing with his dog. He also spends a fifth of an hour every day feeding his dog. How many minutes does Larry spend on his dog each day?" | Unit conversion (hours to minutes) within problem — time measurement conversion | IO |
| D32 | main | 26 | 2250 | "Roberto can skip 4,200 times an hour. Valerie can skip 80 times a minute. If they jump rope for fifteen minutes straight" | Rate conversion (hours to minutes) required for solution | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Consistent USD currency throughout the dataset
- **Dimension(s):** IC
- **Observation:** The overwhelming majority of problems involving monetary amounts use US dollars and cents, including decimal-cent amounts ($1.50, $8.75, $7.22), retail tax scenarios, and large-dollar purchases. No non-US currency (£, €, AUD) was observed in any of the 80 sampled examples.
- **Deployment relevance:** The platform specifies that problems use dollars/cents; this benchmark directly matches that convention, supporting IC validity for the currency dimension.
- **Datapoint citations:**
  - [D1] Example 3 (main, train, label=99): "Her parents bought a unicorn piñata for $13… 4 bags of Reese's for $9 per bag" — USD pricing with American brand names
  - [D2] Example 17 (main, train, label=11): "Linda bought two coloring books at $4 each, 4 packs of peanuts at $1.50 each pack… She gave the cashier $25 and got no change." — USD with decimal cents and cashier transaction
  - [D3] Example 22 (main, train, label=80): "Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change." — USD with sales tax, characteristic of American retail
  - [D28] Example 41 (main, train, label=347): "She went to the mall and spent $250… 3 movies back to back that each cost $24… 20 bags of beans at $1.25/bag." — USD across multiple everyday American contexts

#### Strength 2: Strong coverage of multi-step four-operations arithmetic at grades 3-6 difficulty
- **Dimension(s):** IO
- **Observation:** The sample contains numerous problems requiring 3-6 sequential arithmetic operations across addition, subtraction, multiplication, and division on multi-digit numbers, directly matching the platform's highest-volume grade 3-6 cohort.
- **Deployment relevance:** This is the platform's core use case — the benchmark provides ample examples of the problem type the homework-checker most frequently encounters.
- **Datapoint citations:**
  - [D13] Example 1 (main, train, label=32): "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half… On Wednesday Buddy buys 12… On Thursday he buys a third of what he had on Tuesday." — four sequential steps with division, subtraction, and addition
  - [D24] Example 36 (main, train, label=1080): "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest" — chained multiplication across three steps
  - [D18] Example 30 (main, train, label=7200): "her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples… multiply the increase per month by the number of months in a year" — multi-step percentage and scaling over time

#### Strength 3: US customary units (feet, pounds, inches) present in a meaningful share of problems
- **Dimension(s):** IC
- **Observation:** Several sampled problems use US customary measurement units (feet, pounds, square feet) without any metric equivalent, confirming that at least a portion of the benchmark uses the unit system the platform requires.
- **Deployment relevance:** The platform specifies that problems use US customary units; these examples confirm partial alignment. The question is whether coverage is systematic enough (see Concern 1).
- **Datapoint citations:**
  - [D5] Example 6 (main, train, label=54): "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" — feet/cubic feet throughout
  - [D6] Example 12 (main, train, label=78): "the puppy weighed 6 pounds, but doubled in weight by week 9… adding another 30 pounds" — pounds as the only weight unit
  - [D12] Example 35 (main, train, label=333200): "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft." — square feet used naturally

#### Strength 4: Binary final-answer grading structure perfectly matches deployment output requirements
- **Dimension(s):** OO, OF
- **Observation:** Every example terminates with a clearly delimited final numerical answer (`#### N`), and intermediate computation is shown only in the `answer` field. The question field contains only the word problem. This structure maps directly to a binary correct/incorrect check on the student's submitted number.
- **Deployment relevance:** The platform does not score intermediate steps; the `#### N` convention means the benchmark's evaluation protocol matches the deployment's exact output comparison task with no adaptation needed.
- **Datapoint citations:**
  - [D13] Example 1 (main, train, label=32): "#### 32" — clean numerical delimiter
  - [D21] Example 2 (main, train, label=9): "#### 9" — fraction operations resolve to a clean integer
  - [D22] Example 45 (main, train, label=120): "#### 120" — algebraic problem terminates in final numerical answer

#### Strength 5: Fraction and percentage problems represented across the sample
- **Dimension(s):** IO
- **Observation:** The sample contains multiple problems requiring fraction arithmetic (4/5, 3/4, 1/3) and percentage calculations (30%, 50%, 75%, 80%), covering the grades 4-6 content the platform serves.
- **Deployment relevance:** These sub-skills are explicitly listed in the deployment's problem inventory; their presence in the benchmark supports evaluation coverage for these content types.
- **Datapoint citations:**
  - [D21] Example 2 (main, train, label=9): "She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes." — explicit fraction-of-a-whole operation
  - [D17] Example 4 (main, train, label=21): "The bottle of milk cost was 75% of the total cost of the sandwich and juice… 75/100 * 12 = $<<75/100*12=9>>9" — percentage as fraction applied to cost
  - [D18] Example 30 (main, train, label=7200): "her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples" — percentage increase across multiple items
  - [D26] Example 37 (main, train, label=80): "What percentage towards his goal is he? … (8 / 10) x 100 = <<(8/10)*100=80>>80" — percentage of a goal

#### Strength 6: American cultural settings dominate the sample
- **Dimension(s):** IC
- **Observation:** Problem settings are predominantly American: American football, birthday parties with brand-name US candy, shopping at malls and farmer's markets, school field trips, and babysitting. These settings match the platform's stated requirement for "culturally familiar American settings."
- **Deployment relevance:** IC alignment on cultural setting reduces construct-irrelevant variance — students encounter familiar contextual framing rather than unfamiliar cultural scenarios that might introduce reading comprehension burden beyond the math task.
- **Datapoint citations:**
  - [D4] Example 18 (main, train, label=72): "James joins a football team… He scores 4 touchdowns per game and each touchdown is worth 6 points… 2 point conversions" — American football terminology and scoring
  - [D1] Example 3 (main, train, label=99): "4 bags of Reese's… 3 bags of Snickers… 5 bags of Skittles" — US brand-name candy at a birthday party
  - [D28] Example 41 (main, train, label=347): "She went to the mall and spent $250… she stopped by the farmer's market on her way home" — mall + farmer's market are recognizable American contexts

#### Strength 7: Average/mean calculation appears as an embedded skill in the sample
- **Dimension(s):** IO
- **Observation:** At least one problem explicitly requires computing a mean (average) as the final answer, suggesting that basic statistics operations are not entirely absent from the benchmark.
- **Deployment relevance:** The platform includes mean/median problems; finding at least one mean problem in the 47-example sample is mildly positive evidence, though median problems were not observed.
- **Datapoint citations:**
  - [D10] Example 11 (main, train, label=35): "calculate the average age of the three? … 105 years / 3 people = <<105/3=35>>35 years/person" — explicit mean calculation as the primary question

#### Strength 8: Geometry-adjacent area/volume problems present
- **Dimension(s):** IO
- **Observation:** Two distinct problems in the sample require computing area or volume as a sub-step or primary goal, demonstrating that the benchmark is not entirely devoid of geometry-adjacent measurement content.
- **Deployment relevance:** The platform regularly includes area and perimeter problems. While the sample does not show perimeter problems, area/volume problems are present, partially addressing the documented gap.
- **Datapoint citations:**
  - [D11] Example 6 (main, train, label=54): "4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" — volume of a rectangular prism
  - [D12] Example 35 (main, train, label=333200): "The house is 2,400 sq ft and the barn out back is 1,000 sq ft… 2400+1000 = <<2400+1000=3400>>3,400 sq ft" — area addition applied to real estate pricing

#### Strength 9: Ratio and rate problems represented
- **Dimension(s):** IO
- **Observation:** Several problems require working with ratios, rates, or proportional reasoning, covering the grades 6-8 content listed in the deployment.
- **Deployment relevance:** Ratios/percentages are explicitly listed as part of the platform's problem inventory for upper grades; these examples confirm benchmark coverage extends to that difficulty band.
- **Datapoint citations:**
  - [D15] Example 38 (main, train, label=90): "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440…" — explicit ratio-to-quantity conversion
  - [D14] Example 7 (main, train, label=90): "The 200 people will eat 200/300 = 2/3 as much food as the original group… 60 days / (2/3) = <<60/(2/3)=90>>90 more days." — proportional rate reasoning

---

### Potential Concerns

#### CRITICAL

*(No findings at CRITICAL severity were identified in the sampled data.)*

---

#### MAJOR

#### Concern 1: Metric units appear alongside US customary units without conversion context
- **Dimension(s):** IC
- **Observation:** While many problems use US customary units (feet, pounds), at least one sampled problem uses kilograms as its sole measurement unit with no US customary equivalent provided. This creates a mixed unit environment rather than the consistently US-customary setting the platform uses.
- **Deployment relevance:** The platform states problems "consistently use… US customary units" and that metric "appears only where Common Core mandates some exposure in upper grades." A benchmark that intermixes kilograms without flagging grade-level context reduces IC alignment for the dominant use case (grades 3-6 where metric exposure is minimal).
- **Datapoint citations:**
  - [D8] Example 9 (main, train, label=28): "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms. The second person lost 7 kilograms less than the first person." — kilograms used exclusively, no US customary equivalent

#### Concern 2: No explicit measurement conversion problems (feet↔inches, cups↔gallons, pounds↔ounces) observed in 80-example sample
- **Dimension(s):** IO
- **Observation:** The deployment's highest-priority flagged gap was US customary unit conversion problems. Across 80 sampled examples, no problem required converting between US customary units (e.g., 12 inches = 1 foot, 16 ounces = 1 pound, 4 cups = 1 quart). The measurement problems observed use a single unit throughout or involve time conversions (hours↔minutes), not unit-system conversions within the US customary framework.
- **Deployment relevance:** Measurement conversion is a standard Common Core skill from grades 4-5 onward that the platform includes regularly. Its apparent absence from the sample suggests either low frequency in the full dataset or complete absence — either way, the benchmark may under-test this specific sub-skill.
- **Datapoint citations:**
  - [D31] Example 47 (main, train, label=72): "Larry spends half an hour twice a day… a fifth of an hour every day feeding his dog. How many minutes does Larry spend on his dog each day?" — time conversion (hours to minutes) but not US customary physical unit conversion
  - [D32] Example 26 (main, train, label=2250): "Roberto can skip 4,200 times an hour. Valerie can skip 80 times a minute." — rate conversion hours→minutes, not physical unit conversion (in↔ft, oz↔lb, etc.)
  - [D5] Example 6 (main, train, label=54): "4 feet long, 6 feet wide, and 3 feet high" — feet used but no conversion between feet and inches required

#### Concern 3: Basic statistics problems (mean from small datasets, median) extremely sparse; no median problem observed
- **Dimension(s):** IO
- **Observation:** Only a single mean/average calculation was found in 80 sampled examples, and it appeared as an embedded sub-skill (average age of three people), not as a standalone data/statistics word problem involving a named dataset. No problem asked students to find the median, range, or mode of a set of values, nor did any problem present a table or list of data values to summarize.
- **Deployment relevance:** The platform explicitly lists "basic data/statistics problems (mean/median from small datasets)" as a regular content type and Common Core grades 6-8 content. The near-absence of such problems in a large sample is consistent with the documented gap in the benchmark YAML and represents a meaningful coverage limitation for the upper-grade portion of the platform's student population.
- **Datapoint citations:**
  - [D10] Example 11 (main, train, label=35): "calculate the average age of the three? … 105 years / 3 people = <<105/3=35>>35 years/person" — the only mean calculation observed; embedded in an age problem, not a data-summary context

#### Concern 4: Area and perimeter problems present but perimeter-specifically absent; volume appears instead
- **Dimension(s):** IO
- **Observation:** Two geometry-adjacent problems appeared in the sample, but both involved volume or area-as-pricing rather than the perimeter calculations that are a standard K-8 Common Core skill. No problem asked students to find the perimeter of a shape or use perimeter in a word problem context.
- **Deployment relevance:** The platform "regularly includes area and perimeter word problems" as a paired skill; finding area-type problems but no perimeter problems suggests the benchmark may cover only part of this sub-domain.
- **Datapoint citations:**
  - [D11] Example 6 (main, train, label=54): "4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" — volume, not perimeter
  - [D12] Example 35 (main, train, label=333200): "2,400 sq ft… 1,000 sq ft… 2400+1000 = 3,400 sq ft" — area addition for pricing, not a geometric perimeter task

#### Concern 5: K-2 and lower-elementary single-step arithmetic absent from sample
- **Dimension(s):** IO
- **Observation:** The simplest problems in the 80-example sample still require 2-3 sequential operations and assume competence with multi-digit arithmetic. No single-operation problems (e.g., "Maria has 7 apples and gets 3 more. How many does she have?") appear in the sample, suggesting the benchmark skews toward grades 3-6 difficulty and above.
- **Deployment relevance:** The platform serves K-8, including students in grades K-2 where single-step problems are the norm. If the homework-checker is applied to early-grade submissions, GSM8K provides no test coverage for that difficulty band.
- **Datapoint citations:**
  - [D13] Example 1 (main, train, label=32): "On Monday… On Tuesday Buddy loses half… On Wednesday Buddy buys 12… On Thursday he buys a third of what he had on Tuesday." — minimum of 4 sequential operations; not accessible at K-2 difficulty
  - [D27] Example 27 (main, train, label=9): "He gave 3 to his mom, another 3 to his sister, 5 to his grandmother, and 2 to his dog. Then, he divided the remaining dandelion puffs equally among his 3 friends." — even the simpler-seeming problems require 2+ steps and division

---

#### MINOR

#### Concern 6: Occasional non-US personal names and settings suggest some non-US authorship
- **Dimension(s):** IC
- **Observation:** A small number of problems feature names that are more common in non-US English-speaking contexts (Colin, Helen, Benedict from the UK; Sab and Dane; Elsa and Amalie) and one setting ("castle provisions") that is not characteristically American. This is consistent with the benchmark YAML's note that contractor nationality was undocumented.
- **Deployment relevance:** For the platform's goal of "culturally familiar American settings," these occasional non-US-flavored problems are a minor inconsistency. The arithmetic skills tested remain equivalent, but the cultural framing may not match what students encounter on the platform.
- **Datapoint citations:**
  - [D27] Example 39 (main, train, label=20): "Ian won $100 in the lottery. He decided to use the money to pay off debts. He paid $20 to Colin… paid twice as much to Helen… paid half as much to Benedict" — British names; lottery winnings context
  - [D14] Example 7 (main, train, label=90): "There are enough provisions in a castle to feed 300 people for 90 days." — medieval castle setting, not an American school or everyday context
  - [D15] Example 38 (main, train, label=90): "The ratio of coins that Elsa has to that which Amalie has is 10:45." — Scandinavian names; "coins" without denomination specified

#### Concern 7: One solution contains a potential logical error in problem setup
- **Dimension(s):** OC
- **Observation:** Example 31 states "every sixth customer gets a free ice cream cone" but the solution divides by 5 rather than 6 to find free cones (50/5=10), suggesting either a problem statement error or an interpretation inconsistency. The ground-truth label is 10, which corresponds to the solution's arithmetic (dividing by 5), not the problem's stated rule (every 6th).
- **Deployment relevance:** This is consistent with the paper's documented 1.7% error/ambiguity rate. For a binary-correct homework-checker, a problem where the stated rule and the computed answer do not match could cause the LLM to answer differently from the ground truth — not due to reasoning failure but due to problem ambiguity. The rate is low but worth noting.
- **Datapoint citations:**
  - [D23] Example 31 (main, train, label=10): "Dan owns an ice cream shop and every sixth customer gets a free ice cream cone. Cones cost $2 each. If he sold $100 worth of cones, how many free ones did he give away? … He gave away 10 cones because 50 / 5 = <<50/5=10>>10" — problem says "sixth" but solution divides by 5

#### Concern 8: Algebra-required problems (variable setup) may exceed typical K-8 arithmetic scope
- **Dimension(s):** IO
- **Observation:** Two problems in the sample require setting up and solving a linear equation with a variable, which is more characteristic of grades 7-8 pre-algebra than the four-operations arithmetic that dominates the deployment's K-6 use case. If an LLM is evaluated primarily on arithmetic problems and these algebraic problems are present, they test a somewhat different skill.
- **Deployment relevance:** The platform's stated problem inventory is "multi-step problems with four operations… fractions, decimals/percentages/ratios." Formal variable-based algebra is not listed. These problems are valid for grades 7-8 but their presence means the benchmark includes a small proportion of problems that may not map to the platform's content standards.
- **Datapoint citations:**
  - [D16] Example 23 (main, train, label=220): "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys… Let x represent the number of Chevys… 11x+15=301… x=26" — requires symbolic variable and equation solving
  - [D22] Example 45 (main, train, label=120): "Ten friends decide to get an end-of-year gift… four of the group drop out… If each share is now $8 more, how much does the gift cost? … Let N be the original price… 10N=6(N+8)… N=12" — explicit variable equation required

---

### Content Coverage Summary

The 80 sampled examples (47 `main`, 33 `socratic`) are natural-language arithmetic word problems in American English, almost entirely set in everyday US contexts: shopping, school activities, sports (American football, recess, boxing), pets, home improvement, and financial scenarios. Currency is uniformly USD with decimal cents. US customary units (feet, pounds, square feet) appear in roughly 3-4 of 47 `main` examples; metric units appear in at least 1 example (kilograms). The difficulty range spans approximately grades 3-7: problems consistently require 2-6 sequential operations, with fractions, percentages, ratios, and proportional reasoning well represented. Formal algebra (variable-based equations) appears in 2 examples. 

The `socratic` config contains the identical problem text but with step-by-step sub-questions decomposing each solution step, which is not directly relevant to the deployment's binary answer-checking use case but could be useful for reasoning evaluation.

Key topic observations from the sample:
- **Well represented:** Four operations, fractions, percentages, ratios, time/rate calculations, USD financial math
- **Partially represented:** Area/volume (2 examples), mean/average (1 example embedded), US customary measurement usage (but not conversion)
- **Not observed:** Perimeter problems, median/mode/range statistics problems, US customary unit-to-unit conversion (inches↔feet, ounces↔pounds, cups↔quarts), decimal place value problems, K-2 single-step arithmetic

The socratic config provides the same problems with Socratic sub-question scaffolding added to answers, but questions are identical to `main`, so it does not add new content coverage.

---

### Limitations

1. **Sample size:** 47 `main` + 33 `socratic` examples represent approximately 1.1% of the full 7,473 train + 1,319 test = 8,792 examples. Rare sub-topics (e.g., measurement conversion problems that appear in 2-5% of the dataset) could be entirely absent from this sample by chance. The absence of perimeter problems or unit conversion problems in the sample does not definitively confirm their absence from the full dataset.

2. **No topic labels:** The dataset has no subtopic taxonomy or difficulty tags in its schema (`question` and `answer` only), so the sample cannot be stratified by skill type. A systematic frequency analysis of measurement conversion, statistics, or geometry problems would require processing the full dataset with keyword or semantic search.

3. **Full dataset not inspectable:** Only 80 examples were reviewed. The coverage observations (particularly for statistics, perimeter, and conversion problems) are based on the sample and should be validated against the full 8,500-problem corpus before drawing definitive conclusions.

4. **No difficulty metadata:** Grade-level difficulty cannot be formally assessed from the text alone. The characterization of K-2 absence is based on the observed minimum complexity in the sample, not a systematic difficulty annotation.

5. **Socratic config overlap:** The `socratic` config examples reviewed were identical in question text to `main` examples; no new content coverage information was gained from those 33 examples beyond confirming the step-decomposition format.

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
  "region": "US K-8 Math Tutoring Platform — Homework Checker Deployment",
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
