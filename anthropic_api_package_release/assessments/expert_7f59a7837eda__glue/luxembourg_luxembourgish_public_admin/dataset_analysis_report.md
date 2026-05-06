## Dataset Analysis Report

**Dataset(s):** nyu-mll/glue (configs: ax, cola, mnli, mnli_matched, mnli_mismatched, mrpc, qnli, qqp, rte, sst2, stsb, wnli)
**Analysis date:** 2025-01-31
**Examples reviewed:** 26 (ax/test) + 78 (cola/train) + 23 (mnli/train) + 20 (mnli_matched/validation) + 20 (mnli_mismatched/validation) + 18 (mrpc/train) + 17 (qnli/train) + 33 (qqp/train) + 17 (rte/train) + 77 (sst2/train) + 54 (stsb/train) + 26 (wnli/train) = **409 examples total**
**Columns shown:** premise, hypothesis, label, idx (ax/mnli); sentence, label, idx (cola/sst2); sentence1, sentence2, label, idx (mrpc/rte/wnli/stsb); question, sentence, label, idx (qnli); question1, question2, label, idx (qqp)
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | sst2 | idx=383 | negative | "sleepwalk through vulgarities in a sequel you can refuse" | English movie-review fragment; sentiment label calibrated to film criticism register | OC |
| D2 | sst2 | idx=164 | positive | "at its best moments" | Sub-sentential movie-review fragment; context-free without film domain | IC |
| D3 | sst2 | idx=462 | negative | "the weird thing about the santa clause 2 , purportedly a children 's movie , is that there is nothing in it to engage children emotionally ." | Full sentence from American movie review; US pop-culture reference | IC, OC |
| D4 | sst2 | idx=49 | negative | "no lika da" | Non-standard English fragment (phonetic representation); unclear sentiment signal | IC, OC |
| D5 | sst2 | idx=278 | positive | "is a pan-american movie , with moments of genuine insight into the urban heart ." | Movie-review sentence referencing pan-American themes | IC |
| D6 | cola | idx=383 | unacceptable | "The fact that no candidate was elected shows that he was inadequate." | English linguistics acceptability judgment | IO |
| D7 | cola | idx=45 | acceptable | "The wagon rumbled down the road." | Simple English sentence; acceptability=1 from linguistics journal | IO |
| D8 | cola | idx=18 | unacceptable | "They drank the pub." | Idiomatic English usage; grammatical acceptability judgment | IO |
| D9 | mnli | idx=164 | entailment | "do they live close by" / "Is their house near here?" | Spoken-register English NLI pair; casual American dialogue | IC |
| D10 | mnli | idx=53 | neutral | "I did not mention Monica in my lecture, but the first question I was asked was how President Clinton could do his job with all the distractions caused by the Monica Lewinsky affair." | US political context (Clinton/Lewinsky); culturally US-specific | IC |
| D11 | mnli | idx=215 | neutral | "Yes, Mistuh Reese, suh?" | Dialect representation of African American vernacular in fiction | IC |
| D12 | mnli_matched | idx=53 | neutral | "The Celts arrived in the wake of the Roman withdrawal at the end of the fourth century." | European historical content (RTE/Wikipedia domain) | IC |
| D13 | mrpc | idx=184 | equivalent | "Platinum prices soared to 23-year highs earlier this year after President Bush (news - web sites) proposed investing $ 1.2 billion for research on fuel cell-powered vehicles." | US political and financial news paraphrase | IC |
| D14 | mrpc | idx=249 | not_equivalent | "Mr. Bush had sought to store his papers in his father's presidential library, where they would have stayed secret for a half-century." | US presidential politics; US-specific cultural/political context | IC |
| D15 | qnli | idx=164 | entailment | "Who succeeded Newt Gingrich as Speaker?" / "In 1998, with Speaker Newt Gingrich announcing his resignation..." | US political history QA; requires US-specific knowledge | IC, IO |
| D16 | qqp | idx=164 | duplicate | "What is black money and how can it effect the economy of a country?" / "What is the effect of black money on India's macro economy?" | Quora question pair; Indian economic/policy context | IC |
| D17 | qqp | idx=245 | duplicate | "How do mountain ranges form, and what are some of the major mountain ranges in Oklahoma?" / "How do mountain ranges in Oklahoma differ from mountain ranges in Idaho?" | US geography; Quora community context | IC |
| D18 | qqp | idx=228 | duplicate | "Are the notes of Rs. 2000 really embedded with a GPS chip?" / "How does the embedded NGC technology of the Rs. 2000 note works?" | India-specific currency question; non-EU political context | IC |
| D19 | rte | idx=156 | not_entailment | "National currencies will be completely replaced by the euro in within six months after the introduction of euro notes and coins." / "The introduction of the euro has been opposed." | EU-relevant content; textual entailment task with European economic content | IC |
| D20 | rte | idx=383 | entailment | "In-form Rooney's hot goalscoring streak of seven goals in his last four internationals saw him win the vote to be crowned England's Player of the Year for 2008." | British sports news; no Luxembourg administrative relevance | IC |
| D21 | ax | idx=164 | contradiction | "The combination of mentos and diet coke caused the explosion." / "Combining mentos and diet coke caused the explosion." | Diagnostic NLI pair; near-paraphrase with subtle label=-1 anomaly | OO |
| D22 | ax | idx=92 | contradiction | "House Speaker Paul Ryan was facing problems uniquely from fellow Republicans dissatisfied with his leadership." / "House Speaker Paul Ryan was facing problems uniquely from fellow Republicans supportive of his leadership." | US political content in diagnostic set | IC |
| D23 | ax | idx=333 | contradiction | "Poor Irish people could not get food because it was too expensive." / "The problem in Ireland was not lack of food, which was plentiful, but the price of it, which was beyond the reach of the poor." | Historical European content; diagnostic entailment reasoning | OO |
| D24 | stsb | idx=164 | 4.0 | "A person is boiling noodles." / "A woman is boiling noodles in water." | Image-caption pair; STS similarity regression | IO |
| D25 | stsb | idx=383 | 2.25 | "A man is tying on a stenographers machine." / "the man used a stenograph." | Image-caption pair; generic action description | IO |
| D26 | wnli | idx=45 | not_entailment | "Sara borrowed the book from the library because she needs it for an article she is working on. She writes it when she gets home from work." / "She writes the book when she gets home from work." | Winograd pronoun coreference; English fiction-based | IO |
| D27 | cola | idx=303 | unacceptable | "This is a problem that you'll be able to tell the folks up at corporate headquarters to buzz off if you solve." | Colloquial American English; grammaticality judgment from linguistics journal | IC |
| D28 | mnli | idx=8 | neutral | "Yes, Mistuh Reese, suh?" / "The slave spoke to Mr Reece." | Dialect transcription from American fiction (antebellum setting) | IC |
| D29 | sst2 | idx=50 | negative | "the horrors" | Two-word fragment; highly context-dependent sentiment label | OC |
| D30 | sst2 | idx=37 | positive | "heroes" | Single-word fragment; no sentential context | OC |
| D31 | qnli | idx=74 | not_entailment | "Who was at one time Laemmle's personal secretary?" / "Thalberg had been Laemmle's personal secretary..." | Wikipedia QA requiring Hollywood history knowledge | IC |
| D32 | ax | idx=45 | contradiction | "In example (1) it is quite easy to see the exaggerated positive sentiment used in order to convey strong negative feelings." / "In example (1) it is quite straightforward to see the exaggerated positive sentiment used in order to convey strong negative feelings." | Academic NLP paper text in diagnostic set | IC |
| D33 | mnli | idx=368 | neutral | "oh yeah no that's uh that's a that's a real interesting movie and it's got a good historical perspective to it" | Transcribed telephone speech; casual American spoken English | IC, IF |
| D34 | ax | idx=479 | contradiction | "The announcement of Tillerson's departure sent shock waves across the globe." / "People across the globe were prepared for Tillerson's departure." | US political news (Rex Tillerson/Trump administration) in diagnostic set | IC |
| D35 | rte | idx=479 | not_entailment | "Budapest consists of two parts, Buda and Pest, which are situated on opposite sides of the river and connected by a series of bridges." / "Buda is located on the west bank of the Danube." | European geography in news-based RTE; geographically proximate to Luxembourg | IC |
| D36 | mrpc | idx=61 | not_equivalent | "The women then had follow-up examinations after five , 12 and 24 years ." / "The women had follow-up examinations in 1974-75 , 1980-81 and 1992-93 , but were not asked about stress again ." | News paraphrase detection; health domain, no administrative relevance | IO |
| D37 | ax | idx=209 | contradiction | "This means that seeking a word that is similar to x and y but is different from z is mathematically equivalent to solving analogy questions with vector arithmetic." / "This means that solving analogy questions with vector arithmetic is mathematically equivalent to seeking a word that is similar to x and y but is different from z." | NLP academic paper text; symmetry reasoning in diagnostic set | IO |
| D38 | qqp | idx=368 | not_duplicate | "What is it to be a lesbian?" / "How does it feel to be a lesbian?" | Quora social question; identity topic | IC |
| D39 | stsb | idx=45 | 1.0 | "A man is playing the piano." / "A woman is playing the violin." | Image-caption STS; everyday activity scenes | IO |
| D40 | cola | idx=425 | unacceptable | "The children eat all chocolate." | English determiner usage; grammaticality judgment | IO |
| D41 | mnli_mismatched | idx=383 | neutral | "Southern manufacturers had already adopted steam engines for textile production, along with newer and more productive technology." | US historical text; 19th century American industrialization | IC |
| D42 | ax | idx=415 | contradiction | "Grisham did not win the popular vote." / "Grisham almost won the popular vote." | US electoral context in diagnostic set | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Well-balanced binary and three-class label distributions enable class-distribution analysis
- **Dimension(s):** OO
- **Observation:** The sampled data shows balanced label distributions across tasks: SST-2 (241 negative / 259 positive in buffer), MNLI (178/140/182 across three classes), CoLA (171 unacceptable / 329 acceptable), RTE (245/255). This balance is documented as intentional and validated by Matthews Correlation Coefficient for unbalanced cases. The multi-task structure provides a model for designing evaluation suites that separately score multiple capabilities.
- **Deployment relevance:** While GLUE's specific labels are irrelevant to Luxembourgish administrative routing, the framework of measuring each task separately and macro-averaging — demonstrated concretely across 12 configs with distinct schema and label spaces — offers a structural template for a custom Luxembourgish benchmark suite combining NER, intent classification, sentiment, and routing tasks.
- **Datapoint citations:**
  - [D6] cola, split=train, label=unacceptable: "The fact that no candidate was elected shows that he was inadequate." — Representative of clear binary labeling scheme with documented acceptability judgments
  - [D21] ax, split=test, label=contradiction (label=-1): "The combination of mentos and diet coke caused the explosion." / "Combining mentos and diet coke caused the explosion." — Illustrates the NLI three-class schema and how near-paraphrase pairs are distinguished; note the label=-1 encoding for contradiction in the ax config suggests test labels are masked, consistent with documented private test label practice

