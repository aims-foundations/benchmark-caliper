## Dataset Analysis Report

**Dataset(s):** masakhane/AfriDocMT
**Analysis date:** 2025-07-12
**Examples reviewed:** 51 total (5 from doc_health train, 5 from doc_health_10 train, 5 from doc_health_25 train, 5 from doc_health_5 train, 5 from doc_tech train, 5 from doc_tech_10 train, 5 from doc_tech_25 train, 5 from doc_tech_5 train, 5 from health train, 6 from tech train, 5 from doc_tech train)
**Columns shown:** am, en, ha, sw, yo, zu
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | doc_health, train | Ex. 1 | health | "የሞቃታማ ዐውሎ ነፋሶች ... ለሞቃታማ አውሎ ነፋሶች፣ እንዲሁም ሀይለኛ አውሎ ነፋስ ወይም አውሎ ነፋሶች ... ኃይለኛ ክብ አውሎ ነፋሶች ... 233 000 ሰዎችን ገድለዋል" | Full Amharic document on tropical cyclones (WHO article), multi-sentence, Ethiopic script, with clinical/epidemiological content and specific numbers | IF, IC |
| D2 | doc_health, train | Ex. 1 | health | "When tropical cyclones cause floods and sea surges, the risk of drowning and water- or vector-borne diseases increase." | WHO English source on tropical cyclones — generic global health content, no Ethiopia-specific epidemiological context | IC |
| D3 | doc_health, train | Ex. 2 | health | "አካል ጉዳተኝነት ሰው የመሆን አካል ነው፡፡ ሁሉም ሰው ማለት ይቻላል በሕይወታቸው ላይ በሆነ ወቅት ጊዚያዊ ወይም ዘላቂ የአካል ጉዳት ያጋጥማቸዋል" | Amharic WHO article on disability — prose narrative, full document preserved | IC, IF |
| D4 | doc_health, train | Ex. 3 | health | "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት ... ጨቅላ ህፃናት ... ጡት ማጥባት" | Amharic complementary feeding article — maternal-child health topic directly relevant to deployment (maternal-health booklets) | IC, OC |
| D5 | doc_health, train | Ex. 4 | health | "ፀረ-ተሕዋስያንን መቋቋም(AMR) ... ባክቴሪያ፣ ጥገኛ ተውሳኮች፣ ቫይረሶችና በፈንገሶች ምክንያት" | Amharic AMR article — specialized medical terminology in Ethiopic script | OC, IF |
| D6 | doc_health, train | Ex. 5 | health | "ክራይሚያ-ኮንጎ የደም መፍሰስ ትኵሳት ... CCHF ወረርሽኞች ... ከ10-40% ሞት ... ሞቃታማ አውሎ ነፋስ" | Amharic article on CCHF hemorrhagic fever — clinical terminology, disease outside typical Ethiopian endemic profile | IC |
| D7 | doc_health_10, train | Ex. 1 | health | "ነገር ግን፣ በ2023 እስከ ዛሬ 46 ደብሊዉፒቪ1 አዎንታዊ የአካባቢ ናሙናዎች ... ናንጋርሃር እና ኩናር አውራጃዎች ... ሚሊዮን ተመላሾች" | Amharic WHO article on Afghanistan polio — geographic specificity to Afghanistan/Pakistan, not Ethiopia; pseudo-document chunk (10 sentences) | IC, IO |
| D8 | doc_health_10, train | Ex. 2 | health | "የጤና አጠባበቅ አቅራቢዎች ከአካባቢያዊ አስጊ ሁኔታዎች ጋር የተዛመዱ የህጻናት በሽታዎችን ... ከሁለቱም ያደጉ እና በማደግ ላይ ያሉ ሀገራት" | Short Amharic sentence fragment — environment/child health with global framing | IC |
| D9 | doc_health_25, train | Ex. 2 | health | "ዓለም አቀፍ ትብብር የጋራ ዓላማን ለማሳካት ... ዜሮ ዶዝ ... ህፃናት ፈልጎ ማግኘት ... ዶ/ር ጆርጅ ምዊንያ" | Amharic WHO Assembly article about immunization — broad vaccination language relevant to vaccination schedule booklets | IC |
| D10 | doc_health_5, train | Ex. 4 | health | "Malnutrition in the early years of life can have long-lasting impacts on physical and mental development... WHO recommends breastfeeding babies exclusively for 6 months" | English WHO source on malnutrition — maternal-child health content aligned with deployment domain | IC |
| D11 | health, train | Ex. 4 | health (sentence) | "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation to populations who do not yet have access to basic services, as well as vaccination with Oral Cholera Vaccines." | Sentence-level WHO cholera prevention content — cholera is endemic in Ethiopia but article is generic global | IC, IO |
| D12 | health, train | Ex. 1 | health (sentence) | "OCV ni zana ambayo hutumiwa pamoja na hatua za kudhibiti kipindupindu." (sw) / "OCV jẹ́ ohun èlò fún àfikún àwọn ìlànà fún ṣíṣe àmójútó àrùn onígbá méjì" (yo) | Sentence-level multi-language row — all six languages present including Amharic | IF |
| D13 | doc_tech, train | Ex. 1 | tech | "ፔይ ዴይ ለሽያጭ ? ዛሬ በ ቴክ ፖይንት አፍሪካ ... የናይጄሪያ ፕረዚዳንት ... ፔይ ደይ ... ኦባሲ ኢነ-ኦቦንግ" | Amharic Techpoint Africa tech-news article about Nigerian fintech/genomics — not relevant to Ethiopian MOH deployment | IC, IO |
| D14 | doc_tech, train | Ex. 2 | tech | "ደቡብ አፍሪካ ጎጂ ይዘቶችን በመስመር ላይ ማቆም ትፈልጋለች ... YouTube ... NALA ... Cellulant ... ሴሉላንት 20%" | Long Amharic tech article: South Africa content regulation, YouTube, NALA remittances, Cellulant layoffs — entirely irrelevant to Ethiopian clinical translation | IO, IC |
| D15 | doc_health, train | Ex. 3 | health | "ደህንነቱ የተጠበቀ፡- በንጽህና ተከማችተው እና ተዘጋጅተዋል እንዲሁም ጠርሙሶች እና ፕላስቲኮችን ሳይሆን በንጹህ እቃዎች ... ጡት ማጥባት" | Complementary feeding clinical guidance in Amharic — high relevance (maternal health booklet content) | IC, OC |
| D16 | doc_health, train | Ex. 1 | health | "Tropical cyclones, also known as typhoons or hurricanes, are among the most destructive weather phenomena." | WHO article on tropical cyclones — generic global health emergency content | IC |
| D17 | doc_health_25, train | Ex. 4 | health | "ጡት ማጥባት የማስተዋል አቅም መጨመር፣ የትምህርት ቤት አፈፃፀም ... ጡት ማጥባት ትቁ ብሎ ይመክራሉ" | Amharic infant nutrition article — direct overlap with maternal-health booklet deployment | IC |
| D18 | doc_health, train | Ex. 2 | health | "Disability results from the interaction between individuals with a health condition, such as cerebral palsy, Down syndrome and depression, with personal and environmental factors" | WHO disability article — relevant to health sector but not to primary clinical guideline/maternal-health booklet domain | IC |
| D19 | doc_health_25, train | Ex. 3 | health | "COVID-19 ... Interim position paper: considerations regarding proof of COVID-19 vaccination for international travellers" | COVID-19 international travel advisory — time-limited, globally generic, not Ethiopia-specific | IC |
| D20 | doc_health_25, train | Ex. 5 | health | "ዓለም አቀፍ የጤና ደንቦች ... IHR 194 የዓለም ጤና ድርጅት አባላትን ጨምሮ" | International Health Regulations article — relevant to health systems globally, but highly technical/regulatory, not maternal-clinical prose | IC |
| D21 | doc_health, train | Ex. 4 | health | "Antimicrobial resistance ... AMR threatens the effective prevention and treatment of an ever-increasing range of infections caused by bacteria, parasites, viruses and fungi." | AMR — critical global health topic relevant to clinical settings, within WHO source domain | IC |
| D22 | doc_tech_25, train | Ex. 1 | tech | "Fatanmi identifies is its effect on marketing a business ... Gen Zs ... Building in public..." | Tech article about startup marketing strategy — entirely irrelevant to Ethiopian MOH clinical translation deployment | IO |
| D23 | health, train | Ex. 2 | health (sentence) | "However, what is clear is that health systems need to predominantly rely on public revenue sources: mandatory, pre-paid and pooled" | Health financing sentence — health systems policy, not clinical guideline content | IC |
| D24 | health, train | Ex. 3 | health (sentence) | "Similarly, the development and promotion of WHO international reference standards helps ensure that biological therapeutics are standardized between different manufacturers, countries, and laboratories." | Biological therapeutics standardization — very specialized regulatory content | IC |
| D25 | doc_health_10, train | Ex. 3 | health | "ጤና ስርዓቱ መጠነ ሰፊ ለውጥ ... የቅድመ ክፍያ ፈንድ ... ዘላቂ ልማት ግቦች" | Health financing/health accounts article — health systems economics, not clinical or maternal-health prose | IC |
| D26 | doc_health_10, train | Ex. 4 | health | "ዚካ ቫይረስ ... ፀረ-ተባይ ... Vector control operations framework for Zika virus" | Short Zika virus sentence fragment — topic not endemic to Ethiopia | IC |
| D27 | doc_health_10, train | Ex. 5 | health | "የጤና አካውንት ሥርዓት ... የጤና ወጪን ... SHA 2011" | Health accounts system article — health financing methodology, not clinical guideline content | IC |
| D28 | doc_health_5, train | Ex. 1 | health | "የ ቲአርአይፒኤስ ስምምነት ... TRIPS ... ዓለም ንግድ ድርጅት ... WTO ... WIPO" | TRIPS/intellectual property & medicines article — health policy, not clinical guideline | IC |
| D29 | doc_health_5, train | Ex. 3 | health | "ግብር እና ድጎማ ... ማህበራዊ ሚዲያ ይዘቶቻቸውን ለፖሊሲ ምርጫ" | Health system governance/taxes sentence fragment — health policy tools | IC |
| D30 | doc_health, train | Ex. 3 | health | "Ensuring that infants nutritional needs are met requires that complementary foods be: timely ... adequate ... safe ... properly fed" | WHO complementary feeding — directly matches maternal-health booklet deployment content | IC, OC |
| D31 | doc_health_25, train | Ex. 4 | health | "ጡት ማጥባት … ሞተዋል .... 820,000 ... 40% ..." | Amharic infant nutrition WHO article — directly relevant to maternal-health booklet | OC |
| D32 | doc_health, train | Ex. 5 | health | "Crimean-Congo haemorrhagic fever (CCHF) is a viral haemorrhagic fever usually transmitted by ticks ... CCHF is endemic in all of Africa, the Balkans, the Middle East and in Asia." | CCHF article — hemorrhagic fever not a primary health priority in Ethiopia; tick-borne virus | IC |
| D33 | doc_health_25, train | Ex. 3 | health | "A volcano is a vent in the Earth's crust from which eruptions occur... There are about 1500 potentially active volcanoes worldwide." | Volcanic eruption WHO article — not relevant to Ethiopian clinical translation deployment | IC, IO |
| D34 | doc_health_10, train | Ex. 1 | health | "Afghanistan continues to implement an intense campaign schedule, focusing on improving quality in the endemic zone... massive population movement significantly increases the risk of cross-border poliovirus spread" | WHO Afghanistan polio article — geographically specific to Afghanistan, not Ethiopia | IC |
| D35 | doc_health_5, train | Ex. 2 | health | "ይህ ለሕዝብ ጤና ድንገተኛ አደጋዎች እና ለ አይኤችአር ትግበራ ... WGIHR6 ... PHEIC" | International health regulations/WGIHR process article — technical governance content | IC |
| D36 | doc_health_25, train | Ex. 2 | health | "The WHA evaluated the unique epidemiological opportunity which exists over the next six months to eradicate the remaining chains of endemic wild poliovirus transmission." | WHO Assembly polio article — immunization content indirectly relevant (vaccination schedules), but Afghanistan/global framing not Ethiopia-specific | IC |
| D37 | doc_health_5, train | Ex. 5 | health | "WHO works with Member States to ensure key populations have adequate knowledge about appropriate foods and feeding practices" | WHO complementary feeding counselling — maternal-child health, highly relevant | IC, OC |
| D38 | doc_tech_10, train | Ex. 1 | tech | "የሕንድ ኢድቴክ ኢንዱስትሪ ... ሕንድ ከዩናይትድ ስቴትስ (ዩ ኤስ) ቀጥሎ ... edtech ... Central Square Foundation ... Nigerian Edtech ecosystem" | Indian/Nigerian edtech article — entirely irrelevant to Ethiopian clinical translation | IO |
| D39 | doc_tech_25, train | Ex. 2 | tech | "Nigerian healthtech startup, Clafiya, raises $610,000 in pre-seed funding" | African healthtech/fintech startup news — entirely irrelevant to Ethiopian MOH clinical translation deployment | IO |
| D40 | health, train | Ex. 5 | health (sentence) | "Safe, effective and quality-assured blood products contribute to improving and saving millions of lives every year" | Blood products sentence — health domain but not maternal/clinical guideline focus | IC |
| D41 | doc_health, train | Ex. 1 | health | "WHO helps to restore primary care services so that facilities can deliver essential services, including immunization, basic treatment for common illnesses, acute malnutrition and maternal care" | WHO cyclone response includes immunization + maternal care — partially relevant content | IC, OC |
| D42 | doc_health_25, train | Ex. 4 | health | "የዓለም ጤና ድርጅት ሕፃናትን ለ6 ወራት ብቻ እንዲያጠቡ ይመክራል ... ደህንነቱ የተጠበቀ እና ተጨማሪ ምግብ" | Amharic WHO recommendation on exclusive breastfeeding — direct match for maternal-health booklet content | IC, OC |
| D43 | doc_health, train | Ex. 4 | health | "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ፣ ፀረ-ፈንገስ ... 'ሱፐርበግስ(superbugs)'" | AMR article with English loanword "superbugs" retained in Amharic — illustrates translationese patterns | IC, OC |
| D44 | doc_health, train | Ex. 3 | health | "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ እና ከፊል ጠጣር ምግቦችን መመገብ ይችላሉ" | Amharic instruction for pureed/mashed foods from 6 months — clinically precise maternal-health instruction | OC |
| D45 | doc_health_10, train | Ex. 2 | health | "To allow healthcare providers to better identify and prevent childhood diseases related to environmental risk factors, experts from both developed and developing countries" | Short environmental health sentence — health domain but generic | IC |
| D46 | doc_health_5, train | Ex. 1 | health | "TRIPS Agreement, many resolutions of the World Health Assemblies have requested WHO to address the impact of trade agreements and intellectual property protection on public health and access to medicines" | TRIPS/IP health policy — highly technical policy content | IC |
| D47 | doc_health, train | Ex. 5 | health | "CCHF ወረርሽኞች ቫይረሱ ወደ ወረርሽኞች ሊያመራ ስለሚችል ከፍተኛ የሞት መጠን (ከ10-40%)... ህክምና፡- የክራይሚያ-ኮንጎ ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" | CCHF treatment article in Amharic including "ribavirin" (transliterated drug name) — medical terminology rendering pattern visible | OC |
| D48 | doc_health_25, train | Ex. 4 | health | "ዓለም አቀፍ የጤና ሽፋን ... ዘላቂ የልማት ግቦች ... SDG ... ዘርፈ ብዙ የህዝብ ጤና" | Disability/UHC policy article — health governance framing, not clinical maternal health | IC |
| D49 | doc_health_25, train | Ex. 1 | health | "Continue to support research to improve vaccines that reduce transmission and have broad applicability; to understand the full spectrum, incidence and impact of post COVID-19 condition" | COVID-19 research policy article — time-limited global policy content | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic Amharic Ethiopic-script health translations present throughout
- **Dimension(s):** IF, IC
- **Observation:** All health examples contain Amharic (`am`) column text in Ethiopic/Ge'ez script. The data consistently includes full-document Amharic prose across health topics, with complex multi-sentence Amharic translations demonstrating that the benchmark actually contains the script and language variant required. The documents are narrative prose, matching the user's accepted scope.
- **Deployment relevance:** This directly confirms that the benchmark evaluates the target script and language combination (Amharic, Ethiopic script) for the deployment. The text in [D1] shows a full multi-paragraph Amharic WHO article of the type that would appear in MOH distribution materials, and [D4] and [D5] demonstrate medical terminology rendering in Ethiopic script.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች ... ኃይለኛ ክብ አውሎ ነፋሶች ... 233 000 ሰዎችን ገድለዋል" — Full-length Amharic health document in Ethiopic script with numbers, medical terms, and multi-paragraph structure.
  - [D5] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR) ... ባክቴሪያ፣ ጥገኛ ተውሳኮች፣ ቫይረሶችና" — Medical terminology for AMR rendered in Ethiopic script with parenthetical English acronym, showing how clinical terms are handled.
  - [D47] Example 5 (doc_health, split=train): "ህክምና፡- የክራይሚያ-ኮንጎ ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Drug name "ribavirin" transliterated alongside Amharic clinical treatment text.

