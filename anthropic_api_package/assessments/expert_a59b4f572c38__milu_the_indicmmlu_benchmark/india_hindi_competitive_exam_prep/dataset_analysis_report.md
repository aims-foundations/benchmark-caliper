## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | MILU/Hindi | 33 | option1 | "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत या सार्वजनिक प्राधिकरण को एक आधिकारिक कर्तव्य को सही ढंग से निभाने का निर्देश देता है।" | Mandamus writ definition question — Indian constitutional law | IO, IC |
| D2 | MILU/Hindi | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" | Constitutional amendment adding 'armed rebellion' — Indian Polity | IO, IC |
| D3 | MILU/Hindi | 39 | option3 | "भारत में किस संवैधानिक संशोधन विधेयक द्वारा मतदान की आयु 21 वर्ष से घटाकर 18 वर्ष की गई थी?" | Constitutional amendment lowering voting age — Indian Polity | IO, IC |
| D4 | MILU/Hindi | 42 | option3 | "निम्नलिखित में से कौन मसौदा समिति का सदस्य नहीं था?" | Drafting committee membership — Indian Constitution | IO, IC |
| D5 | MILU/Hindi | 93 | option2 | "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है?" | Three-tier Panchayati Raj middle unit — Indian Governance | IO, IC |
| D6 | MILU/Hindi | 136 | option4 | "भारत के संविधान के अनुसार, संसद का कौन सा सदन संविधान संशोधन विधेयक पारित करता है?" | Which house passes constitutional amendment bill | IO, IC |
| D7 | MILU/Hindi | 50 | option3 | "1882 में भारत में स्थानीय स्वशासन की शुरुआत किसने की?" | Who introduced local self-government in India 1882 | IO, IC |
| D8 | MILU/Hindi | 199 | option4 | "1907 के कांग्रेस सत्र में उदारवादियों और उग्रवादियों के बीच मुख्य अंतर किस विषय पर था?" | 1907 Congress session — moderate vs extremist split | IO, IC |
| D9 | MILU/Hindi | 32 | option4 | "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया।" | Who completed Qutub Minar — Medieval Indian history | IO, IC |
| D10 | MILU/Hindi | 96 | option2 | "कौन सा अधिनियम प्रांतों में द्वैध शासन प्रणाली स्थापित करता है?" | Which act established dyarchy in provinces — Modern India history | IO, IC |
| D11 | MILU/Hindi | 158 | option3 | "'देवानांप्रिय' और 'प्रियदर्शी' वे उपाधियाँ थीं जिन्हें राजा ______ ने अपनाया था।" | Titles 'Devanampiya' and 'Priyadarshi' — Ashoka/Ancient India | IO, IC |
| D12 | MILU/Hindi | 237 | option3 | "मोहनजोदड़ो और हड़प्पा के खंडहर दिखाते हैं कि ये शानदार और अच्छी तरह से योजनाबद्ध ________ थे।" | Harappan civilization characterized as merchant cities | IO, IC |
| D13 | MILU/Hindi | 36 | option3 | "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." | Letter series completion — Logical Reasoning | IO |
| D14 | MILU/Hindi | 44 | option2 | "दिए गए अक्षर श्रृंखला के रिक्त स्थानों में क्रमिक रूप से रखे जाने पर श्रृंखला को पूरा करने वाले अक्षरों के संयोजन का चयन करें। _q p p_p p_p p q_" | Letter pattern completion — Logical Reasoning | IO |
| D15 | MILU/Hindi | 84 | option3 | "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली और उसे विनय को उसी दर पर वार्षिक चक्रवृद्धि ब्याज पर दो वर्षों के लिए उधार दिया।" | Simple vs. compound interest calculation — Quantitative Aptitude/Mathematics | IO |
| D16 | MILU/Hindi | 120 | option4 | "किसी कंपनी में सभी कर्मचारियों का औसत वेतन रु. 10500 है। सभी पुरुष कर्मचारियों का औसत वेतन रु. 15000 है।" | Average salary mixture problem — Quantitative Aptitude | IO |
| D17 | MILU/Hindi | 111 | option3 | "आठ लोग दो समानांतर पंक्तियों में बैठे हैं... A के ठीक विपरीत कौन बैठता है?" | Seating arrangement reasoning problem | IO |
| D18 | MILU/Hindi | 208 | option4 | "कथन: I. कुछ पेन कप हैं। II. सभी कप प्लेट हैं। निष्कर्ष: I. सभी पेन प्लेट हैं।" | Syllogism — formal logical reasoning | IO |
| D19 | MILU/Hindi | 74 | option4 | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" | India GDP growth rate Q2 2018-19 — Current Affairs (dated) | IO, IC |
| D20 | MILU/Hindi | 132 | option4 | "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" | WCD Ministry head as of 2018 — Current Affairs (dated) | IO, IC |
| D21 | MILU/Hindi | 88 | option1 | "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा। उस क्षुद्रग्रह का नाम है:" | JAXA asteroid landing 2019 — Current Affairs (dated) | IO, IC |
| D22 | MILU/Hindi | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | Archery Asia Cup 2022 India gold medals — Sports Current Affairs (dated) | IO, IC |
| D23 | MILU/Hindi | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" | Mineral not found in Uttar Pradesh — North India–specific geography | IC |
| D24 | MILU/Hindi | 68 | option2 | "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" | 'Bajju' reserve forest in Rajasthan — state-specific geography | IC |
| D25 | MILU/Hindi | 156 | option1 | "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है?" | Rajasthan literacy rate 2011 — state-specific GK | IC |
| D26 | MILU/Hindi | 190 | option2 | "राजस्थान का आकार है-" | Shape of Rajasthan state — state-specific geography | IC |
| D27 | MILU/Hindi | 182 | option1 | "निम्नलिखित में से किस राज्य ने 2011-12 में सबसे अधिक दूध उत्पादन दर्ज किया?" | Highest milk production state 2011-12 — UP-specific GK | IC |
| D28 | MILU/Hindi | 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है, जिसमें शिफॉन, मलमल, ऑर्गेंजा, ऑर्गेंडी और रेशम जैसे कपड़ों पर नाजुक पारंपरिक हाथ कढ़ाई की जाती है।" | Chikankari — UP traditional embroidery craft | IC |
| D29 | MILU/Hindi | 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" | Kota painting school — Rajasthan art history | IC |
| D30 | MILU/Hindi | 198 | option2 | "छत्तीसगढ़ के निम्नलिखित विद्रोहों में से किसे 'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है?" | Chhattisgarh tribal rebellion — Central India history (outside North India core states) | IC |
| D31 | MILU/Hindi | 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था" | Pandya kingdom expansion — South Indian history, less relevant to UPSC North India focus | IC |
| D32 | MILU/Hindi | 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" | First cartoons in Tamil magazine — Tamil literary history | IC |
| D33 | MILU/Hindi | 126 | option3 | "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" | Telangana literary work — Telangana-specific cultural question | IC |
| D34 | MILU/Hindi | 41 | option1 | "टी-हब तेलंगाना राज्य सरकार की एक पहल है" | T-Hub Telangana tech incubator — state-specific non-central content | IC |
| D35 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" | DC series motor behavior — Engineering, not UPSC/SSC priority | IO |
| D36 | MILU/Hindi | 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" | Half-wave rectifier output — Electrical engineering technical content | IO |
| D37 | MILU/Hindi | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" | FORTRAN 77 fixed format — specialist programming, not UPSC/SSC priority | IO |
| D38 | MILU/Hindi | 104 | option4 | "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" | Intermediate frequency for AM receivers — electronics engineering specialist content | IO |
| D39 | MILU/Hindi | 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं।" | William Wordsworth's nationality — English literature, minimal India relevance | IC |
| D40 | MILU/Hindi | 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" | English vocabulary question: 'didactic' meaning — Language Studies, English vocabulary in Hindi context | IC, IF |
| D41 | MILU/Hindi | 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें।" | Synonym of English word 'grim' — English vocabulary tested in Hindi-labeled context | IC, IF |
| D42 | MILU/Hindi | 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में, चार विकल्पों में से उस शब्द का चयन करें जो दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है। Evangelize" | English word 'Evangelize' meaning — English vocabulary question in Hindi dataset | IC, IF |
| D43 | MILU/Hindi | 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें और दिए गए विकल्पों में से सही उत्तर चुनें: (1) और (3) केवल" | Ethanol statements question — options reference numbered statements absent from the question | IF |
| D44 | MILU/Hindi | 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" | Multidimensional poverty states — options reference A/B/C/D/E labels with no list in question | IF |
| D45 | MILU/Hindi | 94 | option4 | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? (केवल a, d) / (केवल b, c)" | Redox reactions question — options reference a/b/c/d labels absent from question text | IF |
| D46 | MILU/Hindi | 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (b), (c) और (d)" | Pure substance — options reference items (a)/(b)/(c)/(d) absent from question | IF |
| D47 | MILU/Hindi | 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं। AEDBCF" | Sentence ordering — sentences B/C/D/E absent from question text | IF |
| D48 | MILU/Hindi | 106 | option2 | "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" | Chronological ordering of substances — substance list absent from question | IF |
| D49 | MILU/Hindi | 109 | option4 | "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए पर्यवेक्षण, दिशा और नियंत्रण का प्रावधान किस अनुच्छेद में है? इनमें से कोई नहीं" | Article on municipality elections in Chhattisgarh — answer is 'none of these' suggesting data quality issue | OC |
| D50 | MILU/Hindi | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" | Author of Mughal text Maasir-i-Alamgiri — Mughal history relevant to UPSC | IC |
| D51 | MILU/Hindi | 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" | 'Iron Man of India' — Sardar Patel, standard UPSC GK | IC |
| D52 | MILU/Hindi | 100 | option2 | "मध्यकालीन काल की सरकार एक मिश्रित संरचना थी। यह किन तत्वों का समामेलन था? फारसी-अरबी, तुर्को-मंगोल - भारतीय तत्व" | Medieval Indian governance structure — UPSC History topic | IC |
| D53 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" | is_translated=True — electrical engineering question translated from English | IC |
| D54 | MILU/Hindi | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" | Indirect speech conversion — Hindi language grammar question | IC, IO |
| D55 | MILU/Hindi | 51 | option2 | "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" | Active voice conversion — Hindi grammar | IC, IO |
| D56 | MILU/Hindi | 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है... आदिवासी लोग जर्जर झोपड़ियों में रह रहे थे" | Ethics/governance scenario for senior civil officer — UPSC GS Paper IV Ethics | IO, IC |
| D57 | MILU/Hindi | 145 | option2 | "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा? एमएनक्यू / एमओक्यू" | Letter series in Hindi transliteration of English letters — code-mixing in reasoning | IC, IF |
| D58 | MILU/Hindi | 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" | 1991 economic crisis trigger — Indian Economy/Current Affairs (historical) | IO, IC |
| D59 | MILU/Hindi | 119 | option2 | "आरबीआई के नोट जारी करने वाले विभाग के पास हमेशा न्यूनतम कितने मूल्य का सोना होना चाहिए?" | RBI minimum gold reserve requirement — Indian Economy | IO, IC |
| D60 | MILU/Hindi | 28 | option2 | "निम्नलिखित में से कौन खेरवार आंदोलन के नेता थे? भागीरथ मांझी" | Kherwar movement leader — tribal history in Jharkhand/Bihar context | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strong Indian Polity and Governance Coverage
- **Dimension(s):** IO, IC
- **Observation:** The sample contains numerous questions directly aligned with UPSC/SSC priority topic of Indian Polity and Constitution — covering constitutional amendments (44th, 42nd), parliamentary procedures, Panchayati Raj, writs, and governance acts.
- **Deployment relevance:** Polity is one of the highest-weight subjects for UPSC GS Paper II and SSC General Awareness; these questions directly serve the deployment's primary subject requirements.
- **Datapoint citations:**
  - [D1] Example 33 (MILU/Hindi, validation, option1): "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत या सार्वजनिक प्राधिकरण को एक आधिकारिक कर्तव्य को सही ढंग से निभाने का निर्देश देता है।" — Mandamus writ definition, UPSC standard question type
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — 44th Amendment question, core UPSC Polity
  - [D3] Example 39 (MILU/Hindi, validation, option3): "भारत में किस संवैधानिक संशोधन विधेयक द्वारा मतदान की आयु 21 वर्ष से घटाकर 18 वर्ष की गई थी?" — 61st Amendment, standard Polity question
  - [D5] Example 93 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है?" — Panchayati Raj, UPSC/SSC staple
  - [D6] Example 136 (MILU/Hindi, validation, option4): "भारत के संविधान के अनुसार, संसद का कौन सा सदन संविधान संशोधन विधेयक पारित करता है?" — Constitutional amendment procedure

