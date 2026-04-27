## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi configuration)
**Analysis date:** 2025-08-04
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Dimension |
|----|---------|-----------|-------|---------|-----------|
| D1 | MILU/Hindi | All 245 | is_translated=True | Every sampled example has `is_translated: True` | IC |
| D2 | MILU/Hindi | Ex. 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं।" (Arts & Humanities / Literature and Linguistics) | IC |
| D3 | MILU/Hindi | Ex. 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" (Arts & Humanities / Language Studies) | IC |
| D4 | MILU/Hindi | Ex. 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें।" (Arts & Humanities / Language Studies) | IC |
| D5 | MILU/Hindi | Ex. 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में...दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize" (Arts & Humanities / Language Studies) | IC |
| D6 | MILU/Hindi | Ex. 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" (Arts & Humanities / Language Studies) | IC, OO |
| D7 | MILU/Hindi | Ex. 51 | option2 | "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" (Arts & Humanities / Language Studies) | IC |
| D8 | MILU/Hindi | Ex. 97 | option3 | "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है।" (postposition grammar; Language Studies) | IC |
| D9 | MILU/Hindi | Ex. 195 | option4 | "निर्देश: उस खंड की पहचान करें जिसमें व्याकरण संबंधी त्रुटि है... 'के शासन द्वारा'" | IC |
| D10 | MILU/Hindi | Ex. 118 | option2 | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें." [question text for the idiom is absent] | IC, IF |
| D11 | MILU/Hindi | Ex. 152 | option1 | "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें." [underlined segment missing] | IC, IF |
| D12 | MILU/Hindi | Ex. 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें..." [statements 1-4 not present in question text] | IC, IF |
| D13 | MILU/Hindi | Ex. 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल, (b) केवल, (c) केवल" [referents a,b,c,d absent] | IC, IF |
| D14 | MILU/Hindi | Ex. 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक...राज्यों A,B,C,D,E..." [states not named] | IC, IF |
| D15 | MILU/Hindi | Ex. 94 | option4 | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? (a), (b), (c), (d)" [reactions not listed] | IC, IF |
| D16 | MILU/Hindi | Ex. 106 | option2 | "निम्नलिखित पदार्थों को...कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4" [substances not named] | IC, IF |
| D17 | MILU/Hindi | Ex. 143 | option4 | "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करने के लिए सही विकल्प चुनें." [words absent] | IC, IF |
| D18 | MILU/Hindi | Ex. 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है. वाक्य A और F स्थिर हैं." [sentences not present] | IC, IF |
| D19 | MILU/Hindi | Ex. 151 | option1 | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं...कौन सा तर्क मजबूत है?" [statement/arguments absent] | IC, IF |
| D20 | MILU/Hindi | Ex. 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" (Arts & Humanities / History — Mughal historiography) | IC |
| D21 | MILU/Hindi | Ex. 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था" (Arts & Humanities / History — South Indian history) | IC |
| D22 | MILU/Hindi | Ex. 48 | option3 | "भांड पाथेर थिएटर मुख्य रूप से भारत के निम्नलिखित में से किस राज्य/केंद्र शासित प्रदेश की परंपरा है?" (Arts & Humanities / Arts and Culture — Jammu & Kashmir) | IC |
| D23 | MILU/Hindi | Ex. 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" (Arts & Humanities / Literature and Linguistics — Tamil-specific) | IC |
| D24 | MILU/Hindi | Ex. 232 | option2 | "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है?" (Arts & Humanities / Literature and Linguistics — Tamil classic) | IC |
| D25 | MILU/Hindi | Ex. 126 | option3 | "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" (Arts & Humanities / Literature and Linguistics — Telugu/Telangana-specific) | IC |
| D26 | MILU/Hindi | Ex. 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" (Arts & Humanities / Arts and Culture — Rajasthan-specific) | IC |
| D27 | MILU/Hindi | Ex. 198 | option2 | "'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है?" (Arts & Humanities / History — Chhattisgarh-specific) | IC |
| D28 | MILU/Hindi | Ex. 68 | option2 | "राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" (Geography — Rajasthan-specific) | IC |
| D29 | MILU/Hindi | Ex. 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" (Geography — UP-specific) | IC |
| D30 | MILU/Hindi | Ex. 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" (Arts & Humanities / Arts and Culture — UP-specific) | IC |
| D31 | MILU/Hindi | Ex. 115 | option4 | "किस लेखक ने...किस्सा किस्सा लखनऊवा-लखनऊ के आवामी किस्से के लिए साहित्य अकादमी युवा पुरस्कार 2021 जीता?" (Literature — recent award) | IC |
| D32 | MILU/Hindi | Ex. 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" (History — national patriotic figure) | IC |
| D33 | MILU/Hindi | Ex. 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम..." (Sociology — ethics scenario) | IC, OO |
| D34 | MILU/Hindi | Ex. 142 | option1 | "क्या तेलंगाना सरकार को सभी को मुफ्त शिक्षा प्रदान करनी चाहिए?" (Education — argumentation item) | IC |
| D35 | MILU/Hindi | Ex. 188 | option3 | "नई शिक्षा नीति 2020 में देखा गया है..." [problems (a)(b) not stated] | IC, IF |
| D36 | MILU/Hindi | Ex. 122 | option4 | "प्रधानमंत्री मुद्रा योजना (PMMY) के बारे में निम्नलिखित में से कौन सा कथन सही है? न तो 1 और न ही 2 / दोनों 1 और 2..." [statements 1 and 2 absent] | IC, IF |
| D37 | MILU/Hindi | Ex. 157 | option4 | "पद्म पुरस्कार 2021 के संदर्भ में निम्नलिखित कथनों पर विचार करें. 1...2...3..." (multi-statement item — complete in question) | IC |
| D38 | MILU/Hindi | Ex. 201 | option4 | "BIOS के संदर्भ में निम्नलिखित में से कौन सा कथन सही है? केवल I और II / केवल I और III..." [statements I, II, III absent] | IC, IF |
| D39 | MILU/Hindi | Ex. 222 | option2 | "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C, D, E केवल..." [items A-E absent] | IC, IF |
| D40 | MILU/Hindi | Ex. 74 | option4 | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" (Economics — time-stamped current affairs) | IC |
| D41 | MILU/Hindi | Ex. 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022..." (Sports and Recreation — time-stamped current affairs) | IC |
| D42 | MILU/Hindi | Ex. 132 | option4 | "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" (Politics — time-stamped) | IC |
| D43 | MILU/Hindi | Ex. 127 | option2 | "भारतीय दंड संहिता किस वर्ष प्रभावी हुई? (target: option2 = 1862)" (Law and Ethics — factual) | OC |