#### Strength 2: Multi-parallel structure enables comparison across all six languages simultaneously
- **Dimension(s):** IF, OO
- **Observation:** Every data row contains parallel translations in all six languages (am, en, ha, sw, yo, zu) from the same source document. This enables evaluation of Amharic translation quality directly against the English source, while also permitting cross-linguistic comparison.
- **Deployment relevance:** The deployment is English→Amharic. The benchmark directly supports this evaluation direction. The parallel structure means one can assess whether a model correctly translates a sentence such as [D2] into Amharic [D1] within the same row.
- **Datapoint citations:**
  - [D12] Example 1 (health, split=train, sentence-level): "OCV wata hanya ce da ake amfani da ita a ƙari a kan hanyar kula da kwalara" (ha) — Each row contains all six translations of the same sentence, enabling direct comparison.

#### Strength 3: Maternal and child health content directly matching deployment domain
- **Dimension(s):** IC, OC
- **Observation:** Several WHO articles in the health corpus directly cover topics central to the MOH deployment scope: complementary feeding (Example 3, doc_health train), infant nutrition including breastfeeding recommendations (doc_health_25, Example 4), and similar maternal-child health topics. These represent the closest thematic match to the stated deployment use case of maternal-health booklets and vaccination schedules.
- **Deployment relevance:** The deployment specifically names maternal-health booklets as a primary document type. The complementary feeding, breastfeeding, and infant nutrition articles are substantively equivalent to maternal-health booklet content, making these the highest-value examples in the corpus for validity assessment.
- **Datapoint citations:**
  - [D4] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ፡- በ 6 ወር አካባቢ የሕፃኑ የኃይል ፍላጎት ... ጨቅላ ህፃናት" — Full Amharic complementary feeding article directly matching maternal-health booklet content.
  - [D15] Example 3 (doc_health, split=train): "Ensuring that infants nutritional needs are met requires that complementary foods be: timely ... adequate ... safe" — English source for complementary feeding guidelines.
  - [D42] Example 4 (doc_health_25, split=train): "የዓለም ጤና ድርጅት ሕፃናትን ለ6 ወራት ብቻ እንዲያጠቡ ይመክራል ... ደህንነቱ የተጠበቀ እና ተጨማሪ ምግብ" — Amharic WHO breastfeeding recommendation — directly applicable to maternal-health booklet context.
  - [D37] Example 5 (doc_health_5, split=train): "WHO works with Member States to ensure key populations have adequate knowledge about appropriate foods and feeding practices" — maternal-child health domain.

