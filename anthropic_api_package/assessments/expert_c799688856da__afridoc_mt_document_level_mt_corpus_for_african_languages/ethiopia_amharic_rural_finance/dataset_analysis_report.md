## Dataset Analysis Report

**Dataset(s):** masakhane/AfriDocMT
**Analysis date:** 2025-07-11
**Examples reviewed:** 61 total (doc_health: 5, doc_health_10: 5, doc_health_25: 5, doc_health_5: 5, doc_tech: 5, doc_tech_10: 5, doc_tech_25: 5, doc_tech_5: 5, health: 5, tech: 6)
**Columns shown:** am, en, ha, sw, yo, zu
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | doc_health, train | 1 | health/WHO | "ሞቃታማ አውሎ ነፋሶችን እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች በመባል የሚታወቁት በጣም አጥፊ የአየር ሁኔታ ክስተቶች ናቸው" | Amharic translation of WHO health content on tropical cyclones — health domain, Ethiopic script | IC, IF |
| D2 | doc_health, train | 2 | health/WHO | "አካል ጉዳተኝነት ሰው የመሆን አካል ነው" | Amharic translation: "Disability is part of being human" — WHO health article | IC |
| D3 | doc_health, train | 3 | health/WHO | "በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት እና የተመጣጠነ ምግብ አቅርቦት በእናት ጡት ወተት ከሚሰጠው በላይ መጨመር የሚጀምር" | Amharic: infant complementary feeding guidance from WHO — health domain | IC |
| D4 | doc_health, train | 4 | health/WHO | "ፀረ-ተሕዋስያንን መቋቋም(AMR) የሚከሰተው ባክቴሪያ፣ ቫይረሶች፣ ፈንገሶች እና ጥገኛ ተህዋሲያን" | Amharic: antimicrobial resistance — health domain, WHO | IC |
| D5 | doc_health_10, train | 1 | health/WHO | "ይህ የሚያሳየው የደብሊውፒቪ1 ስርጭት ከአፍጋኒስታን (ምስራቅ ክልል) እና ፓኪስታን (ደቡብ ኬፒ) ዞኖች" | Amharic: polio surveillance language, mentions sub-national zones and infection control measures | IC, OO |
| D6 | doc_health_10, train | 3 | health/WHO | "ፋይናንስ ማካተት አሁናዊ ሁኔታዎችን ከሚያስፈልጉ ሰዎች ጋር ፍቃደኛ ከሆኑ" [Financial protection discussion] | Amharic: financial protection policy discourse — health financing domain | IC |
| D7 | doc_tech, train | 1 | tech/Techpoint | "ፔይ ደይ ለመሸጥ ይፈልጋል...ናይጄሪያ ፕሬዚዳንት አዲስ CBN ገዥን ሾሙ" | Amharic: African technology news digest — IT/fintech domain, no agricultural or legal content | IO |
| D8 | doc_tech, train | 2 | tech/Techpoint | "ደቡብ አፍሪካ ጎጂ ይዘቶችን በመስመር ላይ ማቆም ትፈልጋለች...ናላ ከ ዩኬ እና የአውሮፓ ህብረት ለናይጄሪያ ክፍያዎችን ይጀምራል" | Amharic: African fintech and content moderation news | IO |
| D9 | doc_tech, train | 3 | tech/Techpoint | "ኔስት ኮይን (Nestcoin) የሂሳብ መዛግብቱን ለማጠናከር እና የአዲሱን ምርት በኦንቦርድ እድገት" | Amharic: crypto/Web3 fintech startup news | IO |
| D10 | doc_tech, train | 4 | tech/Techpoint | "ኤርቴል ኡጋንዳ ለጃማይካዊው ዘፋኝ 180ሺህ ዶላር ለመክፈል...ቲክቶክ በኬንያ ቢሮ ለመክፈት" | Amharic: telecom copyright law and African tech platform expansion news | IO |
| D11 | health, train | 1 | health/WHO-sentence | "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" | Hausa sentence-level: oral cholera vaccine health terminology | IC |
| D12 | health, train | 2 | health/WHO-sentence | "ሆኖም የጤና ስርአቶች በዋነኛነት በህዝብ የገቢ ምንጮች ላይ መተማመን ያለባቸው" | Amharic sentence: "health systems need to predominantly rely on public revenue sources" | IC |
| D13 | tech, train | 1 | tech/sentence | "Sahel Capital's SEFAA (Social Enterprise Fund for Agriculture in Africa) Fund" | Tech sentence: agriculture-sector investment fund — only agricultural adjacent content in dataset | IO |
| D14 | tech, train | 6 | tech/sentence | "ፍርድ ቤቱን ጠይቋል" / "He also asked the court to order the telco to pay him royalties" | Amharic sentence: legal/court language in tech context — royalties claim against Safaricom | IO |
| D15 | doc_health_25, train | 2 | health/WHO | "WHA evaluated the unique epidemiological opportunity which exists over the next six months to eradicate the remaining chains of endemic wild poliovirus" | Complex administrative/WHO governance language; multi-sentence Amharic document | OO |
| D16 | doc_health_25, train | 4 | health/WHO | "ገቢ የሆነ የህፃናት አመጋገብ ከልደት ጀምሮ እስከ አዋቂነት ድረስ ለልጁ ዘላቂ ጤና መሰረታዊ ነው" | Amharic: infant nutrition health domain, WHO; long document with cross-sentence references | IC, OO |
| D17 | doc_health_25, train | 5 | health/WHO | "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ በሕግ አስገዳጅ የሆነ የዓለም አቀፍ ሕግ መሣሪያ ነው" | Amharic: International Health Regulations — legally-binding international law framework; closest genre to legal-administrative register in the dataset | IO, OO |
| D18 | doc_health_5, train | 1 | health/WHO | "ከ ቲአርአይፒኤስ ስምምነት ከፀደቀበት ጊዜ አንሥቶ የዓለም የጤና ስብሰባዎች ብዙ ውሳኔዎች" | Amharic: TRIPS agreement, intellectual property law in health sector — international health-law language | IO |
| D19 | doc_tech_25, train | 1 | tech/Techpoint | "ቬንቸር ካፒታሊስቶች(Venture capitalists) የ ኩባንያዎችን ማንነት የሚያገኙት" | Amharic: startup/entrepreneurship discourse — tech sector, no agricultural or cooperative content | IO |
| D20 | doc_tech_10, train | 1 | tech/Techpoint | "The edtech industry in India has exploded in the last few years, making it the world's epicentre." | English: edtech industry news — IT domain, no agricultural domain | IO |
| D21 | health, train | 4 | health/WHO-sentence | "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation" | English: public health measure description — WHO public health register | IC |
| D22 | doc_health, train | 1 | health/WHO | "ጊዜያዊ የስራ መደብ ወረቀት፡ ለአለም አቀፍ ተጓዦች የኮቪድ-19 ክትባት ማረጋገጫን" | Amharic: interim WHO policy paper — policy document register | OO |
| D23 | doc_health_10, train | 4 | health/WHO | "የጤና ባለሥልጣናት የትንኝ ብዛትን እና የበሽታውን ስርጭት ለመቀነስ ላርቪሳይድ" | Amharic: Zika vector control guidance — specific technical health terminology | IC |
| D24 | doc_health_10, train | 5 | health/WHO | "የጤና አካውንት ሥርዓት 2011 (ጤ/አ/ስ 2011) የጤና ወጪን ለመከታተል" | Amharic: System of Health Accounts — health financing framework document | OO |
| D25 | doc_tech_5, train | 1 | tech/Techpoint | "Remittances are typically transfers between individuals...immigrants send home to support their families" | English: diaspora remittances — fintech/financial inclusion domain | IO |
| D26 | doc_health_25, train | 3 | health/WHO | "እሳተ ገሞራ ፍንዳታዎች አጠቃላይ እይታ፦ እሳተ ገሞራ በምድር ቅርፊት ውስጥ የሚገኝ ክፍተት" | Amharic: volcanic eruptions health risk — WHO emergency preparedness | IC |
| D27 | doc_tech, train | 5 | tech/Techpoint | "ፕሮዳክት ዳይቭ እንዴት ነው የተጀመረው...ወደ ምርት አስተዳደር ጉዞ" | Amharic: long-form interview with tech entrepreneur — informal, personal narrative register | IF |
| D28 | tech, train | 3 | tech/sentence | "In dissecting the social impacts, it becomes vital to delve deep into real-life cases that embody both the positive and negative facets of sports betting in Kenya." | English: sports betting social impacts — not directly relevant to deployment context | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Amharic in Ethiopic Script with Multi-Sentence Document Structure
- **Dimension(s):** IF, IC
- **Observation:** All sampled Amharic content is rendered in Ethiopic (Ge'ez) script throughout all configurations, including full-document (doc_health, doc_tech), pseudo-document (10/25/5-sentence chunks), and sentence-level splits. Amharic script rendering is consistent and coherent across documents of varying length. The benchmark explicitly accommodates Ethiopic script tokenization by increasing token limits for Amharic.
- **Deployment relevance:** The deployment system must handle Amharic in Ethiopic script. The benchmark's demonstrated ability to process, segment, and evaluate multi-sentence Amharic documents in Ethiopic script confirms that the language/script dimension is technically addressed. This directly matches the target output modality.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች የሞቃታማ ዐውሎ ነፋሶች አጠቃላይ እይታ፡-" — Extended Ethiopic-script Amharic document covering multiple paragraphs; confirms multi-sentence Ethiopic document handling at the doc level.
  - [D3] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ..." — Mid-length WHO health article in Amharic, correctly segmented into numbered recommendations with discourse coherence preserved.

#### Strength 2: Multi-Sentence Discourse Phenomena in Amharic Are Present
- **Dimension(s):** IO, OO
- **Observation:** Several sampled Amharic documents contain multi-clause cross-sentence references, numbered recommendations, and conditional structures (e.g., "ካልተሰጡ ወይም ተገቢ ባልሆነ መንገድ ከተሰጡ" — "if not given or given inappropriately"), which mirror the benchmark's explicit aim to capture coreference resolution and lexical cohesion across sentences.
- **Deployment relevance:** The user acknowledged that document-level structural demands are broadly similar across genres. The benchmark captures cross-sentence dependency structures in Amharic, which the deployment will also need MT systems to handle when translating multi-clause legal and agricultural documents.
- **Datapoint citations:**
  - [D16] Example 4 (doc_health_25, split=train): "ምንም እንኳን በህፃናት መብቶች ስምነቱ መሰረት እያንዳንዱ ጨቅላ እና ህጻን ጥሩ አመጋገብ የማግኘት መብት ቢኖረውም" — Cross-clause conditional referencing: "although every infant… has the right… in many countries less than a fourth…"; demonstrates multi-sentence Amharic coherence across a qualifying clause.
  - [D15] Example 2 (doc_health_25, split=train): "WHA ሕዝቡ ጤና ድንገተኛ አደጋ አለም አቀፍ ስጋት… ሀገራት… አሳስበዋል" — Multi-clause WHO governance language in Amharic preserving cross-sentence referential structure.

#### Strength 3: Multiple Evaluation Configurations Including Document- and Sentence-Level Splits
- **Dimension(s):** IO, OF
- **Observation:** The HF dataset provides ten distinct configurations — sentence-level (health, tech), full-document (doc_health, doc_tech), and pseudo-document chunks (k=5, k=10, k=25) for both domains. All configurations include Amharic. This allows evaluation of MT systems at sentence and sub-document granularities that approximate the chunk sizes relevant for processing bureau documents.
- **Deployment relevance:** Bureau documents in the deployment context may range from short notices to multi-page proclamations. The availability of sentence-level and pseudo-document splits (k=5 through full document) enables evaluation across a range of document lengths comparable to those in the deployment.
- **Datapoint citations:**
  - [D11] Example 1 (health, split=train): "OCV wata hanya ce da ake amfani da ita a ƙari" — Short single-sentence health item; confirms that sentence-level granularity is included for all languages including Amharic.
  - [D5] Example 1 (doc_health_10, split=train): "ይህ የሚያሳየው የደብሊውፒቪ1 ስርጭት ከአፍጋኒስታን (ምስራቅ ክልል)..." — 10-sentence pseudo-document chunk in Amharic; demonstrates the k=10 chunking configuration relevant for medium-length document evaluation.

#### Strength 4: Health Domain Includes Some Policy and Regulatory-Adjacent Register
- **Dimension(s):** IC, OO
- **Observation:** A subset of the WHO health content uses formal policy register features: numbered recommendations ("1. …2. …"), cross-references to proclamation-like frameworks (IHR, TRIPS), and governance vocabulary. The International Health Regulations document (D17) explicitly describes a legally-binding international law instrument with numbered state obligations.
- **Deployment relevance:** This is the closest approximation in the benchmark to the formal administrative register of Ethiopian proclamation documents. While the domain mismatch is severe, the presence of multi-clause numbered obligations, legal vocabulary, and policy cross-references in Amharic provides at least a partial analog to the discourse structure of the deployment genre.
- **Datapoint citations:**
  - [D17] Example 5 (doc_health_25, split=train): "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ በሕግ አስገዳጅ የሆነ የዓለም አቀፍ ሕግ መሣሪያ ነው" — "IHR is an instrument of international law that is legally-binding on 196 countries"; formal legal-regulatory register in Amharic with numbered obligations.
  - [D18] Example 1 (doc_health_5, split=train): "ከ ቲአርአይፒኤስ ስምምነት ከፀደቀበት ጊዜ አንሥቶ የዓለም የጤና ስብሰባዎች ብዙ ውሳኔዎች" — TRIPS Agreement reference; international IP law cross-referenced in health-policy Amharic document.

#### Strength 5: Human-Translated Amharic by Named Native-Speaker Translators
- **Dimension(s):** OC
- **Observation:** The benchmark's four named Amharic translators (Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede) produced translations under a controlled workflow with quality estimation filtering and terminology workshop preparation. The translation process included human review by a native-speaker language coordinator.
- **Deployment relevance:** The target deployment requires high-quality Amharic translations assessable by native speakers. Benchmark reference translations were produced by human translators (not MT), providing a legitimate upper-bound Amharic quality signal in the health domain, even if domain-mismatched for agriculture/legal.
- **Datapoint citations:**
  - [D2] Example 2 (doc_health, split=train): "አካል ጉዳተኝነት ሰው የመሆን አካል ነው" — "Disability is part of being human"; fluent, naturalistically rendered Amharic sentence consistent with human translation quality.
  - [D4] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR) የሚከሰተው ባክቴሪያ፣ ቫይረሶች፣ ፈንገሶች" — Technical medical terminology rendered with consistent Amharic neologisms across the document (e.g., "ፀረ-ባክቴሪያ" for antibiotic), demonstrating terminological consistency within the health domain.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Total Domain Absence — No Agricultural, Land-Use, Credit-Scheme, or Cooperative Governance Content