---

### Findings

#### CRITICAL

#### Finding CRITICAL1: All 245 sampled validation examples are marked `is_translated: True` — the translated proportion appears to dominate or constitute the entire validation split

- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 245 sampled examples carries `is_translated: True`. The published paper reports that only ~25% of the released 79K questions are translated from English [Q47], which would predict a minority of translated items in any representative sample. Yet no item in this 245-item sample has `is_translated: False`. This may indicate that the validation split was specifically constructed from translated items (as opposed to the test split which may contain the organically sourced majority), or that the `is_translated` flag has a different semantics than expected.
- **Potential concern for deployment:** If the validation split consists entirely of translated items, few-shot examples drawn from this split (as MILU intends [Q51]) will always be translated-origin content. For the Hindi-medium teacher deployment, this means that in-context examples used to calibrate LLM performance will never reflect organically sourced Hindi-exam register. Translated items may carry GPT-4O translation artifacts — formal but potentially non-idiomatic Khari Boli — and may not match the register of school-board or state-exam question papers. The entire few-shot calibration corpus would then be drawn from a systematically different distribution than the test corpus.
- **Datapoint citations:**
  - [D1] All 245 examples (MILU/Hindi, split=validation): `is_translated: True` on every row — if this is representative of the split, the validation set is 100% translated-origin, sharply at odds with the paper's reported 25% translated figure for the full dataset.

---

#### MAJOR

#### Finding MAJOR1: Pervasive truncated/incomplete question stems — answer options refer to absent content

