## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (configs: Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-08-01
**Examples reviewed:** 215 total (21 Bengali, 20 English, 24 Gujarati, 26 Hindi, 17 Kannada, 16 Malayalam, 21 Marathi, 21 Odia, 25 Punjabi, 19 Tamil, 25 Telugu) — all from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Hindi, validation | 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" | Polity/Constitution question in Hindi, about 44th Constitutional Amendment — UPSC core topic | IC, IO |
| D2 | Hindi, validation | 25 | option1 | "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? … साकी मुस्तईद खान" | Mughal-period history question in Hindi — directly relevant to North India medieval history | IC, IO |
| D3 | Hindi, validation | 26 | option2 | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? … अभ्रक" | State-specific GK question about Uttar Pradesh minerals — North India sub-regional content | IC, IO |
| D4 | Hindi, validation | 2 | option2 | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते? … आठ" | Current Affairs question (2022) about archery medal count — time-bounded, may be stale | IC, IO |
| D5 | Hindi, validation | 1 | option2 | "जब एक डीसी सीरीज मोटर बिना लोड के चलती है: … मोटर की गति बहुत अधिक होती है" | Engineering/Physics question in Hindi, `is_translated: True` — not in UPSC/SSC core syllabus | IC, IO |
| D6 | Hindi, validation | 3 | option2 | "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है: … पल्सेटिंग डीसी" | Technical engineering question in Hindi, `is_translated: True` — domain not central to UPSC/SSC GS | IC, IO |
| D7 | Hindi, validation | 4 | option2 | "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है। … शेल" | Electrical engineering, translated — technical domain not prioritized for Hindi-medium UPSC prep | IO |
| D8 | English, validation | 6 | option3 | "Fill in the gap below with suitable word. Fruit ∶ Reap∶∶ Flower ∶ _____… Bloom" | Logical Reasoning/analogy question in English — confirms presence of reasoning subject | IO |
| D9 | English, validation | 7 | option2 | "If Rs. 4000 becomes Rs. 5760 in 2 years at compound interest … what is the annual rate of interest? … 20 percent" | Mathematics/Quantitative Aptitude question (compound interest) — confirms presence in English partition | IO |
| D10 | Hindi, validation | 17 | option4 | "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? … संपत्ति कर" | Economics/direct tax question in Hindi — Economics is relevant to GK syllabus | IC |
| D11 | Hindi, validation | 13 | option1 | "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? … अरबी भाषा" | General Knowledge question in Hindi (monsoon etymology) — accessible, pan-India GK | IC |
| D12 | Hindi, validation | 19 | option3 | "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? … पाकिस्तान" | Geography GK question in Hindi — relevant to UPSC/SSC syllabus, Devanagari script, no English terms | IC, IF |
| D13 | Hindi (all examples) | all 26 | — | All 26 Hindi examples: is_translated = True | Every Hindi validation example in the sample is machine-translated from English | IC |
| D14 | English, validation | 1 | option3 | "What was the immediate cause for loss of foreign reserves triggering the financial crisis in 1991? … Sharp rise in value of imports of oil & petroleum products" | English original; same question appears in Hindi (D15) and Bengali — confirms translation pipeline | IC |
| D15 | Hindi, validation | 18 | option3 | "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था? … तेल और पेट्रोलियम उत्पादों के आयात के मूल्य में तीव्र वृद्धि" | Hindi translation of D14 — fluent Hindi, but `is_translated: True`, confirms translation pipeline | IC |
| D16 | Hindi, validation | 8 | option1 | "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है? … एक जंप लेबल या फॉर्मेट लेबल" | Computer Science / Fortran programming question in Hindi — very niche for UPSC/SSC aspirants | IO |
| D17 | Hindi, validation | 9 | option3 | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा। … प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" | Hindi Language Studies question (indirect speech) — tests Hindi grammar directly | IC, IF |
| D18 | Hindi, validation | 22 | option4 | "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? … अमृता शेरगिल" | Arts & Culture GK in Hindi — pan-India Indian art figure | IC |
| D19 | Marathi, validation | 16 | option3 | "हलषष्ठी सण का साजरा केला जातो? … मुलाच्या दीर्घायुष्यासाठी" | Regional festival question in Marathi — culturally specific, regional content (not Hindi/North India) | IC |
| D20 | Gujarati, validation | 16 | option2 | "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' પણ કહેવામાં આવે છે? … લિંગગિરી બળવો" | Chhattisgarh tribal revolt question — regional Indian history, culturally grounded | IC |
| D21 | Hindi, validation | 5 | option1 | "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं … सदाबहार ओक के पेड़ … भूमध्यसागरीय" | Geography question (Mediterranean climate) — translated, pan-India geography, no English code-mixing | IC, IF |
| D22 | English, validation | 3 | option4 | "What was the first capital of the Bahamani Kingdom? … Gulbarga" | India-specific historical knowledge (Deccan Sultanate) — same question appears across all languages | OC |
| D23 | Hindi, validation | 15 | option3 | "1950 में स्थापित, भारतीय रेलवे द्वारा स्वामित्व वाली औद्योगिक इकाइयों में से एक का नाम भारतीय स्वतंत्रता सेनानी के नाम पर रखा गया है: … चित्तरंजन दास" | Indian history/GK — freedom fighter named railway unit; is_translated: True | IC |
| D24 | English, validation | 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct? … Estimate Committee: All members of this committee are from Assembly only." | State-level (Maharashtra) governance question in English partition — not central exam scope | IO |
| D25 | Punjabi, validation | 5 | option4 | "ਫਰਵਰੀ - ਮਾਰਚ 2022 ਵਿੱਚ ਹੋਈ ਰਾਜ ਵਿਧਾਨਸਭਾ ਚੋਣਾਂ ਵਿੱਚ, ਆਮ ਆਦਮੀ ਪਾਰਟੀ (AAP) ਨੇ … ਪੰਜਾਬ" | Current Affairs (2022 state elections) in Punjabi — politically specific, time-bounded | IC |
| D26 | Hindi, validation | 20 | option3 | "नेत्रगोलक लगभग गोलाकार होता है जिसकी व्यास लगभग कितनी होती है? … 2.3 सेमी" | Biology/Science question in Hindi — `is_translated: True`, basic science fact | IO |
| D27 | Telugu, validation | 25 | option1 | "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? … మొరెనా" | State-level GK (Madhya Pradesh industrial geography) in Telugu — regional, not central exam | IO |
| D28 | Hindi, validation | 24 | option4 | "तंगस्टन तत्व का प्रतीक क्या है? … W" | Chemistry/Science fact question in Hindi, `is_translated: True` — basic science, not UPSC priority | IO |
| D29 | Malayalam, validation | 6 | option1 | "ദേശീയ അടിയന്തരാവസ്ഥ പ്രഖ്യാപിക്കാൻ 'സായുധ കലാപം' എന്ന പദം ഭരണഘടനയിൽ ചേർത്തത് എപ്പോൾ? … 44-ാമത് ഭരണഘടനാ ഭേദഗതി നിയമം വഴി" | Same Constitutional Amendment question appears in Hindi (D1), Tamil, and Malayalam — cross-language duplication | IC, OC |
| D30 | Marathi, validation | 13 | option2 | "प्रांतांमध्ये द्वैधशासन प्रणाली कोणत्या कायद्याने स्थापन केली? … भारत सरकार अधिनियम 1919" | Indian constitutional history question (dyarchy) — India-specific, historically grounded | IC |
| D31 | English, validation | 15 | option3 | "Founded in 1950, one of the industrial units owned by Indian Railways is named after the Indian freedom fighter: … Chittaranjan Das" | India-specific GK, English original — Chittaranjan Das is a pan-India figure relevant to GK | IC |
| D32 | Hindi, validation | 11 | option2 | "संदीप माइकल निम्नलिखित में से किस खेल से जुड़े थे? … हॉकी" | Sports GK in Hindi — niche figure, is_translated: True | IC |
| D33 | Bengali, validation | 5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) … পাঞ্জাব" | 2022 state elections Current Affairs — AAP, UP, Goa all named; time-bounded content | IC |
| D34 | English, validation | 11 | option2 | "The owner of the textile shop brought a … Calculator" | Incomplete stem — "brought a" with no further context; question appears malformed | IC, OC |
| D35 | Malayalam, validation | 14 | option4 | "ദിശകൾ: മാർബിൾ ഉപയോഗിക്കാവുന്നത് … ശിൽപ്പം" | Incomplete stem ("Directions: marble can be used") — same truncated structure appears across languages | IC, OC |
| D36 | Hindi, validation | 16 | — | "एएम की बैंडविड्थ _________ है। … 1110 kHz" | AM bandwidth engineering question — highly technical, `is_translated: True`; unlikely in UPSC GS | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Core UPSC/SSC Polity and Constitutional Law Coverage in Hindi
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition includes substantive questions on Indian constitutional law — specifically the 44th Constitutional Amendment (adding 'armed rebellion' for national emergency declaration) and other governance questions. These directly address the high-priority UPSC/SSC subject of Indian Polity & Constitution.
- **Deployment relevance:** For central exam aspirants, constitutional amendment questions are among the most tested areas in UPSC GS Paper 2 and SSC General Awareness. The Hindi rendering is clear and uses correct Devanagari terminology without excessive code-mixing.
- **Datapoint citations:**
  - [D1] Example 6 (Hindi, split=validation, label=option1): "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" — UPSC-relevant Polity question in fluent Devanagari, no significant English intrusion.