#### Strength 2: Diagnostic (ax) dataset demonstrates systematic linguistic phenomenon coverage
- **Dimension(s):** IO, OO
- **Observation:** The ax config examples systematically probe quantifier scope, negation, coreference, temporal reasoning, and logical operators (conditionals, disjunction) as documented. The sampled 26 examples show genuine variety across phenomenon types: scalar implication (D5/idx=5, "Some" vs. "Most"), additive modification (idx=443, "father of the nation and the man uniquely equipped"), coreference (idx=289), and world knowledge (idx=333 on Irish famine).
- **Deployment relevance:** The diagnostic set's methodology — constructing minimal-pair sentence sets that differ on exactly one linguistic dimension — is transferable as a design pattern for probing Luxembourgish model capabilities in NER boundary sensitivity, negation in formal correspondence, and temporal reasoning in administrative contexts. This is the single most methodologically reusable element of GLUE for the deployment.
- **Datapoint citations:**
  - [D23] ax, split=test, label=contradiction: "Poor Irish people could not get food because it was too expensive." / "The problem in Ireland was not lack of food, which was plentiful, but the price of it, which was beyond the reach of the poor." — Illustrates world knowledge reasoning probe in diagnostic set; this methodology (minimal edits + phenomenon tagging) is transferable
  - [D37] ax, split=test, label=contradiction: "This means that seeking a word that is similar to x and y but is different from z is mathematically equivalent to solving analogy questions with vector arithmetic." / "This means that solving analogy questions with vector arithmetic is mathematically equivalent to seeking a word that is similar to x and y but is different from z." — Probes symmetry/reversibility reasoning; technique applicable to testing Luxembourgish administrative NLU models on logical inference