- **Dimension(s):** IO, IC
- **Observation:** All 61 sampled examples draw exclusively from two domains: WHO health news and Techpoint Africa IT news. Not a single example contains agricultural input subsidy notices, land-tenure policy language, credit-scheme terms, cooperative membership governance language, or federal proclamation text. The dataset's vocabulary is drawn entirely from these two domains. In the entire sample, the only "agricultural" item is a single sentence naming a fund with "Agriculture in Africa" in its title (D13), which is a fintech story about an agricultural investment fund — not agricultural document content.
- **Deployment relevance:** The deployment's four target document genres (agricultural input subsidy notices, land-use policy updates, credit-scheme terms, cooperative membership notices) are completely unrepresented. This is not a partial gap — it is a total absence confirmed across all sampled configurations. The benchmark cannot be used as a direct domain-validity test for the deployment. Any performance score on AFRIDOC-MT will not predict MT quality on the deployment's actual document types.
- **Datapoint citations:**
  - [D7] Example 1 (doc_tech, split=train): "ፔይ ደይ ለመሸጥ ይፈልጋል...ናይጄሪያ ፕሬዚዳንት አዲስ CBN ገዥን ሾሙ" — Technology news bulletin: PayDay startup, CBN governor appointment — no agricultural content whatsoever.
  - [D8] Example 2 (doc_tech, split=train): "ናላ ከ ዩኬ እና የአውሮፓ ህብረት ለናይጄሪያ ክፍያዎችን ይጀምራል... ሴሉላንት 20% የሚሆነውን የሰው ኃይል ለማሰናበት" — Fintech remittances and tech layoffs news — no cooperative, land, or subsidy content.
  - [D13] Example 1 (tech, split=train): "Sahel Capital's SEFAA (Social Enterprise Fund for Agriculture in Africa) Fund" — The only "agriculture" mention in the entire sample is the name of an investment fund in a tech news story, not agricultural document content.
  - [D25] Example 1 (doc_tech_5, split=train): "Remittances are typically transfers between individuals…immigrants send home to support their families" — Closest fintech-adjacent item to rural microfinance, but purely in context of diaspora remittances, not ACSI loan agreements or cooperative credit schemes.

