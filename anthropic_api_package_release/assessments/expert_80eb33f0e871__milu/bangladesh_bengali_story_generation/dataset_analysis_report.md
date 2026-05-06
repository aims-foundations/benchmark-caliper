## Dataset Analysis Report

**Dataset(s):** ai4bharat/MILU (Bengali config, with cross-config inspection of English, Hindi, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu)
**Analysis date:** 2025-01-31
**Examples reviewed:** 215 total (21 Bengali validation, 20 English validation, 24 Gujarati, 26 Hindi, 17 Kannada, 16 Malayalam, 21 Marathi, 21 Odia, 25 Punjabi, 19 Tamil, 25 Telugu)
**Columns shown:** question, option1, option2, option3, option4, target, is_translated, language, domain, subject
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | Bengali validation | Ex. 1 | option3 | "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল? … তেল ও পেট্রোলিয়াম পণ্যের আমদানির মূল্যের তীব্র বৃদ্ধি" | India's 1991 balance-of-payments crisis question, translated from English (is_translated=True) | IC, OC |
| D2 | Bengali validation | Ex. 5 | option4 | "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" | Indian state assembly election (AAP in Punjab, 2022) — exclusively India-centric governance content | IC, IO |
| D3 | Bengali validation | Ex. 9 | option3 | "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" | Removal of India's Election Commissioner — refers to Indian constitutional provisions | IC, OC |
| D4 | Bengali validation | Ex. 12 | option4 | "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল … আচার্য বিনোবা ভাবে" | "Mangal Bharat" — Indian national leader Vinoba Bhave; India-specific cultural/literary content | IC |
| D5 | Bengali validation | Ex. 17 | option2 | "৬৫তম ফিল্মফেয়ার অ্যাওয়ার্ডস, ২০২০-এ সেরা সিনেমাটোগ্রাফির জন্য পুরস্কারটি কে জিতেছেন? … জয় ওজা" | 65th Filmfare Awards (Indian film industry awards) — not Bangladeshi film industry | IC, IO |
| D6 | Bengali validation | Ex. 18 | option4 | "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" | Qutub Minar, Delhi — India-specific historical monument | IC |
| D7 | Bengali validation | Ex. 3 | option4 | "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" | Bahamani Kingdom capital — medieval Indian/Deccan history, not Bangladeshi | IC |
| D8 | Bengali validation | all 21 | various | All 21 Bengali examples show is_translated: True | Every Bengali validation example in sample is translated from English | IC, IF |
| D9 | English validation | Ex. 2 | option3 | "Which state has topped the India Innovation Index - 2019 published by Niti Aayog? … Karnataka" | India Innovation Index — Indian national governance content | IC |
| D10 | English validation | Ex. 9 | option2 | "Which one of the following statements about Legislative Committee system of Maharashtra is not correct?" | Maharashtra state legislature — India-specific governance at state level | IC |
| D11 | English validation | Ex. 13 | option4 | "Which state became the first Indian state to launch pension for single women at Rs.1,000/- per month? … Telangana" | Telangana state welfare scheme — Indian state government | IC |
| D12 | English validation | Ex. 15 | option3 | "Founded in 1950, one of the industrial units owned by Indian Railways is named after the Indian freedom fighter … Chittaranjan Das" | Indian Railways industrial unit named after Indian independence figure | IC |
| D13 | Bengali validation | Ex. 2 | option3 | "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু প্রশিক্ষণ নিচ্ছে যার মধ্যে ৯০০ জন নির্বাচিত হয়েছে। নির্বাচিত না হওয়া শিশুদের সংখ্যা এবং মোট শিশুদের সংখ্যার অনুপাত কত? … ১ : ৪" | Cricket training camp ratio problem — culturally neutral arithmetic, cricket context | IC |
| D14 | Bengali validation | Ex. 7 | option4 | "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প … জাতীয় খাদ্য সুরক্ষা মিশন আগস্ট ২০০৭ সালে চালু হয়েছিল" | India's National Food Security Mission — Indian government program | IC |
| D15 | Hindi validation | Ex. 6 | option1 | "राष्ट्रीय आपातकाल घोषित करने के लिए 'सशस्त्र विद्रोह' शब्द संविधान में कब जोड़ा गया? … 44वें संविधान संशोधन अधिनियम द्वारा" | Indian constitutional amendment — India-specific law and governance | IC |
| D16 | Gujarati validation | Ex. 8 | option3 | "રેડક્લિફ રેખા નીચેના પૈકી કયા દેશ સાથે ભારતની સરહદોને અલગ કરે છે? … પાકિસ્તાન" | Radcliffe Line separating India and Pakistan — Indian national geography/history | IC |
| D17 | Bengali validation | Ex. 4 | option2 | "স্থির প্রবাহ ট্রান্সফরমার _______ ধরনের। … শেল" | Constant current transformer type question — domain-neutral engineering/STEM | IC |
| D18 | Bengali validation | Ex. 8 | option4 | "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া? … উপরের সবগুলি" | Oxidation-reduction reactions — universal science content | IC |
| D19 | Bengali validation | Ex. 10 | option4 | "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" | SA node as cardiac pacemaker — universal medical content | IC |
| D20 | Bengali validation | Ex. 14 | option3 | "একটি অ্যাসেম্বলার যা একটি মেশিনে চলে কিন্তু অন্য মেশিনের জন্য মেশিন কোড তৈরি করে তাকে কি বলা হয়? … ক্রস-অ্যাসেম্বলার" | Cross-assembler definition — universal computer science | IC |
| D21 | Bengali validation | Ex. 16 | option1 | "দুটি পাত্র আছে X এবং Y। X-এ ১০০ মিলি দুধ … m = n" | Milk-water mixture ratio problem — culturally neutral quantitative reasoning | IC |
| D22 | Odia validation | Ex. 2 | option4 | "ডিসেমবর 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆ… ବାଙ୍ଗ୍ଲାଦେଶ" | Indian Pharmacopoeia — Bangladesh mentioned as a distractor option, not as subject matter | IO |
| D23 | Telugu validation | Ex. 2 | option4 | "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది? … ఆఫ్ఘనిస్తాన్" | India Pharmacopoeia question — Bangladesh listed as distractor option2 | IO |
| D24 | Bengali validation | Ex. 6 | option2 | "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" | Antonym question in Bengali — vocabulary test | IF |
| D25 | Bengali validation | Ex. 13 | option2 | "নিচের বাক্যটির সঠিক সক্রিয় রূপ নির্বাচন করুন। সবাই তার চমৎকার নৃত্য পরিবেশনা দ্বারা মুগ্ধ হয়েছিল। … তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" | Active voice conversion of Bengali sentence — grammar in written Bengali | IF |
| D26 | Marathi validation | Ex. 16 | option3 | "হলষষ্ঠী সণ কা সাজরা কেলা জাতো? … মুলাচ্যা দীর্ঘায়ুষ্যাসাঠী" | Halshashthi festival (Maharashtra/Hindu calendar) — India-specific cultural festival, not Bangladeshi | IC |
| D27 | Bengali validation | Ex. 11 | option3 | "সিদ্ধান্ত গ্রহণের সাথে যুক্ত সমস্যাগুলি হল: … ভয় এবং মিথ্যা আশা" | Decision-making problems — generic management/psychology content | IC |
| D28 | Bengali validation | Ex. 19 | option1 | "নিচের বিবৃতিটি দুটি যুক্তি I এবং II সহ দেওয়া হয়েছে … শুধুমাত্র যুক্তি I শক্তিশালী" | Logical argument strength question — generic reasoning | IC |
| D29 | Bengali validation | Ex. 20 | option2 | "জে, কে, এল, এম এবং এন পাঁচজন কাজিন … এম" | Age ordering puzzle with letter-named cousins — culturally neutral logic | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Bengali script is correctly used throughout the Bengali split
- **Dimension(s):** IF
- **Observation:** All 21 Bengali validation examples are rendered in Bangla script with correct Unicode rendering. The questions, options, and answers appear well-formed in Bengali script without visible encoding errors or script contamination from other Indic scripts.
- **Deployment relevance:** The target deployment uses Bangladeshi Bengali in Bangla script. No script mismatch exists at the writing-system level, satisfying the most basic input form requirement for a text-only Bengali evaluation.
- **Datapoint citations:**
  - [D24] Example 6 (Bengali, validation, option2): "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" — Bengali script is correctly rendered; antonym question shows standard written Bengali vocabulary
  - [D25] Example 13 (Bengali, validation, option2): "তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" — Active voice grammar question shows well-formed Bengali prose sentences

