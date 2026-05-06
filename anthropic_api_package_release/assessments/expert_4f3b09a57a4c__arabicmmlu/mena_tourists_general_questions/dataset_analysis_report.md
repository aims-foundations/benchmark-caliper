## Dataset Analysis Report

**Dataset(s):** MBZUAI/ArabicMMLU
**Analysis date:** 2025-01-31
**Examples reviewed:** ~210 examples across 41 configs (5–8 per config)
**Columns shown:** ID, Source, Country, Group, Subject, Level, Question, Context, Answer Key, Option 1–5, is_few_shot
**Columns skipped (media):** None (text-only dataset; Context field is mostly null in sampled examples)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | History (High School) | ID 3049, Jordan | D | "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين: إتمام وحدة الضفتين عام 1950م / رفضه إعطاء اليهود ممراً إلى حائط البراق / دعوة العرب إلى دعم صندوق الأمة الفلسطيني / رفضه معاهدة سايكس بيكو ووعد بلفور رفضاً قاطعاَ" | Jordan HS history question about King Abdullah I's positions on Zionism and Palestine — framed from Jordanian curriculum perspective | IO, IC, OC |
| D2 | Civics (High School) | ID 14526, Jordan | B | "مثّل ______ العرب في مؤتمر الصلح الذي عقده الحلفاء في باريس: ١-الأمير عبدالله بن الحسين / ٢-الأمير فيصل بن الحسين / ٣-الشريف الحُسين بن علي / ٤-الحُسين بن طلال" | Jordan civics HS: who represented Arabs at Paris Peace Conference — Jordanian Hashemite framing | IC, OC |
| D3 | Civics (High School) | ID 14529, Jordan | C | "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" | Jordan civics HS: primary goal of the 1948 Jordanian-British treaty — Jordanian national framing | IC, OC |
| D4 | Civics (Middle School) | IDs 14291–14327 (5 items), Jordan | various | "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952... القوة العربية من تشكيلات الجيش العربي الأردني... عُدل قانون الأحزاب الأردني" | All 5 sampled Civics Middle School items are exclusively about Jordanian political history | IO, IC |
| D5 | Law (Professional) | IDs 4824, 4843, 4880, 4881, 4652, Morocco | B/C/D/E/C | "يبتدئ أجل الاستئناف... من وزير العدل والسلطة الحكومية المكلفة بالدفاع الوطني" | All 5 sampled Law (Professional) items are from Morocco (Moroccan procedural law) | IO, IC |
| D6 | Geography (Middle School) | ID 8055, Jordan | A | "توجد كنيسة سيدة الجبل في ……. عنجرة" | Jordan middle school geography: location of Lady of the Mountain church in Ajloun, Jordan | IC |
| D7 | Geography (High School) | ID 8529, Jordan | D | "محمية طبيعية في الأردن تشرف عليها إدارة مشتركة بين سلطة المنطقة الاقتصادية الخاصة في العقبة ووزارة السياحة والجمعية الملكية لحماية الطبيعة: وادي رم" | Jordan HS geography: Jordan-specific nature reserve question | IC |
| D8 | History (High School) | ID 2819, Jordan | D | "صدر دستور عام 1952 في عهد جلالة الملك: طلال بن عبدالله" | Jordan HS history: which Jordanian king issued 1952 constitution | IC |
| D9 | History (High School) | ID 2716, Jordan | D | "ترمز الكرة الارضية في شعار المملكة الاردنية الهاشمية إلى: انتشار الاسلام" | Jordan HS history: symbolism in the Hashemite Kingdom's emblem | IC |
| D10 | Social Science (Primary School) | ID 5489, Jordan | D | "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات المتخصصة... مستشفى المدينة الطبية" | Jordan primary social science: Jordan Royal Medical Services institutions | IC |
| D11 | Social Science (Primary School) | ID 5481, Jordan | D | "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" | Jordan primary social science: fact about King Talal's reign — Jordan-specific | IC |
| D12 | Economics (High School) | ID 11412, Jordan | C | "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" | Jordan HS economics: URL of the Central Bank of Jordan — Jordan-institution specific | IC |
| D13 | Economics (High School) | ID 11561, Jordan | B | "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" | Jordan HS economics: Jordan-specific financial inclusion statistic | IC |
| D14 | Islamic Studies (General) | IDs 165, 385, 46, 157, 54 — Country=null | A/D | "من هو النبي الذي علم منطق الطير؟ سليمان عليه السلام / كم مرة اعتمر النبي صلى الله عليه وسلم؟ أربع عمرات" | Pan-Islamic knowledge questions: no country field — factual hadith/Quran questions | IC, IO |
| D15 | Arabic Language (General) | ID 11728, Country=null | B | "يعود تاريخ العرب إلى آلاف السنين... سُمِّيَ العدنانيون بعرب [فراغ]. الشمال" | Pan-Arab ethnolinguistic history reading comprehension — culturally grounded, no country marker | IC |
| D16 | Arabic Language (Grammar) | ID 12626, Country=null | A | "In the following Quranic verse, what is the correct parsing of the word ــكَ" | Grammar question with English question stem — unexpected language mixing in nominally Arabic benchmark | IF |
| D17 | Geography (Middle School) | ID 8136, Palestine | D | "من الجزر المحيطة بقارة أقيانوسيا: نيوزيلندا / تسمانيا / سلمن / جميع ما ذكر" | Palestine middle school geography: world geography (Oceania islands) — no regional specificity | IC |
| D18 | Geography (Middle School) | ID 8064, Palestine | C | "جمع ما يلي من عناصر الدولة عدا: الشعب / الاقليم / الاحتلال / السيادة" | Palestine MS geography: elements of a state — "occupation" appears as a distractors option | OC |
| D19 | History (Middle School) | ID 2641, Palestine | A | "العلم الذي يبحث في حركات ومواقع النجوم والكواكب: الفلك" | Palestine MS history: astronomy definition — not politically sensitive | IC |
| D20 | Computer Science (Primary School) | IDs 7354–7599, Palestine | various | "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" | Palestine primary CS: binary number systems — STEM, no contested content | IC |
| D21 | Biology (High School) | IDs 9699, 9707, 9834, Palestine | B/B/B | "مقدار تكبير العدسة الزيتية في المجهر الضوئي هو: X100 / إحدى العضيات التالية مسئولة عن تصنيع الليبيدات في الخلية: الشبكة الاندوبلازمية الملساء" | Palestine HS biology: standard cellular biology — culturally neutral STEM | IC |
| D22 | Accounting (University) | IDs 7185–7245, Egypt | A/B | "يفترض أسلوب المراجعة حول الحاسب أنه إذا كانت المدخلات سليمة... فإن عملية التشغيل تكون سليمة بالتبعية: صح" | Egypt university accounting — auditing/financial statements questions | IO |
| D23 | Management (University) | IDs 6174–6175, Egypt | B/C | "درجتة تهييتع الدتلطة بتين الألتخاص... تذتير إلى: ال مركز ة" | Severely garbled OCR text making question almost illegible | IC, OC |
| D24 | Political Science (University) | IDs 7008, 7024, Egypt | D | "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ: كل ما سبق" | Egypt university political science with severe OCR corruption — content partially unreadable | IC, OC |
| D25 | Civics (High School) | ID 14546, Jordan | B | "الدول التي سعت الى اقامة مجلس التعاون الخليجي هي (الامارات العربيه المتحده، قطر، عُمان، اليمن، العراق): لا" | Jordan civics HS: false claim about GCC founding states — correct answer is "No" since Yemen and Iraq were not founders | IO, OC |
| D26 | Driving Test | IDs 687, 695, UAE; 1025, Lebanon; 806, 798, Egypt | various | "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" | Driving test questions from UAE, Lebanon, Egypt — practical/regulatory, not school-curriculum history/geography | IO |
| D27 | General Knowledge (Primary School) | ID 4381, Jordan | B | "برغي سن الصاج هو: مسمار لولبي الشكل مسلوب من نهايته" | Jordan primary GK: sheet metal screw definition — vocational/practical knowledge | IO |
| D28 | General Knowledge (Middle School) | ID 4556, Jordan | A | "الشامل الأكاديمي يمثل: الأدبي" | Jordan middle school GK: Jordanian academic track system — Jordan-specific educational structure | IC |
| D29 | Arabic Language (Grammar) | ID 12655, Country=null | D | "في الآية القرآنية ﴿إنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحاتِ﴾، ما هو الإعراب الصحيح لكلمة إنَّ: حرف توكيد ونصب" | Arabic grammar parsing using Quranic verse — MSA grammar directly relevant to deployment | IF |
| D30 | History (High School) | ID 2827, Jordan | A | "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة... القيام بشعائر الأديان" | Jordan HS history/civics: Jordanian constitution rights — Jordan-specific legal framing | IC, OC |
| D31 | Islamic Studies (High School) | ID 14064, Jordan | E | "للتفكير آثار إيجابية عدة: جميع ما ذكر" | Jordan HS Islamic studies: positive effects of thinking (Islamic values framing) — presented as school subject | IC |
| D32 | Social Science (Middle School) | ID 5261, Country=null | D | "أنعم الله على بلادنا العربية بثروات كبيرة من النفط والغاز الطبيعي... يرجع السبب في ذلك إلى: توافره بكميات قليلة" | Pan-Arab social science MS: Arab world natural resources | IC |
| D33 | Geography (Primary School) | ID 7848, Jordan | A | "يمتد الوطن العربي في قارتي: آسيا وأفريقيا" | Jordan primary geography: Arab world spans Asia and Africa — broad pan-Arab framing | IC |
| D34 | History (Primary School) | ID 2437, Jordan | D | "يثرب هو الاسم القديم ل: المدينة المنورة" | Jordan primary history: ancient name of Medina — Islamic history, factual | IC |
| D35 | Arabic Language (General) | ID 12069, Country=null | B | "لا يمكن أنْ يصلي المسلم [فراغ]: بدون وضوء" | Arabic language reading with Islamic ritual context — assumes Muslim reader perspective | IC |
| D36 | Computer Science (University) | IDs 7262–7303, KSA | C/A/B/A | "جميع البرامج التالية تعتبر من التطبيقات باستثناء: نظام التشغيل" | KSA university CS: basic computer science concepts — confirmed KSA source | IO |
| D37 | Geography (Middle School) | ID 8058, Jordan | C | "يوجد متحف التاريخ الطبيعي في: نيويورك" | Jordan MS geography: Natural History Museum location — answer is New York, not the primary one | OC |
| D38 | Natural Science (Middle School) | IDs 1902, 1865 — Country=null | C/B | "قام أحمد بحرق كمية من الماغنيسيوم بالمختبر؛ أي المعادلات التالية تصف التفاعل الذي حصل؟ الماغنيسيوم + أكسجين -> أكسيد الماغنيسيوم" | Natural science MS: chemistry reactions — country-neutral STEM | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic school-curriculum framing directly matches deployment knowledge scope
- **Dimension(s):** IO, IC
- **Observation:** The benchmark is genuinely sourced from national school exam materials, not translated from English. Subjects directly relevant to the deployment — history, geography, civics, Arabic language, Islamic studies, and social science — appear across multiple levels and multiple countries. The sampled data confirms subject labels match the deployment's "school-curriculum level" scope.
- **Deployment relevance:** Tourists seeking educational-level knowledge about Arab history, geography, and language will encounter exactly the types of questions the benchmark tests. This supports construct validity for the core knowledge-testing use case.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — Modern Arab history question at HS level, directly in-scope for deployment
  - [D15] Arabic Language (General), ID 11728, null, label=B: "يعود تاريخ العرب إلى آلاف السنين... سُمِّيَ العدنانيون بعرب [فراغ]. الشمال" — Reading comprehension about Arab ethnolinguistic history at appropriate level
  - [D33] Geography (Primary School), ID 7848, Jordan, label=A: "يمتد الوطن العربي في قارتي: آسيا وأفريقيا" — Basic Arab world geography, school-level