#### Strength 2: Mughal and North Indian Medieval History Coverage
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition contains Mughal-period history questions (e.g., the authorship of 'Masir-e-Alamgiri') and pan-India medieval history questions (e.g., who completed the Qutb Minar). These are directly in scope for UPSC GS Paper 1 Indian history, with emphasis on the Delhi Sultanate and Mughal era that is especially prominent in North Indian exam preparation.
- **Deployment relevance:** Mughal administrative history and North Indian medieval landmarks are high-frequency topics in both UPSC and SSC GK sections. The Qutb Minar question also appears consistently across all language partitions, confirming it as a pan-India GK anchor.
- **Datapoint citations:**
  - [D2] Example 25 (Hindi, split=validation, label=option1): "मुगल ग्रंथ 'मासिर-ए-आलमगीरी' के रचयिता कौन हैं? … साकी मुस्तईद खान" — Mughal literary history, directly relevant to UPSC GS1.
  - [D22] Example 3 (English, split=validation, label=option4): "What was the first capital of the Bahamani Kingdom? … Gulbarga" — pan-India medieval history, same question appearing in all language partitions.

#### Strength 3: North India–Specific Regional GK Present in Hindi Partition
- **Dimension(s):** IC, IO
- **Observation:** The Hindi sample contains at least one question specifically about Uttar Pradesh's mineral resources, addressing sub-regional content within a central-exam framing. This is the type of India-within-India regional knowledge that the deployment requires the AI to handle.
- **Deployment relevance:** Central exams (UPSC, SSC) occasionally test state-specific geography and resource questions. The presence of a UP-specific item in the Hindi partition confirms that MILU does include some North India sub-regional content, partially addressing the documented gap.
- **Datapoint citations:**
  - [D3] Example 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है? … अभ्रक" — UP state GK question in Hindi; directly serves the North India sub-regional layer.

