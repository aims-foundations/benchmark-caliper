## Dataset Analysis Report

**Dataset(s):** cais/mmlu (57 subject configurations)
**Analysis date:** 2025-01-31
**Examples reviewed:** ~290 examples across 57 subject configs (5–6 per config)
**Columns shown:** question, subject, choices, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | mmlu | high_school_government_and_politics, test, Ex1 | A | "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" | US constitutional law — exclusively US institutional framing | IO, IC |
| D2 | mmlu | high_school_government_and_politics, test, Ex2 | B | "In the majority of cases, federal programs are implemented by state and local governments, by means of federal funding" | US federal governance structure | IO, IC |
| D3 | mmlu | high_school_government_and_politics, test, Ex4 | D | "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" | US-specific legislative history | IO, IC |
| D4 | mmlu | high_school_us_history, test, Ex2 | B | "John C. Calhoun, 'South Carolina Exposition and Protest,' 1828" | US political history — no Arab-region analog | IO, IC |
| D5 | mmlu | high_school_us_history, test, Ex5 | A | "Tonight, the daughter of an immigrant from Italy has been chosen to run for (vice) president… Geraldine Ferraro, Vice Presidential Nomination Acceptance Address, July 19, 1984" | US domestic politics 1984 | IO, IC |
| D6 | mmlu | professional_law, test, Ex1 | A | "A truck driver was assigned to drive a huge tractor-trailer loaded with logs… the girl was struck by the tractor-trailer and was seriously injured" | US tort law scenario | IO, IC, OC |
| D7 | mmlu | professional_law, test, Ex3 | C | "A patient filed a medical malpractice action against a hospital in federal court" | US federal court procedure | IO, IC, OC |
| D8 | mmlu | professional_law, test, Ex5 | A | "A buyer filed a lawsuit against a seller based on a written contract allegedly executed at the time of the sale of the seller's hot dog stand" | US contract law | IO, IC, OC |
| D9 | mmlu | us_foreign_policy, test, Ex3 | C | "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" | US Cold War policy — framed entirely from US perspective | IO, IC, OC |
| D10 | mmlu | us_foreign_policy, test, Ex4 | D | "In American government, the power to declare war rests with Congress." | US constitutional structure | IO |
| D11 | mmlu | us_foreign_policy, test, Ex5 | A | "Revelations that the NSA was monitoring the communications of American citizens without obtaining warrants" | US domestic surveillance scandal | IO, IC |
| D12 | mmlu | moral_scenarios, test, Ex1 | A | "For which of these two scenarios does the main character do something clearly morally wrong, according to ordinary moral standards in the US as of 2020?" | Explicitly frames moral judgment via US 2020 standards | OC, OO |
| D13 | mmlu | moral_scenarios, test, Ex2 | B | "according to ordinary moral standards in the US as of 2020? Scenario 1: When I went through the road block I gave the policeman my brothers ID." | US-anchored moral framing | OC, OO |
| D14 | mmlu | moral_scenarios, test, Ex3 | C | "according to ordinary moral standards in the US as of 2020? Scenario 2: I was due to start work soon, so I went to a baseball game." | US cultural reference (baseball) embedded in moral reasoning | OC, OO, IC |
| D15 | mmlu | high_school_world_history, test, Ex2 | B | "British journalist William Howard Russell, My Indian Mutiny Diary, 1860… 'the deed was done by a subject race — by black men who dared to shed the blood of their masters'" | Colonial-era British framing of Indian revolt | IC, OC |
| D16 | mmlu | high_school_world_history, test, Ex5 | A | "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E. … Jews, Buddhists, Hindus, Nasoreans, Christians, Maktak, and Manichaeans in the empire were smitten" | Near Eastern (Persian) source — the only example touching the broader Middle East region | IO, IC |
| D17 | mmlu | world_religions, test, Ex1 | A | "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" | Christian ecclesiastical history — no Islamic content in sampled examples | IO, IC |
| D18 | mmlu | world_religions, test, Ex2 | B | "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" | Jainism content | IO |
| D19 | mmlu | world_religions, test, Ex3 | C | "Which are the synoptic Gospels? … Matthew, Mark, Luke" | Christian Biblical content | IO |
| D20 | mmlu | world_religions, test, Ex4 | D | "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" | Jainism content — no Islamic content in sample | IO |
| D21 | mmlu | world_religions, test, Ex5 | A | "What is the most important prayer in Judaism? … The Shema" | Jewish religious content | IO |
| D22 | mmlu | global_facts, test, Ex1 | A | "About what percentage of survey respondents from China report having paid a bribe in the last year to access public services … as of 2017?" | China-focused global facts | IO, IC |
| D23 | mmlu | global_facts, test, Ex2 | B | "As of 2017, what fraction of the population in India used the internet in the past three months? … 26%" | India-focused global facts | IO, IC |
| D24 | mmlu | global_facts, test, Ex3 | C | "As of 2019, which of the following had the lowest life expectancy? … Mexico" | Global health — Latin American and Asian countries featured; no Arab countries | IO, IC |
| D25 | mmlu | global_facts, test, Ex4 | D | "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … makes it a better place to live?" | India-focused survey data | IO, IC |
| D26 | mmlu | global_facts, test, Ex5 | A | "At the time of independence, there were already hundreds of thousands of university graduates in ____, but hardly any at all in ____. … India, Congo" | Development economics — Africa/Asia framing, no Arab countries | IO, IC |
| D27 | mmlu | high_school_geography, test, Ex1 | A | "What is the most rapidly growing religion in the United States today? … Islam" | US-context geography question; Islam mentioned but in US demographic context | IO, IC |
| D28 | mmlu | high_school_geography, test, Ex5 | A | "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric zone model of urban form?" | US urban sociology model (Burgess) | IO, IC |
| D29 | mmlu | high_school_european_history, test, Ex1 | A | "Leeds Woolen Workers Petition, 1786 … The sentiments expressed by the Leeds woolen workers illustrate which of the following historical trends?" | British industrial history | IO, IC |
| D30 | mmlu | high_school_european_history, test, Ex2 | B | "Voltaire, Letters on the English Nation, 1733 … of all religions, the Christian ought doubtless to inspire the most tolerance" | European Enlightenment philosophy | IO, IC |
| D31 | mmlu | business_ethics, test, Ex5 | A | "civil society is far less developed than in, for instance, _______ … Russia, China, Britain" | Western-centric civil society framing; Arab world absent from options | IC |
| D32 | mmlu | human_aging, test, Ex3 | C | "The age at which one can receive full benefits from social security … Has been increasing" | US social security system | IC |
| D33 | mmlu | human_aging, test, Ex4 | D | "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" | US demographic framing | IC |
| D34 | mmlu | human_sexuality, test, Ex1 | A | "Which of the following is the most common method of birth control for married couples in the U.S. … Sterilization" | US-specific reproductive health statistics | IC |
| D35 | mmlu | human_sexuality, test, Ex5 | A | "From 1988 to 1990 among heterosexuals in the US, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" | US sexual behavior survey data | IC |
| D36 | mmlu | prehistory, test, Ex4 | D | "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" | Middle East referenced as origin of cattle domestication — one of very few regional mentions | IO, IC |
| D37 | mmlu | high_school_world_history, test, Ex4 | D | "Kwame Nkrumah, Neo-Colonialism, 1965 … 'A State in the grip of neo-colonialism is not master of its own destiny.'" | African post-colonial context — non-Western source, though not Arab | IC |
| D38 | mmlu | jurisprudence, test, Ex4 | D | "Which of the following statements best describes the postmodernist project? … It rejects the Kantian concern with individual rights, equality, and justice." | Western jurisprudential theory; no Islamic jurisprudence | IO |
| D39 | mmlu | international_law, test, Ex4 | D | "What is the meaning of cultural relativism? … Cultural relativism posits that local culture should validate the existence and practice of all human rights" | International law — potentially relevant to Arab regional norms | IO |
| D40 | mmlu | auxiliary_train, train, Ex1 | B | "Jim watched a liquor store furtively for some time, planning to hold it up … On a charge of burglary, Jim's best defense would be that the liquor store was open to the public." | US criminal law scenario | IO, IC, OC |
| D41 | mmlu | high_school_statistics, test, Ex5 | A | "As reported on CNN, in a May 1999 national poll 43% of high school students expressed fear about going to school" | US-sourced statistics example | IC |
| D42 | mmlu | security_studies, test, Ex2 | B | "Best described as intensification of worldwide social relations and increasing interdependence, globalization is the result of the compression of space and time" | Abstract IR theory — not regionally specific | IO |
| D43 | mmlu | professional_psychology, test, Ex2 | B | "With regard to minority and nonminority clients, psychotherapy is … equally effective" | US psychology research context | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Universal STEM and Formal Reasoning Content
- **Dimension(s):** IO, IC, IF
- **Observation:** A large proportion of MMLU subjects — abstract algebra, anatomy, astronomy, college chemistry, college physics, computer science, electrical engineering, formal logic, elementary mathematics, machine learning — contain questions with no cultural or geographic specificity. These questions test universal scientific and mathematical knowledge equally valid for Arab-region users and non-Arab users alike.
- **Deployment relevance:** The deployment covers school-level general educational knowledge. STEM content that tourists and expats ask about (basic science, geography concepts, math) can be evaluated fairly through MMLU even in an Arab-region deployment. A model scoring well on these subjects demonstrates transferable academic competence.
- **Datapoint citations:**
  - [D1–D43 passim] Abstract algebra (Ex 1–5), anatomy (Ex 1–5), astronomy (Ex 1–5), college chemistry (Ex 1–5), formal logic (Ex 1–5) — all contain culturally neutral mathematical or biological content. For example, abstract algebra Ex3: "Find all zeros in the indicated finite field of the given polynomial with coefficients in that field. x^3 + 2x + 2 in Z_7" — no cultural grounding required.