#### Strength 4: Document-level structure preserved, enabling assessment of paragraph-level cohesion
- **Dimension(s):** IF, OO
- **Observation:** The `doc_health` config contains full documents (Example 1 is a complete WHO tropical cyclones article; Example 2 is a full disability article), not isolated sentences. The chunked configs (`doc_health_10`, `doc_health_5`, etc.) preserve multi-sentence pseudo-documents. This means the benchmark can test context-dependent translation phenomena such as pronoun resolution and terminological consistency across paragraphs.
- **Deployment relevance:** Clinical practice guidelines and maternal-health booklets are multi-page documents. The benchmark's document-level structure directly supports evaluation of translation fidelity across longer clinical text units, which is critical for the deployment.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): The Amharic tropical cyclones article contains multiple paragraphs with consistent use of "ዐውሎ ነፋሶች" (tropical cyclones) across sections, demonstrating intra-document terminological consistency.
  - [D3] Example 2 (doc_health, split=train): "አካል ጉዳተኝነት ሰው የመሆን አካል ነው፡፡ ሁሉም ሰው ..." — Full WHO disability article across many paragraphs.

#### Strength 5: WHO-sourced health prose directly equivalent to Ethiopian MOH distribution materials
- **Dimension(s):** IC
- **Observation:** The health corpus is entirely sourced from WHO public health articles. The register, topic range, and structural patterns (overview → impact → WHO response) match the type of narrative prose typical of WHO-aligned MOH health communication materials. Topics such as cholera prevention (D11), AMR (D21), immunization (D36, D9), and maternal-child health (D4, D42) all fall within the scope of clinical guideline and health booklet content distributed by Ministries of Health.
- **Deployment relevance:** The user accepted generic WHO-sourced health prose as sufficient for the current evaluation scope. This is confirmed as a good match: the corpus provides the same institutional register and authorial voice as source documents that Ethiopian MOH materials would be translated from.
- **Datapoint citations:**
  - [D11] Example 4 (health, split=train): "Measures for the prevention of cholera mostly consist of providing clean water and proper sanitation" — WHO cholera prevention sentence; cholera is endemic in Ethiopia, making this directly relevant.
  - [D41] Example 1 (doc_health, split=train): "WHO helps to restore primary care services so that facilities can deliver essential services, including immunization, basic treatment for common illnesses, acute malnutrition and maternal care" — WHO response article encompasses immunization and maternal care, both central to the deployment domain.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Annotator credentials for Amharic reference translations are undocumented and likely do not match deployment ground-truth authority