#### Strength 2: Palestine confirmed as top-3 source country with substantial curriculum content
- **Dimension(s):** IO, IC
- **Observation:** Multiple samples confirm Palestinian-sourced questions exist across subjects: Biology (high school, multiple items), Computer Science (primary, 5+ items), Math (primary), Physics (high school), Geography (middle school), Social Science (primary), Arabic Language (primary school). This is a stronger regional representation than anticipated by the benchmark YAML's uncertainty.
- **Deployment relevance:** Palestine is a deployment country, and its curriculum content is substantively represented. For STEM and language subjects, Palestinian curriculum questions appear consistent with pan-Arab academic content and do not differ from Jordanian content in ways that would cause validity problems.
- **Datapoint citations:**
  - [D21] Biology (High School), IDs 9699/9707/9834, Palestine, label=B/C/B: "مقدار تكبير العدسة الزيتية في المجهر الضوئي هو: X100" — Palestinian HS biology is standard STEM content
  - [D20] Computer Science (Primary School), IDs 7354–7599, Palestine: "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" — Palestinian primary CS questions
  - [D17] Geography (Middle School), ID 8136, Palestine, label=D: "من الجزر المحيطة بقارة أقيانوسيا: جميع ما ذكر" — Palestinian geography content is globally framed, not locally contested

