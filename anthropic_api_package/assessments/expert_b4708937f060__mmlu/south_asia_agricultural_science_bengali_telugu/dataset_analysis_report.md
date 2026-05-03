## Dataset Analysis Report

**Dataset(s):** cais/mmlu (57 subject configurations)
**Analysis date:** 2025-07-29
**Examples reviewed:** ~175 examples across 37 configs sampled (approximately 5 per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | cais/mmlu | moral_scenarios Ex1 | A | "For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**?" | Question explicitly frames moral standards as US-specific, 2020 vintage | OC |
| D2 | cais/mmlu | high_school_us_history Ex1 | A | "The song, and the movement that it was connected to, highlight which of the following developments in the broader society in the late 1800s?" (re: "The Hayseed", US Populist movement) | US-specific historical content with no South Asian relevance | IO, IC |
| D3 | cais/mmlu | high_school_government_and_politics Ex1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | Entirely US constitutional law content | IO, IC |
| D4 | cais/mmlu | high_school_government_and_politics Ex4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president." | US-specific legislative history | IO |
| D5 | cais/mmlu | us_foreign_policy Ex4 | D | "In American government, the power to declare war rests with Congress." | US government structure; no relevance to South Asian governance or environmental policy | IO |
| D6 | cais/mmlu | us_foreign_policy Ex3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy?" | US Cold War policy — no South Asian agro-ecological relevance | IO |
| D7 | cais/mmlu | professional_law Ex1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs. The logs were being sold by a lumber company… the girl was struck by the tractor-trailer and was seriously injured." | US tort law scenario — US legal context | IO, IC |
| D8 | cais/mmlu | professional_law Ex2 | B | "An avid baseball fan learned that a local professional baseball club was conducting a baseball camp… forwarded the club a $50 registration deposit" | US contract law — US sports/cultural context | IC |
| D9 | cais/mmlu | human_aging Ex3 | C | "The age at which one can receive full benefits from social security" with answer "Has been increasing" | US Social Security system — entirely US institutional context | IC, OC |
| D10 | cais/mmlu | human_sexuality Ex1 | A | "Which of the following is the most common method of birth control for married couples in the **U.S.**" | Explicitly US demographic data | IC, OC |
| D11 | cais/mmlu | human_sexuality Ex5 | A | "From 1988 to 1990 among heterosexuals in the **US**, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" | US-specific behavioral survey data | IC, OC |
| D12 | cais/mmlu | moral_scenarios Ex2–5 | B/C/D/A | "For which of these two scenarios does the main character … do something clearly morally wrong, according to ordinary moral standards in the US as of 2020?" (repeated framing across all 5 examples) | Every moral_scenarios question frames correctness relative to US 2020 norms | OC, OO |
| D13 | cais/mmlu | global_facts Ex2 | B | "As of 2017, what fraction of the population in **India** used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%" | South Asia-referenced factual question, but static 2017 statistic | IC |
| D14 | cais/mmlu | global_facts Ex1 | A | "About what percentage of survey respondents from **China** report having paid a bribe in the last year to access public services … as of 2017?" | Global factual question but no South Asian agricultural content | IC |
| D15 | cais/mmlu | business_ethics Ex5 | A | "in many other countries, such as **Russia** and **China** civil society is far less developed than in, for instance, **Britain**" | Western-normative framing of civil society development | IC |
| D16 | cais/mmlu | high_school_european_history Ex1 | A | "The Scribbling-Machines have thrown thousands of your petitioners out of employ… Leeds Woolen Workers Petition, 1786" | Entirely European industrial history — no South Asian relevance | IO |
| D17 | cais/mmlu | high_school_european_history Ex2 | B | "What is tolerance?… Of all religions, the Christian ought doubtless to inspire the most tolerance… Voltaire, Letters on the English Nation, 1733" | European Enlightenment philosophy — no South Asian agricultural relevance | IO, IC |
| D18 | cais/mmlu | high_school_world_history Ex2 | B | "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters… British journalist William Howard Russell, My Indian Mutiny Diary, 1860" | British colonial framing of Indian history | IC, OC |
| D19 | cais/mmlu | high_school_geography Ex3 | C | "The way of life based on breeding and herding of animals that is used as a source of food, shelter, and clothing is called pastorialism" | Generic geography — no delta/wetland/aquaculture content | IO |
| D20 | cais/mmlu | high_school_geography Ex5 | A | "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric **zone model of urban form**?" | US urban planning model (Burgess model, Chicago School) | IC |
| D21 | cais/mmlu | nutrition Ex1–5 | various | "Which of the following inborn errors of metabolism gives rise to zinc deficiency?"; "What characteristic is not representative of a type IIb muscle fibre?" | Clinical/biochemical nutrition — no South Asian food system or crop nutrition content | IO |
| D22 | cais/mmlu | college_biology Ex1 | A | "In fungi, cell walls are reinforced by which of the following? (A) Chitin (B) Silica (C) Lignin (D) Collagen fibers" | General biology — not agricultural/agro-ecological | IO |
| D23 | cais/mmlu | high_school_biology Ex4 | D | "Which describes an African butterfly species that exists in two strikingly different color patterns?" | Biology question with African species reference — no South Asian agricultural relevance | IO |
| D24 | cais/mmlu | security_studies Ex1 | A | "In what ways do theories of conventional and critical social constructivism differ?" | Western IR theory — no South Asian environmental/agricultural policy content | IO |
| D25 | cais/mmlu | jurisprudence Ex1 | A | "Bill purchased a can of Sipep from the Ajax Minimart. After he finished drinking the Sipep, Bill noticed that the can contained dead insects stuck on the inside bottom of the can. In a strict product liability tort action against Ajax, Bill must prove…" | US-style product liability tort — US legal culture | IO, IC |
| D26 | cais/mmlu | sociology Ex3 | C | "Smith & Tomlinson argued that school character far outweighed ethnic background in determining educational success" | UK-centric sociological research | IC |
| D27 | cais/mmlu | international_law Ex4 | D | "Cultural relativism posits that local culture should validate the existence and practice of all human rights" | International law question — some nominal global relevance, but no South Asian agricultural law content | IO |
| D28 | cais/mmlu | high_school_macroeconomics Ex1–5 | various | "If firms that make a particular product expect its price will be lower in the future, this will cause the supply of the product to increase right now." | Generic macroeconomics — no South Asian agricultural market or agri-policy content | IO |
| D29 | cais/mmlu | elementary_mathematics Ex1 | A | "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" | US units (miles per hour) — not metric; minor cultural assumption | IC |
| D30 | cais/mmlu | high_school_statistics Ex1 | A | "The Department of Health plans to test the lead level in a specific park. Because a high lead level is harmful to children, the park will be closed if the lead level exceeds the allowed limit." | Environmental testing question, but no South Asian or agricultural context | IO |
| D31 | cais/mmlu | professional_medicine Ex2 | B | "A 31-year-old man with a 5-year history of HIV infection comes to the office because of anal pain… He says he and his partner engage in anal-receptive intercourse." | US clinical medicine scenario — Western clinical context | IC |
| D32 | cais/mmlu | college_chemistry Ex5 | A | "A substance that is NOT generally considered to be a toxic pollutant in water is (A) carbonic acid (B) a halogenated hydrocarbon (C) lead (D) mercury" | Closest approach to environmental science — but generic water chemistry, not delta/haor/saline intrusion relevant | IO |
| D33 | cais/mmlu | high_school_geography Ex1 | A | "What is the most rapidly growing religion in the United States today?" | US-centric cultural geography | IC |
| D34 | cais/mmlu | auxiliary_train Ex1 | B | "Jim watched a liquor store furtively for some time, planning to hold it up. He bought a realistic-looking toy gun for the job… On a charge of burglary, Jim's best defense would be that the liquor store was open to the public." | US criminal law scenario — US legal context, no South Asian relevance | IO, IC |
| D35 | cais/mmlu | miscellaneous Ex1 | A | "A flashing red traffic light signifies that a driver should do what? (A) stop" | US traffic law assumption (red = stop is near-universal but framed as US rule) | IC |
| D36 | cais/mmlu | world_religions Ex2 | B | "In Jainism, what is the cycle that one must liberate oneself from? (A) Punya (B) Samsara" | South Asian religion reference (Jainism) — one of very few South Asian cultural anchors in the dataset | IC |
| D37 | cais/mmlu | prehistory Ex2 | B | "The origins of Chinese civilization can be traced to: chiefdoms and states in numerous regions throughout China." | East Asian prehistory — no South Asian relevance | IO |
| D38 | cais/mmlu | high_school_world_history Ex4 | D | "Which of the following most inspired the national plan advanced by Nkrumah? … Socialism" | African postcolonial history — no South Asian agricultural relevance | IO |
| D39 | cais/mmlu | college_medicine Ex4 | D | "When preparing for the **MCAT exam**, a student begins studying electrochemical cells." | MCAT (US Medical College Admissions Test) reference — US academic system assumed | IC |
| D40 | cais/mmlu | global_facts Ex5 | A | "At the time of independence, there were already hundreds of thousands of university graduates in **India**, but hardly any at all in **Congo**." | India referenced but as a factual datapoint about independence-era education, not agro-ecological | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Universal STEM reasoning tasks provide a language-independent cross-model baseline
- **Dimension(s):** IO, OF
- **Observation:** A substantial portion of MMLU items test mathematical, logical, and physical reasoning that does not depend on cultural or geographic knowledge. Examples include abstract algebra (ring theory, group theory), college mathematics (optimization, real analysis), formal logic (predicate logic translation), and physics (electromagnetic, thermodynamic calculations). These items can serve as a culture-neutral baseline for comparing frontier vs. smaller regional models.
- **Deployment relevance:** The environmental scientist's stated goal includes cross-model comparison between frontier LLMs and smaller regional models. STEM reasoning items provide a stable substrate for this comparison even when domain-specific agricultural content is absent.
- **Datapoint citations:**
  - [D1 context] abstract_algebra Ex1 (cais/mmlu, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — Pure abstract mathematics with no cultural loading; valid cross-model comparison point.
  - [D1 context] college_mathematics Ex2 (cais/mmlu, split=test, label=B): "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" — Geometry/optimization; culturally neutral.
  - [D1 context] college_physics Ex3 (cais/mmlu, split=test, label=C): "White light is normally incident on a puddle of water (index of refraction 1.33). A thin (500 nm) layer of oil (index of refraction 1.5) floats on the surface of the puddle. Of the following, the most strongly reflected wavelength is" — Physical optics; no cultural dependency.

#### Strength 2: Some globally-framed factual items reference South Asia tangentially
- **Dimension(s):** IC
- **Observation:** A small number of items in the `global_facts` and `prehistory` configs reference India or broader South Asia, providing a minimal foothold of non-exclusively-Western content. These are sparse but confirm MMLU is not entirely US-only in geographic reference.
- **Deployment relevance:** These items are too few and too shallow to support agricultural knowledge evaluation, but they confirm that some fraction of MMLU questions touch South Asian contexts — marginally relevant for baseline comparison.
- **Datapoint citations:**
  - [D13] global_facts Ex2 (cais/mmlu, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%." — India-referenced factual question; dated (2017) and not agricultural.
  - [D40] global_facts Ex5 (cais/mmlu, split=test, label=A): "At the time of independence, there were already hundreds of thousands of university graduates in India, but hardly any at all in Congo." — India referenced as a comparative datapoint.
  - [D36] world_religions Ex2 (cais/mmlu, split=test, label=B): "In Jainism, what is the cycle that one must liberate oneself from? (A) Punya (B) Samsara" — South Asian religious tradition (Jainism) represented; one of very few South Asian cultural anchors observed across all 175+ reviewed examples.

#### Strength 3: Statistical and scientific reasoning items are moderately transferable
- **Dimension(s):** IO, OF
- **Observation:** High_school_statistics and related items test general inferential reasoning (hypothesis testing, confidence intervals, Type I/II error, sampling) at a level that is conceptually relevant to environmental science methodology universally, including for South Asian researchers. These items test skills the environmental scientist would use regardless of regional context.
- **Deployment relevance:** An environmental scientist evaluating LLMs for agricultural applications would benefit from knowing whether a model understands statistical inference, even if the specific application domains differ.
- **Datapoint citations:**
  - [D30] high_school_statistics Ex1 (cais/mmlu, split=test, label=A): "The Department of Health plans to test the lead level in a specific park. Because a high lead level is harmful to children, the park will be closed if the lead level exceeds the allowed limit… Which of the following decisions would result from the type I error?" — Environmental monitoring framing of Type I error; the content domain is health/environment, though not South Asian specific.
  - [D1 context] high_school_statistics Ex2 (cais/mmlu, split=test, label=B): "In a high school of 1650 students, 132 have personal investments in the stock market. To estimate the total stock investment… Plan I would sample 30 students at random…" — Sampling methodology reasoning, transferable.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Zero subject coverage of South Asian agro-ecology, delta farming, or wetland ecology
- **Dimension(s):** IO
- **Observation:** Across all 57 subject configurations, not a single subject in the MMLU taxonomy addresses haor wetland ecology, boro/aman/aus rice cultivation, char-land agriculture, Brahmaputra-Jamuna floodplain systems, delta hydrology, dry-land Deccan cropping (Rabi/Kharif on black/red soils), coastal aquaculture in Andhra Pradesh, or any South Asian agro-ecological subdomain. The reviewed examples confirm this: the closest environmental content observed is generic water chemistry (D32) and a lead-level park test (D30), neither of which relates to South Asian farming systems. High_school_geography items reference Burgess's Chicago-school urban zone model (D20) and US religion demographics (D33), not Asian agricultural geography.
- **Deployment relevance:** This is a complete structural gap. The deployment's primary purpose — assessing LLM knowledge of South Asian agricultural and environmental science — finds zero targeted test items in MMLU's entire 57-subject taxonomy. The benchmark cannot measure what it does not test.
- **Datapoint citations:**
  - [D19] high_school_geography Ex3 (cais/mmlu, split=test, label=C): "The way of life based on breeding and herding of animals that are used as a source of food, shelter, and clothing is called pastorialism." — Most geographically relevant agriculture item observed; covers generic pastoral farming, not South Asian systems.
  - [D32] college_chemistry Ex5 (cais/mmlu, split=test, label=A): "A substance that is NOT generally considered to be a toxic pollutant in water is (A) carbonic acid (B) a halogenated hydrocarbon (C) lead (D) mercury." — Nearest environmental science content; generic water chemistry with no connection to saline intrusion, haor ecology, or delta hydrology.
  - [D22] college_biology Ex1 (cais/mmlu, split=test, label=A): "In fungi, cell walls are reinforced by which of the following? (A) Chitin (B) Silica (C) Lignin (D) Collagen fibers." — Exemplary of biology coverage: cellular/molecular, not agro-ecological.
  - [D21] nutrition Ex1 (cais/mmlu, split=test, label=A): "Which of the following inborn errors of metabolism gives rise to zinc deficiency? (A) Acrodermatitis enteropathica." — Nutrition content is clinical biochemistry, not crop nutrition or soil science.

#### Concern 2: English-only input format directly contradicts multilingual deployment requirement
- **Dimension(s):** IF
- **Observation:** Every single example reviewed across all 37 configs is in English only. The HF metadata explicitly tags the dataset as `monolingual` with `language: en`. The schema requires English-language question strings. The deployment requires Telugu, Bangladeshi Bengali (Mymensingh dialect), and Indian Bengali as query languages. There is no mechanism within MMLU's format to accept, process, or evaluate non-English input.
- **Deployment relevance:** The elicitation confirms queries will include Telugu and Bengali in both varieties — a direct and absolute format mismatch. No workaround within MMLU's design can address this.
- **Datapoint citations:**
  - [D2] high_school_us_history Ex1 (cais/mmlu, split=test, label=A): "The song, and the movement that it was connected to, highlight which of the following developments in the broader society in the late 1800s?" — Typical English-only question format; no provision for Bengali or Telugu input.
  - [D29] elementary_mathematics Ex1 (cais/mmlu, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" — Even the most basic numeric reasoning items are framed entirely in English with US measurement units.

#### Concern 3: Moral scenarios explicitly anchor correctness in US 2020 norms — irreconcilable with South Asian OC validity
- **Dimension(s):** OC, OO
- **Observation:** The entire `moral_scenarios` config (500 test items) uses a fixed framing: "according to ordinary moral standards in the US as of 2020." This is not incidental phrasing — it is the operative definition of the correct answer for every question in this large subtask. Cultural divergence between Bangladeshi, Bangladeshi-Bengali, and US moral standards (e.g., around family hierarchy, religious obligation, land-use decisions) would produce legitimately different correct answers that this framing cannot accommodate.
- **Deployment relevance:** If the deployment includes any assessment of socially-situated reasoning — relevant for extension workers advising farmers on land use, water management, or community decisions — the US-anchored moral_scenarios labels would be actively misleading as a validity measure.
- **Datapoint citations:**
  - [D1] moral_scenarios Ex1 (cais/mmlu, split=test, label=A): "For which of these two scenarios does the main character (who uses I/me/my) do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." — US normative framing is explicit and constitutive of the label.
  - [D12] moral_scenarios Ex2–5 (cais/mmlu, split=test): "For which of these two scenarios does the main character … do something clearly morally wrong, **according to ordinary moral standards in the US as of 2020**?" — The US normative anchor appears identically in all five reviewed moral_scenarios examples, confirming it is structural, not incidental.

#### Concern 4: Ground-truth labels for human_sexuality, human_aging carry US-specific factual claims as correct answers
- **Dimension(s):** OC, IC
- **Observation:** Several items frame US-specific empirical facts (US birth control statistics, US social security eligibility age, US behavioral survey data 1988–1990) as universally correct answers. A South Asian researcher or LLM optimized for South Asian contexts would reasonably disagree with or be penalized for correctly knowing that these facts differ regionally.
- **Deployment relevance:** While these specific tasks are peripheral to agricultural science, they illustrate a systematic pattern: MMLU's "correct" answers embed US institutional and demographic facts that have no transfer validity to South Asian contexts.
- **Datapoint citations:**
  - [D10] human_sexuality Ex1 (cais/mmlu, split=test, label=A): "Which of the following is the most common method of birth control for married couples in the **U.S.**: (A) Sterilization." — Correct answer is US-specific; would differ for Bangladesh or India.
  - [D11] human_sexuality Ex5 (cais/mmlu, split=test, label=A): "From 1988 to 1990 among heterosexuals in the **US**, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women." — US-specific survey finding from 35+ years ago, embedded as a correct answer.
  - [D9] human_aging Ex3 (cais/mmlu, split=test, label=C): "The age at which one can receive full benefits from social security: (A) Is 62 (B) Is 65 (C) Has been increasing (D) Will never change." — Answer presupposes the US Social Security system.

---

#### MAJOR

#### Concern 5: US legal, political, and historical content dominates multiple large subject categories
- **Dimension(s):** IO, IC
- **Observation:** Multiple high-item-count subjects (professional_law, high_school_us_history, high_school_government_and_politics, us_foreign_policy, jurisprudence) are predominantly or exclusively US-centric. The reviewed professional_law items all involve US tort, contract, and evidence law. High_school_government_and_politics items assume US constitutional structure (First Amendment, War Powers Act, Articles of Confederation). These subjects represent a substantial portion of MMLU's total item count.
- **Deployment relevance:** These subjects are irrelevant to the South Asian agricultural deployment. An LLM performing well on US law or US government questions provides no signal about its knowledge of Bangladesh water law, Indian agricultural extension policy, or Andhra Pradesh coastal aquaculture regulation.
- **Datapoint citations:**
  - [D3] high_school_government_and_politics Ex1 (cais/mmlu, split=test, label=A): "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment." — Entirely US-specific constitutional content.
  - [D4] high_school_government_and_politics Ex4 (cais/mmlu, split=test, label=D): "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president." — US legislative history; no cross-regional transfer.
  - [D7] professional_law Ex1 (cais/mmlu, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs… the girl was struck by the tractor-trailer and was seriously injured. The girl's parents … assert a claim against the lumber company…" — US personal injury/tort law scenario.
  - [D5] us_foreign_policy Ex4 (cais/mmlu, split=test, label=D): "In American government, the power to declare war rests with Congress." — US constitutional structure.

#### Concern 6: World history and European history items frame non-Western events through colonial/Western lenses
- **Dimension(s):** IC, OC
- **Observation:** The `high_school_world_history` config includes South Asian content — specifically the 1857 Indian Uprising (Cawnpore/Kanpur massacres) — but presents it through a British colonial journalist's perspective as primary source, followed by a postcolonial historian's reframing. The correct answer (D18, label=B) is adjudicated by the benchmark. This framing of South Asian history through colonial sources, with labels set by a US academic team, represents a potential OC validity risk where Bangladeshi or Indian stakeholders may assess the "correct" answer differently.
- **Deployment relevance:** If any historical or geopolitical framing questions arise in the deployment context (e.g., framing of Bangladesh-India water disputes), this pattern of colonial-origin primary sources with US-adjudicated correctness is concerning.
- **Datapoint citations:**
  - [D18] high_school_world_history Ex2 (cais/mmlu, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters… British journalist William Howard Russell, My Indian Mutiny Diary, 1860." — Indian history presented through British colonial journalism; label set by US academic team.

#### Concern 7: Global_facts items are temporally stale (2017–2019) for a South Asian deployment context
- **Dimension(s):** IC, OC
- **Observation:** The `global_facts` config contains questions about India and other countries anchored to 2017–2019 data (internet penetration, demographic statistics). For a South Asian deployment in 2025, these figures are significantly outdated. An LLM that correctly knows 2024 India internet penetration figures would be penalized for not knowing the 2017 benchmark answer.
- **Deployment relevance:** The Mymensingh scientist is evaluating LLMs for current-context agricultural and environmental knowledge. Benchmarking against 2017 data for South Asia-relevant questions produces systematically misleading signals about contemporary model knowledge.
- **Datapoint citations:**
  - [D13] global_facts Ex2 (cais/mmlu, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? (A) 11% (B) 26% (C) 41% (D) 56%." — The 2017 figure (26%) is the correct answer; a model knowing the 2025 figure (~55%) would be penalized.
  - [D14] global_facts Ex1 (cais/mmlu, split=test, label=A): "About what percentage of survey respondents from China report having paid a bribe in the last year to access public services … as of 2017?" — Year-anchored question; staleness applies across all global_facts items.

#### Concern 8: No annotator demographic information documented; US MTurk baseline is the only human reference
- **Dimension(s):** OC
- **Observation:** The HF card tags the dataset as `annotations_creators: no-annotation`, and the paper documents only a US MTurk baseline (34.5% accuracy). No South Asian domain experts, agronomists, or environmental scientists were involved in item creation or answer validation, based on all available documentation. The graduate/undergraduate students who collected items are entirely from US institutions.
- **Deployment relevance:** For any questions that could have regionally contingent correct answers (cross-border water policy, comparative agricultural practice), the labels carry no authority for the South Asian deployment context. The user explicitly confirmed this risk for Bangladesh–India water-sharing questions.
- **Datapoint citations:**
  - [D9] human_aging Ex3 (cais/mmlu, split=test, label=C): "The age at which one can receive full benefits from social security … Has been increasing." — Illustrates how US institutional facts are treated as universally correct without regional annotation review.
  - [D12] moral_scenarios, all five reviewed examples — US 2020 normative framing repeated across the entire config without any annotation for cross-cultural validity.

---

#### MINOR

#### Concern 9: US customary units in elementary mathematics assume US educational context
- **Dimension(s):** IC
- **Observation:** Elementary mathematics items use miles per hour (D29) rather than metric units. While this is a minor issue for mathematical reasoning evaluation, it introduces an unnecessary US-centric cultural assumption into what should be culturally neutral content.
- **Deployment relevance:** Minor; the mathematical reasoning being tested is metric-neutral, but the unit choice reflects the US educational sourcing of items.
- **Datapoint citations:**
  - [D29] elementary_mathematics Ex1 (cais/mmlu, split=test, label=A): "If a freight train travels at a speed of **20 miles per hour** for 6 hours, how far will it travel?" — US customary units in an otherwise neutral math problem.

#### Concern 10: College_medicine MCAT reference assumes US higher education system
- **Dimension(s):** IC
- **Observation:** A college_medicine item references the MCAT (US Medical College Admissions Test) as a natural reference point for a study scenario, embedding US higher education assumptions into what purports to be general medical knowledge.
- **Deployment relevance:** Minor; the actual content (elaborative rehearsal psychology) is not US-specific, but the MCAT framing signals the US academic origin of the item and would be unfamiliar to South Asian medical students.
- **Datapoint citations:**
  - [D39] college_medicine Ex4 (cais/mmlu, split=test, label=D): "When preparing for the **MCAT exam**, a student begins studying electrochemical cells… The student's process is best characterized as: (D) Elaborative rehearsal." — MCAT reference embeds US academic context in a psychology-of-learning question.

#### Concern 11: High_school_geography and sociology items carry Western-normative theoretical frameworks
- **Dimension(s):** IC
- **Observation:** Geography questions use Burgess's concentric zone model (Chicago, 1920s) as the reference urban geography theory; sociology questions use UK-origin research (Smith & Tomlinson, Bowlby, Chodorow) as authoritative references. These frameworks were developed in US/UK contexts and may not describe South Asian urban or social patterns.
- **Deployment relevance:** Minor for the primary agricultural deployment; more relevant if the deployment expands to social science evaluation.
- **Datapoint citations:**
  - [D20] high_school_geography Ex5 (cais/mmlu, split=test, label=A): "Which zone contains low-income slums, ethnic ghettos, and general deterioration in **Burgess's concentric zone model of urban form**?" — Chicago School urban theory presented as authoritative geography.
  - [D26] sociology Ex3 (cais/mmlu, split=test, label=C): "Smith & Tomlinson argued that **school character** far outweighed ethnic background in determining educational success." — UK-based educational sociology as the reference frame.

---

### Content Coverage Summary

The 175+ examples reviewed span all 37 sampled configurations and confirm the documented structure: MMLU is an English-only, US/Western-institution-anchored multiple-choice benchmark. The subject matter is dominated by US academic and professional preparation content — US law (professional_law, jurisprudence), US government (high_school_government_and_politics, us_foreign_policy), US history, Western European philosophy and history, and US clinical medicine. General STEM subjects (physics, mathematics, chemistry, computer science, biology) are culturally lighter but still framed through US/Anglophone university materials.

The dataset contains no items addressing boro/aman/aus rice cultivation cycles, haor or beel wetland ecology, char-land agriculture, Brahmaputra-Jamuna floodplain dynamics, Deccan dry-land Rabi/Kharif cropping, brackishwater shrimp aquaculture, or any Bengal/Telugu-specific agro-ecological subdomain. The closest environmental science content observed is generic water chemistry and a Type I error example set in a lead-level park-testing scenario. South Asia is referenced tangentially in two global_facts items (India internet statistics 2017; India vs. Congo university graduates at independence) and one world_religions item (Jainism/samsara). The 1857 Indian Uprising appears in world_history but is framed through British colonial primary sources.

The moral_scenarios config (500 items) explicitly anchors correctness in "ordinary moral standards in the US as of 2020" — a framing that is constitutive, not incidental, and that produces direct OC invalidity for South Asian deployment. Human_sexuality and human_aging items embed US-specific demographic facts as correct answers. The auxiliary_train split contains US bar-exam-style criminal and property law questions with no non-US legal content detected.

Register throughout is formal academic English, consistent with US standardized test preparation. No dialect variation, no Bengali or Telugu script, and no colloquial register is present in any reviewed example.

---

### Limitations

1. **Sample size per config:** Only 5–6 examples were reviewed per configuration. With 100+ items per test split, subject-level coverage patterns within each config cannot be fully characterized from the sample.

2. **Unreviewed configs:** Approximately 20 of the 57 configs were not directly sampled (e.g., formal_logic, prehistory, human_sexuality, and others were sampled but some configs such as prehistory were reviewed with fewer examples). Agricultural or South Asian-adjacent outlier items within those configs cannot be ruled out from the sample alone, though the taxonomy analysis makes their presence extremely unlikely.

3. **No Telugu or Bengali text to inspect:** Because MMLU is English-only, there is no non-English text to assess for dialect, script, or register quality. The language mismatch concern is absolute and visible at the metadata level, but its practical effect on specific model evaluation cannot be further characterized from dataset content alone.

4. **Temporal staleness of global_facts:** The global_facts items are dated (2017–2019); whether any items have been updated in the HuggingFace distribution cannot be confirmed from the sample.

5. **Auxiliary_train split:** The auxiliary_train split contains structured training data in a nested format (`train` column containing a dict). The full content scope of this split was sampled but only 5 examples inspected; it appears to contain US bar-exam-style law questions, but comprehensive characterization requires larger sampling.

6. **Cross-config agricultural content:** It is theoretically possible that a small number of items in the `miscellaneous` config (500 items) or `global_facts` config address South Asian agricultural topics not represented in the 5-example sample. The sample is insufficient to rule out rare outliers, though the documented sourcing from US standardized exams makes such items structurally improbable.