- **Dimension(s):** OC
- **Observation:** The four named Amharic translators (Bereket Tilahun, Hana M. Tamiru, Biniam Asmlash, Lidetewold Kebede, per Q109) appear in data rows containing complex clinical terminology — including AMR, antimicrobials, hemorrhagic fever treatment (ribavirin), and infant nutrition guidance. The benchmark documentation provides no professional credentials, institutional affiliations, or clinical backgrounds for these translators. No MOH certification or EFDA terminology training is documented. The terminology in the Amharic translations (e.g., loanword handling for "superbugs," "ribavirin," drug class names in [D43], [D47]) is visible in the data but cannot be independently verified against any institutional standard.
- **Deployment relevance:** The user explicitly identifies MOH-trained clinical translators or Amharic-speaking physicians as the authoritative ground-truth population. If the benchmark's Amharic reference translations were produced by general-purpose translators without clinical MOH credentials, the reference translations against which system outputs are scored may not reflect the clinical accuracy standards the deployment requires. This is the most consequential OC gap: evaluation scores computed against these references may validate translations that do not meet MOH clinical standards, and vice versa.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ ... 'ሱፐርበግስ(superbugs)'" — The transliterated English term "superbugs" in Amharic parentheses suggests a translator choice that may or may not conform to MOH/EFDA approved terminology for this concept.
  - [D47] Example 5 (doc_health, split=train): "ፀረ-ቫይረስ መድሃኒት ... ribavirin" — The drug name "ribavirin" is retained in transliterated form; it is unverifiable whether this matches the EFDA-approved Amharic pharmaceutical terminology for this antiviral.
  - [D44] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ እና ከፊል ጠጣር ምግቦችን" — Maternal-health guidance translated with specific clinical language; conformance to MOH terminology for infant feeding guidance is unverifiable.

