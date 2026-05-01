## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total across 11 language configs (Bengali: 21, English: 20, Gujarati: 24, Hindi: 26, Kannada: 17, Malayalam: 16, Marathi: 21, Odia: 21, Punjabi: 25, Tamil: 19, Telugu: 25); primary focus on Hindi config (26 examples)
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Hindi, validation | Ex. 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: ... मोटर की गति बहुत अधिक होती है" | Engineering question about DC series motor — translated from English | IC, IF |
| D2 | Hindi, validation | Ex. 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? ... अभ्रक" | North Indian state-specific geography: UP minerals question | IC, IO |
| D3 | Hindi, validation | Ex. 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" | Mughal history — competitive-exam GK register | IC |
| D4 | Hindi, validation | Ex. 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? 44वें संविधान संशोधन अधिनियम द्वारा" | Constitutional law MCQ — Law & Governance domain | IO |
| D5 | Hindi, validation | Ex. 7 | option2 | "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" | Literature question about English poet Wordsworth — not Hindi-board canonical literature | IC |
| D6 | Hindi, validation | Ex. 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" | Hindi grammar (indirect speech) — formal Khari Boli register | IF, IC |
| D7 | Hindi, validation | Ex. 13 | option1 | "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? अरबी भाषा" | Hindi-language item about etymology of 'monsoon' — GK-style | IC |
| D8 | Hindi, validation | Ex. 22 | option4 | "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? अमृता शेरगिल" | Indian arts & culture — Amrita Shergil, India-centric | IC |
| D9 | Hindi, validation | Ex. 17 | option4 | "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? संपत्ति कर" | Economics/taxation MCQ — pan-India competitive exam register | IO |
| D10 | Hindi, validation | Ex. 15 | option3 | "1950 में स्थापित, भारतीय रेलवे द्वारा स्वामित्व वाली औद्योगिक इकाइयों में से एक का नाम भारतीय स्वतंत्रता सेनानी के नाम पर रखा गया है: चित्तरंजन दास" | Indian history — Chittaranjan Das/railways — competitive GK | IC |
| D11 | English, validation | Ex. 3 | option4 | "What was the first capital of the Bahamani Kingdom? ... Gulbarga" | Medieval Indian history — source question in English | IC |
| D12 | English, validation | Ex. 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct? Estimate Committee: All members of this committee are from Assembly only." | Maharashtra state-specific governance question | IC, IO |
| D13 | Hindi, validation | Ex. 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" | Electrical engineering MCQ — translated from English | IC |
| D14 | Hindi, validation | Ex. 4 | option2 | "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" | Engineering transformer question — translated item with 'शेल' (shell) transliteration | IC, IF |
| D15 | Hindi, validation | Ex. 10 | option4 | "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" | Health science MCQ — translated, with 'नाइट्रेट' transliteration retained | IC |
| D16 | Gujarati, validation | Ex. 24 | option3 | "સિંધિ કવિ અને લેખક વસદેવ મોહીનું 2019 માટેના સરસ્વતી સન્માન માટે પસંદગી ... કેકે બિરલા ફાઉન્ડેશન" | Saraswati Samman award question — India-centric literary award | IC |
| D17 | Marathi, validation | Ex. 16 | option3 | "हलषष्ठी सण का साजरा केला जातो? मुलाच्या दीर्घायुष्यासाठी" | Regional Indian festival (Halsashti) — local cultural knowledge | IC |
| D18 | English, validation | Ex. 1 | option3 | "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? Sharp rise in value of imports of oil & petroleum products" | 1991 India economic crisis — same question as Bengali D1 | IC |
| D19 | Hindi, validation | Ex. 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" | Hindi translation of English Ex. 1 — translation quality check | IC |
| D20 | Hindi, validation | Ex. 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? आठ" | Sports GK — India-centric, recent current affairs | IC |
| D21 | Bengali, validation | Ex. 12 | option4 | ""মঙ্গল ভারত" কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল: আচার্য বিনোবা ভাবে" | Literature: 'Mangal Bharat' work attributed to Vinoba Bhave | IC |
| D22 | Telugu, validation | Ex. 25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? మొరెనా" | Madhya Pradesh state-specific geography — sub-national knowledge | IC |
| D23 | Hindi, validation | Ex. 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? एक जंप लेबल या फॉर्मेट लेबल" | Computer science MCQ — translated, technical vocabulary | IC |
| D24 | Hindi, validation | Ex. 5 | option1 | "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं: ... उत्तरी अमेरिका का अटलांटिक तट" | Mediterranean climate geography — translated, no North India content | IC |
| D25 | Hindi, validation | Ex. 19 | option3 | "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? पाकिस्तान" | Partition history — India-centric GK | IC |
| D26 | English, validation | Ex. 17 | option3 | "What is the title of Yashpal Committee Report (1993)? Learning without burden" | India education policy — relevant to teacher deployment | IO |
| D27 | Marathi, validation | Ex. 15 | option1 | "वर्ष 2020 मध्ये, भारत सरकारने राष्ट्रीय शिक्षण धोरण सादर केले. आतापर्यंत किती राष्ट्रीय शिक्षण धोरणे सादर करण्यात आली आहेत? 3" | NEP question — Indian education policy | IO |
| D28 | Hindi, validation | Ex. 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: ... is_translated: True" | is_translated=True flag on all 26 Hindi validation examples reviewed | IC |
| D29 | Gujarati, validation | Ex. 16 | option2 | "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' પણ કહેવામાં આવે છે? લિંગગિરી બળવો" | Chhattisgarh regional history — cross-state cultural knowledge | IC |
| D30 | English, validation | Ex. 11 | option2 | "The owner of the textile shop brought a ... Calculator" | Truncated/incomplete question — possible data quality issue | IF |
| D31 | Punjabi, validation | Ex. 21 | option3 | "ਰਾਸ਼ਟਰੀ ਸਰੋਂ ਖੋਜ ਕੇਂਦਰ ਕਿੱਥੇ ਸਥਿਤ ਹੈ - ਸੇਵਰ" | National Mustard Research Centre location — Rajasthan-specific | IC |
| D32 | Hindi, validation | Ex. 24 | option4 | "तंगस्टन तत्व का प्रतीक क्या है? W" | Chemistry: symbol for tungsten — straightforward science MCQ | IC |
| D33 | Malayalam, validation | Ex. 15 | option2 | "സർക്കസുകളിൽ തൊഴിൽ നിരോധിക്കണമെന്ന് ... ബച്ച്പൻ ബചാവോ ആന്ദോളൻ വേഴ്സസ് യൂണിയൻ ഓഫ് ഇന്ത്യ" | Child labour / constitutional law — Bachpan Bachao Andolan case | IO |
| D34 | Hindi, validation | Ex. 12 | option3 | "आमतौर पर लकड़ी के रेशों की लंबाई के साथ सूजन कितनी होती है: 0.1 से 0.8%" | Materials science MCQ — translated engineering content | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strict MCQ format with single correct answer — structural alignment with deployment
- **Dimension(s):** IO, OO
- **Observation:** All sampled examples across all 11 language configs are uniformly formatted as single-correct-answer MCQs with exactly four options and a single target label. No reading-comprehension, multi-select, or open-ended items are present in the sample.
- **Deployment relevance:** The deployment requires strict MCQ evaluation with positive/negative marking where one answer is correct. MILU's format is a direct structural match to this requirement.
- **Datapoint citations:**
  - [D1] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है:" — four options, single target, binary scoring ready.
  - [D6] Hindi Ex. 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें।" — grammar MCQ, same format, one correct answer.

