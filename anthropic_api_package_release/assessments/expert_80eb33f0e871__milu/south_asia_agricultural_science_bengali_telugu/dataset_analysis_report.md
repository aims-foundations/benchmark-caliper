## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (configs: Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total (Bengali: 21, English: 20, Gujarati: 24, Hindi: 26, Kannada: 17, Malayalam: 16, Marathi: 21, Odia: 21, Punjabi: 25, Tamil: 19, Telugu: 25) — all from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Bengali | Ex.7 | option4 | "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... জাতীয় খাদ্য সুরক্ষা মিশন মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" | National Food Security Mission: crop development scheme, soil health restoration — Indian scheme, no Bangladesh context | IO, IC |
| D2 | Bengali | Ex.1 | option3 | "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" | India's 1991 foreign reserve crisis — Indian economic history, irrelevant to Bangladesh agricultural deployment | IC |
| D3 | Bengali | Ex.1 | option3 | **is_translated:** True | All 21 Bengali validation examples are machine-translated from English | IF |
| D4 | Bengali | Ex.5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP)... পাঞ্জাব" | Indian state assembly election — Indian polity, no Bangladesh relevance | IC |
| D5 | Bengali | Ex.9 | option3 | "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" | Removal of Indian Election Commissioner — Indian constitutional law only | OC |
| D6 | English | Ex.5 | option1 | "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" | Mediterranean climate region identification — generic geography | IO |
| D7 | English | Ex.10 | option4 | "Which of the following are claimed as advantageous in respect of aerobic sludge digestion as compared to anaerobic sludge digestion?" | Wastewater engineering/environmental science — technically relevant but not agro-ecological | IO |
| D8 | English | Ex.9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" | Maharashtra state governance — India-specific law, not relevant to Bangladesh | IC, OC |
| D9 | English | Ex.13 | option4 | "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" | Telangana state welfare policy — classified under Geography, reflects generic Indian current affairs | IC, OO |
| D10 | Bengali | Ex.7 | option4 | domain: Environmental Sciences, subject: Agriculture | Agriculture-labeled question about India's National Food Security Mission — only MILU "Agriculture" example in Bengali sample | IO, IC |
| D11 | Kannada | Ex.7 | option4 | "ರಾಷ್ಟ್ರೀಯ ಆಹಾರ ಭದ್ರತಾ ಮಿಷನ್ ಒಂದು ಬೆಳೆ ಅಭಿವೃದ್ಧಿ ಯೋಜನೆ... ಮಣ್ಣಿನ ಆರೋಗ್ಯವನ್ನು ಪುನಃಸ್ಥಾಪಿಸಲು" | National Food Security Mission crop scheme in Kannada — same Indian policy content replicated across languages | IC, IO |
| D12 | Marathi | Ex.7 | option4 | "राष्ट्रीय अन्न सुरक्षा मिशन हे एक पीक विकास योजना आहे... मातीचे आरोग्य पुनर्संचयित करणे" | National Food Security Mission in Marathi — same question across languages confirms India-only policy content | IC |
| D13 | Marathi | Ex.21 | option3 | "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" | Location of National Mustard Research Centre in India — India-specific agricultural institution | IC, IO |
| D14 | Odia | Ex.21 | option4 | "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" | Which Indian company produces agricultural equipment rapidly (Kirloskar) — India-specific corporate knowledge | IC, IO |
| D15 | Punjabi | Ex.7 | option4 | "ਰਾਸ਼ਟਰੀ ਖਾਦ ਸੁਰੱਖਿਆ ਮਿਸ਼ਨ ਇੱਕ ਫਸਲ ਵਿਕਾਸ ਯੋਜਨਾ ਹੈ... ਮਿੱਟੀ ਦੀ ਸਿਹਤ ਨੂੰ ਬਹਾਲ ਕਰਨਾ" | National Food Security Mission in Punjabi — same cross-language India-scoped agriculture question | IC |
| D16 | Telugu | Ex.25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది?... మొరెనా" | Location of Banmore Industrial Development Centre in Madhya Pradesh — Indian geography | IC |
| D17 | Telugu | Ex.9 | option2 | "క్రింది వాటిలో మహారాష్ట్ర శాసనసభ కమిటీ వ్యవస్థ గురించి ఏ ప్రకటన సరైనది కాదు?" | Maharashtra Legislative Committee system in Telugu — state-specific Indian governance | IC, OC |
| D18 | English | Ex.5 | option1 | domain: Environmental Sciences, subject: Geography | Mediterranean climate question under Environmental Sciences — geographic reasoning, not agro-ecological depth | IO |
| D19 | Bengali | Ex.3 | option4 | "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল?... গুলবার্গা" | First capital of Bahmani Kingdom — medieval Indian history, no agriculture/environment relevance | IC |
| D20 | Bengali | Ex.12 | option4 | "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল" | "Mangal Bharat" literary work by Vinoba Bhave — Indian literary/national leader trivia | IC |
| D21 | Odia | Ex.2 | option4 | "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆକୁ ପ୍ରଥମେ ଜଣା ଦେଇଥିବା ଦେଶ କେଉଁଟି?... ଆଫଗାନିସ୍ତାନ; option2: ବାଙ୍ଗ୍ଲାଦେଶ" | Which country first reported Indian Pharmacopoeia (Afghanistan) — Bangladesh appears as wrong answer option | IC, OC |
| D22 | Hindi | Ex.10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है?... नाइट्रेट" | Blue Baby Syndrome caused by excess nitrate in blood — generic health/environmental science | IO |
| D23 | English | Ex.10 | option4 | "Lower BOD concentration in supernatant liquor... Production of a sludge with excellent dewatering propensity... aerobic sludge digestion" | Aerobic vs. anaerobic sludge digestion advantages — environmental engineering question | IO |
| D24 | Bengali | Ex.8 | option4 | "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া?" | Oxidation-reduction reactions — basic chemistry | IO |
| D25 | Telugu | Ex.2 | option4 | "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది?... ఆఫ్ఘనిస్తాన్; option2: బంగ్లాదేశ్" | Same Indian Pharmacopoeia question in Telugu — Bangladesh again used only as distractor | IC, OC |
| D26 | Bengali | Ex.2 | option3 | "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু... নির্বাচিত না হওয়া শিশুদের সংখ্যা এবং মোট শিশুদের সংখ্যার অনুপাত" | Ratio problem about cricket training camp — numeracy/reasoning, irrelevant to agricultural science | IO |
| D27 | Gujarati | Ex.8 | option3 | "રેડક્લિફ રેખા નીચેના પૈકી કયા દેશ સાથે ભારતની સરહદોને અલગ કરે છે?... પાકિસ્તાન" | Radcliffe Line divides India from Pakistan — Indian partition geography | IC |
| D28 | Hindi | Ex.6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?... 44वें संविधान संशोधन अधिनियम द्वारा" | Indian constitutional amendment for 'armed rebellion' clause — Indian law and governance | IC, OC |
| D29 | Marathi | Ex.16 | option3 | "हलषष्ठी सण का साजरा केला जातो?... मुलाच्या दीर्घायुष्यासाठी" | Halashashthi festival purpose (for son's longevity) — Indian/Hindu cultural practice, Agriculture-labeled but not agricultural | IO |
| D30 | Punjabi | Ex.21 | option3 | "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ... ਸੇਵਰ" | Location of National Mustard Research Centre — Indian agricultural institution trivia | IC, IO |
| D31 | Bengali | Ex.4 | option2 | "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" (is_translated: True) | Shell-type constant current transformer — engineering question, machine-translated from English | IF |
| D32 | English | Ex.20 | option2 | "Flower colours of red, pink, blue and purple come mainly from pigments called... Anthocyanins" | Plant pigment biology question — generic botany | IO |
| D33 | Odia | Ex.17 | option1 | "T - Hub ଏକ ତେଲେଙ୍ଗାନା ରାଜ୍ୟ ସରକାରର ପ୍ରୟାସ... ଉଦ୍ୟମିତାକୁ ପ୍ରୋତ୍ସାହନ ଦେବାକୁ ଏକ ପ୍ରଯୁକ୍ତି ଉତ୍ପ୍ରେରଣ କେନ୍ଦ୍ର" | T-Hub Telangana state entrepreneurship tech incubator — Telangana-specific but non-agricultural | IC |
| D34 | Bengali | Ex.6 | option2 | "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" (question body missing the target word) | Antonym question — incomplete stem, illustrates quality issues in translated questions | IF |
| D35 | Bengali | Ex.19 | option1 | "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" (arguments not shown in question field) | Argument evaluation question — missing argument content, shows data quality gap in translated items | IF |
| D36 | English | Ex.11 | option2 | "The owner of the textile shop brought a... Calculator" | Incomplete question stem — no meaningful question context present | IF |
| D37 | Hindi | Ex.13 | option1 | "'মানসून' শব্দের উৎপত্তি কোন ভাষা থেকে?... আরবি ভাষা" (Hindi): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है?... अरबी भाषा" | Origin of word 'monsoon' from Arabic — climate vocabulary trivia, tangentially relevant to agricultural climate | IO |
| D38 | Marathi | Ex.13 | option2 | "प्रांतांमध्ये द्वैधशासन प्रणाली कोणत्या कायद्याने स्थापन केली?... भारत सरकार अधिनियम 1919" | Government of India Act 1919 establishing dyarchy — Indian colonial law | IC, OC |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-script Indic language coverage including Bengali
- **Dimension(s):** IF
- **Observation:** The benchmark successfully delivers text-based MCQ content in Bengali script across all 21 sampled Bengali validation examples, as well as Telugu (25 examples), Hindi, and 8 other Indic scripts. The deployment's primary modality — text-based Indic script queries — is technically supported.
- **Deployment relevance:** The environmental scientist's queries in Bengali and Telugu scripts are at least modality-compatible with the benchmark format. Script-level compatibility ensures that model performance scores on MILU reflect at minimum the correct input encoding for the target scripts.
- **Datapoint citations:**
  - [D3] Bengali Ex.1 (Bengali, validation, option3): `is_translated: True` — Confirms Bengali script is fully populated across all sampled examples, though all are machine-translated.
  - [D31] Bengali Ex.4 (Bengali, validation, option2): "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" — Technical content in Bengali script, confirming script rendering is functional even for translated engineering content.

#### Strength 2: Environmental Sciences and Agriculture subject labels present in multiple languages
- **Dimension(s):** IO
- **Observation:** The "Agriculture" subject appears in the Environmental Sciences domain across at least Bengali (Ex.7), Kannada (Ex.7), Marathi (Ex.7, Ex.21), Punjabi (Ex.7, Ex.21), and Odia (Ex.21). A single Agriculture-labeled question also appears in Bengali. The Environmental Sciences domain contributes Geography, Earth Sciences, and Environmental Science sub-subjects as well.
- **Deployment relevance:** The presence of Agriculture-labeled questions across languages demonstrates that the subject taxonomy does include agricultural content, even if surface-level. For an initial screening of whether a model has any agricultural knowledge, these items provide at least minimal signal.
- **Datapoint citations:**
  - [D10] Bengali Ex.7 (Bengali, validation, option4, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — Only Bengali Agriculture question in sample; concerns soil health but in the context of an Indian national scheme.
  - [D13] Marathi Ex.21 (Marathi, validation, option3, subject=Agriculture): "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" — Agriculture question about location of National Mustard Research Centre.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Agricultural equipment manufacturer in India.

#### Strength 3: Broad domain coverage enabling baseline comparisons across general knowledge areas
- **Dimension(s):** IO, OF
- **Observation:** Across 215 sampled examples, MILU covers Engineering, Science (Physics, Chemistry, Biology, Computer Science, Logical Reasoning), Social Sciences, Arts & Humanities, Law & Governance, Health & Medicine, Business Studies, and Environmental Sciences. This allows a broad model capability baseline.
- **Deployment relevance:** For the scientist's use of both frontier LLMs (GPT-4o, Gemini) and regional small LLMs, MILU's breadth enables diagnosis of whether regional LLMs fail specifically in science/environment or broadly across all domains — a useful comparative signal even if the agricultural domain content is inadequate.
- **Datapoint citations:**
  - [D7] English Ex.10 (English, validation, option4, subject=Environmental Science): "Which of the following are claimed as advantageous in respect of aerobic sludge digestion as compared to anaerobic sludge digestion? (1) Lower BOD concentration in supernatant liquor..." — Technical environmental engineering question, at least adjacent to environmental science professional knowledge.
  - [D22] Hindi Ex.10 (Hindi, validation, option4, subject=Health and Medicine): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है?... नाइट्रेट" — Nitrate-related health question, tangentially relevant to agro-environmental context (nitrate contamination in agricultural water).

#### Strength 4: Consistent MCQ structure enables cross-language and cross-model comparison
- **Dimension(s):** OF
- **Observation:** All sampled examples follow identical 4-option MCQ structure with `target` field, `is_translated` flag, and domain/subject labels. This structural consistency enables controlled comparison across 11 languages and across model families.
- **Deployment relevance:** If the goal includes benchmarking multiple LLMs (frontier + regional) across Bengali and Telugu, MILU's consistent format allows reproducible, comparable evaluation — a practical strength for the meta-analytic purpose of assessing whether regional Indic LLMs perform adequately on science content before deployment in the agricultural query context.
- **Datapoint citations:**
  - [D6] English Ex.5 (English, validation, option1, subject=Geography): "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" — Illustrates clean MCQ structure with unambiguous single-correct answer.
  - [D11] Kannada Ex.7 (Kannada, validation, option4, subject=Agriculture): "ರಾಷ್ಟ್ರೀಯ ಆಹಾರ ಭದ್ರತಾ ಮಿಷನ್ ಒಂದು ಬೆಳೆ ಅಭಿವೃದ್ಧಿ ಯೋಜನೆ" — Same question appears in Bengali, Kannada, Marathi, Malayalam, Punjabi, confirming reliable cross-language structural alignment for identical underlying content.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of Bangladesh-specific agricultural content
- **Dimension(s):** IO, IC
- **Observation:** Across all 215 sampled examples, zero questions address Bangladeshi agro-ecological systems. The Agriculture-labeled items that do appear concern Indian national schemes: the National Food Security Mission (NFSM) and the National Mustard Research Centre, and an Indian agricultural equipment company (Kirloskar). No question in the sample touches haor wetlands, beel fisheries, boro or aman rice cultivation, char-land farming, Brahmaputra-Jamuna floodplain management, or any Bangladeshi agricultural institution. This is consistent with the confirmed structural absence documented in the YAML and web search, and is directly observable in the data.
- **Deployment relevance:** The environmental scientist's primary knowledge domain — Bangladeshi delta agro-ecology — is entirely unrepresented. A model that scores well on MILU Agriculture questions has demonstrated knowledge of Indian food policy schemes, not Bangladeshi farming systems. The benchmark provides no discriminative power for the agricultural science retrieval use case as described.
- **Datapoint citations:**
  - [D10] Bengali Ex.7 (Bengali, validation, option4, domain=Environmental Sciences, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — The only Bengali Agriculture example in the validation sample concerns India's NFSM, not Bangladesh farming.
  - [D13] Marathi Ex.21 (Marathi, validation, option3, subject=Agriculture): "राष्ट्रीय मोहरी संशोधन केंद्र कुठे स्थित आहे... सेवर" — Agriculture question asking for location of Indian Mustard Research Centre in Rajasthan; no agronomic depth, no cross-border relevance.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Agricultural equipment company trivia (Kirloskar); no agro-ecological science content.
  - [D15] Punjabi Ex.7 (Punjabi, validation, option4, subject=Agriculture): "ਰਾਸ਼ਟਰੀ ਖਾਦ ਸੁਰੱਖਿਆ ਮਿਸ਼ਨ ਇੱਕ ਫਸਲ ਵਿਕਾਸ ਯੋਜਨਾ ਹੈ... ਮਿੱਟੀ ਦੀ ਸਿਹਤ ਨੂੰ ਬਹਾਲ ਕਰਨਾ" — Same NFSM policy question replicated in Punjabi; Indian scheme only.

#### CRITICAL Concern 2: Bengali validation sample is 100% machine-translated; no original Bengali-authored questions visible
- **Dimension(s):** IF, IC
- **Observation:** Every one of the 21 Bengali validation examples has `is_translated: True`. This means the Bengali validation set in this sample consists entirely of questions translated from English (presumably Indian English exam content) via GPT-4O. This is consistent with the 25% overall translation rate documented in the paper, but the validation split sampled here shows complete translation saturation. The translated questions adopt standard Bengali script but carry formal translated register, not the naturalistic Bangladeshi Bengali or West Bengal exam register.
- **Deployment relevance:** Bangladeshi Bengali-register competence is a core requirement for the deployment. A benchmark where Bengali performance is assessed entirely on machine-translated questions conflates translation quality with language knowledge. For Mymensingh-dialect users, the register mismatch is compounded: the translation pipeline renders Indian English into what is likely to be a generic, somewhat stilted written Bengali, not the natural phrasing of a Bangladeshi agricultural scientist.
- **Datapoint citations:**
  - [D3] Bengali Ex.1 (Bengali, validation): `is_translated: True` — Confirmed for all 21 sampled Bengali validation examples; no `is_translated: False` observation in this split.
  - [D31] Bengali Ex.4 (Bengali, validation, option2): "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। ... শেল" — Engineering transformer question translated into Bengali; the phrasing is formally correct but exam-register, not naturalistic professional Bengali.
  - [D34] Bengali Ex.6 (Bengali, validation): "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" — Antonym question with the target word missing from the question field entirely; the translated question is incomplete, suggesting translation pipeline quality issues.
  - [D35] Bengali Ex.19 (Bengali, validation): "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" — Argument evaluation question where Arguments I and II are absent from the question field; answer cannot be verified from the question stem alone.

#### CRITICAL Concern 3: Environmental Sciences domain is surface-level general knowledge, not agro-ecological science
- **Dimension(s):** IO, IC
- **Observation:** The Environmental Sciences examples sampled across languages consistently classify geography questions (Mediterranean climate, Radcliffe Line, state populations) and generic earth science questions under this domain, not agro-ecological or soil science content. Agriculture-labeled questions (when they appear) concern Indian policy schemes or corporate trivia, not technical crop science. Across 215 examples, no question addresses: soil types and crop suitability, water management, wetland ecology, irrigation science, delta morphology, or climate change impacts on agriculture.
- **Deployment relevance:** The user explicitly confirmed that MILU's agricultural content is "surface-level." The data confirms this: the Environmental Sciences and Agriculture subject labels in MILU do not map to the technical depth required by a professional environmental scientist. MILU cannot assess whether a model can answer questions about floodplain hydrology, alluvial soil classification, or wetland rice agronomy — the core knowledge domains in the deployment context.
- **Datapoint citations:**
  - [D18] English Ex.5 (English, validation, option1, domain=Environmental Sciences, subject=Geography): "A geographic region has the following distinct characteristics: 1. Warm and dry climate 2. Mild and wet winter 3. Evergreen oak trees" — Mediterranean climate identification; classified as Environmental Sciences but has no agro-ecological depth.
  - [D6] English Ex.5 (same as D18) — Further confirms that "Environmental Sciences" domain encodes geography trivia, not environmental science.
  - [D29] Marathi Ex.16 (Marathi, validation, option3, domain=Arts & Humanities, subject=Arts and Culture): "हलषष्ठी सण का साजरा केला जातो?... मुलाच्या दीर्घायुष्यासाठी" — A festival question classified under Arts & Culture that in a different taxonomy could be agriculture-adjacent (harvest festivals), but demonstrates how culturally specific Indian content dominates even "Environmental Sciences"-adjacent categories.
  - [D9] English Ex.13 (English, validation, option4, domain=Environmental Sciences, subject=Geography): "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" — Welfare policy question classified under Environmental Sciences/Geography; illustrates how the domain-subject taxonomy is applied loosely, and that "Telangana" appears in the sample only in a non-agricultural governance context.

---

#### MAJOR

#### MAJOR Concern 4: Indian-centric ground-truth labels for all governance, law, and policy questions; Bangladesh structurally excluded from answer keys
- **Dimension(s):** OC, OO
- **Observation:** Every governance and law question sampled encodes exclusively Indian constitutional, electoral, and policy knowledge as the ground truth. These include Indian Election Commissioner removal procedure (Bengali Ex.9), the 44th Constitutional Amendment (Hindi Ex.6, Malayalam Ex.6, Tamil Ex.6), Maharashtra state legislature committee rules (English Ex.9, Telugu Ex.9), and Indian state election results (Bengali Ex.5, Punjabi Ex.5). Bangladesh appears in two sampled examples solely as a wrong-answer distractor option (Odia Ex.2, Telugu Ex.2), never as the basis for a correct answer.
- **Deployment relevance:** While the user confirmed that Indian exam answer keys are "generally considered authoritative" for environmental science facts, the governance domain is categorically different. For trans-border agricultural policy questions (river-water allocation, bilateral treaty terms), Indian exam answers encode nationally partial perspectives. The current bilateral volatility (Ganges treaty nearing expiry December 2026, Teesta unresolved) makes this more acute. No such questions exist in the sampled data — confirming the structural absence documented in the YAML.
- **Datapoint citations:**
  - [D5] Bengali Ex.9 (Bengali, validation, option3, domain=Law & Governance, subject=Politics and Governance): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Answer concerns Indian constitutional procedure; Bangladeshi constitutional norms are categorically different.
  - [D8] English Ex.9 (English, validation, option2, domain=Law & Governance): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — Maharashtra-specific state law; no cross-border relevance.
  - [D21] Odia Ex.2 (Odia, validation, option4, domain=Health & Medicine): "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆକୁ ପ୍ରଥମେ ଜଣା ଦେଇଥିବା ଦେଶ କେଉଁଟି?... ଆଫଗାନିସ୍ତାନ; option2: ବାଙ୍ଗ୍ଲାଦେଶ" — Bangladesh listed as a wrong answer; correct answer is Afghanistan. Illustrates Bangladesh's role in this benchmark: a distractor, not a knowledge frame.
  - [D25] Telugu Ex.2 (Telugu, validation, option4): "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది?... option2: బంగ్లాదేశ్" — Bangladesh again used as wrong-answer distractor across languages.

#### MAJOR Concern 5: Agriculture-labeled questions are policy trivia and institutional facts, not agronomic science
- **Dimension(s):** IO, OO
- **Observation:** Every Agriculture-subject question identified in the sample falls into one of three categories: (a) Indian government scheme facts (NFSM launch date, objectives), (b) Indian institutional locations (National Mustard Research Centre at Sever, Rajasthan), or (c) Indian corporate knowledge (Kirloskar as agricultural equipment manufacturer). None address agronomic principles, soil science, crop physiology, pest management, irrigation design, or ecosystem dynamics.
- **Deployment relevance:** An environmental scientist using LLMs to retrieve and reason over agricultural and environmental science knowledge requires models that can demonstrate technical depth — understanding soil types and water retention, rice growth stages and water requirements, integrated crop-fish system management. MILU Agriculture questions test Indian bureaucratic and corporate general-knowledge facts, not agronomic science. A model scoring well on these items provides no assurance about agricultural science competence.
- **Datapoint citations:**
  - [D1] Bengali Ex.7 (Bengali, validation, option4, subject=Agriculture): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প... মাটির স্বাস্থ্য পুনরুদ্ধারের লক্ষ্য রাখে" — Factual recall about Indian scheme objectives; no agronomy.
  - [D30] Punjabi Ex.21 (Punjabi, validation, option3, subject=Agriculture): "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ... ਸੇਵਰ" — Asks the location of India's mustard research centre; pure institutional geography.
  - [D14] Odia Ex.21 (Odia, validation, option4, subject=Agriculture): "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁ ଶିଳ୍ପ ଦୃତଗତିରେ କୃଷି ଉପକରଣ ଉତ୍ପାଦନ କରେ?... ଦ କିର୍ଲୋସ୍କାର" — Corporate brand identification; not agricultural science.

#### MAJOR Concern 6: Telugu sample shows no Telangana/Andhra agro-ecological content; only general Indian exam material
- **Dimension(s):** IO, IC
- **Observation:** The 25 Telugu examples contain no questions about Telangana dry-land cropping, Andhra coastal aquaculture, or sub-regional agro-ecological specifics. Telangana appears once in the sampled data (English Ex.13 and Gujarati Ex.13) only in a social welfare policy context (pension for single women). The Telugu sample covers engineering, health, history, computer science, geography (generic), economics, and materials science — no regionally specific agricultural content is present.
- **Deployment relevance:** The deployment context explicitly targets Telangana dry-land cropping (cotton, sorghum, pigeonpea, red Deccan soils) and Andhra coastal aquaculture (L. vannamei shrimp farming, MPEDA/CAA regulatory framework) as cross-reference agro-ecological zones. MILU Telugu does not assess model knowledge of these sub-regional systems.
- **Datapoint citations:**
  - [D33] Odia Ex.17 (Odia, validation, option1, subject=Business and Management): "T - Hub ଏକ ତେଲେଙ୍ଗାନା ରାଜ୍ୟ ସରକାରର ପ୍ରୟାସ... ଉଦ୍ୟମିତାକୁ ପ୍ରୋତ୍ସାହନ ଦେବାକୁ ଏକ ପ୍ରଯୁକ୍ତି ଉତ୍ପ୍ରେରଣ କେନ୍ଦ୍ର" — T-Hub Telangana tech incubator; Telangana context appears only in tech entrepreneurship, not agriculture.
  - [D9] English Ex.13 (English, validation, option4, domain=Environmental Sciences): "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? ... Telangana" — Telangana surfaces as a welfare policy answer; no agricultural content.
  - [D16] Telugu Ex.25 (Telugu, validation, option1, domain=Environmental Sciences, subject=Geography): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది?... మొరెనా" — Madhya Pradesh industrial centre location; Environmental Sciences domain again populated with geography trivia, not ecological content.

#### MAJOR Concern 7: MCQ format with single correct answer cannot accommodate cross-border knowledge pluralism on contested environmental/policy topics
- **Dimension(s):** OO, OF
- **Observation:** MILU enforces a single-correct-answer MCQ format with a definitive `target` field. The deployment includes scenarios — trans-border river management, water-sharing agreement terms, upstream dam impacts on Bangladeshi agriculture — where the "correct" answer is nationally contested and legitimately differs between Indian and Bangladeshi perspectives. No such questions exist in the current corpus, but the format structurally precludes them.
- **Deployment relevance:** Even if MILU were augmented with trans-border content, the MCQ format would force selection of a single answer key (likely Indian-exam-derived) for questions where Bangladeshi scientists hold different scientifically and politically valid positions. This is a structural output ontology constraint, not merely a coverage gap.
- **Datapoint citations:**
  - [D5] Bengali Ex.9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে... প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Illustrates how Indian constitutional answers are encoded as the single correct response; a parallel Bengali question about Bangladesh's election commission removal would have a categorically different correct answer.
  - [D28] Hindi Ex.6 (Hindi, validation, option1, domain=Law & Governance): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?... 44वें संविधान संशोधन अधिनियम द्वारा" — Indian constitutional amendment as definitive answer; demonstrates how the MCQ single-correct format encodes nationally specific legal facts.

---

#### MINOR

#### MINOR Concern 8: Incomplete question stems visible in translated examples, indicating pipeline quality issues
- **Dimension(s):** IF
- **Observation:** At least two Bengali validation examples have incomplete or truncated question stems: Ex.6 asks for an antonym but the target word is absent; Ex.19 references "Arguments I and II" that are not present in the question field. English Ex.11 ("The owner of the textile shop brought a...") also presents an incomplete sentence with no meaningful context for answering. These truncation artifacts are present in the publicly released dataset.
- **Deployment relevance:** While these are minor quality issues that do not affect the dominant validity concerns, they indicate that the machine-translation and cleaning pipeline introduced some data quality degradation, particularly in Bengali. This slightly undermines confidence in translated Bengali content quality overall.
- **Datapoint citations:**
  - [D34] Bengali Ex.6 (Bengali, validation): "নিচের প্রশ্নে... সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে" — The antonym target word is absent from the question text.
  - [D35] Bengali Ex.19 (Bengali, validation): "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে" — Arguments I and II are referenced but not present in the question field.
  - [D36] English Ex.11 (English, validation, option2): "The owner of the textile shop brought a... Calculator" — Incomplete sentence with no meaningful question context.

#### MINOR Concern 9: Cross-language duplication of identical questions provides inflated coverage illusion
- **Dimension(s):** IO
- **Observation:** The same underlying questions appear across all 11 languages. The National Food Security Mission question (Ex.7 in Bengali, Kannada, Malayalam, Marathi, Punjabi), the cross-assembler definition (Ex.14 across Bengali, English, Kannada, Punjabi, Tamil, Telugu), the Bahmani Kingdom capital (Ex.3 across Bengali, English, Gujarati, Hindi, Malayalam, Punjabi, Tamil), and the Mediterranean climate question appear verbatim across most language configs. These represent translated duplicates of single source items, not independent language-specific questions.
- **Deployment relevance:** The apparent 79,000-question scale of MILU overstates content diversity; the underlying distinct-question count is substantially smaller, and for agricultural content specifically, the number of distinct agronomic questions is very low. A naive count of "Agriculture subject questions" across 11 languages would inflate the perceived agricultural coverage by a factor of up to 11×.
- **Datapoint citations:**
  - [D11] Kannada Ex.7 / [D12] Marathi Ex.7 / [D1] Bengali Ex.7 / [D15] Punjabi Ex.7 — All ask identical NFSM questions in different Indic scripts; same question content replicated across languages.
  - [D19] Bengali Ex.3 / [D27] (implicit in Gujarati, Hindi, Malayalam, Punjabi, Tamil samples) — Bahmani Kingdom capital question identical across multiple language configs.

---

### Content Coverage Summary

The 215 sampled examples span 11 Indic language configs and show a consistent pattern across all of them. Domain distribution in the sample favors Engineering & Technology (frequent), Arts & Humanities (history, language studies, arts/culture), and Business Studies (economics, finance), with Science (physics, chemistry, computer science, logical reasoning) and Social Sciences (sports, sociology) also well-represented. Environmental Sciences appears but is populated almost entirely with geography trivia (climate regions, political boundaries, state-level facts) rather than environmental or agro-ecological science.

The topical content is dominated by Indian competitive exam material: Indian constitutional law, Indian civil service facts, Indian national schemes and institutions, Indian history (medieval and colonial), Indian electoral politics, and Indian corporate/industrial knowledge. All Bengali examples in the validation split are machine-translated from English. South Asian content that appears to be cross-regional (e.g., geographic climate questions, basic physics/engineering) is generic and could have originated from any English-language exam.

Bangladesh appears in the sampled data exclusively as a wrong-answer distractor in two questions (Odia Ex.2, Telugu Ex.2) about Indian Pharmacopoeia recognition. No Bangladeshi agricultural institution, ecological system, land tenure concept, or trans-border water policy appears anywhere in the sample. Telangana and Andhra Pradesh appear only in non-agricultural contexts (tech incubator, welfare pension). The agricultural science vocabulary of the deployment context — haor, beel, boro, aman, char, Farakka, Teesta — has zero representation in the sampled content.

---

### Limitations

1. **Sample is from validation split only.** All 215 examples are drawn from the validation split (~9,000 total questions used for few-shot examples). The test split (~79,000 questions) may have different subject and domain distributions, including potentially more original (non-translated) Bengali questions and more Agriculture/Environmental Sciences content. The 100% translation rate observed in Bengali validation may not hold for the test split.

2. **Sample size per language is small (16–26 examples).** With 16–26 examples per language config, rare subjects (e.g., specific agro-ecological content, if any exists in the test split) would likely not appear in this sample even if present. The absence of Bangladesh-specific content and technical agricultural science in this sample is consistent with structural gaps documented in the YAML, but the sample cannot confirm the exact count of such questions in the full dataset.

3. **Subject distribution within Environmental Sciences is not fully observable.** Table 9 of the MILU paper contains per-subject per-language question counts but was not accessible in this analysis. The sampled data confirms surface-level coverage in Environmental Sciences, but the exact proportion of Agriculture, Environmental Science, Geography, and Earth Sciences sub-subjects in Bengali and Telugu test splits cannot be determined from this sample alone.

4. **Telugu agricultural sub-regional specificity requires corpus-level inspection.** Whether any Telugu test questions address Telangana dry-land cropping or Andhra coastal aquaculture cannot be confirmed or excluded from 25 validation examples. Direct inspection of the Telugu test split subject distribution would be needed.

5. **Machine translation register effects are not directly assessable from this data.** The extent to which GPT-4O translation introduces Indian Bengali register conventions (vs. generic translated register) cannot be assessed from reading translated MCQs alone, as the content of these questions is domain-neutral (engineering, computing, history). Register effects would be most visible in culturally-loaded or dialect-sensitive agricultural terminology, which is absent from the sample.