#### Strength 3: Morocco is present with country-specific legal/professional content
- **Dimension(s):** IO, IC
- **Observation:** The Law (Professional) config consists entirely of Morocco-sourced questions in the sample (all 5 examples, Country=Morocco), drawn from Moroccan procedural law. This confirms Morocco has substantive, country-specific representation in at least one subject area. The legal language is distinctly Moroccan in register and references Moroccan legal institutions.
- **Deployment relevance:** Morocco is a flagged coverage gap in the deployment context. Finding authentic Moroccan-sourced content confirms the country is not entirely absent, though its coverage is concentrated in a subject area (professional law) that is out of scope for the tourist/expat school-knowledge use case.
- **Datapoint citations:**
  - [D5] Law (Professional), ID 4824, Morocco, label=E: "يتم استدعاء الشهود بأحد الطرق التالية... الطريقة الإدارية / جميع الأجوبة صحيحة" — Moroccan procedural law question with five options, distinctly Moroccan legal framing
  - [D5] Law (Professional), ID 4652, Morocco, label=C: "من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — Moroccan "Gendarmerie Royale" ("الدرك الملكي") referenced — culturally distinctive Moroccan institutional name

#### Strength 4: MSA text-only format aligns with deployment's text modality requirement
- **Dimension(s):** IF
- **Observation:** All sampled questions are in Modern Standard Arabic (Arabic script), text-only, with clear question–option structure. There are no images, audio, or multimodal elements in any sampled example. Contextual passages where present (e.g., Arabic Language General config) are also in MSA prose. The format is consistent across all 41 configs.
- **Deployment relevance:** The deployment is text-only and targets MSA-using Arabic learners. The benchmark's uniform MSA text format matches the interaction modality.
- **Datapoint citations:**
  - [D29] Arabic Language (Grammar), ID 12655, null, label=D: "في الآية القرآنية ﴿إنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحاتِ﴾، ما هو الإعراب الصحيح لكلمة إنَّ: حرف توكيد ونصب" — Clear MSA grammar question, text-only
  - [D15] Arabic Language (General), ID 11728, null, label=B: full passage in MSA prose about Arab history with comprehension question — demonstrates passage-based reading in MSA

