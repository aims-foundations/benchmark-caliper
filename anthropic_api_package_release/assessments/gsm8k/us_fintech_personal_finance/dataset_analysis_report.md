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
| D1 | main | 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | Multi-step counting problem with no financial domain content | IO |
| D2 | main | 19 | 54 | "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" | Percentage growth applied to toy cars — not compound interest | IO |
| D3 | main | 43 | 720 | "Ariella has $200 more in her son's saving account than Daniella has in her son's savings account. Ariella's account earns her simple interest at the rate of 10% per annum. If Daniella has $400, how much money will Arialla have after two years?" | Simple interest problem — uses savings account framing but applies flat annual rate, not compound | IC, IO |
| D4 | main | 43 | 720 | "In the second year, she earns the same amount of interest, which $60 + $60 = $120" | Answer treats the second year interest as identical to year one — confirming this is simple interest, not compound | OO, OC |
| D5 | main | 30 | 7200 | "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples because she was at fault in an accident." | Personal budgeting scenario — percentage increases on fixed monthly expenses | IO, IC |
| D6 | main | 44 | 11000 | "James decides to replace his car. He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value. How much was he out of pocket?" | Car resale/purchase — percentage of face value, single-step arithmetic | IO |
| D7 | main | 35 | 333200 | "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" | Real estate price calculation — multiplication of unit price by area | IO |
| D8 | main | 13 | 1825 | "Sally and Bob have made plans to go on a trip at the end of the year. They both decide to work as babysitters and save half of what they've earned for their trip. If Sally makes $6 per day and Bob makes $4 per day, how much money will they both have saved for their trip after a year?" | Simple daily savings with no interest; savings framing but no financial instrument | IO, IC |
| D9 | main | 45 | 120 | "Ten friends decide to get an end-of-year gift for their teacher. They plan to split the cost of the gift equally. But four of the group drop out. The remaining friends split the cost equally among themselves. If each share is now $8 more, how much does the gift cost, in dollars?" | Algebraic bill-splitting — the closest GSM8K analog to the deployment's "bill splitting" use case | IO |
| D10 | main | 39 | 20 | "Ian won $100 in the lottery. He decided to use the money to pay off debts. He paid $20 to Colin. He then paid twice as much to Helen, as he had paid to Colin. Then finally, he paid half as much to Benedict, as he had paid to Helen. How much money, in dollars, does he have left after paying off debts?" | Debt-payment problem — uses "debts" vocabulary but involves no interest, APR, or balance computations | IC |
| D11 | main | 23 | 220 | "Jim collects model cars, and he has 301 models total. Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys. How many Buicks does Jim have?" | Multi-variable algebraic word problem — no financial content | IO |
| D12 | main | 7 | 90 | "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle. How many more days are left until all the food runs out?" | Rate/ratio problem — requires proportional reasoning across changing quantities | IO |
| D13 | main | 6 | 54 | "Nancy is filling an aquarium for her fish...If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" | Volume + fraction chaining — geometry-based multi-step | IO |
| D14 | main | 3 | 99 | "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag. How much did the unicorn piñata and the treats cost altogether?" | Grocery/party supply addition — simplest form of monetary arithmetic | IO |
| D15 | socratic | 19 | 54 | "How many new cars will Bobby acquire in the first year? ** In the first year, Bobby will acquire 16 * .5 = <<16*.5=8>>8 new cars. ... How many cars will Bobby have after the third year? ** After the third year, he will have 36 + 18 = <<36+18=54>>54 cars in total." | Socratic format decomposes growth steps but each year is computed from prior year's total — additive not exponential framing | IF, OO |
| D16 | main | 22 | 80 | "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change. How much did Austin start with?" | Retail transaction with tax and change — closest analog to everyday consumer arithmetic with dollar amounts | IO |
| D17 | main | 32 | 2290 | "Daniel has a collection of 346 video games. 80 of them, Daniel bought for $12 each. Of the rest, 50% were bought for $7. All others had a price of $3 each. How much did Daniel spend on all the games in his collection?" | Multi-tier cost calculation with percentages — 3-step monetary reasoning | IO |
| D18 | main | 38 | 90 | "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys, how many will she remain with?" | Ratio-based partition problem — abstract currency-free | IO |
| D19 | main | 20 | 138 | "One pie costs $4 for a piece. Each pie is having 3 pieces. During one hour the bakery can make 12 pies. Creating one pie costs the bakery $0.5. Considering the bakery would be able to sell all pie pieces, how much money would it make?" | Bakery profit calculation — revenue minus cost | IO |
| D20 | socratic | 23 | 220 | "Define a variable ** Let x represent the number of Chevys ... Combine like terms ** 11x+15=301 ... Divide by 11 ** x=<<26=26>>26" | Socratic config adds explicit algebraic reasoning sub-steps — useful for evaluating chain-of-thought decomposition | IF |
| D21 | main | 43 | 720 | "Ariella's account earns her simple interest at the rate of 10% per annum" | Explicit "simple interest" label — benchmark treats this as equivalent in difficulty to non-financial problems, but distinguishes from compound | OO, IC |
| D22 | main | 2 | 9 | "Anna baked 60 cupcakes. She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes. How many cupcakes does she have left?" | Fraction subtraction — everyday context, zero financial domain content | IO |
| D23 | main | 28 | 40 | "A company has 200 employees. 60% of the employees drive to work. Of the employees who don't drive to work, half take public transportation. How many more employees drive to work than take public transportation?" | Percentage partition — applied to commuting, not finance | IO |
| D24 | main | 31 | 10 | "Dan owns an ice cream shop and every sixth customer gets a free ice cream cone. Cones cost $2 each. If he sold $100 worth of cones, how many free ones did he give away?" | Simple division with a promotional rule — monetary context but trivial | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-step arithmetic with traceable natural-language reasoning chains
- **Dimension(s):** IO, IF
- **Observation:** The benchmark consistently demands 3–6 sequential arithmetic operations expressed in coherent natural language before arriving at a final answer. The `main` config shows step-by-step solutions embedded inline with calculator annotations; the `socratic` config decomposes the same problems into explicit sub-questions. Both formats confirm the chain-of-thought requirement documented in the paper.
- **Deployment relevance:** The deployment requires a chatbot that can walk users through multi-step finance calculations (e.g., tracking a payoff timeline month by month). GSM8K exercises the structural skill of multi-step traceable reasoning, even though the content domain differs. A model that scores well must produce coherent intermediate steps, not just final answers.
- **Datapoint citations:**
  - [D17] Example 32 (main, train, label=2290): "On 80 games, Daniel spend 80 games * $12/game = $960. The rest of the collection is 346 games - 80 games = 266 games. 50% of these games means 50/100 * 266 games = 133 games..." — Three-tier cost computation requiring sequential sub-totals before a final sum.
  - [D12] Example 7 (main, train, label=90): "After 30 days, there will be enough food left to sustain 300 people for 90 days – 30 days = 60 days... The 200 people will eat 200/300 = 2/3 as much food... The 60 days' worth of food will last this smaller group for 60 days / (2/3) = 90 more days." — Rate-ratio chaining requiring proportion manipulation across multiple steps.