#### CRITICAL Concern 2: No mechanism for evaluating MOH/EFDA glossary compliance — the primary deployment success criterion is entirely unoperationalized
- **Dimension(s):** OO
- **Observation:** The benchmark's scoring functions — d-BLEU, d-chrF, GPT-4o-as-judge, and human DA — are all agnostic to any institutional terminology list. The data rows contain medical terminology choices (clinical vocabulary for AMR, vaccines, infant nutrition, hemorrhagic fever) that would need to be assessed against MOH and EFDA approved glossaries in the deployment context, but the benchmark provides no mechanism to do this. The planned terminology harmonization step for translators (Q121) is not documented as having been completed, and no reference to any Ethiopian-specific glossary is found in the data or documentation.
- **Deployment relevance:** The user states that glossary compliance is a primary success criterion. A system that scores well on d-chrF against AFRIDOC-MT references may nonetheless fail to comply with MOH/EFDA approved Amharic medical terminology. Conversely, a system that correctly uses MOH-approved terminology might score lower if that terminology differs from the benchmark translators' choices. This renders d-chrF and BLEU scores partially construct-invalid as measures of the deployment's primary success criterion.
- **Datapoint citations:**
  - [D5] Example 4 (doc_health, split=train): "ፀረ-ተሕዋስያንን መቋቋም(AMR)" — The Amharic rendering of "antimicrobial resistance" uses a descriptive phrase; whether this matches the Academy of Ethiopian Languages Amharic Medical Dictionary or the MOH/EFDA approved term is unverifiable from the benchmark alone.
  - [D4] Example 3 (doc_health, split=train): "ተጨማሪ ምግብ ማጠቃሊያ" (complementary feeding) — Specific infant feeding terminology in Amharic; compliance with MOH approved nutrition terminology cannot be assessed.
  - [D21] Example 4 (doc_health, split=train): "Antimicrobial resistance ... AMR threatens the effective prevention and treatment of an ever-increasing range of infections" — English source with clinical pharmacology terminology that requires verified EFDA-approved Amharic equivalents.