#### Strength 2: Meaningful Indian History Coverage Including Medieval and Modern Periods
- **Dimension(s):** IO, IC
- **Observation:** The sample includes questions on Mughal history, ancient Indian civilization, modern independence movement, and colonial-era governance acts — all core UPSC History syllabus areas.
- **Deployment relevance:** History is a top-priority subject for central exams; these questions represent standard UPSC Prelims question types.
- **Datapoint citations:**
  - [D9] Example 32 (MILU/Hindi, validation, option4): "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया।" — Medieval Delhi Sultanate history
  - [D10] Example 96 (MILU/Hindi, validation, option2): "कौन सा अधिनियम प्रांतों में द्वैध शासन प्रणाली स्थापित करता है?" — Government of India Act 1919, standard modern history
  - [D11] Example 158 (MILU/Hindi, validation, option3): "'देवानांप्रिय' और 'प्रियदर्शी' वे उपाधियाँ थीं जिन्हें राजा ______ ने अपनाया था।" — Ashoka, Ancient Indian History
  - [D50] Example 25 (MILU/Hindi, validation, option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं?" — Mughal history, North India–relevant
  - [D52] Example 100 (MILU/Hindi, validation, option2): "मध्यकालीन काल की सरकार एक मिश्रित संरचना थी। यह किन तत्वों का समामेलन था?" — Medieval governance structure
  - [D8] Example 199 (MILU/Hindi, validation, option4): "1907 के कांग्रेस सत्र में उदारवादियों और उग्रवादियों के बीच मुख्य अंतर किस विषय पर था?" — Surat Split, modern Indian history

#### Strength 3: Logical Reasoning Representation in the Dataset
- **Dimension(s):** IO
- **Observation:** The sample contains a meaningful number of logical reasoning question types including seating arrangements, syllogisms, blood relations, letter/number series, and coding-decoding — which together constitute a significant share of SSC CGL and banking exam papers.
- **Deployment relevance:** Mathematics/Reasoning is flagged as a top-priority gap in MILU's documented taxonomy, but the actual data confirms Logical Reasoning is represented as a subject under the Science domain, partially addressing the gap for SSC/banking exam prep.
- **Datapoint citations:**
  - [D13] Example 36 (MILU/Hindi, validation, option3): "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." — Letter series completion
  - [D17] Example 111 (MILU/Hindi, validation, option3): "आठ लोग दो समानांतर पंक्तियों में बैठे हैं...A के ठीक विपरीत कौन बैठता है?" — Seating arrangement
  - [D18] Example 208 (MILU/Hindi, validation, option4): "कथन: I. कुछ पेन कप हैं। II. सभी कप प्लेट हैं। निष्कर्ष: I. सभी पेन प्लेट हैं।" — Syllogism reasoning
  - [D14] Example 44 (MILU/Hindi, validation, option2): "दिए गए अक्षर श्रृंखला के रिक्त स्थानों में क्रमिक रूप से रखे जाने पर श्रृंखला को पूरा करने वाले अक्षरों के संयोजन का चयन करें। _q p p_p p_p p q_" — Letter pattern

#### Strength 4: Quantitative Aptitude Content Present
- **Dimension(s):** IO
- **Observation:** Several questions involve arithmetic calculations (simple/compound interest, averages, mixture problems) that are representative of the Quantitative Aptitude sections in SSC and banking exams. While labeled under Business Studies/Economics, these are functional math questions.
- **Deployment relevance:** Mathematics/Reasoning is the most critical undocumented gap in MILU's taxonomy; finding actual arithmetic content in the data partially mitigates this concern for SSC/banking preparation.
- **Datapoint citations:**
  - [D15] Example 84 (MILU/Hindi, validation, option3): "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली...दो वर्षों के अंत में उसे 1230 रुपये का चक्रवृद्धि ब्याज प्राप्त हुआ।" — Simple vs. compound interest problem
  - [D16] Example 120 (MILU/Hindi, validation, option4): "किसी कंपनी में सभी कर्मचारियों का औसत वेतन रु. 10500 है...कंपनी में कुल कर्मचारियों की संख्या कितनी है?" — Mixture/average problem

#### Strength 5: North India–Specific Regional Content Present
- **Dimension(s):** IC
- **Observation:** Several questions address knowledge specifically relevant to North Indian states (UP, Rajasthan) — covering state-specific geography (minerals in UP), traditional crafts (Chikankari embroidery), literacy statistics (Rajasthan Census 2011), Rajasthan geography, and agricultural data (milk production leader UP).
- **Deployment relevance:** The deployment requires the AI to handle both pan-India GK and North India sub-regional content. These examples confirm that some such content is present, partially addressing the documented partial gap.
- **Datapoint citations:**
  - [D23] Example 26 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — UP-specific mineral geography
  - [D28] Example 242 (MILU/Hindi, validation, option4): "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है, जिसमें शिफॉन, मलमल, ऑर्गेंजा, ऑर्गेंडी और रेशम जैसे कपड़ों पर नाजुक पारंपरिक हाथ कढ़ाई की जाती है।" — Chikankari (UP embroidery)
  - [D25] Example 156 (MILU/Hindi, validation, option1): "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है?" — Rajasthan state-specific statistics
  - [D27] Example 182 (MILU/Hindi, validation, option1): "निम्नलिखित में से किस राज्य ने 2011-12 में सबसे अधिक दूध उत्पादन दर्ज किया? उत्तर प्रदेश" — UP agricultural data
  - [D29] Example 193 (MILU/Hindi, validation, option3): "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" — Kota painting school (Rajasthan art)

#### Strength 6: Hindi Grammar and Language Proficiency Questions
- **Dimension(s):** IO, IC
- **Observation:** The dataset contains Hindi language grammar questions (active/passive voice, indirect speech, sentence structure) that align with the Hindi Language Proficiency component of central exams (UPSC Mains Hindi compulsory paper, SSC Hindi sections).
- **Deployment relevance:** Hindi language proficiency is listed as a priority subject area; these questions are in pure Hindi and reflect standard Hindi grammar exercises appropriate for the target student.
- **Datapoint citations:**
  - [D54] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Indirect speech conversion
  - [D55] Example 51 (MILU/Hindi, validation, option2): "दिए गए वाक्य का सही सक्रिय रूप चुनें। सभी को उसके शानदार नृत्य प्रदर्शन ने मोहित कर दिया।" — Active voice question

#### Strength 7: Ethics and Governance Scenarios (UPSC-Style)
- **Dimension(s):** IO, IC
- **Observation:** Example 83 presents a complex ethical scenario for a civil officer — a format directly mirroring UPSC GS Paper IV (Ethics, Integrity, Aptitude) case studies.
- **Deployment relevance:** UPSC aspirants must prepare for ethics-based scenario questions; this confirms MILU captures this question type, which is otherwise rare in competitive exam benchmarks.
- **Datapoint citations:**
  - [D56] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है...आदिवासी लोग जर्जर झोपड़ियों में रह रहे थे।" — UPSC-style ethics scenario

#### Strength 8: Indian Economy and Finance Coverage
- **Dimension(s):** IO, IC
- **Observation:** Questions on the 1991 economic crisis, RBI operations, MSP (Minimum Support Price), Five-Year Plans, PMMY (Pradhan Mantri Mudra Yojana), and banking sector are present — all standard Economics/GK topics in central exams.
- **Deployment relevance:** Indian economy is a consistently tested area in UPSC GS Paper III and SSC/banking exams.
- **Datapoint citations:**
  - [D58] Example 18 (MILU/Hindi, validation, option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" — 1991 crisis
  - [D59] Example 119 (MILU/Hindi, validation, option2): "आरबीआई के नोट जारी करने वाले विभाग के पास हमेशा न्यूनतम कितने मूल्य का सोना होना चाहिए?" — RBI operations

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete Output Format Mismatch — No Explanatory Rationale Infrastructure
- **Dimension(s):** OO, OF
- **Observation:** Every example in the sample is structured as a 4-option MCQ with a single correct label (`target`). There are no rationale fields, explanation columns, or any annotation supporting the deployment's core output requirement: a substantive Hindi-language explanation of why an answer is correct or incorrect.
- **Deployment relevance:** The deployment explicitly requires "both a correct/incorrect label and a substantive explanation of why the answer is right or wrong, delivered in Hindi" (Elicitation Q3). MILU's schema (question, option1–4, target, is_translated, language, domain, subject) contains no field for rationale. This is a total mismatch with the deployed task; benchmark accuracy scores cannot validate whether a model produces accurate or coherent Hindi explanations. This is confirmed by the benchmark paper itself (Q85) and by the absence of any explanation field across all 245 reviewed examples.
- **Datapoint citations:**
  - [D1] Example 33 (MILU/Hindi, validation, option1): "______ एक अदालत का आदेश है जो एक अधीनस्थ अदालत..." — Correct answer is option1, but no explanation of why mandamus fits the definition is provided
  - [D15] Example 84 (MILU/Hindi, validation, option3): "सूरज ने अजय से एक निश्चित दर पर साधारण ब्याज पर दो वर्षों के लिए एक राशि उधार ली..." — Math problem with answer only; no worked solution or rationale
  - [D56] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में..." — Ethics scenario answer marked option1 with no reasoning explaining why option1 is preferred over other plausible options

---

#### MAJOR

#### MAJOR Concern 1: Truncated/Self-Referential Questions — Construct-Irrelevant Variance
- **Dimension(s):** IF, OC
- **Observation:** A substantial number of questions (at minimum 5 identified in the 245-sample) have answer options that reference items, statements, or sentences that are absent from the question text itself. Options contain labels like "(a), (b), (c), (d)" or "1 2 3 4" or "AEDBCF" without the corresponding items being present in the question field. These appear to be reading-comprehension or list-based questions from which the source material was stripped during data collection, leaving the MCQ shell without the necessary context.
- **Deployment relevance:** A student interacting with these questions cannot evaluate the answer options without the missing content. Any model evaluated on these items is effectively guessing. For the deployment, presenting such incomplete questions would actively harm the student's learning experience, and benchmark accuracy on these items does not measure genuine knowledge.
- **Datapoint citations:**
  - [D43] Example 56 (MILU/Hindi, validation, option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...विकल्प (1) और (3) केवल" — Options reference statements (1)(2)(3)(4) that are absent from question
  - [D44] Example 86 (MILU/Hindi, validation, option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" — Options reference states A/B/C/D/E with no list provided
  - [D45] Example 94 (MILU/Hindi, validation, option4): "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d" — Options reference reactions a/b/c/d absent from question
  - [D46] Example 69 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (b), (c) और (d)" — Options reference items (a)–(d) absent
  - [D48] Example 106 (MILU/Hindi, validation, option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" — Substances to be ordered are absent from question
  - [D47] Example 95 (MILU/Hindi, validation, option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं। AEDBCF" — Sentences B/C/D/E absent from question

#### MAJOR Concern 2: 100% Translation Rate in Observed Sample — Unknown Effect on Hindi Register
- **Dimension(s):** IC, IF
- **Observation:** Every single example in the 245-sample (all 245) has `is_translated=True`. This is the entire validation split reviewed. While the overall dataset is documented to have ~25% translated items, the validation split may have a substantially higher translation rate, or there may be a systematic sampling issue. All translated items were produced by GPT-4O, and the Hindi phrasing varies in naturalness.
- **Deployment relevance:** The deployment specifies a ~10% English code-mixing ceiling for Hindi-medium students. Machine-translated questions may use unnatural Hindi phrasing, Sanskritized vocabulary, or carry over English-medium structural conventions. For example, engineering and computer science questions (DC motor, FORTRAN, rectifier) that are entirely technical/specialist in nature appear translated into Hindi with mixed terminology. This inflates the engineering/technical content proportion and may introduce phrasing patterns foreign to Hindi-medium exam-style content.
- **Datapoint citations:**
  - [D53] Example 1 (MILU/Hindi, validation, is_translated=True): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — Engineering question translated from English; typical Hindi-medium UPSC/SSC exam aspirants would not encounter DC motor questions
  - [D37] Example 8 (MILU/Hindi, validation, is_translated=True): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN programming language question, translated; not in UPSC/SSC scope

#### MAJOR Concern 3: English-Language Questions Classified as Hindi Content
- **Dimension(s):** IC, IF
- **Observation:** Multiple questions in the Hindi-labeled dataset are substantively about English vocabulary — testing the meaning of English words ('grim', 'didactic', 'Evangelize') or converting English sentences — rather than being Hindi-medium content questions. These are labeled `language=Hindi` and `subject=Language Studies` but require knowledge of English vocabulary, not Hindi.
- **Deployment relevance:** The target student population has limited English exposure; a ~10% code-mixing ceiling applies. English vocabulary synonym questions embedded in the Hindi benchmark are a direct mismatch. A Hindi-medium student who cannot identify the synonym of 'grim' in English is not being tested on any UPSC/SSC competency — these exams do not test English vocabulary for Hindi-medium candidates. Benchmark performance on these items does not reflect the target student's actual exam competency.
- **Datapoint citations:**
  - [D41] Example 90 (MILU/Hindi, validation, option3): "शब्द 'grim' का पर्यायवाची लिखें।" — Asks for a synonym of the English word 'grim'; answer options are in Hindi, but the knowledge tested is English vocabulary
  - [D40] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — English vocabulary meaning question
  - [D42] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में, चार विकल्पों में से उस शब्द का चयन करें जो दिए गए शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है। Evangelize" — English word meaning question; options in Hindi but knowledge is English vocabulary

#### MAJOR Concern 4: Substantial Over-Representation of Engineering/Technical Content Irrelevant to Deployment
- **Dimension(s):** IO
- **Observation:** The sample contains a high density of specialist engineering and computer science questions (electrical engineering, FORTRAN programming, AM/FM modulation, DC motors, TDM frame rates, transfer machines, chopper circuits) that fall outside the scope of UPSC/SSC/banking central exam syllabi. These items appear predominantly translated from English and constitute a significant fraction of the sample.
- **Deployment relevance:** UPSC, SSC CGL, and banking exams do not test specialist engineering knowledge at this level. Benchmark accuracy on these items measures specialized engineering knowledge, not the GK/History/Polity/Reasoning competencies that the deployment targets. High model performance on engineering items inflates overall benchmark scores without corresponding validity for the deployment context.
- **Datapoint citations:**
  - [D35] Example 1 (MILU/Hindi, validation): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — DC series motor behavior (Engineering)
  - [D36] Example 3 (MILU/Hindi, validation): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" — Half-wave rectifier (Engineering)
  - [D37] Example 8 (MILU/Hindi, validation): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN programming (Engineering/Computer Science)
  - [D38] Example 104 (MILU/Hindi, validation): "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" — Intermediate frequency for AM receivers (Engineering)

#### MAJOR Concern 5: Current Affairs Questions Are Significantly Dated
- **Dimension(s):** IC, IO
- **Observation:** Current Affairs is one of the most heavily weighted and dynamic UPSC GS areas. The sample contains multiple Current Affairs questions tied to specific dates in 2018–2022, including GDP growth rates for Q2 2018-19, cabinet minister assignments as of 2018, international events in 2019–2022. These questions would have stale or incorrect answers for students preparing for 2024-2026 exams.
- **Deployment relevance:** UPSC Current Affairs directly covers the preceding year; questions about 2018-2022 events are outdated for students currently preparing. A model evaluated highly on these items may still fail on current 2024-2025 affairs questions, and the benchmark cannot capture this currency dimension at all.
- **Datapoint citations:**
  - [D19] Example 74 (MILU/Hindi, validation, option4): "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी?" — GDP figure from 2018-19; outdated for current exam prep
  - [D20] Example 132 (MILU/Hindi, validation, option4): "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं?" — Ministry head as of 2018; politically outdated
  - [D21] Example 88 (MILU/Hindi, validation, option1): "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा।" — 2019 space event Current Affairs
  - [D22] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — 2022 sports event, dated

#### MAJOR Concern 6: Significant South India–Specific Content in Hindi Dataset
- **Dimension(s):** IC
- **Observation:** Several questions in the Hindi-labeled sample test knowledge that is specific to South Indian states (Telangana, Andhra Pradesh, Tamil Nadu) or South Indian literary/cultural heritage — including T-Hub Telangana, Tamil classical texts (Silappathikaram), Telangana book ('Telangana Rastrodayamalu'), Tamil cartoons, and Pandya kingdom history. While pan-India GK may include some of this, the density of Telangana/Tamil-specific items in a Hindi deployment is unexpected.
- **Deployment relevance:** Central exam syllabi do cover pan-India GK, but North India–based Hindi-medium students would not encounter these as high-priority preparation topics. Moreover, the benchmark documents that regional state exam questions are pooled across language partitions via translation — these may originate from Telugu/Tamil state exam questions translated into Hindi, representing a category mismatch for central-exam preparation.
- **Datapoint citations:**
  - [D33] Example 126 (MILU/Hindi, validation, option3): "निम्नलिखित में से किसने 'तेलंगाना राष्ट्रोदयमालु' पुस्तक लिखी?" — Telangana-specific literary question
  - [D34] Example 41 (MILU/Hindi, validation, option1): "टी-हब तेलंगाना राज्य सरकार की एक पहल है" — Telangana state government policy
  - [D32] Example 108 (MILU/Hindi, validation, option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए?" — Tamil literary history question
  - [D31] Example 52 (MILU/Hindi, validation, option2): "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था" — Pandya kingdom (South Indian history)

---

#### MINOR

#### MINOR Concern 1: Reasoning Questions Use Transliterated English Letters, Introducing Mild Code-Mixing
- **Dimension(s):** IC, IF
- **Observation:** Some logical reasoning questions use transliterated English letter names in Hindi script (e.g., "एमएनक्यू", "एमओक्यू" for MNQ, MOQ) rather than Hindi-medium equivalent notation. While this is a minor form of code-mixing, it may create unnatural reading for students accustomed to Hindi-medium reasoning materials.
- **Deployment relevance:** The ~10% code-mixing ceiling is set for content, not isolated letter labels in pattern sequences; this is likely acceptable. However, the transliteration may be less natural than using the Latin letters directly (which Hindi-medium exam books do routinely).
- **Datapoint citations:**
  - [D57] Example 145 (MILU/Hindi, validation, option2): "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा? एमएनक्यू / एमओक्यू" — Transliterated letter group names

#### MINOR Concern 2: Potential Answer Quality Issue — 'None of These' as Correct Answer for Factual Question
- **Dimension(s):** OC
- **Observation:** Example 109 asks about the constitutional article governing municipal election supervision in Chhattisgarh and the correct answer is "इनमें से कोई नहीं" (none of these). The provided options include Articles 243(ख), 243(क), and 241(ग). 'None of these' as the correct answer for a specific constitutional article question raises a potential data quality concern — either the correct article number was not included in the options, or the source portal recorded an ambiguous answer.
- **Deployment relevance:** Questions where 'none of these' is the correct answer are inherently difficult to explain in a rationale-based deployment, and may reflect data quality issues from the scraping pipeline (correct option not included in the option set).
- **Datapoint citations:**
  - [D49] Example 109 (MILU/Hindi, validation, option4): "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए पर्यवेक्षण, दिशा और नियंत्रण का प्रावधान किस अनुच्छेद में है? इनमें से कोई नहीं" — 'None of these' as answer to specific constitutional article query

#### MINOR Concern 3: Non-India–Specific Literary Questions with Low Deployment Relevance
- **Dimension(s):** IC
- **Observation:** A small number of questions test knowledge about non-Indian subjects that are tangentially connected to India's GK scope — such as the nationality of William Wordsworth or the 2019 Man Booker Prize winner (Bernadine Evaristo). These may appear in some competitive exam general awareness sections but are at the periphery of UPSC/SSC core content.
- **Deployment relevance:** These items represent minor dilution of deployment-relevant content. Their presence is not harmful but adds noise for the target student population.
- **Datapoint citations:**
  - [D39] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं।" — Wordsworth's nationality, borderline relevance to central exam GK

---

### Content Coverage Summary

The 245-sample Hindi validation set covers a broad range of subjects with meaningful representation of Indian Polity/Constitution, Indian History (ancient, medieval, and modern), Indian Economy, Environmental Science/Geography, and Health/Medicine. Logical Reasoning (seating arrangements, syllogisms, blood relations, coding-decoding, series completion) is present as a subject under the Science domain, partially addressing the documented taxonomy gap. Quantitative arithmetic questions (simple/compound interest, averages) appear within Business Studies/Economics.

North India–specific content is present but not dominant: examples covering UP minerals, Chikankari (UP embroidery), Rajasthan geography and literacy, Kota painting, and Bihar/UP agricultural data confirm some sub-regional coverage. However, the sample does not include Chhath Puja, zamindari/land-revenue history, or North Indian freedom movement figures beyond Sardar Patel and general mentions.

A notable characteristic is that 100% of the 245 reviewed examples have `is_translated=True`, which may reflect the composition of the validation split specifically. The translated items include heavy representation of specialist Engineering & Technology and Computer Science content (DC motors, FORTRAN, AM/FM modulation, rectifiers) that falls outside UPSC/SSC/banking central exam syllabi. Several questions are structurally incomplete — answer options reference lists, statements, or sentences absent from the question text, likely artifacts of the source portal scraping process.

Current Affairs content is present but dated to 2018–2022, creating a staleness concern for students preparing for 2025–2026 central exams. English vocabulary questions (synonym/meaning of 'grim', 'didactic', 'Evangelize') are labeled as Hindi Language Studies content but test English word knowledge, which is misaligned with Hindi-medium students' target exam requirements.

The benchmark has no rationale or explanation fields — every item is a bare MCQ with a correct label only.

---

### Limitations

1. **Translation rate in validation split**: All 245 reviewed examples have `is_translated=True`. It is unclear whether this reflects the full validation split composition or a systematic ordering in the parquet file. The test split (14,831 examples) likely has a substantially different translation rate and subject distribution; findings about over-representation of engineering content and translation artifacts may not fully generalize.

2. **Sample size relative to total dataset**: 245 examples from a 14,831-example test set and 812-example validation set; topic distribution within the full dataset may differ from the sample. Rare subjects (Chhath Puja, land-revenue systems, specific North Indian historical figures) may be present in the full test set but absent from this sample.

3. **No inspection of test split**: The test set (14,831 examples) was not reviewed. Domain/subject distribution, translation rates, and data quality issues (truncated questions) in the test split are unconfirmed.

4. **Code-mixing cannot be quantified**: While specific English terms (RMS, AM, PCM, RBI, GDP, FORTRAN) appear in questions, a systematic quantitative estimate of English term density per question is not possible from manual review of 245 examples.

5. **Answer correctness not independently verifiable**: The target labels are inherited from exam portal answer keys. For the ~5 structurally truncated questions (where option lists are absent), the correctness of the labeled answer cannot be assessed without the original source.

6. **North India sub-regional coverage**: The sample confirms some UP/Rajasthan content but cannot establish whether Chhath Puja, zamindari abolition, specific North Indian freedom fighters, or Bihar-specific history appear in the test set at deployable density.

7. **Validation split composition uncertainty**: The fact that all 245 validation examples are translated may indicate the validation split was specifically constructed from translated items, or may be a coincidence of sampling order. This cannot be resolved without examining the full split statistics.