- **Dimension(s):** IC, IF
- **Observation:** A substantial number of questions in the sample are self-evidently incomplete: the question stem references numbered statements, lettered items, underlined text, or a list of substances/reactions that are not present in the `question` field. Affected examples include at minimum: Ex. 56 (four statements about ethanol not provided), Ex. 69 (substances (a)–(d) absent), Ex. 86 (states A–E not named), Ex. 94 (reactions (a)–(d) not listed), Ex. 95 (sentences B–E absent), Ex. 106 (substances 1–4 not listed), Ex. 118 (idiom text missing), Ex. 122 (statements 1 and 2 absent), Ex. 143 (words to be arranged absent), Ex. 151 (statement and arguments absent), Ex. 152 (underlined segment missing), Ex. 188 (NEP problems (a)(b) absent), Ex. 201 (BIOS statements I–III absent), Ex. 222 (Fortune 500 items A–E absent).
- **Potential concern for deployment:** These items cannot be answered from the `question` field alone. If an LLM is evaluated on these items using only the structured fields provided, it must guess among four options without the necessary referent content — systematically degrading accuracy scores for no construct-valid reason. For the North Indian teacher deployment, where MILU is being assessed as a benchmark for Hindi-medium MCQ evaluation, this data quality issue means a non-trivial fraction of Hindi items are functionally unanswerable and will depress measured accuracy in ways unrelated to language or cultural competence. The fraction of affected items in the validation split appears substantial (at least 14/245 = ~6% confirmed from the sample, likely higher).
- **Datapoint citations:**
  - [D12] Example 56 (MILU/Hindi, split=validation, label=option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें और दिए गए विकल्पों में से सही उत्तर चुनें:" — answer options reference statements 1–4 that are not present in the question field.
  - [D13] Example 69 (MILU/Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल, (b) केवल, (c) केवल" — substances (a)–(d) not provided.
  - [D14] Example 86 (MILU/Hindi, split=validation, label=option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C..." — states A–E not identified.
  - [D15] Example 94 (MILU/Hindi, split=validation, label=option4): "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं?" — reactions (a)–(d) absent.
  - [D16] Example 106 (MILU/Hindi, split=validation, label=option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4" — substances 1–4 not named.
  - [D10] Example 118 (MILU/Hindi, split=validation, label=option2): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें." — the idiom itself is absent.
  - [D11] Example 152 (MILU/Hindi, split=validation, label=option1): "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें." — underlined segment not present.
  - [D18] Example 95 (MILU/Hindi, split=validation, label=option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है. वाक्य A और F स्थिर हैं." — sentences not provided.
  - [D19] Example 151 (MILU/Hindi, split=validation, label=option1): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं...कौन सा तर्क मजबूत है?" — statement and arguments I/II absent.
  - [D35] Example 188 (MILU/Hindi, split=validation, label=option3): "नई शिक्षा नीति 2020 में देखा गया है कि भारत में उच्च शिक्षा प्रणाली निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b)..." — problems (a)/(b) not stated.
  - [D36] Example 122 (MILU/Hindi, split=validation, label=option4): "प्रधानमंत्री मुद्रा योजना (PMMY) के बारे में निम्नलिखित में से कौन सा कथन सही है? न तो 1 और न ही 2..." — statements 1 and 2 absent.
  - [D38] Example 201 (MILU/Hindi, split=validation, label=option4): "BIOS के संदर्भ में निम्नलिखित में से कौन सा कथन सही है? केवल I और II..." — statements I, II, III absent.
  - [D39] Example 222 (MILU/Hindi, split=validation, label=option2): "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C, D, E केवल..." — companies A–E not named.

---

#### Finding MAJOR2: Hindi Arts & Humanities items do not include canonical North Indian literary content (Tulsidas, Premchand, Kabir, Mahadevi Verma)

- **Dimension(s):** IC, IO
- **Observation:** Across 245 sampled Hindi validation items, Arts & Humanities / Literature and Linguistics questions reference Kashmiri poets (Ex. 98: "कश्मीर का जॉन कीट्स"), Tamil classics (Ex. 108: Subramanya Bharati; Ex. 232: Silappatikaram/Ilango Adigal), Telugu literary works (Ex. 126: Telangana Rastrodayamalu), Sindhi writers (Ex. 179: Sahitya Akademi), and William Wordsworth (Ex. 7). No sampled item references Tulsidas, Premchand, Kabir, Mahadevi Verma, Jaishankar Prasad, Nirala, or Dinkar — the canonical Hindi-board literary figures listed as high-priority for the deployment. The History items reference Mughal historiography (Ex. 25: Masir-e-Alamgiri), Pandya kings (Ex. 52), Indus Valley (Ex. 237), and Asoka (Ex. 158), but not figures specifically canonical to North Indian state-board Hindi literature curricula.
- **Potential concern for deployment:** The deployment requires assessment of student responses to MCQs covering canonical Hindi literature as taught in UP, MP, Bihar, and Rajasthan boards. If Hindi Literature and Linguistics items are drawn from competitive-exam general-knowledge framings featuring South Indian, Kashmiri, or international literary figures rather than the canonical Hindi-board authors, the benchmark will not measure what North Indian teachers actually test their students on. This directly instantiates the highest-priority IC gap identified in the coverage gap analysis.
- **Datapoint citations:**
  - [D2] Example 7 (Arts & Humanities / Literature and Linguistics, label=option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं।" — a UK Romantic poet, not part of Hindi board syllabus; no equivalent item found for Tulsidas or Premchand.
  - [D23] Example 108 (Arts & Humanities / Literature and Linguistics, label=option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" — Tamil literary history, not North Indian board Hindi literature.
  - [D24] Example 232 (Arts & Humanities / Literature and Linguistics, label=option2): "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है?" — Tamil classic literature.
  - [D25] Example 126 (Arts & Humanities / Literature and Linguistics, label=option3): "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" — Telugu/Telangana literary topic.
  - [D20] Example 25 (Arts & Humanities / History, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" — Mughal court historiography, competitive-exam framing rather than school-board Hindi literature perspective.

---

#### Finding MAJOR3: English-vocabulary Language Studies items in a Hindi-language benchmark

- **Dimension(s):** IC, IF
- **Observation:** Multiple Language Studies items in the Hindi benchmark ask about English vocabulary or English grammar in a Hindi-translated wrapping: Ex. 76 asks the meaning of 'didactic' in English; Ex. 90 asks for the synonym of 'grim'; Ex. 105 asks the Hindi meaning of 'Evangelize'; Ex. 3 (implicitly) tests English grammar concepts (active/passive voice in Hindi phrasing). These items appear to be translated from English-language verbal-ability competitive-exam questions (SSC, banking exams) where the original task was English vocabulary proficiency, not Hindi language competence.
- **Potential concern for deployment:** North Indian Hindi-medium teachers assess students on Hindi grammar, Hindi literature, and sometimes Sanskrit-origin vocabulary — not on English synonym/antonym or English word definition tasks. Items that test knowledge of English vocabulary words (grim, didactic, evangelize) within the Hindi benchmark do not align with Hindi-medium state-board curricula. A model performing well on these items would be demonstrating English vocabulary knowledge accessed through Hindi translation, not Hindi-medium linguistic competence. This conflation may inflate or distort benchmark scores in ways irrelevant to the deployment context.
- **Datapoint citations:**
  - [D3] Example 76 (Arts & Humanities / Language Studies, label=option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — Hindi item asking meaning of the English word 'didactic.'
  - [D4] Example 90 (Arts & Humanities / Language Studies, label=option3): "शब्द 'grim' का पर्यायवाची लिखें." — Hindi item asking for synonym of the English word 'grim.'
  - [D5] Example 105 (Arts & Humanities / Language Studies, label=option4): "निर्देश:...दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है और उसके अनुरूप बटन पर क्लिक करें। Evangelize" — Hindi item asking Hindi translation of English 'Evangelize.'

---

#### Finding MAJOR4: Competitive-exam IAS/civil-services framing dominates Social Sciences and Ethics items; school-board register absent

- **Dimension(s):** IC
- **Observation:** The one Ethics/Governance scenario item in the sample (Ex. 83) presents a complex multi-paragraph real-world dilemma cast explicitly from the perspective of "एक वरिष्ठ सिविल अधिकारी" (a senior civil servant) deciding how to respond to tribal displacement by an old-age home. This is textbook UPSC Mains Ethics, Paper IV framing — far from any school-board MCQ context. Similarly, Ex. 142 asks students to evaluate arguments about whether the Telangana government should provide free education to all, a policy-reasoning format typical of state PCS exams but foreign to UP Board Class 10–12 MCQ contexts.
- **Potential concern for deployment:** State-board teachers at the secondary level assess students on factual civics, basic constitutional law, and social science MCQs — not on complex IAS-style ethical reasoning scenarios or multi-paragraph argument evaluation. The presence of such items in the Hindi benchmark means a deployed LLM calibrated on MILU may be optimized for competitive-exam reasoning patterns that teachers in the deployment context never need to evaluate.
- **Datapoint citations:**
  - [D33] Example 83 (Social Sciences / Sociology, label=option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है..." — 4-option scenario question in UPSC Ethics Paper IV register.
  - [D34] Example 142 (Arts & Humanities / Education, label=option1): "क्या तेलंगाना सरकार को सभी को मुफ्त शिक्षा प्रदान करनी चाहिए? तर्क: A: हाँ... B: नहीं..." — argument-strength evaluation item typical of state PCS prelims, not school-board MCQs.

---

#### Finding MAJOR5: Strong South India / non-Hindi-belt regional content bias in Arts & Humanities and Geography

- **Dimension(s):** IC, IO
- **Observation:** A disproportionate share of regionally specific content in the sample is drawn from South India, Eastern India, or states outside the Hindi belt. Arts & Culture items reference: Bhānd Pather theatre (Jammu & Kashmir, Ex. 48), Kota painting school (Rajasthan, Ex. 193 — one of the few Hindi-belt items), Tamil magazine cartoons (Ex. 108), Silappatikaram (Tamil, Ex. 232), Telangana literature (Ex. 126). History items feature Pandya kingdom (Ex. 52), Bastar rebellion/Chhattisgarh (Ex. 198). Geography features Manipur's Imphal Basin (Ex. 186), Jharkhand river origins (Ex. 107). UP/MP/Bihar/Rajasthan-specific content is rare: only Ex. 26 (UP minerals), Ex. 68 (Rajasthan reserved area), Ex. 242 (UP chikankari embroidery) are clearly Hindi-belt specific in this sample.
- **Potential concern for deployment:** The deployment targets North Indian Hindi-belt teachers whose students are assessed on UP/MP/Bihar/Rajasthan regional history, geography, and culture. The apparent under-representation of Hindi-belt regional content and over-representation