#### CRITICAL Concern 2: Source Language Direction Mismatch — Benchmark Translates FROM English; Deployment Translates FROM Amharic
- **Dimension(s):** IC, OC
- **Observation:** Every example in the dataset has an English source document and Amharic as the target translation. The benchmark evaluates English→Amharic MT. The deployment translates FROM Amharic government documents INTO a target language (presumably also Amharic, or possibly from Amharic source texts where the output needs to be evaluated in Amharic). More precisely: the deployment produces Amharic translations of documents that originate in Amharic government-register language — effectively evaluating MT quality in a very different structural direction. Even if the deployment were English→Amharic, the benchmark's English sources (WHO health news, Techpoint Africa IT news) are structurally and lexically distant from Ethiopian federal bureau documents.
- **Deployment relevance:** The benchmark's reference Amharic translations exhibit translationese — unnatural syntax and structural patterns influenced by English source texts. Deployment Amharic documents originate in Amharic proclamation register and have no such English structural bias. A model that performs well on AFRIDOC-MT (English health news → Amharic) may not perform well on the deployment's actual source texts.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "Tropical cyclones, also known as typhoons or hurricanes, are among the most destructive weather phenomena. They are intense circular storms that originate over warm tropical oceans..." — The English source is WHO public health news; the Amharic translation follows English syntactic ordering. Ethiopian proclamation documents are natively authored in Amharic with a distinct formal register.
  - [D17] Example 5 (doc_health_25, split=train): "አይኤችአር 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ በ196 አገሮች ላይ" — IHR article translated from English; even the closest regulatory-register content is a translation FROM English, not native Amharic administrative writing.