---

#### MAJOR

#### MAJOR Concern 1: A substantial portion of the health corpus covers topics with low direct relevance to Ethiopian MOH clinical priorities
- **Dimension(s):** IC, IO
- **Observation:** While the health corpus is domain-aligned at the level of "WHO health articles," a significant subset covers topics that are either geographically remote from Ethiopia or substantively distant from clinical practice guidelines, vaccination schedules, and maternal-health booklets. In the sampled data: tropical cyclones (Ex. 1, doc_health — [D1]), Crimean-Congo hemorrhagic fever endemic to the Balkans/Central Asia (Ex. 5, doc_health — [D32]), Afghanistan polio campaigns ([D7], [D34]), volcanic eruptions ([D33]), international health financing mechanisms ([D25], [D27], [D28]), TRIPS/IP policy ([D46]), COVID-19 international travel guidance ([D19]), and IHR process documentation ([D20], [D35]). These topics occupy a substantial share of sampled examples.
- **Deployment relevance:** The deployment translates clinical practice guidelines, vaccination schedules, and maternal-health booklets — all of which involve disease-treatment, preventive care, and patient-facing language. Training or fine-tuning a system on the AFRIDOC-MT health corpus, then evaluating it using these examples, will include substantial signal from topics (disaster preparedness, international health law, health financing) that do not appear in the actual deployment document types.
- **Datapoint citations:**
  - [D33] Example 3 (doc_health_25, split=train): "A volcano is a vent in the Earth's crust from which eruptions occur. There are about 1500 potentially active volcanoes worldwide." — WHO volcanic eruption article; not relevant to Ethiopian MOH clinical materials.
  - [D7] Example 1 (doc_health_10, split=train): "ናንጋርሃር እና ኩናር አውራጃዎች ... 1.7 ሚሊዮን ተመላሾች" — Afghanistan polio returnees article; geographic and contextual mismatch with Ethiopia.
  - [D32] Example 5 (doc_health, split=train): "Crimean-Congo haemorrhagic fever (CCHF) ... CCHF is endemic in all of Africa, the Balkans, the Middle East and in Asia." — CCHF hemorrhagic fever; not a primary Ethiopian clinical guideline topic.
  - [D26] Example 4 (doc_health_10, split=train): "Vector control operations framework for Zika virus" — Zika is not endemic in Ethiopia.

#### MAJOR Concern 2: Significant tech corpus included in the benchmark — entirely irrelevant to MOH clinical deployment
- **Dimension(s):** IO
- **Observation:** Approximately half the benchmark data is the tech corpus (`doc_tech`, `doc_tech_5`, `doc_tech_10`, `doc_tech_25`, `tech`), consisting of Techpoint Africa news articles about Nigerian/African technology startups, fintech, cryptocurrency, content regulation, and product management. The sampled examples include articles on Cellulant layoffs [D14], Nestcoin crypto funding [D13], Nigerian VC investment [D22], South Africa online content regulation, and Indian edtech [D38].
- **Deployment relevance:** The deployment is exclusively concerned with health document translation for MOH distribution. Tech-domain data contributes no valid signal for health translation quality and could introduce domain-specific vocabulary and register patterns into fine-tuning or evaluation that actively degrade health translation performance. If researchers evaluate models on the combined benchmark, tech-domain scores would dilute health-domain signals.
- **Datapoint citations:**
  - [D14] Example 2 (doc_tech, split=train): "South Africa wants to stop harmful content online ... YouTube ... NALA launches payments from UK and EU to Nigeria ... Cellulant to lay off 20% of its workforce" — Entirely irrelevant to clinical translation deployment.
  - [D38] Example 1 (doc_tech_10, split=train): "የሕንድ ኢድቴክ ኢንዱስትሪ ... ሕንድ ከዩናይትድ ስቴትስ ... Central Square Foundation" — Indian edtech article in Amharic; no relevance to Ethiopian MOH.
  - [D22] Example 1 (doc_tech_25, split=train): "One benefit Fatanmi identifies is its effect on marketing a business... Gen Zs ... Building in public" — Startup marketing article; entirely irrelevant.