#### Strength 5: Broad multi-subject taxonomy across education levels confirmed in data
- **Dimension(s):** IO
- **Observation:** The sampled data confirms 40 distinct tasks are genuinely populated with level-appropriate content: primary school questions are simpler (e.g., basic arithmetic, vocabulary, animal facts), middle school questions involve more abstract concepts, and high school questions involve analytical reasoning. The taxonomy covers STEM, Humanities, Social Science, Language, and Other as labeled.
- **Deployment relevance:** The broad level distribution allows assessment of whether a system can handle the full range of school-curriculum knowledge a tourist might ask about — from basic facts to higher-level concepts.
- **Datapoint citations:**
  - [D38] Natural Science (Middle School), ID 1902, null, label=C: "قام أحمد بحرق كمية من الماغنيسيوم بالمختبر؛ أي المعادلات التالية تصف التفاعل الذي حصل؟" — Level-appropriate chemistry content
  - [D22] Accounting (University), ID 7245, Egypt, label=A: "يفترض أسلوب المراجعة حول الحاسب أنه إذا كانت المدخلات سليمة..." — University-level auditing/IT question
  - [D34] History (Primary School), ID 2437, Jordan, label=D: "يثرب هو الاسم القديم ل: المدينة المنورة" — Primary-level Islamic history fact

