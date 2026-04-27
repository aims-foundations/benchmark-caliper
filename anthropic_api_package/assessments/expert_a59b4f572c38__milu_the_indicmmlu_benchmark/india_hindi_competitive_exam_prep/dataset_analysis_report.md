## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Hindi configuration)
**Analysis date:** 2025-01-31
**Examples reviewed:** 245 from `validation` split
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Dimension |
|----|---------|-----------|-------|---------|-----------|
| D1 | MILU/Hindi | All 245 | is_translated=True | Every single example in the 245-item sample has `is_translated: True` | IC |
| D2 | MILU/Hindi | Ex.69 | option2 (Chemistry) | "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल / (b) केवल / (c) केवल" — options reference unlisted items (a)(b)(c) | IC/IF |
| D3 | MILU/Hindi | Ex.86 | option2 (Sociology) | "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C और E / केवल A, B, D और E" — options reference state list not present in question | IC/IF |
| D4 | MILU/Hindi | Ex.56 | option2 (Chemistry) | "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें... (1) और (2) केवल" — numbered statements absent from question text | IC/IF |
| D5 | MILU/Hindi | Ex.94 | option4 (Chemistry) | "निम्नलिखित में से कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d / केवल b, c" — lettered reactions not shown | IC/IF |
| D6 | MILU/Hindi | Ex.95 | option1 (Sports) | "विकल्प चुनें जो वाक्यों B, C, D और E को एक तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं" — sentences B-F completely absent | IC/IF |
| D7 | MILU/Hindi | Ex.106 | option2 (Chemistry) | "निम्नलिखित पदार्थों को...कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4 / 4 2 3 1" — numbered substances not named in question | IC/IF |
| D8 | MILU/Hindi | Ex.110 | option4 (Agriculture) | "राष्ट्रीय खाद्य सुरक्षा मिशन... (a) राष्ट्रीय खाद्य सुरक्षा मिशन एक फसल विकास योजना है। (b)..." — this item actually includes statements, appears intact | IF |
| D9 | MILU/Hindi | Ex.135 | option3 (Politics) | Option 4 reads "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" — option4 is a meta-instruction, not an answer | IF |
| D10 | MILU/Hindi | Ex.137 | option4 (Politics) | "ग्राम सभा क्या है: (ख) और (ग) केवल / (ग) और (घ) केवल" — options reference lettered list absent from question | IC/IF |
| D11 | MILU/Hindi | Ex.118 | option2 (Language) | "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें" — no idiom/मुहावरा is given in the question text | IC/IF |
| D12 | MILU/Hindi | Ex.152 | option1 (Language) | "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए सबसे उपयुक्त विकल्प चुनें" — no sentence or underlined portion present | IC/IF |
| D13 | MILU/Hindi | Ex.151 | option1 (Economics) | "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं... कौन सा तर्क मजबूत है?" — statement and arguments completely missing | IC/IF |
| D14 | MILU/Hindi | Ex.143 | option4 (Logical Reasoning) | "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करें: 3,1,5,2,4 / 5,2,3,1,4" — words to order are absent | IC/IF |
| D15 | MILU/Hindi | Ex.145 | option2 (Logical Reasoning) | "कौन सा अक्षर समूह प्रश्न चिह्न (?) को बदलकर दी गई श्रृंखला को पूरा करेगा?" — no series is provided | IC/IF |
| D16 | MILU/Hindi | Ex.188 | option3 (Education) | "नई शिक्षा नीति 2020 में देखा गया है कि... निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b) / उपरोक्त सभी" — problems (a)(b) not listed | IC/IF |
| D17 | MILU/Hindi | Ex.201 | option4 (Computer Science) | "निम्नलिखित में से कौन सा कथन BIOS के संदर्भ में सही है? केवल I और II / केवल I और III / सभी कथन सही हैं" — statements I, II, III absent | IC/IF |
| D18 | MILU/Hindi | Ex.222 | option2 (Business) | "2022 में फॉर्च्यून 500 सूची में भारतीय कंपनियों के संबंध में निम्नलिखित पर विचार करें: A, B, C और D केवल" — items A-E not enumerated | IC/IF |
| D19 | MILU/Hindi | Ex.7 | option2 (Literature) | "विलियम वर्ड्सवर्थ _________ के कवि हैं" — tests knowledge of English poet; India-relevance absent | IC |
| D20 | MILU/Hindi | Ex.76 | option2 (Language) | "निर्देश: 'डिडैक्टिक' शब्द का अर्थ क्या है?" — English word 'Didactic' asked in Hindi; tests English vocabulary | IC |
| D21 | MILU/Hindi | Ex.90 | option3 (Language) | "शब्द 'grim' का पर्यायवाची लिखें" — English word 'grim' asked in Hindi question | IC |
| D22 | MILU/Hindi | Ex.105 | option4 (Language) | "निर्देश: निम्नलिखित प्रश्न में... शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize" — English word tested in Hindi | IC |
| D23 | MILU/Hindi | Ex.9 | option3 (Language Studies) | "दिए गए वाक्य का सही अप्रत्यक्ष रूप चुनें। प्रबंधक ने अपने सहायक से कहा..." — tests Hindi grammar (indirect speech) directly relevant to deployment | IC/IO |
| D24 | MILU/Hindi | Ex.51 | option2 (Language Studies) | "दिए गए वाक्य का सही सक्रिय रूप चुनें" — active/passive voice in Hindi | IO |
| D25 | MILU/Hindi | Ex.74 | option4 (Economics) | "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी? 7.1 प्रतिशत" — specific historical data point (2018) | OC |
| D26 | MILU/Hindi | Ex.2 | option2 (Sports) | "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022 स्टेज 2 अभियान में भारत ने कितने स्वर्ण पदक जीते?" | OC |
| D27 | MILU/Hindi | Ex.88 | option1 (Physics) | "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान एक क्षुद्रग्रह पर उतरा... रयुगु" | OC |
| D28 | MILU/Hindi | Ex.242 | option4 (Arts) | "______ उत्तर प्रदेश के महत्वपूर्ण शिल्पों में से एक है... चिकनकारी" — UP-specific cultural craft content | IC |
| D29 | MILU/Hindi | Ex.26 | option2 (Earth Sciences) | "निम्नलिखित में से कौन सा खनिज उत्तर प्रदेश में नहीं पाया जाता है?" — UP-specific geography content | IC |
| D30 | MILU/Hindi | Ex.68 | option2 (Geography) | "राजस्थान के किस जिले में 'बज्जू' आरक्षित क्षेत्र स्थित है?" — Rajasthan state-level content | IC |
| D31 | MILU/Hindi | Ex.193 | option3 (Arts) | "कोटा के शासक के किस काल को कोटा चित्रकला स्कूल के लिए उत्कृष्ट काल माना जाता है?" — Rajasthan state-level cultural content | IC |
| D32 | MILU/Hindi | Ex.115 | option4 (Literature) | "'किस्सा किस्सा लखनऊवा-लखनऊ के आवामी किस्से' के लिए साहित्य अकादमी युवा पुरस्कार 2021" — UP/Lucknow literary content | IC |
| D33 | MILU/Hindi | Ex.28 | option2 (Sociology) | "खेरवार आंदोलन के नेता — भागीरथ मांझी" — Jharkhand/tribal movement, less central-exam prominent | IC |
| D34 | MILU/Hindi | Ex.83 | option1 (Sociology) | Complex ethics scenario about senior civil officer, tribal displacement, old-age home; very long UPSC-style case | IO |
| D35 | MILU/Hindi | Ex.170 | option2 (Business) | "कपड़ा दुकान के मालिक ने क्या खरीदा? कैलकुलेटर" — decontextualized; passage/context missing | IC/IF |
| D36 | MILU/Hindi | Ex.36 | option3 (Logical Reasoning) | "TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______" — letter series with Roman characters in Hindi question | IC |
| D37 | MILU/Hindi | Ex.52 | option2 (History) | "सुंदर पांड्यन — पांड्य साम्राज्य को कावेरी तक संगठित और विस्तारित किया" — South Indian dynasty, less prominent in UPSC Hindi prep | IC |
| D38 | MILU/Hindi | Ex.109 | option4 (Politics) | "छत्तीसगढ़ में नगरपालिकाओं के सभी चुनावों के संचालन के लिए... अनुच्छेद 243 (ख)..." — state-specific (Chhattisgarh) content | IC |
| D39 | MILU/Hindi | Ex.200 | option4 | Correct answer for "पितृसत्तात्मक परिवार" labels patriarchal family; accepted factual answer | OC |

