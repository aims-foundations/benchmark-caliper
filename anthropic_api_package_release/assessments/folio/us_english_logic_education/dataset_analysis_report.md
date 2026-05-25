## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-07-14
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO/train | Ex. 1 | True | "No plants are fungi. Mushrooms are fungi. / ∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" | Simple 2-premise syllogism with parallel NL and FOL | IO, IC |
| D2 | FOLIO/train | Ex. 2 | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises… Mike works in this tech company. If Mike is not a person who wears the same flannel shirts every day, has very high energy, and is impulsive, then Mike either is very consistent and enjoys sticking to his regular routines or does not like surprises." | Multi-premise story (7 premises) about a tech company worker; complex conditional | IO, IC |
| D3 | FOLIO/train | Ex. 3 | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac. If a song is not titled 'Perfect,' Sam will never play it." | Multi-step chain mixing disjunction, implication, and named individual | IO |
| D4 | FOLIO/train | Ex. 4 | False | "No trick-shot artist in Yale's varsity team struggles with half court shots. Everyone on Yale's varsity team is someone who struggles with half court shots or who successfully shoots a high percentage of 3-pointers." — "Jack is bad at mid-range shots." | Basketball sports story requiring 4+ step chain | IO, IC |
| D5 | FOLIO/train | Ex. 5 | Uncertain | "All Yale students at the event are college students. Everyone at the event is a Yale student or a Harvard student. If Susan is a Yale student, then she does not like independence." | Classic university-setting syllogism with exclusive disjunction | IO |
| D6 | FOLIO/train | Ex. 6 | Uncertain | "All entrepreneurs at the business conference enjoy the opportunity of starting a business. Everyone at the business conference who is an ardent communist prefers state ownership of the means of production. Ho is at the business conference and prefers state ownership of the means of production." | Politically framed scenario with communist/investor dichotomy | IC, OC |
| D7 | FOLIO/train | Ex. 7 | Uncertain | "Andy Chang directed EndGame. Andy Chang is from Hong Kong." — conclusion: "All of Andy Chang's movies are filmed outside of Washington." | Wikipedia-seeded story about a real-world film director from Hong Kong | IC |
| D8 | FOLIO/train | Ex. 8 | Uncertain | "Every person in Potterville that knows magic flies. All wizards in Potterville know magic. Harry, who lives in Potterville either yells or flies." | Fictional Potterville scenario referencing Harry/Potter (Harry Potter allusion) | IC |
| D9 | FOLIO/train | Ex. 11 | False | "Everything in Size Town is big or small. All big things in Size Town are heavy… The bird is in Size Town and it is not both heavy and still." — conclusion: "If the bird is small or still, then it is either unpredictable or changing." | Purely abstract Size Town scenario — no real-world content | IC |
| D10 | FOLIO/train | Ex. 12 | True | "Some cats are not pets. All cats are mammals." — conclusion FOL: "∃x ∃y (Mammal(x) ∧ Mammal(y) ∧ ¬Pet(x) ∧ ¬Pet(y))" | Simple existential syllogism; conclusion FOL is strictly stronger than needed | OC, OO |
| D11 | FOLIO/train | Ex. 13 | False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable… ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Real-world brand story about a specific luxury cosmetics product | IC |
| D12 | FOLIO/train | Ex. 15 | Uncertain | "John Nash designed Oxford Circus. John Nash is a British architect. Oxford Circus is the entrance to Oxford Circus tube station, a part of the Central line in 1900." | Wikipedia-seeded story about real architect John Nash | IC |
| D13 | FOLIO/train | Ex. 16 | True | "All Olympic gold medal winners are professional athletes. All Nobel physics laureates are full-time scientists. Amy spends the most time on sports, or Amy is an Olympic gold medal winner. If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Multi-step chain combining disjunction, contrapositive, complex reasoning | IO |
| D14 | FOLIO/train | Ex. 17 | False | "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire" — conclusion: "There are no journalists that were born in Yorkshire." | Simple false universal overgeneralization from a positive instance | OO |
| D15 | FOLIO/train | Ex. 21 | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing… Clyde is a professor who takes a historical approach." | Complex 6-premise story about cultural interests and academic roles | IO |
| D16 | FOLIO/train | Ex. 22 | Uncertain | "All PRC nationals are entitled to national social insurance coverage. Everyone in the Franco-China diplomatic conference is either a PRC national or a French national, but not both… Either Mei is a North Korean and can have medical bills partially covered, or neither is true." | Geopolitical scenario involving PRC, France, North Korea nationals | IC |
| D17 | FOLIO/train | Ex. 23 | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus." — conclusion: "There exists a SpaceX commercial aircraft." | Real-world entities (Boeing, Airbus, SpaceX) in an Uncertain-labeled example | IC, OC |
| D18 | FOLIO/train | Ex. 27 | Uncertain | "Bobby Flynn finished 7th while competing on Australian Idol. Australian Idol competitors are Australian citizens." — conclusion: "Bobby Flynn flew to America in 2007." | Wikipedia-seeded story about Australian musician | IC |
| D19 | FOLIO/train | Ex. 28 | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. There is an embargo on Russian foreign trade goods." — conclusion: "In Russia, an effective monetary policy is possible." | Real-world geopolitical/economic scenario involving Russia and embargos | IC, OC |
| D20 | FOLIO/train | Ex. 33 | Uncertain | "No battery-powered watch is automatic. All digital watches are battery-powered. Moonwatch is either a digital watch and an automatic, or it is neither." | Classic syllogistic chain about watches | IO |
| D21 | FOLIO/train | Ex. 34 | True | "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." | Scientific Wikipedia-seeded story about astronomy | IC |
| D22 | FOLIO/train | Ex. 43 | True | "All inductive reasoning processes derive general principles from a body of observations. Modus Ponens is not both used in inductive reasoning and used for statistical generalization. Modus Ponens is a component of a major part of reasoning rule." | Story explicitly about Modus Ponens and inductive/deductive reasoning | IC, IO |
| D23 | FOLIO/train | Ex. 52 | True | "No athletes never exercise. All professional basketball players are athletes… Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." — NOTE: FOL annotation says "jim" while NL says "John" | Annotation inconsistency: NL uses "John," FOL uses "jim" | OC |
| D24 | FOLIO/train | Ex. 2 | Uncertain | premises-FOL contains: "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" — uses unbound variable x in outer formula | FOL annotation contains a free variable 'x' not properly bound | OC |
| D25 | FOLIO/train | Ex. 36 | True | "Lily is in James' family; she watches TV series in cinemas." — premises-FOL: "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Malformed FOL: missing closing parenthesis in the premises-FOL formula | OC |
| D26 | FOLIO/train | Ex. 57 | False | "Matt does not invest in the public stock market regularly. Matt likes financial risks." — premises-FOL premise 6: "InvestInRegularly(matt, publicStockMarket)" | NL premise contradicts FOL annotation: NL says "does not invest" but FOL asserts InvestInRegularly(matt) without negation | OC |
| D27 | FOLIO/train | Ex. 10 | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — extra closing parenthesis in last premise FOL | Minor FOL syntax artifact (extra parenthesis) | OC |
| D28 | FOLIO/train | Ex. 4 | False | "No trick-shot artist in Yale's varsity team struggles with half court shots." conclusion-FOL: "BadAt(jack, midRangeShot)" | Short FOL conclusion for a 5-premise story requiring multi-step chain | IO |
| D29 | FOLIO/train | Ex. 46 | Uncertain | "Everyone that knows about breath-first-search knows how to use a queue… Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." | CS / human rights story — 7 premises requiring complex multi-step chain | IO |
| D30 | FOLIO/train | Ex. 54 | True | "All players must reach the yellow stage before they can reach the green stage. The yellow stage comes after the red stage." — premises-FOL contains "∃x ∃y ∃y ∃w" (duplicate variable y) | Minor FOL annotation typo: variable y declared twice | OC |
| D31 | FOLIO/train | Ex. 50 | Uncertain | "Each building is tall. Everything tall has height." — conclusion: "All buildings are magnificent." | Extremely short, minimal story (2 premises) — simple non-sequitur conclusion | IO |
| D32 | FOLIO/train | Ex. 55 | False | "TikTok is a social media application, and it is not ideal for preteens." — conclusion-FOL: "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" — extra closing parenthesis | FOL annotation has mismatched parenthesis | OC |
| D33 | FOLIO/train | Ex. 13 | False | "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." | Double-negative NL phrasing ("No X do not have") that may create ambiguity | IF |
| D34 | FOLIO/train | Ex. 43 | True | "Modus Ponens is a component of a major part of reasoning rule." premises-FOL: "ArgumentForm(modusPonens)" | Example featuring logic-domain content (Modus Ponens) — relevant to deployment | IC, IO |
| D35 | FOLIO/train | Ex. 16 | True | "All professional athletes spend most of their time on sports… If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Contrapositives and multi-step chains matching textbook exercise style | IO |
| D36 | FOLIO/train | Ex. 38 | False | "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination… James has a car or works at Meta." | Contemporary real-world scenario (Meta/Google) embedded in logic chain | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strong coverage of multi-premise, multi-step deductive FOL reasoning
- **Dimension(s):** IO
- **Observation:** The sampled examples span a wide range of reasoning depths, from simple 2-premise syllogisms to 7-premise chains requiring sequential chaining of conditionals, universal quantifiers, and disjunctions. Multiple examples require traversing 4–6 logical steps before reaching a conclusion, directly matching the deployment's need to evaluate complex deductive reasoning.
- **Deployment relevance:** The deployment must assess whether an LLM can correctly determine argument validity before generating a pedagogical trace. FOLIO's depth distribution — confirmed in the data — provides genuine difficulty stratification across introductory (simple syllogisms) and advanced (multi-step chains) registers.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Minimal 2-premise syllogism, analogous to introductory-level exercises.
  - [D2] Example 2 (FOLIO, train, Uncertain): "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises… Mike works in this tech company." — 7-premise story requiring multiple chained universals and a complex conditional, analogous to advanced-level exercises.
  - [D29] Example 46 (FOLIO, train, Uncertain): "Everyone that knows about breath-first-search knows how to use a queue… Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." — 7-premise story with chained conditionals and disjunction.