#### Strength 2: English-Language Text-Only Format Matches Primary Interaction Mode
- **Dimension(s):** IF
- **Observation:** MMLU is exclusively text-based, English-only, and multiple-choice. The deployment's primary user cohort (non-Arab tourists and expats) interacts in English. MMLU's format matches the primary interaction modality.
- **Deployment relevance:** For the majority English-language user cohort, MMLU's format creates no signal-distribution mismatch. Questions are well-formed, unambiguous in structure, and test reading comprehension at an appropriate register for educated adult users.
- **Datapoint citations:**
  - [D6] professional_law, Ex1: "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — demonstrates the clear, formal English register used throughout.
  - [D7] professional_law, Ex3: "A patient filed a medical malpractice action against a hospital in federal court" — standard formal English with no dialect or register barriers for educated English speakers.

#### Strength 3: International Law and Human Rights Coverage with Some Global Applicability
- **Dimension(s):** IO, IC
- **Observation:** The `international_law` subject contains questions about treaty-based human rights mechanisms, cultural relativism, and the distinction between public and private acts under international law. These topics have global applicability and touch on norms relevant to all eight deployment countries.
- **Deployment relevance:** Tourists and expats may have general curiosity about human rights frameworks that apply to the Arab world. International law questions are framed abstractly enough to not be exclusively US-anchored.
- **Datapoint citations:**
  - [D39] international_law, Ex4: "What is the meaning of cultural relativism? … Cultural relativism posits that local culture should validate the existence and practice of all human rights" — this question is abstractly framed and relevant to discussions of human rights in Arab-region contexts.
  - [D39] international_law, Ex3: "Is the unlawful homicide committed by Minister of country X abroad an act jure imperii or jure gestionis?" — abstractly framed, not anchored to any specific legal system.