---

### Findings

#### CRITICAL

#### Finding CRITICAL1: Systematic Missing Content in Translated Items — Questions Reference Absent Lists, Statements, and Passages

- **Dimension(s):** IC, IF
- **Observation:** A substantial minority of the 245 sampled items (approximately 15–20 items identified) contain questions that explicitly instruct the model/student to evaluate "the following statements," "the following items (a, b, c, d)," "the given sentence," or "the given idiom" — but the referenced content is entirely absent from the question field. The answer options reference these missing elements (e.g., "केवल A और B," "केवल 1 और 3," "AEDBCF"). This renders the items unanswerable without the original source material, and a model's correct response would be chance-level or based on residual training knowledge rather than the provided content. This pattern appears across multiple subjects including Chemistry, Sociology, Language Studies, Logical Reasoning, Computer Science, and Economics.
- **Potential concern for deployment:** For a system evaluating Hindi-medium students preparing for central competitive exams, these items represent a fundamental data integrity failure. If a model "correctly" answers these questions, it demonstrates memorization of the answer from training data rather than reasoning from presented content — precisely the behavior this benchmark cannot differentiate. Benchmark accuracy scores on these items are not interpretable, inflating or deflating performance measures for the deployment use case in a non-reproducible way.
- **Datapoint citations:**
  - [D2] Example 69 (MILU/Hindi, split=validation, label=option2, Chemistry): "निम्नलिखित में से कौन सा एक शुद्ध पदार्थ है? (a) केवल / (b) केवल / (c) केवल" — options reference items (a)(b)(c) not present in question.
  - [D3] Example 86 (MILU/Hindi, split=validation, label=option2, Sociology): "भारत में सभी बहुआयामी गरीब व्यक्तियों में से आधे से अधिक निम्नलिखित राज्यों में रहते हैं: केवल A, B, C और E" — states A–E never enumerated.
  - [D4] Example 56 (MILU/Hindi, split=validation, label=option2, Chemistry): "एथेनॉल के बारे में दिए गए चार कथनों पर विचार करें... (1) और (2) केवल" — four statements entirely absent.
  - [D5] Example 94 (MILU/Hindi, split=validation, label=option4, Chemistry): "कौन सी ऑक्सीकरण-अपचयन प्रतिक्रियाएँ हैं? केवल a, d" — reactions a–d not shown.
  - [D6] Example 95 (MILU/Hindi, split=validation, label=option1, Sports): "वाक्यों B, C, D और E को तार्किक क्रम में व्यवस्थित करता है। वाक्य A और F स्थिर हैं" — sentences B–F entirely absent.
  - [D7] Example 106 (MILU/Hindi, split=validation, label=option2, Chemistry): "निम्नलिखित पदार्थों को कालानुक्रमिक क्रम में व्यवस्थित करें: 1 2 3 4 / 4 2 3 1" — substances 1–4 unnamed.
  - [D10] Example 137 (MILU/Hindi, split=validation, label=option4, Politics): "ग्राम सभा क्या है: (ख) और (ग) केवल / (ग) और (घ) केवल" — definitions (क)(ख)(ग)(घ) absent.
  - [D11] Example 118 (MILU/Hindi, split=validation, label=option2, Language): "दिए गए मुहावरे का सबसे उपयुक्त अर्थ चुनें" — no idiom appears in question.
  - [D12] Example 152 (MILU/Hindi, split=validation, label=option1, Language): "दिए गए वाक्य में रेखांकित खंड को बदलने के लिए..." — no sentence provided.
  - [D13] Example 151 (MILU/Hindi, split=validation, label=option1, Economics): "नीचे दिए गए कथन के बाद दो तर्क I और II दिए गए हैं... कौन सा तर्क मजबूत है?" — statement and arguments not present.
  - [D14] Example 143 (MILU/Hindi, split=validation, label=option4, Logical Reasoning): "निम्नलिखित शब्दों को तार्किक और अर्थपूर्ण क्रम में व्यवस्थित करें" — words to order absent.
  - [D15] Example 145 (MILU/Hindi, split=validation, label=option2, Logical Reasoning): "कौन सा अक्षर समूह...दी गई श्रृंखला को पूरा करेगा?" — series not provided.
  - [D16] Example 188 (MILU/Hindi, split=validation, label=option3, Education): "निम्नलिखित में से किन समस्याओं का सामना कर रही है? केवल (a) / केवल (b)" — problems (a)(b) not listed.
  - [D17] Example 201 (MILU/Hindi, split=validation, label=option4, Computer Science): "BIOS के संदर्भ में सही है? केवल I और II" — statements I, II, III absent.
  - [D18] Example 222 (MILU/Hindi, split=validation, label=option2, Business): "फॉर्च्यून 500 सूची में... A, B, C और D केवल" — items A–E not enumerated.

