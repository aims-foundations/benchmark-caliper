## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-01-31
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO | Ex. 1 (story_id=271) | True | "No plants are fungi. Mushrooms are fungi. / No plants are mushrooms." | Simple two-premise syllogism; purely formal deductive structure with no evidentiary content | IO |
| D2 | FOLIO | Ex. 28 (story_id=252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. … There is an embargo on Russian foreign trade goods." | Macro-economics scenario; premises stated as given facts, not cited evidence requiring credibility assessment | IC |
| D3 | FOLIO | Ex. 43 (story_id=393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." | Story uses "inductive reasoning" as a named category but treats it deductively — no actual inductive inference is performed | IO |
| D4 | FOLIO | Ex. 6 (story_id=423) | Uncertain | "Everyone at the business conference is either an investor or an entrepreneur. … Ho is at the business conference and prefers state ownership of the means of production." | Normative terms (planned economy, state ownership, ardent communist) appear only as predicate labels; no value judgment is required or possible | IC |
| D5 | FOLIO | Ex. 22 (story_id=475) | Uncertain | "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered. … Either Mei is a North Korean and can have medical bills partially covered, or neither is true." | Policy-adjacent content framed as pure deductive entailment; no contested empirical or value claim is assessed | IC |
| D6 | FOLIO | Ex. 2 (story_id=376) | Uncertain | "Mike works in this tech company. If Mike is not a person who wears the same flannel shirts every day, has very high energy, and is impulsive, then Mike either is very consistent and enjoys sticking to his regular routines or does not like surprises." | Multi-premise WikiLogic scenario with 7 premises; reasoning depth is high but entirely deductive | IO |
| D7 | FOLIO | Ex. 3 (story_id=180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac." | Technical CS scenario with exclusive disjunction chain; no debate-relevant argument structure | IO |
| D8 | FOLIO | Ex. 8 (story_id=482) | Uncertain | "Harry, who lives in Potterville either yells or flies. Potter, who lives in Potterville, is a wizard and flies." | Fictional fantasy premise set; content has no overlap with competitive debate argument types | IC |
| D9 | FOLIO | Ex. 2 (story_id=376) | Uncertain | "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" | FOL annotation is theorem-prover verified; labels are mechanically derived, not from human judgment of argument quality | OC |
| D10 | FOLIO | Ex. 46 (story_id=448) | Uncertain | "If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is. … Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." | Human rights framing used as deductive predicate; no normative assessment required or possible | OO |
| D11 | FOLIO | Ex. 11 (story_id=486) | False | "Everything in Size Town is big or small. … The bird is in Size Town and it is not both heavy and still." | Fully abstract fictional scenario; label is True/False/Uncertain with no sub-dimensions | OO |
| D12 | FOLIO | Ex. 28 (story_id=252) | False | "∀x (Country(x) ∧ PossibleEffectiveMonetaryPolicy(x) → SuccessfulInflationControl(x) ∧ StongNationalCurrency(x))" | Ground truth derived from FOL inference engine, not from domain expert or debate-community judgment | OC |
| D13 | FOLIO | Ex. 16 (story_id=346) | True | "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes. … If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Six-premise chain requiring multi-step deductive inference; output is single True/False/Unknown label | OF |
| D14 | FOLIO | Ex. 57 (story_id=362) | False | "People who like financial risks invest in the public stock market regularly or enjoy gambling regularly. … Matt does not invest in the public stock market regularly. Matt likes financial risks." | Complex multi-step deduction; conclusion collapses to single categorical label with no sub-scores or rationale | OF |
| D15 | FOLIO | Ex. 13 (story_id=395) | False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable. … ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Real consumer product used as topic seed; content is factual/commercial, not argumentative or evidentiary | IC |
| D16 | FOLIO | Ex. 34 (story_id=377) | True | "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." | Scientific real-world entity used as topic; premises are stated as fixed facts, not contested empirical claims | IC |
| D17 | FOLIO | Ex. 23 (story_id=108) | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus. … There exists a SpaceX commercial aircraft." | Factual world knowledge embedded as premise; no evidence citation, credibility assessment, or warrant evaluation | IC |
| D18 | FOLIO | Ex. 4 (story_id=408) | False | "No trick-shot artist in Yale's varsity team struggles with half court shots. … Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." | Same story_id generates multiple conclusions (examples 1134, 1141, 1140) — confirms single-label per conclusion structure | OF |
| D19 | FOLIO | Ex. 52 (story_id=337) | True | "No athletes never exercise. … Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." | Negation/exclusive-disjunction complexity; output remains a single binary-equivalent label | OF |
| D20 | FOLIO | Ex. 21 (story_id=381) | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing. … If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." | Long six-premise chain typical of WikiLogic track; no rhetorical, persuasive, or debate-structural elements | IO |
| D21 | FOLIO | Ex. 36 (story_id=422) | True | "Customers in James' family subscribe to AMC A-List or HBO service. … Lily is in James' family; she watches TV series in cinemas." | Everyday consumer scenario; label is machine-verified True — no qualitative feedback dimension possible | OF |
| D22 | FOLIO | Ex. 55 (story_id=477) | False | "If a social media application is addictive, then it is not ideal for preteens. TikTok is a social media application, and it is not ideal for preteens." | Contemporary tech topic; "addictive" treated as a logical predicate, not a value-laden or contested empirical claim | IC |
| D23 | FOLIO | Ex. 56 (story_id=27) | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin. … Kowloon District is in Hong Kong." | Geographic factual premises; conclusion about a completely different city is Uncertain — confirms open-world assumption | OO |
| D24 | FOLIO | Ex. 38 (story_id=425) | False | "Everyone working at Meta has a high income. … James has a car or works at Meta." | Contemporary workplace scenario; premises stated as definitional universals, not empirically disputed claims | IC |
| D25 | FOLIO | Ex. 43 (story_id=393) | True | "∀x (MajorArgumentForm(x) → (InductiveReasoning(x) ⊕ DeductiveReasoning(x))" | Inductive reasoning is modeled as a named entity/predicate; the reasoning task itself remains purely deductive | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Text-Only English Input with No Modality or Script Mismatch
- **Dimension(s):** IF
- **Observation:** All 57 sampled examples are text-based, written in standard American English with grammatically natural sentences. No audio, images, non-Latin scripts, or multilingual content appear anywhere in the sample.
- **Deployment relevance:** The deployment platform processes written cases and transcripts in English text. There is zero signal-distribution mismatch at the input form level between FOLIO and the deployment context; this dimension does not introduce construct-irrelevant variance.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Grammatically natural English, text-only, no modality concerns.
  - [D8] Example 8 (FOLIO, train, Uncertain): "Harry, who lives in Potterville either yells or flies." — Complex sentence structure rendered cleanly in standard English prose.

#### Strength 2: High Logical Complexity and Multi-Step Inference Chains
- **Dimension(s):** IO
- **Observation:** Multiple sampled examples require chaining five or more premises through conjunction, disjunction, implication, and universal/existential quantifiers. Examples 2, 16, 20, 21, 36, 43, 46, and 57 all involve four to seven distinct premises with multi-step inference requirements. This is the highest-fidelity logical-validity signal available in any natural-language benchmark.
- **Deployment relevance:** While insufficient on its own for the deployment's needs, one of the four required sub-scores (logical structure and warrant quality) does include inferential validity as a component. FOLIO provides a rigorous upper bound on that sub-dimension — if a model scores well here, its deductive validity component is demonstrably strong.
- **Datapoint citations:**
  - [D6] Example 2 (FOLIO, train, Uncertain): "Mike works in this tech company. If Mike is not a person who wears the same flannel shirts every day, has very high energy, and is impulsive, then Mike either is very consistent and enjoys sticking to his regular routines or does not like surprises." — 7-premise scenario requiring multi-step deductive inference.
  - [D20] Example 21 (FOLIO, train, False): "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing. … If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." — 6-premise WikiLogic chain.
  - [D14] Example 57 (FOLIO, train, False): "People who like financial risks invest in the public stock market regularly or enjoy gambling regularly. … Matt does not invest in the public stock market regularly. Matt likes financial risks." — Multi-step deductive chain with complex disjunction.

#### Strength 3: Mechanically Verified, Unambiguous Ground-Truth Labels
- **Dimension(s):** OC
- **Observation:** Every label in the dataset is verified by an FOL inference engine, not by human subjective judgment. Within the narrow scope of formal deductive entailment, labels are objectively correct and consistent across all examples reviewed.
- **Deployment relevance:** For the specific sub-task of checking whether a stated logical argument form is internally consistent (a sub-component of "logical structure" sub-score), FOLIO provides a reliable, reproducible signal. There is no annotator disagreement or subjective variance within its defined scope.
- **Datapoint citations:**
  - [D9] Example 2 (FOLIO, train, Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — FOL formula mechanically derived and verified; label is theorem-prover output, not human judgment.
  - [D12] Example 28 (FOLIO, train, False): "∀x (Country(x) ∧ PossibleEffectiveMonetaryPolicy(x) → SuccessfulInflationControl(x) ∧ StongNationalCurrency(x))" — Ground truth is FOL inference engine output, internally consistent and reproducible.

#### Strength 4: Diverse Topic Coverage Across WikiLogic Stories
- **Dimension(s):** IC
- **Observation:** The WikiLogic track (which dominates the sample) draws on a wide range of real-world topics: geography (Croton River, Guilin districts), science (mammals, planets, biology), economics (Russian trade embargo), technology (Meta employees, TikTok), films (EndGame, Adventures of Rusty), and consumer products (Rouge Dior lipstick, watch types). This topical breadth means the benchmark does not test a narrow domain vocabulary.
- **Deployment relevance:** While topical variety does not substitute for debate-specific content, it confirms that FOLIO does not introduce systematic domain-specific knowledge bias (e.g., only testing science or history). For any sub-component testing of domain-neutral logical validity, this breadth is a minor positive.
- **Datapoint citations:**
  - [D16] Example 34 (FOLIO, train, True): "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." — Astronomy topic seed.
  - [D2] Example 28 (FOLIO, train, False): "There is an embargo on Russian foreign trade goods." — Economic/geopolitical topic seed.
  - [D15] Example 13 (FOLIO, train, False): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable." — Consumer product topic seed.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Zero Coverage of Inductive, Evidentiary, or Evidence-Quality Reasoning
- **Dimension(s):** IO, IC
- **Observation:** Every single one of the 57 sampled examples is a closed-world deductive entailment problem: premises are stated as definitional universals or given facts, conclusions are derived by formal inference rules, and no example contains cited sources, empirical uncertainty, evidence recency, or warrant credibility. The word "evidence" does not appear in any premise or conclusion. No example models contested empirical claims.
- **Deployment relevance:** The deployment user explicitly identified evidence quality (source credibility, recency, miscontextualization, cherry-picking) as the *highest-weight* sub-dimension. FOLIO contains literally zero content of this type. An LLM that scores at ceiling on FOLIO may still be completely unable to assess whether a card is outdated, miscut, or from a non-credible source. The benchmark provides no signal whatsoever for this top-priority deployment requirement.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Premises are stated definitional facts with no source, citation, or credibility dimension.
  - [D2] Example 28 (FOLIO, train, False): "There is an embargo on Russian foreign trade goods." — An empirically contested geopolitical claim is stated as a given logical axiom, stripping all evidence quality assessment from the task.
  - [D17] Example 23 (FOLIO, train, Uncertain): "The world's only major large passenger aircraft manufacturers are Boeing and Airbus. … There exists a SpaceX commercial aircraft." — Factual claims are encoded as fixed premises; no warrant or source credibility evaluation is possible or required.

#### Concern 2: Total Absence of Debate-Specific Argument Structures
- **Dimension(s):** IO
- **Observation:** None of the 57 sampled examples contains any structure resembling a disadvantage (DA), counterplan (CP), kritik (K), topicality shell (T), theory argument, burden-of-proof claim, or impact calculus. The argument structures present are exclusively syllogistic/predicate-logic chains. The tokens "disadvantage," "counterplan," "kritik," "topicality," "solvency," "impact," "turn," "burden," "framework," "value," "criterion" do not appear in any premise or conclusion in the sample.
- **Deployment relevance:** The deployment user identified DAs, CPs, kritiks, and burden-shifting as "first-class argument types" required by the system. FOLIO's ontology has zero overlap with these structures. A model evaluated on FOLIO cannot demonstrate any capability for recognizing or scoring these debate-specific moves.
- **Datapoint citations:**
  - [D7] Example 3 (FOLIO, train, Uncertain): "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac." — Exclusively syllogistic structure; no debate argument structure present.
  - [D20] Example 21 (FOLIO, train, False): "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing." — Extended WikiLogic syllogism; no debate-structural elements.
  - [D3] Example 43 (FOLIO, train, True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." — "Inductive reasoning" is used as a deductive predicate label, not as an actual inductive argument structure.

#### Concern 3: Output Space Categorically Mismatched to Deployment Requirements
- **Dimension(s):** OO, OF
- **Observation:** Every example produces exactly one of three outputs: True, False, or Uncertain. No example produces a sub-score breakdown, a qualitative rationale, a pairwise comparison, or any circuit/format-conditioned evaluation. The schema confirms this: the only label column is a single string field. Multiple conclusions from the same story (e.g., story_id=408 generates examples 1134, 1140, 1141) each receive their own independent True/False/Uncertain label with no cross-conclusion comparison.
- **Deployment relevance:** The deployment requires: (a) separate sub-scores across logic, evidence, relevance, and persuasiveness; (b) qualitative coaching feedback; (c) pairwise comparison for rebuttal practice; and (d) format/circuit-conditioned scoring. FOLIO's output space cannot approximate any of these. Benchmark performance metrics (accuracy over True/False/Unknown) are structurally uninformative for assessing whether a model can provide coaching feedback or rank arguments comparatively.
- **Datapoint citations:**
  - [D13] Example 16 (FOLIO, train, True): "All professional athletes spend most of their time on sports. … If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." — Six-premise reasoning chain collapses to single label "True"; no sub-scores, no rationale.
  - [D18] Example 4 / story_id=408 (FOLIO, train, multiple): "No trick-shot artist in Yale's varsity team struggles with half court shots." — Same premises generate three separate conclusions (examples 1134, 1140, 1141) each with independent True/False/Uncertain labels; no head-to-head comparative ranking structure exists.
  - [D21] Example 36 (FOLIO, train, True): Label is machine-verified "True" — no coaching explanation, no weakness identification, no qualitative feedback dimension.

#### Concern 4: Annotator Population Completely Mismatched to Deployment Quality Standards
- **Dimension(s):** OC
- **Observation:** All labels are derived from a formal FOL inference engine, not from human judges with debate expertise. The human annotators are CS students with formal FOL training. The deployment's correctness standard is defined by NSDA norms, TOC circuit paradigms, and coaching staff rubrics — a community with entirely different domain knowledge and quality intuitions.
- **Deployment relevance:** Whether an argument is "strong" in competitive debate is a community-norm judgment that varies by circuit and format. FOLIO's theorem-prover labels have no relationship to these norms. A label of "True" on a FOLIO example says nothing about whether a debate judge would find the corresponding argument persuasive, well-warranted, or topically responsive.
- **Datapoint citations:**
  - [D9] Example 2 (FOLIO, train, Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Label is theorem-prover output; a debate judge paradigm plays no role in determining this label.
  - [D12] Example 28 (FOLIO, train, False): Ground truth "False" is derived mechanically from FOL inference over stated premises about Russia's monetary policy; no debate-community judgment is involved or approximated.

#### Concern 5: No Value-Laden or Normatively Contested Content
- **Dimension(s):** IC
- **Observation:** As explicitly documented in the benchmark design and confirmed across all 57 examples, FOLIO deliberately avoids normatively contested content. Even examples that name politically adjacent entities (state ownership of means of production, North Korean nationals, Russian trade embargoes) use these as deductive predicate labels requiring no value judgment. The content is cleansed of the very quality — genuine normative contestation — that defines LD and Congressional debate.
- **Deployment relevance:** LD and Congressional debate center on value claims where reasonable people disagree (e.g., "civil liberties outweigh national security"). The system must score argument structure and warrant quality for these claims without taking sides. FOLIO's total avoidance of such content means it cannot measure any aspect of a model's capacity to assess value-laden arguments without injecting normative bias.
- **Datapoint citations:**
  - [D4] Example 6 (FOLIO, train, Uncertain): "Everyone at the business conference is either an investor or an entrepreneur. … Ho is at the business conference and prefers state ownership of the means of production." — "Planned economy" and "state ownership" appear as logical predicates, not contested value claims; no normative assessment is required.
  - [D5] Example 22 (FOLIO, train, Uncertain): "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered." — Social policy claim treated as a definitional universal; no value dispute is present or assessed.
  - [D10] Example 46 (FOLIO, train, Uncertain): "Every person who has human rights is entitled to the right to life and liberty. … Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." — Human rights framing is purely a logical predicate; no normative weight is assigned or evaluated.

---

#### MAJOR

#### Concern 6: No Pairwise or Comparative Argument Structure
- **Dimension(s):** OO, OF
- **Observation:** All 57 examples evaluate a single conclusion against a fixed premise set in isolation. No example involves two competing arguments, a rebuttal structure, or a head-to-head comparison. Multiple conclusions from the same story (story_id=408: examples 1134, 1140, 1141; story_id=482: examples 1406, 1407, 1408) are scored independently, not comparatively.
- **Deployment relevance:** The deployment explicitly requires pairwise argument comparison for rebuttal practice. This is a structural requirement with no analog in FOLIO's design. There is no way to derive pairwise rankings or contrastive strength assessments from FOLIO's True/False/Uncertain labels.
- **Datapoint citations:**
  - [D18] Example 4 / story_id=408 (FOLIO, train, False and Uncertain): Three separate conclusions from the same premise set receive independent labels (False, Uncertain, False); no comparative ranking between these conclusions is provided or evaluable.
  - [D11] Example 11 (FOLIO, train, False): "The bird is in Size Town and it is not both heavy and still." — Single isolated conclusion scored in isolation; no opposing argument structure present.

#### Concern 7: Register Mismatch — Formal Logical Universals vs. Competitive Debate Discourse
- **Dimension(s):** IC, IF
- **Observation:** FOLIO premises are written as formal logical universals ("All X are Y," "No X are Z," "If X then Y") with named constants (Mike, Amy, Jack, Ho, Mei). This register is characteristic of logic textbooks. Competitive debate arguments — even structurally similar ones — use hedged empirical language ("Studies show that…," "According to [author], the [mechanism] causes…," "Extend the [impact] — it outweighs because…"). The surface form difference is substantial.
- **Deployment relevance:** A model fine-tuned on or evaluated by FOLIO learns to process clean formal-universal sentence structures that differ significantly from the hedged, warrant-heavy, evidence-citing register of actual debate arguments. Even the logical structure sub-dimension of the deployment involves discourse forms not represented in FOLIO.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Formal universal statements characteristic of logic textbooks, not debate speech transcripts.
  - [D24] Example 38 (FOLIO, train, False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination." — Clean formal universals; no hedging, no citation, no warrant-evidence structure typical of competitive debate.
  - [D22] Example 55 (FOLIO, train, False): "If a social media application is addictive, then it is not ideal for preteens. TikTok is a social media application, and it is not ideal for preteens." — Contemporary content but rendered as definitional logical axioms, not contested empirical claims with evidence.

---

#### MINOR

#### Concern 8: Small Dataset Size Limits Statistical Reliability for Sub-Population Analysis
- **Dimension(s):** IF
- **Observation:** The full dataset contains only 1,204 examples (train + validation; test set is withheld on HuggingFace). Even if the benchmark were otherwise appropriate for the deployment, the small size makes it difficult to analyze performance by topic domain, reasoning depth, or label distribution with statistical confidence.
- **Deployment relevance:** If used as a proxy for any sub-component of deployment scoring, the small dataset limits the ability to distinguish model performance on harder vs. easier reasoning chains or to detect systematic failure modes across topic categories.
- **Datapoint citations:**
  - [D13] Example 16 / [D1] Example 1: Both are training examples from a dataset totaling ~1,000 train examples — insufficient to disaggregate by the multiple format × circuit × argument-type combinations required by the deployment.

#### Concern 9: Potential Pretraining Data Contamination for WikiLogic Examples
- **Dimension(s):** IC
- **Observation:** WikiLogic stories are based on Wikipedia article topics and may share surface patterns with LLM pretraining corpora (as acknowledged in the benchmark documentation). Examples like Ex. 15 (Oxford Circus, John Nash), Ex. 17 (Michael O'Donnell), and Ex. 27 (Bobby Flynn, Australian Idol) use real named entities drawn from Wikipedia.
- **Deployment relevance:** If an LLM is being evaluated for deployment on this benchmark, strong performance on WikiLogic examples may reflect memorized factual patterns rather than genuine reasoning capability — making benchmark performance an overestimate of the model's actual logical reasoning ability on novel debate arguments.
- **Datapoint citations:**
  - [D15] Example 15 (FOLIO, train, Uncertain): "Oxford Circus is a road junction connecting Oxford Street and Regent Street. … John Nash designed Oxford Circus." — Named real-world entities likely present in Wikipedia-derived pretraining data.
  - [D8] Example 27 (FOLIO, train, Uncertain): "Bobby Flynn finished 7th while competing on Australian Idol. … Bobby Flynn was born in Queensland." — Specific biographical facts from Wikipedia; potential contamination risk.

---

### Content Coverage Summary

The 57 sampled examples represent FOLIO's two collection tracks faithfully. **WikiLogic examples** (the majority) cover a diverse range of real-world topics seeded from Wikipedia: geography (Guilin districts, Croton River, New Haven/Manhattan buildings), scientific entities (rogue planets, mammalian egg-laying, sea eels), consumer products (Rouge Dior lipstick, Moonwatch), technology companies (Meta, Google, TikTok, tech company with "Mike"), sports (Yale varsity basketball, Olympic athletes), media (Harry Potter, films, Bobby Flynn), and geopolitical scenarios (Russia embargo, Franco-China conference). **HybLogic examples** (the minority) use more abstract or archetypal scenarios with named constants: a fictional town "Potterville" with wizards, "Size Town" with abstract properties, and syllogism-heavy chains about cooking talent or financial risk.

In every case, the content is structured as a closed-world logical puzzle: premises are stated as definitional universals or given facts, and the task is to determine whether a conclusion follows by formal deduction. No example contains cited evidence, disputed empirical claims, normative arguments, rhetorical moves, or debate-specific structural elements. The register is consistently that of a logic textbook — formal universal statements, named constants, and clean implications — rather than the hedged, evidence-citing, warrant-heavy language of competitive debate.

The label distribution in the sample shows roughly equal representation of True (approximately 30%), False (approximately 30%), and Uncertain (approximately 40%), consistent with the documented test set distribution (87/78/61). All labels are mechanically verified by an FOL inference engine.

---

### Limitations

1. **Test split not available on HuggingFace**: The HF repository exposes only train (1,001 examples) and validation (203 examples). The test split (226 examples) is withheld. All analysis is based on training examples; any systematic differences in the test split cannot be assessed from this sample.

2. **Sample size (57/1,001 train)**: The reviewed sample is 5.7% of the training split. While the logical structure and content register are highly consistent across all examples reviewed, rare topic categories or unusual reasoning patterns in the other 94% cannot be ruled out from this sample alone.

3. **No FOL formula evaluation**: The `premises-FOL` and `conclusion-FOL` columns contain parallel formal logic annotations that were reviewed visually but not formally executed against an inference engine. Annotation errors in the FOL (noted as a known quality issue in the benchmark documentation) cannot be detected from the natural language alone.

4. **No audio, image, or speech-transcript examples**: The deployment involves potentially processing speech transcripts from debate rounds. Whether the clean prose register of FOLIO examples generalizes to ASR-transcribed speech artifacts (disfluencies, mid-sentence corrections, spread delivery) cannot be assessed from this dataset.

5. **HybLogic vs. WikiLogic proportion in sample**: The sample appears heavily WikiLogic-weighted (consistent with the 304 vs. 183 story split documented in the benchmark). HybLogic patterns — which tend to be more structurally regular and potentially more learnable by fine-tuned models — may be underrepresented in the reviewed examples.