#### Strength 4: Hindi Script Fidelity and Low Code-Mixing in Observed Examples
- **Dimension(s):** IF, IC
- **Observation:** Across all 26 Hindi examples examined, the questions and answer options are written in standard Devanagari. Technical terms are rendered in Hindi transliterations (e.g., "पल्सेटिंग डीसी" for "pulsating DC," "ट्रांसफार्मर" for transformer) or Hindi equivalents. Roman script or English-medium phrasing is minimal — the observed Hindi items do not appear to exceed the deployment's ~10% code-mixing ceiling.
- **Deployment relevance:** The target student population can read standard Devanagari Hindi; the absence of heavy Roman-script intrusion in the observed sample is a positive signal for accessibility.
- **Datapoint citations:**
  - [D12] Example 19 (Hindi, split=validation, label=option3): "रेडक्लिफ रेखा भारत की सीमाओं को निम्नलिखित में से किस देश के साथ विभाजित करती है? … पाकिस्तान" — Pure Devanagari, no English terms.
  - [D21] Example 5 (Hindi, split=validation, label=option1): "एक भौगोलिक क्षेत्र में निम्नलिखित विशिष्ट विशेषताएँ हैं … सदाबहार ओक के पेड़ … भूमध्यसागरीय" — "ओक" (oak) is retained as a transliterated loanword; "भूमध्यसागरीय" (Mediterranean) is a full Sanskrit-Hindi rendering — appropriate register.