#### CRITICAL Concern 3: Complete Absence of Proclamation-Derived Agricultural and Financial Terminology
- **Dimension(s):** IC, OC
- **Observation:** The benchmark contains zero instances of the critical term categories identified by the user: input subsidy scheme names, land-tenure category labels (rist-derived terms, usufruct rights, holding certificates), cooperative membership tier designations from Proclamation 985/2016 (ቀዳሚ የሕብረት ሥራ ማኅበር, የሕብረት ሥራ ማህበራት ዩኒዮን), or MFI credit-scheme terms (ACSI group lending terminology). The Amharic vocabulary in the dataset is drawn from health (disease names, medical procedures, nutrition, epidemiology) and IT (startup names, fintech terms, crypto vocabulary) — entirely non-overlapping with the deployment's operative terminology.
- **Deployment relevance:** For the deployment, translation errors on specific legal terms (e.g., misrendering "ቀዳሚ ሕብረት ሥራ ማኅበር" vs. "ሕብረት ሥራ ማህበር ዩኒዮን") have direct legal and financial consequences for cooperative leaders. The benchmark provides no mechanism to evaluate whether an MT system correctly and consistently renders these terms, since they never appear in the data.
- **Datapoint citations:**
  - [D9] Example 3 (doc_tech, split=train): "ኔስት ኮይን (Nestcoin) የሂሳብ መዛግብቱን ለማጠናከር...ሃሺድ ኢመርጀንት" — Crypto/fintech vocabulary (stablecoin, FTX, pre-seed funding) — zero overlap with cooperative proclamation vocabulary or agricultural subsidy terminology.
  - [D4] Example 4 (doc_health, split=train): "ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ፣ ፀረ-ፈንገስ እና ፀረ-ተባይ መድሃኒቶች" — Medical antimicrobial terminology; no connection to land-tenure or cooperative tier vocabulary.
  - [D11] Example 1 (health, split=train): "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" — Oral cholera vaccine terminology in Hausa; illustrates the exclusively health-domain vocabulary present at sentence level.

