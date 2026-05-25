## Dataset Analysis Report

**Dataset(s):** openai/gsm8k (configs: `main`, `socratic`)
**Analysis date:** 2025-07-15
**Examples reviewed:** 47 (`main`, train) + 33 (`socratic`, train) = 80 total
**Columns shown:** question, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | main | 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | Clean, multi-step prose word problem requiring 4 sequential arithmetic operations | IO |
| D2 | main | 1 | 32 | "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." | Well-formed natural language solution with calculator annotation format; no student notation | IC, IF |
| D3 | main | 6 | 54 | "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" | Uses US customary units (feet, cubic feet) in a volume problem | IC |
| D4 | main | 12 | 78 | "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." | Answer annotation contains an error in the expression: <<6+6=12>> should be <<6*2=12>>; confirms the paper's acknowledgment of annotation imperfections | OC |
| D5 | main | 3 | 99 | "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag. How much did the unicorn piñata and the treats cost altogether?" | US-branded consumer products; implicitly assumes familiarity with US candy brands | IC |
| D6 | main | 22 | 80 | "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change. How much did Austin start with?" | Multi-step problem with decimal arithmetic and tax — above-grade for grades 3–4 but within scope | IO |
| D7 | main | 7 | 90 | "The 60 days' worth of food will last this smaller group for 60 days / (2/3) = <<60/(2/3)=90>>90 more days." | Division by a fraction — aligned with grade 5–6 CCSS-M but not lower grades | IO |
| D8 | main | 23 | 220 | "Let x represent the number of Chevys; Fords:3+2x; Buicks:4(3+2x)=12+8x; Total:x+3+2x+12+8x=301; 11x+15=301" | Uses algebraic variables and simultaneous-style equation — above elementary grade band (grades 3–6) | IO |
| D9 | main | 43 | 720 | "If she earns an interest of 10% in the first year, her savings account increases by 10/100 * $600 = $<<10/100*600=60>>60. In the second year, she earns the same amount of interest, which $60 + $60 = $<<60+60=120>>120" | Simple interest calculation — above typical grades 3–6 curriculum; note solution applies simple (not compound) interest correctly | IO |
| D10 | main | 45 | 120 | "Let N be the original price each friend was going to pay. 10N=6(N+8); 10N=6N+48; 4N=48; N=<<12=12>>12" | Algebraic equation setup with variable N — outside grades 3–6 scope | IO |
| D11 | main | 38 | 90 | "The total ratio of the coins they both have is 10+45 = <<10+45=55>>55. The fraction of the ratio representing the number of coins that Amalie has is 45/55, and since the total number of coins they both have is 440, Amalie has 45/55*440 = <<45/55*440=360>>360 coins." | Ratio and proportion problem — grade 6 borderline, but not typical grades 3–5 | IO |
| D12 | main | 2 | 9 | "After giving away 4/5 of the cupcakes, Anna has 60 / 5 = <<60/5=12>>12 cupcakes. After eating 3 cupcakes, Anna has 12 - 3 = <<12-3=9>>9 cupcakes." | 2-step problem with fractions of a whole — matches grade 3–4 level | IO |
| D13 | main | 4 | 21 | "The juice was two times more expensive than the sandwich, so it was 4 * 2 = $<<2*4=8>>8. The juice and the sandwich in total were a cost of 4 + 8 = $<<4+8=12>>12. So the cost of one bottle of milk was 75/100 * 12 = $<<75/100*12=9>>9." | "Two times more expensive" phrasing is ambiguous (could mean 3× total vs. 2×) — potential construct-irrelevant variance | IC |
| D14 | main | 19 | 54 | "In the first year, Bobby will acquire 16 * .5 = <<16*.5=8>>8 new cars. After the first year, he will have a total of 16 + 8 = <<16+8=24>>24 cars." | Percentage/decimal computation (50% growth) — grade 5–6 | IO |
| D15 | main | 30 | 7200 | "First find the increase in rent by multiplying last year's rent by 30%: $1000 * .3 = $<<1000*.3=300>>300. Then find the food cost increase by multiplying last year's costs by 50%: $200 * .5 = $<<200*.5=100>>100." | Multi-operation percentage problem with adult financial context (rent, insurance) — above grades 3–6 child context | IC |
| D16 | main | 20 | 138 | "If the bakery can make 12 pies, this means there would be 12 * 3 = <<12*3=36>>36 pie pieces. For all the pieces the bakery would make 36 * 4 = $<<36*4=144>>144. The cost of making 12 pies is 12 * 0.5 = $<<12*0.5=6>>6. That means the bakery would make 144 - 6 = $<<144-6=138>>138." | 4-step business profit problem — structurally representative multi-step | IO |
| D17 | main | 24 | 180 | "In a northwestern town, it rained 4 inches per day during the first 15 days of November. For the remainder of the month, the average daily rainfall was twice the amount observed during the first 15 days." | "Inches" as a US customary unit; geographic reference to a "northwestern town" — US-situated | IC |
| D18 | main | 13 | 1825 | "Since each year have 365 days, the total amount of money Sally will save in a year is $3/day * 365 days/year = $<<3*365=1095>>1095/year" | Use of 365 days/year as incidental background knowledge | IC |
| D19 | main | 36 | 1080 | "First find the total number of birds eaten per day: 30 snakes * 3 birds/snake = <<30*3=90>>90 snakes. Then multiply the number of snakes by the number of beetles per snake to find the total number of beetles eaten per day: 90 snakes * 12 beetles/snake = <<90*12=1080>>1080 beetles" | Solution contains a labeling error: "90 snakes" should be "90 birds"; illustrates that correct final answers can have flawed intermediate narration | OC |
| D20 | main | 5 | 36 | "The cost of the ice cream is 10 × $4 = $<<10*4=40>>40. The cost of the frozen yoghurt is 4 × $1 = $<<4*1=4>>4. Caleb spent $40 − $4 = $36 more on ice cream than on frozen yogurt." | "How much more" subtraction problem — matches Common Core phrasing; solved correctly | IO, IC |
| D21 | main | 27 | 9 | "Caleb was left with 40 - 3 - 3 - 5 - 2 = <<40-3-3-5-2=27>>27 dandelion puffs to give to his friends. They each received 27/3 = <<27/3=9>>9 dandelion puffs" | Subtraction then equal-sharing division — grade 3–4 level | IO |
| D22 | main | 31 | 10 | "He sold 50 cones because 100 / 2 = <<100/2=50>>50. He gave away 10 cones because 50 / 5 = <<50/5=10>>10" | Note: "every sixth customer" → solution divides by 5, not 6. Possible arithmetic/logic error in problem or solution | OC |
| D23 | socratic | 23 | 220 | "Define a variable ** Let x represent the number of Chevys; How many Fords does Jim have? ** Fords:3+2x; Write an equation ** Total:x+3+2x+12+8x=301; Combine like terms ** 11x+15=301" | Socratic config breaks algebraic solution into explicit sub-question steps — useful chain-of-thought scaffold | IF |
| D24 | main | 9 | 28 | "Second person = 27 - 7 = <<27-7=20>>20 kg; 103 - 27 - 20 = <<103-27-20=56>>56 kg; 56/2 = <<56/2=28>>28 kg; The last two people each lost 28 kilograms of weight." | Uses metric units (kilograms) — not US customary; one of the few non-US-unit examples in the sample | IC |
| D25 | main | 39 | 20 | "Starting with $100, he paid $20 to Colin, leaving him with $100-$20=$<<100-20=80>>80. Twice as much as $20 is 2*$20=$<<2*20=40>>40. Thus, he paid $40 to Helen, leaving him with $80-$40=$<<80-40=40>>40." | Clean running-total tracking across 4 sequential operations — illustrates well-formed multi-step solution | IO |
| D26 | main | 11 | 35 | "Arlette is 3/4 * 28 years = <<3/4*28=21>>21 years old. If you add up their ages, it sums to 21 years + 56 years + 28 years = <<21+56+28=105>>105 years. The average age for the three is 105 years / 3 people = <<105/3=35>>35 years/person" | Fraction multiplication then averaging — appropriate for grade 5–6 | IO |
| D27 | main | 44 | 11000 | "He sold his car for 20000*.8=$<<20000*.8=16000>>16,000. He bought the new car for 30,000*.9=$<<30000*.9=27000>>27,000. That means he was out of pocket 27,000-16,000=$<<27000-16000=11000>>11,000" | Adult financial scenario (car purchase, percentages of $20,000–$30,000) — well outside elementary student context | IC |
| D28 | main | 35 | 333200 | "The price is $98 per sq ft and it's 3,400 sq ft big so the property costs 98*3400 = $<<98*3400=333200.00>>333,200.00" | Real estate pricing problem with $333,200 result — entirely adult financial domain | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-step arithmetic chain-of-thought solutions present throughout
- **Dimension(s):** IO
- **Observation:** Every sampled problem requires 2–6 sequential arithmetic operations, and the solutions demonstrate intermediate step recording. The dataset design explicitly favors chain-of-thought reasoning over direct answer generation, confirmed empirically in the paper (performance drops from 20.6% to 5.2% without intermediate steps).
- **Deployment relevance:** The deployment LLM must trace a student's step-by-step reasoning to identify errors at specific steps. GSM8K's solutions demonstrate the multi-step reasoning chain format the LLM will be asked to analyze — if only as an idealized reference. The step structure in the `main` config and the explicit sub-question decomposition in `socratic` both represent intermediate-step problem-solving.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — 4-step solution illustrating sequential arithmetic chains.
  - [D16] Example 20 (main, train, label=138): "If the bakery can make 12 pies, this means there would be 12 * 3 = <<12*3=36>>36 pie pieces. For all the pieces the bakery would make 36 * 4 = $<<36*4=144>>144." — 4-step business profit problem with explicit intermediate labeling.
  - [D25] Example 39 (main, train, label=20): "Starting with $100, he paid $20 to Colin, leaving him with $100-$20=$<<100-20=80>>80. Twice as much as $20 is 2*$20=$<<2*20=40>>40." — Running-total tracking across sequential operations.