#### Strength 5: Breadth of India-Centric General Knowledge Subjects
- **Dimension(s):** IO, IC
- **Observation:** Across the Hindi and English partitions, the sample contains questions spanning Economics (direct tax, 1991 financial crisis), Geography (Radcliffe Line, Mediterranean climate), Biology (eyeball diameter, Blue Baby Syndrome), Arts & Culture (Amrita Shergil), and History — consistent with the multi-domain pan-India GK coverage required for UPSC and SSC.
- **Deployment relevance:** The multi-domain spread matches the general awareness section tested across all central exams, confirming that the benchmark does not over-index on a single domain.
- **Datapoint citations:**
  - [D10] Example 17 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन प्रत्यक्ष कर का उदाहरण है? … संपत्ति कर" — Economics GK in Hindi, UPSC/SSC relevant.
  - [D11] Example 13 (Hindi, split=validation, label=option1): "'मानसून' शब्द की उत्पत्ति किस भाषा से हुई है? … अरबी भाषा" — GK in Hindi, accessible register.
  - [D18] Example 22 (Hindi, split=validation, label=option4): "निम्नलिखित में से कौन एक प्रसिद्ध भारतीय चित्रकार थीं, जिन्हें कभी-कभी भारत की फ्रिदा काहलो के नाम से जाना जाता है? … अमृता शेरगिल" — Indian arts culture GK.

#### Strength 6: Presence of Logical Reasoning and Quantitative Questions (in English Partition)
- **Dimension(s):** IO
- **Observation:** The English partition includes both Logical Reasoning (analogy questions, coding-decoding in Telugu) and Quantitative Aptitude (compound interest calculation). These subjects correspond to UPSC CSAT Paper 2 and SSC CGL Tier 1, which are priority areas the deployment must cover.
- **Deployment relevance:** While these appear in the English partition specifically, their presence confirms that MILU's taxonomy does encompass the Reasoning and Mathematics domains that were flagged as potentially absent. The English partition is described as covering Indian-culture-specific content; the presence of reasoning questions here suggests the Hindi partition likely also has them.
- **Datapoint citations:**
  - [D8] Example 6 (English, split=validation, label=option3): "Fill in the gap below with suitable word. Fruit ∶ Reap∶∶ Flower ∶ _____ … Bloom" — Analogy reasoning question confirming domain presence.
  - [D9] Example 7 (English, split=validation, label=option2): "If Rs. 4000 becomes Rs. 5760 in 2 years at compound interest (compounded annually), then what is the annual rate of interest? … 20 percent" — Quantitative aptitude/compound interest.

#### Strength 7: Hindi Grammar and Language Proficiency Questions Present
- **Dimension(s):** IO, IC
- **Observation:** The Hindi partition includes a Hindi Language Studies question testing indirect speech transformation (reported speech) — a topic directly tested in UPSC Hindi language paper and SSC Hindi proficiency sections.
- **Deployment relevance:** Hindi language proficiency is explicitly listed as a priority subject for this deployment, and the benchmark contains at least some questions testing grammatical competence in Hindi.
- **Datapoint citations:**
  - [D17] Example 9 (Hindi, split=validation, label=option3): "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा, तुम्हें अगले महीने बोनस मिलेगा। … प्रबंधक ने अपने सहायक से कहा कि उसे अगले महीने बोनस मिलेगा।" — Hindi indirect speech transformation, tests Hindi grammatical knowledge.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: 100% Translation Rate in Hindi Validation Sample — No Natively Authored Hindi Questions Observed