---

#### Finding CRITICAL2: Option-as-Meta-Instruction Format Corruption

- **Dimension(s):** IF, OC
- **Observation:** At least one item has an answer option that is a meta-instruction rather than a substantive answer choice. Example 135, option4 reads "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" ("Select the correct answer using the code given below") — this is a formatting artifact from a multi-step MCQ format (common in UPSC Prelims) where the original question provided a numbered code table, but the code table has been stripped during dataset processing. The correct answer is option3, meaning a student must choose from options that include one non-answer.
- **Potential concern for deployment:** This indicates systematic stripping of table/code structures during competitive exam scraping and dataset formatting. For central-exam competitive preparation (UPSC GS Paper I heavily uses "which of the following statements is/are correct?" with code tables), this format corruption is particularly consequential: the exact item types most representative of UPSC Prelims are the ones most likely to be corrupt in this dataset.
- **Datapoint citations:**
  - [D9] Example 135 (MILU/Hindi, split=validation, label=option3, Politics and Governance): Option4 = "नीचे दिए गए कोड का उपयोग करके सही उत्तर चुनें" — a formatting directive appearing as an answer choice, indicating the code table (1/2 only, 2/3 only, etc.) was stripped.

---

#### MAJOR

#### Finding MAJOR1: 100% of Sampled Validation Items Are Machine-Translated from English