#### Strength 2: Socratic config provides explicit sub-question decomposition
- **Dimension(s):** IO, IF
- **Observation:** The `socratic` configuration reformats every solution as a sequence of sub-questions with answers, explicitly labeling each reasoning step with a guiding question. This is the closest representation in the dataset to structured step-level annotation.
- **Deployment relevance:** The deployment requires identifying which step contains the first error. The socratic format's step-question–answer structure provides a useful structural parallel to step-indexed solution analysis, even though the solutions are model-facing clean prose rather than student work.
- **Datapoint citations:**
  - [D23] Example 23 (socratic, train, label=220): "Define a variable ** Let x represent the Chevys; How many Fords does Jim have? ** Fords:3+2x; Write an equation ** Total:x+3+2x+12+8x=301" — Each reasoning step labeled with an explicit sub-question.
  - [D2] Example 1 (socratic config): "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. How many cards does Buddy have on Wednesday? ** On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Step-indexed intermediate reasoning format.

#### Strength 3: US dollar currency and implicitly US cultural contexts
- **Dimension(s):** IC
- **Observation:** The overwhelming majority of problems in the sample use USD ($) as the currency and reference US consumer contexts (candy brands, football, tax, bakeries, malls). No foreign currency appears in the sample. This aligns with the deployment's US elementary school context.
- **Deployment relevance:** The deployment population is US-based; US dollar problems at least partially match the cultural reference frame. Problems involving "how much more" (subtraction) and equal-sharing (division) mirror Common Core phrasing.
- **Datapoint citations:**
  - [D5] Example 3 (main, train, label=99): "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." — US-branded consumer products, USD pricing.
  - [D20] Example 5 (main, train, label=36): "The cost of the ice cream is 10 × $4 = $<<10*4=40>>40…Caleb spent $40 − $4 = $36 more on ice cream than on frozen yogurt." — "How much more" subtraction phrasing in a USD context.