- **Dimension(s):** IC
- **Observation:** All 26 Hindi validation examples in the sample carry `is_translated: True`. Not a single natively authored Hindi question appears in this sample. This means every Hindi question observed was originally written in English and translated via GPT-4O. The benchmark documentation states that only ~25% of the total dataset is translated; however, this sample suggests the Hindi validation partition may have a much higher translated proportion than the overall dataset average.
- **Deployment relevance:** This is critical for the deployment. Translated questions may not reflect the vocabulary conventions, sentence structures, or idiomatic phrasing of Hindi-medium competitive exam papers (which have their own established register). Questions authored in Hindi for exams like UPSC Hindi medium, UPPSC, or Hindi SSC papers have characteristic patterns that differ from back-translated English. If the Hindi partition predominantly consists of translated items, the benchmark may poorly represent the linguistic environment of the target student — and models fine-tuned or evaluated on translated Hindi may perform differently on authentically authored Hindi exam content.
- **Datapoint citations:**
  - [D13] All 26 examples (Hindi, split=validation): is_translated = True for all — "जब एक डीसी सीरीज मोटर बिना लोड के चलती है…", "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है…", "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह'…" — every item carries the translated flag.
  - [D15] Example 18 (Hindi, split=validation, label=option3): "1991 में वित्तीय संकट को ट्रिगर करने वाले विदेशी मुद्रा भंडार की हानि का तात्कालिक कारण क्या था?" — direct translation of D14 (English: "What was the immediate cause for loss of foreign reserves…"), confirming the translation pipeline.

#### CRITICAL Concern 2: Output Ontology Mismatch — MCQ Labels Only, No Explanatory Rationale Infrastructure
- **Dimension(s):** OO, OF
- **Observation:** Every datapoint in the dataset provides only a `target` field (one of option1–option4) as the ground-truth output. There is no rationale field, explanation field, or any annotation supporting the deployment's required output: a substantive Hindi-language explanation of why an answer is right or wrong.
- **Deployment relevance:** The deployment's core output is a correct/incorrect label **plus** a Hindi-language explanatory rationale (elicitation Q3). MILU benchmark scores measure only whether a model selects the correct MCQ option — they cannot validate whether the model's Hindi explanations are factually accurate, fluent, or pedagogically appropriate. This is a fundamental scope mismatch confirmed by direct inspection of the data schema. The paper's own limitation section acknowledges the log-likelihood evaluation may differ from generation-based approaches (Q85), but even generation-based scoring in MILU only assesses option selection.
- **Datapoint citations:**
  - [D1] Example 6 (Hindi, split=validation, label=option1): target = "option1" — the only output label is the MCQ choice; no rationale, no explanation field exists in the schema.
  - [D9] Example 7 (English, split=validation, label=option2): target = "option2" — compound interest answer with no worked solution or explanation provided; the schema has no field for this.

#### MAJOR

#### MAJOR Concern 1: Heavy Engineering/Technology Domain Skew in Hindi Sample — Misalignment with Central Exam Priority
- **Dimension(s):** IO
- **Observation:** Of the 26 Hindi validation examples, at least 7 are from Engineering & Tech (DC motor behavior, half-wave rectifier, constant current transformer, AM bandwidth, Fortran 77 column labels, wood swelling in timber, Materials Science) and 3 more are from Science (Computer Science, Biology). Together these constitute approximately 38% of the Hindi sample. By contrast, only 1 question is from Law & Governance (the 44th Amendment, D1) and only 2 are from Arts & Humanities with historical content (D2, D23).
- **Deployment relevance:** For UPSC/SSC/banking central exam preparation, Engineering & Tech and advanced Computer Science questions (e.g., Fortran 77 syntax, D16) are low-priority relative to History, Polity, Geography, and Economics. The observed sample distribution suggests the Hindi partition may over-represent technical domains (possibly because English engineering exam content was translated to fill gaps), which does not reflect the actual subject distribution of UPSC GS or SSC General Awareness syllabi.
- **Datapoint citations:**
  - [D5] Example 1 (Hindi, split=validation): "जब एक डीसी सीरीज मोटर बिना लोड के चलती है" — Engineering question, is_translated: True.
  - [D6] Example 3 (Hindi, split=validation): "हाफ वेव रेक्टिफायर का आउटपुट क्या होता है" — Engineering question, is_translated: True.
  - [D7] Example 4 (Hindi, split=validation): "स्थिर धारा ट्रांसफार्मर _______ प्रकार का होता है" — Engineering question, is_translated: True.
  - [D16] Example 8 (Hindi, split=validation): "फॉरट्रान 77 के फिक्स्ड फॉर्मेट में कॉलम 2 से 5 में संख्या का क्या उद्देश्य होता है" — Niche Computer Science, is_translated: True; not in UPSC/SSC General Studies syllabus.
  - [D36] Example 16 (Hindi, split=validation): "एएम की बैंडविड्थ _________ है। … 1110 kHz" — Electrical engineering bandwidth, is_translated: True.