#### Strength 2: Socratic sub-question decomposition format
- **Dimension(s):** IF, OF
- **Observation:** The `socratic` config reformats every problem so that each sub-step is explicitly prefaced by a natural-language sub-question, then answered. This structure provides a finer-grained window into whether a model's intermediate reasoning is correct, not just its final answer.
- **Deployment relevance:** For a fintech chatbot where reasoning transparency is a CFPB-relevant concern, the socratic format offers an evaluation scaffold that better mirrors the "show your work" expectation. It provides a basis for step-level correctness scoring that is closer to what the deployment needs than the flat main-format evaluation.
- **Datapoint citations:**
  - [D20] Example 23 (socratic, train, label=220): "Define a variable ** Let x represent the number of Chevys ... Combine like terms ** 11x+15=301 ... Divide by 11 ** x=26" — Algebraic reasoning decomposed into named sub-operations, enabling step-level verification.
  - [D15] Example 19 (socratic, train, label=54): "How many new cars will Bobby acquire in the first year? ** In the first year, Bobby will acquire 16 * .5 = 8 new cars. ... How many cars will Bobby have after the third year? ** After the third year, he will have 36 + 18 = 54 cars in total." — Growth-over-time problem decomposed into per-period steps, structurally parallel to how one might verify a compound-interest accumulation calculation period by period.

