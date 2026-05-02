## Dataset Analysis Report

**Dataset(s):** MBZUAI/ArabicMMLU
**Analysis date:** 2025-01-30
**Examples reviewed:** ~185 examples across 40 subject-level configurations
**Columns shown:** ID, Source, Country, Group, Subject, Level, Question, Context, Answer Key, Option 1–5, is_few_shot
**Columns skipped (media):** None (all text)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | ArabicMMLU | Civics (HS), ID 14501 | A | "من مظاهر التغير التي طرأت على طبيعة المجتمع الاردني الحديث" | "What are the manifestations of change in modern Jordanian society?" — country-specific Jordanian civics | IC |
| D2 | ArabicMMLU | Civics (MS), ID 14291 | C | "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة:" | "The first coalition government in Jordan in 1952 was known as the ___ government" — Jordanian political history | IC |
| D3 | ArabicMMLU | Civics (MS), ID 14255 | D | "المجلس صاحب الولآية العامة على شؤون الدولة كافة هو ب" with answer "مجلس الوزارء" | "The council with general sovereignty over all state affairs is the Council of Ministers" — specifically Jordanian constitutional structure | OC |
| D4 | ArabicMMLU | History (HS), ID 2827 | A | "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة" | "Rights under the [Jordanian] Kingdom's constitution" — explicitly references the Jordanian Hashemite Kingdom | IC, OC |
| D5 | ArabicMMLU | History (HS), ID 2819 | D | "صدر دستور عام 1952 في عهد جلالة الملك" with options referring to Jordanian kings | "The 1952 constitution was issued during the reign of King [Talal bin Abdullah]" — Jordanian royal history | IC |
| D6 | ArabicMMLU | Economics (HS), ID 11412 | C | "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" | "Complaints to the Central Bank [of Jordan] via www.cbj.gov.jo" — explicitly references Jordan's central bank | IC |
| D7 | ArabicMMLU | Economics (HS), ID 11561 | B | "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" | "67% of Jordanians cannot access formal financial services" — Jordan-specific statistic as universal economic fact | IC, OC |
| D8 | ArabicMMLU | Law (Prof), ID 4881 | B | "لا يقبل استئناف الأحكام التمهميدية أو الصادرة في نزاع عارض أو دفوع إلا بعد صدور الحكم في جوهر الدعوى" | Moroccan procedural law — appeals rules under Moroccan Code of Civil Procedure | IC, OC |
| D9 | ArabicMMLU | Law (Prof), ID 4652 | C | "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...بقرار من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" | Moroccan judicial police powers — references "الدرك الملكي" (Royal Gendarmerie of Morocco) | IC, OO |
| D10 | ArabicMMLU | Law (Prof), ID 4843 | C | "إذا تنازل الطرف المدني قبل صدور الحكم: جميع الأجوبة صحيحة" | Moroccan civil party withdrawal in criminal proceedings | IC, OC |
| D11 | ArabicMMLU | Political Science (Univ), ID 6960 | C | "احداث متتابعة قد تكون تعاونیة أو صراعیة ھى: التفاعلات" | "Sequential events, cooperative or conflictual, are called: interactions" — general IR concept | IC |
| D12 | ArabicMMLU | Political Science (Univ), ID 7131 | A | "ﺗﻌﺗﺑر اﻟﺛورة اﻟﻔرﻧﺳﯾﺔ ﻋﺎم 1789 أﺑرز ﻣﺛﺎل ﻟﻠﺛورات اﻟﻛﺑرى اﻟﺗﻲ ﻋززت ﺣﻘوق اﻹﻧﺳﺎن: ﺻﺢ" | "The French Revolution is the foremost example of revolutions that strengthened human rights: True" — all from Egyptian sources (aun.edu.eg) | IC |
| D13 | ArabicMMLU | Accounting (Univ), ID 7245 | A | "يفترض أسموب المراجعة حول الحاسب أنو إذا كانت المدخالت سميمة...فإن عممية التشغيل تكون سميمة بالتبعية" | Computer auditing concept — general accounting principle, from Egyptian source | IC |
| D14 | ArabicMMLU | Management (Univ), ID 6175 | B | "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة...تذتير إلى" | Severely OCR-distorted text about authority distribution in organizations, from Egyptian source | IF |
| D15 | ArabicMMLU | Management (Univ), ID 6174 | C | "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت." | Severely OCR-corrupted management question with unreadable answer options | IF |
| D16 | ArabicMMLU | Computer Science (Univ), ID 7280 | C | "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" | "A microcomputer is a desktop computer" — from KSA source (faculty.ksu.edu.sa) | IC |
| D17 | ArabicMMLU | Islamic Studies (HS), ID 14064 | E | "للتفكير آثار إيجابية عدة: جميع ما ذكر" — Country: Jordan | 5-option Islamic studies question about positive effects of thinking | IO, OO |
| D18 | ArabicMMLU | Islamic Studies (General), ID 165 | D | "قال الرسول صلى الله عليه وسلام: (لا يدخل الجنة قتات)، فمن هو القتات؟ النمام" | "The Prophet said: the 'qattat' shall not enter paradise — who is qattat? A gossip/slanderer" — no country field, generic Islamic trivia source | IC |
| D19 | ArabicMMLU | Arabic Language (Grammar), ID 12626 | A | "In the following Quranic verse, what is the correct parsing of the word ــكَ" | English-language question stem in an Arabic grammar dataset | IF |
| D20 | ArabicMMLU | Social Science (PS), ID 5489 | D | "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات...منها: مستشفى المدينة الطبية" | "Royal Medical Services include: Medical City Hospital" — specifically Jordanian Royal Medical Services | IC |
| D21 | ArabicMMLU | Social Science (PS), ID 5481 | D | "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" | "King Talal bin Hussein's reign ended for health reasons in 1952 — one year" — Jordanian royal history in primary school | IC |
| D22 | ArabicMMLU | Geography (MS), ID 8055 | A | "توجد كنيسة سيدة الجبل في ……. عنجرة" | "Lady of the Mountain Church is in Anjara [Jordan]" — Jordanian religious geography | IC |
| D23 | ArabicMMLU | Computer Science (PS), ID 7354 | A | "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" | "The binary number system is used by computers" — Palestine-sourced primary CS | IC |
| D24 | ArabicMMLU | Biology (HS), ID 9842 | D | "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" | Calvin cycle question — Palestine-sourced biology; universal factual content | IC |
| D25 | ArabicMMLU | Civics (HS), ID 14529 | C | "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" | "The main goal of the 1928 Jordanian-British treaty was liberation from Mandate restrictions" — Jordanian national history | IC |
| D26 | ArabicMMLU | All (Islamic Studies), ID 165–54 | null | All 5 examples: Country = null, Source = folderat.com, Subject = Islamic Studies | Islamic Studies "All" config examples have no country metadata — source appears to be generic Arabic quiz site | IO, OC |
| D27 | ArabicMMLU | Arabic Language (General), ID 11849–11736 | null | All 5 examples: Country = null, Source = madinaharabic.com | Arabic Language General has no country metadata — sourced from online Arabic language learning site | IO |
| D28 | ArabicMMLU | Economics (Univ), ID 11228 | B | "إذا كان حجم الاستثمار المطلوب ١٠٠ر٠٠٠ جنيه...معدل العائد على الأموال المستثمرة هو: % ١٥" | Egyptian currency (جنيه = Egyptian pound) in university economics — Egypt-specific monetary context | IC, OC |
| D29 | ArabicMMLU | Political Science (Univ), ID 7008 | D | "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ" | Severely OCR-distorted Arabic text about conditions for an Islamic ruler — from Egyptian source | IF |
| D30 | ArabicMMLU | Geography (HS), ID 8529 | D | "محمية طبيعية في الأردن تشرف عليها إدارة مشتركة...وادي رم" | "Wadi Rum is a Jordanian nature reserve under joint management" — Jordan-specific geography fact | IC |
| D31 | ArabicMMLU | History (HS), ID 3049 | D | "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" | King Abdullah I's positions on Zionism — highly sensitive political content, Jordanian framing of Palestinian history | IC, OC |
| D32 | ArabicMMLU | Social Science (MS), ID 5261 | D | "أنعم الله على بلادنا العربية بثروات كبيرة من النفط والغاز الطبيعي...يرجع السبب في ذلك إلى: توافره بكميات قليلة" | "Gas is available in limited quantities" — possibly incorrect answer key for general Arab world social science | OC |
| D33 | ArabicMMLU | Computer Science (MS), ID 7333–7343 | all Jordan | All 5 examples: Country = Jordan, Windows OS questions | Middle school CS focuses on Windows OS user interface — likely dated Jordanian curriculum content | IC |
| D34 | ArabicMMLU | Law (Prof), all 5 examples | Morocco | All 5 Law (Professional) examples: Country = Morocco, from single Google Drive PDF | All sampled law questions are exclusively from Morocco — single-source PDF | IC, OC |
| D35 | ArabicMMLU | Driving Test, ID 687, 695 | UAE | "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" | UAE driving rule (50m warning triangle placement) — country-specific traffic regulation | IO, OO |
| D36 | ArabicMMLU | General Knowledge (MS), ID 4556 | A | "الشامل الأكاديمي يمثل ……. الأدبي" | "The 'comprehensive academic' [track] is the humanities track" — Jordanian secondary school track system | IC |
| D37 | ArabicMMLU | Islamic Studies (Primary), ID 12853 | D | "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Country: Jordan | Generic Islamic etiquette of Quran recitation — no madhab specificity indicated | IC |
| D38 | ArabicMMLU | Islamic Studies (HS), ID 14042 | D | "فوائد إيراد الأمثال في القرآن الكريم: جميع ما ذكر" — Country: Jordan | Islamic studies question about examples in Quran — Jordanian curriculum framing | IC |
| D39 | ArabicMMLU | Accounting (Univ), ID 7245 | A | Source: http://www.aun.edu.eg/commerce/... | All 5 accounting examples from Assiut University (Egypt) — single Egyptian university source | IC, OC |
| D40 | ArabicMMLU | Economics (University), all 5 | Egypt | Source: http://www.aun.edu.eg — all 5 from same Assiut University Egypt URL | University economics exclusively from Egyptian university source | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic country-sourced exam content in target languages and format
- **Dimension(s):** IC, IF
- **Observation:** The sampled questions demonstrate genuine national exam provenance — questions are clearly drawn from real school assessments, not translations. Arabic language, grammar, STEM, and Islamic studies questions are well-formed MSA suitable for the school tutoring context. The format is entirely MCQ with 2–5 options, directly matching the deployment's primary format.
- **Deployment relevance:** For the deployment's core use case (supporting students with MCQ exam preparation), the native exam origin means content register, vocabulary difficulty, and question structure are authentic to what students encounter in real exams.
- **Datapoint citations:**
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Authentic Palestinian high school biology question in proper MSA with scientific terminology.
  - [D37] Example Islamic Studies (PS), ID 12853 (Jordan, test): "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Primary school Islamic studies question in standard school format.
  - [D25] Example Civics (HS), ID 14529 (Jordan, test): "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" — Tawjihi-style question format.