#### Strength 4: Incidental coverage of US customary length and weight units
- **Dimension(s):** IC
- **Observation:** Several problems use feet, pounds, and inches — US customary units relevant to the deployment's grades 3–6 curriculum (where unit conversion in the customary system is a CCSS-M standard). The sample includes at least cubic feet (Example 6), feet (Example 35), pounds (Examples 9, 12, 25).
- **Deployment relevance:** US customary units are a high-frequency error source in the deployment. GSM8K at least incidentally uses these units in problem contexts, which means some problems exercise the arithmetic operations that underlie unit-conversion errors, even if no problem explicitly requires a unit conversion computation.
- **Datapoint citations:**
  - [D3] Example 6 (main, train, label=54): "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" — Volume problem using US customary units (feet).
  - [D17] Example 24 (main, train, label=180): "In a northwestern town, it rained 4 inches per day during the first 15 days of November." — Inches as measurement unit in a US-located context.

#### Strength 5: Problems cover the "how many more" subtraction phrasing
- **Dimension(s):** IC, IO
- **Observation:** Multiple sampled problems use "how many more" as the operative question, which is explicitly flagged as a high-frequency Common Core phrasing that triggers student confusion between subtraction and addition. The problems correctly operationalize this as subtraction.
- **Deployment relevance:** Common Core phrasing misread ("how many more" vs. "how many total") is one of the five named error categories in the deployment's taxonomy. GSM8K's linguistic diversity does appear to include this phrasing, confirming at least partial coverage of this error trigger.
- **Datapoint citations:**
  - [D20] Example 5 (main, train, label=36): "How much more did Caleb spend on ice cream than on frozen yoghurt?" — "How much more" operationalized as subtraction.
  - [D28] Example 28 (main, train, label=40): "How many more employees drive to work than take public transportation?" with solution "80-40=<<80-40=40>>40 employees" — "How many more" correctly solved via subtraction.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: No error-type taxonomy — binary correct/incorrect label only