#### Strength 3: Monetary arithmetic with dollar amounts and percentages
- **Dimension(s):** IO, IC
- **Observation:** A meaningful subset of the sampled problems use dollar amounts, percentages, and consumer-purchase framing. These problems require correct handling of decimal arithmetic, percentage-to-decimal conversion, and multi-item totaling — skills that are prerequisite for any financial reasoning task.
- **Deployment relevance:** The deployment's simpler query tier (bill splitting, expense totaling, percentage-based budgeting) uses the same arithmetic primitives tested in these problems. A model that fails on GSM8K dollar-amount problems would almost certainly fail on the chatbot's simpler tasks.
- **Datapoint citations:**
  - [D16] Example 22 (main, train, label=80): "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change. How much did Austin start with?" — Retail transaction with tax and change arithmetic.
  - [D5] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%, food costs increase by 50%... How much more does Jessica pay for her expenses over the whole year compared to last year?" — Monthly budget with percentage increases annualized.
  - [D6] Example 44 (main, train, label=11000): "He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value. How much was he out of pocket?" — Two-transaction net cost computation.

#### Strength 4: Inline calculator annotations confirm arithmetic execution traceability
- **Dimension(s):** IF, OF
- **Observation:** Every arithmetic operation in the answer string is annotated with a `<<expression=result>>` inline tag (e.g., `<<30/2=15>>`, `<<9*4=36>>`). This annotation convention provides machine-verifiable intermediate computation traces alongside natural language.
- **Deployment relevance:** The deployment needs a model that can be verified at the arithmetic level, not just at the final answer. The annotation format provides a template for building similar verification infrastructure over financial reasoning answers, and its presence in all 80 sampled examples confirms consistent coverage.
- **Datapoint citations:**
  - [D14] Example 3 (main, train, label=99): "The four bags of Reese's cost $9 x 4 = $<<9*4=36>>36. The three bags of Snickers cost $5 x 3 = $<<5*3=15>>15." — Each arithmetic step tagged independently, enabling automated step verification.
  - [D9] Example 45 (main, train, label=120): "10N=6(N+8) ... 4N=48 ... N=<<12=12>>12 ... the present costs 10*12=<<10*12=120>>120." — Algebraic solution with all numeric derivations annotated.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of financial-instrument problem types
- **Dimension(s):** IO
- **Observation:** Across all 80 sampled examples, zero problems involve compound interest, APR, amortization, credit card payoff timelines, minimum payment calculations, credit utilization ratios, or balance transfer computations. The closest financial-domain example is a simple interest problem (Example 43) that explicitly labels itself "simple interest" and applies a flat annual rate rather than compounding. All other monetary problems involve one-time retail purchases, salary/savings accumulation without interest, or abstract cost allocation.
- **Deployment relevance:** The deployment team confirmed that 40–50% of expected queries involve APR, compound interest, amortization, and payoff timelines — described as the product's core value proposition. The benchmark provides zero signal on the model's ability to perform these computations. A model that achieves high GSM8K accuracy could still fail entirely on the deployment's defining query types.
- **Datapoint citations:**
  - [D3] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum. If Daniella has $400, how much money will Arialla have after two years?" — The only savings/interest problem in the sample; explicitly "simple interest," not compound.
  - [D4] Example 43 (main, train, label=720): "In the second year, she earns the same amount of interest, which $60 + $60 = $120" — Second-year interest is identical to first year — confirming flat-rate simple interest; compound interest would yield $66 in year two (10% of $660), making this structurally different from a real savings account.
  - [D1] Example 1 (main, train, label=32): "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them." — Representative of the modal problem type: no monetary content whatsoever.
  - [D8] Example 13 (main, train, label=1825): "They both decide to work as babysitters and save half of what they've earned for their trip. If Sally makes $6 per day... how much money will they both have saved... after a year?" — Savings accumulation with zero interest — no financial instrument logic.