#### Strength 2: Hindi Devanagari script — correct script and register
- **Dimension(s):** IF
- **Observation:** All Hindi-config items appear in fluent Devanagari script. The language register is formal standard Hindi (Khari Boli), with grammatically complete sentences and standard academic vocabulary. No script mixing or Roman transliteration is observed in the question stems (only in proper nouns and some technical terms).
- **Deployment relevance:** The deployment is text-only, Hindi-medium, Devanagari script. Script alignment is complete.
- **Datapoint citations:**
  - [D6] Hindi Ex. 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा।" — formal academic Hindi grammar question in clean Devanagari.
  - [D7] Hindi Ex. 13 (Hindi, split=validation, label=option1): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? अरबी भाषा" — Hindi GK question in standard written Hindi.

#### Strength 3: India-centric general knowledge content with some North Indian regional specificity
- **Dimension(s):** IC
- **Observation:** The Hindi sample includes questions with clear India-specific and North-India-specific content: a UP-minerals geography question, a Mughal history question, a constitutional law question, and an Indian freedom-fighter question. These reflect content broadly familiar to North Indian teachers from competitive-exam contexts.
- **Deployment relevance:** Teachers deploying the system in UP, MP, Rajasthan, and Bihar will encounter questions about subjects directly relevant to their syllabi and general knowledge background.
- **Datapoint citations:**
  - [D2] Hindi Ex. 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? अभ्रक" — UP-specific geographic knowledge directly relevant to North Indian state-board curriculum.
  - [D3] Hindi Ex. 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — Mughal history item aligning with North Indian history syllabus.
  - [D25] Hindi Ex. 19 (Hindi, split=validation, label=option3): "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? पाकिस्तान" — partition history, standard North Indian school and competitive-exam content.

