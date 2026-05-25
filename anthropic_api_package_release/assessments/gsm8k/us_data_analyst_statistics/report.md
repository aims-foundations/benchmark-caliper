## Deployment Context

We are a US data science consultancy evaluating whether an LLM can serve as an automated statistical analysis assistant for American data analysts. The tool will help analysts perform regression modeling, hypothesis testing, ANOVA, experimental design, and interpretation of statistical results. Users paste datasets and ask analytical questions. We need to evaluate the LLM's quantitative reasoning capabilities before deployment.

# Validity Analysis: gsm8k
**Target context:** US Professional Data Science Consultancy — Statistical Analysis Assistant
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 2 | Significant gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 2 | Significant gaps | high |
| **Average** | **1.3** | | |

> ⚠ = highest concern &nbsp; ✓ = strongest dimension

### Dimension Key

| Abbr. | Dimension | Definition |
|:-----:|-----------|------------|
| IO | Input Ontology | Whether the benchmark's test case categories cover the query types expected in deployment. |
| IC | Input Content | Whether individual datapoint content is culturally and contextually appropriate for the target region. |
| IF | Input Form | Whether the input signal encoding (text, audio, image parameters) matches deployment conditions. |
| OO | Output Ontology | Whether the benchmark's output categories and scoring criteria reflect regionally valid decision boundaries. |
| OC | Output Content | Whether ground-truth labels align with the judgments of regional stakeholders. |
| OF | Output Form | Whether the expected output modality matches regional deployment needs and accessibility. |

## Overall Summary

GSM8K is fundamentally misaligned with the US Professional Data Science Consultancy deployment across all four HIGH-priority dimensions (IO, IC, OO, OC) and substantially misaligned on the two MODERATE-priority dimensions (IF, OF). The benchmark evaluates elementary arithmetic reasoning via child-oriented narrative word problems [Q11, DATASET-D1, D3] scored by binary exact-match against single numeric answers produced by crowdworkers [Q60, Q105, DATASET-D10, D21], while the deployment requires graduate-level statistical reasoning over semi-structured professional inputs evaluated by methodological soundness with expert-statistician ground truth. Dataset analysis of 80 sampled items unambiguously confirms zero coverage of statistical reasoning categories, zero professional vocabulary, zero tabular/software-output structure, and zero multi-valid-answer scoring. The only redeeming alignments are shared English-text modality and the natural-language solution format [Q32, Q33], which prevent the lowest possible scores on IF and OF but do not address the construct gap. The web research surfaced credible candidate benchmarks (StatQA [WEB-2], StatEval [WEB-7], StatLLM [WEB-9]) that collectively address parts of the gap, but none individually replaces GSM8K for this deployment's full task profile.

## Practical Guidance

### What This Benchmark Measures

GSM8K provides evidence about an LLM's ability to perform multi-step elementary arithmetic word problems in casual English prose, including parsing narrative quantitative information, executing sequential arithmetic, and producing extended reasoning chains [Q1, Q11, Q32]. For the target deployment, this measures, at best, a precondition for numerical computation in narrow computational subtasks (e.g., 'compute degrees of freedom given supplied data') — the only deployment task category for which GSM8K has any partial relevance per the elicitation taxonomy. No HIGH-priority dimension (IO, IC, OO, OC) is meaningfully addressed by this benchmark.

### Construct Depth

GSM8K probes elementary arithmetic shallowly relative to deployment needs: maximum problem complexity in sampled items is one-variable algebra [DATASET-D9, D16] or simple interest [DATASET-D13]. No item touches distributional reasoning, inference, uncertainty quantification, model selection, or methodological pluralism. The benchmark itself acknowledges the MATH dataset is 'significantly more complex' [Q20], and even MATH has been confirmed by web research [WEB-5] to lack applied statistical categories. The construct depth for the deployment's primary tasks (regression diagnostics, ANOVA, power analysis, software output interpretation) is effectively zero.

### What Else You Need

Substantial supplementation is required across all four HIGH-priority dimensions. For IO and IC, supplement with StatQA [WEB-2] (hypothesis testing method selection, 11,623 examples) and StatEval [WEB-7] (formal statistical reasoning including regression/Bayesian, 13,817+2,374 examples). For OC and OO, supplement with StatLLM [WEB-9] (expert-annotated multi-criterion scoring for R/SAS code). For IF, the specific gap of natural-language interpretation of pre-existing R lm()/statsmodels output blocks remains unaddressed by any extant benchmark and would require a bespoke evaluation set. A hybrid evaluation suite (computational subtasks scored exact-match; methodological reasoning scored by expert-rubric) is the recommended architecture, consistent with the user's elicitation response Q3.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GSM8K's task taxonomy is restricted to elementary arithmetic word problems where 'solutions depend only on elementary concepts' [Q11], with difficulty arising from 'high diversity among problems' [Q10] rather than conceptual depth. The deployment requires an entirely different taxonomy — regression diagnostics, ANOVA, hypothesis testing under violated assumptions, power analysis, and methodological pluralism — none of which are represented in any sampled datapoint. Dataset analysis confirms zero coverage: the most 'statistically-flavored' item computes a simple arithmetic mean of three ages [DATASET-D6], and the most complex item is a one-variable linear equation [DATASET-D16]. The paper itself acknowledges the MATH dataset is 'significantly more complex' [Q20] than GSM8K, and offers only the hope — without evidence — that 'GSM8K supports the development of new methods that scale even better' [Q101]. For an IO-HIGH-priority deployment, this is a fundamental taxonomic mismatch.

**Strengths:**
- GSM8K does provide internal taxonomic structure (finetuning vs. verification methodology branches [Q27, Q30]) that, while not deployment-relevant, demonstrates methodological care in benchmark design.
- The two-config structure (main and socratic) offers reasoning decomposition formats [DATASET-D17, DATASET-D18] that could superficially serve as scaffolds for multi-step diagnostic evaluation design — though the content gap dwarfs this structural similarity.

**Checklist:**

- **IO-1**: Deployment-required categories include regression diagnostics, hypothesis testing under violated assumptions, ANOVA with post-hoc corrections, experimental design, power analysis, statistical software output interpretation, and methodological pluralism modeling choices. None overlap with GSM8K's elementary arithmetic taxonomy. — _Sources: DATASET-D6, DATASET-D4_
- **IO-2**: GSM8K's taxonomy omits ALL regionally/deployment-relevant categories. Sampled items confirm only elementary arithmetic, ratios, simple interest, percentages, and one-variable algebra [DATASET-D4, D6, D9, D13, D14, D15, D16]. No statistical inference category exists [Q11]. — _Sources: Q11, DATASET-D6, DATASET-D9, DATASET-D16_
- **IO-3**: GSM8K categories (grade school arithmetic narratives [Q1, Q8]) are not so much 'irrelevant' as taxonomically disjoint from the deployment. They do not actively introduce harmful content, but consume evaluation attention without yielding deployment-relevant signal. — _Sources: Q1, Q11_
- **IO-4**: Content validity is severely harmed: GSM8K performance carries no evidential weight about an LLM's ability to diagnose heteroscedasticity, interpret VIF, select between Welch and Student t-tests, or compute effect sizes. Candidate complementary benchmarks include StatQA [WEB-2], StatEval [WEB-7], and StatLLM [WEB-9], though none individually closes the full gap. — _Sources: Q20, Q101, WEB-2, WEB-7, WEB-9_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal.' (p.2)
- [Q10] 'State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems.' (p.2)
- [Q20] 'The MATH dataset (Hendrycks et al., 2021) is larger and significantly more complex than GSM8K' (p.4)
- [Q101] 'we hope GSM8K supports the development of new methods that scale even better.' (p.12)

*Web sources:*
- [WEB-2] StatQA (NeurIPS 2024) — 11,623 examples covering hypothesis testing method selection
- [WEB-7] StatEval (Oct 2025) — first comprehensive benchmark for formal statistical reasoning, including regression and Bayesian analysis
- [WEB-9] StatLLM — statistical analysis tasks in SAS and R with human expert evaluation

*Dataset analysis:*
- DATASET-D6: 'calculate the average age of the three' — the most 'statistical' item is arithmetic mean of three given numbers, not inference
- DATASET-D4: aquarium volume — most formula-heavy non-algebraic item, elementary geometry
- DATASET-D9: 'Jim has 4 times as many Buicks as Fords' — most complex item is system reducible to single-variable algebra
- DATASET-D16: 10N=6(N+8) — peak complexity is one-variable linear equation