#### MAJOR Concern 3: GPT-4o-as-judge documented as unreliable for Amharic — deployment cannot use it as scalable quality proxy
- **Dimension(s):** OO, OF
- **Observation:** The benchmark documentation explicitly states that GPT-4o produced inconsistent judgments when translating into African languages (Q66, Q67, Q99, Q218, Q219) and that the benchmark consequently deprioritizes it in favor of human DA for African languages. This is independently corroborated by the Walia-LLM study (EMNLP 2024). The data itself — including long clinical Amharic texts such as [D1], [D5], [D43] — cannot be reliably scored by GPT-4o as a judge.
- **Deployment relevance:** The deployment would benefit from a scalable, automated quality-assessment mechanism to evaluate clinical Amharic translations without requiring human clinical translators for every document. The benchmark confirms that GPT-4o-as-judge cannot fill this role for Amharic, and no validated document-level embedding metric (e.g., long-context AfriCOMET) exists for Amharic. This leaves d-chrF/d-BLEU as the primary scalable metrics, which cannot capture MOH/EFDA terminological compliance.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ ... 'ሱፐርበግስ(superbugs)'" — A complex clinical sentence with a mixed Amharic/English term; GPT-4o's inconsistent Amharic capabilities mean it cannot reliably judge whether this rendering is acceptable.
  - [D47] Example 5 (doc_health, split=train): "ህክምና፡- ... ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Drug terminology requiring clinical judgment that GPT-4o cannot reliably provide.

#### MAJOR Concern 4: Inter-annotator agreement for Amharic human evaluation is low (α = 0.46), compounding the annotator-credentials gap
- **Dimension(s):** OC
- **Observation:** Even among the benchmark's own Amharic human evaluators, Krippendorff's alpha is 0.46 — the lowest agreement level among the five languages (Yorùbá achieves 0.81). This means the human DA signal for Amharic is noisy even within the benchmark's own framework, before considering whether those annotators represent the deployment's authoritative population (MOH-trained clinical translators). The data cannot reveal why agreement is low — it could reflect genuine translation ambiguity, annotator background differences, or the fine granularity of the 0-100 scale — but it means that even if benchmarking scores are computed, the human evaluation signal has substantial uncertainty for Amharic specifically.
- **Deployment relevance:** The deployment requires confident quality signals for clinical Amharic translations. An inter-annotator agreement of α = 0.46 implies that even if the benchmark's human evaluators were acceptable proxies for MOH translators (which is unverified), approximately half their quality signal would be noise. This compounds the annotator-credentials concern: the reference translation quality signal for Amharic is both uncertain in provenance and noisy in annotation.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): The complex multi-paragraph Amharic cyclones article — exactly the type of document where annotator disagreement on translation quality would be expected, given the technical register and length.
  - [D44] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት ከ6 ወር ጀምሮ የተጣራ፣ የተፈጨ" — Maternal-health clinical instruction where annotator agreement on the correct Amharic rendering of feeding guidance would matter most for the deployment.

---

#### MINOR

#### MINOR Concern 1: Translationese effects visible in Amharic data — English-centric structural patterns may not reflect natural Amharic clinical register
- **Dimension(s):** IC, OC
- **Observation:** The benchmark explicitly acknowledges translationese risk (Q103–Q105). In the sampled Amharic data, English structural patterns appear clearly: parenthetical acronyms like "(AMR)" and "(CCHF)" embedded in Amharic text [D5, D6], English loanwords like "superbugs" (ሱፐርበግስ) with parentheses [D43], and direct transliterations of drug names like "ribavirin" [D47]. The document-level Amharic text in [D1] follows the WHO article's topic-sentence structure closely, which may not reflect how Amharic health writers would naturally organize health guidance.
- **Deployment relevance:** If a system trained/evaluated on AFRIDOC-MT produces translations with English-centric structural patterns (calqued phrasing, parenthetical acronyms, transliterated drug names), these may be judged acceptable by d-chrF (since they match the references) but may be considered unnatural or confusing by MOH clinical translators or semi-literate patients — the actual end-users.
- **Datapoint citations:**
  - [D43] Example 4 (doc_health, split=train): "ፀረ-ተህዋሲያን - ፀረ-ባክቴሪያ ፣ፀረ-ቫይረስ ... 'ሱፐርበግስ(superbugs)'" — English loanword in Amharic parentheses suggests translated-from-English structural dependency.
  - [D47] Example 5 (doc_health, split=train): "ፀረ-ቫይረስ መድሃኒት ... ribavirin" — Untranslated drug name retained in Amharic text.