#### Strength 2: Broad subject taxonomy covering all six deployment university subjects
- **Dimension(s):** IO
- **Observation:** The dataset's 40 configurations directly observed include Accounting (University), Computer Science (University), Economics (University), Management (University), Political Science (University), and Law (Professional) — all six university-level subjects the deployment targets. This is confirmed through direct data inspection, not just paper claims.
- **Deployment relevance:** The deployment specifically requires coverage of law, management, economics, CS, political science, and accounting for university students. All are present as distinct, queryable configurations.
- **Datapoint citations:**
  - [D13] Example Accounting (Univ), ID 7245 (Egypt, test): "يفترض أسموب المراجعة حول الحاسب أنو إذا كانت المدخالت سميمة...فإن عممية التشغيل تكون سميمة بالتبعية" — University accounting question about computer auditing methodology.
  - [D16] Example CS (Univ), ID 7280 (KSA, test): "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" — University CS definitional question from Saudi source.
  - [D11] Example Political Science (Univ), ID 6960 (Egypt, test): "احداث متتابعة قد تكون تعاونیة أو صراعیة ھى: التفاعلات" — University-level international relations concept.

#### Strength 3: Moroccan law content is present and confirmed in the data
- **Dimension(s):** IC, IO
- **Observation:** The Law (Professional) configuration — the only university/professional law split — contains exclusively Moroccan questions in the sample (all 5 sampled questions from Morocco, sourced from a single Google Drive PDF of Moroccan procedural law). These cover Moroccan appellate procedures, civil party rules, and judicial police powers under Moroccan law, referencing Morocco-specific institutions (الدرك الملكي — Royal Gendarmerie).
- **Deployment relevance:** The web search found this Moroccan law content was used as an illustrative example in the paper, and the data confirms it is genuinely present. For the deployment's Moroccan law students, some Moroccan-jurisdiction legal content exists.
- **Datapoint citations:**
  - [D8] Example Law (Prof), ID 4881 (Morocco, test): "لا يقبل استئناف الأحكام التمهميدية...إلا بعد صدور الحكم في جوهر الدعوى" — Moroccan Code of Civil Procedure appeal rules.
  - [D9] Example Law (Prof), ID 4652 (Morocco, test): "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — Moroccan judicial police appointment procedure referencing Morocco-specific institutions.
  - [D10] Example Law (Prof), ID 4843 (Morocco, test): "إذا تنازل الطرف المدني قبل صدور الحكم: جميع الأجوبة صحيحة" — Moroccan criminal procedure rule.