</details>

**Information gaps:**
- The full test split (1,319 items) was not sampled; though the sampled 80 items uniformly confirm the elementary scope documented in the paper.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GSM8K instances are child-oriented narrative scenarios authored by Upwork/Surge AI crowdworkers [Q103, Q104] involving 'quantities of food, animals, and everyday objects' [implied across Q128-Q136]. Dataset analysis confirms every sampled item is a domestic/consumer narrative — birthday piñatas [DATASET-D3], baseball cards [DATASET-D1], cupcakes [DATASET-D2], toy cars [DATASET-D8], babysitting savings [DATASET-D7]. No item contains professional statistical vocabulary (heteroscedasticity, VIF, Type III SS), tabular data, or software output. The deployment's input distribution — CSV snippets, R lm() output, statsmodels OLS tables, jargon-dense queries — is entirely disjoint. For an IC-HIGH-priority deployment, this is a categorical content mismatch.

**Strengths:**
- GSM8K demonstrates documented quality control on input authoring: pairwise similarity scoring prevented template reuse [Q113], and contractors were instructed to be descriptive and non-repetitive [Q112].
- Inputs are 'high quality linguistically diverse' [Q1], which at least ensures lexical variety within the elementary-arithmetic domain — useful for evaluating linguistic robustness in that narrow scope.

**Checklist:**

- **IC-1**: Deployment inputs require professional statistical jargon and software-output literacy. GSM8K inputs require only everyday consumer/domestic vocabulary [DATASET-D1, D3, D7, D20]. The two distributions are lexically disjoint. — _Sources: DATASET-D1, DATASET-D3, DATASET-D7, DATASET-D20_
- **IC-2**: Not applicable in the traditional cultural sense. The mismatch is professional-register, not cross-cultural: GSM8K's child-oriented register is misaligned with the graduate-trained-analyst register, but not culturally inappropriate. — _Sources: DATASET-D3_
- **IC-3**: GSM8K does not require Western-specific cultural knowledge that would fail to transfer; the relevant gap is register and domain, not geography. Inputs use US-style consumer scenarios (dollars, baseball cards) consistent with the US deployment locale. — _Sources: DATASET-D3, DATASET-D7_
- **IC-4**: Regional annotators (practicing US statisticians) would unanimously identify GSM8K instances as outside the deployment's input distribution; no GSM8K item resembles a real consultancy query. StatQA [WEB-2] and StatLLM [WEB-9] use vocabulary closer to the deployment register, though only StatLLM uses expert annotators. — _Sources: WEB-2, WEB-9_
- **IC-5**: Content validity is severely harmed: the input distribution does not sample from the construct space (professional statistical queries) the deployment requires. Confirmed by dataset analysis — zero items contain statistical vocabulary across 80 sampled examples. — _Sources: Q1, Q9, DATASET-D2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems.' (p.1)
- [Q103] 'We initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork' (p.15)
- [Q104] 'We then worked with Surge AI (surgehq.ai), an NLP data labeling platform, to scale up our data collection.' (p.15)
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)

*Web sources:*
- [WEB-2] StatQA uses domain-specific statistical terminology by design for hypothesis testing applicability tasks
- [WEB-9] StatLLM covers R and SAS statistical code, closer to deployment vocabulary

*Dataset analysis:*
- DATASET-D3: 'unicorn piñata for $13 ... bags of Reese's ... Snickers ... Skittles' — archetypal child-oriented consumer scenario, no professional vocabulary
- DATASET-D1: baseball cards narrative — confirms domestic/recreational register
- DATASET-D7: babysitting savings — confirms casual narrative register
- DATASET-D20: 'Each bird eats 12 beetles per day, each snake eats 3 birds per day' — ecological chain, entirely non-statistical
- DATASET-D2: cupcakes and classmates — school-lunch scenario, no quantitative professional register

</details>

**Information gaps:**
- Annotator demographics, native languages, and statistical training of Upwork/Surge contractors are not documented in the paper.

---

### Input Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Both GSM8K and the deployment are English text-only [Q32, DATASET-D1], which limits the worst-case form-level mismatch and was noted as a strength in dataset analysis. However, GSM8K's inputs are continuous narrative prose with quantitative information embedded in sentences [DATASET-D3, D5, D15], while the deployment requires parsing semi-structured content: CSV snippets, R lm() coefficient tables, statsmodels OLS output blocks, and correlation matrices. Dataset analysis confirms no sampled item contains tabular structure, column headers, or software-output formatting conventions. The benchmark-internal <<...>> calculator annotations [Q40, Q119, DATASET-D10, D14] are auto-generated training artifacts with no deployment analogue. For an IF-MODERATE-priority deployment, the shared text-English modality prevents a score of 1, but the semi-structured-input gap is substantial.

**Strengths:**
- Modality and language alignment: both benchmark and deployment are English plain text [Q32, DATASET-D1], eliminating script, language, or media mismatch as sources of construct-irrelevant variance.
- Two-config structure offers reasoning-decomposition flexibility (main prose vs. socratic sub-question scaffolding) [DATASET-D17, D18], providing some adaptability for evaluation design.

**Checklist:**

- **IF-1**: Signal distributions partially align (English text), but diverge on structural form: GSM8K is continuous narrative prose [DATASET-D3]; deployment requires semi-structured/tabular inputs (R lm() output, CSV previews, statsmodels tables). — _Sources: Q32, DATASET-D5, DATASET-D15_
- **IF-2**: Regional infrastructure (US professional consultancy with broadband and desktop workstations) fully supports both text-input modalities. Not a limiting factor. — _Sources: DATASET-D1_
- **IF-3**: Domain-specific form differences are substantial: deployment inputs include software output blocks and tabular previews with specific formatting conventions (e.g., 'Coefficients: Estimate Std. Error t value Pr(>|t|)') entirely absent from GSM8K's narrative-prose distribution [DATASET-D5, D15]. — _Sources: DATASET-D3, DATASET-D15_
- **IF-4**: External validity is harmed for semi-structured inputs. Models tuned on GSM8K's prose distribution have not been evaluated on parsing software-output formats. DS-1000 [WEB-4] and StatQA [WEB-2] offer partial coverage of structured input forms, but no benchmark specifically tests interpretation of pre-existing R/statsmodels output blocks. — _Sources: Q9, WEB-4, WEB-2, DATASET-D10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q32] 'we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions.' (p.5)
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q40] 'we train all models to use a calculator by injecting calculation annotations into the training set.' (p.6)
- [Q119] 'During training, there is no special distinction between the annotated tokens and the rest of the solution: they are all just tokens.' (p.17)

*Web sources:*
- [WEB-4] DS-1000 uses realistic Python data science contexts including structured data
- [WEB-2] StatQA uses tabular data as input context for hypothesis testing tasks

*Dataset analysis:*
- DATASET-D1: English plain-text narrative — confirms modality alignment with deployment
- DATASET-D5: 'enough provisions in a castle to feed 300 people for 90 days' — quantitative info embedded in prose, not tabular
- DATASET-D15: ratio '10:45' given in prose, not as a table or data structure
- DATASET-D10: <<30/2=15>> calculator annotations embedded in every answer — benchmark-internal artifact with no deployment analogue

</details>

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GSM8K's output ontology is binary exact-match against a single numeric answer: 'Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer' [Q60]. Dataset analysis confirms every sampled item ends with '#### {single number}' [DATASET-D10, D12, D21, D23], with no concept of partial credit or methodological pluralism. The paper itself documents structural limitations: 'some solutions will reach the correct final answer using flawed reasoning, leading to false positives' [Q61], with visualized examples of both false negatives (correct reasoning marked wrong [Q153]) and false positives (wrong reasoning reaching right answer [Q154, Q155]). The deployment explicitly requires evaluation that rewards methodologically defensible reasoning even when final numbers differ (regression covariate selection, log-transformation choices, fixed vs. random effects). For an OO-HIGH-priority deployment, binary exact-match is structurally incompatible.

**Strengths:**
- The verifier output ontology is internally well-designed: 'Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct' [Q59], with the token-level verifier acting as 'a token-level value function' [Q74] — providing some scalar reasoning-quality signal beyond pure final-answer matching.
- The paper transparently documents failure modes of binary scoring (false positives and false negatives [Q61, Q153, Q154, Q155]), demonstrating awareness of the limits of exact-match correctness.

**Checklist:**