#### CRITICAL Concern 2: No financial terminology — complete semantic grounding gap
- **Dimension(s):** IC
- **Observation:** Across all 80 sampled examples, no problem uses the terms APR, annual percentage rate, compound interest, credit card, minimum payment, balance transfer, credit utilization, amortization, or any related consumer finance vocabulary. All monetary problems use colloquial consumer-purchase framing (candy, robots, shoes, bakery goods, car purchase at a discount). No problem requires a model to parse a financial term and map it to a mathematical operation.
- **Deployment relevance:** The deployment team identified financial terminology handling as essential and named the misinterpretation of APR as a flat rate as "a serious failure mode even when the arithmetic itself is trivial." GSM8K does not test this construct at all. A model could achieve perfect GSM8K performance while having no ability to correctly interpret "APR" or "minimum payment" in a user query.
- **Datapoint citations:**
  - [D10] Example 39 (main, train, label=20): "Ian won $100 in the lottery. He decided to use the money to pay off debts. He paid $20 to Colin." — Uses "debts" as a plain word but involves no interest, no schedule, no rate — pure arithmetic subtraction.
  - [D5] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%..." — Personal budget language but zero financial instrument vocabulary; the arithmetic is percentage application to fixed costs.
  - [D7] Example 35 (main, train, label=333200): "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft..." — Real estate multiplication; no mortgage, interest rate, or amortization content.

#### CRITICAL Concern 3: Binary exact-match scoring is structurally misaligned with assumption-sensitive financial queries
- **Dimension(s):** OO
- **Observation:** All 80 sampled problems have a single unambiguous correct integer or decimal answer, and the answer field terminates with a `#### N` final-answer marker that is compared by exact match. There is no mechanism in the dataset for range-based answers, tolerance bands, or assumption-pinned variants. Even the one interest problem (Example 43) has a single correct answer because the problem explicitly pins the interest type as "simple."
- **Deployment relevance:** The deployment team confirmed that a meaningful fraction of target queries (credit card payoff timelines, effective vs. nominal APR comparisons, amortization total interest) have legitimate answer ranges depending on compounding frequency, issuer minimum payment formulas, and assumed timing conventions. Evaluating a chatbot on such queries using GSM8K's binary scoring scheme would penalize correct answers that use different but valid assumptions, and reward numerically matching but reasoning-flawed answers.
- **Datapoint citations:**
  - [D4] Example 43 (main, train, label=720): "In the second year, she earns the same amount of interest, which $60 + $60 = $120 ... #### 720" — Single labeled answer; if this were compound interest, the correct answer would be $726, and neither answer would be accepted under the other's label.
  - [D9] Example 45 (main, train, label=120): "Let N be the original price each friend was going to pay. 10N=6(N+8) ... #### 120" — Algebraic problem with one exact solution; illustrates the scoring schema's assumption that each well-posed problem has exactly one correct numeric answer.
  - [D2] Example 19 (main, train, label=54): "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" — Growth problem stated additively rather than as compound growth; the single answer 54 would be wrong if interpreted as exponential compounding (which would yield the same result here coincidentally, but the method differs significantly for financial instruments where compounding convention matters).