#### Strength 2: Parallel NL and FOL representations per example
- **Dimension(s):** IO, IF
- **Observation:** Every example contains both a natural-language story and its parallel FOL annotation, supporting both the validity-determination task and the NL-to-FOL translation secondary task. The FOL layer uses the standard operator inventory (¬, ∧, ∨, →, ⊕, ∀, ∃, =) consistently across examples.
- **Deployment relevance:** The deployment requires NL-to-formal-logic translation as a core capability. FOLIO's parallel annotations allow evaluation of whether an LLM can correctly formalize NL premises, which is a prerequisite for the Fitch-style proof generation the tool needs to produce.
- **Datapoint citations:**
  - [D13] Example 16 (FOLIO, train, True): NL "All Olympic gold medal winners are professional athletes" → FOL "∀x (OlympicGoldMedalWinner(x) → ProfessionalAthlete(x))" — straightforward universal conditional mapping.
  - [D21] Example 34 (FOLIO, train, True): "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." — complex conditional with negated conjunction, illustrating the NL→FOL difficulty range.

#### Strength 3: Topical diversity supporting broad argument-type coverage
- **Dimension(s):** IC
- **Observation:** The sampled examples cover a wide range of content domains: natural science (biology, astronomy, physics), geography, sports, technology, economics, media, cultural activities, and everyday scenarios. This variety mirrors the range of argument types students encounter in US undergraduate logic courses, where textbook exercises span analogous domains.
- **Deployment relevance:** Students in intro logic courses encounter arguments drawn from diverse subject matter. FOLIO's topical range reduces the risk that a model fine-tuned or evaluated on FOLIO will be topically overfitted to any single domain.
- **Datapoint citations:**
  - [D21] Example 34 (FOLIO, train, True): "All orphan planets are rogue planets… PSO J318.5−22…" — astrophysics domain.
  - [D11] Example 13 (FOLIO, train, False): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable…" — consumer products domain.
  - [D19] Example 28 (FOLIO, train, False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. There is an embargo on Russian foreign trade goods." — macroeconomics/geopolitics domain.
  - [D4] Example 4 (FOLIO, train, False): "No trick-shot artist in Yale's varsity team struggles with half court shots." — sports domain.

#### Strength 4: Three-way label distribution includes True, False, and Uncertain
- **Dimension(s):** OO
- **Observation:** The sampled examples include all three label categories. Across the 57 reviewed examples, all three labels appear in meaningful proportions, including several False examples requiring the reasoner to identify why a conclusion does not follow or is contradicted.
- **Deployment relevance:** The deployment must identify both valid and invalid arguments. The False and Uncertain labels cover two distinct failure modes (contradiction and underdetermination), which partially map to the deployment's need to handle invalid arguments (for which countermodels are required). FOLIO does not produce countermodels, but the label space at least identifies where they would be needed.
- **Datapoint citations:**
  - [D14] Example 17 (FOLIO, train, False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire" — conclusion "There are no journalists that were born in Yorkshire" is False because the premises provide a direct counterexample.
  - [D28] Example 4 (FOLIO, train, False): "Jack is bad at mid-range shots" — labeled False given the premises about Yale's varsity team.
  - [D5] Example 5 (FOLIO, train, Uncertain): "Susan is a college student" — labeled Uncertain because her affiliation (Yale vs. Harvard) cannot be determined.

#### Strength 5: Explicit formal premise structure matching formal-logic course exercises
- **Dimension(s):** IC
- **Observation:** FOLIO premises are stated as explicit, closed-world assertions (all universals, conditionals, and individual facts are spelled out), directly matching the style of textbook logic exercises where students are given a set of premises and asked to assess a conclusion. This matches the exercise format in Barwise & Etchemendy-style courses.
- **Deployment relevance:** The deployment tool must handle arguments presented as explicit premise sets (as in textbook exercises), which is the dominant format in US undergraduate logic courses. FOLIO's explicit-premise style is well-suited for this sub-task, even if implicit-premise reconstruction is separately needed.
- **Datapoint citations:**
  - [D20] Example 33 (FOLIO, train, Uncertain): "No battery-powered watch is automatic. All digital watches are battery-powered. Some mechanical watches are automatic. All smart watches are digital. Moonwatch is either a digital watch and an automatic, or it is neither." — Complete set of explicit premises in the style of a textbook exercise.
  - [D31] Example 50 (FOLIO, train, Uncertain): "Each building is tall. Everything tall has height." — Minimal premise set; conclusion "All buildings are magnificent" tests non-sequitur recognition.

#### Strength 6: One example contains content directly relevant to logic pedagogy
- **Dimension(s):** IC, IO
- **Observation:** One example in the sample explicitly features Modus Ponens as a named entity within the story, along with discussion of inductive vs. deductive reasoning. While framed as a logic puzzle rather than a pedagogical explanation, this content is directly relevant to the deployment's domain.
- **Deployment relevance:** Students using the tool will be reasoning about logic itself (meta-logical arguments). FOLIO contains at least some examples where the content domain is formal reasoning, which aligns with logic course content.
- **Datapoint citations:**
  - [D22] Example 43 (FOLIO, train, True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning… Modus Ponens is a component of a major part of reasoning rule." — The entity "Modus Ponens" appears as a subject of logical predicates, directly engaging the deployment's pedagogical domain.
  - [D34] Example 43 (FOLIO, train, True): "ArgumentForm(modusPonens)" in the FOL annotation — confirms the named rule appears in formal representation.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Output space is a three-way classification label — no proof traces, no countermodels
- **Dimension(s):** OO, OF
- **Observation:** Every example in the dataset has a single string label (True/False/Uncertain). There are no fields for step-by-step reasoning chains, numbered deduction steps, premise citation patterns, inference rule names, or countermodel specifications. The schema has exactly six fields: premises, premises-FOL, conclusion, conclusion-FOL, label, and IDs. No ground-truth proof trace or explanation artifact exists anywhere in the data.
- **Deployment relevance:** The deployment's primary output requirement is a numbered, rule-justified, register-differentiated proof trace (or countermodel for invalid arguments). FOLIO cannot directly evaluate whether a model produces such an output. The benchmark's output ontology and output form are completely orthogonal to what the deployment needs to score. Every False-labeled example (where a countermodel is required) provides only the label, with no reference countermodel to evaluate against.
- **Datapoint citations:**
  - [D14] Example 17 (FOLIO, train, False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire as the son of a general practitioner." — Labeled False, but the dataset provides no countermodel showing that there exists a journalist born in Yorkshire; only the string "False" is present.
  - [D4] Example 4 (FOLIO, train, False): "Jack is bad at mid-range shots." — Labeled False with no explanation of which step in the chain fails or what interpretation demonstrates the falsity.
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Labeled True, but no proof trace showing the deduction steps is provided; a deployment requiring "applying modus ponens to premises 2 and 4" has no reference output to compare against.

#### Concern 2: Notation mismatch — FOLIO uses Russell & Norvig FOL, not Fitch-style natural deduction
- **Dimension(s):** IF, OO
- **Observation:** All FOL annotations in the dataset use Russell & Norvig-style flat predicate logic notation (e.g., `∀x (Plant(x) → ¬Fungi(x))`, with infix operators and no subproof structure). Fitch-style natural deduction, as used in Barwise & Etchemendy's LPL curriculum, uses a structurally different notation: numbered lines, subproof boxes, and named inference rules (e.g., →E, ∧I, ¬I). There is no Fitch-style annotation, no rule-name vocabulary, and no subproof structure anywhere in the 57 reviewed examples.
- **Deployment relevance:** The deployment's target students are taught Fitch-style notation. A tool producing outputs in Russell & Norvig FOL notation would be misaligned with what students are expected to produce and recognize. There is no documented mapping between FOLIO's operator vocabulary and LPL rule names. This is not merely a surface formatting difference — ∀E (universal elimination, a named Fitch rule) vs. the implicit universal instantiation in FOLIO's flat FOL involves different pedagogical scaffolding.
- **Datapoint citations:**
  - [D13] Example 16 (FOLIO, train, True): "∀x (OlympicGoldMedalWinner(x) → ProfessionalAthlete(x))" — flat FOL implication, no rule name cited; in Fitch style this would be referenced as line N, rule ∀E applied to a specific premise line.
  - [D2] Example 2 (FOLIO, train, Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Russell & Norvig predicate notation with no Fitch structural markers.

#### MAJOR

#### Concern 3: No propositional-logic-only examples — all examples use FOL constructs
- **Dimension(s):** IO
- **Observation:** Every example in the sample uses at least one first-order logic construct (universal quantifier ∀, existential quantifier ∃, or predicates with arguments). There are no propositional-only examples using only sentential connectives (¬, ∧, ∨, →, ↔) applied to atomic propositions without quantification. The deployment requires handling of propositional logic as a distinct layer.
- **Deployment relevance:** US introductory logic courses (both philosophy and CS-flavored) typically begin with propositional/sentential logic before introducing predicate logic. Students learning to use the tool early in their course will present purely propositional arguments. FOLIO provides no coverage of this sub-domain.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" — even the simplest example uses universal quantification, not propositional logic.
  - [D31] Example 50 (FOLIO, train, Uncertain): "∀x (Building(x) → Tall(x)) ∀x (Tall(x) → Height(x))" — 2-premise minimal example still uses FOL quantifiers rather than sentential connectives.
  - [D9] Example 11 (FOLIO, train, False): "∀x (In(x, sizeTown) → (Big(x) ∨ Small(x)))" — abstract scenario still uses universal quantification throughout.

#### Concern 4: All premises are fully explicit — no implicit-premise or enthymeme cases
- **Dimension(s):** IC
- **Observation:** In every reviewed example, all premises needed for the inference are stated explicitly in the premise set. There are no enthymematic arguments where a premise is left implicit and must be reconstructed from context or background knowledge. The annotation process explicitly added commonsense premises as explicit FOL statements, confirmed by the data: even highly structured "everyday" scenarios list every required premise.
- **Deployment relevance:** The deployment explicitly requires handling arguments where premises are implicit and must be reconstructed — "Students regularly encounter arguments with implicit premises and multi-step chains drawn from everyday or quasi-legal scenarios." FOLIO provides no coverage of this sub-task. A model evaluated solely on FOLIO would have no signal about its ability to perform premise reconstruction.
- **Datapoint citations:**
  - [D36] Example 38 (FOLIO, train, False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination. People will either take a bus or drive to their destination. Everyone who has a car will choose to drive to their destination. No students drive to their destination. James has a car or works at Meta." — What could be a 1-premise implicit argument ("James works at Meta, so he won't take the bus") is instead fully expanded into 6 explicit premises, eliminating any need for premise reconstruction.
  - [D19] Example 28 (FOLIO, train, False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. A country cannot simultaneously regulate the exchange rate and successfully control inflation… There is an embargo on Russian foreign trade goods." — All intermediate economic causal links are stated as explicit premises; no inference to unstated background knowledge is required.

#### Concern 5: FOL annotation errors found in sampled examples
- **Dimension(s):** OC
- **Observation:** Several FOL annotations in the reviewed sample contain apparent errors: (a) a free (unbound) variable `x` in Example 2's premises-FOL; (b) a missing closing parenthesis in Example 36's premises-FOL; (c) a contradictory annotation in Example 57 where the NL premise states "Matt does not invest in the public stock market regularly" but the FOL encodes `InvestInRegularly(matt, publicStockMarket)` without negation; (d) a variable declared twice (`∃x ∃y ∃y ∃w`) in Example 54; (e) an extra closing parenthesis in Example 55's conclusion-FOL; (f) a cross-name inconsistency in Example 52 where NL says "John" but FOL uses "jim."
- **Deployment relevance:** If FOLIO is used to evaluate a model's NL-to-FOL translation capability (the secondary task), annotation errors in the reference FOL create incorrect ground truth, inflating or deflating translation scores. More critically, if a model is trained on FOLIO's FOL annotations, these errors propagate into learned behavior. Given the deployment's requirement for formally correct proof traces, training data with FOL inconsistencies is a meaningful concern.
- **Datapoint citations:**
  - [D24] Example 2 (FOLIO, train, Uncertain): "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → ..." — `x` is unbound in this formula while `mike` is bound, indicating a free-variable error.
  - [D25] Example 36 (FOLIO, train, True): "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — missing closing parenthesis after `jameSFamily`.
  - [D26] Example 57 (FOLIO, train, False): NL: "Matt does not invest in the public stock market regularly" vs. FOL premise 6: "InvestInRegularly(matt, publicStockMarket)" — the negation is absent from the FOL annotation.
  - [D23] Example 52 (FOLIO, train, True): NL uses "John" throughout; FOL uses "jim" — inconsistent entity naming between NL and FOL layers.
  - [D30] Example 54 (FOLIO, train, True): "∃x ∃y ∃y ∃w" — variable `y` declared twice in the existential prefix.
  - [D27] Example 10 (FOLIO, train, Uncertain): "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — extra closing parenthesis.

#### Concern 6: Content occasionally involves politically or geopolitically sensitive real-world scenarios
- **Dimension(s):** IC, OC
- **Observation:** Several examples use real-world geopolitical entities and politically loaded content: one example involves an "ardent communist" in a business conference context, another uses Russian economic sanctions, and another uses PRC/French/North Korean nationals in a diplomatic conference. While the logical structure is neutral, the content choices may introduce distracting associations for US undergraduate students and could touch on politically sensitive areas in a classroom setting.
- **Deployment relevance:** For an educational tool targeting US undergraduates, content involving communist ideology, Russian sanctions, or North Korean nationality may generate controversy or distraction unrelated to the logic task. The deployment context mentions content neutrality as a concern.
- **Datapoint citations:**
  - [D6] Example 6 (FOLIO, train, Uncertain): "Everyone at the business conference who is an ardent communist prefers state ownership of the means of production. Ho is at the business conference and prefers state ownership of the means of production." — "Ardent communist" as a predicate in a logical argument.
  - [D19] Example 28 (FOLIO, train, False): "There is an embargo on Russian foreign trade goods." — Contemporary geopolitical scenario.
  - [D16] Example 22 (FOLIO, train, Uncertain): "No North Korean nationals are citizens of the European Union… Either Mei is a North Korean and can have medical bills partially covered, or neither is true." — North Korean nationality as a logical predicate.

#### MINOR

#### Concern 7: Absent test split in the HuggingFace dataset
- **Dimension(s):** OF
- **Observation:** The HF dataset schema shows only `train` (1,001 examples) and `validation` (203 examples) splits. The test split (226 examples per the paper) is not present in the public HuggingFace release. All sampled examples are from the train split.
- **Deployment relevance:** If the deployment uses FOLIO as an evaluation benchmark, the relevant held-out test set is unavailable via the standard HuggingFace loader. The validation set (203 examples) would need to serve as the evaluation partition, which reduces the evaluation sample size and may introduce slight coverage differences from what the paper reports.
- **Datapoint citations:** (schema-level observation, not datapoint-specific — all 57 reviewed examples are from `train` split per the metadata)

#### Concern 8: Some examples contain double-negative or ambiguous NL phrasing
- **Dimension(s):** IF
- **Observation:** At least one premise in the reviewed examples uses a double-negative construction ("No satin-finish lipsticks in the set do not have 'rosewood' in its official description") that is grammatically non-standard and could be construed as either a negated universal or an accidentally-double-negated affirmative. While the FOL annotation resolves the ambiguity, NL-level phrasing quality is uneven.
- **Deployment relevance:** The deployment requires clear, natural-language explanations that students can follow. If FOLIO's NL tier contains confusingly phrased premises, models trained on or evaluated against these examples may learn to produce similarly unclear phrasing in pedagogical explanations.
- **Datapoint citations:**
  - [D33] Example 13 (FOLIO, train, False): "No satin-finish lipsticks in the set do not have 'rosewood' in its official description." — Double negative construction may confuse students who encounter this as an explanation example.

#### Concern 9: Some HybLogic examples are visibly template-derived with artificial scenario framing
- **Dimension(s):** IC
- **Observation:** Several examples use purely abstract or fictional settings (Size Town, Potterville) that have no real-world grounding. While logically valid as test cases, these scenarios may feel pedagogically thin relative to the everyday and quasi-legal argument contexts the deployment aims to support.
- **Deployment relevance:** The deployment specifically targets arguments "drawn from everyday or quasi-legal scenarios." Abstract fictional-world examples like Size Town or Potterville do not represent the argument types students encounter in practice, though they may still be useful for evaluating logical form comprehension in isolation.
- **Datapoint citations:**
  - [D9] Example 11 (FOLIO, train, False): "Everything in Size Town is big or small. All big things in Size Town are heavy… The bird is in Size Town and it is not both heavy and still." — Entirely abstract fictional world with no real-world referent.
  - [D8] Example 8 (FOLIO, train, Uncertain): "If someone in Potterville yells, then they are not cool… Harry, who lives in Potterville either yells or flies." — Fictional scenario (Harry Potter allusion) with no everyday reasoning context.

---

### Content Coverage Summary

The 57 reviewed examples span a realistic range of multi-step FOL deductive reasoning scenarios, drawn from both Wikipedia-seeded real-world topics (British architects, Australian musicians, aerospace companies, Russian economic policy, astronomy) and template-generated syllogistic chains (watch types, basketball shooting percentages, abstract Size Town). The label distribution in the sample skews toward Uncertain (approximately 55%), with True (~30%) and False (~15%) also present, consistent with the documented test-set distribution.

Topically, the examples cover science, sports, consumer goods, geopolitics, CS/technology, media, everyday social scenarios, and even one example explicitly about Modus Ponens and inductive reasoning. Register is consistently formal written English with care given to grammatical naturalness, though several double-negative or structurally complex NL phrasings were observed.

The FOL annotation layer is dense and uses the full operator inventory (¬, ∧, ∨, →, ⊕, ∀, ∃, =) across examples. However, the sample revealed a non-trivial rate of annotation artifacts: free variables, mismatched parentheses, contradictory NL/FOL pairs, and cross-entity name inconsistencies across 6 of 57 reviewed examples (~10%). These are not concentrated in any single story cluster but appear distributed across the sample.

Critically for the deployment, the dataset contains no propositional-logic-only examples, no implicit-premise cases, no proof traces of any kind, and no countermodel artifacts. The output schema is uniformly a three-way classification label. The FOL notation is Russell & Norvig-style flat predicate logic, with no Fitch-style structural markers, subproof annotations, or inference-rule name vocabulary.

---

### Limitations

1. **Sample size and split coverage:** Only 57 of 1,204 total examples were reviewed, all from the `train` split. The validation split (203 examples) was not sampled. Coverage uncertainty exists for rare story types and edge cases.

2. **Test split unavailability:** The HuggingFace release omits the test split (226 examples), so the reported benchmark performance figures (majority baseline 38.5%, expert accuracy 95.98%) cannot be directly verified against the available data.

3. **HybLogic vs. WikiLogic proportions:** The sample does not allow precise identification of which examples are WikiLogic vs. HybLogic (no `source` field is present in the schema). Differential analysis of implicit-premise style or AST diversity by source pipeline is not possible from the available data.

4. **FOL annotation error rate:** Six annotation artifacts were found in 57 examples. This is a lower bound — other syntactically valid but semantically incorrect annotations may exist and are not detectable without running the inference engine. The true error rate across the full dataset may differ.

5. **Countermodel content:** It is not possible from the data alone to determine whether the inference engine, when applied to False-labeled examples, could generate countermodels as a byproduct. The schema captures only the truth-value label, not any intermediate inference engine output.

6. **P-FOLIO companion dataset:** The web search findings identified P-FOLIO (EMNLP 2024) as a companion dataset with human-written NL proof chains for FOLIO stories. P-FOLIO was not sampled or analyzed here; it may partially address the output-form gap noted above, though it uses narrative NL chains rather than Fitch-style proofs.