#### Strength 4: Palestine is substantively present across STEM and language subjects
- **Dimension(s):** IC, IO
- **Observation:** Palestinian-sourced questions appear across multiple configurations: Biology (HS) — 4 of 5 examples from Palestine; Computer Science (Primary) — all 5 examples from Palestine; Math (Primary) — multiple Palestine examples; Arabic Language (Primary) — one Palestine example; Geography (Middle) — 2 Palestine examples; Physics (HS) — 2 Palestine examples. This confirms Palestine is a real contributor, not just a nominal listing.
- **Deployment relevance:** Palestine is a high-priority deployment target. The data shows that for STEM and basic academic subjects, Palestinian curriculum content is genuinely represented.
- **Datapoint citations:**
  - [D23] Example CS (PS), ID 7354 (Palestine, test): "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" — Palestinian primary school CS.
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Palestinian HS biology.

#### Strength 5: STEM content is genuinely curriculum-neutral and reliable across countries
- **Dimension(s):** IC, OC
- **Observation:** Math (Primary), Biology (HS), Physics (HS), Natural Science, and CS questions in the data contain factual content that does not vary by national curriculum. The answers are objectively verifiable regardless of student nationality, making ground-truth labels reliable across all eight deployment countries for these subjects.
- **Deployment relevance:** For the large portion of the deployment serving STEM students, the benchmark's content validity is high. Country-specific annotation bias (the major OC concern) does not affect factual STEM questions.
- **Datapoint citations:**
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Universal biology fact.
  - [D1] through standard math examples: "ما ناتج جمع 2+ 6 = 8" — universal arithmetic.

