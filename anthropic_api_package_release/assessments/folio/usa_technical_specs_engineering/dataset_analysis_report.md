## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-01-31
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | yale-nlp/FOLIO | Ex. 1 (story_id 271) | True | "No plants are fungi. Mushrooms are fungi." | Minimal 2-premise syllogism; fully explicit closed-world premises | IO, IC |
| D2 | yale-nlp/FOLIO | Ex. 2 (story_id 376) | Uncertain | "People in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises." | Multi-premise narrative about a tech company employee; all predicates fully stated | IO, IC |
| D3 | yale-nlp/FOLIO | Ex. 3 (story_id 180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac." | Self-contained programming scenario; all relevant constraints explicitly stated in premises | IO |
| D4 | yale-nlp/FOLIO | Ex. 28 (story_id 252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. A country cannot simultaneously regulate the exchange rate and successfully control inflation." | Policy/economics domain; fully explicit premises; no external standard referenced | IC, IO |
| D5 | yale-nlp/FOLIO | Ex. 22 (story_id 475) | Uncertain | "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered. All PRC nationals are entitled to national social insurance coverage." | International policy scenario; all rules fully spelled out | IO |
| D6 | yale-nlp/FOLIO | Ex. 11 (story_id 486) | False | "Everything in Size Town is big or small. All big things in Size Town are heavy." | Abstract taxonomy story; no real-world domain knowledge required | IC |
| D7 | yale-nlp/FOLIO | Ex. 43 (story_id 393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." | Meta-logical content; fully closed-world | IC, IO |
| D8 | yale-nlp/FOLIO | Ex. 34 (story_id 377) | True | "Everything is either outside the solar system or in the solar system. Nothing outside the solar system has the Sun as its star." | Scientific premises fully stated; no reference to external standards | IC |
| D9 | yale-nlp/FOLIO | Ex. 46/47 (story_id 448) | Uncertain/False | "Everyone that knows about breath-first-search knows how to use a queue. If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is." | CS/software domain; all premises explicit and domain-neutral | IC |
| D10 | yale-nlp/FOLIO | Ex. 23 (story_id 108) | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus. All American Airlines planes are from the world's major large passenger aircraft manufacturers." | Aviation adjacent; but no technical specifications, tolerances, or implicit standards | IC, IO |
| D11 | yale-nlp/FOLIO | Ex. 55 (story_id 477) | False | "TikTok is a social media application, and it is not ideal for preteens." | Consumer tech scenario; ¬(chat ⊕ computer_program) conclusion structure | OO |
| D12 | yale-nlp/FOLIO | Ex. 2 (story_id 376) | Uncertain | "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" | FOL parallel annotation; shows explicit closed-world FOL encoding | IF, OO |
| D13 | yale-nlp/FOLIO | Ex. 4 (story_id 408) | False | "No trick-shot artist in Yale's varsity team struggles with half court shots." | Multi-premise sports scenario; label False from fully explicit premises | OO |
| D14 | yale-nlp/FOLIO | Ex. 16 (story_id 346) | True | "All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports." | 6-premise chain with compound conditional; inference-engine verified True | OC |
| D15 | yale-nlp/FOLIO | Ex. 21 (story_id 381) | False | "If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." | Complex conditional with exclusive disjunction; no domain knowledge required | IO |
| D16 | yale-nlp/FOLIO | Ex. 36 (story_id 422) | True | "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Parenthesis error in FOL annotation for Lily's premise | OC |
| D17 | yale-nlp/FOLIO | Ex. 57 (story_id 362) | False | "Matt does not invest in the public stock market regularly. Matt likes financial risks." | Contradictory premise pair (Ex 57 NL says Matt does NOT invest but FOL says InvestInRegularly(matt, publicStockMarket)) | OC |
| D18 | yale-nlp/FOLIO | Ex. 52 (story_id 337) | True | "Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises. … ¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))" | NL says "John," FOL says "jim" — name inconsistency between NL and FOL | OC |
| D19 | yale-nlp/FOLIO | Ex. 33 (story_id 341) | Uncertain | "Moonwatch is either a digital watch and an automatic, or it is neither." | Product-domain scenario; conclusion-FOL uses "moonWatch" while NL uses "Moonwatch" — capitalization inconsistency | OC |
| D20 | yale-nlp/FOLIO | Ex. 13 (story_id 395) | False | "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." | Double negation in premise NL ("do not have" in a "No…not" construction); potential NL ambiguity | IC, OC |
| D21 | yale-nlp/FOLIO | Ex. 5 (story_id 348) | Uncertain | "All Yale students at the event are college students. Everyone at the event is a Yale student or a Harvard student." | Classic syllogistic structure, fully explicit | IO |
| D22 | yale-nlp/FOLIO | Ex. 38 (story_id 425) | False | "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination." | Contemporary brand reference; all premises fully stated | IC |
| D23 | yale-nlp/FOLIO | Ex. 6 (story_id 423) | Uncertain | "Everyone at the business conference who is an ardent communist prefers state ownership of the means of production." | Political/ideological content (communist, planned economy); explicitly stated in premises | IC |
| D24 | yale-nlp/FOLIO | Ex. 29 (story_id 210) | False | "The only types of mammals that lay eggs are either platypuses or echidnas. … Grebes are not platypuses and also not echidnas." | Biology facts used as premises; verifiable real-world knowledge | IC |
| D25 | yale-nlp/FOLIO | Ex. 50 (story_id 284) | Uncertain | "Each building is tall. Everything tall has height." | Minimal 2-premise story; "All buildings are magnificent" — Uncertain since 'magnificent' not derivable | OO |
| D26 | yale-nlp/FOLIO | Ex. 7 (story_id 30) | Uncertain | "Andy Chang is from Hong Kong." | Specific named person (likely real individual); Wikipedia-seeded | IC |
| D27 | yale-nlp/FOLIO | Ex. 57 (story_id 362) | False | "∀x (SpendAt(x, alotOfMoney, casino) ∨ (∃y (¬(y=casino) ∧ BettingGame(y) ∧ SpendAt(x, aLotOfMoney, y)) → AtRiskOf(x, gamblingAddiction))" | FOL missing closing parenthesis — syntactic issue in annotation | OC |
| D28 | yale-nlp/FOLIO | Ex. 10 (story_id 391) | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" | Extra closing parenthesis in FOL — syntactic issue | OC |

---

### Deployment-Relevant Strengths

#### Strength 1: Verified multi-hop logical inference chains
- **Dimension(s):** IO
- **Observation:** Examples in the sample demonstrate multi-step deductive chains that require chaining several conditional rules before a conclusion can be evaluated. The Yale varsity team scenario (story 408) chains four universal conditionals before the False label for "Jack is bad at mid-range shots" can be derived; the Size Town scenario (story 486) chains six sequential implications.
- **Deployment relevance:** For the deployment's crisp-contradiction detection sub-task (e.g., explicit numeric contradictions), FOLIO's multi-hop classical logic coverage is genuinely relevant as a lower-bound proxy for a model's ability to chain explicit rules. A model that performs poorly here is almost certainly unfit for deployment.
- **Datapoint citations:**
  - [D13] Example 4 (yale-nlp/FOLIO, split=train, label=False): "No trick-shot artist in Yale's varsity team struggles with half court shots. Everyone on Yale's varsity team is someone who struggles with half court shots or who successfully shoots a high percentage of 3-pointers." — Four chained universals required to reach False verdict.
  - [D6] Example 11 (yale-nlp/FOLIO, split=train, label=False): "Everything in Size Town is big or small. All big things in Size Town are heavy. All small things in Size Town are light. All heavy things in Size Town are still. All light things in Size Town are unstable." — Six-hop chain ending in a compound disjunctive conclusion.

#### Strength 2: Full operator coverage including exclusive disjunction and implication
- **Dimension(s):** IO
- **Observation:** The sampled examples confirm FOLIO's documented operator coverage: negation (¬), conjunction (∧), inclusive and exclusive disjunction (∨, ⊕), implication (→), and quantifiers (∀, ∃) all appear throughout the sample, often combined within single premises.
- **Deployment relevance:** Defense specification contradictions often hinge on biconditional or disjunctive requirements ("A or B, but not both"). FOLIO's operator breadth ensures a tested model has been exposed to these logical structures in at least a minimal sense.
- **Datapoint citations:**
  - [D12] Example 2 (yale-nlp/FOLIO, split=train, label=Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Shows conjunction + implication + negation combined.
  - [D15] Example 21 (yale-nlp/FOLIO, split=train, label=False): "¬(FocusedOn(clyde, futuristicSubject) ∧ FocusedOn(clyde, vocationalSubject))→ ¬(FocusedOn(clyde, futuristicSubject) ∧ FocusedOn(clyde, vocationalSubject) ∨ (Enjoy(clyde, dressingUp, oldFashionedClothing)…)" — Complex nested negation and disjunction.

#### Strength 3: Well-balanced three-way label distribution confirmed in sample
- **Dimension(s):** OO, OC
- **Observation:** Of the 57 sampled examples, True/False/Uncertain labels are all substantially represented, consistent with the documented near-equal split (~38.5% True majority in test set). The sample includes clear True examples (Ex. 1, 12, 31, 48, 53), clear False examples (Ex. 4, 11, 17, 29, 30, 37, 38, 47), and many Uncertain examples, with labels verified by inference engine.
- **Deployment relevance:** A model trained or evaluated on FOLIO is unlikely to collapse to a binary classifier, which is minimally necessary for downstream use in detecting "possibly conflicting but not definitively" requirement relationships.
- **Datapoint citations:**
  - [D14] Example 16 (yale-nlp/FOLIO, split=train, label=True): "All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports." — True label from 6-premise chain, inference-engine verified.
  - [D25] Example 50 (yale-nlp/FOLIO, split=train, label=Uncertain): "Each building is tall. Everything tall has height." with conclusion "All buildings are magnificent." — Uncertain because "magnificent" is not derivable from stated premises — good illustration of the undecidability semantics.

#### Strength 4: Self-contained English prose — no modality mismatch
- **Dimension(s):** IF
- **Observation:** All examples are written in grammatical English prose with no images, tables, audio, or non-English content. Premises and conclusions are short declarative sentences amenable to direct text input.
- **Deployment relevance:** The deployment is text-only English, so there is no input modality mismatch. This is the one dimension where FOLIO is well-aligned.
- **Datapoint citations:**
  - [D4] Example 28 (yale-nlp/FOLIO, split=train, label=False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency." — Clean English declarative prose.
  - [D8] Example 34 (yale-nlp/FOLIO, split=train, label=True): "Everything is either outside the solar system or in the solar system. Nothing outside the solar system has the Sun as its star." — Unambiguous English prose.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: All premises are fully and explicitly stated — the inverse of the deployment's core challenge
- **Dimension(s):** IO, IC
- **Observation:** Every example in the sample provides a complete, self-contained premise set. No example requires a model to recognize that a referenced external authority (standard, specification, convention) carries implicit constraints. When domain facts are needed, they are added directly as explicit premises. This is confirmed across the entire reviewed sample without exception.
- **Deployment relevance:** The deployment's highest-priority challenge is detecting latent contradictions where one side of the conflict is implicit in a referenced standard (MIL-STD, IEEE) not restated in the document. FOLIO systematically excludes this challenge by design. A model that achieves high FOLIO accuracy may still completely fail to invoke implicit domain constraints — and FOLIO provides no signal for this capability.
- **Datapoint citations:**
  - [D1] Example 1 (yale-nlp/FOLIO, split=train, label=True): "No plants are fungi. Mushrooms are fungi." — Complete logical world in two sentences; no external knowledge needed.
  - [D3] Example 3 (yale-nlp/FOLIO, split=train, label=Uncertain): "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac." — All constraints explicitly stated; nothing implicit.
  - [D5] Example 22 (yale-nlp/FOLIO, split=train, label=Uncertain): "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered. All PRC nationals are entitled to national social insurance coverage." — Even geopolitical facts are restated as premises rather than assumed.

#### Concern 2: Zero engineering-domain vocabulary or domain-grounded latent contradiction content
- **Dimension(s):** IC
- **Observation:** The full sample of 57 examples contains no examples involving thermal budgets, timing requirements, bus bandwidth, interface parameters, tolerances, power dissipation, signal integrity, mass/volume allocations, or any other systems-engineering domain. Domains present include: sports, consumer products, biology, film, geography, social policy, personal habits, philosophy of logic, and pop culture. Even examples that touch adjacent technical domains (aviation, software) remain fully domain-neutral.
- **Deployment relevance:** The deployment's highest-value cases are latent contradictions that require physics- and systems-engineering-grounded reasoning. FOLIO provides no coverage of this content whatsoever. FOLIO accuracy scores will be construct-irrelevant for this sub-task.
- **Datapoint citations:**
  - [D10] Example 23 (yale-nlp/FOLIO, split=train, label=Uncertain): "The world's only major large passenger aircraft manufacturers are Boeing and Airbus. All American Airlines planes are from the world's major large passenger aircraft manufacturers." — Aviation adjacent but entirely domain-neutral; no technical specifications.
  - [D9] Example 46 (yale-nlp/FOLIO, split=train, label=Uncertain): "Everyone that knows about breath-first-search knows how to use a queue. If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is." — Software domain but fully explicit; no MIL-STD, IEEE, or technical constraint vocabulary.
  - [D7] Example 43 (yale-nlp/FOLIO, split=train, label=True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." — Meta-logical content; no engineering domain.

#### Concern 3: Single self-contained story per example — no cross-document or multi-context reasoning
- **Dimension(s):** OF, IO
- **Observation:** Every example in the sample is structurally a single story with one consolidated premise set and one or more conclusions derived from that single context. No example requires a model to hold multiple documents or premise sets in context simultaneously and detect a contradiction between them. The benchmark's structural unit is the (premise_set, conclusion) pair.
- **Deployment relevance:** Cross-document reasoning — tracing a requirement in a system-level SRD against a constraint in a subsystem spec or ICD — is the deployment's central use case. FOLIO cannot measure this capability at all. Performance on FOLIO provides no evidence about cross-document reasoning.
- **Datapoint citations:**
  - [D21] Example 5 (yale-nlp/FOLIO, split=train, label=Uncertain): "All Yale students at the event are college students. Everyone at the event is a Yale student or a Harvard student. Susan is at the event…" — Single event/world; all premises in one consolidated set.
  - [D2] Example 2 (yale-nlp/FOLIO, split=train, label=Uncertain): "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises. … Mike works in this tech company." — Single company "world"; all context in one premise block.

#### Concern 4: Output is bare True/False/Uncertain label — no natural-language explanation or confidence grade
- **Dimension(s):** OO, OF
- **Observation:** Every example in the dataset has exactly one of three string labels: "True", "False", or "Uncertain". The schema confirms no explanation field, no rationale field, no confidence field, and no mechanism to produce or evaluate natural-language descriptions of why a conclusion holds or fails. The NL and FOL columns provide input but no output explanatory structure.
- **Deployment relevance:** The deployment explicitly requires natural-language explanations of the conflict mechanism paired with a confidence grade. Bare True/False/Uncertain labels are described as explicitly non-actionable. FOLIO's evaluation apparatus cannot assess this requirement at all.
- **Datapoint citations:**
  - [D11] Example 55 (yale-nlp/FOLIO, split=train, label=False): "TikTok is a social media application, and it is not ideal for preteens." — Label is simply "False"; no explanation of why the disjunctive conclusion fails is stored or evaluated.
  - [D25] Example 50 (yale-nlp/FOLIO, split=train, label=Uncertain): "Each building is tall. Everything tall has height." — Label "Uncertain" gives no indication of what additional information would resolve the undecidability, which is a hard requirement for this deployment's uncertainty outputs.

---

#### MAJOR

#### Concern 5: Annotation errors and NL/FOL inconsistencies observed in sample
- **Dimension(s):** OC
- **Observation:** Several examples in the sample contain apparent annotation errors: (a) Ex. 57 (story 362) has a contradiction between NL ("Matt does not invest in the public stock market regularly") and FOL (InvestInRegularly(matt, publicStockMarket) as a ground fact) along with a missing closing parenthesis in a FOL formula; (b) Ex. 52 (story 337) uses "John" in the NL premises but "jim" in the FOL; (c) Ex. 36 (story 422) has a missing closing parenthesis in the FOL for Lily's premise; (d) Ex. 10 (story 391) has an extra closing parenthesis in the last FOL premise; (e) Ex. 20 (story 395) has a double negation in the NL ("No satin-finish lipsticks in the set do not have 'rosewood' in its official description") that may not parse as intended.
- **Deployment relevance:** These errors in a 57-example sample suggest the annotation quality, while generally high, is not error-free. For a deployment where ground-truth label reliability directly calibrates trust in the benchmark as a proxy, annotation errors undermine the evidentiary value of FOLIO accuracy scores.
- **Datapoint citations:**
  - [D17] Example 57 (yale-nlp/FOLIO, split=train, label=False): "Matt does not invest in the public stock market regularly. Matt likes financial risks." (NL) vs. "InvestInRegularly(matt, publicStockMarket)" (FOL) — NL and FOL directly contradict on whether Matt invests.
  - [D18] Example 52 (yale-nlp/FOLIO, split=train, label=True): "Either John is a professional basketball player and he never exercises…" (NL uses "John") vs. "¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))" (FOL uses "jim") — Name mismatch.
  - [D16] Example 36 (yale-nlp/FOLIO, split=train, label=True): "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — Parenthesis closed inside the In() predicate rather than after it, producing syntactically malformed FOL.
  - [D27] Example 57 (yale-nlp/FOLIO, split=train, label=False): "∀x (SpendAt(x, alotOfMoney, casino) ∨ (∃y (¬(y=casino) ∧ BettingGame(y) ∧ SpendAt(x, aLotOfMoney, y)) → AtRiskOf(x, gamblingAddiction))" — Missing closing parenthesis on existential quantifier scope.
  - [D20] Example 13 (yale-nlp/FOLIO, split=train, label=False): "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." — Double negation in NL ("No … do not have") creates potential ambiguity about intended logical content.

#### Concern 6: Domain-neutral general knowledge content — systematic construct-irrelevant variance for the deployment
- **Dimension(s):** IC
- **Observation:** The sample spans consumer products (lipstick, watches, brand products), pop culture (Harry Potter, TikTok, Meta), sports (basketball, Yale varsity), entertainment (films, TV), political philosophy (communism, planned economy), and casual social scenarios (travel planning, party food). No example is recognizably from technical specification, requirements engineering, or defense/aerospace domains. Even the economics example (story 252, Russian embargo) uses general macroeconomic reasoning, not engineering domain logic.
- **Deployment relevance:** Every topic in FOLIO introduces construct-irrelevant variance relative to the deployment. A model could learn topic-specific heuristics from FOLIO that do not transfer to technical specification reasoning. FOLIO accuracy measures general logical reasoning in familiar narrative registers, not reasoning in the normalized "shall/should" requirements-language register used by defense engineers.
- **Datapoint citations:**
  - [D23] Example 6 (yale-nlp/FOLIO, split=train, label=Uncertain): "Everyone at the business conference who is an ardent communist prefers state ownership of the means of production." — Political philosophy scenario with no engineering relevance.
  - [D22] Example 38 (yale-nlp/FOLIO, split=train, label=False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination." — Consumer/social scenario; contemporary brand reference.
  - [D26] Example 7 (yale-nlp/FOLIO, split=train, label=Uncertain): "Andy Chang is from Hong Kong." — Named individual from Wikipedia; general-knowledge prose.

#### Concern 7: Annotators are CS students/researchers — no systems engineering expertise represented
- **Dimension(s):** OC
- **Observation:** As confirmed by the YAML documentation (Q108, Q111, Q122, Q123), annotators are CS students with formal FOL training. The sample content reflects their background: CS/software examples (story 448 on BFS/queues, story 180 on C++/Python), academic and social settings dominate. No annotator with aerospace, defense, ICD, or requirements engineering background is documented.
- **Deployment relevance:** Ground-truth labels in FOLIO are correct for closed-world logical provability from stated premises — but this is a fundamentally different correctness criterion from "would a practicing systems engineer recognize this as a latent contradiction involving an implicit domain constraint?" The annotator pool lacks the expertise to evaluate the deployment's actual task.
- **Datapoint citations:**
  - [D9] Example 46 (yale-nlp/FOLIO, split=train, label=Uncertain): "Everyone that knows about breath-first-search knows how to use a queue." — CS-domain content consistent with annotator background; no engineering specification domain.
  - [D14] Example 16 (yale-nlp/FOLIO, split=train, label=True): "All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports." — Accurate label from logical provability perspective, but annotators have no basis to evaluate domain-convention conflicts in engineering specifications.

---

#### MINOR

#### Concern 8: Short-story input format — no evaluation of long-context or multi-section document handling
- **Dimension(s):** IF
- **Observation:** Premises in the sample range from 2 sentences (Ex. 1, Ex. 12, Ex. 50) to approximately 8–9 sentences (Ex. 2, Ex. 21, Ex. 57). No example approaches the multi-thousand-word, multi-section input format of a real specification document. The benchmark does not evaluate any form of long-document processing.
- **Deployment relevance:** Target documents are 20,000–250,000+ words. FOLIO's short stories (estimated 50–200 tokens per example) cannot assess whether a model maintains reasoning quality at the document lengths encountered in deployment. This is a structural gap in IF, though the benchmark documentation already acknowledges it.
- **Datapoint citations:**
  - [D1] Example 1 (yale-nlp/FOLIO, split=train, label=True): "No plants are fungi. Mushrooms are fungi." — Two-sentence premise set; represents minimal possible input complexity relative to deployment documents.
  - [D2] Example 2 (yale-nlp/FOLIO, split=train, label=Uncertain): Full premises span approximately 7 sentences and ~180 words — still orders of magnitude shorter than a system-level SRD.

#### Concern 9: "Uncertain" label semantics do not match deployment's actionable uncertainty requirement
- **Dimension(s):** OO
- **Observation:** FOLIO's "Uncertain" (labeled "Uncertain" in the data, not "Unknown" as in some documentation) means the conclusion is not provable in either direction from the stated closed-world premises — formal undecidability. In the deployment, an "Uncertain" output must be accompanied by a statement of what additional information would resolve the ambiguity (e.g., "the content of MIL-STD-461F Section 4.3 is needed to determine if this requirement conflicts"). These are different concepts with different user actions required.
- **Deployment relevance:** Models evaluated on FOLIO's Uncertain label learn to recognize closed-world undecidability, not to reason about what missing information would resolve an open-world conflict. An "Uncertain" output without a resolution path is described as a tool failure for this deployment.
- **Datapoint citations:**
  - [D25] Example 50 (yale-nlp/FOLIO, split=train, label=Uncertain): "Each building is tall. Everything tall has height." with conclusion "All buildings are magnificent." — Uncertain because "magnificent" is not in the premise vocabulary at all; no resolution path is possible or expected in FOLIO's framework.
  - [D5] Example 22 (yale-nlp/FOLIO, split=train, label=Uncertain): "Mei is at the Franco-China diplomatic conference… Either Mei is a North Korean and can have medical bills partially covered, or neither is true." — Uncertain because Mei's nationality is underdetermined; in the deployment context, this would require a statement like "the specific text of section X would resolve this."

#### Concern 10: Some NL content uses real named entities that may create Wikipedia contamination confounds
- **Dimension(s):** IC
- **Observation:** Several WikiLogic examples reference real-world entities by name: Michael O'Donnell (British physician/broadcaster, story 70), Bobby Flynn (Australian Idol contestant, story 89), the Croton River (story 12), Oxford Circus (story 205), and PSO J318.5−22 (rogue planet, story 377). LLMs that have processed Wikipedia may have seen related content.
- **Deployment relevance:** In the deployment context, this contamination concern is somewhat less relevant since the deployment goal is not benchmark leaderboard performance — but it does mean FOLIO scores may overestimate reasoning capability for novel technical content that LLMs have not encountered.
- **Datapoint citations:**
  - [D26] Example 7 (yale-nlp/FOLIO, split=train, label=Uncertain): "Andy Chang directed EndGame. Andy Chang is from Hong Kong." — Real or Wikipedia-plausible person; LLMs may have pretraining signal about this entity.
  - [D24] Example 29 (yale-nlp/FOLIO, split=train, label=False): "The only types of mammals that lay eggs are either platypuses or echidnas. … Grebes lay eggs. Grebes are not platypuses and also not echidnas." — Uses real biological facts from Wikipedia; model may answer from world knowledge rather than logical inference.

---

### Content Coverage Summary

The 57 sampled examples span a wide range of everyday and academic topics: sports (basketball, Olympic athletes), consumer technology (TikTok, Meta, products), biology (mammals, plants, fish), geography (New York, London, Guilin), film and media, economics (monetary policy, embargo), philosophy (inductive/deductive reasoning), and social scenarios (family, travel, parties). Two examples touch CS/software domains (BFS/queues; C++/Python projects) but remain fully domain-neutral.

Every example is structured as a compact self-contained "world" with 2–9 explicit premises followed by one conclusion to be evaluated as True, False, or Uncertain. Premises are grammatical English prose supported by parallel FOL annotations using standard logical operators (∧, ∨, ⊕, →, ¬, ∀, ∃). The register is informal general English, completely absent of requirements-language conventions ("shall," "should," standards identifiers).

A small number of annotation quality issues are observable in the sample: at least one NL/FOL name inconsistency (John vs. jim in story 337), one NL/FOL semantic inconsistency (Matt's investment status in story 362), and several FOL parenthesis errors (stories 362, 391, 422). These suggest the annotation process, while largely rigorous, is not error-free at the individual example level.

---

### Limitations

- **Sample size:** 57 examples from 1,001 training examples (~5.7%). The observed annotation error rate (~3–4 examples with identifiable issues) may not be representative of the full dataset.
- **Test split not accessible:** The HF schema shows only `train` and `validation` splits publicly; the test split (226 examples) is not in the viewer. Benchmark accuracy results in the literature are reported on test; this analysis covers only training examples.
- **No validation split reviewed:** The 203 validation examples were not sampled; topic or complexity distribution may differ.
- **HybLogic vs. WikiLogic proportions:** The sample may oversample one pipeline; the relative proportion of the two pipeline types in the 57 examples was not directly verifiable from the data alone.
- **FOL annotation correctness:** Syntactic issues in the FOL were identifiable by inspection, but semantic correctness of FOL translations (NL–FOL alignment) cannot be fully assessed without running the inference engine.
- **Explanation quality:** FOLIO has no explanation field; the downstream scoring module cannot assess the quality of model-generated explanations from this dataset, only classification accuracy.