#### MAJOR

#### MAJOR Concern 1: No Rubric Component for Terminological Consistency — The Critical Coherence Requirement for Deployment
- **Dimension(s):** OO
- **Observation:** The benchmark's output scoring framework evaluates fluency (GPT-4o 1-5 scale), content errors (CE), lexical cohesion errors (LE), and grammatical cohesion errors (GE). The lexical cohesion error definition ("issues with vocabulary usage, incorrect or missing synonyms, or overuse of certain words that disrupt the flow") addresses narrative discourse flow, not legal terminological consistency. No rubric component tests whether a specific legal term (e.g., a subsidy scheme name or cooperative tier designation) is rendered identically across all clauses of a document. The data examples confirm this: WHO documents are evaluated for narrative coherence, not for whether "Oral Cholera Vaccine" is always rendered the same way throughout.
- **Deployment relevance:** For the deployment, the key quality requirement is not narrative fluency but terminological stability — that "ቀዳሚ የሕብረት ሥራ ማኅበር" is always rendered identically across 50 clauses of a proclamation. This property is not measured by any metric in AFRIDOC-MT. Even if the deployment were adapted to use AFRIDOC-MT scoring, the scores would not capture the critical coherence dimension.
- **Datapoint citations:**
  - [D16] Example 4 (doc_health_25, split=train): "Ó dara jùlọ... abẹ́rẹ́ àjẹsára... ọmọ ọwọ́" — WHO nutrition document evaluated for fluency and cohesion in Yorùbá; assessment concerns narrative flow of infant feeding guidance, not consistent rendering of defined legal categories.
  - [D22] Example 1 (doc_health_5, split=train): "ጊዜያዊ የስራ መደብ ወረቀት፡ ለአለም አቀፍ ተጓዦች የኮቪድ-19 ክትባት ማረጋገጫን" — Interim WHO position paper; the document mentions specific policy concepts (PHEIC, IHR), but the scoring rubric would assess fluency, not consistent cross-document rendering of "PHEIC" as a defined term.