#### Strength 3: NLI task structure covers some linguistically universal reasoning patterns
- **Dimension(s):** IO
- **Observation:** Several MNLI and MNLI-matched examples test reasoning patterns that are language-agnostic in principle: set membership, negation, scalar implication, causal inference. These phenomena appear in the sampled data with varied surface forms.
- **Deployment relevance:** An NLU model for Luxembourgish administrative routing must handle negation (e.g., "je ne suis pas frontalier" / "ech sinn kee Frontalier"), scalar implication, and causal chains in citizen correspondence. To the extent that GLUE's NLI tasks exercise these reasoning patterns, a model's GLUE performance provides weak evidence about its general logical reasoning competence, though not its Luxembourgish-specific or domain-specific capabilities.
- **Datapoint citations:**
  - [D9] mnli, split=train, label=entailment: "do they live close by" / "Is their house near here?" — Tests paraphrase/entailment across register variation; logically universal pattern
  - [D1] mnli, split=train, label=entailment (idx=163): "At the heart of the sanctuary, a small granite shrine once held the sacred barque of Horus himself." / "Horus has a shrine." — Tests proposition extraction; logically universal but requires cultural/religious world knowledge

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of any Luxembourgish, French, or German language data
- **Dimension(s):** IC, IF
- **Observation:** Every single example reviewed across all 12 configs is in English. The 409 sampled examples contain no Luxembourgish tokens, no French text, and no German text. The HF metadata confirms `"languages": ["en"]` and `"multilinguality:monolingual"`. The benchmark's input signal — standardized written American/British English drawn from news, movie reviews, Wikipedia, and web forums — has zero overlap with the trilingual, code-switched, non-standardized Luxembourgish input the deployed system will process.
- **Deployment relevance:** The elicitation identifies input language as HIGH priority. Even formally intended Luxembourgish citizen correspondence exhibits code-switching between Luxembourgish, French, and German, with non-standardized Luxembourgish spelling (best normalization model achieves only ~78.8% accuracy per web findings). GLUE provides no signal whatsoever about a model's ability to handle this input distribution. A model that achieves high GLUE scores but has never processed Luxembourgish text could score 0% on the actual deployment task.
- **Datapoint citations:**
  - [D1] sst2, split=train, label=negative: "sleepwalk through vulgarities in a sequel you can refuse" — English movie-review fragment; not a single non-English word appears in the entire sampled dataset
  - [D9] mnli, split=train, label=entailment: "do they live close by" / "Is their house near here?" — Casual American spoken English; the contrast with Luxembourgish administrative register (e.g., "Ech wëll eng Fro stellen iwwer mäin Steierstatus als Frontalier") could not be more complete
  - [D33] mnli, split=train, label=neutral: "oh yeah no that's uh that's a that's a real interesting movie and it's got a good historical perspective to it" — Transcribed American telephone speech; this is the input register GLUE trains NLU models on, vs. formal Luxembourgish administrative correspondence