#### Strength 6: Multi-level education coverage confirmed in data
- **Dimension(s):** IO
- **Observation:** The data directly confirms questions at Primary, Middle, High School, and University (Univ/Prof) levels across multiple subjects. The Level field is consistently populated for school-level questions, and university-level configurations (Accounting, Economics, Management, CS, Political Science) are separately queryable.
- **Deployment relevance:** The deployment targets all four educational tiers. The benchmark's level-specific configurations allow the tutoring system to select difficulty-appropriate questions.
- **Datapoint citations:**
  - [D13] Example Accounting (Univ), Level=Univ — university-level confirmed.
  - [D21] Example Social Science (PS), ID 5481, Level=Primary — primary level confirmed with Jordanian political content.
  - [D5] Example History (HS), ID 2819, Level=High — high school level confirmed.

#### Strength 7: Driving Test subject provides country-specific coverage for UAE, Egypt, and Lebanon
- **Dimension(s):** IO, IC
- **Observation:** The Driving Test configuration contains questions from UAE, Egypt, and Lebanon with country-specific traffic regulations. The UAE examples reference specific UAE road authority rules (50m warning triangle placement), and Lebanon examples reference Lebanese traffic law.
- **Deployment relevance:** While not a core tutoring subject, this demonstrates the benchmark's actual country-specific rule calibration for at least some subjects beyond academic content.
- **Datapoint citations:**
  - [D35] Example Driving Test, ID 687 (UAE, test): "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" — UAE-specific driving rule.
  - [D35] Example Driving Test, ID 1025 (Lebanon, test): "يُحَظَّر على سائق المركبة: يجري مناورة عكس الإتجاه (Demi Tour) وسط الطريق" — Lebanese traffic law (note French loan word "Demi Tour").

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Civics and Social Studies are overwhelmingly Jordanian-centric — not pan-Arab
- **Dimension(s):** IC, OC
- **Severity:** CRITICAL
- **Observation:** In the sampled civics, history, social science, geography, and general knowledge data, the vast majority of country-specific content reflects exclusively Jordanian national curriculum content — Jordanian constitutional structure, Jordanian royal history, Jordanian medical institutions, Jordanian party laws, and Jordanian geographic landmarks. This is not a minor imbalance: the content is not presented as Jordanian-specific but as general curriculum knowledge. A Moroccan, UAE, or Kuwaiti student encountering these questions would be tested on Jordanian national content.
- **Deployment relevance:** The deployment requires curriculum-aligned answers for each of the eight countries. Questions about "الملك طلال بن الحسين," "مجلس التعاون الأردني," and Jordan's 1952 constitution are irrelevant or actively misleading for students from Morocco, UAE, Kuwait, or Palestine whose civics exams test entirely different national content. For civics subjects specifically, the benchmark effectively functions as a Jordanian civics test.
- **Datapoint citations:**
  - [D1] Example Civics (HS), ID 14501 (Jordan): "من مظاهر التغير التي طرأت على طبيعة المجتمع الاردني الحديث" — Explicitly asks about Jordanian society; not applicable to students from other eight countries.
  - [D2] Example Civics (MS), ID 14291 (Jordan): "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة:" — Jordanian political history fact irrelevant to Moroccan or Emirati civics.
  - [D3] Example Civics (MS), ID 14255 (Jordan): "المجلس صاحب الولآية العامة على شؤون الدولة كافة هو ب: مجلس الوزارء" — Framed as a general question but answer is grounded in Jordanian constitutional law.
  - [D21] Example Social Science (PS), ID 5481 (Jordan): "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Jordanian royal history taught as primary school social studies.
  - [D36] Example General Knowledge (MS), ID 4556 (Jordan): "الشامل الأكاديمي يمثل ……. الأدبي" — Jordanian secondary school track labeling system specific to Jordan's education structure.