#### MAJOR Concern 2: Annotator Domain Expertise Absent for Agricultural/Legal Amharic
- **Dimension(s):** OC
- **Observation:** The four named Amharic translators produced reference translations for WHO health news and Techpoint Africa IT news. There is no documentation of their institutional affiliation, agricultural translation experience, or legal Amharic background. The preferred ground-truth authority specified by the user (domain-trained federal bureau translators) is entirely absent. The inter-annotator agreement for Amharic (Krippendorff's alpha = 0.46) is already low for the health domain in which the translators were specifically prepared; performance would likely be lower still in the agricultural-legal domain.
- **Deployment relevance:** Any quality judgment derived from AFRIDOC-MT Amharic reference translations — whether for training, evaluation, or benchmarking — reflects the judgments of translators working in health/IT contexts, not the federal bureau translation standard the user specified. Ground-truth misalignment means that high benchmark scores do not predict acceptability to the user's preferred evaluators.
- **Datapoint citations:**
  - [D3] Example 3 (doc_health, split=train): "ተጨማሪ ምግቦቹ በ 6 ወር ጊዜ ውስጥ ካልተሰጡ ወይም ተገቢ ባልሆነ መንገድ ከተሰጡ" — Amharic health translation requiring WHO pediatric nutrition domain expertise; translator preparation was appropriate for this domain but not for agricultural proclamation register.
  - [D5] Example 1 (doc_health_10, split=train): "የቅርብ ጊዜውን እድገት መቀልበስ ነው. መርሃግብሩ ከፍተኛ ጥራት ያላቸውን ዘመቻዎች" — Polio surveillance Amharic document; complex public health vocabulary produced by health-domain translators, not agricultural domain translators.

#### MAJOR Concern 3: Translationese Risk Compounds Domain Gap — Benchmark Amharic Does Not Reflect Native Administrative Register
- **Dimension(s):** IC
- **Observation:** The benchmark explicitly acknowledges that all Amharic reference translations may exhibit "unnatural syntax or overly literal phrasing" due to English source material. The sampled data confirms this: sentences follow English subordination patterns and clause ordering. Amharic federal proclamation documents use a distinct formal register with specific formulaic phrase structures (cross-article reference formulas, numbered subclause templates) that are natively authored in Amharic and absent from any translated text in the benchmark.
- **Deployment relevance:** MT systems fine-tuned or benchmarked on AFRIDOC-MT Amharic may learn English-influenced Amharic sentence structures. These structures may be legible but could fail to match the formal register expectations of rural cooperative leaders and bureau staff, who associate official documents with specific Amharic administrative phrasing.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "ሞቃታማ አውሎ ነፋሶች፣ እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች በመባል የሚታወቁት" — The Amharic renders "also known as typhoons or hurricanes" as a relative clause; this is a structurally English-influenced subordination pattern. Native Amharic administrative documents would likely employ a different grammatical structure.
  - [D27] Example 5 (doc_tech, split=train): "ቶቢ ከ ቴክ ፖይንት አፍሪካ ጋር ያደረጉት ቃለ ምልልስ" — Interview-register Amharic (tech domain): informal, conversational sentence structures that differ markedly from proclamation-register Amharic. Illustrates that even within the dataset, register variation exists that does not approach legal-administrative Amharic.

#### MINOR

#### MINOR Concern 1: Technology Domain Contains Some Legally Adjacent Content but Not Applicable to Deployment
- **Dimension(s):** IO
- **Observation:** Several tech domain documents contain legal or quasi-legal language: copyright infringement claims (D14), telecom regulatory decisions, and securities/investment disclosures. However, this legal language concerns corporate IP law, telecommunications regulation, and fintech compliance — entirely different from Ethiopian agricultural proclamation law, cooperative registration, and land-tenure regulation.
- **Deployment relevance:** These items might superficially appear to close the legal-register gap, but the specific legal vocabulary (royalties, capital markets, exchange rate unification) has no relevance to cooperative proclamations or subsidy scheme terms. The domain-register mismatch persists.
- **Datapoint citations:**
  - [D14] Example 6 (tech, split=train): "ፍርድ ቤቱን ጠይቋል" / "He also asked the court to order the telco to pay him royalties and licensing fees" — Amharic legal vocabulary in a copyright/IP context; not applicable to cooperative membership or land-tenure law.
  - [D10] Example 4 (doc_tech, split=train): "ኤርቴል ኡጋንዳ ለጃማይካዊው ዘፋኝ 180ሺህ ዶላር ለመክፈል... ፍርድ ቤቱ ተከሳሾቹን በቅጂ መብት ጥሰት" — Copyright infringement court ruling in Uganda; Amharic legal vocabulary but in IP/copyright register, not agricultural proclamation register.

#### MINOR Concern 2: Sports Betting and Some Tech Content Irrelevant to Any Deployment Need
- **Dimension(s):** IO
- **Observation:** Two examples in the tech dataset concern sports betting social impacts in Kenya (D28) and extended personal interviews about tech entrepreneurship. These are not only irrelevant to the agricultural deployment but represent the least formal, most conversational Amharic register in the dataset.
- **Deployment relevance:** Minor — these items do not affect the overall domain analysis, but they do further dilute the relevance of the tech domain for any purpose related to the deployment.
- **Datapoint citations:**
  - [D28] Example 3 (tech, split=train): "In dissecting the social impacts, it becomes vital to delve deep into real-life cases that embody both the positive and negative facets of sports betting in Kenya." — Sports betting commentary; no deployment relevance.
  - [D27] Example 5 (doc_tech, split=train): "ቶቢ...ስለ አስተዳደሯ፣ ስለ እምነቷ፣ የምርት ሥራ አስኪያጅ ለመሆን ስላላት መንገድ" — Extended personal interview on tech entrepreneurship; informal, narrative register; no deployment relevance.

---

### Content Coverage Summary

The dataset contains exclusively two content domains confirmed by direct examination: (1) WHO global health news covering topics including tropical cyclones, disability, antimicrobial resistance, complementary feeding, cholera, polio vaccination, COVID-19 policy, and International Health Regulations; and (2) African technology news from Techpoint Africa covering fintech startups, crypto/Web3, African tech ecosystem, mobile money, edtech, and agritech investment (but not agritech content — only investment news about agritech companies).

The Amharic translations are extensive, fluent, and technically handled in Ethiopic script throughout. Document-level examples average 30-37 sentences in length. The health domain employs formal WHO institutional register; the tech domain employs informal news-digest and interview register. The closest approximation to regulatory/legal language in the entire dataset is the International Health Regulations article (legally-binding international law framework) and TRIPS Agreement references — both translated from English and neither approaching Ethiopian agricultural proclamation vocabulary.

The dataset contains zero instances of: Ethiopian government document vocabulary, cooperative membership terminology, land-tenure language, agricultural subsidy scheme names, microfinance loan terms, or Amhara regional administrative vocabulary. The source-language direction is English→Amharic throughout; no Amharic-originating documents are present.

---

### Limitations

1. **Sample size within configurations**: 5-6 examples per configuration were reviewed. With 240-334 training documents per domain, unseen examples might include edge cases. However, given that sources are exclusively WHO.int and Techpoint Africa, additional samples cannot change the domain finding.

2. **Translator background unverifiable**: Web searches for the four named Amharic translators returned no results. It is possible but undocumented that any translator has agricultural or legal Amharic expertise. This cannot be confirmed or excluded from the data alone.

3. **Register quality assessment limited**: Evaluating whether the Amharic translations exhibit procurement-register appropriateness requires native-speaker expert judgment from someone familiar with Ethiopian bureau Amharic. The current analysis can identify structural patterns (clause ordering, subordination) but cannot definitively characterize the full register distance.

4. **Evaluation metric properties not directly observable**: The scoring behavior of d-chrF, d-BLEU, and GPT-4o on out-of-domain text (i.e., agricultural proclamation language) cannot be assessed from the dataset content alone; this would require running evaluation experiments with deployment-domain text.

5. **Amhara sub-regional dialect features**: Whether the Amharic translations reflect Addis Ababa standard or Amhara regional administrative variety cannot be determined from the data. No dialect-distinguishing features are observable in health/IT domain text.