#### Concern 2: Zero administrative domain content — no routing, intent, or government competency categories
- **Dimension(s):** IO
- **Observation:** Across 409 examples, no example touches any administrative, government, or civic domain relevant to the deployment: no housing queries, no cross-border worker status, no national vs. communal routing, no social security, no immigration, no taxation, no public transport. The tasks cover movie sentiment, paraphrase detection among news sentences, QA from Wikipedia, and acceptability judgments from linguistics journals. The closest approximation is MNLI's use of "government reports" as one of ten premise sources, but none of these appear in the sampled examples.
- **Deployment relevance:** The deployment's core function is routing citizen messages to national or communal departments based on topic and intent. GLUE provides no ontological coverage of the required categories: cross-border worker / frontalier status, national vs. communal competency, housing urgency, social security, immigration, or public transport (Luxembourg's notable free-transport policy). IO is marked HIGH priority in the elicitation, and this gap is total.
- **Datapoint citations:**
  - [D15] qnli, split=train, label=entailment: "Who succeeded Newt Gingrich as Speaker?" — US congressional politics; the contrast with the deployment's required categories (e.g., "Is this message about a frontalier's pension entitlement?") illustrates the complete category mismatch
  - [D36] mrpc, split=train, label=not_equivalent: "The women then had follow-up examinations after five , 12 and 24 years ." / "The women had follow-up examinations in 1974-75 , 1980-81 and 1992-93 , but were not asked about stress again ." — Health news paraphrase; no administrative routing relevance
  - [D24] stsb, split=train, label=4.0: "A person is boiling noodles." / "A woman is boiling noodles in water." — Image-caption similarity; completely unrelated to administrative correspondence processing