#### MINOR Concern 2: Sentence-level health config (`health`) contains highly varied content — some items have marginal clinical relevance
- **Dimension(s):** IC
- **Observation:** The `health` (sentence-level) config contains short, standalone sentences that are contextually disconnected from the document-level clinical narrative. Samples include health financing policy [D23], biological therapeutics standardization [D24], blood products [D40], and OCV sentence fragments [D12]. While individually these are within the "health" domain, their standalone nature removes the document context that makes clinical translation meaningful and assessable.
- **Deployment relevance:** Sentence-level evaluation without document context is less relevant for the deployment (clinical practice guidelines, maternal-health booklets) than document-level evaluation. The `doc_health` and chunked configs are better suited to the deployment's needs than the `health` sentence-level config.
- **Datapoint citations:**
  - [D23] Example 2 (health, split=train): "However, what is clear is that health systems need to predominantly rely on public revenue sources: mandatory, pre-paid and pooled" — Health financing sentence lacking clinical guideline register.
  - [D24] Example 3 (health, split=train): "the development and promotion of WHO international reference standards helps ensure that biological therapeutics are standardized between different manufacturers" — Regulatory/technical sentence without clinical patient-facing relevance.

#### MINOR Concern 3: Regional Amharic register variation across Ethiopia's health bureaus is unaddressed — single national-standard reference
- **Dimension(s):** OC
- **Observation:** The benchmark produces a single Amharic reference translation per document (by four translators working independently, with harmonization planned but not confirmed as completed). No sub-national or regional register variation (Tigray, Oromia, Somali, Amhara bureaus) is represented. The translators are identified by name but no regional affiliation is documented.
- **Deployment relevance:** The deployment serves multiple regional health bureaus where Amharic is used as a lingua franca by non-native speakers (Oromia, Tigray, Somali regions). Whether a single Addis Ababa-centric reference translation would be uniformly accepted as ground truth across all bureaus was not resolved in elicitation. This is a lower-severity concern given that Amharic dialects are mutually intelligible, but health register preferences may diverge, particularly for localized disease terminology or administrative terms.
- **Datapoint citations:**
  - [D1] Example 1 (doc_health, split=train): "የሞቃታማ ዐውሎ ነፋሶች" — A single Amharic rendering of "tropical cyclone" — whether this specific vocabulary choice would be accepted by health workers in Somali or Tigray regions is unverifiable.
  - [D4] Example 3 (doc_health, split=train): "ጨቅላ ህፃናት" (infant) — A single Amharic term for infant used consistently in the complementary feeding article; regional health registers may prefer alternative terminology.

---

### Content Coverage Summary

The sampled data contains a mixture of WHO health articles and Techpoint Africa technology news articles, all originating in English with human translations into Amharic, Hausa, Swahili, Yorùbá, and Zulu. The health corpus includes a wide range of WHO topics: maternal/infant nutrition (complementary feeding, breastfeeding), immunization/vaccination (cholera OCV, polio), disability, antimicrobial resistance, infectious diseases (CCHF, AMR), public health emergencies, and health systems governance (health financing, IHR, TRIPS). Medical terminology is present throughout the Amharic translations in Ethiopic script, including clinical terms, drug names (often transliterated), and health systems vocabulary.

Approximately half the sample is tech-domain (Techpoint Africa news), which is entirely irrelevant to the deployment. Within the health corpus, the most deployment-relevant subset — maternal-child health (complementary feeding, infant nutrition, breastfeeding) and immunization articles — constitutes a minority of the total health samples, with health policy, health financing, emergency preparedness, and globally generic disease topics occupying a substantial share. Document-level configs preserve multi-paragraph health articles; the sentence-level config provides shorter, context-free sentence pairs.

Amharic text quality in the available samples appears generally consistent in terms of script rendering and sentence fluency, but translator credential verification and MOH/EFDA terminology compliance cannot be assessed from the data alone.

---

### Limitations

1. **Sample size**: 51 examples were reviewed across 10 configs. The full benchmark contains 28,201 rows; the health domain has ~10,000 sentences and the tech domain ~10,000. The sampled examples provide directional evidence but cannot characterize the full distribution of topics, terminology choices, or translation quality across the entire corpus.

2. **Annotator credentials unverifiable from data**: The data rows themselves contain no metadata about translator credentials. Verification of MOH certification or clinical training background for the four Amharic translators requires direct contact with AFRIDOC-MT authors.

3. **MOH/EFDA glossary compliance unassessable from data alone**: No reference terminology list is included with the benchmark. Verifying whether specific Amharic term choices in the data conform to MOH/EFDA standards requires comparison against those glossaries, which are not publicly accessible in a verified form.

4. **Inter-annotator variation within the four Amharic translators unobservable in this sample**: The benchmark uses one translator per sentence (distributed equally), so single-document rows do not show variance across all four translators for the same passage. This limits assessment of translation consistency.

5. **Translationese extent not quantifiable from inspection**: Whether the Amharic translations exhibit systematic translationese effects (unnatural syntax, calqued phrase structure) requires native-speaker clinical evaluation beyond what visual inspection of the Ethiopic text can determine.

6. **GPT-4o judge output not directly observable**: The benchmark's GPT-4o evaluation results are reported in the paper but the per-document GPT-4o scores are not included in the HuggingFace dataset release, so the inconsistency documented for Amharic cannot be directly observed in the sampled rows.