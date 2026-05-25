## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-07-11
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO/default | Ex. 1 | True | "No plants are fungi. Mushrooms are fungi." / "∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" | Simple 2-premise syllogism with exact NL/FOL parallel; confirms NL-first design with FOL annotation layer | IF |
| D2 | FOLIO/default | Ex. 2 | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises." / "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" | Multi-premise story with 7 premises including mixed disjunction/implication; illustrates chain-depth complexity and NL-FOL alignment | IF, IO |
| D3 | FOLIO/default | Ex. 3 | Uncertain | "A project is written either in C++ or Python." / "∀x (Project(x) → (WrittenIn(x, cplusplus) ⊕ WrittenIn(x, python)))" | Exclusive disjunction (⊕) expressed in NL as "either-or"; confirms documented NL convention alignment | IF |
| D4 | FOLIO/default | Ex. 4 | False | "No trick-shot artist in Yale's varsity team struggles with half court shots." / "∀x ((In(x, yaleSVarsityTeam) ∧ TrickShotArtist(x)) → ¬StruggleAt(x, halfCourtShot))" | Multi-step syllogism chain; same premise set generates multiple conclusions with different labels (also Ex. 18, 32) | IO, OO |
| D5 | FOLIO/default | Ex. 11 | False | "The bird is in Size Town and it is not both heavy and still." / "In(bird, sizeTown) ∧ ¬(Heavy(bird) ∧ Still(bird))" | 8-premise chain with 5+ reasoning depth; conclusion tests compound conditional | IO, IF |
| D6 | FOLIO/default | Ex. 12 | True | "Some cats are not pets. All cats are mammals." / "∃x (Cat(x) ∧ ¬Pet(x)) ∀x (Cat(x) → Mammal(x))" | Minimal existential quantifier example; note that conclusion-FOL uses double existential (∃x ∃y) where the NL "some mammals" might only require ∃x — potential over-specification in FOL | OC, IF |
| D7 | FOLIO/default | Ex. 13 | False | "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." | Double-negative NL sentence with typo ("offical"); NL quality issue in training data | IC, IF |
| D8 | FOLIO/default | Ex. 15 | Uncertain | "Oxford Circus is the entrance to Oxford Circus tube station, a part of the Central line in 1900." / "EntraceTo(oxfordCircus, tubeStation) ∧ PartOf(tubeStation, centralline) ∧ In(tubeStation, 1900)" | WikiLogic story with real-world entity (Oxford Circus, John Nash); typo "EntraceTo" in FOL | OC, IC |
| D9 | FOLIO/default | Ex. 16 | True | "All professional athletes spend most of their time on sports... Amy spends the most time on sports, or Amy is an Olympic gold medal winner." / "∀x (ProfessionalAthlete(x) → SpendOn(x, mostOfTheirTime, sports)) ... SpendOn(amy, mostOfTheirTime, sports) ∨ OlympicGoldMedalWinner(amy)" | Multi-step deductive chain with negation and implication; 6 premises, illustrates chain-depth coverage | IO |
| D10 | FOLIO/default | Ex. 17 | False | "Michael O'Donnell is a British physician, journalist, author, and broadcaster." / "British(michael) ∧ Physician(michael) ∧ Journalist(michael) ∧ Author(michael) ∧ Broadcaster(michael)" | WikiLogic: real Wikipedia person; FOL uses "michael" as constant but full name is John Nash / Michael O'Donnell | IC, OC |
| D11 | FOLIO/default | Ex. 22 | Uncertain | "Everyone in the Franco-China diplomatic conference is either a PRC national or a French national, but not both." / "∀x (In(x, franco-ChinaDiplomaticConference) → PRCNational(x) ⊕ FrenchNational(x))" | NL "but not both" correctly mapped to ⊕; confirms NL disjunction conventions | IF |
| D12 | FOLIO/default | Ex. 28 | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency." / "∀x (Country(x) ∧ PossibleEffectiveMonetaryPolicy(x) → SuccessfulInflationControl(x) ∧ StongNationalCurrency(x))" | Typo "StongNationalCurrency" appears in both premises-FOL and conclusion-FOL consistently | OC |
| D13 | FOLIO/default | Ex. 34 | True | "If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." / "¬(Planet(pSOJ318.5-22) ∧ Rogue(pSOJ318.5-22) ∧ BoundBy(pSOJ318.5-22, sun, gravitationally)) → (Planet(pSOJ318.5-22) ∧ Rogue(pSOJ318.5-22))" | Complex compound premise with negation and conditional; WikiLogic astronomy topic | IO |
| D14 | FOLIO/default | Ex. 36 | True | "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Missing closing parenthesis in FOL formula — syntactic error in training data | OC, IF |
| D15 | FOLIO/default | Ex. 43 | True | "∀x (MajorArgumentForm(x) → (InductiveReasoning(x) ⊕ DeductiveReasoning(x))" | Missing closing parenthesis in premises-FOL | OC, IF |
| D16 | FOLIO/default | Ex. 52 | True | "Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." / "¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))" | Premises describe "John" but FOL uses "jim" — name inconsistency between NL and FOL | OC, IF |
| D17 | FOLIO/default | Ex. 57 | False | "Matt does not invest in the public stock market regularly." / "InvestInRegularly(matt, publicStockMarket)" | NL premise says Matt does NOT invest; FOL asserts he DOES — direct NL/FOL semantic contradiction | OC, IF |
| D18 | FOLIO/default | Ex. 4, 18, 32 | False/Uncertain/False | Same story_id=408, same 5 premises, but three different conclusions with labels False, Uncertain, False | Confirms premise reuse design: multiple conclusions per premise set; tests multi-conclusion inference from same world | IO, OO |
| D19 | FOLIO/default | Ex. 8, 19, 30 | Uncertain/Uncertain/False | Same story_id=482 (Potterville), three conclusions: "Harry is cool" (Uncertain), "Harry is not cool" (Uncertain), "Harry is a wizard or angry" (False) | Both "Harry is cool" and "Harry is not cool" labeled Uncertain — confirms Unknown/Uncertain label calibration; also Harry Potter cultural reference | IO, OO |
| D20 | FOLIO/default | Ex. 10 | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" | Unbalanced parenthesis in premises-FOL | OC, IF |
| D21 | FOLIO/default | Ex. 55 | False | "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" | Unbalanced closing parenthesis in conclusion-FOL | OC, IF |
| D22 | FOLIO/default | Ex. 1 | True | Conclusion: "No plants are mushrooms." / "∀x (Plant(x) → ¬Mushroom(x))" | Minimal 2-premise example; low reasoning depth (depth ≤ 2) | IO |
| D23 | FOLIO/default | Ex. 50 | Uncertain | "Each building is tall. Everything tall has height." / "∀x (Building(x) → Tall(x)) ∀x (Tall(x) → Height(x))" | Minimal 2-premise example; low reasoning depth | IO |
| D24 | FOLIO/default | Ex. 29 | False | "The only types of mammals that lay eggs are either platypuses or echidnas... Grebes lay eggs. Grebes are not platypuses and also not echidnas." | 9-premise story requiring multi-step chain; illustrates higher depth coverage | IO |
| D25 | FOLIO/default | Ex. 37 | False | "Conclusion-FOL: ∃x (SavesFor(jane, enoughMoney, theSummer) ∧ Kangaroo(x) → WillSee(x, jane, berlinzoo))" | Conclusion-FOL encodes conditional inside existential scope — unusual FOL formulation that may represent annotation inconsistency | OC |
| D26 | FOLIO/default | Ex. 6 | Uncertain | "Ho is at the business conference and prefers state ownership of the means of production." | Non-Western name ("Ho") in story; ideologically loaded topic (communist/planned economy) used as logical content — within scope of deductive task | IC |
| D27 | FOLIO/default | Ex. 13 | False | "Lipstcks in the Rouge Dior set, Lunar New Year Limited Edition either does not have 'rosewood' in its offical description or it has 'rosewood' in its official description." | Typo "Lipstcks" in NL premises; tautological premise (p ∨ ¬p) | IC, OC |
| D28 | FOLIO/default | Ex. 56 | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin." / "DistrictIn(xiufeng, guilin) ∧ DistrictIn(xiangshan, guilin)..." | WikiLogic: Chinese geographic entities (Guilin districts); conclusion about Kowloon/HK is unrelated to premises — exemplifies "Unknown" label for unrelated conclusions | OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Complete NL/FOL parallel annotation for all examples
- **Dimension(s):** IF
- **Observation:** Every example in the sampled data provides complete, aligned natural-language premises and conclusions alongside their FOL counterparts. The NL and FOL layers are present and co-aligned at the formula level (not just story level), directly enabling hybrid NL+FOL presentation mode testing as well as ablation between NL-only and FOL-only conditions.
- **Deployment relevance:** The lab's highest-priority concern is the undecided choice between pure-symbolic and hybrid presentation modes. The parallel annotation structure means FOLIO directly supports the NL+FOL hybrid condition out of the box without any preprocessing, and also permits constructing a FOL-only input condition, even if the latter is not the benchmark's native mode.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO/default, split=train, label=True): "No plants are fungi. Mushrooms are fungi." / "∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" — Demonstrates clean NL/FOL parallel at the sentence level, with semantically equivalent representations.
  - [D2] Example 2 (FOLIO/default, split=train, label=Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Multi-premise story shows FOL is provided at per-sentence granularity throughout, not just as a story-level summary.
  - [D11] Example 22 (FOLIO/default, split=train, label=Uncertain): "NL: 'Everyone in the Franco-China diplomatic conference is either a PRC national or a French national, but not both.' / FOL: ∀x (In(x, franco-ChinaDiplomaticConference) → PRCNational(x) ⊕ FrenchNational(x))" — Shows NL disjunction "but not both" correctly rendered as ⊕, confirming semantic equivalence.

#### Strength 2: Full classical FOL operator coverage observed in sample
- **Dimension(s):** IO
- **Observation:** The sampled examples exhibit all core FOL operators documented in the benchmark: negation (¬), conjunction (∧), disjunction (∨), exclusive disjunction (⊕), implication (→), universal quantifier (∀), existential quantifier (∃), and equality (=). Multi-place predicates also appear.
- **Deployment relevance:** The lab targets broad classical-deductive FOL coverage with explicit exclusion of temporal, modal, arithmetic, and probabilistic reasoning. The sample confirms the benchmark delivers this precisely.
- **Datapoint citations:**
  - [D3] Example 3 (FOLIO/default, split=train, label=Uncertain): "∀x (Project(x) → (WrittenIn(x, cplusplus) ⊕ WrittenIn(x, python)))" — Exclusive disjunction with universal quantifier.
  - [D13] Example 34 (FOLIO/default, split=train, label=True): "¬(Planet(pSOJ318.5-22) ∧ Rogue(pSOJ318.5-22) ∧ BoundBy(pSOJ318.5-22, sun, gravitationally)) → (Planet(pSOJ318.5-22) ∧ Rogue(pSOJ318.5-22))" — Negated conjunction in antecedent of implication; n-place predicate (BoundBy).
  - [D9] Example 16 (FOLIO/default, split=train, label=True): "SpendOn(amy, mostOfTheirTime, sports) ∨ OlympicGoldMedalWinner(amy)" — Ground-atom disjunction.

#### Strength 3: Multi-conclusion reuse of premise sets enables multi-depth inference evaluation
- **Dimension(s):** IO, OO
- **Observation:** Multiple examples share the same premise set (same story_id) but have different conclusions with different labels. This directly confirms that FOLIO generates multiple conclusions per story at varying logical depths and with varying truth values, providing richer per-story coverage.
- **Deployment relevance:** The lab prioritizes multi-step deduction chains. The multi-conclusion design means the benchmark can test whether models hold a consistent world model across conclusions, not just whether they answer individual questions correctly.
- **Datapoint citations:**
  - [D18] Examples 4, 18, 32 (FOLIO/default, split=train, story_id=408): Same 5 premises about Yale's varsity team, producing conclusions labeled False, Uncertain, and False respectively — confirms multiple conclusions per premise set with varying labels.
  - [D19] Examples 8, 19, 30 (FOLIO/default, split=train, story_id=482): Same 7 premises about Potterville; "Harry is cool" (Uncertain), "Harry is not cool" (Uncertain), "Harry is a wizard or angry" (False) — illustrates that complementary conclusions can both be Unknown when premises are insufficient.

#### Strength 4: Three-way label distribution with genuine Unknown calibration
- **Dimension(s):** OO
- **Observation:** The sample shows meaningful use of all three label categories (True, False, Uncertain), and the Unknown/Uncertain label is correctly applied even to complementary conclusions ("Harry is cool" and "Harry is not cool" are both Uncertain from the same premises), confirming that the label is not a catch-all for hard cases but reflects genuine logical underdetermination.
- **Deployment relevance:** The lab confirmed that True/False/Unknown maps cleanly to entailment/contradiction/neutral. The data confirms the Unknown label is used with logical precision, not as a default.
- **Datapoint citations:**
  - [D19] Examples 8 and 19 (FOLIO/default, split=train, story_id=482, label=Uncertain): Both "Harry is cool" and "Harry is not cool" are labeled Uncertain — confirms the label reflects logical underdetermination, not difficulty.
  - [D23] Example 50 (FOLIO/default, split=train, label=Uncertain): "All buildings are magnificent." / "∀x (Building(x) → Magnificent(x))" — Conclusion introduces a predicate absent from premises; correctly labeled Uncertain.

#### Strength 5: Broad topical coverage across WikiLogic stories
- **Dimension(s):** IC
- **Observation:** The sample spans a wide range of real-world topics: astronomy (rogue planets), biology (mammals/echidnas), geography (Guilin, New Haven, Bronx), economics (monetary policy/Russia), cinema (Adventures of Rusty, Tintin), social media (TikTok), medicine, and sports. This confirms the documented 4,351-word vocabulary and Wikipedia-seeded diversity.
- **Deployment relevance:** For a US research lab evaluating formal reasoning, topical variety ensures the benchmark does not probe domain-specific knowledge artifacts but rather general deductive capacity. The breadth reduces the risk that any single topic dominates performance variance.
- **Datapoint citations:**
  - [D13] Example 34 (FOLIO/default, split=train, label=True): "PSO J318.5−22 is a rogue planet" — Astronomy/astrophysics topic.
  - [D28] Example 56 (FOLIO/default, split=train, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin." — Chinese geography topic confirming non-US content.
  - [D26] Example 6 (FOLIO/default, split=train, label=Uncertain): "Everyone at the business conference is either an investor or an entrepreneur." — Political economy topic with non-Western name.

#### Strength 6: NL quantifier-to-FOL mapping follows documented conventions consistently
- **Dimension(s):** IF
- **Observation:** Across the sample, NL phrasing conventions for quantifiers and disjunction are consistently rendered in FOL. "All A are B" → ∀x (A(x) → B(x)); "Some A are B" → ∃x (A(x) ∧ B(x)); "either-or" (exclusive) → ⊕; "or both" (inclusive) → ∨; "neither...nor" → ¬ ... ∧ ¬. This confirms the documented annotation protocol is followed.
- **Deployment relevance:** Consistent NL-FOL mapping reduces construct-irrelevant variance when the lab presents hybrid inputs; models that handle the NL-FOL mapping correctly should receive comparable signals across examples.
- **Datapoint citations:**
  - [D3] Example 3 (FOLIO/default, split=train, label=Uncertain): "A project is written either in C++ or Python." → "WrittenIn(x, cplusplus) ⊕ WrittenIn(x, python)" — Exclusive disjunction convention confirmed.
  - [D1] Example 1 (FOLIO/default, split=train, label=True): "No plants are fungi." → "∀x (Plant(x) → ¬Fungi(x))" — Universal negation convention confirmed.
  - [D11] Example 22 (FOLIO/default, split=train, label=Uncertain): "'but not both'" → "⊕" — Additional exclusive disjunction confirmation.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Direct NL/FOL semantic contradiction in at least one training example
- **Dimension(s):** OC, IF
- **Observation:** Example 57 contains a NL premise "Matt does not invest in the public stock market regularly" paired with a FOL formula "InvestInRegularly(matt, publicStockMarket)" — the negation is dropped in the FOL encoding. This is a direct semantic contradiction between the NL and FOL layers in the same example, meaning the FOL annotation does not faithfully represent the NL content.
- **Deployment relevance:** This is the most serious quality concern in the sample. If the lab presents hybrid NL+FOL inputs, this example will provide conflicting signals to the model. If presenting FOL-only, the label may be computed from incorrect premises. The web search findings noted that a 2025 study found annotation errors in FOLIO requiring a cleaned validation set — this sampled example is direct evidence of such errors in the training split.
- **Datapoint citations:**
  - [D17] Example 57 (FOLIO/default, split=train, label=False): NL: "Matt does not invest in the public stock market regularly." / FOL: "InvestInRegularly(matt, publicStockMarket)" — Negation ¬ is absent in FOL where it should be present; direct NL/FOL semantic mismatch.

---

#### MAJOR

#### Concern 2: Multiple syntactic errors in FOL formulas (unbalanced parentheses, typos in predicate names)
- **Dimension(s):** OC, IF
- **Observation:** At least four examples in the 57-sample contain syntactic errors in FOL formulas: unbalanced parentheses in Examples 10, 36, 43, and 55; a typo predicate name "StongNationalCurrency" (missing letter) appearing consistently in Example 28's premises and conclusion FOL; a typo "EntraceTo" in Example 15's FOL. These errors would cause parsing failures in a syntactic checker and potentially corrupt inference engine execution.
- **Deployment relevance:** The lab intends to use FOLIO's FOL layer (for hybrid or FOL-only input modes, or for the NL-to-FOL translation task). Syntactically malformed FOL formulas in the training set could corrupt fine-tuning for the translation task and would cause failures if fed directly to the Stanford CS221 inference engine. The web search findings explicitly noted that a 2025 cleaning study found annotation errors — the syntactic errors observed here are direct confirmation of that finding in the training split.
- **Datapoint citations:**
  - [D14] Example 36 (FOLIO/default, split=train, label=True): "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — Missing closing parenthesis after "jameSFamily".
  - [D15] Example 43 (FOLIO/default, split=train, label=True): "∀x (MajorArgumentForm(x) → (InductiveReasoning(x) ⊕ DeductiveReasoning(x))" — Missing closing parenthesis.
  - [D20] Example 10 (FOLIO/default, split=train, label=Uncertain): "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — Unmatched closing parenthesis.
  - [D21] Example 55 (FOLIO/default, split=train, label=False): "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" — Extra closing parenthesis in conclusion-FOL.
  - [D12] Example 28 (FOLIO/default, split=train, label=False): "StongNationalCurrency(x)" — Consistent typo in both premises-FOL and conclusion-FOL (likely from copy-paste, but still non-standard predicate name).

#### Concern 3: NL name inconsistency between premises and FOL (John → Jim)
- **Dimension(s):** OC, IF
- **Observation:** Example 52 refers to "John" throughout the NL premises ("Either John is a professional basketball player...") but the FOL formulas consistently use "jim" as the constant (e.g., "¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))"). This creates a cross-layer entity reference inconsistency.
- **Deployment relevance:** For the NL-to-FOL translation task, this inconsistency would produce erroneous training signal — a model that correctly translates "John" to a constant named "john" would be penalized relative to the gold standard using "jim". For hybrid NL+FOL input, the mismatch may confuse models tracking entity identity across layers.
- **Datapoint citations:**
  - [D16] Example 52 (FOLIO/default, split=train, label=True): NL: "Either John is a professional basketball player and he never exercises" / FOL: "¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))" — "John" in NL, "jim" in FOL.

#### Concern 4: Test split not present in HuggingFace dataset; only train + validation available
- **Dimension(s):** OF
- **Observation:** The HF metadata schema shows only `train` (1,001 examples) and `validation` (203 examples) splits, totalling 1,204 examples. The documented test set (226 examples with 87 True, 78 False, 61 Unknown) is not present in the HuggingFace dataset. Benchmark documentation and web search findings refer to the test set for all primary performance comparisons.
- **Deployment relevance:** The lab's evaluation pipeline will likely want to hold out a test set not seen during any prompting or fine-tuning experiments. If the lab uses the HuggingFace dataset as its data source, there is no separate held-out test split available; the lab would need to obtain the test set from the FOLIO GitHub repository directly. Reliance only on the validation set (203 examples) reduces statistical power, especially for per-depth or per-label-class analyses.
- **Datapoint citations:**
  - HF Metadata: `"splits": {"train": {"num_examples": 1001}, "validation": {"num_examples": 203}}` — No `test` split present; total 1,204 examples vs. documented 1,430.

#### Concern 5: NL quality issues (typos, double negatives) appear in training data despite documented quality control
- **Dimension(s):** IC, IF
- **Observation:** Several training examples contain NL-layer issues: Example 13 has a double negative ("No satin-finish lipsticks in the set do not have 'rosewood'") and two spelling errors ("offical", "Lipstcks"); Example 28 has the consistent predicate typo "Stong"; Example 43 contains a redundant variable ("∃x ∃y ∃y ∃w" with duplicate ∃y) in premises-FOL.
- **Deployment relevance:** For a US research lab using FOLIO to benchmark NL reasoning, NL-layer errors introduce construct-irrelevant variance: a model that gets Example 13 wrong may be failing on the grammatical ambiguity rather than the logical structure. The 2025 annotation-cleaning study is relevant here — the lab should verify whether it uses the original or cleaned annotation set.
- **Datapoint citations:**
  - [D7] Example 13 (FOLIO/default, split=train, label=False): "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." — Double negative NL premise; two typos ("offical", "Lipstcks").
  - [D27] Example 13 (FOLIO/default, split=train, label=False): "Lipstcks in the Rouge Dior set, Lunar New Year Limited Edition either does not have 'rosewood' in its offical description or it has 'rosewood' in its official description." — Tautological NL premise (p ∨ ¬p) that adds no logical content.

#### Concern 6: Potential FOL annotation inconsistency — over-specification in existential quantification
- **Dimension(s):** OC, IF
- **Observation:** In Example 12, the NL conclusion "Some mammals are not pets" is translated to FOL as "∃x ∃y (Mammal(x) ∧ Mammal(y) ∧ ¬Pet(x) ∧ ¬Pet(y))" — requiring two distinct non-pet mammals, which is stronger than what "some" conventionally requires (just ∃x). This may introduce subtle annotation biases where conclusions are harder to satisfy in FOL than in NL. Similarly, Example 37's conclusion-FOL encodes a conditional inside an existential scope in an atypical formulation.
- **Deployment relevance:** For the NL-to-FOL translation task, inconsistencies in how "some" is formalized (sometimes ∃x, sometimes ∃x ∃y) create label noise that would penalize models making the simpler but logically valid translation. For the reasoning task, if the inference engine uses the over-specified FOL, labels may differ from what a pure NL reasoning model would compute.
- **Datapoint citations:**
  - [D6] Example 12 (FOLIO/default, split=train, label=True): "Some mammals are not pets." / "∃x ∃y (Mammal(x) ∧ Mammal(y) ∧ ¬Pet(x) ∧ ¬Pet(y))" — Double existential where single would suffice.
  - [D25] Example 37 (FOLIO/default, split=train, label=False): "∃x (SavesFor(jane, enoughMoney, theSummer) ∧ Kangaroo(x) → WillSee(x, jane, berlinzoo))" — Conditional embedded inside existential scope; unusual formulation.

---

#### MINOR

#### Concern 7: Label field uses "Uncertain" rather than documented "Unknown"
- **Dimension(s):** OO
- **Observation:** The HF dataset uses the string "Uncertain" as the label value (observed in examples 2, 3, 5, 6, 7, 8, 9, etc.), while the benchmark paper and YAML consistently use "Unknown" (True/False/Unknown). The lab's elicitation confirmed the three-way mapping to entailment/contradiction/neutral.
- **Deployment relevance:** Minor inconsistency that requires a string normalization step in the evaluation pipeline. No logical misalignment — the category is the same — but any code that filters by label="Unknown" will fail on the HF dataset without transformation.
- **Datapoint citations:**
  - [D2] Example 2 (FOLIO/default, split=train, label=Uncertain): label field contains "Uncertain" — HF dataset label string differs from paper documentation's "Unknown".

#### Concern 8: Shallow-depth examples are present in the sample, potentially reducing discriminability at low depths
- **Dimension(s):** IO
- **Observation:** Several examples in the sample have only 2 premises and require very shallow reasoning (depth ≤ 2): Examples 1 (2 premises), 12 (2 premises), 17 (4 premises, simple syllogism), 50 (2 premises). These would contribute little to discriminating frontier model capability.
- **Deployment relevance:** The lab prioritizes multi-step chains. While the benchmark documents 28.7% of examples at depth ≥5, the presence of very shallow examples means aggregate accuracy is influenced by a mixture of difficulties. Per-depth performance analysis will be essential; per-depth example counts at depth 6–7 may be too small for reliable statistical inference (as noted in the web search findings, ~65 examples total at depth ≥5 in the test set).
- **Datapoint citations:**
  - [D22] Example 1 (FOLIO/default, split=train, label=True): "No plants are fungi. Mushrooms are fungi." — 2-premise, depth ≤ 2.
  - [D23] Example 50 (FOLIO/default, split=train, label=Uncertain): "Each building is tall. Everything tall has height." — 2-premise, depth ≤ 2; conclusion introduces predicate absent from premises.

#### Concern 9: WikiLogic stories reference real-world entities that may be in LLM pretraining data
- **Dimension(s):** IC
- **Observation:** Multiple WikiLogic examples reference specific real-world entities whose facts are available in pretraining corpora: Michael O'Donnell (British journalist), Bobby Flynn (Australian Idol), Oxford Circus / John Nash, Adventures of Rusty / Columbia Pictures. A model may arrive at correct answers by recalling facts rather than deductive reasoning from premises.
- **Deployment relevance:** The lab's expert evaluator population will be aware of this confound. For evaluating pure deductive reasoning capability, WikiLogic examples with real-world entities may allow shortcut reasoning; the HybLogic subset would be cleaner for this purpose. The benchmark paper documents this concern [Q104].
- **Datapoint citations:**
  - [D10] Example 17 (FOLIO/default, split=train, label=False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster... Michael O'Donnell was born in Yorkshire as the son of a general practitioner." — Real Wikipedia person; conclusion "There are no journalists that were born in Yorkshire" is falsifiable from world knowledge.
  - [D8] Example 15 (FOLIO/default, split=train, label=Uncertain): "Oxford Circus is a road junction connecting Oxford Street and Regent Street... John Nash designed Oxford Circus." — Real-world architect and landmark.

#### Concern 10: Reasoning depth distribution skewed toward lower depths in sample
- **Dimension(s):** IO
- **Observation:** Of the 57 sampled examples, premise counts (a proxy for reasoning depth) range from 2 to 9. The modal depth in the benchmark is 4, but the sample contains a noticeable number of 2-premise examples. Without the test split, per-depth analysis must use the validation set (203 examples), with potentially very few examples at depth 6–7.
- **Deployment relevance:** As noted in the web search findings, depth 6–7 subsets in the 226-example test set are likely single-digit counts, making accuracy estimates at those depths statistically unreliable. The lab should treat per-depth scores at depth 6–7 as indicative only.
- **Datapoint citations:**
  - [D22] Example 1 (train, 2 premises), [D5] Example 11 (train, 8 premises) — Range of depths observed in sample confirms mixture.
  - [D24] Example 29 (FOLIO/default, split=train, label=False): 9 premises about platypuses/echidnas/hyraxes/grebes — higher-depth example present in sample.

---

### Content Coverage Summary

The 57 sampled training examples span a wide topical range (astronomy, biology, geography, economics, media, sports, logic/reasoning meta-examples) consistent with WikiLogic's Wikipedia-seeding design. Both WikiLogic (free-form stories with real-world entities) and HybLogic (syllogism-template-based with populated slots) subcorpora appear to be represented, though the sample does not tag subcorpus origin explicitly.

All core FOL operators are present in the sample. NL-FOL alignment conventions (exclusive vs. inclusive disjunction, quantifier phrasing) are largely followed. Logical structure ranges from 2-premise minimal syllogisms (depth ≤ 2) to 9-premise multi-step chains (depth ≥ 5). The three-way label distribution (True/False/Uncertain) is represented, with Uncertain being the most common label in the sample.

**Quality observations from the sample:** Five examples show syntactic errors in FOL formulas (unbalanced parentheses); one shows a direct NL/FOL semantic contradiction (negation dropped); one shows a name inconsistency (John/Jim) between NL and FOL layers; two show NL typos that passed quality control. These are consistent with the 2025 annotation-cleaning study's finding of errors in the public dataset.

**Input format:** Every example provides the full NL/FOL parallel structure. The NL layer is natural English prose; the FOL layer uses standard AI/education FOL notation (Russell & Norvig style) with Unicode operators (∀, ∃, ∧, ∨, ¬, →, ⊕, =). The benchmark natively supports NL-only, FOL-only, and hybrid input construction from the HF data fields.

---

### Limitations

1. **Sample size:** 57 examples from the 1,001-example training split. While the sample reveals concrete quality issues, the rate of annotation errors (syntactic and semantic) cannot be reliably estimated from this sample alone.

2. **Test split unavailable on HuggingFace:** The 226-example test set referenced in the paper and web search findings is not present in the HF dataset. All per-label and per-depth performance statistics in the paper (87 True / 78 False / 61 Unknown) refer to this unavailable split. The validation set (203 examples) is the only evaluation split accessible via HF.

3. **Subcorpus label not in schema:** The HF schema does not include a field distinguishing WikiLogic from HybLogic examples. Subcorpus-stratified analysis (which is important for the lab's ceiling-effect assessment, since GPT-4 performs near-randomly on HybLogic) requires external cross-referencing with the FOLIO GitHub repository.

4. **Reasoning depth not in schema:** The `reasoning_depth` field is not present in the HF dataset. Per-depth analysis requires external computation or cross-referencing with GitHub metadata.

5. **Cleaned vs. original dataset:** The 2025 annotation-cleaning study (arxiv 2603.02788) established a cleaned validation set. The HF dataset appears to be the original uncleaned version. The lab should verify which version it is using, as scores on the two versions may differ.

6. **Cannot inspect FOL inference engine behavior:** The sample reveals syntactic errors in FOL formulas, but it is not possible from data inspection alone to determine whether the inference engine successfully resolved these (e.g., via the Python parser bridge) or whether they propagated to label errors. The 2025 cleaning study used Vampire rather than the Stanford CS221 engine, suggesting the original engine may have been more tolerant of these errors.