- **Dimension(s):** IO, OO
- **Observation:** Every sampled problem has exactly two fields: `question` (prose) and `answer` (final numeric value preceded by natural language steps). There is no label for error type, error location, misapplied operation, arithmetic slip, or any other diagnostic category. The label is entirely determined by the final number after `####`. No metadata field encodes step-level correctness.
- **Deployment relevance:** The deployment requires classifying every error into one of five categories (misapplied operation, arithmetic slip, wrong setup, incomplete chain, plus US-curriculum subtypes). GSM8K provides zero support for this. An LLM evaluated on GSM8K accuracy cannot be assessed for its ability to diagnose which *kind* of error occurred — the benchmark's entire label space is orthogonal to the deployment's output ontology.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): Answer field ends "#### 32" with no error-type annotation anywhere in the record. The problem is labeled only by its correct final answer.
  - [D2] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards." — Calculator annotation encodes computational expression but carries no information about what error type a student might commit here.
  - [D22] Example 31 (main, train, label=10): "He gave away 10 cones because 50 / 5 = <<50/5=10>>10" — The problem states "every sixth customer" but the solution divides by 5; if this is an error in the dataset, it goes uncategorized; if intentional, the taxonomy for distinguishing problem-setup errors from arithmetic errors is absent.

#### Concern 2: Input distribution is professionally authored clean prose — no student-work features
- **Dimension(s):** IC, IF
- **Observation:** Every sampled problem and solution is fluent, grammatically complete English prose with no carry marks, partial products, crossing-out, abbreviations ("r" for remainder, "b/c"), informal phrasing ("I did 5 times 3"), area model notation, number bonds, or partial-quotients division. All solutions flow linearly with standard calculator annotations (`<<expr=result>>`).
- **Deployment relevance:** The deployment system must correctly parse noisy student-authored work containing precisely these features. GSM8K provides no training signal or evaluation surface for parsing unconventional student notation. An LLM that performs well on GSM8K-format clean prose has never been tested on the input distribution it will actually encounter. The 2026 DrawEduMath follow-up study (web search findings) directly confirms models misdiagnose errors specifically when student work is non-standard.
- **Datapoint citations:**
  - [D2] Example 1 (main, train): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Perfectly formatted prose with machine-generated calculator annotations; no student register elements.
  - [D19] Example 36 (main, train, label=1080): "First find the total number of birds eaten per day: 30 snakes * 3 birds/snake = <<30*3=90>>90 snakes" — Even where a narration label error appears ("90 snakes" instead of "90 birds"), the format is clean annotated prose, not student informal work.