#### CRITICAL Concern 2: University-level content is dominated by a single Egyptian institution
- **Dimension(s):** IC, OC
- **Severity:** CRITICAL
- **Observation:** All 5 sampled Accounting (University) examples, all 5 Economics (University) examples, all 5 Management (University) examples, and all 5 Political Science (University) examples originate from a single source: Assiut University's Faculty of Commerce (aun.edu.eg). The Management examples notably include severely OCR-corrupted text rendering some questions and answer options unreadable. The Computer Science (University) examples all come from a single KSA source (faculty.ksu.edu.sa).
- **Deployment relevance:** The deployment requires university-level content for students in all eight countries. If university-level accounting, management, economics, and political science are sourced almost exclusively from one Egyptian university's question bank, the benchmark is measuring alignment with that specific institution's curriculum framing, not pan-Arab or per-country university education. For university students in Morocco, UAE, Kuwait, Lebanon, or Jordan, these Egyptian university questions may reflect different course structures, textbook traditions, or exam formats.
- **Datapoint citations:**
  - [D39] Examples Accounting (Univ), IDs 7245, 7196, 7215, 7186, 7185 — all Source: http://www.aun.edu.eg/commerce/... — single Egyptian university.
  - [D40] Examples Economics (Univ), all 5 — all Source: http://www.aun.edu.eg — same Egyptian university.
  - [D14] Example Management (Univ), ID 6175 (Egypt): "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة تذتير إلى" — OCR-corrupted to the point of being unreadable; correct answer cannot be verified from the text alone.
  - [D15] Example Management (Univ), ID 6174 (Egypt): "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت." — Answer options are corrupted Arabic OCR artifacts.

#### CRITICAL Concern 3: Law (Professional) is exclusively Moroccan in the observed data — no evidence of multi-jurisdiction coverage
- **Dimension(s):** IC, OO, OC
- **Severity:** CRITICAL
- **Observation:** All 5 sampled Law (Professional) questions come from a single Moroccan source (a single Google Drive PDF of Moroccan procedural law). While this confirms Moroccan law is present, the deployment requires country-specific legal tutoring for Egypt (Egyptian civil code), UAE (federal civil law with Sharia overlay), Jordan (civil law), KSA (Sharia-based), Lebanon, Kuwait, and Palestine. The observed data provides no evidence that other legal jurisdictions are covered. The benchmark's flat single-correct-answer schema cannot encode that the answer to an appellate procedure question differs between Morocco and Egypt.
- **Deployment relevance:** The deployment user explicitly stated that "the system must tailor legal answers to each country's specific legal system." A benchmark where all sampled law questions are Moroccan procedural law cannot validate a tutoring system's legal correctness for Egyptian, UAE, Jordanian, or Saudi students. The jurisdictional ground truth cannot be determined from the flat label schema.
- **Datapoint citations:**
  - [D8] Example Law (Prof), ID 4881 (Morocco): "لا يقبل استئناف الأحكام التمهميدية...إلا بعد صدور الحكم في جوهر الدعوى" — Moroccan appellate rule; rule may differ under Egyptian or UAE procedural law.
  - [D9] Example Law (Prof), ID 4652 (Morocco): "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — References "الدرك الملكي" (Morocco's Royal Gendarmerie) — institution does not exist in other deployment countries.
  - [D34] All 5 Law examples — Country = Morocco, single source URL — confirms single-jurisdiction observation.

---

#### MAJOR