- **Dimension(s):** IC, IF
- **Observation:** Every single one of the 245 sampled validation examples carries `is_translated: True`. The benchmark documentation states that only ~25% of released questions are translated, and the remainder are natively sourced. However, the entire validation split sample reviewed here is 100% translated. This is either a property of the validation split specifically (which may have been populated disproportionately with translated items) or a sampling artifact. Either way, any few-shot evaluation using this validation set as the source of in-context examples will expose models exclusively to translated content as exemplars.
- **Potential concern for deployment:** For Hindi-medium competitive exam students, the register and phrasing of natively sourced Hindi exam questions differs substantially from machine-translated content. If few-shot examples are drawn from this validation split (as documented in Q51), models are being primed with translated Hindi that may not reflect the register of actual competitive exam question language. This is a potential construct-irrelevant variance source for deployment evaluation.
- **Datapoint citations:**
  - [D1] All 245 examples (MILU/Hindi, split=validation): `is_translated: True` — 245/245 items in sample are translated from English; no natively sourced Hindi validation items appear in this sample.

---

#### Finding MAJOR2: English Vocabulary Testing Within Hindi Language Studies Items — Exceeds 10% Code-Mixing Threshold

- **Dimension(s):** IC
- **Observation:** Several Language Studies items in the Hindi configuration test vocabulary knowledge of English words directly, asking Hindi-medium students to define English terms like "Didactic," "grim," and "Evangelize." These are not technical terms with standard Hindi equivalents but English literary/rhetorical vocabulary. Additionally, Logical Reasoning items use Roman-alphabet letter sequences (e.g., "TAB, TTZBB, TTBBB..." in Example 36) embedded in Hindi text. While some code-mixing with English technical terms is acceptable per the deployment specification (~10% ceiling), items that require knowledge of English literary vocabulary as the *core* assessment construct go beyond incidental code-mixing.
- **Potential concern for deployment:** Hindi-medium competitive exam aspirants preparing for UPSC/SSC are assessed on Hindi language proficiency (Hindi grammar, idiom, comprehension) not English vocabulary recognition. Items testing "Didactic," "grim," or "Evangelize" definitions create construct-irrelevant difficulty for this population: failure represents English vocabulary deficit, not Hindi language knowledge deficit. This is a direct IC validity concern for the target student population.
- **Datapoint citations:**
  - [D20] Example 76 (MILU/Hindi, split=validation, label=option2, Language Studies): "'डिडैक्टिक' शब्द का अर्थ क्या है? / नैतिक पाठ पढ़ाना" — English word 'Didactic' is the core test construct.
  - [D21] Example 90 (MILU/Hindi, split=validation, label=option3, Language Studies): "शब्द 'grim' का पर्यायवाची लिखें" — 'grim' is an English word; the question tests English synonym knowledge.
  - [D22] Example 105 (MILU/Hindi, split=validation, label=option4, Language Studies): "शब्द का अर्थ सबसे अच्छी तरह व्यक्त करता है... Evangelize / उपदेश देना" — English word tested.
  - [D36] Example 36 (MILU/Hindi, split=validation, label=option3, Logical Reasoning): "TAB, TTZBB, TTBBB, TTTYBBB, TTTCBBB, _______" — Roman letter series embedded in Hindi question.