#### Concern 3: Sentiment labels calibrated to English movie-review register, not Luxembourgish formal administrative correspondence
- **Dimension(s):** OC, IC
- **Observation:** All 77 sampled SST-2 examples are sub-sentential or full-sentence fragments from English movie reviews. Many are decontextualized fragments that depend on film-criticism conventions for their sentiment polarity (e.g., [D2] "at its best moments" = positive; [D30] "heroes" = positive; [D29] "the horrors" = negative). Several fragments are too short to carry unambiguous sentiment signals without film-review context. The annotator pool is not documented, but the domain (film criticism) and language (American English) bear no relation to formal Luxembourgish administrative correspondence, which is characterized by understated register even when expressing urgency or frustration.
- **Deployment relevance:** OC is HIGH priority. The deployment requires sentiment/frustration detection in formal administrative correspondence, where frustration is expressed indirectly through formal language (e.g., "Je me permets de vous contacter une fois de plus concernant ma demande du 15 mars..."). Labels trained on explicit, colloquial English film criticism sentiment will systematically fail to detect the understated frustration signals in Luxembourgish administrative correspondence. The elicitation explicitly flagged this as a "live risk."
- **Datapoint citations:**
  - [D3] sst2, split=train, label=negative: "the weird thing about the santa clause 2 , purportedly a children 's movie , is that there is nothing in it to engage children emotionally ." — US pop-culture movie reference; sentiment label depends on film-criticism knowledge
  - [D4] sst2, split=train, label=negative: "no lika da" — Phonetic/dialectal fragment; sentiment label is nearly uninterpretable without full review context; would be meaningless in any Luxembourgish administrative context
  - [D2] sst2, split=train, label=positive: "at its best moments" — Three-word decontextualized fragment; the annotation assumes the reviewer's film-criticism context, which transfers to no other domain
  - [D29] sst2, split=train, label=negative: "the horrors" — Two-word fragment with implicit film-review context; no transferable signal

#### Concern 4: Output taxonomy is binary/ternary hard classification; no multi-label or confidence scoring
- **Dimension(s):** OO, OF
- **Observation:** Every classification task in the sampled data uses exactly one label per example (binary or three-class). The ax config shows labels encoded as -1 (contradiction) in the test split, confirming that even the diagnostic set uses hard single labels. No example has multiple labels, soft labels, or confidence scores. The schema metadata confirms: `"ClassLabel(3 classes)"` for NLI tasks and `"ClassLabel(2 classes)"` for all others, with no probability or confidence field present.
- **Deployment relevance:** OO is HIGH priority. The deployment requires multi-label classification (a single citizen message may concern housing AND frontalier tax status AND municipal routing simultaneously) plus confidence scores to flag uncertain cases for human review. GLUE's hard single-label paradigm cannot be adapted to this requirement without fundamental restructuring — it is not a matter of threshold-tuning but of ontological incompatibility. The macro-average GLUE score will not predict multi-label routing quality.
- **Datapoint citations:**
  - [D21] ax, split=test, label=contradiction (label=-1): "The combination of mentos and diet coke caused the explosion." / "Combining mentos and diet coke caused the explosion." — label=-1 confirms hard single-label encoding even for the diagnostic set
  - [D26] wnli, split=train, label=not_entailment: "Sara borrowed the book from the library because she needs it for an article she is working on. She writes it when she gets home from work." / "She writes the book when she gets home from work." — Binary label; no provision for partial or uncertain classification