#### MAJOR Concern 4: Significant OCR corruption in university-level management and political science questions
- **Dimension(s):** IF, OC
- **Severity:** MAJOR
- **Observation:** Multiple university-level management and political science questions contain severely corrupted Arabic text that appears to result from poor OCR of PDF scan material. Answer options in some management questions are entirely unreadable (e.g., "الرخرحم ت," "الح ً ت," "اليؾام"). Some political science questions have broken Arabic words mid-sentence. This affects ground-truth label reliability — if the question text is corrupted, it is unclear whether annotators could correctly verify the answer.
- **Deployment relevance:** The deployment targets university students including management and political science majors. Questions with corrupted text cannot reliably serve as evaluation items and would confuse or mislead students in a tutoring context.
- **Datapoint citations:**
  - [D15] Example Management (Univ), ID 6174 (Egypt): "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت. ...اليؾام" — Multiple answer options are OCR artifacts, not valid Arabic words.
  - [D14] Example Management (Univ), ID 6175 (Egypt): "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة" — Question text has inserted random Arabic letters/diacritics breaking word boundaries.
  - [D29] Example Political Science (Univ), ID 7008 (Egypt): "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ" — Letters are doubled/tripled throughout, rendering text difficult to parse.

#### MAJOR Concern 5: Islamic Studies has no country metadata in the "General" and "All" configurations, and no madhab labeling anywhere
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** The five sampled Islamic Studies (General/All config) examples all have Country = null and are sourced from a generic Arabic quiz website (folderat.com). These questions cover Hadith-based ethics and Prophetic biography — content that is broadly consistent across Sunni traditions. However, no Islamic Studies question observed across any configuration has any madhab labeling, and the Islamic Studies (HS) questions are all Jordanian-curriculum. For Morocco (Maliki), the specific fiqh rulings and jurisprudential framing that appear in school Islamic studies curricula differ from Jordanian (mixed Shafi'i/unspecified) or Saudi (Hanbali) tradition.
- **Deployment relevance:** While the deployment user assessed madhab-level divergence as unlikely at school level, the actual data shows no mechanism for madhab identification or filtering. If a Moroccan student encounters a Hanbali-framing fiqh question from the Jordanian curriculum, the benchmark provides no flag for this. For the tutoring system to confidently support Moroccan Islamic studies students, this is a latent risk.
- **Datapoint citations:**
  - [D26] Examples Islamic Studies (All), IDs 165, 385, 46, 157, 54 — Country = null, Source = folderat.com — no curriculum attribution; generic Islamic knowledge quiz.
  - [D38] Example Islamic Studies (HS), ID 14042 (Jordan): "فوائد إيراد الأمثال في القرآن الكريم: جميع ما ذكر" — Jordanian high school framing of Quranic analysis; Saudi or Moroccan curricula may frame this differently.
  - [D37] Example Islamic Studies (PS), ID 12853 (Jordan): "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Practices of Quran recitation etiquette; factually consistent but Jordanian curriculum source only.

#### MAJOR Concern 6: Jordan-specific national content embedded as school-level "social science" and "history" without country-specific flagging
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** Primary and middle school Social Science questions include Jordanian-specific institutional facts (Jordan's Royal Medical Services, King Talal's reign) presented as factual questions without explicit country labels in question text. History questions at all levels heavily feature Jordanian royal history and Jordanian constitutional content. A benchmark user evaluating model performance on "History (Middle School)" or "Social Science (Primary School)" would receive a metric reflecting Jordanian curriculum knowledge, not pan-Arab or country-neutral historical knowledge.
- **Deployment relevance:** For Moroccan, Emirati, Saudi, or Kuwaiti primary and middle school students, the tutoring system evaluated against ArabicMMLU's history/social science subset would be tested on Jordanian-specific knowledge that is irrelevant to their national curriculum. This creates construct-irrelevant variance that could make a model appear stronger or weaker than it truly is for non-Jordanian curricula.
- **Datapoint citations:**
  - [D21] Example Social Science (PS), ID 5481 (Jordan): "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Primary school Jordan-specific royal history.
  - [D20] Example Social Science (PS), ID 5489 (Jordan): "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات المتخصصة...مستشفى المدينة الطبية" — Jordan-specific institution.
  - [D4] Example History (HS), ID 2827 (Jordan): "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة" — Explicitly the Jordanian (Hashemite) Kingdom's constitution.
  - [D31] Example History (HS), ID 3049 (Jordan): "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — Politically sensitive question about King Abdullah I's positions; framing reflects Jordanian historical narrative which may differ from Palestinian national narrative.

#### MAJOR Concern 7: Economics (HS) contains Jordan-specific financial statistics and institutions
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** High school economics questions reference Jordan's Central Bank (CBJ) website and Jordan-specific financial inclusion statistics (67% of Jordanians without access to formal financial services) as factual questions without flagging them as Jordanian-specific. These figures are not cross-nationally applicable.
- **Deployment relevance:** For a UAE or Saudi Arabian high school economics student, a question asking for the Central Bank of Jordan's website address or Jordan-specific financial statistics would be irrelevant and potentially misleading. The benchmark does not distinguish between general economics principles and jurisdiction-specific institutional facts.
- **Datapoint citations:**
  - [D6] Example Economics (HS), ID 11412 (Jordan): "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" — Jordan-specific institutional URL as exam fact.
  - [D7] Example Economics (HS), ID 11561 (Jordan): "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" — Jordan-specific statistic presented as curriculum fact.

#### MAJOR Concern 8: Egyptian currency denomination used as default in university economics
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** University Economics examples from Assiut University use Egyptian pounds (جنيه) in quantitative finance problems. For students in UAE (using dirhams), Kuwait (dinars), Jordan (dinars), or Morocco (dirhams), the currency denomination embeds Egyptian economic context as a universal fact.
- **Deployment relevance:** For the deployment's university economics students in non-Egyptian countries, correct application of financial formulas requires recognizing this currency context, and any tutor response would need to translate this into local context. The benchmark's ground truth treats Egyptian pound calculations as universally correct.
- **Datapoint citations:**
  - [D28] Example Economics (Univ), ID 11228 (Egypt): "إذا كان حجم الاستثمار المطلوب ١٠٠ر٠٠٠ جنيه...معدل العائد على الأموال المستثمرة هو: % ١٥" — Egyptian pound (جنيه) used in an ROI calculation presented as a general economics problem.

---

#### MINOR

#### MINOR Concern 9: One Arabic grammar question has an English-language question stem
- **Dimension(s):** IF
- **Severity:** MINOR
- **Observation:** In the Arabic Language (Grammar) configuration, one example (ID 12626) has an English question stem: "In the following Quranic verse, what is the correct parsing of the word ــكَ" — while the answer options are in Arabic. This appears to be a data entry anomaly from the madinaharabic.com source.
- **Deployment relevance:** Minor data quality concern; single example unlikely to materially affect aggregate scores, but suggests the data scraping pipeline did not filter out mixed-language question stems consistently.
- **Datapoint citations:**
  - [D19] Example Arabic Language (Grammar), ID 12626 (null country): "In the following Quranic verse, what is the correct parsing of the word ــكَ" — English stem in an Arabic grammar configuration.

#### MINOR Concern 10: Multiple configurations have null Country and null Level fields
- **Dimension(s):** IO, IC
- **Severity:** MINOR
- **Observation:** The Islamic Studies (General), Islamic Studies (All config), Arabic Language (General), Arabic Language (Grammar), and several other configurations have Country = null and Level = null for all sampled examples. These questions come from generic online quiz platforms (folderat.com, madinaharabic.com) rather than national exam sources, meaning they are not tied to any specific national curriculum or education level.
- **Deployment relevance:** Null-country questions cannot be used for country-specific evaluation. For the deployment's diagnostic use case (evaluating model performance per country and per level), these questions contribute noise to aggregate metrics without providing actionable per-country signal.
- **Datapoint citations:**
  - [D26] Examples Islamic Studies (All), IDs 165, 385, 46, 157, 54 — Country = null, Level = null.
  - [D27] Examples Arabic Language (General), IDs 11849–11736 — Country = null, Level = null, Source = madinaharabic.com.

#### MINOR Concern 11: Social Science (Middle School) may contain a questionable ground-truth label
- **Dimension(s):** OC
- **Severity:** MINOR
- **Observation:** Example ID 5261 from Social Science (Middle School) asks why natural gas is an important energy source and provides the answer "توافره بكميات قليلة" ("available in limited quantities") as correct. This appears to be an odd ground truth — natural gas importance is generally attributed to abundance, not scarcity. This could be an exam error carried over from the source, or a printing artifact. The benchmark's 96% accuracy ceiling acknowledges approximately 4% error rate.
- **Deployment relevance:** For a tutoring system, propagating potentially incorrect factual claims to students would be harmful. This single example is unlikely to be more than a data error within the acknowledged 4% noise floor, but it illustrates that some answer keys may be incorrect.
- **Datapoint citations:**
  - [D32] Example Social Science (MS), ID 5261 (null country): "يرجع السبب في ذلك إلى: توافره بكميات قليلة" — Answer states natural gas is important because it is available in limited quantities, which is contrary to standard economic reasoning.

#### MINOR Concern 12: Middle school Computer Science is Windows OS-centric with potentially dated content
- **Dimension(s):** IC
- **Severity:** MINOR
- **Observation:** The Computer Science (Middle School) sample contains multiple questions about Windows desktop interface operations (background images, right-click menus, icon arrangement, Windows system files). This is curriculum-specific to Jordan's circa 2015–2020 ICT curriculum and may not reflect UAE, Egyptian, or Palestinian CS middle school content, which may focus on different platforms or concepts.
- **Deployment relevance:** For a tutoring system supporting all eight countries' CS curricula, a heavily Windows-GUI-focused CS subset may misrepresent what CS knowledge looks like for students in other countries.
- **Datapoint citations:**
  - [D33] Example CS (MS), ID 7340 (Jordan): "لتخصيص صورة تحل محل الخلفية الافتراضية تنقر زر: خلفية سطح المكتب" — "To change the desktop background, click: Desktop Background" — Windows UI tutorial question.
  - [D33] Example CS (MS), ID 7343 (Jordan): "إذا تم حذف ملف من ملفات النظام Windows هل يؤثر ذلك على عمل النظام: يؤثر" — Windows system files question.

---

### Content Coverage Summary

The 185+ examples reviewed span all 40 subject-level configurations and provide a clear picture of the benchmark's content composition:

**Country distribution in sample:** Jordan is the dominant country across school-level humanities, social science, civics, history, geography, Arabic language, economics, general knowledge, and Islamic studies configurations. Palestine appears substantially in STEM subjects (Biology HS, CS Primary/HS, Physics HS, Math Primary, Geography Middle) and some social science. Egypt dominates all university-level non-CS configurations (Accounting, Economics, Management, Political Science). Morocco appears exclusively in Law (Professional). KSA appears in CS (University). UAE appears in Driving Test. Lebanon appears in Driving Test. Kuwait and several other countries have zero observed examples across the sample.

**Register and difficulty:** Questions are appropriate for their labeled educational level — primary questions are simple and short, high school questions involve more complex reasoning, and university questions involve domain-specific terminology. MSA is consistently used throughout, with appropriate formal register for educational contexts.

**Content types observed:** (1) Factual recall of national curriculum content — heavily Jordanian for school level; (2) definitional/conceptual questions in STEM and social science; (3) procedural/institutional knowledge (legal procedures, constitutional facts); (4) quantitative problems in mathematics and applied economics; (5) Arabic language morphology and grammar analysis.

**Quality issues:** OCR corruption is a material concern in some university-level PDFs, particularly management and political science from Egyptian sources. A small number of questions have null answer options (Option 3/4 = null when only 2-3 options provided) which is expected given the 2–5 option range. Some questions have truncated or incomplete text, likely from the original PDF scraping.

**Geographic representation gap confirmed in data:** No Kuwait or UAE examples observed outside the Driving Test. No Moroccan examples outside Law (Professional) and one or two Arabic language items. The Jordan-Egypt-Palestine dominance documented in the paper is directly observable in the data.

---

### Limitations

1. **Sample size per configuration:** Most configurations were sampled at 5–8 examples out of test splits ranging from 50–500+ questions. Individual configurations (especially smaller ones) may be substantially different from what the sample shows. Country distribution within configurations beyond Jordan/Egypt/Palestine is particularly uncertain.

2. **Kuwait coverage unverifiable:** No Kuwaiti examples appeared in any sampled configuration. This is consistent with the documented concern but cannot be definitively confirmed as zero-coverage from this sample alone — a full dataset scan would be needed.

3. **University-level sample is thin:** With ~6.1% of questions at university level (~889 total), each university subject configuration is small. The 5 examples sampled per university configuration may represent a substantial fraction of the total, making these configurations particularly sensitive to source diversity (or lack thereof).

4. **Law (Professional) is the only law configuration:** The sample cannot determine whether other law content is embedded in other humanities configurations. The Moroccan dominance of Law (Professional) in the sample may not generalize to all 299+ law questions identified by ArabLegalEval.

5. **Islamic studies madhab calibration:** The data does not contain any explicit madhab identifiers, and the question content observed does not clearly differentiate between madhab traditions. Confirming whether any questions are madhab-specific would require expert Islamic jurisprudence review, which is outside the scope of this data analysis.

6. **OCR corruption extent:** The Management (University) and Political Science (University) OCR corruption was observed in the sample but the total proportion of corrupted questions in these configurations cannot be estimated from 5-question samples.

7. **No inspection of few-shot split:** The `is_few_shot` field was observed (value = 0 for all sampled test examples), but the dev split (few-shot examples) was not sampled. Few-shot examples may have different country distributions.