#### Strength 4: Zero-Shot/Few-Shot Evaluation Design Appropriate for Generalization Testing
- **Dimension(s):** OF
- **Observation:** MMLU is designed for zero-shot and few-shot evaluation, probing knowledge acquired during pretraining. For a deployed system that must generalize to novel queries, this evaluation paradigm (rather than fine-tuned task-specific scoring) is more aligned with deployment behavior.
- **Deployment relevance:** Tourists and expats ask unpredictable general knowledge questions. A model evaluated under zero-shot/few-shot conditions demonstrates the same generalization property required for open-domain question answering about Arab history, geography, and language.
- **Datapoint citations:** All sampled examples are zero-shot MCQ without task-specific training — consistent with the deployment's need to evaluate generalization rather than narrow fine-tuned performance.

#### Strength 5: World Religions Subject Nominally Covers Multiple Faith Traditions
- **Dimension(s):** IO
- **Observation:** The `world_religions` subject includes questions on Jainism, Judaism, and Christianity across the six sampled examples. The subject label indicates coverage of multiple world religions, which nominally includes Islam — the dominant religion across all eight deployment countries.
- **Deployment relevance:** Tourists and expats frequently have questions about Islamic practices, the Islamic calendar, and Islamic history, which are core deployment topics. The world_religions subject is the closest available MMLU proxy for this content area.
- **Datapoint citations:**
  - [D17] world_religions, Ex1: "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" — Christian content.
  - [D18] world_religions, Ex2: "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism content.
  - [D21] world_religions, Ex5: "What is the most important prayer in Judaism? … The Shema" — Jewish content. No Islamic content appeared in the six sampled world_religions examples, but the subject label does not preclude its presence in the full 171-question set.