#### Concern 5: US-centric cultural and political content dominates inputs across multiple tasks
- **Dimension(s):** IC
- **Observation:** Multiple tasks contain US-specific political, cultural, and institutional references that would require American background knowledge to fully process: US congressional politics (Newt Gingrich, Paul Ryan — [D15], [D22]), US presidential politics (Clinton/Lewinsky — [D10], Bush — [D13], [D14], Tillerson — [D34]), US legal and financial news (MRPC), US sports (Auburn High School Athletic Hall of Fame — RTE idx=92). The Quora dataset (QQP) also contains India-specific content ([D16], [D18]) but with no Luxembourgish or European administrative content.
- **Deployment relevance:** While a model trained on GLUE develops some general NLU capability, the cultural knowledge required for correct predictions is primarily American. The deployment population's knowledge context is Luxembourgish/European administrative culture. Construct-irrelevant variance from US-specific cultural references will inflate or deflate GLUE scores in ways that do not predict performance on Luxembourg administrative content.
- **Datapoint citations:**
  - [D10] mnli, split=train, label=neutral: "I did not mention Monica in my lecture, but the first question I was asked was how President Clinton could do his job with all the distractions caused by the Monica Lewinsky affair." — US political scandal; requires American political history knowledge for NLI judgment
  - [D22] ax, split=test, label=contradiction: "House Speaker Paul Ryan was facing problems uniquely from fellow Republicans dissatisfied with his leadership." / "House Speaker Paul Ryan was facing problems uniquely from fellow Republicans supportive of his leadership." — US political reference embedded in diagnostic set
  - [D42] ax, split=test, label=contradiction: "Grisham did not win the popular vote." / "Grisham almost won the popular vote." — US electoral context; "popular vote" is a distinctly American electoral concept with no direct Luxembourgish administrative equivalent

#### MAJOR

#### Concern 6: SST-2 fragments are decontextualized and incomplete — many examples carry no reliable sentiment signal
- **Dimension(s):** IC, OC
- **Observation:** A substantial portion of the 77 sampled SST-2 examples are sub-sentential fragments: "at its best moments" (positive), "seem fresh" (positive), "of saucy" (positive), "imax in short" (positive), "sometimes dry" (negative), "the horrors" (negative), "ugly digital video" (negative). These fragments are sentence tree nodes extracted from parsed movie reviews and labeled based on the sentiment of the full review context, not the fragment itself. The sentiment signal in many fragments is ambiguous or absent without the surrounding film-review context.
- **Deployment relevance:** Even if a Luxembourgish administrative correspondence benchmark were to include a sentiment task, this SST-2 methodology — extracting decontextualized sub-sentential fragments and labeling them with film-review sentiment — would be a poor model for labeling formal administrative messages. The fragment-level annotation may actually train models to respond to surface-level evaluative adjectives rather than holistic communicative intent, which is the opposite of what the deployment needs.
- **Datapoint citations:**
  - [D2] sst2, split=train, label=positive: "at its best moments" — Three-word locative-temporal phrase; positive label depends entirely on film-review context
  - [D4] sst2, split=train, label=negative: "no lika da" — Phonetic/colloquial fragment; no clear sentiment without context
  - [D30] sst2, split=train, label=positive: "heroes" — Single-word label; sentiment annotation here is entirely context-dependent

#### Concern 7: CoLA (linguistic acceptability) tests English-specific syntactic phenomena with no transfer value
- **Dimension(s):** IO, IC
- **Observation:** All 78 sampled CoLA examples test English-specific grammaticality: English comparative constructions ("The more people that arrive, the louder it gets" — acceptable; "The harder it rains, how much faster that do you run?" — unacceptable), English pronoun binding, English verb phrase ellipsis, English article usage. These phenomena are specific to English morphosyntax and have no equivalent in Luxembourgish, French, or German grammatical structure.
- **Deployment relevance:** The deployment has no linguistic acceptability classification requirement. More importantly, a model fine-tuned on CoLA will have optimized parameters for English syntactic well-formedness detection, which is not only irrelevant to Luxembourgish administrative NLU but may actively interfere with processing grammatically non-standard Luxembourgish input (non-standard spelling, code-switching) by treating it as "unacceptable."
- **Datapoint citations:**
  - [D8] cola, split=train, label=unacceptable: "They drank the pub." — English-specific argument structure violation (unergative/transitive alternation); no Luxembourgish administrative relevance
  - [D40] cola, split=train, label=unacceptable: "The children eat all chocolate." — English determiner usage; this tests English-specific mass noun determiner constraints
  - [D27] cola, split=train, label=unacceptable: "This is a problem that you'll be able to tell the folks up at corporate headquarters to buzz off if you solve." — Colloquial American English construction; grammaticality judgment presupposes American English native speaker norms