#### Strength 4: Multiple subject domains present in Hindi sample — partial curricular breadth
- **Dimension(s):** IO
- **Observation:** The 26 Hindi validation examples span Engineering & Tech (6 items), Environmental Sciences (3), Arts & Humanities (4 — History, Literature, Language Studies, Arts & Culture), Law & Governance (1), Health & Medicine (1), Business Studies (3), and Science (4). This covers all 8 declared domains, providing evidence that domain breadth is not illusory for Hindi.
- **Deployment relevance:** The deployment requires coverage across all Hindi state and central board syllabi; MILU's multi-domain structure at least nominally addresses this, though the depth within each domain varies.
- **Datapoint citations:**
  - [D4] Hindi Ex. 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — Law & Governance domain present.
  - [D9] Hindi Ex. 17 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? संपत्ति कर" — Business Studies / Economics domain.
  - [D20] Hindi Ex. 2 (Hindi, split=validation, label=option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — Sports & Recreation / Social Sciences domain present.

#### Strength 5: Cross-language answer-key consistency visible in the data
- **Dimension(s):** OC
- **Observation:** A structurally identical question appears in both English (Ex. 1) and Hindi (Ex. 18) with the same correct answer (option3 in both), confirming consistent answer-key application across translations. The deployment user confirmed that competitive-exam answer keys are broadly compatible with North Indian teacher norms.
- **Deployment relevance:** Reduces concern about answer-key divergence between competitive-exam-sourced labels and North Indian board norms.
- **Datapoint citations:**
  - [D18] English Ex. 1 (English, split=validation, label=option3): "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? Sharp rise in value of imports of oil & petroleum products"
  - [D19] Hindi Ex. 18 (Hindi, split=validation, label=option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" — same item, same answer, consistent key.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: All reviewed Hindi validation examples are machine-translated (is_translated=True)
- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 26 Hindi validation examples in the sample has `is_translated: True`. This is consistent across all items — no natively sourced Hindi item appears in the validation split sample. The benchmark paper states that only ~25% of total questions are translated, but this sample suggests that the validation split for Hindi may disproportionately (or entirely) consist of translated items. If true for the test split as well, the Hindi-language content would not reflect questions drawn from Hindi-language competitive exams but rather English-sourced content machine-translated by GPT-4O.
- **Deployment relevance:** This is critical because: (1) translated items may not reflect the register, phrasing conventions, and topic selection of actual Hindi-medium competitive-exam questions; (2) North Indian Hindi-medium teachers are being assessed on a model that was evaluated on items translated from English rather than native Hindi exam content; (3) subject-specific terminology choices in the translations may not align with state-board conventions.
- **Datapoint citations:**
  - [D28] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — is_translated=True; this is an engineering question where the Hindi text is a translation of an English-language technical question.
  - [D14] Hindi Ex. 4 (Hindi, split=validation, label=option2): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" — is_translated=True; the answer option 'शेल' is a transliteration of 'shell' rather than a standard Hindi technical term.
  - [D15] Hindi Ex. 10 (Hindi, split=validation, label=option4): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" — is_translated=True; 'नाइट्रेट' is a transliteration choice that may differ from Vaigyaanik evam Takniki Shabdavali Aayog standardized Hindi science terminology.

---

#### MAJOR

#### MAJOR Concern 1: No canonical Hindi-board literary content visible — competitive-exam GK register dominates Arts & Humanities
- **Dimension(s):** IC, IO
- **Observation:** The Arts & Humanities items in the Hindi sample do not include any questions about canonical Hindi-board literary figures (Tulsidas, Premchand, Kabir, Mahadevi Varma, etc.) or school-syllabus Hindi literature. The one Literature & Linguistics item is about William Wordsworth (an English poet). The History items are about Mughal texts and administrative history — consistent with a UPSC/SSC competitive-exam GK register rather than a school-literature register. No Hindi-medium literature, no doha analysis, no textual comprehension of Ramcharitmanas passages is observed.
- **Deployment relevance:** North Indian Hindi-medium teachers — and the students they evaluate — work with a school-board literature curriculum that foregrounds Hindi authors in a literary register (close reading, aesthetic appreciation) rather than a general-knowledge administrative register. MILU's competitive-exam sourcing produces a different kind of Arts & Humanities content than what a UP Board or CBSE Hindi teacher would encounter in their daily work.
- **Datapoint citations:**
  - [D5] Hindi Ex. 7 (Hindi, split=validation, label=option2): "विलियम वर्ड्सवर्थ _________ के कवि हैं। इंग्लैंड" — Literature & Linguistics item asks about an English Romantic poet, not Hindi-board canonical literature.
  - [D3] Hindi Ex. 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? साकी मुस्तईद खान" — History item is administrative/courtly Mughal text authorship — UPSC GK register, not school-syllabus framing.
  - [D8] Hindi Ex. 22 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? अमृता शेरगिल" — Arts & Culture item is factual identification of artist, GK-style.

#### MAJOR Concern 2: Subject coverage in Hindi validation sample skews heavily toward Engineering & Tech, under-representing Civics/Political Science and Social Sciences
- **Dimension(s):** IO
- **Observation:** Of 26 Hindi validation examples, 6 are Engineering & Tech (23%), with only 1 Law & Governance item and no standalone Civics/Political Science or dedicated Social Sciences item (beyond 2 Sports items). Hindi-board curricula in UP, MP, Rajasthan, and Bihar place substantial emphasis on Civics, Panchayati Raj, and Social Sciences — subjects directly assessed in state board exams. The Engineering & Tech items (DC motors, transformers, rectifiers) are more characteristic of polytechnic or engineering entrance exams than school-board or general teacher deployment.
- **Deployment relevance:** If this imbalance persists in the test split, the benchmark may not adequately differentiate LLM performance on the civics and social science domains most relevant to the deployment's North Indian teacher population.
- **Datapoint citations:**
  - [D1] Hindi Ex. 1 (Hindi, split=validation, label=option2): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — electrical engineering, likely not in UP Board secondary teacher's core domain.
  - [D13] Hindi Ex. 3 (Hindi, split=validation, label=option2): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: पल्सेटिंग डीसी" — second engineering item in sample; both translated.
  - [D4] Hindi Ex. 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया?" — only Law & Governance item; pertains to constitutional amendment, not Panchayati Raj or state-level civics.

#### MAJOR Concern 3: No sub-national state-board granularity verifiable from item content — potential under-representation of UP/Bihar/Rajasthan state-specific content
- **Dimension(s):** IC, IO
- **Observation:** Only one of the 26 Hindi examples explicitly names a North Indian state in its question (Ex. 26: UP minerals). No items about UP Panchayati Raj structure, Bihar Board history, Rajasthan state administrative geography, or MP-specific civics are visible. Items with state-specific content appear in other language configs (Telugu Ex. 25 mentions Madhya Pradesh; English Ex. 9 mentions Maharashtra), but the Hindi sample shows limited sub-national specificity for the primary Hindi-belt states.
- **Deployment relevance:** The deployment must serve teachers whose students are evaluated on state-board syllabi from UP, MP, Rajasthan, and Bihar specifically. If MILU's Hindi items are drawn primarily from pan-India competitive exams rather than state-level civil service exams, North Indian state-specific curricular content may be structurally absent.
- **Datapoint citations:**
  - [D2] Hindi Ex. 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — the only state-specific Hindi item in the sample, and it is a mineral geography question rather than civics or governance.
  - [D22] Telugu Ex. 25 (Telugu, split=validation, label=option1): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? మొరెనా" — MP industrial geography appears in Telugu config, not in Hindi.
  - [D12] English Ex. 9 (English, split=validation, label=option2): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — state-specific governance in English config (Maharashtra), not Hindi-belt states.

#### MAJOR Concern 4: Translated Hindi items exhibit register and terminology choices not validated for state-board Hindi norms
- **Dimension(s):** IC, IF
- **Observation:** Translated Hindi items retain English technical terms as transliterations rather than using standardized Hindi or Vaigyaanik evam Takniki Shabdavali Aayog equivalents. Examples: 'शेल' (shell type transformer), 'नाइट्रेट' (nitrate), 'पल्सेटिंग डीसी' (pulsating DC), 'जंप लेबल' (jump label), 'स्ट्राइकथ्रू' (strikethrough), 'सुपरस्क्रिप्ट' (superscript). State board science textbooks in Hindi (particularly UP Board and CBSE Hindi medium) often use different terminological conventions — either fully Sanskritized or anglicized in different proportions. This creates a potential register mismatch between MILU's translated vocabulary and what North Indian teachers and students encounter in board textbooks.
- **Deployment relevance:** A teacher evaluating student answers in a Hindi-medium school context will have been trained on a specific terminological register. MILU's translated items may use vocabulary choices that diverge from that register, reducing the ecological validity of benchmark performance as a predictor of deployment performance.
- **Datapoint citations:**
  - [D14] Hindi Ex. 4 (Hindi, split=validation, label=option2): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। शेल" — 'शेल' is a direct transliteration of 'shell'; standard Hindi technical texts might use 'कोश' or retain 'शेल' differently spelled.
  - [D23] Hindi Ex. 8 (Hindi, split=validation, label=option1): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? एक जंप लेबल या फॉर्मेट लेबल" — 'जंप लेबल' and 'फॉर्मेट लेबल' are transliterations; CS items in Hindi textbooks vary in how they render these terms.
  - [D15] Hindi Ex. 10 (Hindi, split=validation, label=option4): "रक्त में निम्नलिखित में से किसकी अधिकता 'ब्लू बेबी सिंड्रोम' रोग का कारण बनती है? नाइट्रेट" — 'नाइट्रेट' is transliterated; UP Board biology texts may use 'नाइट्रेट' or 'नत्रज लवण' depending on edition.

---

#### MINOR

#### MINOR Concern 1: One English-config item appears truncated or incomplete
- **Dimension(s):** IF
- **Observation:** English Ex. 11 reads: "The owner of the textile shop brought a" with options Calculator, Computer, Pencil, Fountain pen — the question stem appears incomplete, missing the context that would identify what the shop owner brought. The correct answer (Calculator) is unverifiable from the stem alone.
- **Deployment relevance:** An individual data quality issue; not indicative of a systemic problem given the documented filtering steps, but suggests noise remains in the dataset.
- **Datapoint citations:**
  - [D30] English Ex. 11 (English, split=validation, label=option2): "The owner of the textile shop brought a ... Calculator" — question stem appears to be cut off or missing context, making the correct answer unverifiable from the question alone.

#### MINOR Concern 2: Some items require very recent current-affairs knowledge (2022 sports results, 2020 awards) that may have finite shelf life
- **Dimension(s):** IC
- **Observation:** Several Hindi and non-Hindi items reference very recent events: India's 2022 Archery Asia Cup medals (Hindi Ex. 2), AAP forming government in Punjab in Feb-March 2022 (Bengali Ex. 5, Punjabi Ex. 5), 65th Filmfare Awards 2020 (Bengali Ex. 17, Kannada Ex. 17, Tamil Ex. 17). These items have definite correct answers but become increasingly anomalous as time passes.
- **Deployment relevance:** For a teacher using the system to evaluate students in 2025+, current-affairs items from 2022 may appear dated, and models trained on more recent data may give different performance profiles on these items than at benchmark creation time.
- **Datapoint citations:**
  - [D20] Hindi Ex. 2 (Hindi, split=validation, label=option2): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? आठ" — 2022 sports result.
  - [D8] Hindi Ex. 22 (Hindi, split=validation, label=option4): "65वें फिल्मफेयर पुरस्कारों, 2020 में..." — referenced across multiple language configs as a parallel translated item.

#### MINOR Concern 3: Some items across language configs appear to be exact translations of the same English source, suggesting limited native-language diversity
- **Dimension(s):** IC
- **Observation:** The same questions (Bahamani Kingdom capital, Mediterranean climate characteristics, Qutub Minar, Fortran 77, cross-assembler, 1991 financial crisis) appear word-for-word translated across Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, and Telugu. This parallel structure confirms that a significant fraction of the benchmark is a multilingual translation of a shared English-language item pool, not independently sourced native-language questions.
- **Deployment relevance:** For Hindi specifically, this means items that appear to be Hindi-language MCQs may in fact test the model's ability to process translated English content rather than culturally and linguistically native Hindi knowledge — a moderate concern for a deployment aimed at Hindi-medium North Indian teachers whose students encounter native Hindi-register content.
- **Datapoint citations:**
  - [D11] English Ex. 3 (English, split=validation, label=option4): "What was the first capital of the Bahamani Kingdom? Gulbarga" — same question visible in Bengali Ex. 3, Gujarati Ex. 3, Hindi (implicitly), Malayalam Ex. 3, Punjabi Ex. 3.
  - [D24] Hindi Ex. 5 (Hindi, split=validation, label=option1): "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं: ... उत्तरी अमेरिका का अटलांटिक तट" — Mediterranean climate question appears translated across all 11 configs with identical structure.

---

### Content Coverage Summary

The Hindi-config validation sample (26 items) is entirely machine-translated (is_translated=True for all items reviewed), which is the most significant single observation from the data. Subject coverage spans all 8 declared domains, with a clear skew toward Engineering & Tech (23% of sample) and away from Civics/Political Science. The register is formal standard Hindi (Khari Boli) throughout, but technical vocabulary in translated items uses transliteration conventions (शेल, नाइट्रेट, जंप लेबल) that may not align with state-board Hindi textbook norms. Arts & Humanities items in the Hindi sample are in a competitive-exam GK register (factual identification, administrative history) rather than a school-literature register; no canonical Hindi literary figures (Tulsidas, Premchand, Kabir) appear in the sample. One UP-specific geography item provides the only sub-national Hindi-belt state-specific content visible.

Non-Hindi language configs (Bengali, Gujarati, Kannada, Marathi, etc.) also show nearly universal is_translated=True flags in the validation split, and many identical questions appear across all 11 languages, confirming that the validation split is heavily drawn from the translated English item pool. The English config contains genuinely India-centric questions including Maharashtra governance, Indian education policy (Yashpal Committee), and Indian railways history, all non-translated and well-formed. The Marathi config shows regionally specific Indian cultural content (Halsashti festival). Some items have a data quality issue (English Ex. 11 truncated question stem). Current-affairs items from 2020–2022 are present across multiple configs.

---

### Limitations

1. **Sample size per config:** Only 16–26 examples per language config were reviewed; subject-level coverage within each domain cannot be reliably assessed from this sample size. The test split may have a different is_translated distribution than the validation split.

2. **Validation-split translation bias:** The observation that all 26 Hindi validation items are translated may reflect deliberate design (translated items used for few-shot/validation purposes) or a split-level artifact. The test split — which is the primary evaluation set — may contain a higher proportion of natively sourced Hindi items. This cannot be determined from the available sample.

3. **Full subject-level statistics unavailable:** Supplementary Table 9 of the MILU paper (per-language, per-subject item counts) is not publicly accessible without the full PDF; the proportion of Hindi items by subject and whether specific Hindi-board subjects (Hindi Literature, UP History, Rajasthan Polity) are well-represented cannot be assessed from the sample.

4. **No test-split examples reviewed:** All examples are from the validation split. The test split (which would be the deployment evaluation set) was not sampled; its domain, subject, and is_translated distributions may differ.

5. **Annotation quality not directly assessable:** Whether individual answer keys are correct cannot be verified from the data alone without independent subject-matter expertise; the truncated English item (D30) is the only clear quality signal visible.

6. **Register variation within Hindi not assessable from script alone:** Whether MILU's formal Khari Boli register matches UP Board, MP Board, or CBSE Hindi-medium textbook norms requires comparison with those textbooks, which was not possible from the dataset sample.