---

#### Finding MAJOR3: Output Ontology Fundamental Mismatch — MCQ Label Scoring Cannot Validate Hindi Explanatory Rationale

- **Dimension(s):** OO, OF
- **Observation:** All 245 sampled items follow the MCQ format with a single correct answer and `target` field specifying one of four options. The benchmark provides no rationale, explanation, or annotation of *why* an answer is correct. The deployment requires the AI system to return both a correct/incorrect label *and* a substantive Hindi-language explanation of why the answer is right or wrong.
- **Potential concern for deployment:** MILU benchmark accuracy scores measure only label selection correctness, not explanation quality. A model that achieves high accuracy on MILU MCQs may generate factually incorrect, incoherent, or pedagogically unhelpful Hindi explanations for the same questions. This is a fundamental output form mismatch: benchmark scores cannot be used to validate the deployment's core output, and no proxy measure for explanation quality exists within the benchmark infrastructure. This was anticipated in documentation but the sampled data confirms there is zero annotation supporting rationale assessment.
- **Datapoint citations:**
  - [D2]–[D18]: All examples — none contain a rationale field, explanation, or annotation of reasoning. The `target` field specifies only which option letter is correct. For instance, Example 83 [D34] presents a complex multi-paragraph civil services ethics scenario whose correct answer (option1) requires nuanced reasoning about tribal rights and official duties, yet no explanation is provided in the dataset.

---

#### Finding MAJOR4: Current Affairs Items Are Temporally Dated — Knowledge Currency Risk for Central Exam Deployment

- **Dimension(s):** OC
- **Observation:** Multiple Current Affairs and GK items reference specific events from 2018–2022 that are time-bound fact questions. Examples include India's GDP growth rate for July–September 2018 (Ex.74), the 2020 Archery Asia Cup gold medals won by India (Ex.2), the 2019 Japanese asteroid mission Ryugu (Ex.88), the 2020 Minister of Women and Child Development (Ex.132 — as of 2018), and the 2022 ASSOCHAM President (Ex.123 — December 2020). For a deployment targeting students preparing for current UPSC/SSC exams (2024–2026), questions testing 2018–2022 Current Affairs have limited validity for the "Current Affairs" domain.
- **Potential concern for deployment:** Current Affairs is a top-priority domain for UPSC/SSC/banking exam preparation. Students preparing for 2025–2026 exams need current knowledge; a benchmark evaluating 2018–2022 events cannot validly measure Current Affairs preparedness for the deployment cohort. Model performance on these items may also be inflated due to training data contamination (these events were well-covered in pre-training corpora).
- **Datapoint citations:**
  - [D25] Example 74 (MILU/Hindi, split=validation, label=option4, Economics): "जुलाई-सितंबर 2018 तिमाही के दौरान भारत की GDP की वृद्धि दर क्या थी? 7.1 प्रतिशत" — 2018 economic data.
  - [D26] Example 2 (MILU/Hindi, split=validation, label=option2, Sports): "मई 2022 में इराक के सुलेमानिया में आयोजित तीरंदाजी एशिया कप 2022..." — 2022 sports event.
  - [D27] Example 88 (MILU/Hindi, split=validation, label=option1, Physics): "जुलाई 2019 में, जापान की अंतरिक्ष एजेंसी का एक अंतरिक्ष यान... रयुगु" — 2019 space event.