#### Strength 6: High School World History Includes Some Non-Western Primary Sources
- **Dimension(s):** IC
- **Observation:** The `high_school_world_history` subject includes non-Western and non-European primary sources. Among the five sampled examples, one is drawn from an ancient Persian inscription (Kerdir at Naqsh-e-Rustam), one from an African anti-colonial theorist (Kwame Nkrumah), and one from a British account of Indian colonialism. This demonstrates that the subject does not exclusively cover Western European history.
- **Deployment relevance:** The deployment requires school-level world history knowledge including pre-Islamic Middle Eastern history. The Persian inscription example shows the subject can include content from the broader Middle East/Central Asia region.
- **Datapoint citations:**
  - [D16] high_school_world_history, Ex5: "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E. … Jews, Buddhists, Hindus, Nasoreans, Christians, Maktak, and Manichaeans in the empire were smitten" — Near Eastern content, though pre-Islamic and Persian rather than Arab.
  - [D37] high_school_world_history, Ex4: "Kwame Nkrumah, Neo-Colonialism, 1965 … 'A State in the grip of neo-colonialism is not master of its own destiny.'" — African post-colonial perspective, showing non-Western framing is possible.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: No Arab-Region Subject Categories in the 57-Subject Taxonomy
- **Dimension(s):** IO
- **Observation:** Across all 57 MMLU subject configurations, not one is dedicated to Arab history, Middle Eastern geography, Arabic language, Islamic jurisprudence, or any sub-regional Arab topic. The subject list is exhaustively confirmed from the HF metadata: subjects include `high_school_us_history`, `high_school_european_history`, `high_school_government_and_politics` (US-framed), and `us_foreign_policy` — but no Arab history, no MENA geography, no Islamic law or culture.
- **Deployment relevance:** The deployment is specifically designed to answer questions about Arab history, regional geography, and Arabic language across eight Arab countries. The complete absence of dedicated Arab-region subjects means MMLU cannot evaluate whether a model knows anything useful for the core deployment domain. This is a structural gap, not a sampling artifact.
- **Datapoint citations:**
  - [D1] high_school_government_and_politics, Ex1: "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — one of five government/politics examples, all US-institutional.
  - [D10] us_foreign_policy, Ex4: "In American government, the power to declare war rests with Congress." — The "Foreign Policy" subject is entirely framed from a US perspective with no Arab-country policy questions in the sample.
  - [D3] high_school_government_and_politics, Ex4: "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" — US-specific legislation.

#### CRITICAL Concern 2: Global Facts Subject Excludes Arab Countries in Sampled Questions
- **Dimension(s):** IO, IC
- **Observation:** `global_facts` is the subject most likely to contain Arab-region statistical questions. All five sampled examples reference China (2), India (3), Mexico (1), and an Africa/Korea comparison (1). No Arab country appears in any of the five sampled global_facts questions.
- **Deployment relevance:** The deployment covers general school-level knowledge about the Arab world, including geography and demography. If `global_facts` — the subject most suited to cross-regional factual knowledge — contains no Arab-country questions even in a sample of five, this signals extremely low Arab-region density.
- **Datapoint citations:**
  - [D22] global_facts, Ex1: "About what percentage of survey respondents from China report having paid a bribe…" — China-focused.
  - [D23] global_facts, Ex2: "As of 2017, what fraction of the population in India used the internet…" — India-focused.
  - [D24] global_facts, Ex3: "As of 2019, which of the following had the lowest life expectancy? … Mexico" — Latin American comparison.
  - [D25] global_facts, Ex4: "As of 2018, about what percentage of Indians say that having an increasing number of people of many different races … makes it a better place to live?" — India-focused.
  - [D26] global_facts, Ex5: "At the time of independence, there were already hundreds of thousands of university graduates in India, but hardly any at all in Congo" — Africa/Asia comparison.

#### CRITICAL Concern 3: Moral Scenarios Explicitly Anchored to "US Standards as of 2020"
- **Dimension(s):** OC, OO
- **Observation:** Every sampled `moral_scenarios` example contains the explicit phrase "according to ordinary moral standards in the US as of 2020." This is not merely an implicit cultural bias — it is a stated label constraint encoding US moral standards as the ground truth. For users asking about moral or social norms in Arab countries, this labeling scheme encodes a directly contradictory cultural standard.
- **Deployment relevance:** The deployment system serves users in eight Arab countries where moral norms around alcohol, gender relations, family honor, public behavior, and religious observance diverge significantly from "US standards as of 2020." For any Arab-region moral or social knowledge domain, MMLU's moral_scenarios ground-truth labels are categorically misaligned with local stakeholder judgments.
- **Datapoint citations:**
  - [D12] moral_scenarios, Ex1: "For which of these two scenarios does the main character do something clearly morally wrong, according to ordinary moral standards in the US as of 2020? Scenario 1 | The bomb shelter was filling up, but I made sure my grand piano got a spot." — US moral framing as explicit label criterion.
  - [D13] moral_scenarios, Ex2: "according to ordinary moral standards in the US as of 2020? Scenario 1 | When I went through the road block I gave the policeman my brothers ID." — identity document fraud scenario judged by US standards.
  - [D14] moral_scenarios, Ex3: "according to ordinary moral standards in the US as of 2020? Scenario 2 | I was due to start work soon, so I went to a baseball game." — baseball as a culturally embedded reference in a moral reasoning task.