#### Strength 6: KSA content confirmed through university-level source URLs
- **Dimension(s):** IO, IC
- **Observation:** The Computer Science (University) config is sourced entirely from KSA (King Saud University: `faculty.ksu.edu.sa`), confirming KSA's presence in at least the STEM university tier. Saudi internal workers are also represented in the annotator pool per the documentation.
- **Deployment relevance:** KSA is a deployment country. The presence of KSA-sourced university STEM questions confirms some Gulf coverage in the benchmark.
- **Datapoint citations:**
  - [D36] Computer Science (University), ID 7280, KSA, label=C: "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" — Sourced from `faculty.ksu.edu.sa`, confirming KSA institutional sourcing

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Output form is entirely MCQ — cannot evaluate multi-perspective acknowledgment required by deployment
- **Dimension(s):** OO, OF
- **Observation:** Every single sampled example uses a single-correct-answer MCQ format (options A–E, one labeled correct). Contested historical and civic questions — such as the question about King Abdullah I's positions on Zionism [D1], or the Jordanian-Palestinian political questions [D2, D3] — are all assigned a single "correct" answer from the Jordanian curriculum perspective. The benchmark cannot evaluate whether a system acknowledges competing Palestinian, Egyptian, or pan-Arab framings of the same events.
- **Deployment relevance:** The deployment explicitly requires the system to "acknowledge multiple perspectives and note that different countries hold different positions." This is the most critical structural mismatch: the benchmark scores only factual recall within one curriculum's framing, not pluralistic or explanatory responses.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — A question about Jordanian/Palestinian political history has a single Jordanian-curriculum correct answer, with no mechanism to flag that Palestinian perspectives may frame this history differently
  - [D25] Civics (High School), ID 14546, Jordan, label=B: "الدول التي سعت الى اقامة مجلس التعاون الخليجي هي (الامارات العربيه المتحده، قطر، عُمان، اليمن، العراق): لا" — True/false about GCC founding — correct answer is "No" but only one national framing is tested
  - [D18] Geography (Middle School), ID 8064, Palestine, label=C: "جمع ما يلي من عناصر الدولة عدا: الشعب / الاقليم / الاحتلال / السيادة" — "Occupation" (الاحتلال) appears as a distractor for "elements of a state" — a politically loaded framing that receives a single correct answer without any acknowledgment of the contested status of Palestinian statehood

#### CRITICAL Concern 2: Civics content is overwhelmingly Jordan-specific, not pan-Arab or multi-country
- **Dimension(s):** IO, IC
- **Observation:** All 5 sampled Civics (Middle School) items are exclusively about Jordanian political institutions, Jordanian government history, and Jordanian party law. All 5 sampled Civics (High School) items are also Jordan-centric (Jordanian society, Arab Cooperation Council from Jordanian perspective, Jordanian-British treaty). This confirms the Jordan-skew documented in the YAML extends to the civics domain, which is the most sensitive for the multi-perspective deployment requirement.
- **Deployment relevance:** For tourists in any of the other seven deployment countries (Morocco, Egypt, Palestine, Lebanon, UAE, Kuwait, KSA), civics questions about Jordanian government structures, Jordanian army formations, and Jordanian party law have minimal relevance. More critically, a system trained or evaluated on these civics items may produce Jordanian-framed answers to generic Arab civics questions asked by users in other countries.
- **Datapoint citations:**
  - [D4] Civics (Middle School), IDs 14291–14327, Jordan: "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة: الوطنية" / "القوة العربية من تشكيلات الجيش العربي الأردني في المرحلة: الأولى" / "عُدل قانون الأحزاب الأردني حيث جاء فيه ألا يقل عدد المؤسسين للحزب عن (500) عضو عام: 2007" — All five civics MS items are Jordanian-specific
  - [D2] Civics (High School), ID 14526, Jordan, label=B: "مثّل ______ العرب في مؤتمر الصلح الذي عقده الحلفاء في باريس: الأمير فيصل بن الحسين" — Presents Hashemite framing of pan-Arab representation without acknowledging other national narratives
  - [D3] Civics (High School), ID 14529, Jordan, label=C: "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨" — Highly Jordan-specific political history content

#### MAJOR

#### MAJOR Concern 3: Jordanian-curriculum framing in contested history questions risks annotation bias
- **Dimension(s):** IC, OC
- **Observation:** The history content sampled is heavily Jordanian in framing. The question about King Abdullah I and Zionism [D1] presents the Jordanian narrative as the sole "correct" answer. The question about the 1952 Jordanian constitution [D8] and Hashemite emblem symbolism [D9] treats Jordan-specific historical facts as the authoritative framing. Since no Palestinian annotators verified Palestinian-sourced questions, and the civics sample confirms Jordan-centric framing, the benchmark's ground-truth for contested historical events may reflect Jordanian national consensus rather than pan-Arab or Palestinian perspectives.
- **Deployment relevance:** A system evaluated well on these items might give Jordanian-framed answers to tourists in Palestine, Lebanon, or Morocco who ask about shared historical events. The deployment requires explicit flagging of country-specific perspectives, but the benchmark labels do not encode this requirement.
- **Datapoint citations:**
  - [D1] History (High School), ID 3049, Jordan, label=D: "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين: رفضه معاهدة سايكس بيكو ووعد بلفور رفضاً قاطعاً" — The "correct" answer (he did NOT reject Balfour unequivocally) reflects Jordanian historical consensus that may be contested by Palestinian historiography
  - [D30] History (High School), ID 2827, Jordan, label=A: "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة... القيام بشعائر الأديان" — Jordanian constitutional framing of religious freedom rights
  - [D11] Social Science (Primary School), ID 5481, Jordan, label=D: "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Jordanian royal history presented as school-level social science