#### Concern 3: Output evaluation is final-answer correctness only — no diagnostic explanation mechanism
- **Dimension(s):** OO, OF
- **Observation:** The dataset schema has two string fields: `question` and `answer`. The `answer` field contains natural language steps followed by `#### [number]`. Benchmark evaluation parses only the number after `####` and checks it against the gold answer. There is no field, rubric, or scoring mechanism for evaluating whether a generated explanation identifies the error location, names the error type correctly, or uses classroom-teacher register.
- **Deployment relevance:** The deployment requires evaluating three distinct output dimensions: (1) correct identification of the earliest error step, (2) correct error-type classification, and (3) teacher-register explanation quality. GSM8K's scoring function evaluates none of these. A model that generates "you multiplied when you needed to divide because the problem is asking how many groups" cannot be distinguished from one that generates "the answer is wrong" using GSM8K's evaluation apparatus.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): The answer field "#### 32" is the entirety of what the benchmark scores; the preceding natural language steps are not evaluated for register, pedagogical clarity, or error diagnosis.
  - [D16] Example 20 (main, train, label=138): "That means the bakery would make 144 - 6 = $<<144-6=138>>138. #### 138" — Evaluation anchors entirely on 138; the quality or register of the intermediate explanation receives no score.

#### Concern 4: Ground truth generated by freelance contractors with no pedagogical expertise or grade-level differentiation
- **Dimension(s):** OC
- **Observation:** The benchmark uses final numerical answer agreement among Upwork/Surge AI contractors as its correctness criterion. No domain educators, curriculum specialists, or classroom teachers participated. No grade-level acceptability criteria are applied (e.g., whether an improper fraction is acceptable at grade 3 vs. grade 5). The estimated error rate is 1.7% with an acknowledged possibility of more subtle errors.
- **Deployment relevance:** The deployment's ground truth is defined by former elementary teachers and curriculum specialists applying grade-differentiated pedagogical standards. These annotator populations and judgment criteria are entirely different from GSM8K's. A label agreement on GSM8K does not constitute evidence that the model's diagnostic output would match teacher judgment on the same problem.
- **Datapoint citations:**
  - [D4] Example 12 (main, train, label=78): "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." — The calculator annotation `<<6+6=12>>` is inconsistent with the surrounding text `6*2`; the final answer is correct but the annotation contains a notation error that contractor review missed, confirming annotation limitations.
  - [D22] Example 31 (main, train, label=10): "He gave away 10 cones because 50 / 5 = <<50/5=10>>10" — The problem says "every sixth customer" yet the solution uses ÷5 rather than ÷6. If this is a genuine error that survived contractor review, it illustrates the quality control gap. The label is '10' regardless.

---

#### MAJOR

#### Concern 5: Substantial proportion of problems are above grades 3–6 CCSS-M scope
- **Dimension(s):** IO
- **Observation:** Among the 47 sampled `main` examples, at least 6 clearly involve content beyond grades 3–6 CCSS-M: algebraic variable introduction (Examples 23, 45), ratio/proportion problems (Example 38), percentage of large adult-scale financial quantities (Examples 30, 44, 35), and compound/simple interest over years (Example 43). Grade-band coverage is uneven; the benchmark has no grade-level metadata.
- **Deployment relevance:** The deployment targets grades 3–6. If an LLM's diagnostic capability is being evaluated using GSM8K, problems above this grade band would assess reasoning abilities not relevant to the deployment, and good performance on algebra-level problems would not indicate fitness for grade-3 arithmetic diagnosis.
- **Datapoint citations:**
  - [D8] Example 23 (main, train, label=220): "Let x represent the number of Chevys; Fords:3+2x; Buicks:4(3+2x)=12+8x; Total:x+3+2x+12+8x=301; 11x+15=301" — Formal algebraic variable introduction and linear equation, beyond grades 3–6.
  - [D10] Example 45 (main, train, label=120): "Let N be the original price each friend was going to pay. 10N=6(N+8); 10N=6N+48; 4N=48" — Algebraic equation solving, outside grades 3–6 scope.
  - [D9] Example 43 (main, train, label=720): "If she earns an interest of 10% in the first year, her savings account increases by 10/100 * $600 = $<<10/100*600=60>>60." — Simple interest computation, typically a middle school or high school topic.
  - [D27] Example 44 (main, train, label=11000): "He sold his car for 20000*.8=$<<20000*.8=16000>>16,000. He bought the new car for 30,000*.9=$<<30000*.9=27000>>27,000." — Adult financial scenario with $20,000–$30,000 values, outside elementary context.