#### CRITICAL Concern 4: World History Arab-Region Absence; Middle East Appears Only as Ancient Persia and Agricultural Origin
- **Dimension(s):** IO, IC
- **Observation:** Across five sampled `high_school_world_history` examples, the Middle East/Arab region appears exactly once — in a Sasanian Persian inscription from the 3rd century CE (pre-Islamic, non-Arab). No Arab nationalist history, no Ottoman period, no Islamic civilization, no 20th-century Arab state formation, no Palestinian history, and no Levantine, Egyptian, or Gulf-specific content appears. The prehistory subject mentions the Middle East only as the origin of cattle domestication (~10,500 years ago).
- **Deployment relevance:** The deployment's core subject matter includes Arab history from the Islamic Golden Age through modern state formation. The near-complete absence of Islamic and Arab-period history in the world history and prehistory subjects means MMLU cannot assess a model's knowledge of the content tourists and expats most frequently ask about.
- **Datapoint citations:**
  - [D16] high_school_world_history, Ex5: "Excerpt from the inscription of Kerdir at Naqsh-e-Rustam, Persia, late third century C.E." — only Middle East reference in the five world history examples; pre-Islamic, Persian, not Arab.
  - [D36] prehistory, Ex4: "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" — Middle East mentioned only as an ancient agricultural origin, no cultural content.
  - [D29] high_school_european_history, Ex1: "Leeds Woolen Workers Petition, 1786" — European industrial history.
  - [D30] high_school_european_history, Ex2: "Voltaire, Letters on the English Nation, 1733" — European Enlightenment.

#### CRITICAL Concern 5: US Foreign Policy Subject Framed Entirely from US Perspective
- **Dimension(s):** IO, IC, OC
- **Observation:** All five sampled `us_foreign_policy` examples are framed from within US institutional and policy perspectives — NSC 68, War Powers Act, NSA surveillance, "Philadelphian System" exceptionalism. For a deployment covering Arab countries where US foreign policy is a contested and politically sensitive topic (Gulf War, Arab-Israeli conflict, Iraq War), the US-centric framing encodes one perspective as the correct answer.
- **Deployment relevance:** Users asking about US foreign policy in the Arab world — a frequent tourist/expat query about why certain regional conditions exist — will receive answers framed from a US perspective that may contradict the perspectives of host-country citizens in Jordan, Palestine, Lebanon, and Egypt.
- **Datapoint citations:**
  - [D9] us_foreign_policy, Ex3: "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" — entirely US institutional framing.
  - [D11] us_foreign_policy, Ex5: "Revelations that the NSA was monitoring the communications of American citizens without obtaining warrants" — US domestic civil liberties framing of surveillance.

---

#### MAJOR

#### MAJOR Concern 1: Professional Law, Jurisprudence, and Human Aging Encode US Institutional Specifics
- **Dimension(s):** IO, IC, OC
- **Observation:** The `professional_law` subject (500 test examples, the largest in MMLU) consists entirely of US common law scenarios — tort law, contract law, evidence rules, DUI statutes, federal court procedure. `human_aging` references US Social Security age thresholds and alcohol abuse rates among "Americans." These questions have no validity for an Arab-region deployment where legal systems are based on civil law (Morocco, Egypt), Islamic law (Saudi Arabia, Kuwait), or mixed systems (Lebanon, Jordan).
- **Deployment relevance:** Tourists and expats may ask general legal questions (e.g., "What are my rights?" or "How does property law work here?"). A model evaluated on MMLU professional law has been tested only on US common law knowledge, which may actively mislead users about Arab legal systems.
- **Datapoint citations:**
  - [D6] professional_law, Ex1: "A truck driver was assigned to drive a huge tractor-trailer loaded with logs…" — US tort law.
  - [D8] professional_law, Ex5: "A buyer filed a lawsuit against a seller based on a written contract allegedly executed at the time of the sale of the seller's hot dog stand" — US contract law.
  - [D32] human_aging, Ex3: "The age at which one can receive full benefits from social security … Has been increasing" — US social security specifics.
  - [D33] human_aging, Ex4: "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" — US demographic categories.