#### MAJOR Concern 4: Kuwait is effectively absent from the sampled data
- **Dimension(s):** IO, IC
- **Observation:** Across all 41 sampled configs (approximately 210 examples), no single example has Country=Kuwait. The web search findings confirm Kuwait is absent from the country-grouped model performance table in the paper, and no Kuwaiti collaborators are acknowledged. This absence is confirmed in practice by the sampled data.
- **Deployment relevance:** Kuwait is one of the eight deployment countries. Any system evaluated on ArabicMMLU will have essentially no Kuwaiti curriculum exposure in its evaluation, meaning the benchmark cannot assess whether the system handles Kuwait-specific school knowledge appropriately.
- **Datapoint citations:**
  - Zero instances of Country=Kuwait across all 210 sampled examples — absence constitutes the evidence; no positive citations possible

#### MAJOR Concern 5: OCR/digitization quality issues create illegible questions in some university-level items
- **Dimension(s):** IC, OC
- **Observation:** Multiple university-level items from Egyptian sources show severe OCR corruption that renders question text partially or wholly illegible. Characters are scrambled, words are unreadable, and answer options contain garbled text. This affects at least the Management (University) and Political Science (University) configs and potentially others.
- **Deployment relevance:** A system that answers OCR-corrupted questions "correctly" is exploiting noise rather than demonstrating knowledge. Benchmark scores on corrupted items have no validity for the deployment's knowledge-testing purpose. The 96% answer-key accuracy ceiling documented in the YAML may be overestimated for university-level Egyptian content.
- **Datapoint citations:**
  - [D23] Management (University), ID 6175, Egypt, label=C: "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة تذتير إلى: ال مركز ة" — Severely corrupted OCR; question is unreadable without reconstruction
  - [D24] Political Science (University), ID 7008, Egypt, label=D: "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ: كل ما سبق" — OCR corruption throughout; answer options also corrupted

#### MAJOR Concern 6: Morocco's curriculum representation is limited to professional law, absent from school-curriculum subjects
- **Dimension(s):** IO, IC
- **Observation:** While Morocco appears in the Law (Professional) config (all 5 sampled items), no Morocco-sourced questions were found in the school-curriculum subjects (History, Geography, Civics, Social Science, Islamic Studies, Arabic Language) across the sampled data. The Moroccan legal questions reference Moroccan legal procedure and institutions, but the deployment requires school-curriculum knowledge (history, geography, Arabic language), which is where Moroccan curriculum distinctiveness (Maghrebi historical framing, French-influenced educational tradition) would matter most.
- **Deployment relevance:** Tourists visiting Morocco and asking about Moroccan history, geography, or civic life will encounter questions where the benchmark provides no Moroccan-curriculum grounding. A system evaluated only on Jordanian and Egyptian history framing may produce non-Moroccan answers to Moroccan historical questions.
- **Datapoint citations:**
  - [D5] Law (Professional), IDs 4824/4843/4880/4881/4652, Morocco: All five Morocco-sourced samples are procedural law items — none are from history, geography, or school-level curricula
  - [D4] Civics (Middle School), IDs 14291–14327, Jordan: All five civics MS items are Jordan-only — confirms Morocco's absence from this high-priority subject category

