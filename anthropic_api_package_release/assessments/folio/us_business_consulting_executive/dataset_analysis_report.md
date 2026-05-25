## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (default config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO | Ex.1 (story_id=271) | True | "No plants are fungi. Mushrooms are fungi." — "No plants are mushrooms." | Minimal 2-premise syllogism; domain-free categorical reasoning | IO, IC |
| D2 | FOLIO | Ex.28 (story_id=252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency... There is an embargo on Russian foreign trade goods." | Closest to business domain content in sample; still a closed formal logical puzzle with no quantitative metrics | IC |
| D3 | FOLIO | Ex.57 (story_id=362) | False | "People who like financial risks invest in the public stock market regularly or enjoy gambling regularly. If people invest in the public stock market regularly, then they read the Wall Street Journal and other newspapers regularly to keep updated on financial metrics." | Uses financial-domain vocabulary superficially; logic structure identical to non-business examples | IC, IO |
| D4 | FOLIO | Ex.6 (story_id=423) | Uncertain | "Everyone at the business conference is either an investor or an entrepreneur. None of those at the business conference who enjoy the opportunity of starting a business prefer a planned economy." | Business-themed surface vocabulary masking pure categorical deduction; no business reasoning required | IC |
| D5 | FOLIO | Ex.2 (story_id=376) | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises... Mike works in this tech company." | Tech-company framing; reasoning purely about personality traits as formal predicates | IC |
| D6 | FOLIO | Ex.14 (story_id=436) | False | "All of this brand's products are either produced in China or in the US. All of this brand's products produced in China are labeled... G-910 is a product of this brand." | Supply-chain vocabulary; conclusion is purely a logical deduction from closed-world rules, no real supply-chain knowledge | IC |
| D7 | FOLIO | Ex.3 (story_id=180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac." | Self-contained narrative; no domain knowledge required or applicable | IO |
| D8 | FOLIO | Ex.11 (story_id=486) | False | "Everything in Size Town is big or small. All big things in Size Town are heavy... The bird is in Size Town and it is not both heavy and still." | Fully abstract fictional-world taxonomy; epitomizes closed-world design | IO, IC |
| D9 | FOLIO | Ex.8/19/30 (story_id=482) | Uncertain/Uncertain/False | "If someone in Potterville yells, then they are not cool. If someone in Potterville is angry, then they yell... Harry, who lives in Potterville either yells or flies." | Fantasy fictional world; single story_id generates multiple conclusions — all evaluated as deductive classification | IO, OO |
| D10 | FOLIO | Ex.16 (story_id=346) | True | "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes... If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Multi-step syllogistic chain; label True by deductive closure | IO |
| D11 | FOLIO | Ex.43 (story_id=393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning... Modus Ponens is a component of a major part of reasoning rule." | Ironically, FOLIO uses inductive/deductive reasoning as narrative content, but evaluates it through deductive classification only | IO |
| D12 | FOLIO | Ex.22 (story_id=475) | Uncertain | "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered. All PRC nationals are entitled to national social insurance coverage. Everyone in the Franco-China diplomatic conference is either a PRC national or a French national." | Geopolitical and policy vocabulary; all reasoning is closed-world categorical deduction | IC |
| D13 | FOLIO | Ex.4/18/32 (story_id=408) | False/Uncertain/False | "No trick-shot artist in Yale's varsity team struggles with half court shots... Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." | Same story yields 3+ distinct conclusions all scored as discrete True/False/Uncertain labels | OO, OF |
| D14 | FOLIO | Ex.36 (story_id=422) | True | "All customers in James' family who subscribe to AMC A-List are eligible to watch three movies every week without any additional fees... Lily is in James' family; she watches TV series in cinemas." | Consumer-services framing; logic is purely closed-world set membership | IC |
| D15 | FOLIO | Ex.46/47 (story_id=448) | Uncertain/False | "Everyone that knows about breath-first-search knows how to use a queue. If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is." | Computer-science professional vocabulary; entirely closed-world deductive | IC |
| D16 | FOLIO | Ex.13/51 (story_id=395) | False/False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable... ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Consumer product details used as predicate placeholders; no product domain knowledge required | IC |
| D17 | FOLIO | Ex.55 (story_id=477) | False | "All social media applications containing chat features are software... TikTok is a social media application, and it is not ideal for preteens." | TikTok named but reasoning requires no actual knowledge of TikTok; named entity is a logical constant only | IC |
| D18 | FOLIO | Ex.50 (story_id=284) | Uncertain | "Each building is tall. Everything tall has height." — "All buildings are magnificent." | Minimal 2-premise example demonstrating Unknown label for unprovable conclusions | OO |
| D19 | FOLIO | Ex.9 (story_id=264) | Uncertain | "No television stars are certified public accountants. All certified public accountants have good business sense." — "All television stars have good business sense." | Business-adjacent vocabulary; Unknown because the premises don't entail the conclusion | OO |
| D20 | FOLIO | Ex.38 (story_id=425) | False | "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination... James has a car or works at Meta." — "James is a student." | Meta/tech employer named; logic is purely closed-world | IC |
| D21 | FOLIO | Ex.52 (story_id=337) | True | "No athletes never exercise. All professional basketball players are athletes... Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." — "Jim is not a Knicks player." | Contains minor internal inconsistency (premises refer to "John" but conclusion and FOL refer to "Jim") | OC |
| D22 | FOLIO | Ex.31 (story_id=60) | True | "All buildings in New Haven are not high. All buildings managed by Yale Housing are located in New Haven... Tower A is managed by Yale Housing." — "Tower A is low." | 7-premise chain with recognizable US place names; closed-world deductive | IO |
| D23 | FOLIO | Ex.34 (story_id=377) | True | "Everything is either outside the solar system or in the solar system... If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." | Scientific/astronomical vocabulary; multi-step deductive chain; no astronomy knowledge needed | IC |
| D24 | FOLIO | Ex.21 (story_id=381) | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing... If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up." | Complex 6-premise chain; demonstrates benchmark's structural diversity | IO |
| D25 | FOLIO | Ex.56 (story_id=27) | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin. Yangshuo is not a district in Guilin." — "Kowloon District is in Hong Kong." | Conclusion is entirely unrelated to premises; Unknown because nothing can be deduced | OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Clean English prose with natural logical connective phrasing
- **Dimension(s):** IF
- **Observation:** All 57 examples are grammatically correct, well-formed American English sentences. Logical connectives are expressed in idiomatic forms ("either-or," "if...then," "some," "all") rather than formal symbolic notation, matching the register of professional business writing at the sentence level.
- **Deployment relevance:** The consulting deployment requires text-only English input and output. There is zero script, modality, or encoding mismatch between the benchmark and deployment. This is a genuine, if narrow, strength.
- **Datapoint citations:**
  - [D10] Example 16 (story_id=346, label=True): "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports." — Demonstrates natural quantifier phrasing ("all," "no") that mirrors business writing conventions.
  - [D3] Example 57 (story_id=362, label=False): "If people invest in the public stock market regularly, then they read the Wall Street Journal and other newspapers regularly to keep updated on financial metrics." — Natural conditional phrasing in a quasi-business context.

#### Strength 2: Multi-step reasoning chains with documented depth up to 7+ steps
- **Dimension(s):** IO
- **Observation:** Several examples in the sample require extended chains of inference. The story_id=408 examples (D13) involve 5-premise chains with exclusive disjunctions at each step. Story_id=381 (D24) and story_id=448 (D15) require tracking 6–7 premises simultaneously. This multi-step structure corresponds to the deductive sub-component of consulting argument chains.
- **Deployment relevance:** While deductive reasoning is only a minor component of the consulting task, the benchmark's documented difficulty (GPT-4 near-chance on HybLogic) confirms it provides a non-trivial floor assessment for that sub-component.
- **Datapoint citations:**
  - [D13] Examples 4/18/32 (story_id=408): "No trick-shot artist in Yale's varsity team struggles with half court shots. Everyone on Yale's varsity team is someone who struggles with half court shots or who successfully shoots a high percentage of 3-pointers. Everyone on Yale's varsity team who successfully shoots a high percentage of 3-pointers is solid at shooting 2-pointers. No one on Yale's varsity team who is solid at shooting 2-pointers is bad at mid-range shots." — 5-premise chain requiring careful tracking of quantifier scope.
  - [D24] Example 21 (story_id=381, label=False): "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing. If people are fascinated by the history of the Renaissance and other past eras, then they attend Renaissance fairs regularly." — 6-premise chain with nested implications.

#### Strength 3: Three-way label taxonomy catches absence-of-evidence cases
- **Dimension(s):** OO
- **Observation:** The True/False/Unknown trichotomy is a genuine strength relative to binary benchmarks: "Unknown" correctly captures conclusions that are neither provable nor disprovable from given premises. This mirrors the consulting need to distinguish "this follows from the evidence," "this contradicts the evidence," and "the evidence is silent on this."
- **Deployment relevance:** Although the full output ontology is misaligned for the consulting use case, the Unknown category's logic — acknowledging what cannot be inferred from available premises — maps conceptually to epistemic humility in evidence-based business arguments.
- **Datapoint citations:**
  - [D18] Example 50 (story_id=284, label=Uncertain): "Each building is tall. Everything tall has height." — "All buildings are magnificent." — Unknown because "magnificent" is not derivable, illustrating that silence of evidence is a distinct epistemic state.
  - [D25] Example 56 (story_id=27, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin. Yangshuo is not a district in Guilin." — "Kowloon District is in Hong Kong." — Unknown because the premises contain no information about Kowloon or Hong Kong.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Zero business domain knowledge in any content — including surface business-themed examples
- **Dimension(s):** IC
- **Observation:** The 57 sampled examples confirm the documented design choice: even examples using business-adjacent vocabulary (financial risks, stock market, business conference, supply chain, tech company) require zero real-world business knowledge to solve. Every reasoning step is derivable purely from the closed-world premises. Real business content — financial metrics, valuation, competitive dynamics, regulatory context — is entirely absent.
- **Deployment relevance:** The consulting deployment requires LLMs to retrieve, weigh, and integrate real-world financial metrics, sector benchmarks, and competitive dynamics. The most business-adjacent example in the sample (D2, D3) still treats business concepts as arbitrary predicate labels, not as knowledge domains requiring domain expertise.
- **Datapoint citations:**
  - [D2] Example 28 (story_id=252, label=False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. A country cannot simultaneously regulate the exchange rate and successfully control inflation. The introduction of an embargo on foreign trade goods in a country leads to a sharp decrease in exports." — Despite macroeconomic vocabulary, the answer is derived by pure closed-world deduction; no economics knowledge is needed or tested.
  - [D3] Example 57 (story_id=362, label=False): "People who like financial risks invest in the public stock market regularly or enjoy gambling regularly. If people invest in the public stock market regularly, then they read the Wall Street Journal and other newspapers regularly to keep updated on financial metrics." — "Wall Street Journal" and "financial metrics" appear as opaque predicate labels; no financial knowledge is engaged.
  - [D4] Example 6 (story_id=423, label=Uncertain): "Everyone at the business conference is either an investor or an entrepreneur. None of those at the business conference who enjoy the opportunity of starting a business prefer a planned economy." — Business framing is pure decoration; the reasoning is a syllogism about set membership.
  - [D6] Example 14 (story_id=436, label=False): "All of this brand's products are either produced in China or in the US. All of this brand's products produced in China are labeled... None of this brand's products that are returned by customers are sold at Walmart." — Supply-chain vocabulary, but the conclusion ("G-910 is a product returned by customers") is determined entirely by the internal rules, not by any knowledge of retail or supply-chain practices.

#### Concern 2: Entire output ontology is a discrete classification label — no natural language generation evaluated
- **Dimension(s):** OO, OF
- **Observation:** Every example in the dataset terminates in a True/False/Uncertain label. The schema confirms no free-text output field exists. The dataset structure (premises → conclusion → label) is structurally incapable of evaluating open-ended argument construction, narrative coherence, executive-audience framing, or objection anticipation. Multiple conclusions from a single story (D9, D13) are each scored independently as classification labels with no mechanism for evaluating how arguments are synthesized or communicated.
- **Deployment relevance:** The consulting deployment requires the model to produce a complete, structured, partner-reviewable business case narrative — a long-form text output. FOLIO's evaluation infrastructure is entirely classification-based and cannot produce or evaluate any component of that output form.
- **Datapoint citations:**
  - [D9] Examples 8/19/30 (story_id=482): Three distinct conclusions from the Potterville story — "Harry is cool" (Uncertain), "Harry is not cool" (Uncertain), "Harry is a wizard or angry" (False) — each independently classified. There is no mechanism for synthesizing these into a coherent argument or evaluating how they would be framed for an audience.
  - [D13] Examples 4/18/32 (story_id=408): Three conclusions from the Yale basketball story scored as separate classification labels (False, Uncertain, False). No evaluation of how a consultant would present these findings or structure them for a client.
  - [D18] Example 50 (story_id=284, label=Uncertain): "Each building is tall. Everything tall has height." — "All buildings are magnificent." — A single sentence suffices as the entire output; no narrative structure, evidence selection, or audience calibration is possible or evaluated.

#### Concern 3: Reasoning type coverage gap — no inductive, abductive, analogical, or rhetorical reasoning
- **Dimension(s):** IO
- **Observation:** All 57 examples are strictly deductive: given fully specified closed-world premises, determine if the conclusion is entailed, contradicted, or undetermined. Not a single example requires inferring a general principle from partial observations (inductive), identifying the best explanation for a pattern (abductive), drawing on analogous cases (analogical), or calibrating an argument to an audience (rhetorical). Even the one example that uses reasoning-type vocabulary as content (D11, story_id=393) evaluates it through deductive classification.
- **Deployment relevance:** The user explicitly confirmed that strict deductive reasoning is a small minority of the consulting task. The bulk is inductive (market sizing from partial data) and abductive (best-explanation inference from business signals). FOLIO provides zero signal on these dominant reasoning modes.
- **Datapoint citations:**
  - [D8] Example 11 (story_id=486, label=False): "Everything in Size Town is big or small. All big things in Size Town are heavy. All small things in Size Town are light. All heavy things in Size Town are still." — Paradigmatic closed-world deduction; no incompleteness, uncertainty, or explanatory inference.
  - [D11] Example 43 (story_id=393, label=True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." — The benchmark uses inductive reasoning as a named category in premises but evaluates whether a conclusion about Modus Ponens follows deductively. The irony is instructive: the benchmark cannot evaluate the reasoning type it names.
  - [D7] Example 3 (story_id=180, label=Uncertain): "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac." — Closed world, binary choice, fully specified — nothing analogous to inferring market opportunity from partial signals.
  - [D1] Example 1 (story_id=271, label=True): "No plants are fungi. Mushrooms are fungi." — Minimal syllogism; represents the simplest form of the benchmark's only task type.

---

#### MAJOR

#### Concern 4: Ground-truth labels defined by FOL inference engine, not professional judgment
- **Dimension(s):** OC
- **Observation:** Labels in the dataset are determined by FOL prover output, verified by CS students with formal logic training. The annotator pool (documented as native-English CS undergraduates/graduates) has no overlap with the consulting deployment's evaluative standard: engagement partner professional judgment. The 34.16% accuracy gap between FOL experts and non-experts (documented in the YAML) means the benchmark's human-performance ceiling is a specialist logic skill, not a proxy for professional business reasoning.
- **Deployment relevance:** The user's ground truth is whether an engagement partner would present the output to a client. FOLIO's ground truth is whether an FOL prover returns True/False/Unknown. These two standards are structurally orthogonal. A model that scores well on FOLIO (correct deductive classification) may produce outputs that fail partner review for poor framing, weak evidence selection, or inappropriate confidence level.
- **Datapoint citations:**
  - [D19] Example 9 (story_id=264, label=Uncertain): "No television stars are certified public accountants. All certified public accountants have good business sense." — "All television stars have good business sense." — Labeled Uncertain because the FOL prover cannot derive this from the premises. A business-context judgment would ask whether this is a plausible claim worth investigating — a categorically different question.
  - [D21] Example 52 (story_id=337, label=True): "No athletes never exercise. All professional basketball players are athletes... Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." — "Jim is not a Knicks player." — The premises introduce "John" but the conclusion and FOL annotation refer to "Jim," suggesting a minor annotation inconsistency that the FOL prover may have resolved by treating them as separate constants. A human reviewer would flag this as an error.

#### Concern 5: Surface business/professional vocabulary masks complete absence of domain reasoning
- **Dimension(s):** IC
- **Observation:** Several examples use professional-sounding nouns and contexts (business conference, tech company, Google software engineer, Meta employee, Walmart supply chain, AMC A-List subscriptions, Rouge Dior lipsticks, Wall Street Journal). In every case, these are used purely as arbitrary labels for formal predicates. No example requires or rewards knowing what these concepts actually mean in business practice.
- **Deployment relevance:** A practitioner reviewing the benchmark might initially perceive alignment with business contexts; the surface vocabulary could create a false impression that FOLIO tests business reasoning. Closer inspection confirms the vocabulary is cosmetic — the reasoning structure is identical to abstract examples like "Size Town" (D8) or "Potterville" (D9).
- **Datapoint citations:**
  - [D15] Examples 46/47 (story_id=448): "If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is. Someone is either a seasoned software engineer interviewer at Google, has human rights, or both." — "Google" is used as a location predicate; whether Jack is a seasoned software engineer at Google follows from the FOL premises, not from any knowledge of Google's hiring practices.
  - [D20] Example 38 (story_id=425, label=False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination." — "Meta" functions as a named constant; the reasoning requires knowing nothing about Meta, high-income workers, or commuting patterns beyond the stated premises.
  - [D16] Examples 13/51 (story_id=395): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable." — "Rouge Dior" product attributes are used as arbitrary categorical predicates; no cosmetics domain knowledge is tested.

#### Concern 6: Multiple conclusions per story creates test-set redundancy that overstates coverage
- **Dimension(s):** IO, OC
- **Observation:** Three examples from story_id=408 (D13) appear in the sample (examples 4, 18, 32), three from story_id=482 (D9) (examples 8, 19, 30), two from story_id=70 (examples 17, 41), two from story_id=436 (examples 14, 42), two from story_id=395 (examples 13, 51), two from story_id=474 (examples 44, 49), and two from story_id=448 (examples 46, 47). This means a significant portion of the 1,430 examples share premise sets. A model that learns the premise set succeeds on all derived conclusions.
- **Deployment relevance:** For the consulting use case, this redundancy is doubly problematic: it concentrates test signal on a small number of narrative worlds, and it means benchmark accuracy may overstate a model's ability to generalize across diverse reasoning contexts — precisely the generalization that the consulting deployment requires.
- **Datapoint citations:**
  - [D13] Examples 4/18/32 (story_id=408): Three distinct conclusions evaluated from the same 5-premise basketball story. A model memorizing the premise set scores on all three; a model failing the structure fails all three.
  - [D9] Examples 8/19/30 (story_id=482): Three conclusions from the Potterville story (labels: Uncertain, Uncertain, False). All three share the same 7-premise set.

---

#### MINOR

#### Concern 7: Minor annotation inconsistency observed (name mismatch)
- **Dimension(s):** OC
- **Observation:** Example 52 (story_id=337) introduces "John" in the premises ("Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises") but the conclusion and FOL refer to "Jim" ("Jim is not a Knicks player"). This appears to be an annotator error not caught by the FOL prover (which would treat John and Jim as distinct constants).
- **Deployment relevance:** Isolated quality issue; unlikely to affect aggregate validity scores but suggests the annotation pipeline's NL quality check did not catch all name-consistency errors. In a consulting context, such inconsistencies in evidence presentation would fail partner review.
- **Datapoint citations:**
  - [D21] Example 52 (story_id=337, label=True): Premises: "Either John is a professional basketball player and he never exercises..." Conclusion: "Jim is not a Knicks player." FOL: "¬KnicksPlayer(jim)" — John and Jim appear to be intended as the same individual, but the FOL treats them as separate constants.

#### Concern 8: Fictional and non-US content throughout; no US business or regulatory grounding
- **Dimension(s):** IC, IO-2
- **Observation:** The sample includes fictional worlds (Potterville, Size Town), non-US geographies (Guilin, China, Russia, Franco-China diplomatic conference, Australian Idol, Bobby Flynn from Queensland, Hong Kong), and domain-specific non-business content (astronomy, biology, film, cosmetics, literature). US business regulatory or competitive contexts are entirely absent.
- **Deployment relevance:** The deployment is a US consulting firm evaluating LLMs for US business case construction. While geographic diversity is not per se a problem for a pure-logic benchmark, it underscores that no content is calibrated to US business norms, regulatory environments, or competitive dynamics — the raw material of the consulting task.
- **Datapoint citations:**
  - [D12] Example 22 (story_id=475, label=Uncertain): "All PRC nationals are entitled to national social insurance coverage. Everyone in the Franco-China diplomatic conference is either a PRC national or a French national." — Non-US geopolitical context used as predicate domain.
  - [D25] Example 56 (story_id=27, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin. Yangshuo is not a district in Guilin." — Chinese administrative geography as logical domain.
  - [D8] Example 11 (story_id=486, label=False): "Everything in Size Town is big or small." — Completely fictional world with no real-world grounding of any kind.

---

### Content Coverage Summary

The 57 sampled examples confirm FOLIO's documented design across all priority dimensions. Content is exclusively deductive — every example presents a closed set of premises and asks whether a conclusion follows, contradicts, or is undetermined by those premises. The benchmark's topical breadth (biology, astronomy, sports, technology, film, geography, consumer products, quasi-business) is entirely superficial: domain vocabulary functions as interchangeable predicate labels, not as knowledge to be tested.

The most business-proximate examples in the sample (supply chain in story_id=436, monetary policy in story_id=252, financial risks in story_id=362, business conference in story_id=423) all require zero business domain knowledge. The reasoning required is structurally identical to the abstract "Size Town" example. Named entities (Meta, Google, Walmart, Wall Street Journal, Rouge Dior) appear as logical constants with no semantic content beyond what the premises explicitly stipulate.

Label distribution in the sample: 15 True, 13 False, 29 Uncertain — slightly more Uncertain than documented test-set proportions (87/226 ≈ 38.5% True), but consistent with the documented pattern. Output form is uniformly a single-word classification label. No natural language generation, argument structure, narrative coherence, or audience calibration is evaluated anywhere in the dataset.

The benchmark is internally rigorous within its own frame: FOL annotations are consistent, premises and conclusions are well-formed English, and the closed-world evaluation is mechanically sound. The data simply does not correspond to the deployment's evaluation requirements across the four highest-priority dimensions (IO, IC, OO, OF).

---

### Limitations

1. **Sample size:** 57 examples from 1,001 training instances (~5.7% of train split). The validation split (203 examples) and undisclosed test split were not sampled. Coverage characterizations are based on this sample.

2. **No test split accessible via HF viewer:** The schema shows only `train` and `validation` splits available through the HF dataset viewer; the test split (226 examples, the primary evaluation set) is not in the accessible data. All sampled examples are from training.

3. **HybLogic vs. WikiLogic breakdown not observable from data:** The distinction between the two collection methods (template-based vs. Wikipedia-seeded) cannot be reliably determined from the examples alone without the original metadata. The documented performance difference (GPT-4 near-chance on HybLogic vs. better on WikiLogic) cannot be verified from this sample.

4. **FOL annotation quality not independently verifiable:** The FOL premises and conclusions are present in the schema but evaluating their semantic correctness requires running the Stanford CS221 inference engine, which was not done. The name inconsistency observed in D21 was detectable from NL inspection alone; other annotation issues may exist in the FOL layer.

5. **Label distribution in sample:** The 29/57 Uncertain rate in this sample (51%) is higher than the documented 61/226 ≈ 27% in the test set, suggesting either train-set distribution differs from test, or sampling variance at n=57 is significant. This limits inference about overall label balance from this sample alone.