#### MAJOR Concern 2: High School Government and Politics Is Exclusively US Government
- **Dimension(s):** IO, IC
- **Observation:** All five sampled `high_school_government_and_politics` questions concern US constitutional structure — First Amendment, federal-state relations, Articles of Confederation, War Powers Act, Congressional representation. There is no comparative government content, no coverage of Arab governance structures (monarchies, tribal councils, military governments), and no non-US political systems.
- **Deployment relevance:** Tourists and expats visiting Arab countries frequently ask about governance structures, political history, and civic life. MMLU's government subject cannot evaluate a model's knowledge of Hashemite monarchy, Gulf tribal governance, Lebanese confessionalism, or Egyptian political history.
- **Datapoint citations:**
  - [D1] high_school_government_and_politics, Ex1: "The right of American citizens to petition the government for a redress of grievances is protected under the First Amendment" — US constitutional law.
  - [D2] high_school_government_and_politics, Ex2: "In the majority of cases, federal programs are implemented by state and local governments, by means of federal funding" — US federal structure.
  - [D3] high_school_government_and_politics, Ex4: "Both the War Powers Act of 1974 and the Budget and Impoundment Control Act of 1974 represent efforts by Congress to limit the powers of the president" — US-specific legislation.

#### MAJOR Concern 3: World Religions Sample Shows No Islamic Content; Coverage Depth Unknown
- **Dimension(s):** IO, IC
- **Observation:** Six sampled `world_religions` examples include content on Christian ecclesiastical succession, Jainism (2 questions), Jewish prayer, Daoist text, and Christian Gospels. Zero of the six sampled examples cover Islam. While the full 171-question set may include Islamic content, the absence from the sample raises concerns about proportion and framing.
- **Deployment relevance:** Islam is the dominant religion across all eight deployment countries and a primary topic of tourist/expat curiosity (Islamic calendar, Ramadan, prayer practices, mosque etiquette as general knowledge). A model evaluated only on Christian, Jain, and Jewish content will not have been tested on the religious knowledge most relevant to the deployment.
- **Datapoint citations:**
  - [D17] world_religions, Ex1: "Rome claimed that their bishop (pope) was the direct successor of which leader? … Peter" — Christianity.
  - [D18] world_religions, Ex2: "In Jainism, what is the cycle that one must liberate oneself from? … Samsara" — Jainism.
  - [D19] world_religions, Ex3: "Which are the synoptic Gospels? … Matthew, Mark, Luke" — Christian Biblical content.
  - [D20] world_religions, Ex4: "Which Jaina group only allows women to lead a life of semi-renunciation? … Digambara" — Jainism.
  - [D21] world_religions, Ex5: "What is the most important prayer in Judaism? … The Shema" — Judaism.

#### MAJOR Concern 4: Single-Answer MCQ Label Schema Cannot Accommodate Multi-Perspective Contested Topics
- **Dimension(s):** OO, OC
- **Observation:** MMLU's output schema enforces exactly one correct answer per question (A, B, C, or D). The deployment requirement — to acknowledge multiple perspectives on contested historical/political topics and flag political sensitivity — is structurally incompatible with this scoring paradigm. Across all 290+ sampled examples, every question has exactly one labeled correct answer with no mechanism for flagging contestedness.
- **Deployment relevance:** Key deployment topics — the 1948 war/Nakba framing, Western Sahara status, Lebanese Civil War causes, Palestinian statehood, Ottoman legacy — require multi-perspective responses. MMLU cannot score a model that says "this topic is contested; here are two perspectives" — such a response would score 0% on MMLU regardless of its accuracy for deployment purposes.
- **Datapoint citations:**
  - [D12] moral_scenarios, Ex1 through [D14] moral_scenarios, Ex3: all examples have a single binary label; no partial credit or multi-perspective acknowledgment is possible.
  - [D9] us_foreign_policy, Ex3: "Why is NSC 68 seen as a turning point in US Cold War Foreign policy? … It indicated a shift towards military containment" — one correct answer asserted; no acknowledgment of contested Cold War historiography.
  - [D15] high_school_world_history, Ex2: "According to the second passage, the Cawnpore Massacre … can be viewed as a reaction to the systemic brute force with which the British governed India" — colonial framing resolved to single answer from secondary source.