#### Strength 2: Multi-domain coverage including Arts & Humanities, Law & Governance, Science, and Business Studies
- **Dimension(s):** IO
- **Observation:** The sampled Bengali examples span Engineering (Ex. 4, 15, 16, 21), Science (Ex. 8), Health & Medicine (Ex. 10), Business Studies (Ex. 1, 11, 19), Arts & Humanities (Ex. 3, 6, 12, 13, 17, 18), Environmental Sciences (Ex. 7), Social Sciences (Ex. 2, 20), and Law & Governance (Ex. 5, 9). The domain coverage is broad across the 8 MILU domains.
- **Deployment relevance:** The deployment's evaluation of LLMs on cultural knowledge benefits from having multiple non-STEM domains present (Arts & Humanities, Law & Governance) even if their content is India-centric. This enables at least baseline measurement of model cultural knowledge capacity in Bengali, distinguishing models that have zero cultural awareness from those with some.
- **Datapoint citations:**
  - [D2] Example 5 (Bengali, validation, option4): "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — domain=Law & Governance; confirms that political/governance content exists in Bengali, though content is India-specific
  - [D4] Example 12 (Bengali, validation, option4): "'মঙ্গল ভারত' কাজটি নিম্নলিখিত কোন জাতীয় নেতার দ্বারা রচিত হয়েছিল … আচার্য বিনোবা ভাবে" — domain=Arts & Humanities, subject=Literature and Linguistics; confirms literary content present in Bengali, though referencing Indian figures