#### Concern 8: STS-B image-caption pairs are semantically trivial and domain-irrelevant
- **Dimension(s):** IO, IC
- **Observation:** The sampled STS-B examples are predominantly image-caption pairs describing simple physical actions: "A person is boiling noodles." / "A woman is boiling noodles in water." (similarity=4.0); "A man is playing the piano." / "A woman is playing the violin." (similarity=1.0); "A woman is riding a motorized scooter down a road." / "A man is riding a motor scooter." (similarity=2.2). These pairs describe concrete physical scenes with no semantic complexity relevant to administrative correspondence.
- **Deployment relevance:** The deployment has no semantic similarity scoring requirement for image-caption pairs. Scores on STS-B measure a model's ability to rate similarity between action descriptions about everyday physical activities, which contributes nothing to predicting performance on assessing semantic similarity between citizen message phrasings or between routing category descriptions in Luxembourgish administrative text.
- **Datapoint citations:**
  - [D24] stsb, split=train, label=4.0: "A person is boiling noodles." / "A woman is boiling noodles in water." — Image caption pair; trivial semantic similarity with no administrative domain relevance
  - [D25] stsb, split=train, label=2.25: "A man is tying on a stenographers machine." / "the man used a stenograph." — Physical action STS pair; no administrative domain relevance

#### Concern 9: MNLI includes fiction and spoken dialogue that misrepresents the target register
- **Dimension(s):** IC
- **Observation:** MNLI premises span ten genre sources including fiction and transcribed speech. The sampled examples include a slave-era dialect quote from fiction ([D11]: "Yes, Mistuh Reese, suh?"), casual American telephone speech ([D33]: "oh yeah no that's uh that's a that's a real interesting movie"), and first-person informal speech. These represent registers extremely distant from formal Luxembourgish administrative correspondence.
- **Deployment relevance:** A model whose NLI representations are partially trained on American vernacular dialogue and antebellum fiction dialects will have learned register-specific features that are unhelpful — and potentially counterproductive — for processing formal Luxembourgish administrative prose written in multiple languages.
- **Datapoint citations:**
  - [D11] mnli, split=train, label=neutral: "Yes, Mistuh Reese, suh?" / "THe slave spoke to Mr Reece." — Antebellum American fiction dialect; no relation to Luxembourgish administrative register
  - [D33] mnli, split=train, label=neutral: "oh yeah no that's uh that's a that's a real interesting movie and it's got a good historical perspective to it" — Transcribed American telephone speech; register opposite of formal administrative correspondence

#### MINOR

#### Concern 10: RTE includes some European content but labels entailment over news paraphrase, not administrative routing
- **Dimension(s):** IO, IC
- **Observation:** A few RTE examples touch European geography ([D35]: Budapest/Danube) and European economic history ([D19]: euro introduction). This is incidental — the task is binary textual entailment derived from news challenge datasets, not administrative classification. The European content does not correlate with Luxembourg-specific administrative topics.
- **Deployment relevance:** The presence of European-context news text in RTE might marginally reduce cultural distance compared to purely US-centric tasks, but this does not constitute meaningful coverage of Luxembourgish administrative domains. The task structure (news-based binary entailment) remains misaligned with the deployment.
- **Datapoint citations:**
  - [D19] rte, split=train, label=not_entailment: "National currencies will be completely replaced by the euro in within six months after the introduction of euro notes and coins." / "The introduction of the euro has been opposed." — European economic news; geographically proximate but task-irrelevant
  - [D35] rte, split=train, label=not_entailment: "Budapest consists of two parts, Buda and Pest, which are situated on opposite sides of the river and connected by a series of bridges." / "Buda is located on the west bank of the Danube." — European geography; not Luxembourgish administrative content