- **OO-1**: GSM8K's output labels are binary correct/incorrect against single numeric answers [Q60, DATASET-D10, D12]. The deployment requires multi-criterion rubric evaluation (methodological soundness, alternative valid pathways) — no overlap with GSM8K's output category structure. — _Sources: Q60, DATASET-D10, DATASET-D12_
- **OO-2**: Missing from GSM8K's taxonomy: partial credit, multi-valid-answer scoring, rubric-based methodological soundness, qualitative diagnostic quality. The deployment requires all of these. StatLLM's multi-criterion expert scoring (correctness, effectiveness, readability, executability, output accuracy) [WEB-9] is directionally closer. — _Sources: Q60, WEB-9_
- **OO-3**: GSM8K's binary exact-match does not encode non-regional values per se; it encodes an arithmetic-domain assumption (single correct answer exists) that does not hold in applied statistics where methodological pluralism is structurally unavoidable. — _Sources: Q60_
- **OO-4**: Stakeholder-driven taxonomy redesign is essentially required: the deployment needs a hybrid scoring regime (exact-match for narrow computational subtasks, rubric for open-ended methodological reasoning), and GSM8K's output ontology cannot be patched to accommodate this. — _Sources: WEB-9, WEB-7_
- **OO-5**: Structural validity is severely violated: GSM8K's output ontology cannot represent the construct (methodologically-defensible statistical reasoning) the deployment requires. Content validity also harmed: legitimate alternative-pathway answers would be marked incorrect. — _Sources: Q61, DATASET-D21, DATASET-D23_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q60] 'Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer.' (p.7)
- [Q61] 'In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives.' (p.7)
- [Q31] 'Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer.' (p.5)
- [Q59] 'Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct.' (p.7)

*Web sources:*
- [WEB-9] StatLLM uses multi-criterion human expert scoring (correctness, effectiveness, readability, executability, output accuracy)
- [WEB-7] StatEval proposes evaluation framework tailored to both computational and proof-based tasks

*Dataset analysis:*
- DATASET-D10: '#### 32' — single numeric label, no ambiguity, demonstrates binary scoring structure
- DATASET-D12: algebraic system with single answer '#### 220' — no multi-valid pathway possible
- DATASET-D21: 'Caleb spent ... $36 more on ice cream #### 36' — deterministic answer, no methodological choice
- DATASET-D23: '#### 2290' — multi-step arithmetic but single deterministic ground truth

</details>

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GSM8K ground-truth labels were produced by Upwork/Surge AI contractors who re-solved problems and were checked for final-answer agreement [Q105, Q106], with a residual 1.7% disagreement rate [Q107] and acknowledgment that 'a larger percentage of problems contain subtle errors' [Q109]. Annotator demographics, statistical training, and educational backgrounds are NOT documented. Dataset analysis confirms ground-truth labels are single deterministic numerics [DATASET-D21, D22, D23] verifiable by anyone capable of basic arithmetic — no statistical expertise was required or present. The deployment explicitly requires ground truths reflecting expert statistical judgment with legitimate pluralism (e.g., adjudicating 'VIF threshold of 5 vs. 10', 'log-transformation given this skewness'). For an OC-HIGH-priority deployment, this annotator population is categorically unrepresentative. StatLLM [WEB-9] is the only confirmed statistical-domain benchmark using expert annotators.

**Strengths:**
- Documented quality control process: re-solving by independent contractors [Q105], disagreement-triggered repair/discard [Q106], and a second round of agreement checks measuring residual disagreement [Q107] — represents transparent annotation methodology even though the expertise level is unsuitable for the deployment.
- Honest acknowledgment of annotation limitations: the paper notes 'a larger percentage of problems contain subtle errors' [Q109] and visualizes verifier failure modes [Q153, Q154, Q155] — demonstrates documentation transparency.

**Checklist:**

- **OC-1**: Ground truth labels reflect crowdworker-level arithmetic correctness judgments, not practicing-statistician methodological judgments. For the deployment domain, labels would fail to reflect expert stakeholder perspectives on questions like assumption-violation diagnosis or modeling-choice adjudication. — _Sources: Q105, Q106, DATASET-D21_
- **OC-2**: Significant disagreement would arise if regional experts (practicing US statisticians) were asked to re-annotate deployment-relevant content — but this is moot because GSM8K instances are not deployment-relevant content. The expertise mismatch is categorical: crowdworker arithmetic vs. expert statistical adjudication. — _Sources: Q105, DATASET-D22_
- **OC-3**: INSUFFICIENT DOCUMENTATION — the paper does not report annotator demographics, educational backgrounds, native languages, geographic locations, or whether contractors had mathematical training beyond grade-school level. A Datasheet entry covering these would be required to fully assess representativeness.
- **OC-4**: Re-annotation by representative regional annotators (practicing statisticians) is not feasible because the underlying instances are out-of-domain for the deployment. A new dataset is required rather than re-annotation. StatLLM [WEB-9] provides the only confirmed expert-annotated statistical benchmark exemplar. — _Sources: WEB-9_
- **OC-5**: Aggregation method (final-answer agreement check [Q106]) erases reasoning-quality variation entirely: solutions reaching the correct answer with flawed reasoning are labeled correct [Q61, Q154, Q155]. For the deployment domain, this would erase precisely the methodological-soundness signal that matters. — _Sources: Q106, Q61, DATASET-D23_
- **OC-6**: Convergent validity severely violated: labels do not correlate with expert-statistician judgments on the construct (methodological soundness). External validity violated: arithmetic-correctness judgments do not generalize to applied statistical adjudication. — _Sources: Q109, Q61_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q105] 'After collecting the full dataset, we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote.' (p.15)
- [Q106] 'We checked whether their final answers agreed with the original solutions, and any problems that produced disagreements were either repaired or discarded.' (p.15)
- [Q107] '1.7% of problems still produce disagreements among contractors.' (p.15)
- [Q109] 'It is possible that a larger percentage of problems contain subtle errors.' (p.15)
- [Q61] 'some solutions will reach the correct final answer using flawed reasoning, leading to false positives.' (p.7)

*Web sources:*
- [WEB-9] StatLLM uses human expert evaluation for statistical code — only confirmed expert-annotated statistical benchmark
- [WEB-14] ASA Ethical Guidelines update expected early 2027 — no current AI-specific professional standards

*Dataset analysis:*
- DATASET-D21: '#### 36' — ground truth verifiable by elementary arithmetic, no statistical expertise required
- DATASET-D22: '7 robots * $8.75 ... #### 80' — decimal arithmetic verifiable without domain expertise
- DATASET-D23: '$960 + $931 + $399 = 2290 #### 2290' — multi-step arithmetic, no expert adjudication needed

</details>