#### MAJOR Concern 5: High School Geography Framed Around US Urban Models and US Religious Demographics
- **Dimension(s):** IO, IC
- **Observation:** Five sampled `high_school_geography` questions include: Islam as the "most rapidly growing religion in the United States" (US-contextual framing), a globe/map projection question, pastoralism definition, core-periphery development model, and Burgess's concentric zone model of US urban form. None concern Arab-world physical geography, political geography, or spatial concepts relevant to Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, or KSA.
- **Deployment relevance:** The deployment covers regional geography of eight Arab countries. MMLU's high school geography content evaluates US-anchored urban sociology models and US religious demographics rather than physical or political geography of the Arab world.
- **Datapoint citations:**
  - [D27] high_school_geography, Ex1: "What is the most rapidly growing religion in the United States today? … Islam" — Islam mentioned only in US demographic context.
  - [D28] high_school_geography, Ex5: "Which zone contains low-income slums, ethnic ghettos, and general deterioration in Burgess's concentric zone model of urban form?" — US urban sociology model.

#### MAJOR Concern 6: Human Sexuality and Human Aging Encode US-Specific Survey Data as Ground Truth
- **Dimension(s):** IC, OC
- **Observation:** `human_sexuality` questions cite US statistics (most common US contraceptive method, US heterosexual partner counts 1988–1990), and `human_aging` references US Social Security and US ethnic group alcohol abuse rates. These ground-truth labels reflect US-population norms that diverge substantially from Arab-region norms around sexuality, family planning, gender relations, and social welfare.
- **Deployment relevance:** Tourists and expats may ask general questions about social norms, health practices, and demographics. A model evaluated on US-population ground truths for these topics will have been reinforced with knowledge claims that contradict Arab-region realities (e.g., contraceptive prevalence, attitudes toward sexuality, alcohol norms).
- **Datapoint citations:**
  - [D34] human_sexuality, Ex1: "Which of the following is the most common method of birth control for married couples in the U.S. … Sterilization" — US-specific reproductive health statistic as ground truth.
  - [D35] human_sexuality, Ex5: "From 1988 to 1990 among heterosexuals in the US, the number of unmarried adults aged 20 to 45 who report having multiple partners has: declined for both men and women" — US behavioral survey data.
  - [D33] human_aging, Ex4: "Which of the following groups of Americans have the lowest rate of alcohol abuse? … Asian-American" — alcohol abuse among American ethnic groups.

---

#### MINOR

#### MINOR Concern 1: High School European History Dominates Non-US History Slot
- **Dimension(s):** IO
- **Observation:** MMLU has a dedicated `high_school_european_history` subject but no equivalent for world history outside Europe and the US. The five sampled European history examples cover British industrialization, Voltaire, Pico della Mirandola, Medici-era Neoplatonism, and the Royal Society. This dedicated European history slot confirms that non-European, non-US histories are subordinated to the catch-all `high_school_world_history` subject.
- **Deployment relevance:** Arab history from the Islamic Golden Age, the Ottoman period, or modern state formation has no dedicated subject and must compete with all other non-European world history for representation in a single 237-question subject.
- **Datapoint citations:**
  - [D29] high_school_european_history, Ex1: "Leeds Woolen Workers Petition, 1786 … The sentiments expressed by the Leeds woolen workers illustrate which of the following historical trends?" — British industrial history.
  - [D30] high_school_european_history, Ex2: "Voltaire, Letters on the English Nation, 1733" — French Enlightenment.

#### MINOR Concern 2: Business Ethics Civil Society Question Omits Arab World from Options
- **Dimension(s):** IC
- **Observation:** A `business_ethics` question asks about countries with less developed civil society compared to a more developed example. The correct answer is "Russia, China, Britain" — the Arab world is not even presented as an option in this question about global civil society development.
- **Deployment relevance:** This is a minor individual instance, but it illustrates how MMLU's question design treats Arab countries as outside the scope of even comparative global analysis.
- **Datapoint citations:**
  - [D31] business_ethics, Ex5: "Although the benefit and contribution of civil society in encouraging sustainability … in many other countries, such as _____ and ______ civil society is far less developed than in, for instance, _______. … Russia, China, Britain" — Arab world entirely absent from the answer options for a global civil society comparison question.

#### MINOR Concern 3: Prehistory and Archaeology Show Selective Middle East Coverage
- **Dimension(s):** IC
- **Observation:** The `prehistory` subject contains a question correctly identifying the Middle East as the origin of cattle domestication ~10,500 years ago. However, this represents the region only as a prehistoric agricultural site, not as a culturally meaningful historical location. Other prehistory questions cover Stonehenge, Machu Picchu, Chinese civilization origins, and African butterfly species.
- **Deployment relevance:** For users curious about the deep history of the Arab region, the prehistory subject does contain one relevant data point. However, coverage is incidental rather than systematic, and the framing is archaeological rather than cultural.
- **Datapoint citations:**
  - [D36] prehistory, Ex4: "Archaeological evidence indicates that cattle were first domesticated where and how long ago? … in the Middle East, about 10,500 years ago" — region mentioned as agricultural origin only.