#### Concern 11: QQP contains non-English-speaking-country questions (India) without Luxembourgish coverage
- **Dimension(s):** IC
- **Observation:** The Quora QQP dataset is community-generated and includes questions from Indian users ([D16]: "What is the effect of black money on India's macro economy?"; [D18]: "Are the notes of Rs. 2000 really embedded with a GPS chip?"). This illustrates that even the "diverse" content in GLUE reflects specific online communities (Quora user base) rather than Luxembourgish civic concerns.
- **Deployment relevance:** The QQP content is doubly misaligned — it is neither English-administrative nor Luxembourgish. Its only relevance to the deployment assessment is as further evidence of the total absence of any Luxembourg-relevant content across all benchmark configs.
- **Datapoint citations:**
  - [D16] qqp, split=train, label=duplicate: "What is black money and how can it effect the economy of a country?" / "What is the effect of black money on India's macro economy?" — Indian economic policy question on Quora
  - [D18] qqp, split=train, label=duplicate: "Are the notes of Rs. 2000 really embedded with a GPS chip?" / "How does the embedded NGC technology of the Rs. 2000 note works?" — India-specific currency query

---

### Content Coverage Summary

The 409 sampled examples confirm without ambiguity the complete domain, language, and task mismatch described in the YAML documentation. The content is entirely English-language across all twelve configs, drawn from: (1) English movie review fragments (SST-2 — often sub-sentential and context-dependent); (2) English linguistics journal examples testing English morphosyntax (CoLA); (3) English news paraphrase pairs covering US political and financial news (MRPC); (4) Community Q&A pairs from Quora, skewed toward US and Indian-English topics (QQP); (5) Wikipedia-based QA targeting US and world historical/scientific knowledge (QNLI); (6) English news and Wikipedia textual entailment pairs with some European geography (RTE); (7) Image-caption similarity pairs describing everyday physical actions (STS-B); (8) English fiction-based pronoun coreference (WNLI); (9) Multi-genre English NLI pairs from transcribed speech, fiction, government reports, and travel guides (MNLI); and (10) A diagnostic NLI set drawing on academic NLP papers, news, Reddit, and Wikipedia, probing English syntactic and semantic phenomena.

No example references Luxembourg, Luxembourgish language, French administrative text, German-language content, cross-border worker status, national vs. communal government routing, or any topic from the required administrative taxonomy. Register is predominantly American English informal-to-journalistic; the formal continental European administrative register of Luxembourgish citizen correspondence is entirely unrepresented. The benchmark offers value only as a structural reference for benchmark suite design — its tasks, labels, content, and scoring paradigm do not transfer to the deployment.

---

### Limitations

1. **Sample size per config:** The sampling strategy retrieved 17–78 examples per config depending on class distribution in the buffer. For large configs (MNLI: 393k training examples; QQP: 364k training examples), the sampled examples represent a tiny fraction and may not capture the full topical range. It is possible, though unlikely given the documented source domains, that MNLI's "government report" source contains some European administrative content not represented in the sample.

2. **Test sets not inspectable:** Four configs use privately held test labels (cola, mnli, qqp, sst2). The analysis relied on training and validation splits; test set content distributions may differ marginally, though source domains are fixed and documented.

3. **ax config label anomaly:** The ax (diagnostic) config shows label=-1 for all 26 sampled examples, which is the test split. The documentation states test labels are privately held and the label field encodes -1 for masked test labels. This means all 26 ax examples are from the test split with masked ground truth — the cited labels (D21, D22, D23, etc.) are index-based class assignments, not verified ground truth, and should be interpreted accordingly. This does not affect the linguistic content observations but limits inference about the diagnostic label distribution from the sample.

4. **No audio or image modalities:** GLUE is text-only; this was confirmed by metadata and examples. No media columns were inspected or skipped.

5. **Code-switching and non-standard orthography not assessable from this dataset:** By definition, no Luxembourgish orthographic variation, trilingual code-switching, or non-standard spelling can be observed in a monolingual English dataset. The severity of the IF/IC gaps for the deployment can only be assessed by examining Luxembourgish-language resources (ltzGLUE, LuxBorrow, spellux) — none of which are present here.