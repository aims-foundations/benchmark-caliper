## Use Case
A Luxembourgish public administration system uses an LLM evaluated on topic classification, named entity recognition, intent detection, and sentiment analysis to process citizen correspondence. The system automatically routes messages to appropriate government departments (national or municipal) and prioritizes urgent or frustrated submissions. The benchmark under evaluation is GLUE (2019), an English-only, US-context multi-task NLU benchmark with no porting to Luxembourgish or related administrative domains.

## Target Population
Civil servants in Luxembourgish government agencies who process digital correspondence written by a linguistically diverse citizenry. Luxembourg's population includes a large cross-border worker constituency (~47% of the workforce), multilingual residents using Luxembourgish, French, and German in variable proportions, and citizens accustomed to code-switching even in formal written communication. The target language, Luxembourgish (Lëtzebuergesch), is low-resource and lacks standardized spelling norms in common practice. Sub-national routing distinctions (state vs. communal authority) add a further layer of administrative specificity.

## Elicitation Responses

Q1 [IO]: Citizen feedback to Luxembourgish government agencies likely spans topics specific to local governance — such as cross-border worker issues, multilingual administrative procedures (French/German/Luxembourgish coexistence), housing, transport like the free public transit policy, or EU institutional matters. Does the benchmark's topic coverage address these Luxembourg-specific administrative domains, or does it focus on other areas not typical of local government correspondence?
A1: The deployment requires distinguishing cross-border workers from residents (a legally critical classification), flagging cost-of-living and housing queries as high-priority given current political sensitivity, and differentiating between national and municipal competencies to route messages correctly. None of these topic categories appear in GLUE's task suite, which covers sentiment, paraphrase, textual entailment, and general QA sourced from English-language news and web corpora.

Q2 [IC]: Citizen messages to public administration are often written in non-standard Luxembourgish — code-switching with French or German, informal orthography, or dialect forms. Does your deployment need to handle this kind of mixed or non-standardized language input, or can you assume messages are written in reasonably standard Luxembourgish prose?
A2: Even formally intended correspondence will exhibit significant orthographic variation in Luxembourgish, along with frequent alternation between French- and German-derived lexical variants for the same concept (e.g., "Administratioun" vs. "Verwaltung"). The model must be robust to this mixed-language, non-standardized input. A benchmark built on standardized news or legal English text is therefore not representative of actual input signal the deployed system will encounter.

Q3 [OC]: For sentiment and frustration detection specifically, were the benchmark's sentiment or tone labels validated by people familiar with Luxembourgish civil communication norms — for example, the typically understated or formal register citizens use when writing to government bodies — or were they produced by a broader, potentially non-Luxembourg-resident annotator pool?
A3: The user acknowledges that ground-truth sentiment labels ideally should be validated by annotators familiar with Luxembourg's administrative culture, but concedes that low-resource constraints may force reliance on out-of-domain labels initially. A human-in-the-loop audit mechanism is included so that civil servants can correct erroneous "urgent" or "frustrated" flags, allowing the routing logic to self-calibrate over time. This confirms that OC is a recognized live risk in the deployment.

Q4 [OO]: Your system triggers automated routing and prioritization decisions based on classified intent and sentiment — does the benchmark's assumption of a single hard label per message match your routing logic, or do you require multi-label or confidence-scored outputs?
A4: The routing logic requires multi-label classification, since a single message may concern multiple departments or topics simultaneously. Confidence scores are used to flag uncertain cases for human review rather than forcing a single top-label decision. GLUE's hard single-label scoring paradigm therefore does not match the output structure the deployment needs.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | GLUE's task ontology (paraphrase, entailment, general QA, English news sentiment) contains no categories for Luxembourg-specific administrative domains — cross-border worker status, national vs. municipal routing, housing urgency — identified as the core classification requirements. |
| IC | HIGH | Deployment input is Luxembourgish-French-German code-switched text with non-standardized orthography; GLUE instances are drawn from standardized English corpora with no overlap in script, language, or content type, introducing severe construct-irrelevant variance. |
| IF | HIGH | The target language is low-resource Luxembourgish with non-Latin-norm orthographic variation and frequent trilingual mixing; GLUE is English-only text, creating a fundamental input signal mismatch. |
| OO | HIGH | The deployment requires multi-label outputs with confidence scoring and combined intent-plus-sentiment categorization, while GLUE's scoring assumes single hard labels per task; the output taxonomy is also designed for a culturally unrelated English context. |
| OC | HIGH | Sentiment and urgency ground-truth labels in GLUE were not validated by annotators familiar with Luxembourgish administrative register; the user explicitly flagged this as a live risk, and the target population's understated formal tone norms are not represented in the annotator pool. |
| OF | MODERATE | Both deployment and benchmark use text-in / label-out pipelines, which partially aligns; however, GLUE's hard single-label output format conflicts with the deployment's need for confidence-scored and multi-label outputs, warranting moderate concern. |

## Flagged Gaps

1. **Luxembourgish as a low-resource language**: No GLUE task covers Luxembourgish. Downstream web search should investigate whether any NLU benchmarks exist for Luxembourgish (lb/ltz ISO code), including any academic or government-sponsored corpora from the University of Luxembourg or Luxembourg Institute of Science and Technology (LIST).

2. **Trilingual code-switching corpora**: The deployment's input signal is code-switched Luxembourgish/French/German. Web search should investigate benchmarks or evaluation sets specifically designed for code-switched or multilingual low-resource input in Romance/Germanic contact scenarios.

3. **Administrative/government correspondence datasets in Luxembourg**: GLUE contains no public administration text. Search should target whether the Luxembourg government's digital transformation program (e.g., MyGuichet, CTIE) has produced any annotated citizen correspondence datasets or NLP evaluation resources.

4. **Cross-border worker classification as an NLP category**: This highly deployment-specific category (resident vs. frontalier status) has no precedent in general NLU benchmarks. Flagged as a gap requiring custom annotation or expert elicitation rather than benchmark substitution.

5. **Annotator representativeness for Luxembourgish administrative sentiment**: GLUE's SST-2 sentiment labels come from English movie review annotators. Search should investigate whether any sentiment or tone datasets exist that were annotated by Luxembourgish civil servants or individuals familiar with formal European continental administrative register.

6. **National vs. municipal routing taxonomy**: The distinction between state and communal competency is specific to Luxembourg's administrative structure and absent from all known general NLU benchmarks. This represents a construct gap that cannot be filled by benchmark substitution alone and should be flagged for the region YAML synthesis stage.

7. **Sub-national variation within Luxembourg**: While Luxembourg is geographically small, linguistic and cultural variation between the Minett (southern industrial) region, the Ardennes north, and Luxembourg City's highly international population may affect both input language norms and sentiment calibration. This sub-national dimension is unaddressed by GLUE.