#### Concern 6: Adult financial and professional contexts dominate, mismatching elementary student frame of reference
- **Dimension(s):** IC
- **Observation:** A sizeable fraction of the sampled problems involve adult contexts: car purchases ($20,000–$30,000 — Example 44), real estate ($98/sq ft property — Example 35), annual savings and interest calculations (Examples 13, 43), business profit (Example 20), and professional workplace scenarios (Example 46). While not technically preventing arithmetic evaluation, these contexts differ meaningfully from the school, playground, and household contexts that appear in grades 3–6 CCSS-M problem sets.
- **Deployment relevance:** The deployment serves grades 3–6 students whose problems involve familiar child-accessible contexts. GSM8K's adult-domain problems would not represent the phrasing and contextual reasoning patterns that elementary students encounter, reducing the alignment between benchmark and deployment input distributions.
- **Datapoint citations:**
  - [D28] Example 35 (main, train, label=333200): "The price is $98 per sq ft and it's 3,400 sq ft big so the property costs 98*3400 = $<<98*3400=333200.00>>333,200.00" — Real estate problem with $333,200 total; entirely outside elementary student frame.
  - [D15] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month." — Adult budget management problem.
  - [D27] Example 44 (main, train, label=11000): "James decides to replace his car. He sold his $20,000 car for 80% of its value." — Adult vehicle transaction context.

#### Concern 7: No unit conversion problems found in sample; coverage of high-frequency US curriculum error type unknown
- **Dimension(s):** IO, IC
- **Observation:** None of the 80 sampled examples involves an explicit unit conversion computation (e.g., converting inches to feet, cups to quarts, ounces to pounds). The problems use US customary units incidentally (as given quantities) but never require students to convert between units within the same measurement system — a documented CCSS-M grade 4 standard and a high-frequency error source in the deployment.
- **Deployment relevance:** Unit conversion slips (inches/feet, cups/quarts) are explicitly named as a high-frequency error type in the deployment's taxonomy. If this problem type is underrepresented or absent from GSM8K (which the sample suggests), the benchmark would fail to assess the LLM's diagnostic capability for this specific error category.
- **Datapoint citations:**
  - [D3] Example 6 (main, train, label=54): "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high" — Uses feet as given quantities but requires no conversion computation.
  - [D17] Example 24 (main, train, label=180): "it rained 4 inches per day during the first 15 days of November" — Inches used as given unit; no conversion to feet or other unit required.

#### Concern 8: Metric units appear in the sample alongside US customary, inconsistent with deployment population
- **Dimension(s):** IC
- **Observation:** At least one sampled problem uses kilograms as the primary unit (Example 9: "Four people lost a total of 103 kilograms of weight"). The deployment population operates under US customary units exclusively in grades 3–6 CCSS-M; metric units are not introduced as a standard until later grades.
- **Deployment relevance:** Problems using metric units would not represent the unit conventions of the deployment's target curriculum and could introduce confounds in evaluating unit-related reasoning.
- **Datapoint citations:**
  - [D24] Example 9 (main, train, label=28): "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms. The second person lost 7 kilograms less than the first person." — Metric units throughout; inconsistent with grades 3–6 US customary curriculum.

---

#### MINOR

#### Concern 9: Calculator annotation format (`<<expr=result>>`) is invisible to human readers and irrelevant to deployment evaluation
- **Dimension(s):** IF
- **Observation:** All solutions embed calculator annotations in the form `<<expression=result>>` (e.g., `<<30/2=15>>`). These are present in every sampled answer. They serve GSM8K's evaluation mechanism (Python `eval` override) but have no counterpart in student-submitted work or in the deployment's evaluation.
- **Deployment relevance:** Minor formatting noise for any system that processes GSM8K answers; a system trained on or evaluated with GSM8K solutions would need to strip these annotations to avoid learning the annotation format as a feature. Not a fundamental validity concern, but worth noting.
- **Datapoint citations:**
  - [D2] Example 1 (main, train): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards." — Calculator annotation present in every solution line.

