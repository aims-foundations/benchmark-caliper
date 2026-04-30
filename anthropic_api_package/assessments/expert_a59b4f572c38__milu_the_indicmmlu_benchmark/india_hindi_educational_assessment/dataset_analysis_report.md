## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi config)
**Analysis date:** 2025-01-30
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | MILU/Hindi | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" | DC series motor no-load speed — translated Engineering item | IC, IF |
| D2 | MILU/Hindi | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" | Constitutional amendment — Law & Governance item | IO, IC |
| D3 | MILU/Hindi | 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" | William Wordsworth's nationality — translated Arts/Literature item, non-Indian literary content | IC |
| D4 | MILU/Hindi | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" | Hindi indirect speech conversion — Language Studies item | IC, IF |
| D5 | MILU/Hindi | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" | Mughal text authorship — History item with India-specific content | IO, IC |
| D6 | MILU/Hindi | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" | UP-specific minerals question — North Indian regional geography | IC, IO |
| D7 | MILU/Hindi | 28 | option2 | "निम्नलिखित में से कौन खेरवार आंदोलन के नेता थे? भागीरथ मांझी" | Kherwar movement leader — regional tribal history | IC |
| D8 | MILU/Hindi | 32 | option4 | "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया। इल्तुतमिश" | Completion of Qutub Minar — medieval Indian history | IO, IC |
| D9 | MILU/Hindi | 48 | option3 | "भांड पाथेर थिएटर मुख्य रूप से भारत के निम्नलिखित में से किस राज्य/केंद्र शासित प्रदेश की परंपरा है? जम्मू और कश्मीर" | Bhand Pather theatre tradition — regional Indian arts | IC |
| D10 | MILU/Hindi | 52 | option2 | "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था सुंदर पांड्यन" | Pandya kingdom history — South Indian dynastic history, not North India | IC |
| D11 | MILU/Hindi | 54 | option3 | "भारत की पहली टेक्नीकलर फिल्म कौन सी है? झांसी की रानी" | First Technicolor Indian film — India GK, Rani Lakshmibai connection | IC |
| D12 | MILU/Hindi | 57 | option4 | "किस राज्य सरकार ने राज्य भर में इलेक्ट्रॉनिक सिगरेट के निर्माण और बिक्री-खरीद पर पूर्ण प्रतिबंध लगाया है? बिहार" | Bihar e-cigarette ban — North Indian state-level policy | IC |
| D13 | MILU/Hindi | 64 | option3 | "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है? सरदार वल्लभभाई पटेल" | Iron Man of India — national GK, competitive exam style | IO, IC |
| D14 | MILU/Hindi | 65 | option4 | "झारखंड की उप राजधानी क्या है? दुमका" | Jharkhand sub-capital — regional Indian geography | IC |
| D15 | MILU/Hindi | 68 | option2 | "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है? बीकानेर" | Rajasthan reserved area — North Indian state-specific geography | IC |
| D16 | MILU/Hindi | 76 | option2 | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" | Meaning of English word 'didactic' asked in Hindi — English vocabulary test | IC |
| D17 | MILU/Hindi | 83 | option1 | "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है" | Civil officer ethics scenario — UPSC/civil services ethics framing | IO, IC |
| D18 | MILU/Hindi | 90 | option3 | "शब्द 'grim' का पर्यायवाची लिखें। भयानक" | Synonym of English word 'grim' asked in Hindi | IC |
| D19 | MILU/Hindi | 93 | option2 | "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है? पंचायत समिति" | Three-tier Panchayati Raj — civics, relevant to North Indian governance | IC, IO |
| D20 | MILU/Hindi | 97 | option3 | "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" | Hindi postposition fill-in — language/grammar item | IC, IF |
| D21 | MILU/Hindi | 98 | option1 | "किस प्रसिद्ध कश्मीरी कवि को आमतौर पर 'कश्मीर का जॉन कीट्स' कहा जाता है? रसूल मीर" | Kashmiri poet comparison to John Keats — regional literature | IC |
| D22 | MILU/Hindi | 105 | option4 | "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" | English vocabulary 'Evangelize' — meaning tested in Hindi | IC |
| D23 | MILU/Hindi | 108 | option3 | "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए? सी. सुब्रह्मण्य भारती" | First cartoons in Tamil magazine — South Indian literary history | IC |
| D24 | MILU/Hindi | 115 | option4 | "निम्नलिखित लेखकों में से किसने लघु कथाओं के संग्रह 'किस्सा किस्सा लखनऊवा' के लिए साहित्य अकादमी युवा पुरस्कार 2021 जीता? हिमांशु वाजपेयी" | Sahitya Akademi award for Lucknow-themed stories — North Indian literary content | IC |
| D25 | MILU/Hindi | 130 | option4 | "2019 का मैन बुकर पुरस्कार फिक्शन के लिए जीतने वाली पहली अश्वेत महिला कौन बनी हैं? बर्नाडिन एवरिस्टो" | Man Booker Prize winner — international literary GK | IC |
| D26 | MILU/Hindi | 156 | option1 | "2011 की जनगणना के अनुसार राजस्थान की कुल साक्षरता का लगभग प्रतिशत कितना है? 66.11%" | Rajasthan literacy rate — North Indian state statistics | IC |
| D27 | MILU/Hindi | 182 | option1 | "निम्नलिखित में से किस राज्य ने 2011 - 12 में सबसे अधिक दूध उत्पादन दर्ज किया? उत्तर प्रदेश" | Milk production by state — UP-relevant agricultural GK | IC |
| D28 | MILU/Hindi | 190 | option2 | "राजस्थान का आकार है- समचतुर्भुज" | Rajasthan's shape — state-specific geography | IC |
| D29 | MILU/Hindi | 193 | option3 | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है? महाराव उम्मेद सिंह I" | Kota painting school — Rajasthan regional arts | IC |
| D30 | MILU/Hindi | 198 | option2 | "छत्तीसगढ़ के निम्नलिखित विद्रोहों में से किसे 'बस्तर का स्वतंत्रता संग्राम' भी कहा जाता है? लिंगागिरी विद्रोह" | Chhattisgarh tribal revolt — Central Indian regional history | IC |
| D31 | MILU/Hindi | 211 | option3 | "राजस्थान सरकार ने मौसमी और गैर-संचारी रोगों की निगरानी के लिए...कौन सा सॉफ्टवेयर लॉन्च किया है? निदान" | Rajasthan state health software — state-level policy GK | IC |
| D32 | MILU/Hindi | 213 | option1 | "राजतरंगिणी के लेखक कौन हैं? कल्हण" | Rajatarangini author — classical Sanskrit text, competitive-exam GK | IC |
| D33 | MILU/Hindi | 232 | option2 | "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है? इलंगो अडिगल" | Tamil epic Silappatikaram — South Indian literary history | IC |
| D34 | MILU/Hindi | 242 | option4 | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" | UP handicraft Chikankari — North Indian craft, directly relevant | IC, IO |
| D35 | MILU/Hindi | All 245 | — | All 245 examples have `is_translated: True` | Every sampled item is marked as translated from English | IC, IF |
| D36 | MILU/Hindi | 36 | option3 | "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है। TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______." | Letter series with English alphabet labels — Logical Reasoning item | IC, IF |
| D37 | MILU/Hindi | 56 | option2 | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...केवल (1) और (3)" | Reference to numbered statements not present in the question field — truncated/incomplete item | IC, IF |
| D38 | MILU/Hindi | 69 | option2 | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल" | Options reference (a),(b),(c),(d) labels absent from question stem — truncated item | IC, IF |
| D39 | MILU/Hindi | 86 | option2 | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" | Options reference A,B,C,D,E state labels not named in the question — truncated item | IC, IF |
| D40 | MILU/Hindi | 95 | option1 | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। AEDBCF" | Sentence ordering question where actual sentences B,C,D,E are missing | IC, IF |
| D41 | MILU/Hindi | 106 | option2 | "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" | Ordering question where the numbered substances are not listed | IC, IF |
| D42 | MILU/Hindi | 188 | option3 | "नई शिक्षा नीति 2020 में देखा गया है...निम्नलिखित में से किन समस्याओं का सामना कर रही है? उपरोक्त सभी" | Sub-items (a),(b) not listed in question stem — truncated | IC, IF |
| D43 | MILU/Hindi | 118 | option2 | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें। अपने काम को बेहतर तरीके से व्यवस्थित करना" | Idiom question with no idiom in the stem — missing content | IC, IF |
| D44 | MILU/Hindi | 151 | option1 | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं। केवल तर्क I मजबूत है" | Statement and arguments not present in question field — truncated item | IC, IF |
| D45 | MILU/Hindi | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" | FORTRAN 77 programming — highly specialized computing, unlikely in state board | IO |
| D46 | MILU/Hindi | 104 | option4 | "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" | AM receiver intermediate frequency — specialized electronics | IO |
| D47 | MILU/Hindi | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | Archery Asia Cup 2022 results — current affairs, time-sensitive | IC |
| D48 | MILU/Hindi | 34 | option1 | "किस कानून के तहत, विधायिका के सदस्य बजट की आलोचना नहीं कर सकते थे? भारतीय परिषद अधिनियम-1892" | Colonial Indian Council Act — constitutional/legal history | IO, IC |
| D49 | MILU/Hindi | 135 | option3 | "पंचायतों के संबंध में निम्नलिखित में से कौन सा/से सही है/हैं?...नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" | Option4 of the MCQ is an instruction ("use the code below"), not an answer — malformed item | OO |
| D50 | MILU/Hindi | 10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" | Blue Baby Syndrome cause — Health/Medicine competitive-exam item | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Devanagari Hindi script with standard formal register throughout
- **Dimension(s):** IF, IC
- **Observation:** All 245 sampled items are rendered in standard Devanagari Unicode Hindi with a formal, pan-India Khari Boli register appropriate for competitive examinations and board-level assessments. Vocabulary is standard Sanskrit-derived academic Hindi (e.g., "संवैधानिक संशोधन", "पंचायती राज प्रणाली", "सहजीवी संबंध"). No script inconsistencies, romanisation, or Perso-Arabic loanword conflicts were observed.
- **Deployment relevance:** The deployment requires Devanagari script text-only interaction. The consistent formal Hindi register matches what North Indian board teachers and students encounter in official examination materials.
- **Datapoint citations:**
  - [D4] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Standard formal Hindi grammatical question, consistent with board-level language items.
  - [D20] Example 97 (MILU/Hindi, validation, option3): "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" — Hindi postposition fill-in, academic register.