#### MINOR Concern 4: Professional Psychology US-Centric Research Norms
- **Dimension(s):** IC
- **Observation:** `professional_psychology` references US mental health norms (PKU treatment, minority/nonminority client effectiveness, crisis therapy frameworks). These norms reflect US clinical psychology literature and may not transfer to Arab-region mental health contexts or cultural attitudes toward therapy.
- **Deployment relevance:** Minor for this deployment, which focuses on history, geography, and language rather than psychology. However, to the extent users ask general knowledge questions about psychology or mental health, the US-clinical framing introduces cultural mismatch.
- **Datapoint citations:**
  - [D43] professional_psychology, Ex2: "With regard to minority and nonminority clients, psychotherapy is … equally effective" — US racial/ethnic minority framing of clinical effectiveness research.

---

### Content Coverage Summary

The 290+ sampled MMLU examples across 57 subjects confirm the following characterization:

**Dominant content register:** US academic curriculum (high school through professional level), drawing on US standardized tests, US undergraduate course materials, and Western European academic publications. The register is formal, English-only, and assumes familiarity with US institutional structures (federal government, common law, social security, US ethnic demographics).

**Subject concentration relevant to deployment:** Nominally relevant subjects (`high_school_world_history`, `high_school_geography`, `world_religions`, `global_facts`, `international_law`, `security_studies`) contain either no sampled Arab-region content (`global_facts`, `world_religions`, `high_school_geography`) or incidental references to the broader Middle East (`prehistory`: one question; `high_school_world_history`: one Sasanian Persian inscription).

**Subjects with zero Arab-region relevance:** `high_school_us_history`, `high_school_government_and_politics`, `us_foreign_policy`, `professional_law`, `human_sexuality`, `human_aging` — together comprising several hundred questions — are anchored in US-specific institutional, legal, and demographic contexts that transfer nothing meaningful to the Arab-region deployment.

**Moral and social content:** The `moral_scenarios` subject explicitly labels correct answers as "ordinary moral standards in the US as of 2020," creating a direct conflict with Arab-region moral frameworks on topics including alcohol, gender relations, family structures, and religious observance.

**Language:** Entirely English. No Arabic-script content, no dialect questions, no Arabic language instruction questions. The secondary Arabic-learning user cohort is unservable by this benchmark.

**Non-Western content that does appear:** The world history subject contains non-Western sources (Nkrumah, Kerdir inscription), and prehistory touches the Middle East as an agricultural origin point. These are the strongest evidence against total Western monoculture, but they are scattered and do not constitute systematic Arab-region coverage.

---

### Limitations

1. **Sample size per subject:** 5–6 examples per subject from the test split. For subjects with 237 questions (`high_school_world_history`) or 500 questions (`professional_law`, `moral_scenarios`, `professional_psychology`), the sample cannot confirm or rule out rare Arab-region content. It is possible that a small number of world history questions cover Islamic or Arab-period history not captured in the sample.

2. **World religions Islam content:** Six sampled world_religions examples showed no Islamic content. The full 171-question set may contain Islamic questions (possibly covering the Five Pillars, hadith, early Islamic history), but the framing perspective (Western academic vs. Islamic scholarly) cannot be determined from the sample.

3. **Security studies depth:** The security studies subject (245 questions) was sampled at 5 examples, all covering abstract IR theory. This subject might contain questions touching on Middle East security dynamics, but none appeared in the sample.

4. **Miscellaneous subject:** The `miscellaneous` subject (500+ questions) is a catch-all that could contain Arab-region factual questions. The five sampled examples (traffic lights, labor force, geometry, proletariat, material resistance) show no Arab-region content, but coverage uncertainty is high for this heterogeneous category.

5. **Auxiliary train split:** The auxiliary_train examples sampled are all US law scenarios, but this split was not systematically sampled across subjects — it represents only a subset of the training data.

6. **No access to question-level metadata on source:** The dataset does not expose which specific source documents each question came from, preventing confirmation of which questions originated from GRE, USMLE, Oxford Press, etc., vs. other sources that might include non-US content.

7. **Full quantitative coverage audit impossible from sample:** A definitive count of Arab-region questions across all 15,908 MMLU items would require inspecting every question — beyond what a sample-based analysis can provide. The web search finding that no published quantitative audit exists for original English MMLU Arab-region content proportion remains unresolved.