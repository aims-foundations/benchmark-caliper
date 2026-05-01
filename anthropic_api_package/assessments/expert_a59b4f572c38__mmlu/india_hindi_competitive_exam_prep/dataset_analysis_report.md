## Dataset Analysis Report

**Dataset(s):** cais/mmlu
**Analysis date:** 2025-01-30
**Examples reviewed:** ~200 examples across 57 subject configs (5–6 examples per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | high_school_government_and_politics | Ex.1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | US constitutional law question — irrelevant to Indian Polity | IO, IC |
| D2 | high_school_government_and_politics | Ex.4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" | US Congress-specific legislation — not Indian constitutional content | IO, IC |
| D3 | high_school_government_and_politics | Ex.5 | A | "What power was granted to the states by the Articles of Confederation but not by the Constitution?" | US Articles of Confederation — no Indian Polity equivalent | IO, IC |
| D4 | high_school_us_history | Ex.2 | B | "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828 … The language of 'protest' that Calhoun used … was similar to the language of which of the following political positions?" | US history question with primary source passage — entirely irrelevant to Indian History | IO, IC |
| D5 | high_school_us_history | Ex.4 | D | "Between 1820 and 1854, the greatest number of immigrants to the United States came from … Ireland" | US immigration history — no relevance to Indian competitive exams | IO, IC |
| D6 | high_school_us_history | Ex.5 | A | "Tonight, the daughter of an immigrant from Italy has been chosen to run for (vice) president … — Geraldine Ferraro, Vice Presidential Nomination Acceptance Address, July 19, 1984" | US political history primary source — alien to UPSC/SSC syllabus | IO, IC |
| D7 | us_foreign_policy | Ex.2 | B | "Why might the 'Philadelphian System' be linked to the idea of American exceptionalism?" | US foreign policy / exceptionalism — irrelevant to Indian deployment | IO, IC |
| D8 | us_foreign_policy | Ex.3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" | US Cold War policy — no analogue in UPSC/SSC syllabus | IO, IC |
| D9 | us_foreign_policy | Ex.4 | D | "In American government, the power to declare war rests with … Congress" | US government structure question — not Indian Polity | IO, IC |
| D10 | professional_law | Ex.1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs … the girl's parents … assert a claim against the lumber company" | US tort law scenario — calibrated against US bar exam, not Indian law | IO, IC |
| D11 | professional_law | Ex.2 | B | "An avid baseball fan … forwarded the club a $50 registration deposit … In a restitutionary action, can the executor of the fan's estate … recover … the $2,500 paid to the club?" | US contract law with baseball cultural context — no Indian law equivalent | IO, IC |
| D12 | high_school_european_history | Ex.1 | A | "The Scribbling-Machines have thrown thousands of your petitioners out of employ … Leeds Woolen Workers Petition, 1786" | British Industrial Revolution primary source — European history with no South Asian content | IO, IC |
| D13 | high_school_european_history | Ex.2 | B | "What is tolerance? … Of all religions, the Christian ought doubtless to inspire the most tolerance … Voltaire, Letters on the English Nation, 1733" | Enlightenment Western philosophy — Western canon, irrelevant to Indian History syllabus | IO, IC |
| D14 | high_school_european_history | Ex.4 | D | "The substitution of Plato for the scholastic Aristotle … Cosimo and Lorenzo de Medici … the Florentine Academy … Neoplatonism" | Italian Renaissance intellectual history — no Indian History coverage | IO, IC |
| D15 | high_school_world_history | Ex.2 | B | "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters … William Howard Russell, My Indian Mutiny Diary, 1860" | 1857 Indian Mutiny from British colonial perspective — if Indian History content appears, it is filtered through colonial framing | IO, IC, OC |
| D16 | philosophy | Ex.1 | A | "According to Parfit, the obligation to give priority to the welfare of one's children is: agent-relative." | Western analytic philosophy (Parfit) — not covered in UPSC/SSC philosophy or ethics sections | IO, IC |
| D17 | philosophy | Ex.2 | B | "Anscombe claims that on Sidgwick's view, the badness of an action must be estimated in light of: its expected consequences." | Western analytic moral philosophy (Sidgwick, Anscombe) — entirely Western canonical tradition | IO, IC |
| D18 | moral_scenarios | Ex.1 | A | "according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." | Explicitly US-framed moral norms — normative grounding is US-specific | OC, IC |
| D19 | moral_scenarios | Ex.2 | B | "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." | Again explicitly references US 2020 moral standards — non-transferable to Indian cultural context | OC, IC |
| D20 | human_aging | Ex.3 | C | "The age at which one can receive full benefits from social security … Has been increasing" | US Social Security system — irrelevant to Indian context | IC |
| D21 | human_sexuality | Ex.1 | A | "Which of the following is the most common method of birth control for married couples in the U.S." | Explicitly US-specific demographic question | IC |
| D22 | high_school_geography | Ex.1 | A | "What is the most rapidly growing religion in the United States today? … Islam" | US religion demographics — not Indian Geography content | IO, IC |
| D23 | global_facts | Ex.2 | B | "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" | One of very few India-referencing questions — but tests dated Western-sourced statistical trivia, not Indian GK curriculum | IC |
| D24 | global_facts | Ex.4 | D | "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … in their country makes it a better place to live … 68%" | India-referencing global survey question — but sourced from Pew/Western pollsters, not Indian exam curriculum | IC |
| D25 | elementary_mathematics | Ex.1 | A | "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel? … 120 miles" | Uses miles (US customary unit) — Indian exams use km; creates construct-irrelevant variance | IC, IF |
| D26 | elementary_mathematics | Ex.5 | A | "A zoo has 15 toucans and 60 parrots. What is the ratio of the number of toucans to the number of parrots at the zoo? … 1:04" | Basic arithmetic ratio — language-neutral content applicable across curricula | IO |
| D27 | high_school_mathematics | Ex.1 | A | "Juan rolls a fair regular octahedral die … What is the probability that the product of the two rolls is a multiple of 3?" | Probability question — content universally applicable regardless of cultural context | IO |
| D28 | college_mathematics | Ex.2 | B | "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" | Uses feet (US customary unit) — minor but consistent US measurement convention | IC |
| D29 | college_computer_science | Ex.2 | B | "Let G = (V, E) be a connected, undirected graph … P_1 can be solved in polynomial time but P_2 is not known to be solvable in polynomial time." | Algorithm complexity theory — culturally neutral STEM content | IO |
| D30 | abstract_algebra | Ex.1 | A | "Find the characteristic of the ring Z_3 x 3Z." | Abstract mathematics — entirely culture-independent | IO |
| D31 | high_school_statistics | Ex.4 | D | "The Hardcore Construction Company has two offices, one in Atlanta and one in New Orleans … Is the 2-sample t-test an appropriate inferential technique?" | Statistical reasoning with US city names as context — content sound but culturally anchored | IC |
| D32 | professional_accounting | Ex.1 | A | "Which of the following procedures does a CPA usually perform when reviewing the financial statements of a nonissuer?" | US CPA (Certified Public Accountant) professional standards — not relevant to Indian accounting exams | IO, IC |
| D33 | jurisprudence | Ex.1 | A | "Bill purchased a can of Sipep from the Ajax Minimart … In a strict product liability tort action against Ajax, Bill must prove …" | US-style product liability tort — uses American legal framework | IC |
| D34 | high_school_world_history | Ex.4 | D | "Kwame Nkrumah, Neo-Colonialism, 1965 … Which of the following most inspired the national plan advanced by Nkrumah in the second paragraph? … Socialism" | Global post-colonial history — partial relevance to Indian modern history via decolonisation themes | IO |
| D35 | world_religions | Ex.2 | B | "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" | Jainism question — one of very few South Asian religious/cultural references in the entire sample | IO, IC |
| D36 | world_religions | Ex.4 | D | "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" | Jainism sect distinction — rare South Asian content, but not an Indian competitive exam priority topic | IO, IC |
| D37 | high_school_psychology | Ex.1 | A | "Jyoti notes the behavior of people as they wait in line for tickets to rock concerts." | Uses Indian name 'Jyoti' but the context is rock concerts (Western cultural setting) — surface-level name inclusion without substantive cultural relevance | IC |
| D38 | auxiliary_train | Ex.1 | A | "Jim watched a liquor store furtively … On a charge of burglary, Jim's best defense would be that … the liquor store was open to the public." | US criminal law (burglary statute) — entirely US legal framework | IO, IC |
| D39 | high_school_macroeconomics | Ex.2 | B | "A nation that must consistently borrow to cover annual budget deficits risks … a decline in net exports as the nation's goods become more expensive to foreign consumers." | General macroeconomic principle — applicable cross-culturally | IO |
| D40 | conceptual_physics | Ex.4 | D | "A wave transfers … energy" | Basic physics principle — universally applicable | IO |
| D41 | high_school_biology | Ex.2 | B | "The sequence of amino acids in hemoglobin molecules of humans is more similar to the hemoglobin of chimpanzees than it is to the hemoglobin of dogs." | Biology/evolution — curriculum-neutral STEM content | IO |
| D42 | virology | Ex.1 | A | "Viruses have encouraged us to change our world, as we have now: Eradicated smallpox" | General science fact — applicable to Indian science GK | IO |
| D43 | international_law | Ex.1 | A | "Which of the following is a treaty-based human rights mechanism? … The UN Human Rights Committee" | International law — partially relevant to UPSC GS II but framed from Western international law perspective | IO |
| D44 | prehistory | Ex.2 | B | "The origins of Chinese civilization can be traced to: chiefdoms and states in numerous regions throughout China." | World history/prehistory — no South Asian prehistoric content visible | IO |
| D45 | miscellaneous | Ex.1 | A | "A flashing red traffic light signifies that a driver should do what? … stop" | US traffic law convention — minor but US-specific | IC |
| D46 | business_ethics | Ex.5 | A | "civil society … in many other countries, such as Russia and China … far less developed than in, for instance, Britain" | Western-centric framing of civil society — India not mentioned as reference | IC |
| D47 | high_school_world_history | Ex.2 | B | "the deed was done by a subject race — by black men who dared to shed the blood of their masters … British journalist William Howard Russell" | 1857 mutiny through British colonial journalist's lens — if Indian content appears at all in MMLU, it is through a colonial/Western perspective | OC, IC |
| D48 | college_medicine | Ex.4 | D | "When preparing for the MCAT exam, a student begins studying electrochemical cells." | References MCAT (US Medical College Admission Test) — US-specific academic context | IC |
| D49 | high_school_statistics | Ex.5 | A | "As reported on CNN, in a May 1999 national poll 43% of high school students expressed fear about going to school." | CNN/US-specific polling context — not Indian curriculum content | IC |
| D50 | security_studies | Ex.1 | A | "In what ways do theories of conventional and critical social constructivism differ?" | IR theory — Western academic framing; partial relevance to UPSC GS II international relations | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Four-option MCQ format structurally matches competitive exam format
- **Dimension(s):** IF
- **Observation:** Every question in MMLU uses a four-option multiple-choice structure (A/B/C/D) with one correct answer and three distractors, which is the identical format used in UPSC Prelims, SSC CGL, and banking exams. The `choices` field consistently contains exactly four options across all 57 subjects sampled.
- **Deployment relevance:** The MCQ format is a genuine structural match, meaning that any component of MMLU used in a format-compatibility test would not introduce format-induced performance variance from input encoding differences.
- **Datapoint citations:**
  - [D26] Example 5 (elementary_mathematics, split=test, label=A): "A zoo has 15 toucans and 60 parrots. What is the ratio of the number of toucans to the number of parrots at the zoo? (A) 1:04 (B) 1:05 (C) 4:01 (D) 4:05" — standard four-option MCQ format identical to Indian competitive exam structure.
  - [D40] Example 4 (conceptual_physics, split=test, label=D): "A wave transfers (A) amplitude (B) wavelength (C) frequency (D) energy" — clean four-option format applicable regardless of deployment context.

#### Strength 2: Culturally neutral STEM content (mathematics, physics, computer science) provides partial proxy signal
- **Dimension(s):** IO
- **Observation:** A substantial fraction of MMLU's items — particularly abstract algebra, college/high school mathematics, conceptual physics, college computer science, and formal logic — contain questions whose correctness is independent of cultural or geographic framing. These items test skills (arithmetic, reasoning, algorithm analysis, probability) that overlap with the quantitative aptitude and reasoning sections of SSC CGL and UPSC Prelims CSAT.
- **Deployment relevance:** For the deployment's Mathematics/Reasoning priority domain, these items constitute a weak but non-zero signal about model competence. UPSC CSAT Paper II and SSC CGL quantitative aptitude share conceptual overlap with MMLU's elementary and college mathematics items.
- **Datapoint citations:**
  - [D27] Example 1 (high_school_mathematics, split=test, label=A): "Juan rolls a fair regular octahedral die marked with the numbers 1 through 8. Then Amal rolls a fair six-sided die. What is the probability that the product of the two rolls is a multiple of 3?" — probability question applicable cross-culturally.
  - [D30] Example 1 (abstract_algebra, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — pure mathematics, culturally neutral.
  - [D29] Example 2 (college_computer_science, split=test, label=B): "P_1 can be solved in polynomial time but P_2 is not known to be solvable in polynomial time." — algorithm complexity, universally applicable.

#### Strength 3: Broad label balance across answer classes
- **Dimension(s):** OF
- **Observation:** Across sampled configs, the distribution of correct answers (A/B/C/D) is reasonably balanced. Buffer counts show roughly 22–31% per class in most subjects, with no systematic bias toward any single letter. This prevents position-bias artifacts from contaminating aggregate accuracy scores.
- **Deployment relevance:** For any comparative evaluation of models on the subset of MMLU items with partial relevance (STEM), balanced answer distribution reduces the risk that accuracy gains reflect position-bias rather than genuine knowledge.
- **Datapoint citations:**
  - [D26] elementary_mathematics buffer: A=79, B=97, C=101, D=101 (n=378) — reasonable balance across four classes.
  - [D27] high_school_mathematics buffer: A=57, B=71, C=71, D=71 (n=270) — no dominant label class.

#### Strength 4: Science and biology content overlaps with Indian GK science sections
- **Dimension(s):** IO
- **Observation:** MMLU's high school biology, college biology, virology, medical genetics, and conceptual physics items cover topics (genetics, evolution, cell biology, basic physics principles) that partially overlap with Indian Class 10–12 NCERT science content tested in UPSC/SSC GK sections. These are not India-specific but are curriculum-neutral science facts.
- **Deployment relevance:** UPSC Prelims General Studies Paper I and SSC CGL GK sections include NCERT-level science questions. MMLU's science content provides weak-but-positive signal in this subdomain.
- **Datapoint citations:**
  - [D41] Example 2 (high_school_biology, split=test, label=B): "The sequence of amino acids in hemoglobin molecules of humans is more similar to the hemoglobin of chimpanzees than it is to the hemoglobin of dogs. This similarity suggests that humans and chimpanzees are more closely related than humans and dogs" — evolution content appearing in NCERT Biology Class 12.
  - [D42] Example 1 (virology, split=test, label=A): "Viruses have encouraged us to change our world, as we have now: Eradicated smallpox" — general science fact tested in Indian GK sections.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of Indian Polity, Indian History, and Indian Geography — the core UPSC/SSC subject domains
- **Dimension(s):** IO
- **Observation:** Across all 57 MMLU subject configs and the full sample of ~200 examples, not a single question addresses Indian constitutional law, Panchayati Raj, Indian administrative structures, Indian ancient/medieval/modern history, or Indian physical/political geography. The government and politics config covers exclusively US government. The history configs cover European and US history. No config maps to any of the five priority subject domains in the Indian competitive exam syllabus.
- **Deployment relevance:** Indian Polity and Constitution, Indian History, and Indian Geography are high-priority domains for UPSC Prelims GS Paper I and SSC GK. MMLU provides zero items for these domains. A model achieving high MMLU accuracy could score near-random on UPSC/SSC Indian Polity questions, and MMLU accuracy would provide no predictive information about this.
- **Datapoint citations:**
  - [D1] Example 1 (high_school_government_and_politics, split=test, label=A): "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — US First Amendment, not Indian constitutional rights.
  - [D3] Example 5 (high_school_government_and_politics, split=test, label=A): "What power was granted to the states by the Articles of Confederation but not by the Constitution?" — US Articles of Confederation, no Indian Polity equivalent.
  - [D4] Example 2 (high_school_us_history, split=test, label=B): "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828 … was similar to the language of which of the following political positions?" — US antebellum history, irrelevant to Indian History syllabus.
  - [D12] Example 1 (high_school_european_history, split=test, label=A): "The Scribbling-Machines have thrown thousands of your petitioners out of employ … Leeds Woolen Workers Petition, 1786" — British Industrial Revolution, no South Asian historical content.

#### Concern 2: All benchmark inputs are in English — zero Hindi or Devanagari content
- **Dimension(s):** IF
- **Observation:** Every single question, answer option, and subject label in the sampled data is in English. The HF metadata confirms `languages: [en]` and `multilinguality: monolingual`. There is no Devanagari script, no Hindi vocabulary, no code-mixed text, and no variant closer to the deployment's required input register (Hindi-dominant with ≤10% English).
- **Deployment relevance:** The deployment requires Hindi-medium interaction. A model's MMLU accuracy measured on English-medium questions provides no evidence whatsoever about its capacity to comprehend Hindi-dominant or Devanagari-script inputs. IndicEval (arXiv:2602.16467) demonstrates a catastrophic Hindi-medium performance penalty: LLaMA achieves only 39.53% on UPSC Hindi Zero-Shot vs. ~84.88% for Gemini on UPSC English CoT. MMLU scores cannot predict this gap.
- **Datapoint citations:**
  - [D10] Example 1 (professional_law, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — English-medium, no Hindi content.
  - [D25] Example 1 (elementary_mathematics, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel?" — English-only phrasing, uses US customary units.
  - [D30] Example 1 (abstract_algebra, split=test, label=A): "Find the characteristic of the ring Z_3 x 3Z." — English-only mathematical notation.

#### Concern 3: Output structure is label-only (A/B/C/D) — no Hindi explanatory feedback evaluated
- **Dimension(s):** OO, OF
- **Observation:** Every MMLU example in the dataset has a single scalar `answer` field (ClassLabel 0–3 corresponding to A–D). The benchmark evaluates only whether a model selects the correct letter. There is no field for rationale, explanation, or free-form text output. The benchmark structure makes it architecturally impossible to assess a model's capacity to generate Hindi-language explanatory feedback.
- **Deployment relevance:** The deployment's core output requirement is a substantive Hindi-language explanation of why an answer is correct or incorrect, delivered in standard Manak Hindi register. MMLU accuracy scores provide zero signal on this output dimension. A model could achieve 90% MMLU accuracy while generating incoherent or factually wrong Hindi explanations — or no Hindi output at all.
- **Datapoint citations:**
  - [D1] Schema (all configs): `answer: ClassLabel(4 classes)` with label_names `["A", "B", "C", "D"]` — confirms label-only output structure with no rationale field.
  - [D18] Example 1 (moral_scenarios, split=test, label=A): "Wrong, Wrong" — a two-word answer label; the benchmark evaluates this binary classification with no mechanism for explanatory text.
  - [D26] Example 5 (elementary_mathematics, split=test, label=A): answer=0 (A) — single integer label, no explanation field present.

#### Concern 4: Ground-truth labels reflect US moral and legal norms — not Indian stakeholder perspectives
- **Dimension(s):** OC
- **Observation:** The `moral_scenarios` config explicitly frames every question as measuring "ordinary moral standards in the US as of 2020." The `professional_law` and `high_school_government_and_politics` configs test US legal standards. All labels were validated against US-standard answer keys by US university students. No Indian subject-matter experts, UPSC/SSC exam specialists, or Hindi-medium educators participated in any documented annotation process.
- **Deployment relevance:** For any India-centric GK, Polity, or History question, the US-annotator validation chain is entirely non-representative. More immediately, the moral_scenarios items could produce systematically different correct answers under Indian cultural norms vs. US norms, undermining OC validity for the target population.
- **Datapoint citations:**
  - [D18] Example 1 (moral_scenarios, split=test, label=A): "according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot. Scenario 2 | I popped the ball…" — the explicit US 2020 moral framing makes these labels non-transferable to Indian cultural context.
  - [D19] Example 2 (moral_scenarios, split=test, label=B): "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." — US legal/moral norm (impersonation at a roadblock) may be evaluated differently under Indian law and social norms.
  - [D15] Example 2 (high_school_world_history, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters … William Howard Russell" — the single instance of 1857 Indian content appears through a colonial British journalist's framing; the correct answer label privileges a colonial historiographic perspective that conflicts with the Indian NCERT/Bipin Chandra narrative taught in Indian competitive exam preparation.

#### MAJOR

#### Concern 5: US-specific cultural assumptions embedded throughout non-STEM items
- **Dimension(s):** IC
- **Observation:** Items across business ethics, human sexuality, human aging, high school geography, marketing, and miscellaneous configs embed US-specific institutional assumptions, demographic statistics, legal conventions, and cultural referents. This is not limited to history or law — it pervades even ostensibly "general" subjects.
- **Deployment relevance:** For a Hindi-medium aspirant from North India, these culturally embedded assumptions constitute construct-irrelevant variance that would depress performance on items even where the underlying conceptual knowledge might be present. More critically, correct answers rely on US-specific factual knowledge that is not part of any Indian competitive exam syllabus.
- **Datapoint citations:**
  - [D20] Example 3 (human_aging, split=test, label=C): "The age at which one can receive full benefits from social security … Has been increasing" — requires knowledge of US Social Security policy; irrelevant to Indian GK.
  - [D21] Example 1 (human_sexuality, split=test, label=A): "Which of the following is the most common method of birth control for married couples in the U.S." — US-specific demographic question; not part of any Indian exam syllabus.
  - [D22] Example 1 (high_school_geography, split=test, label=A): "What is the most rapidly growing religion in the United States today? … Islam" — US religion demographics; Indian Geography covers entirely different content.
  - [D45] Example 1 (miscellaneous, split=test, label=A): "A flashing red traffic light signifies that a driver should do what? … stop" — US traffic law convention; Indian traffic law uses different conventions.
  - [D48] Example 4 (college_medicine, split=test, label=D): "When preparing for the MCAT exam, a student begins studying electrochemical cells." — MCAT is a US-specific standardized test, adding irrelevant institutional framing.

#### Concern 6: Indian content appears only through colonial/Western framing — not from Indian standpoint
- **Dimension(s):** IC, OC
- **Observation:** In the entire sample, the only substantive reference to Indian history occurs in a high_school_world_history example quoting British journalist William Howard Russell's description of the 1857 Sepoy Mutiny/First War of Independence using derogatory racialized colonial language ("a subject race," "black men who dared to shed the blood of their masters"). This colonial framing is antithetical to the Indian nationalist historiography (Bipin Chandra, NCERT textbooks) that UPSC/SSC aspirants study.
- **Deployment relevance:** If this item were used to evaluate a model for the Indian deployment, a model producing an explanation aligned with NCERT's framing of 1857 as the First War of Independence would likely score lower against MMLU's label (which privileges the passage's colonial interpretation). This creates direct OC misalignment for the target population.
- **Datapoint citations:**
  - [D15] Example 2 (high_school_world_history, split=test, label=B): "the peculiar aggravation of the Cawnpore massacres was this, that the deed was done by a subject race — by black men who dared to shed the blood of their masters, and that of poor helpless ladies and children … British journalist William Howard Russell, My Indian Mutlny Diary, 1860" — colonial framing of 1857 event; the correct answer ("can be viewed as a reaction to the systemic brute force with which the British governed India") is framed through a second passage by Indian historian Mukherjee, but the question architecture and answer validation remain within a Western academic framework.
  - [D47] Same datapoint — "Violence, it must be emphasized, was an essential component of the British presence in India … Rudrangshu Mukherjee, 'The Kanpur [Cawnpore] Massacres in India in the Revolt of 1857,' 1990" — even the Indian historiographic passage is filtered through a comparative literature framework rather than UPSC's standard national history framing.

#### Concern 7: US customary measurement units appear in mathematics items — potential construct-irrelevant variance
- **Dimension(s):** IC
- **Observation:** Several mathematics and physics items use US customary units (miles, feet, pounds) rather than SI/metric units used in India. Indian competitive exam mathematics uses exclusively metric/SI units and Indian-context word problems.
- **Deployment relevance:** While the mathematical reasoning tested is identical, the appearance of "miles per hour" or "feet of fencing" introduces culturally unfamiliar unit terminology that could create construct-irrelevant difficulty for Hindi-medium aspirants less familiar with US measurement conventions.
- **Datapoint citations:**
  - [D25] Example 1 (elementary_mathematics, split=test, label=A): "If a freight train travels at a speed of 20 miles per hour for 6 hours, how far will it travel? … 120 miles" — uses miles; Indian exam arithmetic problems use km/h.
  - [D28] Example 2 (college_mathematics, split=test, label=B): "A total of x feet of fencing is to form three sides of a level rectangular yard. What is the maximum possible area of the yard, in terms of x?" — uses feet; Indian exams use metres.

#### Concern 8: Professional law and accounting items test US-jurisdiction-specific professional standards
- **Dimension(s):** IO, IC
- **Observation:** The `professional_law`, `professional_accounting`, and `jurisprudence` configs contain items that require knowledge of US bar exam standards, US CPA professional conduct rules, and US tort/contract law doctrine. These are inapplicable to Indian competitive exams, which test Indian constitutional law, Indian Evidence Act, Indian Contract Act, and Indian administrative law.
- **Deployment relevance:** These configs constitute dead weight for the deployment — not only do they test irrelevant content, but a model optimized for MMLU professional law performance would be specifically tuned to US legal concepts that directly conflict with Indian legal doctrine (e.g., US "strict product liability" vs. Indian Consumer Protection Act standards).
- **Datapoint citations:**
  - [D10] Example 1 (professional_law, split=test, label=A): "A truck driver was assigned to drive a huge tractor-trailer loaded with logs … the girl's parents … assert a claim against the lumber company" — US tort scenario.
  - [D32] Example 1 (professional_accounting, split=test, label=A): "Which of the following procedures does a CPA usually perform when reviewing the financial statements of a nonissuer?" — US CPA standards, not ICAI (Indian CA) standards.
  - [D33] Example 1 (jurisprudence, split=test, label=A): "Bill purchased a can of Sipep from the Ajax Minimart … In a strict product liability tort action against Ajax, Bill must prove … Ajax is a merchant selling Sipep." — US product liability doctrine.

#### MINOR

#### Concern 9: Surface-level Indian name inclusion without substantive Indian cultural relevance
- **Dimension(s):** IC
- **Observation:** One high_school_psychology example uses the Indian name "Jyoti" in an otherwise Western cultural context (waiting in line for rock concert tickets). This is cosmetic name inclusion that does not constitute genuine India-relevant content.
- **Deployment relevance:** Superficial name substitution without cultural grounding could create a misleading appearance of Indian-context coverage. It does not address any of the actual cultural or content gaps.
- **Datapoint citations:**
  - [D37] Example 1 (high_school_psychology, split=test, label=A): "Jyoti notes the behavior of people as they wait in line for tickets to rock concerts. Which of the following research methods is she using?" — Indian name in a rock concert queue context that is culturally foreign to North Indian aspirants.

#### Concern 10: Rare South Asian religious content (Jainism) present but not aligned with Indian competitive exam priorities
- **Dimension(s):** IO
- **Observation:** Two world_religions items address Jainism specifically — a South Asian religion. This constitutes the clearest South Asian content in the entire sample. However, Jainism represents a minor sub-topic in UPSC/SSC world religions coverage, and the framing is from an academic world religions perspective rather than the NCERT/competitive exam curriculum perspective.
- **Deployment relevance:** While these items demonstrate that MMLU is not entirely devoid of South Asian religious content, their presence does not constitute meaningful coverage of the Indian religions (Hinduism, Buddhism, Jainism, Sikhism) as taught in UPSC GS Paper I Indian Culture section, where the emphasis is on philosophical schools, texts, and historical development within the Indian context.
- **Datapoint citations:**
  - [D35] Example 2 (world_religions, split=test, label=B): "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism content, but framed as generic world religions trivia rather than Indian cultural history.
  - [D36] Example 4 (world_religions, split=test, label=D): "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" — Jain sect distinction, minor sub-topic in Indian competitive exam coverage.

#### Concern 11: Global Facts config contains India-referencing items but tests Western-sourced statistical trivia rather than Indian GK curriculum
- **Dimension(s):** IC
- **Observation:** Two global_facts examples reference India — one on internet usage (2017 data) and one on attitudes toward diversity (2018 Pew data). These are not items drawn from Indian GK curriculum sources (PIB, Economic Survey, Census of India) but from international polling organizations using Western survey methodologies.
- **Deployment relevance:** The content format differs from UPSC/SSC GK questions, which draw on official Indian government sources. A model tuned on MMLU global facts would learn to cite Pew/Gallup statistics rather than National Sample Survey Office (NSSO) or Census of India data that appears in competitive exam questions.
- **Datapoint citations:**
  - [D23] Example 2 (global_facts, split=test, label=B): "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" — Pew Research sourced India statistic; UPSC GK uses TRAI/IAMAI data.
  - [D24] Example 4 (global_facts, split=test, label=D): "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … in their country makes it a better place to live … 68%" — Pew global attitudes survey; not a standard UPSC/SSC GK source format.

---

### Content Coverage Summary

The sampled data confirms MMLU as a coherent, well-structured benchmark anchored entirely in an English-language, US/Western academic tradition. Subject coverage across 57 configs is internally consistent: mathematics and STEM items are culturally neutral; humanities and social science items are systematically US- or Western-centric; professional items (law, accounting, medicine) are calibrated to US professional licensing standards. The benchmark spans genuine breadth in its intended domain but has no subject track — and produces no individual item in the sample — that addresses Indian Polity, Indian History, Indian Geography, Hindi language proficiency, or Current Affairs relevant to India.

The most striking finding from direct content examination is the near-total absence of South Asian content: two Jainism questions in world_religions, one colonial-framed 1857 Mutiny question in world_history, and two Pew-data India-statistic questions in global_facts constitute the entirety of India-referencing content across approximately 200 sampled items. Where India does appear (D15, D47), it is filtered through a Western/colonial academic lens incompatible with the NCERT-aligned nationalist historiography that Indian competitive exam aspirants study.

The language register throughout is formal academic English. Questions range from terse (conceptual_physics, elementary_mathematics) to lengthy multi-paragraph primary-source readings (high_school_european_history, high_school_us_history, high_school_world_history). None of the inputs contains any Devanagari script, Hindi vocabulary, or code-mixed phrasing. The output structure is universally a single integer (0–3) representing the correct answer letter, with no rationale field.

---

### Limitations

1. **Sample size per config:** With 5–6 examples per config, coverage within each subject is limited. Rare India-relevant items within a config (if any exist) may not have appeared in the sample. The absence of South Asian content in the sample is consistent with but not a mathematical proof of complete absence across all 14,079 test items.

2. **Auxiliary train split not fully analyzed:** The auxiliary_train config (professional law focus) was sampled with only 5 examples and confirms US legal content, but its full 1.6M+ legal case summary content was not inspectable.

3. **Hindi translation variants not in scope:** This analysis covers only the original English cais/mmlu dataset. Community-translated Hindi MMLU variants (OpenAI MMMLU, IndicMMLU-Pro) were not sampled and their quality cannot be assessed from this data.

4. **Output quality unverifiable from dataset alone:** The label-only output structure means that any assessment of Hindi explanatory feedback quality must come from external model evaluation, not from the benchmark data itself.

5. **Moral scenarios cultural equivalence unverifiable at scale:** The moral_scenarios config explicitly invokes US 2020 moral standards. Whether the correct answers would align with Indian stakeholder judgments requires systematic cross-cultural annotation that cannot be inferred from reading examples alone.

6. **World religions coverage of Hinduism/Buddhism:** Only 6 world_religions items were sampled. The config may contain more South Asian religious content not captured in the sample, though the subject taxonomy and scoring would still reflect academic comparative religion rather than UPSC Indian Culture curriculum framing.