#### Strength 2: Strong MCQ structural alignment with deployment format
- **Dimension(s):** IO, OO
- **Observation:** All 245 sampled items are 4-option single-correct-answer MCQs with a single `target` field containing the correct option label. The binary correct/incorrect evaluation schema is structurally identical to the deployment's positive/negative marking requirement. No multi-select, open-ended, or partial-credit items appear in the sample.
- **Deployment relevance:** The deployment requires strict MCQ format with single correct answers and binary scoring. MILU's format is a precise match, reducing any format-translation burden.
- **Datapoint citations:**
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — Classic 4-option MCQ, single correct answer.
  - [D13] Example 64 (MILU/Hindi, validation, option3): "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है?" — Standard GK MCQ format.

#### Strength 3: Meaningful coverage of India-centric Law & Governance and Civics content
- **Dimension(s):** IO, IC
- **Observation:** Multiple items address Indian constitutional law (constitutional amendments, writs, parliamentary procedure), Panchayati Raj (three-tier system, gram sabha), and India-specific legal provisions (SC/ST Prevention of Atrocities Act, Sati Prevention Act). These subjects align directly with the civics and political science portions of North Indian board syllabi.
- **Deployment relevance:** North Indian state board syllabi (UP, MP, Rajasthan, Bihar) prominently include Indian polity and constitutional studies. Items on Panchayati Raj (Example 93), constitutional writs (Example 33), and constitutional amendments (Example 6, 39, 136) are directly deployable against board-level student assessments.
- **Datapoint citations:**
  - [D19] Example 93 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा तीन स्तरीय पंचायती राज प्रणाली की मध्य इकाई है? पंचायत समिति" — Panchayati Raj content directly relevant to North Indian civics syllabi.
  - [D2] Example 6 (MILU/Hindi, validation, option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" — Constitutional amendment knowledge.
  - [D48] Example 34 (MILU/Hindi, validation, option1): "किस कानून के तहत, विधायिका के सदस्य बजट की आलोचना नहीं कर सकते थे? भारतीय परिषद अधिनियम-1892" — Indian legislative history.

#### Strength 4: Meaningful presence of North Indian state-specific geographical and cultural content
- **Dimension(s):** IC
- **Observation:** Several items in the sample are directly anchored to North Indian states: UP minerals (Example 26), Rajasthan's district geography (Example 68, 190), Rajasthan literacy statistics (Example 156), UP milk production (Example 182), Rajasthan health policy (Example 211), and UP's Chikankari craft (Example 242). This confirms that MILU's region-specific exam sourcing does include some Hindi-belt state content.
- **Deployment relevance:** The deployment population of North Indian teachers needs to evaluate students on state-board content about their own states. These items demonstrate that MILU is not exclusively pan-India competitive content.
- **Datapoint citations:**
  - [D6] Example 26 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" — UP-specific geography question.
  - [D15] Example 68 (MILU/Hindi, validation, option2): "निम्नलिखित में से राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है? बीकानेर" — Rajasthan district-level geography.
  - [D34] Example 242 (MILU/Hindi, validation, option4): "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है...चिकनकारी" — UP handicraft, directly North Indian cultural content.
  - [D28] Example 190 (MILU/Hindi, validation, option2): "राजस्थान का आकार है- समचतुर्भुज" — Rajasthan-specific geographic question.

#### Strength 5: Coverage of Indian medieval and modern history in Hindi
- **Dimension(s):** IO, IC
- **Observation:** History items cover Mughal-era texts (Example 25), medieval construction history (Example 32), Indian freedom movement framing (Example 64, 235), ancient Indian history (Example 158, 237), and colonial-era governance (Example 50, 96). These are standard components of North Indian board history syllabi.
- **Deployment relevance:** History is a core subject in all Hindi state board syllabi. Items on Ashoka (Example 158), the Qutub Minar (Example 32), the Iron Man of India (Example 64), and Harappan cities (Example 237) align with topics examined at secondary level in UP, MP, Rajasthan, and Bihar boards.
- **Datapoint citations:**
  - [D8] Example 32 (MILU/Hindi, validation, option4): "_______ ने दिल्ली में कुतुब मीनार का निर्माण पूरा किया। इल्तुतमिश" — Medieval Indian history.
  - [D5] Example 25 (MILU/Hindi, validation, option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — Mughal historiography.

#### Strength 6: Hindi language and grammar items present in Language Studies subject
- **Dimension(s):** IC, IO
- **Observation:** The sample includes Hindi grammatical exercises covering active/passive voice conversion (Example 51, 91), indirect speech (Example 9), postposition usage (Example 97), and fill-in-the-blank sentence completion (Example 152). These are directly aligned with Hindi language instruction at board level.
- **Deployment relevance:** Hindi Language and Literature is a compulsory subject in all North Indian board curricula. Grammar items on voice, indirect speech, and postpositions are standard components of Class 10–12 Hindi papers.
- **Datapoint citations:**
  - [D4] Example 9 (MILU/Hindi, validation, option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — Indirect speech (reported speech) conversion.
  - [D20] Example 97 (MILU/Hindi, validation, option3): "टीना कक्षा के सभी छात्रों में सबसे बुद्धिमान ________ है। का" — Hindi postposition fill-in.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: 100% of sampled validation items are marked `is_translated: True`
- **Dimension(s):** IC, IF
- **Observation:** All 245 sampled examples from the Hindi validation split carry `is_translated: True`. The benchmark documentation states that only ~25% of total questions across all 11 languages were translated from English; if Hindi's validation split is entirely composed of translated items, this would substantially exceed the reported dataset-wide average. Even if this is an artifact of the validation split (vs. the test split), an evaluator relying on the validation split for few-shot examples would be drawing exclusively from translated content.
- **Deployment relevance:** Translated items may not reflect the natural Hindi academic register used in North Indian board assessments. GPT-4O translations may produce grammatically correct but register-misaligned Hindi — particularly for subject-specific terminology (science, economics, civics) — that diverges from what UP, MP, Rajasthan, or Bihar board students and teachers would encounter. This is the single highest-risk finding in the sample.
- **Datapoint citations:**
  - [D35] All 245 examples: `is_translated: True` on every record — every item in the validation split is a translation.
  - [D1] Example 1 (MILU/Hindi, validation, option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: मोटर की गति बहुत अधिक होती है" — Translated engineering item; technical Hindi vocabulary (e.g., "डीसी सीरीज मोटर") may follow English-derived transliteration rather than standardised Hindi scientific terminology.
  - [D3] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — Translated item on a British poet, clearly sourced from English.

---

#### MAJOR

#### MAJOR Concern 1: Numerous items with truncated or missing question stems rendering them unevaluable
- **Dimension(s):** IC, IF
- **Observation:** At least 7–8 items in the 245-item sample have options that reference content (numbered statements, lettered sub-items, named sentences) that is absent from the `question` field. This indicates that the original question included a table, passage, or list that was stripped during scraping, leaving the MCQ shell unanswerable without the missing context.
- **Deployment relevance:** If a deployed LLM encounters these items, it cannot evaluate the question correctly — neither can a teacher using the benchmark for reference. These items inflate measurement error and cannot serve their intended evaluative function.
- **Datapoint citations:**
  - [D37] Example 56 (MILU/Hindi, validation, option2): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें...केवल (1) और (3)" — Four statements referenced but absent from question stem.
  - [D38] Example 69 (MILU/Hindi, validation, option2): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल" — Options reference (a),(b),(c),(d) items absent from question.
  - [D39] Example 86 (MILU/Hindi, validation, option2): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, D और E" — State labels A–E not identified in the question.
  - [D40] Example 95 (MILU/Hindi, validation, option1): "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। AEDBCF" — The actual sentences are missing.
  - [D41] Example 106 (MILU/Hindi, validation, option2): "निम्नलिखित पदार्थों को प्रयोगशाला में उनकी पहली संश्लेषण की कालानुक्रमिक क्रम में व्यवस्थित करें: 4 2 3 1" — Numbered substances not listed.
  - [D43] Example 118 (MILU/Hindi, validation, option2): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें। अपने काम को बेहतर तरीके से व्यवस्थित करना" — The idiom itself is absent from the question field.
  - [D44] Example 151 (MILU/Hindi, validation, option1): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं। केवल तर्क I मजबूत है" — Statement and arguments missing from stem.
  - [D42] Example 188 (MILU/Hindi, validation, option3): "नई शिक्षा नीति 2020 में देखा गया है...निम्नलिखित में से किन समस्याओं का सामना कर रही है? उपरोक्त सभी" — Sub-items (a),(b) absent.

#### MAJOR Concern 2: Absence of canonical Hindi literary figures (Tulsidas, Premchand, Kabir, Mahadevi Varma) from the sample
- **Dimension(s):** IC, IO
- **Observation:** No item in the 245-item sample tests knowledge of canonical Hindi-board literary figures — Tulsidas, Premchand, Kabir, Mahadevi Varma, Harivansh Rai Bachchan, or Surdas. The Literature and Linguistics items present are either about: (a) English literary figures (William Wordsworth, Example 7; Man Booker Prize winner, Example 130), (b) South Indian authors (C. Subramania Bharati, Example 108; Silappatikaram, Example 232; Telugu author, Example 126), (c) English vocabulary meanings ('didactic', Example 76; 'grim', Example 90; 'Evangelize', Example 105), or (d) regional/marginal Hindi literary awards (Example 115). While the sample is limited to the validation split and may not reflect test split content, this complete absence is notable.
- **Deployment relevance:** Canonical Hindi literature (Ramcharitmanas, Premchand's Godan, Kabir's dohas) is a required component of every Hindi state board syllabus (UP, MP, Rajasthan, Bihar) at Class 9–12. A benchmark used to evaluate MCQ responses from Hindi-board students that lacks these authors cannot validly assess Hindi literature performance in the deployment context.
- **Datapoint citations:**
  - [D3] Example 7 (MILU/Hindi, validation, option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — British poet identified instead of Hindi literary canon.
  - [D33] Example 232 (MILU/Hindi, validation, option2): "क्लासिकल तमिल महाकाव्य 'सिलप्पतिकारम' की रचना का श्रेय किस लेखक को दिया जाता है? इलंगो अडिगल" — South Indian Tamil epic, not North Indian Hindi literature.
  - [D22] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" — English vocabulary test embedded in Hindi Language Studies subject.
  - [D16] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" — English word meaning tested in Hindi Language Studies.

#### MAJOR Concern 3: Competitive-exam framing dominates; minimal school-board syllabus framing visible
- **Dimension(s):** IO, IC
- **Observation:** The vast majority of items in the sample are structured as UPSC/SSC/state civil service GK-style questions — current affairs (Examples 2, 11, 35, 88, 131), government schemes and policies (Examples 82, 102, 122, 148, 239), constitutional/legal facts (Examples 6, 33, 34, 39, 42, 46, 136), and administrative GK (Examples 50, 71, 72, 132, 165). Only a small subset of items (Hindi grammar, some art history, a few biology/chemistry items) resembles the classroom-instruction framing typical of board-level syllabi. Ethics scenario items (Example 83) are explicitly UPSC Civil Services Paper II format.
- **Deployment relevance:** North Indian board teachers assess students on syllabus-aligned content, not current-affairs or civil-service GK. A benchmark skewed toward civil-service exam framing will produce validity estimates that do not reflect whether an LLM can evaluate students on UP Board Class 12 Hindi, History, or Science papers.
- **Datapoint citations:**
  - [D17] Example 83 (MILU/Hindi, validation, option1): "एक वरिष्ठ सिविल अधिकारी के रूप में, आपको निजी रूप से संचालित वृद्धाश्रम के वार्षिक समारोह में अतिथि बनने के लिए आमंत्रित किया गया है..." — Clearly UPSC GS Paper II (Ethics, Integrity and Aptitude) format scenario.
  - [D47] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Current affairs sports GK, not a board syllabus topic.
  - [D13] Example 64 (MILU/Hindi, validation, option3): "भारत के 'लौह पुरुष' के रूप में किसे जाना जाता है? सरदार वल्लभभाई पटेल" — Standard competitive-exam GK format.

#### MAJOR Concern 4: English-vocabulary questions embedded in Hindi Language Studies subject
- **Dimension(s):** IC, IO
- **Observation:** Multiple items in the Language Studies and Literature and Linguistics subjects test the meaning or synonym of English words, presented in a Hindi instructional frame. Examples include: meaning of 'didactic' (Example 76), synonym of 'grim' (Example 90), meaning of 'Evangelize' (Example 105), and active/passive voice for "क्या आवाज़ ने उसे परेशान किया?" (an English-language structure reframed in Hindi, Example 91). These appear to be translated from English-medium competitive exam language papers.
- **Deployment relevance:** Hindi state board Language Studies papers test Hindi grammar and Hindi literature, not English vocabulary. Items testing synonyms of English words, when labelled as Hindi Language Studies, would produce systematically misleading validity estimates for the deployment — a model that succeeds on these items is being tested on English proficiency, not Hindi Language Studies competence.
- **Datapoint citations:**
  - [D16] Example 76 (MILU/Hindi, validation, option2): "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है? नैतिक पाठ पढ़ाना" — Testing English word meaning within Hindi Language Studies subject.
  - [D18] Example 90 (MILU/Hindi, validation, option3): "शब्द 'grim' का पर्यायवाची लिखें। भयानक" — English synonym tested in Hindi.
  - [D22] Example 105 (MILU/Hindi, validation, option4): "निर्देश: निम्नलिखित प्रश्न में...Evangelize [का अर्थ] उपदेश देना" — English religious term meaning in Hindi Language Studies.

#### MAJOR Concern 5: Malformed answer option — an instruction appearing as an answer choice
- **Dimension(s):** OO, IF
- **Observation:** Example 135 (Panchayats/Politics and Governance) has its fourth option read: "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" ("Select the correct answer using the code below:") — a formatting instruction from the original question, not an answer choice. The target is `option3`. This is a scraping artifact where the answer-code table was stripped but the instruction line was retained as an option.
- **Deployment relevance:** If a deployed model encounters this item, it may select option4 (the instruction) as an answer. This is a data quality defect that can corrupt both model evaluation scores and teacher trust in the system.
- **Datapoint citations:**
  - [D49] Example 135 (MILU/Hindi, validation, option3): "पंचायतों के संबंध में...नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें:" — An instruction line masquerading as answer option 4.

---

#### MINOR

#### MINOR Concern 1: Non-North-Indian regional content takes substantial share of Arts & Humanities and History
- **Dimension(s):** IC
- **Observation:** Several Arts & Humanities History and Literature items in the sample concern South Indian history and literature: Pandya kingdom (Example 52), Tamil epic Silappatikaram (Example 232), Tamil magazine cartoons (Example 108), Telugu book authorship (Example 126), Kashmiri poet (Example 98), and Kota painting (Rajasthan, Example 193). While pan-Indian content is appropriate for general competitive exams, it dilutes the North Indian board syllabus alignment for this specific deployment.
- **Deployment relevance:** North Indian board history syllabi emphasise Mughal, Rajput, and North Indian medieval history, and North Indian freedom movement figures. South Indian dynastic history (Pandya, Chola) and Tamil literary history are less emphasized. This is a calibration concern rather than a fundamental misalignment.
- **Datapoint citations:**
  - [D10] Example 52 (MILU/Hindi, validation, option2): "वह पांड्य राजा जिसने पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया था, वह था सुंदर पांड्यन" — South Indian Pandya dynasty, not a North Indian board syllabus priority.
  - [D23] Example 108 (MILU/Hindi, validation, option3): "तमिल पत्रिका में सबसे पहले कार्टून चित्र किसने प्रस्तुत किए? सी. सुब्रह्मण्य भारती" — Tamil literary history.

#### MINOR Concern 2: Time-sensitive current-affairs items create staleness risk
- **Dimension(s):** IC, OC
- **Observation:** Multiple items are tied to specific events from 2018–2022 with exact statistics that become outdated (e.g., India's GDP growth rate in July–September 2018, Example 74; ASSOCHAM president December 2020, Example 123; Minister of WCD in 2018, Example 132; India's first UNDP Youth Climate Champion in January 2022, Example 239). These items have objectively correct answers only at a specific point in time.
- **Deployment relevance:** If teachers use MILU items to create new assessment questions, or if the LLM is evaluated on whether it correctly marks student answers to these current-affairs questions, staleness could cause the system to mark correct historical answers as incorrect if the LLM's training data reflects a different time period.
- **Datapoint citations:**
  - [D47] Example 2 (MILU/Hindi, validation, option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Time-stamped sports result.
  - Example 132 (MILU/Hindi, validation, option4): "2018 तक, महिला और बाल विकास मंत्रालय (MWCD) के केंद्रीय मंत्री कौन हैं? मेनेका गांधी" — Cabinet position tied to a specific year.

#### MINOR Concern 3: Highly specialised Engineering and Tech content unlikely to appear in school-board assessments
- **Dimension(s):** IO
- **Observation:** A substantial number of Engineering & Tech items are highly specialised — FORTRAN 77 programming (Example 8), AM/SSB-SC modulation bandwidth (Example 43, 104), TDM frame rate calculations (Example 47), and timber fibre swelling percentages (Example 12). These are appropriate for polytechnic entrance exams or engineering qualification tests but not for school-board level assessments.
- **Deployment relevance:** The deployment covers all board types including secondary level, where Engineering & Tech content would be introductory at most. The presence of advanced technical content within what is labelled as the Hindi MILU benchmark means the benchmark over-represents post-secondary technical exam difficulty for the school-board teacher deployment.
- **Datapoint citations:**
  - [D45] Example 8 (MILU/Hindi, validation, option1): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है?" — FORTRAN 77 programming — highly specialised computing, unlikely in any board syllabus.
  - [D46] Example 104 (MILU/Hindi, validation, option4): "540 kHz से 1650 kHz तक ट्यूनिंग करने वाले रिसीवर्स के लिए सबसे लोकप्रिय इंटरमीडिएट फ्रीक्वेंसी (kHz में) कौन सी है" — AM receiver IF — polytechnic/engineering level.

#### MINOR Concern 4: Logical Reasoning items use English alphabetic sequences
- **Dimension(s):** IC, IF
- **Observation:** Logical Reasoning items in the Science domain use sequences of Latin/English letters (TAB, TTZBB, etc. in Example 36; _q p p_ in Example 44; A, C, F, H, ?, M in Example 124) despite being presented in Hindi. The question wrapper is in Hindi but the reasoning object is English alphanumeric.
- **Deployment relevance:** This is a minor structural concern — Hindi board students are familiar with English alphabetic sequences in reasoning tests, which appear in many competitive exams. However, it does confirm the competitive-exam sourcing of Logical Reasoning items and may introduce a slight English-literacy dependency.
- **Datapoint citations:**
  - [D36] Example 36 (MILU/Hindi, validation, option3): "रिचा ने परीक्षा में निम्नलिखित श्रृंखला दी है...TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______. TTTTXBBBB" — Latin letter series reasoning.

---

### Content Coverage Summary

The Hindi validation split of MILU (245 items sampled) spans eight domains with notable concentration in Engineering & Tech (approx. 25%), Science (approx. 20%), Environmental Sciences including Geography and Agriculture (approx. 15%), and Arts & Humanities (approx. 20%), with smaller contributions from Business Studies, Law & Governance, Social Sciences, and Health & Medicine. All items are in standard formal Devanagari Hindi. The entire validation sample is marked `is_translated: True`, which is inconsistent with the paper's reported 25% dataset-wide translation rate and represents the most significant data-quality finding from the sample.

Content topics reflect a pan-Indian competitive-exam orientation: UPSC/SSC-style general knowledge, constitutional law, Indian polity, India-centric science GK, and current affairs. India-centric content is genuinely present (North Indian state geography, Panchayati Raj, Chikankari, medieval Indian history), but canonical Hindi board literary figures (Tulsidas, Premchand, Kabir) are entirely absent from the sample, and Hindi Literature and Linguistics items instead test English vocabulary meanings.

Data quality concerns are non-trivial: approximately 3–4% of sampled items have truncated stems where tables, passages, or sub-item lists were lost during scraping, rendering the question unanswerable. One item has a formatting instruction appearing as an answer option.

The register throughout is uniform formal Hindi — appropriate for the deployment — but the framing is overwhelmingly competitive-exam (UPSC/SSC/state civil service) rather than school/university board syllabus instruction.

---

### Limitations

1. **Validation split only:** All 245 examples are from the validation split (812 total items). The test split contains 14,831 Hindi items. The `is_translated: True` finding on all validation items may not generalise to the test split, which likely contains a higher proportion of natively sourced Hindi questions. The canonical Hindi literature absence, truncation defects, and competitive-exam framing findings should be verified against a sample of the test split before drawing strong conclusions.

2. **Sample size relative to total:** 245 items out of 15,643 total Hindi items (~1.6%) limits subject-level inferences. Subjects like Hindi Literature specifically may have more board-aligned items in the test split that did not appear in this sample.

3. **Subject distribution not controllable:** The sample was drawn from the validation split as provided; subject distribution within the sample may over- or under-represent specific subjects relative to the full test split.

4. **Translation quality not auditable from text alone:** While register concerns about GPT-4O translations can be flagged, assessing whether specific technical translations (electronics, chemistry, economics) use the correct Hindi-board terminology (Vaigyaanik evam Takniki Shabdavali Aayog standard terms vs. transliterated English) requires domain-expert review beyond what can be determined from reading the items.

5. **Annotator demographics unverifiable:** The demographic backgrounds of item annotators and the exam-source distribution for Hindi items cannot be determined from the dataset content alone, as this metadata is not exposed in the HuggingFace schema.

6. **Test split gating:** The test split is available via gated access on HuggingFace (auto-gated), meaning independent validation of subject distribution and translation rates for the full Hindi test set requires dataset access approval.