#### MAJOR Concern 2: Current Affairs Questions Are Time-Bounded and May Be Stale
- **Dimension(s):** IC, IO
- **Observation:** Multiple examples contain Current Affairs questions tied to specific years (2022 state elections, May 2022 archery tournament, 2020 Filmfare Awards, 2021 Padma Awards, Hillary Clinton's June 2014 book). MILU was published in 2024, and these questions reference events from 2014–2022 — meaning a significant portion of "Current Affairs" content is already dated and may not represent the current affairs knowledge tested in 2025–2026 exam cycles.
- **Deployment relevance:** Current Affairs is one of the most heavily weighted and variably tested areas of UPSC GS Paper 1 (confirmed in the web search context). For a deployment serving students preparing for 2025–2026 exam cycles, a benchmark sourced from exams up to ~2023 will have stale current affairs content. Model performance on MILU's Current Affairs items does not predict readiness for current exam cycles.
- **Datapoint citations:**
  - [D4] Example 2 (Hindi, split=validation): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" — 2022 sports event; stale for 2025–26 exam prep.
  - [D25] Example 5 (Punjabi, split=validation): "ਫਰਵਰੀ - ਮਾਰਚ 2022 ਵਿੱਚ ਹੋਈ ਰਾਜ ਵਿਧਾਨਸਭਾ ਚੋਣਾਂ ਵਿੱਚ, ਆਮ ਆਦਮੀ ਪਾਰਟੀ (AAP) ਨੇ … ਪੰਜਾਬ" — 2022 election results; dated.

#### MAJOR Concern 3: Cross-Language Item Duplication Reduces Effective Question Pool Size
- **Dimension(s):** OC, IC
- **Observation:** The same factual questions appear identically translated across multiple language partitions. Examples include: the 1991 financial crisis question (Bengali Ex.1, English Ex.1, Hindi Ex.18, Malayalam Ex.1); the Bahamani Kingdom capital (Bengali Ex.3, English Ex.3, Gujarati Ex.3, Malayalam Ex.3, Punjabi Ex.3); the Qutb Minar completion (Bengali Ex.18, English Ex.18, Gujarati Ex.18, Hindi, Kannada Ex.15, Punjabi Ex.18, Tamil Ex.18); the Mediterranean climate question (English Ex.5, Gujarati Ex.5, Hindi Ex.5, Kannada Ex.5, Malayalam Ex.5, Marathi Ex.5, Punjabi, Tamil Ex.5, Telugu Ex.5). This pattern strongly suggests that a significant fraction of MILU consists of the same items translated, not independently sourced questions for each language.
- **Deployment relevance:** If the same items are used across language partitions via translation, the "79,000 questions" figure conflates distinct items with translated copies. For the Hindi partition specifically, the effective number of unique factual scenarios tested may be substantially smaller than the headline count suggests. Additionally, cross-language translation introduces a risk that questions originally designed for one language/exam context (e.g., SSC English) are not genuinely representative of the Hindi-medium exam ecosystem.
- **Datapoint citations:**
  - [D29] Example 6 (Malayalam, split=validation, label=option1): "ദേശീയ അടിയന്തരാവസ്ഥ പ്രഖ്യാപിക്കാൻ 'സായുധ കലാപം' എന്ന പദം ഭരണഘടനയിൽ ചേർത്തത് എപ്പോൾ?" — same 44th Amendment question as D1 (Hindi), D6 (Tamil), confirmed duplicate across Malayalam.
  - [D14] Example 1 (English, split=validation) and [D15] Example 18 (Hindi, split=validation): "What was the immediate cause for loss of foreign reserves…" / "1991 में वित्तीय संकट को ट्रिगर करने वाले…" — literal translation confirmed by is_translated field.

#### MAJOR Concern 4: Incomplete / Truncated Question Stems Observed
- **Dimension(s):** OC, IC
- **Observation:** At least two distinct examples contain severely truncated or incomplete question stems that do not provide enough context for meaningful answering. English Example 11 reads only "The owner of the textile shop brought a" with options including Computer, Calculator, Pencil, and Fountain pen — with no coherent question preceding this stem fragment. The marble/sculpture directions question appears similarly across Malayalam (Ex.14), Marathi (Ex.14), Telugu (Ex.14), Tamil (Ex.14) as "Directions: marble can be used" or equivalent, with options for painting, music, stones, and sculpture. These appear to be reading-comprehension remnants where the passage was stripped but the question fragment survived.
- **Deployment relevance:** Malformed or incomplete items undermine the validity of the benchmark. A model that encounters such items cannot answer based on the question content — any response is essentially random. If such items appear in the test split, they will add noise to accuracy scores in a way that is not informative about model quality. For a deployment context where the AI must explain the reasoning behind an answer, such items are particularly problematic.
- **Datapoint citations:**
  - [D34] Example 11 (English, split=validation, label=option2): "The owner of the textile shop brought a … Calculator" — No coherent question is present; the stem is a sentence fragment.
  - [D35] Example 14 (Malayalam, split=validation, label=option4): "ദിശകൾ: മാർബിൾ ഉപയോഗിക്കാവുന്നത് … ശിൽപ്പം" — Truncated "Directions:" stem without the relevant passage; same pattern in Marathi Ex.14, Telugu Ex.14, Tamil Ex.14.

#### MINOR

#### MINOR Concern 1: State-Level Content Mixed with Central Exam Content Without Labeling
- **Dimension(s):** IO
- **Observation:** Some items clearly pertain to state-level governance rather than central exams — for example, the Maharashtra Legislative Committee question (English Ex.9) and the Madhya Pradesh Banmore industrial area question (Telugu Ex.25). These are not labeled in the metadata as "state-PSC" versus "central exam" items, making it impossible to filter the benchmark for central-exam-only use without manual review.
- **Deployment relevance:** The deployment is explicitly scoped to central-level examinations (UPSC, SSC, banking), not state PSCs. Items about Maharashtra's legislative committee procedures or MP's industrial geography add noise if used for evaluating central-exam readiness but are not identifiable from the `domain` or `subject` metadata.
- **Datapoint citations:**
  - [D24] Example 9 (English, split=validation, label=option2): "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" — state-level governance question, not central exam scope.
  - [D27] Example 25 (Telugu, split=validation, label=option1): "మధ్యప్రదేశ్‌లోని బన్మోర్ పారిశ్రామిక అభివృద్ధి కేంద్రం ఏ జిల్లాలో ఉంది? … మొరెనా" — State-level (MP) geography question.

#### MINOR Concern 2: North India–Specific Sub-Regional Content Sparse in Observed Hindi Sample
- **Dimension(s):** IC
- **Observation:** Only one question in the Hindi sample (D3, UP minerals) could be classified as specifically North India sub-regional. No questions about Chhath Puja, Bhojpuri culture, zamindari systems, North Indian freedom movement figures (Chandrashekhar Azad, Ram Prasad Bismil), or UP/Bihar/Rajasthan administrative specifics were observed. The Mughal history question (D2) is pan-India/pan-subcontinental rather than specifically North Indian.
- **Deployment relevance:** The deployment must handle both pan-India GK and North India–specific content for central exams. The scarcity of observed North India sub-regional items (1 of 26) suggests this layer may be thinly represented in the Hindi partition, though a 26-item sample is insufficient to make a strong claim.
- **Datapoint citations:**
  - [D3] Example 26 (Hindi, split=validation, label=option2): "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — the only observed North India–specific item in the Hindi sample.

#### MINOR Concern 3: Regional/State-Specific Cultural Content Appears Only in Non-Hindi Partitions
- **Dimension(s):** IC
- **Observation:** Culturally specific regional content (the Halashashthi festival in Marathi Ex.16, Lokranjan Mahotsav in Marathi/Gujarati, Chhattisgarh Bastar revolt in Gujarati/Kannada/Punjabi/Telugu, Sindhi poet Vasdev Mohi in Gujarati, Telangana literature in Kannada) appears in non-Hindi partitions. In the Hindi partition, no comparably region-specific Hindi-belt cultural content (festivals, literary traditions specific to Hindi-speaking North India) was observed.
- **Deployment relevance:** This creates a mild concern that MILU's culturally grounded content — which is a stated design strength — may be distributed toward South Indian and West Indian language partitions, where regional state exams provide richer locally sourced material. The Hindi partition, which is most important for this deployment, may rely more heavily on translated pan-India content than on natively sourced culturally specific Hindi exam content.
- **Datapoint citations:**
  - [D19] Example 16 (Marathi, split=validation, label=option3): "हलषष्ठी सण का साजरा केला जातो? … मुलाच्या दीर्घायुष्यासाठी" — Maharashtra-specific festival question; no equivalent Hindi-belt festival question observed.
  - [D20] Example 16 (Gujarati, split=validation, label=option2): "છત્તીસગઢના નીચેના કયા બળવાઓને 'બસ્તરનો સ્વાતંત્ર્ય સંઘર્ષ' … લિંગગિરી બળવો" — Chhattisgarh tribal revolt; this question also appears in Kannada, Punjabi, Telugu but not observed in Hindi.

---

### Content Coverage Summary

The MILU dataset, as observed across 215 examples from the validation split, is a large-scale MCQ benchmark with broad subject coverage across 11 Indic languages. The Hindi partition (26 examples) demonstrates adequate rendering in standard Devanagari with low observed code-mixing, and contains substantive content relevant to UPSC/SSC central exam topics including Indian constitutional law, Mughal history, and general knowledge in Economics and Geography.

However, two structural features substantially limit the benchmark's fit for this deployment. First, the entire Hindi validation sample is machine-translated (`is_translated: True` for all 26 items), raising questions about linguistic authenticity for the target population of Hindi-medium exam aspirants. Second, the observed domain distribution in the Hindi sample is skewed toward Engineering & Technology (DC motors, transformers, AM bandwidth, Fortran 77) — subjects that are peripheral to UPSC GS and SSC General Awareness. This skew likely results from the translation gap-filling strategy (translating English engineering exam questions to meet minimum thresholds) documented in the benchmark paper.

The English partition shows broader subject coverage, including Logical Reasoning and Mathematics questions, confirming these domains exist within MILU's taxonomy — but their representation in the Hindi partition specifically remains unverified from this sample.

Cross-language item duplication is pervasive: the same factual questions (Bahamani Kingdom capital, Qutb Minar, 1991 financial crisis, Mediterranean climate) appear identically translated across all 11 language partitions in the validation split. This is structurally expected for a translated benchmark but means the effective number of unique factual scenarios is smaller than the total item count implies.

Two malformed items with truncated stems were observed across multiple language partitions, suggesting imperfect filtering of reading-comprehension remnants from the scraping process.

The benchmark's output schema (MCQ `target` field only) provides no infrastructure for evaluating the Hindi-language explanatory rationale that constitutes the deployment's core output — a fundamental mismatch that cannot be remedied by data inspection alone.

---

### Limitations

1. **Sample size and representativeness:** Only validation split examples were examined (26 Hindi, 20–25 per other language). The test split contains approximately 6,600–10,000 examples per language config; the observed 100% translation rate in the Hindi validation sample cannot be generalized to the full test split without examining a larger sample. The actual distribution of natively authored vs. translated Hindi items in the test set requires direct inspection.

2. **Subject distribution cannot be quantified from this sample:** The 26 Hindi examples are insufficient to estimate the true proportion of Engineering/Tech vs. History/Polity/GK/Reasoning items in the Hindi test partition. The observed skew may be an artifact of the small validation sample.

3. **No test split content inspected:** All examples are from the validation split, which is used for few-shot examples in the benchmark's evaluation protocol. The test split (which is the actual evaluation set) was not sampled, and subject distributions may differ.

4. **Translation quality unassessable from inspection alone:** While observed Hindi items are fluent Devanagari, the quality of GPT-4O translations for technical domains (especially Electrical Engineering, Computer Science) relative to authentic Hindi exam register cannot be assessed through casual reading — it would require review by a Hindi-medium domain expert.

5. **No audio or image modality:** These are excluded by MILU's design; no inspectability concern applies.

6. **Rationale quality entirely outside data scope:** The deployment's core output (Hindi explanatory rationale) is wholly absent from the dataset schema. No amount of data inspection can assess this dimension; it requires a separate evaluation framework.