#### MAJOR Concern 7: Islamic Studies content assumes internal Muslim religious perspective, not external educational framing
- **Dimension(s):** IC, OC
- **Observation:** The Islamic Studies questions (at all levels) are framed as internal religious knowledge questions — asking about the number of Prophet Muhammad's Umrah pilgrimages, which Quranic surah contains specific stories, and prescribed Islamic ritual practice. The Arabic Language (General) config uses a reading passage that frames Islamic purification practices prescriptively ("لا يمكن أنْ يصلي المسلم بدون وضوء"). These are presented as school-curriculum content for Muslim students, not as culturally informative questions for non-Muslim visitors.
- **Deployment relevance:** The deployment's target population are non-native, non-Arab tourists and expats, many of whom may be non-Muslim. A system evaluated on these items is tested for its ability to reproduce internal Islamic religious knowledge, not for its ability to explain Islamic practices to a non-Muslim visitor in an appropriately explanatory, non-prescriptive register. The benchmark cannot evaluate whether the system frames Islamic content accessibly for outsiders.
- **Datapoint citations:**
  - [D14] Islamic Studies (General), ID 46, null, label=A: "كم مرة اعتمر النبي صلى الله عليه وسلم؟ أربع عمرات" — Internal Islamic knowledge question presupposing Muslim reader
  - [D35] Arabic Language (General), ID 12069, null, label=B: "لا يمكن أنْ يصلي المسلم [فراغ]: بدون وضوء" — Reading passage frames Islamic ritual as prescriptive instruction ("the Muslim cannot pray without wudu") rather than descriptive/educational
  - [D31] Islamic Studies (High School), ID 14064, Jordan, label=E: "للتفكير آثار إيجابية عدة: جميع ما ذكر" — Islamic studies HS question framing positive thinking within Islamic value framework

#### MINOR

#### MINOR Concern 8: Driving Test questions are out-of-scope for school-curriculum knowledge deployment
- **Dimension(s):** IO
- **Observation:** The Driving Test config includes questions about traffic rules, road safety, and vehicle operation from Egypt, UAE, and Lebanon. These are practical regulatory knowledge items, not school-curriculum knowledge about Arab history, geography, or language.
- **Deployment relevance:** The deployment explicitly scopes to "school-curriculum-level general knowledge (history, geography, Arabic language)" with practical travel knowledge explicitly out of scope. Driving test performance scores are not informative for the tourist knowledge-assistant use case, and including this config in aggregate scoring could dilute or mislead benchmark-to-deployment mapping.
- **Datapoint citations:**
  - [D26] Driving Test, ID 687, UAE, label=A: "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر من مركبتك" — Practical traffic safety rule, not school-curriculum knowledge
  - [D26] Driving Test, ID 1025, Lebanon, label=C: "يُحَظَّر على سائق المركبة: يجري مناورة عكس الإتجاه (Demi Tour) وسط الطريق العام" — Note "Demi Tour" (French term) embedded in Arabic text — reflects Lebanon's French-influenced regulatory register

#### MINOR Concern 9: Some General Knowledge items cover vocational and institutional knowledge irrelevant to tourist context
- **Dimension(s):** IO
- **Observation:** General Knowledge (Primary) and General Knowledge (Middle School) samples include items about sheet metal screws, metal welding, Jordanian Royal Medical Services hospital names, and road safety. These are Jordanian school curriculum items that have no relevance to a tourist or expat seeking knowledge about Arab history and culture.
- **Deployment relevance:** These items contribute to benchmark scores but do not test the specific knowledge domains (history, geography, Arabic language) the deployment targets. High performance on vocational GK does not predict performance on culturally relevant questions.
- **Datapoint citations:**
  - [D27] General Knowledge (Primary School), ID 4381, Jordan, label=B: "برغي سن الصاج هو: مسمار لولبي الشكل مسلوب من نهايته" — Sheet metal screw definition — vocational, not culturally relevant
  - [D10] Social Science (Primary School), ID 5489, Jordan, label=D: "تشمل الخدمات الطبية الملكية الحكومية... مستشفى المدينة الطبية" — Jordanian Royal Medical Services hospitals — Jordan-institutional, not pan-Arab knowledge

#### MINOR Concern 10: One Arabic Language Grammar question has an English question stem
- **Dimension(s):** IF
- **Observation:** In Arabic Language (Grammar), example ID 12626, the question stem is in English: "In the following Quranic verse, what is the correct parsing of the word ـكَ" — while the answer options are in Arabic. This is an unexpected language mix in a benchmark that claims to be exclusively in MSA Arabic (excluding English questions by design).
- **Deployment relevance:** This is a minor data quality observation. The question is answerable in Arabic, but the English stem creates an inconsistency in the input form distribution. For a system tested on purely Arabic inputs, this question introduces a signal that may not represent the benchmark's intended register.
- **Datapoint citations:**
  - [D16] Arabic Language (Grammar), ID 12626, null, label=A: "In the following Quranic verse, what is the correct parsing of the word ـكَ: مضاف إليه مجرور وعلامة جره الكسرة" — English question stem with Arabic answer options; unexpected language mixing