---

#### MAJOR

#### MAJOR Concern 4: Difficulty ceiling — grade-school arithmetic does not proxy financial instrument complexity
- **Dimension(s):** IO
- **Observation:** The arithmetic operations present in the sampled problems are: addition, subtraction, multiplication, division, simple percentage application, basic ratios, and single-variable algebra. The hardest sampled problem (Example 23, car collection algebra) requires solving a two-variable linear equation. No problem requires iterative computation across multiple periods, recursive formula application, or manipulation of annuity formulas.
- **Deployment relevance:** Multi-month amortization, compound interest over years, and break-even analysis on balance transfers require iterative application of financial formulas that exceed grade-school arithmetic by structural complexity, not just magnitude. A model that achieves 80%+ on GSM8K may still fail on the deployment's hardest queries (amortization over 360 months, effective APR computation) because those queries demand different reasoning patterns entirely, not just harder arithmetic.
- **Datapoint citations:**
  - [D2] Example 19 (main, train, label=54): "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" — Year-over-year growth computed by iterating 3 times; a full amortization schedule would require 360 iterations with changing principal — a categorically different computational demand.
  - [D11] Example 23 (main, train, label=220): "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys. How many Buicks does Jim have?" — Most algebraically complex sampled problem; single-variable linear equation, far below the complexity of compound interest or loan amortization formulas.
  - [D3] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum... how much money will Arialla have after two years?" — Only two periods computed; compound interest over 10 or 30 years would require a formula (P(1+r)^n) rather than repeated addition — a structural leap.

#### MAJOR Concern 5: No signal on financial context disambiguation
- **Dimension(s):** IC
- **Observation:** In the sampled problems, all quantities are fully specified numerically in the problem statement. No problem requires a model to recognize that a described quantity maps to a specific financial formula, to disambiguate between nominal and effective rates, or to identify when a stated rate implies a particular compounding convention. The problems that use percentages always state them as direct multipliers applied once.
- **Deployment relevance:** In the deployment, users will phrase queries like "my APR is 24%, how long to pay off $3,000 if I pay $100/month?" — requiring the model to (a) recognize that APR implies monthly periodic rate = APR/12, (b) apply a loan payoff formula, and (c) handle the iterative nature of the calculation. GSM8K trains no part of this disambiguation and formula-selection reasoning.
- **Datapoint citations:**
  - [D5] Example 30 (main, train, label=7200): "This year her rent goes up by 30%... $1000 * .3 = $300" — Percentage applied as a direct multiplier to a single base; no periodic compounding, no formula selection, no disambiguation of rate type.
  - [D6] Example 44 (main, train, label=11000): "He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value." — Percentage-of-face-value calculation; the rate type is unambiguous and the operation is a single multiplication.
  - [D21] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum" — The problem explicitly labels the rate type ("simple interest"), removing the disambiguation challenge that real financial queries present.

---

#### MINOR

#### MINOR Concern 6: Socratic config growth-problem framing is additive, not exponential
- **Dimension(s):** IF, OO
- **Observation:** Example 19 in the socratic config (50% annual growth in toy cars) is computed by iterating addition: new cars = prior_total × 0.5, then added to prior total. While mathematically equivalent for this 3-year problem, the framing trains a model to approach growth problems additively rather than through the compound formula P(1+r)^n. For a financial chatbot, this framing could reinforce the incorrect "multiply then add" approach that leads to errors on longer time horizons.
- **Deployment relevance:** Minor: the difference is negligible for small n and the benchmark makes no claim to teach formula selection. But it is a concrete signal that the benchmark's implicit pedagogy may not transfer to financial instrument reasoning, even for problems that superficially resemble growth scenarios.
- **Datapoint citations:**
  - [D15] Example 19 (socratic, train, label=54): "How many new cars will Bobby acquire in the first year? ** In the first year, Bobby will acquire 16 * .5 = 8 new cars. ... After the third year, he will have 36 + 18 = 54 cars in total." — Step-by-step addition of new cars per period rather than formula application; same pattern would diverge from correct answers at year 10+ under compound vs. simple growth interpretation.

