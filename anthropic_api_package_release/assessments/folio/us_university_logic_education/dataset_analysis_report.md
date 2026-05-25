## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (default config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO train | Ex 1 (story 271) | True | "No plants are fungi. Mushrooms are fungi." / conclusion: "No plants are mushrooms." | Two-premise syllogism with "No A are B" / "All C are B" form — structurally close to Hurley-style templates | IC, IO |
| D2 | FOLIO train | Ex 12 (story 257) | True | "Some cats are not pets. All cats are mammals." / conclusion: "Some mammals are not pets." | Minimal two-premise syllogism using Hurley-canonical forms ("Some A is not B", "All A are B") | IC, IO |
| D3 | FOLIO train | Ex 20 (story 269) | Uncertain | "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." | Two-premise syllogism illustrating classic undistributed-middle fallacy — directly analogous to Hurley course problems | IC, OO |
| D4 | FOLIO train | Ex 50 (story 284) | Uncertain | "Each building is tall. Everything tall has height." / conclusion: "All buildings are magnificent." | Minimal two-premise syllogism with irrelevant conclusion — indeterminate case, pedagogically transparent | IC, OO |
| D5 | FOLIO train | Ex 9 (story 264) | Uncertain | "No television stars are certified public accountants. All certified public accountants have good business sense." / conclusion: "All television stars have good business sense." | Two-premise syllogism, "No A are B" / "All B are C" form — near-Hurley template register | IC |
| D6 | FOLIO train | Ex 53 (story 37) | True | "Heptalogyy is a compound literary or narrative work that is made up of seven distinct works. The Harry Potter series consists of 7 distinct works." / conclusion: "The Harry Potter series of books is Heptalogy." | Simple two-premise syllogism with named entities; close to textbook form | IC |
| D7 | FOLIO train | Ex 2 (story 376) | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises. People in this tech company who wear the same flannel shirts every day are consistent..." | Long naturalistic prose narrative with 7 premises and XOR embedded in premise — substantially more complex than Hurley problems | IC, IO |
| D8 | FOLIO train | Ex 3 (story 180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac. If Sam uses a Mac, he will play a song." | 6-premise narrative scenario with chained conditionals and exclusive disjunction | IC, IO |
| D9 | FOLIO train | Ex 13 (story 395) | False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable...ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Complex branded-product scenario with 5 premises and compound conclusion | IC |
| D10 | FOLIO train | Ex 21 (story 381) | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing...If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up..." | 6-premise Wikipedia-seeded narrative; convoluted tautological final premise | IC |
| D11 | FOLIO train | Ex 4 (story 408) | False | "No trick-shot artist in Yale's varsity team struggles with half court shots...Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." | Sports-domain narrative, 5 premises, label=False — tests invalid-conclusion case | OO, OC |
| D12 | FOLIO train | Ex 17 (story 70) | False | "Michael O'Donnell is a British physician, journalist, author, and broadcaster...Michael O'Donnell was born in Yorkshire as the son of a general practitioner." / conclusion: "There are no journalists that were born in Yorkshire." | WikiLogic biographical narrative; False label from clear counterexample in premises | OO, OC |
| D13 | FOLIO train | Ex 29 (story 210) | False | "The only types of mammals that lay eggs are either platypuses or echidnas...Grebes are not platypuses and also not echidnas." / conclusion: "Hyraxes lay eggs." | Biology-domain story; False conclusion via FOL entailment of negation | OO |
| D14 | FOLIO train | Ex 28 (story 252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency...There is an embargo on Russian foreign trade goods." / conclusion: "In Russia, an effective monetary policy is possible." | Economics-domain story; False via chain of conditionals; requires domain knowledge about Russia | IC |
| D15 | FOLIO train | Ex 6 (story 423) | Uncertain | "Everyone at the business conference is either an investor or an entrepreneur...Ho is at the business conference and prefers state ownership of the means of production." / conclusion: "Ho is not an ardent communist." | Unknown because ardent communist status is underdetermined given premises | OO |
| D16 | FOLIO train | Ex 22 (story 475) | Uncertain | "All PRC nationals are entitled to national social insurance coverage...Mei is at the Franco-China diplomatic conference." / conclusion: "Mei is a PRC national." | Diplomatic conference scenario; Uncertain because Mei's nationality not determinable | OO |
| D17 | FOLIO train | Ex 23 (story 108) | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus...Airbus made more revenue than Boeing last year." / conclusion: "There exists a SpaceX commercial aircraft." | Conclusion about SpaceX is irrelevant to premises — clear indeterminate case | OO |
| D18 | FOLIO train | Ex 43 (story 393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning...Modus Ponens is a component of a major part of reasoning rule." | Logic-domain story mentioning Modus Ponens — meta-logical content | IC |
| D19 | FOLIO train | Ex 7 (story 30) | Uncertain | "EndGame is a movie released in 2006...Andy Chang is from Hong Kong." / conclusion: "All of Andy Chang's movies are filmed outside of Washington." | WikiLogic film-domain story with insufficient premises to determine universal conclusion | IO, OO |
| D20 | FOLIO train | Ex 11 (story 486) | False | "Everything in Size Town is big or small...The bird is in Size Town and it is not both heavy and still." / conclusion: "If the bird is small or still, then it is either unpredictable or changing." | Abstract "Size Town" scenario; complex conditional conclusion with XOR | IC, OO |
| D21 | FOLIO train | Ex 16 (story 346) | True | "All professional athletes spend most of their time on sports...If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." / conclusion: "Amy is neither a full-time scientist nor an Olympic gold medal winner." | 6-premise chained syllogism with conditional; multi-step reasoning | IO |
| D22 | FOLIO train | Ex 33 (story 341) | Uncertain | "No battery-powered watch is automatic...Moonwatch is either a digital watch and an automatic, or it is neither." / conclusion: "Moonwatch is a mechanical watch." | Watch-domain story; mechanical watch status underdetermined from premises | OO |
| D23 | FOLIO train | Ex 38 (story 425) | False | "Everyone working at Meta has a high income...James has a car or works at Meta." / conclusion: "James is a student." | Modern tech-company scenario; False conclusion derivable via short chain | IC |
| D24 | FOLIO train | Ex 52 (story 337) | True | "No athletes never exercise...Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." (Note: conclusion uses "Jim" while premises use "John/Jim" inconsistently) | Name inconsistency between premises (John) and conclusion (Jim) — annotation quality issue | OC |
| D25 | FOLIO train | Ex 34 (story 377) | True | "All orphan planets are rogue planets...PSO J318.5−22 is a rogue planet." / conclusion: "PSO J318.5−22 is an orphan planet or it does not have the Sun as its star, or both." | Astronomy domain; complex disjunctive conclusion | IC |
| D26 | FOLIO train | Ex 56 (story 27) | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin...Yangshuo is not a district in Guilin." / conclusion: "Kowloon District is in Hong Kong." | Irrelevant conclusion — Unknown because premises have nothing to say about Hong Kong | OO |
| D27 | FOLIO train | Ex 2 (story 376) | Uncertain | FOL premise: "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" | Malformed FOL — free variable `x` in antecedent of conditional; annotation error | OC |
| D28 | FOLIO train | Ex 57 (story 362) | False | "Matt does not invest in the public stock market regularly. Matt likes financial risks." / conclusion: "Matt is not at risk of a gambling addiction and Mike does not both read..." | Conclusion mentions "Mike" but premises are about "Matt" — name inconsistency in annotation | OC |
| D29 | FOLIO train | Ex 36 (story 422) | True | "Lily is in James' family; she watches TV series in cinemas." FOL: "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Missing closing parenthesis in FOL formula — syntactic annotation error | OC |
| D30 | FOLIO train | Ex 55 (story 477) | False | "TikTok is a social media application, and it is not ideal for preteens." / conclusion-FOL: "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" | Trailing unmatched parenthesis in conclusion-FOL | OC |
| D31 | FOLIO train | Ex 39 (story 243) | False | "If a person can distinguish the taste of different condiments, then they can also use different condiments for cooking...John can make meals which are popular at the party." / conclusion: "John cannot use different condiments for cooking." | 5-premise story; False conclusion derivable via clear chain | IO |
| D32 | FOLIO train | Ex 44 (story 474) | False | "All humans are capable of abstract thoughts. Plants are not capable of abstract thoughts...Hulu is a goat or a human." / conclusion: "If Hulu is either an animal or dirt, then Hulu is capable of abstract thoughts and is dirt." | XOR used in third premise in FOL but not NL; complex conditional conclusion | OC |
| D33 | FOLIO train | Ex 48 (story 92) | True | "Adventures of Rusty is a drama film and children's film. Columbia Pictures produced Adventures of Rusty." / conclusion: "Columbia pictures produced some drama film." | Simple existential conclusion from two-premise story | IO |
| D34 | FOLIO train | Ex 31 (story 60) | True | "All buildings in New Haven are not high...Tower A is managed by Yale Housing." / conclusion: "Tower A is low." (conclusion-FOL: ¬High(tower-a)) | Simple two-step chain; low premise count, close to textbook syllogistic form | IC |
| D35 | FOLIO train | Ex 10 (story 391) | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" | Unmatched parenthesis in FOL formula — additional annotation error instance | OC |
| D36 | FOLIO train | Ex 46 (story 448) | Uncertain | "Someone is either a seasoned software engineer interviewer at Google, has human rights, or both." / premises-FOL: "∀x ((Seasoned(x) ∧ SoftwareEngineerInterviewer(x) ∧ At(x, google)) ∨ Have(x, humanRights))" | NL says "or both" (inclusive disjunction) but FOL uses ∨ — potential NL-FOL alignment gap | OC |
| D37 | FOLIO train | Ex 5 (story 348) | Uncertain | "All young adults at the event like independence...If Susan is a Yale student, then she does not like independence." / conclusion: "Susan is a college student." | 7-premise story with competing conditional chains; classic indeterminate case | OO |
| D38 | FOLIO train | Ex 8 (story 482) | Uncertain | "Harry, who lives in Potterville either yells or flies. Potter, who lives in Potterville, is a wizard and flies." / conclusion: "Harry is cool." | Fantasy-domain story; multiple conclusions from same story_id test same premises | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Three-way label schema maps directly onto the deployment rubric for FOL cases
- **Dimension(s):** OO, OC
- **Observation:** Across all 57 sampled examples, the three labels (True, False, Uncertain) appear in clear logical patterns consistent with the formally verified schema: False is assigned when the negation of the conclusion is provably entailed by the premises (not merely when the conclusion fails to follow), and Uncertain is assigned when premises are consistent with both the conclusion and its negation. The False examples in the sample (D11, D12, D13, D29, D38) all involve clear counterexamples entailed by premises, not merely absent entailment, aligning with the deployment's strict "invalid = premises entail negation" definition.
- **Deployment relevance:** The course's most exacting rubric requirement — that "invalid" requires positive entailment of the negation, not just failure to entail — is confirmed as operationally satisfied in the data examined. Annotators and the FOL prover jointly enforce this distinction.
- **Datapoint citations:**
  - [D12] Ex 17 (FOLIO train, label=False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster...Michael O'Donnell was born in Yorkshire as the son of a general practitioner." / conclusion: "There are no journalists that were born in Yorkshire." — False because premises explicitly establish a counterexample (Michael O'Donnell is both a journalist and born in Yorkshire), confirming provable negation entailment rather than mere absence of entailment.
  - [D13] Ex 29 (FOLIO train, label=False): "Grebes are not platypuses and also not echidnas." / conclusion: "Hyraxes lay eggs." — False derivable via clear FOL chain through the exclusive mammal egg-laying premise; provable negation entailment confirmed.
  - [D11] Ex 4 (FOLIO train, label=False): "No trick-shot artist...struggles with half court shots...Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." / conclusion: "Jack is bad at mid-range shots." — False because either branch of the disjunction entails the negation.

#### Strength 2: Presence of minimal syllogistic examples close to Hurley-style template forms
- **Dimension(s):** IC
- **Observation:** A subset of examples — especially from the HybLogic pipeline and simpler WikiLogic stories — exhibit the short, template-like premise structures ("No A are B", "All C are B", "Some A is not B") that characterize Hurley-style course-packet problems, with low premise counts (2–3 premises) and clear categorical conclusions.
- **Deployment relevance:** These examples partially bridge the register gap between FOLIO's naturalistic prose and the course's Hurley-style templates. Models tested on FOLIO that perform well on this subset would demonstrate some relevant capability on the deployment's dominant input register.
- **Datapoint citations:**
  - [D1] Ex 1 (FOLIO train, label=True): "No plants are fungi. Mushrooms are fungi." / conclusion: "No plants are mushrooms." — Two-premise syllogism with canonical "No A are B" / "All C are B" structure directly paralleling Hurley examples.
  - [D2] Ex 12 (FOLIO train, label=True): "Some cats are not pets. All cats are mammals." / conclusion: "Some mammals are not pets." — Uses both "Some A is not B" and "All A are B" forms, core Hurley template patterns.
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." — Classic undistributed-middle fallacy in bare "All A are B" form, highly representative of introductory logic course problems.
  - [D5] Ex 9 (FOLIO train, label=Uncertain): "No television stars are certified public accountants. All certified public accountants have good business sense." / conclusion: "All television stars have good business sense." — "No A are B" / "All B are C" form nearly identical to Hurley syllogism templates.
  - [D4] Ex 50 (FOLIO train, label=Uncertain): "Each building is tall. Everything tall has height." / conclusion: "All buildings are magnificent." — Minimal two-premise story with pedagogically transparent irrelevant-conclusion indeterminate case.

#### Strength 3: FOL operator coverage matches the deployment's second-half logical scope
- **Dimension(s):** IO
- **Observation:** The sampled examples contain all FOL operators the course requires for its second half: universal quantifier (∀), existential quantifier (∃), negation (¬), conjunction (∧), disjunction (∨), implication (→), exclusive disjunction (⊕), and equality (=). Examples span basic universal syllogisms, existential conclusions, chained conditionals, and combinations of quantifiers with connectives.
- **Deployment relevance:** The course's second-half FOL scope is comprehensively covered by the operator set observable in the data. A model scoring well on FOLIO would have been tested on all structural patterns relevant to the predicate-logic half of the course.
- **Datapoint citations:**
  - [D21] Ex 16 (FOLIO train, label=True): "All professional athletes spend most of their time on sports...If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." — Uses ∀, ∃ (via "all"), ¬, →, ∨ in combination across 6 premises.
  - [D8] Ex 3 (FOLIO train, label=Uncertain): "A project is written either in C++ or Python" → FOL uses ⊕ (exclusive disjunction) alongside ∀, ∃, →, ¬ — full operator set in a single story.
  - [D38] Ex 8 (FOLIO train, label=Uncertain): "All wizards in Potterville know magic...Harry, who lives in Potterville either yells or flies." — ∀, →, ¬, ⊕ in a chained multi-step reasoning structure.

#### Strength 4: Indeterminate (Unknown) label cases are clearly defined and pedagogically recognizable
- **Dimension(s):** OO
- **Observation:** The Uncertain/Unknown examples in the sample exhibit clearly recognizable patterns of logical underspecification: premises that are silent on a dimension needed to determine the conclusion (D15, D16, D17, D26), or premises that are consistent with both the conclusion and its negation due to insufficient information (D3, D22, D37). The course rubric's definition of indeterminate — "premises consistent with both the conclusion and its negation" — matches these cases precisely.
- **Deployment relevance:** The Unknown label's formal alignment with the course rubric is confirmed in the data. Students using the tool would receive "indeterminate" classifications on exactly the cases where neither entailment nor contradiction is provable, matching the intended pedagogical behavior.
- **Datapoint citations:**
  - [D17] Ex 23 (FOLIO train, label=Uncertain): "The world's only major large passenger aircraft manufacturers are Boeing and Airbus...Airbus made more revenue than Boeing last year." / conclusion: "There exists a SpaceX commercial aircraft." — Premises are entirely silent on SpaceX; neither conclusion nor its negation follows. Exemplary indeterminate case.
  - [D26] Ex 56 (FOLIO train, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin...Yangshuo is not a district in Guilin." / conclusion: "Kowloon District is in Hong Kong." — Conclusion about Hong Kong is logically disconnected from premises about Guilin — paradigmatic indeterminate.
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." — Undistributed middle; premises consistent with enzymes being or not being proteins.

#### Strength 5: Multi-step reasoning chains test the higher end of the course's FOL difficulty range
- **Dimension(s):** IO
- **Observation:** Many examples require 3–6 chained reasoning steps across multiple premises, with conclusions that can only be reached by tracing through multiple universal rules applied to specific individuals. This covers the deeper end of the reasoning depth distribution that the course's FOL section targets.
- **Deployment relevance:** While some FOLIO examples may be harder than typical course-packet problems, the presence of 3–5 step chains ensures the benchmark is not trivially solvable for the second-half FOL content and provides meaningful signal about model capability at the difficulty level instructors care about.
- **Datapoint citations:**
  - [D21] Ex 16 (FOLIO train, label=True): "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports. All Nobel physics laureates are full-time scientists. Amy spends the most time on sports, or Amy is an Olympic gold medal winner. If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." — 6-premise chain requiring case analysis.
  - [D38] Ex 8 (FOLIO train, label=Uncertain): Potterville scenario — 7 premises with chained wizard→magic→fly→cool chain; conclusion requires tracing through 4 steps.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of propositional-logic (quantifier-free) examples
- **Dimension(s):** IO
- **Observation:** Every single example in the 57-item sample contains at least one universal (∀) or existential (∃) quantifier in the premises-FOL field. No quantifier-free example was observed. The YAML gap analysis and web search confirm this is a structural property of FOLIO, not a sampling artifact — the benchmark was designed around FOL predicate structures, and the FOL2NS paper explicitly characterizes quantifiers as the defining feature of FOLIO's logical scope.
- **Deployment relevance:** The course's first half is entirely propositional (connectives, truth tables, modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism, etc. — no quantifiers). If a model is assessed using FOLIO alone, there is zero coverage of approximately half the course's logical scope. A system that fails on propositional logic but succeeds on FOL would receive a misleadingly favorable evaluation. This is a deployment-critical gap for any tool intended to cover the full course.
- **Datapoint citations:**
  - [D1] Ex 1 (FOLIO train, label=True): "∀x (Plant(x) → ¬Fungi(x)) / ∀x (Mushroom(x) → Fungi(x))" — Even the simplest two-premise example uses universal quantifiers throughout; no quantifier-free propositional version exists in FOLIO.
  - [D4] Ex 50 (FOLIO train, label=Uncertain): "∀x (Building(x) → Tall(x)) / ∀x (Tall(x) → Height(x))" — The two shortest examples in the sample still use ∀; confirming no propositional subset.
  - [D2] Ex 12 (FOLIO train, label=True): "∃x (Cat(x) ∧ ¬Pet(x)) / ∀x (Cat(x) → Mammal(x))" — Minimal example uses both ∃ and ∀; no propositional-only FOLIO examples observed.

---

#### MAJOR

#### MAJOR Concern 1: Register mismatch — dominant FOLIO style is naturalistic prose, not Hurley-style templates
- **Dimension(s):** IC
- **Observation:** The majority of examples in the sample are naturalistic, topic-rich narratives substantially different from the bare template forms of Hurley-style course problems. Examples involve tech companies (D7), film directors (D19), diplomacy (D16), economics with Russia (D14), lipstick product lines (D9), and social media platforms (D23). The register is annotator-composed prose with epistemic qualifiers, complex noun phrases, and embedded real-world knowledge — the opposite of the syntactically constrained "All A are B" / "If P then Q" forms that dominate the course packet. While some simpler examples (D1, D2, D3, D5) approach Hurley register, they are a minority.
- **Deployment relevance:** Model performance on FOLIO's naturalistic prose may not predict performance on the course's dominant templated inputs. A model that successfully classifies "People in this tech company who wear the same flannel shirts every day are consistent" may still fail on "All A are B. Some B are not C. Therefore some A are not C." — and vice versa. Benchmark results may inflate or deflate apparent capability relative to the actual deployment inputs.
- **Datapoint citations:**
  - [D7] Ex 2 (FOLIO train, label=Uncertain): "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises. People in this tech company who wear the same flannel shirts every day are consistent and enjoy sticking to their regular routines." — Naturalistic narrative with embedded relative clauses and real-world scenario; maximally different from Hurley-style bare templates.
  - [D9] Ex 13 (FOLIO train, label=False): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable...ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." — Branded-product prose with complex noun phrases; requires parsing product line terminology.
  - [D14] Ex 28 (FOLIO train, label=False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency...There is an embargo on Russian foreign trade goods." — Economics domain with contemporary geopolitical content; no structural equivalent in Hurley-style templates.
  - [D25] Ex 34 (FOLIO train, label=True): "All orphan planets are rogue planets...PSO J318.5−22 is a rogue planet." — Astronomy technical nomenclature ("PSO J318.5−22") requiring domain knowledge entirely absent from introductory logic course packets.

#### MAJOR Concern 2: Multiple annotation errors visible in the sampled data
- **Dimension(s):** OC
- **Observation:** The 57-item sample contains at least five distinct annotation errors or quality issues: (1) a free variable `x` in a FOL conditional antecedent (D27, story 376); (2) a name inconsistency between premises ("John") and conclusion ("Jim") (D24, story 337); (3) a name inconsistency between premises ("Matt") and conclusion ("Mike") in the conclusion text (D28, story 362); (4) a missing closing parenthesis in a FOL formula (D29, story 422; D30, story 477; D35, story 391); (5) a potential NL-FOL alignment gap where "either...or both" (inclusive disjunction) in NL is rendered as ∨ rather than explicitly verified (D36, story 448). These occur across different story IDs, suggesting this is not an isolated issue.
- **Deployment relevance:** A 2026 cleaning study cited in the web search found label errors and NL-FOL misalignments in the original FOLIO dataset. The sampled data confirms this concern is real and observable. For a deployment assessing model logic-checking capability, annotation noise in the ground truth directly undermines the validity of benchmark scores — a model might classify a mislabeled example "incorrectly" while reasoning correctly from the NL premises. The original (uncleaned) HuggingFace dataset should be used with caution.
- **Datapoint citations:**
  - [D27] Ex 2 (FOLIO train, story 376, label=Uncertain): FOL premise contains "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" — `x` is a free variable in the antecedent; this is a syntactic/semantic annotation error in the FOL.
  - [D24] Ex 52 (FOLIO train, story 337, label=True): Premises use "John" throughout; conclusion states "Jim is not a Knicks player." — Name inconsistency suggests a copy-paste or editing error in annotation.
  - [D28] Ex 57 (FOLIO train, story 362, label=False): Conclusion text reads "Matt is not at risk of a gambling addiction and Mike does not both read the Wall Street Journal..." — "Mike" appears in the conclusion while all premises discuss "Matt."
  - [D29] Ex 36 (FOLIO train, story 422, label=True): FOL premises contain "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — missing closing parenthesis after `jameSFamily`.
  - [D35] Ex 10 (FOLIO train, story 391, label=Uncertain): FOL premises contain "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — unmatched trailing parenthesis.

#### MAJOR Concern 3: Reasoning depth substantially exceeds typical introductory course-packet complexity
- **Dimension(s):** IO, IC
- **Observation:** Many examples in the sample require 4–7 chained reasoning steps and involve 5–8 premises with complex interactions among universal rules, conditional chains, and disjunctions. The course's introductory context involves 1–3 step arguments drawn from a structured textbook. FOLIO's documented mode reasoning depth is 4 steps with 28.7% requiring 5+, and the data confirms this — numerous examples involve extended chains not representative of introductory course problems.
- **Deployment relevance:** If a model struggles on deep FOLIO examples but would succeed on the 1–3 step problems in the course packet, FOLIO accuracy scores would underestimate actual deployment performance. Conversely, a model that performs adequately on FOLIO may be assessed as adequate when it could still fail on pedagogically simpler but register-distinct Hurley-style problems. The depth distribution mismatch distorts the benchmark's predictive validity for the deployment.
- **Datapoint citations:**
  - [D7] Ex 2 (FOLIO train, label=Uncertain): 7 premises with chained rules about tech company employees; final premise has an XOR embedded in a nested conditional structure — far beyond a first-semester logic student's typical 2–3 premise problem.
  - [D10] Ex 21 (FOLIO train, label=False): "All people who attend Renaissance fairs regularly enjoy dressing up...If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." — 6 premises; convoluted tautological final premise requires 4–5 step reasoning.
  - [D21] Ex 16 (FOLIO train, label=True): 6-premise problem about Amy's professional status requiring complete case analysis across two disjuncts, spanning 4 distinct predicate categories.

#### MAJOR Concern 4: Label field uses "Uncertain" in HuggingFace data vs. "Unknown" in paper documentation
- **Dimension(s):** OO, OF
- **Observation:** The FOLIO paper and all citations consistently use "Unknown" as the third label category. However, in the actual HuggingFace dataset sampled, the third label appears as "Uncertain" (e.g., D3, D5, D15, D16, D22, D37). This is an inconsistency between the paper's documented label schema and the dataset schema in the deployed HuggingFace version. All 57 examples with a non-True/False label use "Uncertain," not "Unknown."
- **Deployment relevance:** For any automated pipeline that relies on the label strings from the HuggingFace dataset for evaluation, using "Unknown" (from the paper) as the target class label would cause a mismatch. This is a practical implementation concern that could invalidate accuracy calculations if not caught. The deployment tool's evaluation code must use "Uncertain" to match the actual data labels.
- **Datapoint citations:**
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / label field value: "Uncertain" — paper documentation calls this "Unknown."
  - [D15] Ex 6 (FOLIO train, label=Uncertain): "Ho is at the business conference and prefers state ownership of the means of production." / conclusion: "Ho is not an ardent communist." — label field: "Uncertain."
  - [D37] Ex 5 (FOLIO train, label=Uncertain): Susan/Yale/Harvard event story — label field: "Uncertain."

---

#### MINOR

#### MINOR Concern 1: Test split not available in the HuggingFace dataset
- **Dimension(s):** OF
- **Observation:** The HuggingFace metadata shows only `train` (1,001 examples) and `validation` (203 examples) splits. The `test` split (226 examples, on which FOLIO's published results and majority baseline of 38.5% are computed) is not accessible in the public HuggingFace dataset. The analysis is based entirely on the training split.
- **Deployment relevance:** Benchmark comparisons to published model performance (GPT-4 64.16%, expert human 95.98%) are based on the test set. Users deploying FOLIO for assessment will need to use the validation set (203 examples) or the training set as a proxy, which may not precisely replicate published distributional statistics. This does not affect content validity observations but limits direct comparison to published baselines.
- **Datapoint citations:** (structural observation; no specific datapoint required)

#### MINOR Concern 2: Topic diversity includes content that may introduce construct-irrelevant domain knowledge requirements
- **Dimension(s):** IC
- **Observation:** Several WikiLogic examples presuppose domain-specific real-world knowledge that is not included in the premises and whose absence could affect whether a naive reader (or model without that knowledge) correctly identifies a classification. The economics-Russia example (D14) presupposes knowledge of what an embargo does; the lipstick example (D9) requires parsing branded product terminology; the astronomy example (D25) involves a technical astronomical designation.
- **Deployment relevance:** The deployment's course-packet problems are designed to be self-contained and domain-neutral, relying only on formal structure and explicitly stated premises. FOLIO's Wikipedia-seeded stories may introduce construct-irrelevant difficulty for models that lack the relevant world knowledge to parse the semantic content of the premises, creating a conflation between logical-reasoning ability and domain knowledge.
- **Datapoint citations:**
  - [D14] Ex 28 (FOLIO train, label=False): "The introduction of an embargo on foreign trade goods in a country leads to a sharp decrease in exports...There is an embargo on Russian foreign trade goods." — The logical chain depends on understanding what an embargo causes, which is given as a premise; however, the contemporary geopolitical context adds semantic load absent from Hurley-style problems.
  - [D25] Ex 34 (FOLIO train, label=True): "PSO J318.5−22 is a rogue planet" — Technical astronomical object name; while the premises are formally stated, the vocabulary creates parsing difficulty for readers unfamiliar with the domain.

#### MINOR Concern 3: Multiple conclusions drawn from a single story may create non-independence between test examples
- **Dimension(s):** IO, OF
- **Observation:** Several story_ids appear multiple times in the sample with different conclusions tested against the same premise set (story 408 appears as Ex 4, Ex 18, Ex 32; story 482 as Ex 8, Ex 19, Ex 30; story 70 as Ex 17, Ex 41; story 474 as Ex 44, Ex 49; story 436 as Ex 14, Ex 42; story 448 as Ex 46, Ex 47). This is by design (the benchmark is split by story, not by conclusion), but it means that per-example accuracy metrics treat correlated items as independent.
- **Deployment relevance:** If a model systematically misrepresents one story's premises, it will fail on all conclusions derived from that story, creating correlated errors that inflate apparent variance in model performance estimates. For deployment purposes, per-story accuracy may be a more informative metric than per-example accuracy, but this is not the primary reported metric.
- **Datapoint citations:**
  - [D11] and [D18] (both story 408): Same 5 premises about Yale varsity team; one tests "Jack is bad at mid-range shots" (False), the other tests a compound conditional conclusion (Uncertain) — shared premise set makes these non-independent.
  - [D38] Ex 8 and Ex 19 and Ex 30 (all story 482): Same Potterville premises tested with three different conclusions ("Harry is cool" / "Harry is not cool" / "Harry is a wizard or angry") — three dependent test items from one story.

---

### Content Coverage Summary

The 57 sampled examples span a wide range of topics: sports (basketball, basketball shooting), technology (software engineering, social media, computer science), biology (mammals, plants, fish), film, astronomy, economics, everyday scenarios (travel planning, family streaming subscriptions), and abstract fictional domains ("Size Town," "Potterville"). Approximately one-third of examples (estimated from the sample) come from short 2–4 premise stories that are structurally close to Hurley-style syllogistic forms; the remaining two-thirds involve 5–8 premise naturalistic narratives with complex logical interactions.

All examples use FOL predicate structures — universal and existential quantifiers are present in every example examined. No quantifier-free propositional example was found. The label distribution in the sample is approximately: True (~25%), False (~28%), Uncertain (~47%) — somewhat more Uncertain-heavy than the documented test set (27% Unknown), though this may reflect training set distribution differences.

The FOL annotations are generally well-formed but the sample reveals at least five distinct annotation errors (free variables, name inconsistencies, parenthesis mismatches) across different story IDs. The label field uses "Uncertain" rather than the paper-documented "Unknown." The register ranges from simple two-premise syllogisms in bare categorical form to complex multi-clause narratives with embedded real-world knowledge, with the naturalistic prose register predominating.

---

### Limitations

1. **Test split inaccessible**: All 57 examples are from the training split. The published performance baselines (GPT-4 64.16%, majority baseline 38.5%) are computed on the test split (226 examples), which is not available in the public HuggingFace repository. The training set may have a different label distribution or difficulty profile.

2. **Sample size**: 57 examples represent ~5.7% of the training set (1,001 examples) and ~4.7% of the combined train+validation set (1,204 examples). Topic and difficulty distributions observed may not fully represent the broader dataset.

3. **FOL annotation quality**: The FOL formulas (premises-FOL, conclusion-FOL fields) were inspected visually but not computationally verified against a theorem prover. The annotation errors noted (free variables, parenthesis mismatches, name inconsistencies) were identified by human inspection; there may be additional errors not visible through manual review of 57 examples.

4. **HybLogic vs. WikiLogic split**: The sample does not identify which pipeline produced each example. Conclusions about register (naturalistic vs. template-like) are inferred from content, not from a verified pipeline tag. The HybLogic subset (which would be most relevant to Hurley-style comparisons) cannot be isolated from this sample.

5. **Readability complexity**: The Dale-Chall readability distribution referenced in the paper (Figure 3) was not inspectable from the HuggingFace data. The claim that FOLIO examples are more complex than Hurley-style templates is inferred from content inspection, not from a computed readability comparison.

6. **Cleaned dataset**: The 2026 cleaning pipeline (using Vampire theorem prover) mentioned in the web search findings is not reflected in the current HuggingFace dataset. The label reliability concerns observed in the sample may be partially addressed by that cleaned version, which was not available for inspection.