#### MINOR Concern 11: Some Geography items ask about global (non-Arab) facts, reducing regional specificity
- **Dimension(s):** IC
- **Observation:** Several Geography items ask about non-Arab global knowledge: Mt. Kilimanjaro in Tanzania, Shanghai as an industrial smog city, the height of the snow line in equatorial regions, cold ocean currents (West Australia Current). While legitimate world geography content, these do not test Arabic/Arab-regional knowledge specifically.
- **Deployment relevance:** For the deployment's focus on "Arab history and geography," these items have lower diagnostic relevance. However, they do represent the type of factual geography knowledge a tourist might ask about.
- **Datapoint citations:**
  - [D] Geography (High School), ID 8189, Jordan, label=B: "يبلغ ارتفاع جبل كلمنجارو في تنزانيا: 5800 م" — Kilimanjaro altitude — global geography, not Arab-specific
  - [D] Geography (High School), ID 8216, Jordan, label=A: "من المدن الصناعية التي يتكون فيها الضباب الدخاني: شنغهاي" — Industrial smog cities — Shanghai as answer, global content

---

### Content Coverage Summary

The sampled data reveals a benchmark that is predominantly Jordanian in its civics and history domains (all 10 sampled civics items across middle and high school are Jordan-only), moderately represented by Egypt (university-level accounting, economics, political science, philosophy), and more lightly populated by Palestine (strong STEM presence at primary-high school level but minimal contested-history items in the sample), KSA (university STEM), Morocco (professional law only), and Lebanon (driving test). No Kuwait-sourced items appear in any sampled config.

The register is consistently MSA — formal written Arabic appropriate for school examinations — with occasional OCR-corruption artifacts particularly in Egyptian university-level items. One grammar item has an English question stem. The content divides roughly into: (a) culturally neutral STEM items (biology, physics, chemistry, math, computer science) sourced mainly from Jordan and Palestine; (b) Jordanian-centric civic and historical items; (c) pan-Islamic religious knowledge items (Islamic Studies across all levels, pan-Islamic Arabic Language reading texts); (d) Jordanian vocational and institutional items (driving, school tracking, hospital names); and (e) a small Moroccan professional law cluster.

For the deployment's school-curriculum tourist knowledge use case, the most relevant content is in History, Geography, Islamic Studies, Arabic Language, and Social Science. Of these, History and Civics are heavily Jordanian-framed, Geography includes both Jordan-specific and world-geography content, and Islamic Studies presents religious practice as internal knowledge rather than cultural explanation. The Arabic Language configs are well-suited to testing MSA grammar and vocabulary in an educational register.

---

### Limitations

1. **Sample size per config**: Only 5–8 examples per config were available. Some patterns (e.g., complete absence of Kuwait, Morocco's concentration in Law) may be sample artifacts rather than true distributional properties, though they are corroborated by the web search findings.

2. **Country field reliability**: A meaningful number of examples have Country=null (especially in Islamic Studies (General), Natural Science, Physics, Social Science Middle School, and Arabic Language configs). It is not possible from the sample to determine whether null-country items are truly country-agnostic (pan-Arab) or reflect metadata collection gaps.

3. **Contested content not reliably identifiable from MCQ alone**: The most critical deployment concern — whether contested historical questions have ground-truth labels that reflect one national perspective — cannot be fully verified by reading MCQ text alone. Deeper subject-matter analysis by area experts in Palestinian, Moroccan, and pan-Arab historiography would be needed.

4. **Inter-config quality variation**: OCR quality appears to vary substantially across sources. The university-level Egyptian social science items show severe digitization artifacts not visible in primary and middle school Jordanian items. The proportion of corrupted items across the full 14,575-question dataset cannot be estimated from this sample.

5. **Kuwait absence**: The inference that Kuwait is absent or minimally present is based on zero appearances in ~210 sampled examples and the absence from named country lists in the paper. This cannot be ruled out as a sampling artifact without examining the full dataset metadata.

6. **Islamic Studies register analysis**: Whether the Islamic Studies content is presented in an internal-community vs. external-educational register is a judgment call requiring expert review; the sample provides suggestive evidence but not a definitive audit.