---

#### Finding MAJOR5: Subject Distribution Skewed Toward Engineering/Technology — Mismatch With Central Exam Priority Subjects

- **Dimension(s):** IO
- **Observation:** Among the 245 sampled validation items, there is a notably high concentration of Engineering & Technology domain items (approximately 45–50 items, roughly 18–20% of the sample). These cover topics like DC motor behavior (Ex.1), Half-Wave Rectifiers (Ex.3), Transformer types (Ex.4), AM modulation bandwidth (Ex.16), TDM frame rates (Ex.47), and chopper circuits (Ex.160). Engineering and technical content of this specificity is not tested in UPSC Prelims, SSC CGL, or banking exams. By contrast, Mathematics/Quantitative Aptitude — a top-priority subject for SSC and banking exams — appears to have very limited representation (only the compound interest problem Ex.84 and the weighted average Ex.120 are clearly quantitative aptitude items).
- **Potential concern for deployment:** The deployment targets UPSC, SSC, and banking exam preparation. For SSC CGL and IBPS PO, Quantitative Aptitude is a major paper; for UPSC, General Science (not advanced engineering) is tested. The overrepresentation of advanced Engineering content and underrepresentation of Mathematics/Quantitative Aptitude in this sample suggests the Hindi MILU subset may not adequately cover the most critical subject areas for the central exam deployment.
- **Datapoint citations:**
  - [D2], [D3] above plus: Example 1 (DC series motor — Engineering), Example 3 (Half-wave rectifier — Engineering), Example 4 (Transformer type — Engineering), Example 16 (AM bandwidth — Technology), Example 38 (Form factor — Engineering), Example 47 (TDM frame rate — Technology), Example 49 (Ampere's law — Physics/Engineering), Example 160 (Chopper circuit — Engineering) — approximately 18–20% of sample is advanced Engineering/Technology content not tested in UPSC/SSC/banking exams.
  - [D34] Example 83 (Sociology — Ethics case): Complex civil services ethics scenario; UPSC-style but appears only once in sample vs. numerous engineering items.

---

#### MINOR

#### Finding MINOR1: South India–Specific Content Present in Hindi-Language Items

- **Dimension(s):** IC
- **Observation:** Several items in the Hindi configuration specifically test knowledge of South Indian states, dynasties, cultural works, or current affairs not typically emphasized in central exam preparation from a North Indian Hindi-medium perspective. Examples include: the Pandya king who extended the empire to the Kaveri (Ex.52), Tamil magazine cartoon history (Ex.108), the classical Tamil epic "Silappatikaram" (Ex.232), Kota painting school period (Ex.193 — Rajasthan, North India-relevant), and Bhanda Pather theater of J&K (Ex.48). While some such items appear in UPSC GS, the framing and depth suggest sourcing from South Indian or regional state-level exams.
- **Potential concern for deployment:** Hindi-medium students from North India preparing for central exams would encounter UPSC-standard questions about South India, but questions with very fine-grained knowledge about South Indian literary/historical figures (Sundar Pandyan, Tamil epic authorship, Tamil magazine cartoons) may reflect South Indian regional exam content rather than central exam scope. This is a moderate concern for content validity.
- **Datapoint citations:**
  - [D37] Example 52 (MILU/Hindi, split=validation, label=option2, History):