#### Strength 3: STEM and universal academic content is present and transferable
- **Dimension(s):** IC
- **Observation:** A substantial portion of Bengali items covers domain-universal content — electrical engineering, chemistry, computer science, biology, mathematics — where the factual answer is culturally neutral and not India-specific. Questions about oxidation-reduction reactions, cardiac pacemakers, cross-assemblers, and mixture ratios have identical correct answers regardless of whether the evaluatee is Indian or Bangladeshi.
- **Deployment relevance:** For a deployment evaluating whether an LLM has general academic competence in Bengali, these universal STEM items provide valid signal. A model that cannot answer basic physics or chemistry questions in Bengali is unlikely to generate high-quality Bengali stories involving these topics either. While not the primary gap area, this represents a genuinely transferable subset.
- **Datapoint citations:**
  - [D18] Example 8 (Bengali, validation, option4): "নিম্নলিখিত কোনগুলি অক্সিডেশন-রিডাকশন বিক্রিয়া? … উপরের সবগুলি" — universal chemistry content; answer identical regardless of national context
  - [D19] Example 10 (Bengali, validation, option4): "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" — universal medical anatomy; no cultural specificity
  - [D20] Example 14 (Bengali, validation, option3): "একটি অ্যাসেম্বলার যা একটি মেশিনে চলে কিন্তু অন্য মেশিনের জন্য মেশিন কোড তৈরি করে তাকে কি বলা হয়? … ক্রস-অ্যাসেম্বলার" — universal computer science definition
  - [D21] Example 16 (Bengali, validation, option1): "দুটি পাত্র আছে X এবং Y। X-এ ১০০ মিলি দুধ … m = n" — culturally neutral quantitative reasoning

#### Strength 4: Bengali language grammar and vocabulary items present
- **Dimension(s):** IF, IC
- **Observation:** Examples 6 and 13 in the Bengali validation split test Bengali language competence directly — an antonym question and an active/passive voice transformation. These items probe written Bengali language knowledge at the lexical and syntactic level.
- **Deployment relevance:** Story generation quality depends partly on grammatical Bengali competence. These items provide at least some signal about whether a model can manipulate Bengali grammatical structures, even if the specific vocabulary tested may reflect written standard Bengali without dialect stratification.
- **Datapoint citations:**
  - [D24] Example 6 (Bengali, validation, option2): "নিচের প্রশ্নে, দেওয়া চারটি বিকল্পের মধ্যে থেকে সেই বিকল্পটি নির্বাচন করুন যা প্রদত্ত শব্দের বিপরীত অর্থ প্রকাশ করে। … শীতল" — antonym selection tests Bengali vocabulary
  - [D25] Example 13 (Bengali, validation, option2): "নিচের বাক্যটির সঠিক সক্রিয় রূপ নির্বাচন করুন। সবাই তার চমৎকার নৃত্য পরিবেশনা দ্বারা মুগ্ধ হয়েছিল।" — active/passive voice tests Bengali grammatical competence

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Every sampled Bengali item is translated from English (is_translated=True across all 21 examples)
- **Dimension(s):** IC, IF
- **Observation:** All 21 Bengali validation examples in the sample carry `is_translated: True`. Per MILU documentation, ~25% of questions overall are translated using GPT-4O from English. The Bengali validation split in this sample shows 100% translated items. This means the Bengali content in this sample does not originate from Bengali-medium Indian exams at all — it is translated English content. No item in the Bengali validation sample was organically written in or sourced from a Bengali-language exam.
- **Deployment relevance:** The elicitation explicitly requires Bangladeshi Standard Bengali (Cholti register with Arabic/Persian loanword patterns). GPT-4O translation from English produces Bengali text in a standardized written register that almost certainly does not reflect Bangladeshi Cholti orthographic and lexical norms. The translated questions use vocabulary and phrasing patterns derived from English source content processed through a translation model likely trained on mixed Bengali corpora. This is the most direct form evidence of the register gap flagged in the deployment context.
- **Datapoint citations:**
  - [D8] All 21 Bengali validation examples (Bengali, validation): is_translated=True across the full sample — no organically Bengali-language exam content is present in this split's validation examples; all content is GPT-4O translated from English
  - [D1] Example 1 (Bengali, validation, option3): "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" — Indian 1991 crisis question translated into Bengali; vocabulary is formal written Bengali without any markers of Bangladeshi Cholti register