#### Concern 10: Annotation inconsistency confirmed in sample (expression label mismatch)
- **Dimension(s):** OC
- **Observation:** Example 12 contains `6*2=<<6+6=12>>12`, where the left side of the annotation uses multiplication (`6*2`) but the expression inside the annotation uses addition (`6+6`). Both yield 12, so the final answer is unaffected, but the annotation itself is internally inconsistent. The paper acknowledges that calculator annotation logic is imperfect [Q117, Q118].
- **Deployment relevance:** Minor issue that does not affect the final-answer label but confirms the paper's caveat about annotation quality. For a deployment that examines intermediate steps, inconsistent intermediate annotations would be problematic; for GSM8K's binary evaluation, it is a minor defect.
- **Datapoint citations:**
  - [D4] Example 12 (main, train, label=78): "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." — Multiplication stated in prose but addition used inside the calculator annotation.

#### Concern 11: Potential logic/arithmetic error in one sampled problem (every-sixth-customer)
- **Dimension(s):** OC
- **Observation:** Example 31 states "every sixth customer gets a free ice cream cone" but the solution divides paying customers by 5 (not 6) to reach the giveaway count: "He sold 50 cones because 100 / 2 = 50; He gave away 10 cones because 50 / 5 = 10." If the problem means 1 in every 6 customers (1 free + 5 paid), dividing by 5 may be intentional; if "every sixth" means one out of every six total customers, the answer should be ≈8. The ambiguity is unresolved and the solution is internally inconsistent with the stated problem.
- **Deployment relevance:** The paper estimates ~1.7% of problems contain breaking errors or ambiguities [Q107, Q108]. This example illustrates that such errors are real and present in the sample. For a deployment that requires reliable ground truth, problem ambiguities of this kind undermine the trustworthiness of the benchmark as a reference.
- **Datapoint citations:**
  - [D22] Example 31 (main, train, label=10): "Dan owns an ice cream shop and every sixth customer gets a free ice cream cone. Cones cost $2 each. If he sold $100 worth of cones, how many free ones did he give away? … He gave away 10 cones because 50 / 5 = <<50/5=10>>10" — "Sixth customer" but ÷5 in solution.

---

### Content Coverage Summary

The 80 sampled examples are uniformly English-prose arithmetic word problems requiring 2–6 sequential operations. The register is professional and fluent throughout — no informal, abbreviated, or student-register language appears anywhere. Problems span a wide range of contexts: childhood activities (candy, toys, pets — Examples 1, 2, 3, 25, 27), sports (Examples 15, 18, 26), adult financial transactions (rent, real estate, car sales — Examples 30, 35, 44), and abstract quantity reasoning (Examples 7, 9, 38). Currency is overwhelmingly USD. Units include feet, pounds, inches (US customary), and one instance of kilograms (metric). The mathematical content ranges from grade-3-appropriate two-step problems (Examples 2, 8, 21, 27) up to algebraic equation solving and simple interest that are outside the grades 3–6 band (Examples 23, 43, 45). No problem requires a unit conversion computation. No solution exhibits informal notation, carry marks, area models, remainder notation, or any student-register feature. Solutions are clean annotated natural language prose with `<<expr=result>>` annotations. The `socratic` config provides the same content with sub-question scaffolding.

---

### Limitations

1. **Sample size.** 80 examples drawn from 7,473 train examples (~1.1%) are insufficient to quantify the frequency of any specific problem type (e.g., unit conversion problems, specific grade-level topics). Absence of a problem type in the sample does not establish its absence in the full dataset.

2. **No test-split sampling.** All examples come from the training split. The test split (1,319 examples) may have different topic or difficulty distributions; the benchmark documentation provides no breakdown by sub-type.

3. **No grade-level metadata.** Without grade-level labels in the data, it is impossible to measure from the sample what fraction of problems falls within grades 3–6 CCSS-M scope. The above-grade-band examples were identified by content inspection, not by a data field.

4. **Common Core phrasing frequency unquantifiable from sample.** Whether "how many more," "how many total," or other flagged CCSS-M phrasings appear at representative rates in the full dataset cannot be determined from 80 examples.

5. **No error-type annotation to inspect.** Because GSM8K contains no error-type labels, it is impossible to evaluate coverage of the deployment's diagnostic taxonomy from the data itself — this gap is structural and cannot be assessed by inspecting more examples.

6. **Calculator annotation correctness not systematically verified.** Only one annotation inconsistency was identified by inspection (D4); a systematic audit of all 8,500 problems' calculator annotations would be needed to quantify the annotation error rate beyond the paper's 1.7% estimate.