**Information gaps:**
- Annotator demographics, educational backgrounds, native languages, and statistical training are not documented in the paper.
- No formal inter-annotator agreement statistic (e.g., Cohen's kappa) is reported — only a final-answer disagreement rate.

**Requires expert verification:**
- Whether the forthcoming 2027 ASA Ethical Guidelines update [WEB-14] will impose specific expert-annotation requirements for LLM-assisted statistical analysis evaluations.

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Both benchmark and deployment use English text output, limiting the worst-case form-level mismatch. GSM8K outputs are step-by-step natural language prose solutions [Q32, Q33, DATASET-D11, D14] terminating in a single numeric answer ('#### {number}') [DATASET-D10, D12, D21]. The step-by-step prose format has surface-level resemblance to the diagnostic narratives the deployment requires, and the socratic config [DATASET-D17, D18] adds explicit sub-question decomposition. However, the primary evaluation signal is exact-match against the terminal numeric answer at low temperature ('test@1' [Q29, Q46]) or best-of-N sampling [Q52], not the prose quality. The deployment requires open-ended methodological recommendations, diagnostic narratives, and software-output interpretations as the substantive output — not numeric finality. The token-level verifier visualization [Q147, Q148] demonstrates some capacity for reasoning-chain assessment, but remains anchored to binary numeric correctness. For an OF-MODERATE-priority deployment, the shared text modality prevents a score of 1, but the terse-numeric vs. open-ended-narrative mismatch is substantial.

**Strengths:**
- Natural-language solution format [Q32, Q33] enables models to 'develop verbal analytical skills and to produce solutions that are more readily interpretable by humans' [Q33] — a surface-level alignment with deployment's narrative-output requirement, even though the underlying scoring remains numeric.
- Step-by-step prose chains with intermediate-step narration [DATASET-D11, D14] demonstrate extended reasoning-chain output rather than lookup-style answers, providing weak structural similarity to deployment diagnostic chains.
- Token-level verifier provides per-token scoring visualization [Q147, Q148, Q149] — methodologically demonstrates that fine-grained reasoning-quality signals are possible, even if not primary in GSM8K scoring.
- Socratic config [DATASET-D17, D18] offers explicit sub-question scaffolding that loosely maps onto multi-step diagnostic structure.

**Checklist:**

- **OF-1**: Output modality (English text) matches deployment needs. However, the output register (terse numeric finality after prose chain) does not match the deployment's open-ended methodological-recommendation register [Q29, Q46, DATASET-D10]. — _Sources: Q29, DATASET-D10_
- **OF-2**: Not applicable — deployment is text-based; text-to-speech is not required.
- **OF-3**: Not applicable — deployment population is quantitatively trained professionals with high English literacy; accessibility requirements are not flagged.
- **OF-4**: External validity moderately harmed: GSM8K rewards terse numeric answers [Q29, Q46, Q52], whereas deployment requires open-ended diagnostic narratives. The natural-language solution format [Q32] partially aligns, but the scoring rubric does not. The drastic performance drop when models output direct answers without intermediate steps [Q57] suggests GSM8K does train extended-output behavior, mitigating some mismatch. — _Sources: Q29, Q32, Q52, Q57, WEB-9_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'At test time, we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct.' (p.5)
- [Q32] 'we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions.' (p.5)
- [Q33] 'this choice enables our models to develop verbal analytical skills and to produce solutions that are more readily interpretable by humans.' (p.5)
- [Q57] 'If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%.' (p.7)
- [Q147] 'One benefit of the token-level verifiers is that these models become immediately interpretable' (p.21)

*Web sources:*
- [WEB-9] StatLLM evaluates statistical code outputs with multi-criterion expert scoring — closer to deployment's open-ended-output evaluation needs

*Dataset analysis:*
- DATASET-D10: prose solution terminating in '#### 32' — extended reasoning chain anchored to single numeric finality
- DATASET-D11: 'First calculate the volume of the aquarium...' — multi-step prose narration before single answer
- DATASET-D14: six narrated arithmetic steps before '#### 7200' — confirms extended-output format
- DATASET-D17: socratic sub-question scaffolding format with explicit reasoning labels

</details>

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Zero coverage of deployment-required statistical reasoning categories (regression diagnostics, ANOVA, hypothesis testing under violated assumptions, power analysis, model selection under methodological pluralism).

**Recommendation:** Do not rely on GSM8K for statistical reasoning evaluation. Supplement with StatQA [WEB-2] for hypothesis testing method selection and StatEval [WEB-7] for formal statistical inference. Commission a bespoke evaluation set for applied consulting tasks (regression diagnostics + ANOVA post-hoc + power analysis) since no extant benchmark fully covers this combination.

### Input Content ⚠

**Gap:** GSM8K instances contain zero professional statistical vocabulary and no software output or tabular content; vocabulary is entirely child-oriented narrative.

**Recommendation:** Build a deployment-specific evaluation corpus using realistic CSV snippets, R lm()/anova() output blocks, and Python statsmodels OLS tables, paired with analyst-style queries containing target vocabulary (heteroscedasticity, VIF, Type III SS, Cook's distance, random effects). Use StatLLM [WEB-9] as a reference for vocabulary-rich expert-annotated examples.

### Output Ontology ⚠

**Gap:** Binary exact-match against single numeric answers is structurally incompatible with deployment's multi-valid-answer methodological-pluralism requirement.

**Recommendation:** Adopt a hybrid scoring regime as proposed in the elicitation: exact-match numeric correctness for narrow computational subtasks (test statistic computation, degrees of freedom), and rubric-based expert scoring (correctness, methodological soundness, alternative-pathway acceptability) for open-ended diagnostic tasks. Model the rubric on StatLLM's multi-criterion expert scoring [WEB-9].

### Output Content ⚠

**Gap:** Ground-truth labels were produced by crowdworkers verifying arithmetic; deployment requires practicing-statistician adjudication of methodological choices. Annotator demographics not documented.

**Recommendation:** Recruit practicing applied statisticians or quantitatively trained PhDs as annotators for deployment-specific evaluation sets. Use a panel of ≥3 expert annotators per item with documented IAA (e.g., Krippendorff's alpha) on methodological-soundness ratings. Follow StatLLM's expert-evaluation precedent [WEB-9].

### Input Form

**Gap:** GSM8K is continuous narrative prose only; no benchmark exists (per WEB research) that specifically tests natural-language interpretation of pre-existing R/statsmodels output blocks.

**Recommendation:** Construct a custom evaluation set with paired (software-output block, analyst query, expert-annotated diagnostic narrative) triplets. Draw on DS-1000 [WEB-4] and DSCodeBench [WEB-11] for realistic structured-input formats, even though their primary task is code generation rather than output interpretation.

### Output Form

**Gap:** GSM8K rewards terse numeric finality; deployment requires open-ended diagnostic narratives and methodological recommendations.

**Recommendation:** Define output-form requirements for deployment evaluation as structured recommendations (diagnosis + reasoning + alternative-pathway disclosure + interpretation) rather than terminal numeric answers. Use rubric items that explicitly reward open-ended recommendation quality. Monitor for the forthcoming ASA Ethical Guidelines update [WEB-14] in 2027, which may add professional-standard constraints on AI-assisted recommendation outputs.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems." |
| Q2 | 1 | input_ontology | "To increase performance, we propose training verifiers to judge the correctness of model completions." |
| Q3 | 1 | output_form | "At test time, we generate many candidate solutions and select the one ranked highest by the verifier." |
| Q4 | 1 | output_form | "We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline." |
| Q5 | 1 | output_ontology | "One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes (Shen et al., 2021a)." |
| Q6 | 1 | output_ontology | "When generating a solution, autoregressive models have no mechanism to correct their own errors." |
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
| Q34 | 5 | input_ontology | "Finally, we use separate generator and verifier networks, in order to prevent the generator from overfitting." |
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
| Q48 | 6 | output_ontology | "Assuming a log-linear trend, we can naively extrapolate these results to estimate that a model with 10^16 parameters would be required to reach an 80% solve rate, when using the full GSM8K training set." |
| Q49 | 6 | output_form | "It is even harder to extrapolate along the data dimension, since performance does not appear to follow a log-linear trend." |
| Q50 | 6 | input_content | "Nevertheless, it appears likely that the 175B model would require at least two additional orders of magnitude of training data to reach an 80% solve rate." |
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
| Q61 | 7 | output_ontology | "In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives." |
| Q62 | 8 | input_form | "As shown in Figure 4, we train the verifier as follows: 1. Finetune a model (the "generator") for 2 epochs on the training set. 2. Sample 100 completions from the generator for each training problem and label each solution as correct or incorrect. 3. Train a verifier for a single epoch on this dataset." |
| Q63 | 8 | input_ontology | "Training for 2 epochs is enough for the generator to learn basic skills in this domain." |
| Q64 | 8 | output_ontology | "We choose not to train for longer, since the diversity of generated solutions begins to collapse after this point, as shown in Figure 3." |
| Q65 | 8 | input_form | "We train separate generator and verifier models to limit the generator's training and prevent overfitting, but in principle, it should be possible to combine these models." |
| Q66 | 8 | input_form | "Unless otherwise specified, we use the same model size for the generator and the verifier." |
| Q67 | 8 | output_ontology | "In addition to predicting solution correctness, we also train the verifier with the same language modeling objective as the generator." |
| Q68 | 8 | output_form | "At test time, we sample 100 completions to each test problem, rank them with the verifier, and then return the one with the highest verifier score." |
| Q69 | 8 | output_form | "We find that it is not beneficial to use verification at low dataset sizes." |
| Q70 | 8 | output_content | "We believe this is due to the pressure to overfit to the correct answer: with small datasets, overfitting to the correct answer happens faster than learning more generalizable properties of correct reasoning." |
| Q71 | 8 | output_form | "However, once we use a sufficiently large dataset, we see a strong boost from verifiers." |
| Q72 | 9 | input_ontology | "We can either train verifiers to make a single scalar prediction conditioned on the entire generated solution, or to make a scalar prediction after each token in the solution." |
| Q73 | 9 | input_ontology | "By default, we choose the latter, training verifiers to make predictions after each token." |
| Q74 | 9 | input_ontology | "This can be viewed as a token-level value function." |
| Q75 | 9 | output_ontology | "Predicting the value function at every token is a more challenging and noisier task than judging only the full completion." |
| Q76 | 9 | output_form | "However, despite the initially slower training, the token-level verifier ultimately outperforms the solution-level verifier." |
| Q77 | 9 | output_form | "Moreover, the token-level verifier is still improving late in training, whereas the solution-level verifier quickly shows signs of overfitting." |
| Q78 | 9 | input_ontology | "We hypothesize that the full value function provides a useful auxiliary signal that encourages the model to judge the reasoning throughout solutions, rather than merely memorizing the correct final answer." |
| Q79 | 9 | input_ontology | "As discussed in Section 4.2, we can optionally include a language modeling objective alongside the verification objective." |
| Q80 | 9 | output_form | "Although both are reasonable choices, including the language modeling objective is a strict improvement." |
| Q81 | 10 | output_form | "At test time, we can choose to generate arbitrarily many solutions to be judged by the verifier before selecting the highest ranked completion." |
| Q82 | 10 | output_form | "At this scale, performance improves as we increase the number of completions up to 400." |
| Q83 | 10 | output_ontology | "Beyond this point, performance start to decrease. This suggests that the benefits of search are eventually outweighed by the risk of finding adversarial solutions that fool the verifier." |
| Q84 | 10 | output_form | "In general, we evaluate verifier test performance using 100 completions, since this captures most of the benefits of verification with a relatively modest compute cost." |
| Q85 | 10 | output_form | "To further increase performance, we can take a majority vote among the top verifier-ranked solutions instead of selecting only the single top solution." |
| Q86 | 10 | output_ontology | "This suggests that the verifier may often be relying on relatively coarse heuristics to discriminate between solutions from a given generator, rather than attempting a more thorough form of verification." |
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
| Q111 | 15 | output_content | "Contractors were allowed to use those seed questions directly, to use them as inspiration and make modifications, or to come up with their own questions entirely." |
| Q112 | 15 | output_content | "We instructed contractors to be as descriptive as possible in their solutions, and to not re-use problem settings or templates between different questions." |
| Q113 | 15 | input_form | "To ensure contractors were not re-using problem templates, we computed pairwise similarity scores between problems and used this to provide feedback to contractors." |
| Q114 | 16 | output_form | "We performed sweeps of the learning rate and batch size by an order of magnitude in both directions from the values in the table and were unable to find any significant improvements." |
| Q115 | 16 | output_form | "Other reasonable choices for both the verifier temperature (eg: 1.0 instead of 0.7) and objective (cross-entropy instead of mean squared error) also had negligible effect in our ablations." |
| Q116 | 16 | output_form | "Hyperparameters used for all experiments, unless explicitly said otherwise. Notable exceptions include Figure 8c, which uses 4x more tokens per batch and 300 completions at both training and test time. All dropout experiments in Figure 8 use 20% dropout. Figure 7a uses verifiers trained on 100 completions, but searching over more completions at test time." |
| Q117 | 17 | output_content | "The calculator annotations were not provided by human contractors: they were generated by a combination of hard-coded logic and a finetuned language model." |
| Q118 | 17 | output_content | "The logic for auto-generating calculator annotations is imperfect. It is highly unlikely to generate any incorrect annotations, but it is not uncommon for it to ignore some lines that could be annotated." |
| Q119 | 17 | input_form | "During training, there is no special distinction between the annotated tokens and the rest of the solution: they are all just tokens." |
| Q120 | 17 | output_form | "During testing, we override model sampling when a well-formatted annotation exists, specifically overwriting the token(s) directly following "=" and within <<. . . >>." |
| Q121 | 17 | output_form | "To simulate the calculator, we simply use the python eval function to evaluate the tokens in the expression (Figure 9)." |
| Q122 | 17 | output_form | "Evaluations that time out or throw an error result in the annotations being skipped and the model being sampled from as usual." |
| Q123 | 17 | output_form | "We note that the original version of our calculator, used for all results in this paper, had some minor implementation bugs." |
| Q124 | 17 | output_form | "Our reported test performance is therefore a slight underestimate, though the magnitude of this discrepancy is less than 1% in most experiments." |
| Q125 | 17 | output_form | "Fixing the calculator improves verification test performance by about 1% when using the full GSM8K training set." |
| Q126 | 18 | input_ontology | "We showcase a handful of samples comparing finetuning and verification at both 6B and 175B scale." |
| Q127 | 18 | output_content | "Samples were slightly cherry-picked for diversity." |
| Q128 | 19 | input_content | "The meat and context books weigh 2 pounds each, the French book weighs 3 pounds and the English book weighs 1 pound, and the total weight book sit in is for English task, if today is a nice day, what is the total weight of all the books?" |
| Q129 | 19 | output_ontology | "The meat and context books weigh 2 pounds each so they weigh 2*2 = 4=2=6=8 pounds together, the French book weighs 3 pounds and so the total weight of the English book is 6+3 = 10, so if you add up all of the books together, the total weight is 4+3+4 = 11" |
| Q130 | 19 | output_ontology | "Our generated responses weigh books weigh 2 pounds each to a total of 2*2 = or2=4 pounds, use French book weigh 4 pounds and the English book weighs 3 pounds, to a total of 4+3 = or4+3=7 pounds, if so if you add up all of the books, the total weight of the English book, to a total of 3+3 = or2=4=8 pounds" |
| Q131 | 19 | output_ontology | "The English book weight 3 pounds, So all of our books weigh 2 + 4 + 3 = 9=10 =9=10=9=10 pounds." |
| Q132 | 19 | output_ontology | "The total weight of books read at science books is 2*2=or2=4=6=8 pounds total weight of all the books is 4+3=or2=4+3=7 pounds." |
| Q133 | 19 | input_content | "The German Shepherd dog contains 1.5 + = or1+1=1.5=1 diggrams of dog food per day the dog also contains 2.5 +3=or2=5.5 diggrams of dog food per day, During a week, the total is 2.5 + or2+1=3=1+1.5=1 diggrams of dog food is a week." |
| Q134 | 19 | input_content | "Our data 1000=or1=1.5=1.5 diggrams per day for the German Shepherd, if the dog weighs 3.2 + or3+1.7=or3=1.9=1.5 diggrams of dog food per week." |
| Q135 | 19 | input_content | "The German Shepherd's total consumption is 1.5 + =or1=1.5=1.5 diggrams, the dog also and consumption total food per meal is 3.2 + = or3=2.5=1.5=1.5 diggrams." |
| Q136 | 19 | input_content | "The 2 German Shepherd dogs consumes 1.5 + =or1+1=1.5=1.5 diggrams of food per day, the 2 bulldogs consumes 2.3 + =or2=2.5=2.5=1.5 diggrams of food per day." |
| Q137 | 20 | output_ontology | "As noted in section 4.2, we train verifiers with a joint objective where the model learns to label a model completion as correct or incorrect, in addition to the original language modeling objective." |
| Q138 | 20 | input_form | "Architecturally, this means our verifiers are language models, with a small scalar head that outputs predictions on a per-token basis." |
| Q139 | 20 | input_form | "We implement this scalar head as a single bias parameter and single gain parameter that operate on the logits outputted by the language model's final unembedding layer." |
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

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://github.com/HKUSTDial/StatQA |
| WEB-2 | https://arxiv.org/abs/2406.07815 |
| WEB-3 | https://ds1000-code-gen.github.io/ |
| WEB-4 | https://arxiv.org/abs/2211.11501 |
| WEB-5 | https://arxiv.org/abs/2103.03874 |
| WEB-6 | https://github.com/hendrycks/math |
| WEB-7 | https://arxiv.org/abs/2510.09517 |
| WEB-8 | https://stateval.github.io/ |
| WEB-9 | https://www.nature.com/articles/s41597-026-06731-4 |
| WEB-10 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12987956/ |
| WEB-11 | https://www.arxiv.org/abs/2505.15621 |
| WEB-12 | https://www.dlapiperdataprotection.com/?c=US |
| WEB-13 | https://www.shumaker.com/insight/the-patchwork-of-data-privacy-laws-recent-developments-and-implications/ |
| WEB-14 | https://magazine.amstat.org/blog/2025/10/01/apertus-llm-data-for-good/ |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** openai/gsm8k (configs: `main`, `socratic`)
**Analysis date:** 2025-01-31
**Examples reviewed:** 47 from `main` train split; 33 from `socratic` train split (80 total)
**Columns shown:** question, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | main | 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them." | Child-oriented narrative word problem; elementary subtraction/division | IC |
| D2 | main | 2 | 9 | "Anna baked 60 cupcakes. She gives away 4/5 of the cupcakes to her classmates." | Fraction arithmetic in child scenario; no statistical content | IC, IO |
| D3 | main | 3 | 99 | "It's Ava's birthday party. Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats." | Consumer arithmetic in child party scenario | IC |
| D4 | main | 6 | 54 | "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" | Volume calculation; most complex formula seen — elementary geometry | IO |
| D5 | main | 7 | 90 | "There are enough provisions in a castle to feed 300 people for 90 days." | Rate/proportion reasoning; no statistical concepts | IO |
| D6 | main | 11 | 35 | "Omi is twice as old as Kimiko. Arlette is 3/4 times as old as Kimiko. If Kimiko is 28 years old, calculate the average age of the three?" | Simple mean calculation; bears no resemblance to statistical inference | IO |
| D7 | main | 13 | 1825 | "Sally and Bob have made plans to go on a trip at the end of the year. They both decide to work as babysitters and save half of what they've earned for their trip." | Savings arithmetic over 365 days; no variance, distribution, or inference | IC |
| D8 | main | 19 | 54 | "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" | Compound growth arithmetic; not exponential modeling or regression | IO |
| D9 | main | 23 | 220 | "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys. How many Buicks does Jim have?" | Algebraic system of equations — most complex problem type seen | IO |
| D10 | main | 1 | 32 | "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. … On Thursday Buddy has a total of 27+5 = <<27+5=32>>32 baseball cards. #### 32" | Step-by-step natural language solution with embedded calculator annotations; single numeric final answer | OO, OF |
| D11 | main | 6 | 54 | "First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft … #### 54" | Multi-step prose solution; most elaborate reasoning chain in sample — still binary-scored against single number | OO |
| D12 | main | 23 | 220 | "Let x represent the number of Chevys … 11x+15=301 … x=<<26=26>>26 … Buicks:12+8(26)=220 #### 220" | Algebraic solution with variable definition; single deterministic answer | OO |
| D13 | main | 43 | 720 | "If Ariella has $200 more in her son's saving account than Daniella has, then she has $400 + $200 = $600 … The total amount of money in Ariella's account after two years is $600 + $120 = $720 #### 720" | Simple interest calculation; closest to finance/quantitative domain but still elementary | IO, IC |
| D14 | main | 30 | 7200 | "First find the increase in rent by multiplying last year's rent by 30%: $1000 * .3 = $<<1000*.3=300>>300 … $600/month * 12 months/year = $<<600*12=7200>>7200/year #### 7200" | Percentage change and annualization; no statistical inference content | IO |
| D15 | main | 38 | 90 | "The total ratio of the coins they both have is 10+45 = <<10+45=55>>55 … Amalie has 45/55*440 = <<45/55*440=360>>360 coins." | Ratio arithmetic; no correlation, regression, or distributional reasoning | IO |
| D16 | main | 45 | 120 | "Let N be the original price each friend was going to pay. 10N=6(N+8) … 4N=48 … N=<<12=12>>12 … 10*12=<<10*12=120>>120 #### 120" | Linear equation solving; deterministic single answer | IO, OO |
| D17 | socratic | 1 | 32 | "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards." | Socratic sub-question format scaffolding the same arithmetic problem | IF, OF |
| D18 | socratic | 23 | 220 | "Define a variable ** Let x represent the number of Chevys … Combine like terms ** 11x+15=301 … Divide by 11 ** x=<<26=26>>26" | Explicit reasoning step labels in Socratic config; structural difference from main config | IF |
| D19 | main | 4 | 21 | "The juice was two times more expensive than the sandwich, so it was 4 * 2 = $<<2*4=8>>8. … So the cost of one bottle of milk was 75/100 * 12 = $<<75/100*12=9>>9." | Percentage and ratio arithmetic; grocery purchase scenario | IC |
| D20 | main | 36 | 1080 | "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest, how many beetles are eaten each day?" | Chained multiplication; ecological scenario — no statistical modeling | IC, IO |
| D21 | main | 5 | 36 | "The cost of the ice cream is 10 × $4 = $<<10*4=40>>40. The cost of the frozen yoghurt is 4 × $1 = $<<4*1=4>>4. Caleb spent $40 − $4 = $36 more on ice cream than on frozen yogurt. #### 36" | Binary scored; single correct numeric answer; no ambiguity possible | OO, OC |
| D22 | main | 22 | 80 | "7 robots * $8.75 per robot = $<<7*8.75=61.25>>61.25 … $68.47 total spent in store … + $11.53 in change = $<<68.47+11.53=80>>80 to start. #### 80" | Decimal arithmetic; crowdworker-authored, single definitive answer | OC |
| D23 | main | 32 | 2290 | "80 of them, Daniel bought for $12 each … 50% were bought for $7 … On all games in total Daniel spent $960 + $931 + $399 = $<<960+931+399=2290>>2290. #### 2290" | Multi-part arithmetic; no ambiguity in answer | OO, OC |

---

### Deployment-Relevant Strengths

#### Strength 1: English monolingual plain-text format — no modality or language mismatch
- **Dimension(s):** IF
- **Observation:** Every sampled item in both `main` and `socratic` configs is exclusively English plain text. Questions are posed and answered entirely in English prose with no images, audio, tables, or non-ASCII characters. This eliminates script, modality, and language mismatch as sources of construct-irrelevant variance for the deployment, which is also text-only English.
- **Deployment relevance:** While the deployment additionally requires parsing semi-structured software outputs (a form GSM8K does not cover), the basic modality and language alignment means GSM8K's format does not introduce false negatives for the wrong reason — any performance gap reflects content/ontology mismatch, not medium mismatch.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them." — Plain English narrative, no structured data elements.
  - [D17] Example 1 (socratic, train, label=32): "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards." — Same plain-text format with Socratic sub-question scaffold.

#### Strength 2: Step-by-step natural language solution chains as a surface-level proxy for reasoning transparency
- **Dimension(s):** OF
- **Observation:** All sampled answers in both configs are written as multi-step natural language prose, not bare numeric outputs. Each intermediate computation is narrated (e.g., "First find the increase in rent…", "Let x represent the number of Chevys…") and annotated with calculator expressions `<<…>>`. The `socratic` config adds explicit sub-question headers that decompose the reasoning further.
- **Deployment relevance:** The deployment requires open-ended diagnostic narratives, not single-number answers. GSM8K's prose-with-steps format at least demonstrates that the benchmark evaluates models on extended reasoning chains rather than lookup-style answers. However, the similarity is superficial: GSM8K chains are deterministic arithmetic sequences, while deployment chains require methodological judgment. This is a weak strength that documents format resemblance only.
- **Datapoint citations:**
  - [D11] Example 6 (main, train, label=54): "First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft … #### 54" — Extended multi-step solution narrated in prose; all steps explicit.
  - [D14] Example 30 (main, train, label=7200): "First find the increase in rent by multiplying last year's rent by 30%: $1000 * .3 = $<<1000*.3=300>>300 … $600/month * 12 months/year = $<<600*12=7200>>7200/year #### 7200" — Six narrated arithmetic steps before final answer.
  - [D18] Example 23 (socratic, train, label=220): "Define a variable ** Let x represent the number of Chevys … Combine like terms ** 11x+15=301 … Divide by 11 ** x=<<26=26>>26" — Explicit step labels in Socratic config model intermediate reasoning decomposition.

#### Strength 3: Two-config structure offering different reasoning chain formats
- **Dimension(s):** IF, OF
- **Observation:** The dataset includes both a `main` config (prose solutions) and a `socratic` config (sub-question-scaffolded solutions). The Socratic format decomposes reasoning into explicit sub-questions, which is structurally similar to how a diagnostic consultation might proceed (e.g., "Is the homoscedasticity assumption violated here?" as a sub-question before recommending a correction). This configurability adds some methodological flexibility for evaluation design, even if the content remains elementary arithmetic.
- **Deployment relevance:** Minor positive: a benchmark that offers multiple reasoning decomposition formats is more adaptable as a reference point for constructing hybrid evaluation pipelines. The socratic format's explicit sub-question structure maps loosely onto the multi-step nature of statistical diagnostics, though the content is entirely misaligned.
- **Datapoint citations:**
  - [D17] Example 1 (socratic, train, label=32): "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards." — Sub-question format with explicit intermediate questions.
  - [D10] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. … On Thursday Buddy has a total of 27+5 = <<27+5=32>>32 baseball cards. #### 32" — Same problem in continuous-prose format for comparison; both scored against single final number.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of any statistical reasoning task category
- **Dimension(s):** IO
- **Observation:** Across all 80 sampled examples, every single item is an elementary arithmetic word problem. The most conceptually advanced items involve simple ratios (D15), one-variable linear equations (D9, D16), simple interest (D13), or percentage change (D14). None involve any statistical concept: no distributions, no inference, no hypothesis testing, no regression, no ANOVA, no power analysis, no effect size. The most "quantitatively rich" item computes a simple average of three ages (D6). The word "statistics" does not appear anywhere in the sample.
- **Deployment relevance:** The deployment's core task taxonomy — regression diagnostics, hypothesis testing under violated assumptions, ANOVA with post-hoc corrections, power analysis, and model selection — has zero coverage in this benchmark. This is not a gap that can be corrected by sampling more examples; the benchmark was designed to exclude advanced mathematics by construction ("solutions depend only on elementary concepts"). Scores on GSM8K carry no evidential weight about an LLM's ability to diagnose heteroscedasticity, interpret VIF scores, select between Welch and Student t-tests, or compute Cohen's d.
- **Datapoint citations:**
  - [D6] Example 11 (main, train, label=35): "Omi is twice as old as Kimiko. Arlette is 3/4 times as old as Kimiko. If Kimiko is 28 years old, calculate the average age of the three?" — The word "average" appears, but this is arithmetic mean of three given numbers — not statistical inference.
  - [D13] Example 43 (main, train, label=720): "If Ariella has $200 more in her son's saving account than Daniella has, then she has $400 + $200 = $600 … The total amount of money in Ariella's account after two years is $600 + $120 = $720 #### 720" — Simple interest calculation; closest to a finance-quantitative domain but still elementary arithmetic with no uncertainty, variance, or distributional reasoning.
  - [D4] Example 6 (main, train, label=54): "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" — Elementary geometry; the most formula-heavy non-algebraic example seen; not statistical in any sense.
  - [D16] Example 45 (main, train, label=120): "Let N be the original price each friend was going to pay. 10N=6(N+8) … 4N=48 … N=<<12=12>>12 … 10*12=<<10*12=120>>120 #### 120" — Highest-complexity item type (one-variable linear equation); still has a single deterministic solution with no ambiguity.

#### CRITICAL Concern 2: Inputs are child-oriented consumer narrative scenarios — no professional or semi-structured content
- **Dimension(s):** IC
- **Observation:** Every sampled item involves a named child or everyday consumer in a domestic/recreational scenario: birthday parties with piñatas (D3), baseball card collections (D1, D17), cupcake baking (D2), toy cars (D8), dandelion puffs (Example 27), jelly beans and gummy worms (Example 25), field trip vans (Example 8). The most "professional" scenario involves a company's commuting employees (Example 28) and a bakery's profit (Example 20), but both remain elementary arithmetic with no domain-specific vocabulary. No item contains technical jargon of any kind — no Greek letters, no statistical terms, no software output, no variable names, no formulas beyond basic arithmetic.
- **Deployment relevance:** Deployment users will paste CSV snippets, R `lm()` summary tables, Python `statsmodels` OLS output, and queries containing terms like "heteroscedasticity," "VIF," "Type III SS," "Cook's distance," and "random effects." GSM8K's input distribution and vocabulary are entirely disjoint from these inputs. Models that perform well on GSM8K have learned to parse casual domestic narrative — a skill orthogonal to parsing semi-structured statistical software output.
- **Datapoint citations:**
  - [D3] Example 3 (main, train, label=99): "It's Ava's birthday party. Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats. They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." — Archetypal child-oriented consumer scenario; vocabulary is entirely non-technical.
  - [D7] Example 13 (main, train, label=1825): "Sally and Bob have made plans to go on a trip at the end of the year. They both decide to work as babysitters and save half of what they've earned for their trip." — Babysitting savings problem; no domain-specific vocabulary.
  - [D20] Example 36 (main, train, label=1080): "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day." — Ecological chain multiplication; entirely non-statistical narrative.
  - [D2] Example 2 (main, train, label=9): "Anna baked 60 cupcakes. She gives away 4/5 of the cupcakes to her classmates." — Fraction arithmetic embedded in a school-lunch scenario; no quantitative professional register.

#### CRITICAL Concern 3: Binary exact-match scoring against a single numeric answer is structurally incompatible with the deployment's evaluation requirements
- **Dimension(s):** OO
- **Observation:** Every answer in the sample ends with `#### {single integer or decimal}`, and the scoring criterion is whether the model's final answer matches this number exactly. There is no partial credit, no rubric, no alternative valid solution pathway. The `<<…>>` calculator annotations confirm intermediate answers are also single-valued. Even the most complex item (D12, algebraic system of equations) has one and only one correct numerical answer. The `socratic` config changes the decomposition scaffolding but not the scoring: still `#### 220` for Example 23.
- **Deployment relevance:** The deployment explicitly requires evaluation that rewards methodologically defensible reasoning even when final numbers differ (e.g., whether to log-transform a skewed predictor, which covariates to include, fixed vs. random effects). The user confirmed that exact-match correctness is inadequate for most use cases. GSM8K's output taxonomy cannot express any concept of partial credit, methodological soundness, or legitimate answer pluralism. Even GSM8K's own paper acknowledges false positives (correct numbers from flawed reasoning) and false negatives (sound reasoning penalized for ambiguity) — failure modes that would be severely amplified in the deployment domain.
- **Datapoint citations:**
  - [D10] Example 1 (main, train, label=32): "On Thursday Buddy has a total of 27+5 = <<27+5=32>>32 baseball cards. #### 32" — Single numeric label; there is no ambiguity in this answer, which makes the binary scoring appropriate here but demonstrates the mismatch: deployment answers have no analogous uniqueness.
  - [D21] Example 5 (main, train, label=36): "Caleb spent $40 − $4 = $36 more on ice cream than on frozen yogurt. #### 36" — One deterministic answer; scoring is binary. No methodological choice exists.
  - [D12] Example 23 (main, train, label=220): "Let x represent the number of Chevys … 11x+15=301 … Buicks:12+8(26)=220 #### 220" — Most complex problem type; still only one correct answer. Contrasts sharply with deployment questions like "Should I use fixed or random effects for this panel data?" where multiple defensible answers exist.
  - [D23] Example 32 (main, train, label=2290): "On all games in total Daniel spent $960 + $931 + $399 = $<<960+931+399=2290>>2290. #### 2290" — Multi-step arithmetic; single numeric ground truth produced by crowdworker; no expert judgment required.

#### CRITICAL Concern 4: Ground-truth labels authored by crowdworkers solving elementary arithmetic — not representative of expert statistical judgment
- **Dimension(s):** OC
- **Observation:** Every ground-truth label in the sample is a single integer or decimal (32, 9, 99, 21, 36, 54, 90, 80, 28, 22, 35, 78, 1825, 24, 9, 120, 72, 54, 1080, 80, 138, 27, 80, 90, 16, 2250, 9, 40, 2280, 7200, 10, 2290, 2, 500, 333200, 1080, 80, 90, 720, 11000, 120, 24, 72, 220, 180, 16, 283). These were produced by Upwork/Surge AI contractors verifying arithmetic correctness — no statistical domain expertise was required or documented. The labels have no ambiguity for their domain (arithmetic), which is precisely why they are inadequate for the deployment domain (statistical methodology), where legitimate pluralism is structurally unavoidable.
- **Deployment relevance:** Deployment ground truths require practicing statisticians adjudicating questions like "Is this VIF threshold of 5 or 10 more appropriate here?" or "Is log-transformation warranted given this skewness coefficient?" Crowdworker arithmetic verification produces ground truths of an entirely different epistemic type. A benchmark cannot be valid for the deployment if its annotation process is categorically mismatched with the expertise required by the deployment's ground-truth space.
- **Datapoint citations:**
  - [D22] Example 22 (main, train, label=80): "7 robots * $8.75 per robot = $<<7*8.75=61.25>>61.25 … + $11.53 in change = $<<68.47+11.53=80>>80 to start. #### 80" — Ground truth (80) is verifiable by anyone who can add decimals; requires no domain expertise.
  - [D21] Example 5 (main, train, label=36): "Caleb spent $40 − $4 = $36 more on ice cream than on frozen yogurt. #### 36" — Ground truth requires no statistical judgment; any human who can subtract knows the answer.
  - [D23] Example 32 (main, train, label=2290): "On all games in total Daniel spent $960 + $931 + $399 = $<<960+931+399=2290>>2290. #### 2290" — Multi-part arithmetic but single deterministic answer; no expert adjudication needed or present.

---

#### MAJOR

#### MAJOR Concern 5: Input form does not include any semi-structured, tabular, or software-output content
- **Dimension(s):** IF
- **Observation:** All 80 sampled items are continuous narrative prose. No item contains a table, CSV row, column header, software output block, indentation-delimited structure, or any formatting convention associated with R or Python output. The closest approach to structured data is embedded numbers within sentences (e.g., "4 bags of Reese's for $9 per bag"). There are no column names, no variable labels, no p-values embedded in output format, no model summary tables.
- **Deployment relevance:** The deployment's primary input type is semi-structured content: pasted CSV previews, R `lm()` or `summary.aov()` output, Python `statsmodels` OLS tables, or correlation matrices. Evaluating an LLM on GSM8K tests its ability to parse casual English narrative — a signal that does not transfer to parsing `Coefficients: Estimate Std. Error t value Pr(>|t|)` table formats or `Breusch-Pagan test: BP = 12.3, df = 3, p-value = 0.006`.
- **Datapoint citations:**
  - [D3] Example 3 (main, train, label=99): "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." — Information presented as natural language list embedded in prose; no tabular or structured format.
  - [D5] Example 7 (main, train, label=90): "There are enough provisions in a castle to feed 300 people for 90 days." — All quantitative information delivered as sentence-embedded numbers; no semi-structured representation.
  - [D15] Example 38 (main, train, label=90): "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440…" — Ratio given in prose, not as a table or data structure.

#### MAJOR Concern 6: No domain-specific vocabulary — complete lexical disjunction from deployment register
- **Dimension(s):** IC
- **Observation:** Scanning all 80 sampled items, no instance contains any word from the deployment's professional vocabulary: "heteroscedasticity," "multicollinearity," "VIF," "regression," "coefficient," "residual," "ANOVA," "p-value," "confidence interval," "standard error," "hypothesis," "distribution," "variance," "correlation," "t-test," "F-statistic," "effect size," "power," "Bayesian," or any other statistical term. The vocabulary is entirely that of elementary school arithmetic word problems: "baseball cards," "cupcakes," "piñata," "dandelion puffs," "jelly beans," "toy cars," "coins."
- **Deployment relevance:** A model capable of parsing "heteroscedasticity" and recommending the Breusch-Pagan test must have encountered such vocabulary in its training or evaluation. GSM8K contributes zero signal about vocabulary comprehension in the professional statistical register. A model that tops GSM8K leaderboards may still be unable to identify "VIF" or parse `lm()` output — GSM8K performance provides no evidence one way or the other.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them." — Vocabulary: baseball cards, loses, half. No technical terms.
  - [D8] Example 19 (main, train, label=54): "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year." — "Increases by 50%" is the most technical phrase in the sample; no statistical vocabulary.
  - [D19] Example 4 (main, train, label=21): "The bottle of milk cost was 75% of the total cost of the sandwich and juice." — Percentage arithmetic; no statistical terminology.

---

#### MINOR

#### MINOR Concern 7: Socratic config introduces a different reasoning format not present in deployment interaction patterns
- **Dimension(s):** IF, OF
- **Observation:** The `socratic` config reformats solutions as explicit question-answer pairs ("How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2…"), adding scaffolding absent from the `main` config. This format has no direct analogue in the deployment, where users pose open-ended analytical queries and expect integrated recommendations, not Socratic sub-question chains.
- **Deployment relevance:** Minor: the Socratic format's step decomposition has a superficial structural resemblance to multi-step statistical diagnostics, but the content mismatch (arithmetic vs. statistical inference) dwarfs this formal similarity. If the deployment team were to use GSM8K as a component benchmark, they would need to decide which config to use and why.
- **Datapoint citations:**
  - [D17] Example 1 (socratic, train, label=32): "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards." — Sub-question format with explicit labeling; does not resemble deployment's open-ended query format.
  - [D18] Example 23 (socratic, train, label=220): "Define a variable ** Let x represent the number of Chevys … Combine like terms ** 11x+15=301" — Step-labeled algebraic decomposition; format is unique to this config.

#### MINOR Concern 8: Calculator annotation mechanism `<<…>>` is a benchmark-internal artifact with no deployment analogue
- **Dimension(s):** IF
- **Observation:** All 80 sampled answers embed inline calculator annotations in the format `<<expression=result>>`, e.g., `<<30/2=15>>`, `<<9*4=36>>`, `<<600*12=7200>>`. These are auto-generated preprocessing artifacts described in the paper as injected into training solutions for a calculator-simulation mechanism. They appear in every answer in the sample.
- **Deployment relevance:** The deployment involves no equivalent preprocessing annotation; users interact with a live LLM interface. If the evaluation pipeline is not aware that these annotations are training artifacts (not naturally occurring in deployment data), they could introduce construct-irrelevant variance. This is a minor concern because the annotations are in the answers (outputs) rather than the questions (inputs), and most evaluation frameworks strip them before comparison — but it is worth flagging for pipeline implementers.
- **Datapoint citations:**
  - [D10] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. … On Thursday Buddy has a total of 27+5 = <<27+5=32>>32 baseball cards." — Every arithmetic step includes `<<…>>` annotation.
  - [D14] Example 30 (main, train, label=7200): "$1000 * .3 = $<<1000*.3=300>>300 … $200 * .5 = $<<200*.5=100>>100 … $600/month * 12 months/year = $<<600*12=7200>>7200/year" — Six separate calculator annotations in a single answer.

---

### Content Coverage Summary

All 80 sampled items (47 `main`, 33 `socratic`) are elementary arithmetic word problems set in child-oriented or everyday consumer scenarios. The content can be fully characterized by five recurring problem types:

1. **Sequential arithmetic with named quantities** (baseball cards, cupcakes, coins) — ~60% of items
2. **Percentage/ratio/fraction problems** (Anna's cupcakes at 4/5, Amalie's ratio 10:45, Jessica's 30% rent increase) — ~20% of items
3. **Rate/time/unit conversion problems** (Roberto's skipping rate, rainfall per day) — ~10% of items
4. **One-variable linear equations** (Jim's car collection, ten friends splitting a gift cost) — ~5% of items
5. **Simple interest/compound growth** (Ariella's savings, Bobby's toy cars at 50% annual growth) — ~5% of items

The most complex problem in the sample is a one-variable linear equation (D16: `10N=6(N+8)`) or a system expressible as a single variable (D9: `11x+15=301`). No problem involves two independent variables, distributional reasoning, uncertainty quantification, inference under uncertainty, or any concept from introductory statistics.

The `socratic` config reproduces the same problems as `main` with explicit sub-question scaffolding; no new content types appear. The register is uniformly informal and child-oriented. Calculator annotation `<<…>>` artifacts appear in 100% of answers.

This content profile is entirely consistent with the benchmark's documented design as grade school arithmetic word problems and fully confirms all the gap analyses documented in the benchmark YAML and web search findings.

---

### Limitations

1. **Sample is train-split only**: All 80 examples are from the training split. The test split (1,319 items in `main`) was not sampled; test items may differ in complexity distribution, though the benchmark documentation suggests they are drawn from the same population.

2. **80 examples from ~8,500 total**: The sample represents ~0.9% of the full dataset. While the sampled items are highly consistent with documented properties and each other, rare problem types (if any exist that are more complex or statistically relevant) could have been missed. Given the uniformity observed, this is unlikely to alter the conclusions, but cannot be ruled out with certainty.

3. **`socratic` config structure not independently validated**: The 33 `socratic` examples are all paired duplicates of `main` examples. No unique `socratic`-only problem types were observed to differ in complexity or content.

4. **Answer-side quality for annotation purposes**: The sample confirms that labels are single numeric values produced by deterministic arithmetic. Whether the ~1.7% residual annotator disagreement rate (documented in the paper) manifests in any sampled item cannot be determined from the data alone.

5. **No access to model performance stratification**: The dataset does not include metadata about which items are harder or easier, which models fail on which items, or which items triggered the documented false-positive/false-negative verifier failure modes. The analysis is limited to input/output content.