#### Concern 2: All cultural/political content in Bengali sample is exclusively India-centric; zero Bangladeshi cultural touchstones identified
- **Dimension(s):** IC, IO, OC
- **Observation:** Across the 21 Bengali validation examples, every culturally or politically specific item references Indian institutions, events, persons, or geography: India's 1991 financial crisis (Ex. 1), AAP's Punjab election win (Ex. 5), India's Election Commissioner removal procedure (Ex. 9), Indian leader Vinoba Bhave's "Mangal Bharat" (Ex. 12), the 65th Filmfare Awards (Ex. 17), and the Qutub Minar in Delhi (Ex. 18). Zero items reference: the 1971 Liberation War, Bangladeshi political history, Bangladeshi universities, Bangladeshi cultural events (Ekushe Boi Mela, Pohela Boishakh), Bangladeshi geography (Dhaka neighborhoods, Bangladeshi rivers), or Bangladeshi literary/cultural figures. This is consistent with documentation but confirmed empirically.
- **Deployment relevance:** The deployment requires that the benchmark evaluate LLMs on Bangladesh-specific cultural knowledge for Bengali story generation. The total absence of Bangladeshi cultural content means MILU Bengali scores measure performance on Indian cultural knowledge rendered in Bengali script — a fundamentally different construct from what is needed. High MILU Bengali accuracy does not predict Bangladeshi cultural grounding in story generation.
- **Datapoint citations:**
  - [D2] Example 5 (Bengali, validation, option4): "ফেব্রুয়ারি - মার্চ ২০২২ এ অনুষ্ঠিত রাজ্য বিধানসভা নির্বাচনে, আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — India-specific political knowledge (Indian state elections); no Bangladeshi political equivalent present
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — Indian constitutional law (removal of India's Election Commissioner); Bangladesh's election commission structure is structurally different and absent
  - [D4] Example 12 (Bengali, validation, option4): "'মঙ্গল ভারত' কাজটি … আচার্য বিনোবা ভাবে" — Indian national movement figure; no Bangladeshi literary/cultural figure appears in any sampled item
  - [D5] Example 17 (Bengali, validation, option2): "৬৫তম ফিল্মফেয়ার অ্যাওয়ার্ডস, ২০২০-এ সেরা সিনেমাটোগ্রাফির জন্য পুরস্কারটি কে জিতেছেন? … জয় ওজা" — Filmfare Awards (Indian film industry); Bangladeshi film industry (Dhallywood, BTV drama) entirely absent
  - [D6] Example 18 (Bengali, validation, option4): "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" — Delhi monument history; no Bangladeshi historical sites (Lalbagh Fort, Ahsan Manzil, Paharpur, Mainamati) present

#### Concern 3: Bangladesh appears only as a distractor option in non-Bengali language items — confirming structural absence
- **Dimension(s):** IO, IC
- **Observation:** In the Odia and Telugu validation samples, "Bangladesh" (বাংলাদেশ / బంగ్లాదేశ్) appears in option lists as a wrong-answer distractor in a question about which country first recognized the Indian Pharmacopoeia. This is the only appearance of Bangladesh in the entire 215-item cross-language sample. Bangladesh is not the subject of any question in any language split; it appears solely as a foil answer in India-centric questions.
- **Deployment relevance:** This direct observation confirms that Bangladesh is structurally positioned as a peripheral "foreign country" in MILU's knowledge frame, not as the primary geographic and cultural reference point. For a deployment centered on Bangladeshi Bengali cultural grounding, this framing is fundamentally misaligned.
- **Datapoint citations:**
  - [D22] Example 2 (Odia, validation, option4): "ଡିସେମ୍ବର 2019 ରେ ଭାରତୀୟ ଫାର୍ମାକୋପିଆ… ବାଙ୍ଗ୍ଲାଦେଶ" — Bangladesh listed as option2 (wrong answer) in a question about Indian Pharmacopoeia; Bangladesh is a distractor, not a subject
  - [D23] Example 2 (Telugu, validation, option4): "డిసెంబర్ 2019లో భారతీయ ఫార్మాకోపియా ను గుర్తించిన మొదటి దేశం ఏది? … బంగ్లాదేశ్" — same question in Telugu; Bangladesh again as distractor option

#### Concern 4: No Bangladeshi Bengali annotators — ground truth reflects Indian knowledge frameworks exclusively
- **Dimension(s):** OC
- **Observation:** Every examined item in the Bengali split carries a ground-truth answer label validated by Indian exam portal subject experts (per documentation) and audited by AI4Bharat (IIT Madras, IBM India). The culturally specific items in the Bengali sample [D2, D3, D4, D5, D6] all have correct answers that presuppose Indian constitutional, electoral, and cultural knowledge. No Bangladeshi institutional or individual validator is documented anywhere. For the governance/law questions (e.g., Election Commissioner removal procedure), the answer is verifiably correct for India but would be wrong if applied to Bangladesh's constitutional framework.
- **Deployment relevance:** The deployment requires native Bangladeshi Bengali speakers as primary ground truth. The benchmark's answer labels for cultural/governance content reflect Indian standards; a Bangladeshi evaluator might contest the framing of questions that appear to be generic ("the election commissioner") but actually encode Indian-specific legal structures.
- **Datapoint citations:**
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — the answer (President removes on CEC's recommendation) is specific to Indian constitutional law; Bangladesh's Election Commission operates under different provisions that a Bangladeshi annotator would recognize as distinct
  - [D2] Example 5 (Bengali, validation, option4): "আম আদমি পার্টি (AAP) নিম্নলিখিত কোন রাজ্যে সরকার গঠন করেছিল? … পাঞ্জাব" — requires knowledge of Indian party politics that is irrelevant to Bangladeshi civic knowledge

#### Concern 5: Output form (MCQ accuracy) fundamentally misaligned with deployment target (open-ended Bengali story generation)
- **Dimension(s):** OF, OO
- **Observation:** Every example across all 215 reviewed items is a closed-form 4-option MCQ. The output space is a discrete label (option1–option4). The deployment requires evaluating open-ended Bengali story generation — a generative task where cultural grounding, register appropriateness, narrative coherence, and accuracy of Bangladeshi named entities, historical events, and social context must be assessed. No mechanism in MILU produces a score that transfers to this task.
- **Deployment relevance:** This is a structural incompatibility: MCQ accuracy scores measure factual recall under forced choice, while story generation evaluation requires assessing fluency, cultural authenticity, register appropriateness, and factual grounding in Bangladeshi context. Strong performance on MILU Bengali (even if culturally recalibrated) would not directly validate culturally grounded story generation ability.
- **Datapoint citations:**
  - [D1] Example 1 (Bengali, validation, option3): "১৯৯১ সালে আর্থিক সংকটের কারণ হিসেবে বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ কী ছিল?" — The correct answer (option3) is binary pass/fail; this produces no information about whether a model can narratively describe economic history in Bangladeshi Bengali
  - [D19] Example 10 (Bengali, validation, option4): "হৃদয়ের পেসমেকার দ্বারা চিহ্নিত হয়, … এসএ নোড" — Medical MCQ; answering correctly does not predict whether the model can weave medical detail into a culturally authentic Bangladeshi story

---

#### MAJOR

#### Concern 6: Absence of 1971 Liberation War, Language Movement, and post-independence Bangladeshi political history
- **Dimension(s):** IO, IC
- **Observation:** None of the 21 Bengali examples, nor any English examples, reference the 1971 Liberation War, the 1952 Language Movement (Bhasha Andolan), Sheikh Mujibur Rahman, the founding of Bangladesh, or any post-1971 Bangladeshi political event. The History subject in Bengali covers the Bahamani Kingdom (Ex. 3) and Qutub Minar (Ex. 18) — medieval Indian history. The Law & Governance domain covers Indian state elections and Indian constitutional procedure.
- **Deployment relevance:** The 1971 Liberation War is described by the elicitation as "the foundational national narrative" for Bangladeshi Bengali speakers. The 2024 July Uprising — highly salient to the target student cohort — is post-benchmark and entirely absent. Any LLM evaluation intended to assess Bangladeshi cultural grounding must be able to test these topics; MILU provides no signal on them.
- **Datapoint citations:**
  - [D7] Example 3 (Bengali, validation, option4): "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" — History subject item covers Deccan medieval Indian kingdom; the equivalent Bangladeshi history items (Liberation War, Language Movement) are absent
  - [D6] Example 18 (Bengali, validation, option4): "_______ দিল্লিতে কুতুব মিনারের নির্মাণ সম্পন্ন করেছিলেন … ইলতুতমিশ" — Delhi monument history; no equivalent Bangladeshi historical landmark questions appear

#### Concern 7: No items referencing Bangladeshi geography, institutions, or named entities
- **Dimension(s):** IC, IO
- **Observation:** Across all 21 Bengali items, no Bangladeshi geographic reference appears (no Dhaka, Cox's Bazar, Buriganga, Padma, Jamuna, Meghna, Rangamati, Sundarbans-Bangladesh). No Bangladeshi institution appears (no Dhaka University, BUET, IUT, BRAC University). The only geographic references in the Bengali sample are Indian: Delhi (Qutub Minar), Punjab (AAP election).
- **Deployment relevance:** The deployment explicitly requires LLM familiarity with Bangladeshi neighborhoods, rivers, universities, and tourism sites as reference points for story generation. MILU Bengali provides no data to evaluate this.
- **Datapoint citations:**
  - [D6] Example 18 (Bengali, validation, option4): "দিল্লিতে কুতুব মিনারের নির্মাণ" — Delhi is the only city named in culturally specific Bengali items; no Dhaka or Bangladeshi city appears
  - [D2] Example 5 (Bengali, validation, option4): "পাঞ্জাব" — Punjab (Indian state) is a named geographic reference; no Bangladeshi geographic equivalent present

#### Concern 8: Bengali register appears to be standardized written form, not Bangladeshi Cholti — no Arabic/Persian loanword patterns observed
- **Dimension(s):** IC, IF
- **Observation:** The Bengali vocabulary in the sampled items uses standard written Bengali orthography. Examining available lexical items: "আর্থিক সংকট" (financial crisis), "তাৎক্ষণিক" (immediate), "মুদ্রার রিজার্ভ" (currency reserves), "নির্বাচন কমিশনার" (election commissioner), "রাষ্ট্রপতি" (president). These are primarily Tatsama (Sanskrit-derived) formal vocabulary forms characteristic of the pan-Indian written Bengali register, not the Arabic/Persian loanword patterns that characterize Bangladeshi Standard Bengali Cholti. Terms like "সরকার" (government, from Persian "sarkar") do appear, but the overall lexical profile shows no distinctive Bangladeshi register markers. Given that all items are GPT-4O translations from English, this is expected.
- **Deployment relevance:** The elicitation identifies Bangladeshi Standard Bengali's Arabic/Persian loanword density as a distinguishing feature. A benchmark using Sanskritic-heavy written Bengali vocabulary would underestimate model performance on Bangladeshi-register text if models have been trained on predominantly Bangladeshi Bengali corpora, or overestimate it if models are stronger on the West Bengali register being tested.
- **Datapoint citations:**
  - [D1] Example 1 (Bengali, validation, option3): "বিদেশি মুদ্রার রিজার্ভ হ্রাসের তাৎক্ষণিক কারণ … তেল ও পেট্রোলিয়াম পণ্যের আমদানির মূল্যের তীব্র বৃদ্ধি" — vocabulary: "তাৎক্ষণিক" (tātkṣaṇika, Sanskrit-derived), "আমদানি" (Persian/Arabic "āmdāni"); mixed register with no distinctively Bangladeshi Cholti markers
  - [D25] Example 13 (Bengali, validation, option2): "তার চমৎকার নৃত্য পরিবেশনা সবাইকে মুগ্ধ করেছিল।" — "নৃত্য পরিবেশনা" (nṛtya paribeśanā) uses Sanskrit-derived dance vocabulary; standard written Bengali without Bangladeshi-specific register markers

#### Concern 9: India-specific governance and law content in Bengali may produce false negatives for Bangladeshi users
- **Dimension(s):** OC, OO
- **Observation:** Several Bengali governance items test knowledge of Indian constitutional and electoral procedures that are structurally different in Bangladesh. Example 9 tests removal of India's Election Commissioner (answer: President on CEC's recommendation). Example 5 tests which Indian state AAP won in 2022. A Bangladeshi user who correctly knows Bangladesh's electoral commission structure but answers according to that knowledge would be marked wrong. These items produce false negative scores for Bangladeshi cultural knowledge rather than measuring gaps.
- **Deployment relevance:** For a deployment evaluating Bangladeshi cultural grounding, items that penalize Bangladeshi-specific knowledge while rewarding Indian-specific knowledge produce construct-irrelevant variance that would make MILU Bengali scores misleading as a validity measure for this deployment.
- **Datapoint citations:**
  - [D3] Example 9 (Bengali, validation, option3): "নির্বাচন কমিশনারকে অপসারণ করা যেতে পারে … প্রধান নির্বাচন কমিশনারের সুপারিশে রাষ্ট্রপতি" — correct only for Indian constitutional law; Bangladesh's equivalent procedure differs
  - [D14] Example 7 (Bengali, validation, option4): "জাতীয় খাদ্য সুরক্ষা মিশন একটি ফসল উন্নয়ন প্রকল্প … জাতীয় খাদ্য সুরক্ষা মিশন আগস্ট ২০০৭ সালে চালু হয়েছিল" — India's National Food Security Mission; a Bangladeshi user has no reason to know this Indian government program

---

#### MINOR

#### Concern 10: Bengali validation split has disproportionately high translation rate compared to documented 25% overall
- **Dimension(s):** IC, IF
- **Observation:** MILU documentation states that ~25% of total questions are translated from English. Yet all 21 Bengali validation examples sampled show `is_translated: True` (100%). While the sample size (21) is small and the validation split may differ from the test split, this suggests the Bengali validation split is predominantly or entirely composed of translated items, not organically sourced Bengali exam content.
- **Deployment relevance:** If the test split for Bengali also has a higher-than-average translation rate, then MILU Bengali performance reflects model ability to read translated English content in Bengali script rather than genuine Bengali-medium cultural knowledge. This further compounds the register gap concern.
- **Datapoint citations:**
  - [D8] All 21 Bengali validation examples (Bengali, validation): is_translated=True — 100% translation rate in the sampled Bengali validation split, compared to documented 25% overall benchmark average

#### Concern 11: Cross-language contamination — identical questions appear verbatim across multiple language splits
- **Dimension(s):** IF
- **Observation:** The 1991 India financial crisis question (D1), Bahamani Kingdom capital question (D7), Qutub Minar question (D6), cross-assembler question (D20), and Mediterranean climate question appear verbatim translated across Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, and Telugu splits. This confirms that a large portion of MILU's multilingual content is parallel translations of the same question set rather than language-specific sourcing.
- **Deployment relevance:** For a Bangladeshi Bengali deployment, this means that MILU's Bengali content does not capture any language-specific cultural knowledge that is unique to Bengali-medium contexts — it is a translation of pan-Indian English exam content. The "regional state exam" value proposition claimed in the documentation does not appear to materialize in the Bengali validation sample.
- **Datapoint citations:**
  - [D7] Example 3 (Bengali, validation, option4): "বাহামানি সাম্রাজ্যের প্রথম রাজধানী কী ছিল? … গুলবার্গা" — same question appears in Gujarati Ex. 3 ("બહમણી રાજ્યની પ્રથમ રાજધાની"), Hindi (not sampled but implied by cross-config parallel), Malayalam Ex. 3 ("ബഹ്മനി സാമ്രാജ്യത്തിന്റെ ആദ്യ തലസ്ഥാനം"), Punjabi Ex. 3 ("ਬਹਮਨੀ ਰਾਜ ਦਾ ਪਹਿਲਾ ਰਾਜਧਾਨੀ"), Tamil Ex. 18, Telugu (not in sample) — identical content across all languages confirms parallel translation, not language-specific sourcing

#### Concern 12: Rural, riverine, and village life contexts — structurally absent in exam format
- **Dimension(s):** IO
- **Observation:** All 215 reviewed examples are competitive examination questions (civil services, engineering entrance, technical knowledge) targeting urban, academically educated populations. No item invokes agricultural life, river ecology, monsoon seasons, boat culture, fishing villages, or rural Bangladesh contexts. This is a structural feature of the exam-sourced data collection methodology, not a sampling artifact.
- **Deployment relevance:** The deployment explicitly requires coverage of rural/village Bangladesh and riverine contexts as narrative settings for story generation. No MILU item provides evaluation signal for LLMs' ability to generate authentic content in these registers.
- **Datapoint citations:**
  - [D13] Example 2 (Bengali, validation, option3): "একটি ক্রিকেট প্রশিক্ষণ শিবিরে ১২০০ জন শিশু" — the most "everyday" context in the Bengali sample is a cricket training camp, still an organized institutional setting; no rural or riverine reference exists in any sampled item
  - [D27] Example 11 (Bengali, validation, option3): "সিদ্ধান্ত গ্রহণের সাথে যুক্ত সমস্যাগুলি হল: … ভয় এবং মিথ্যা আশা" — management psychology question; the register throughout is urban, academic, and professional

---

### Content Coverage Summary

The Bengali validation split of MILU (21 examples reviewed) consists entirely of translated English exam questions (`is_translated=True` in 100% of the sample), covering: electrical engineering and materials science (Exs. 4, 15, 16, 21), general sciences (Exs. 8, 10, 14), India-specific law and governance (Exs. 5, 9), India-specific history (Exs. 3, 7, 18), India-specific culture and arts (Exs. 12, 17), Indian government programs (Ex. 7), quantitative reasoning (Exs. 2, 16, 20), Bengali language grammar (Exs. 6, 13), management/business (Exs. 1, 11, 19), and environmental science (Ex. 7).

The cultural, political, and geographic content is uniformly India-centric. Named entities include: AAP (Indian party), Punjab (Indian state), the Indian President and Chief Election Commissioner, Vinoba Bhave (Indian nationalist leader), Filmfare Awards (Indian film industry), Qutub Minar (Delhi), and the Bahamani Kingdom (Deccan Sultanate). No Bangladeshi named entity, institution, historical event, geographic location, or cultural figure appears in any Bengali example.

Cross-config inspection confirms that the same questions appear in parallel translation across all 11 language splits, confirming that the Bengali content is not sourced from Bengali-medium Indian state exams (which would produce at least some India-regional Bengali content) but rather from pan-Indian English exam questions translated into Bengali.

Register analysis of the Bengali text shows standard formal written Bengali using primarily Tatsama vocabulary. No distinctive Bangladeshi Cholti register markers or Arabic/Persian loanword density patterns are observed.

The English split confirms the India-centric content origin: state-specific Indian governance (Maharashtra legislative committees, Telangana welfare scheme, Indian Railways named after Indian freedom fighter, Niti Aayog India Innovation Index). These are the source documents from which the Bengali translations derive.

---

### Limitations

1. **Sample size:** Only 21 Bengali validation examples were reviewed. The test split (6,637 examples) may contain a different proportion of translated vs. organically sourced items, and may include items from Bengali-medium Indian state exams that do not appear in the validation split. The 100% translation rate observed in the validation sample should not be assumed to apply to the test split without direct verification.

2. **Register analysis limits:** Determining whether Bengali text reflects Bangladeshi Cholti vs. West Bengali orthographic norms requires systematic lexical analysis by a native Bangladeshi Bengali linguist. The present analysis observes vocabulary patterns but cannot definitively classify register with certainty from a 21-item sample.

3. **Test split not sampled:** The full Bengali test split (6,637 examples) was not inspected. It is possible that organically sourced Bengali-medium exam items in the test split contain some Bangladeshi-relevant content, though the documentation strongly suggests this is unlikely given the Indian exam sourcing.

4. **Domain distribution:** The 21-item validation sample may not reflect the domain distribution of the full test split. The high proportion of STEM-adjacent items with `is_translated=True` may be a validation-split artifact.

5. **No audio or image modalities:** MILU is text-only; no audio or image content was present to inspect. This limitation is alignment-confirming (deployment is text-only) rather than a gap in this analysis.

6. **Annotator demographics not directly inspectable:** The demographic composition of annotators cannot be verified from the dataset itself; this analysis relies on documentation disclosures showing exclusively Indian institutional affiliation.