#### MINOR Concern 7: Dollar-amount problems use simplified tax and pricing conventions
- **Dimension(s):** IC
- **Observation:** The monetary problems in the sample use simple dollar amounts and do not reflect US tax conventions (sales tax, income tax withholding), APY vs. APR distinctions, or any financial regulatory context. Tax appears once (Example 22) as a flat dollar add-on with no percentage derivation. Prices are always whole dollars or simple decimals; no problem involves interest accrual, fees, or conditional charges.
- **Deployment relevance:** Minor, since the benchmark does not claim to test tax or regulatory knowledge. However, it means the benchmark's monetary vocabulary provides no scaffolding for a model that needs to handle real US financial product pricing conventions (e.g., balance transfer fees as a percentage of transferred balance, or daily periodic rate derived from APR).
- **Datapoint citations:**
  - [D16] Example 22 (main, train, label=80): "He was charged $7.22 total for tax." — Tax appears as a pre-computed lump sum, not as a rate applied to a base; no percentage derivation required.
  - [D14] Example 3 (main, train, label=99): "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." — Consumer purchase at stated unit prices; no sales tax, no discount structure, no conditional fee.

---

### Content Coverage Summary

The 80 sampled examples confirm that GSM8K is uniformly composed of grade-school arithmetic word problems set in everyday consumer, school, sports, and household contexts. Problem domains include: food and candy purchases (Examples 2, 3, 25), sports scoring (Example 18), animals and pets (Examples 12, 36), retail and toy purchases (Examples 16, 22, 32), travel and time (Examples 7, 15, 26, 40), simple budgeting (Examples 13, 30), and one explicit savings/interest problem (Example 43, simple interest only). Monetary quantities appear in roughly 40–50% of sampled problems, but invariably as simple multiplicative or additive computations without financial-instrument logic.

The language register is plain American English at approximately a 5th–8th grade reading level, with proper names drawn from a diverse set (Kantana, Omi, Ariella, Amalie), consistent with the documented linguistic diversity goal. All arithmetic annotations use the `<<expr=result>>` inline format and all answers terminate with `#### N`. The socratic config adds sub-question scaffolding to the same problem set, providing a finer-grained reasoning trace.

No example in the sample involves APR, compound interest, amortization, credit cards, minimum payments, balance transfers, credit utilization, or any other consumer finance instrument. The one interest-bearing problem (Example 43) uses simple interest with explicit problem-statement labeling, providing no information about a model's ability to handle compound interest or financial-term disambiguation.

---

### Limitations

1. **Sample size and distribution**: 80 examples from 7,473 training examples represent ~1% of the training set. It is possible — though unlikely given the documented scope — that financial-instrument problems exist elsewhere in the corpus; the sample cannot rule this out with certainty.

2. **Test split not sampled**: All examples are from the training split. If the test split contains categorically different problem types (e.g., more financial-adjacent content), this analysis would not capture that. Given the benchmark's design principles, this is unlikely, but unverifiable from the current sample.

3. **Scoring infrastructure not inspectable**: The `<<expr=result>>` annotation format is visible in the data, but the actual evaluation harness (Python `eval` override at test time, calculator bug behavior) is not inspectable from the HF dataset alone. The paper's documented ~1% performance impact from calculator bugs cannot be confirmed from the data.

4. **Annotator demographics unverifiable**: No annotator metadata is present in the HF dataset or dataset card. Claims about Upwork/Surge AI contractor provenance cannot be verified from the data itself.

5. **Socratic config structural identity**: The socratic config appears to be a reformatted version of the same underlying problems as the main config (all 33 socratic examples match the first 33 main examples). This limits the diversity contribution of the second config for coverage assessment.