## Dataset Analysis Report

**Dataset(s):** QCRI/CrisisBench-all-lang (configs: `humanitarian`, `informativeness`)
**Analysis date:** 2025-01-30
**Examples reviewed:** 131 (humanitarian, train split) + 140 (informativeness, train split) = 271 total
**Columns shown:** id, event, source, text, lang, lang_conf, class_label
**Columns skipped (media):** none (text-only dataset)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | humanitarian | Ex. 19 | displaced_and_evacuations | "El trabajo de la mejor Daniela López que conozco en pantalla grande #mataraunhombe #chile #cinema… http://t.co/asAx6KqNvD" | Spanish tweet about Chilean film, labelled displaced/evacuations — apparent annotation error | OC |
| D2 | humanitarian | Ex. 83 | sympathy_and_support | "RT @FlorrGo: #FuerzaChile ,un 2 de abril ... Que vengan los ingleses a ayudarlos ahora ... A la larga o a la corta ,todo vuelve" | Chilean Spanish earthquake solidarity tweet — not Argentine/Rioplatense | IC |
| D3 | humanitarian | Ex. 106 | sympathy_and_support | "Que lindo saber que en mi ciudad bella #Iquique hay gente con un corazón enorme dispuestos a ayudar... Emocionada" | Chilean Spanish (Iquique city) solidarity tweet — Chilean, not Argentine | IC |
| D4 | informativeness | Ex. 88 | not_informative | "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores" | Chilean Spanish tweet expressing contempt for requesting outside help — not Argentine | IC |
| D5 | informativeness | Ex. 89 | informative | "Declaran tres días de luto nacional por accidente de tren en España: Testigos afirman que el tren… http://t.co/pAcRQGdjFv" | Spanish-language tweet about Spain train crash | IC |
| D6 | informativeness | Ex. 37 | informative | "IMPRESIONANTE terremoto Chile camara de seguridad farmacia - NEW VIDEO E...: http://t.co/bkUElKfFUj vía @YouTube" | Chilean Spanish earthquake tweet — Chilean Spanish, not Rioplatense | IC |
| D7 | informativeness | Ex. 127 | informative | "RT @marieli_d: Nuevamente se incendia #Amuay http://t.co/AiWlhgy3" | Venezuelan Spanish tweet about refinery explosion | IC |
| D8 | humanitarian | Ex. 117 | not_humanitarian | "RT @meteomostoles: El tifón #BOPHA,de cat.4 y 947hPa en su centro,va camino de Filipinas.Lleva vientos sostenidos entre 2010 y 249km/h h ..." | Spanish tweet about Philippines typhoon — meteorological content labelled not_humanitarian | OC |
| D9 | informativeness | Ex. 106 | not_informative | "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree." | Chilean Spanish warning about over-donation — labelled not_informative despite substantive crisis-relevant content | OC |
| D10 | humanitarian | Ex. 102 | infrastructure_and_utilities_damage | "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport\nSaudi regime executes Indonesian women\nIran exports terrorism" | Political/conflict tweet from AIDR labelled infrastructure damage — apparent mislabel | OC |
| D11 | informativeness | Ex. 1 | informative | "when the ambushes of this century, hold closes even when life puts you in discomfiture, hold closes even that one of condescends your family, so God will facilitate you shortcoming" | Philosophical/religious text labelled informative — no disaster content | OC |
| D12 | informativeness | Ex. 3 | informative | "Sweater weather indeed 🌂 #RubyPH" | Short weather comment during typhoon labelled informative — minimal disaster signal | OC |
| D13 | informativeness | Ex. 7 | informative | "i hope everyone is safe" | Generic safety wish labelled informative | OC |
| D14 | informativeness | Ex. 83 | informative | "This hurricane thingy is looking pretty scary! I'm kinda excited by insane weather..." | Personal reaction labelled informative | OC |
| D15 | informativeness | Ex. 121 | informative | "one of the boston bombing suspects looks a bit like rob kardashian. do I have to wait for the new series to find out" | Celebrity comparison tweet during crisis labelled informative | OC |
| D16 | humanitarian | Ex. 9 | not_humanitarian | "New saying for the day... RG 3 and out - A #Steelers fan at the bar" | Sports commentary during Hurricane Sandy — clear not_humanitarian example | OO |
| D17 | humanitarian | Ex. 26 | personal_update | "Tornado watch until 3am. Of course we just got our new garage door today. *sigh*" | Personal complaint about tornado watch — Joplin 2011, North American event | IC |
| D18 | humanitarian | Ex. 11 | personal_update | "RT @tarnsnastylad: They need to name hurricanes better!.. superstorm Sandy? Seriously??.. Sounds like a FUCKING gay wrestler!" | Crude personal opinion during Sandy — North American vernacular | IC |
| D19 | humanitarian | Ex. 16 | affected_individual | "Floods kill 3, 75,000 forced from Calgary homes http://t.co/c6OPFjFLkA | AP #news" | News headline about Canadian flood — affected individuals, clear label | OO |
| D20 | humanitarian | Ex. 2 | caution_and_advice | "As many as 100,000 people could be forced from their homes by heavy flooding in western Canada. Water levels peak today at noon." | Factual caution about Canadian floods | OO |
| D21 | humanitarian | Ex. 57 | caution_and_advice | "RT @frankowolf1: il comune di Mirandola cerca ing. e arch. contattare Polizia Municipale: 0535/611039, 800/197197 #terremoto" | Italian tweet seeking engineers after earthquake — non-English caution | IC/IF |
| D22 | humanitarian | Ex. 30 | sympathy_and_support | "Mi è piaciuto un video di @YouTube: http://t.co/l5MttNyHPa Alluvione in Sardegna: commenti idioti" | Italian tweet about Sardinia floods — "liked a video about idiotic comments on flooding" | IC |
| D23 | humanitarian | Ex. 44 | sympathy_and_support | "Lac-Mégantic: Éric Forest sur place pour donner son appui http://t.co/wKSAXEtZWm" | French tweet about Canadian train crash — politician on site | IC |
| D24 | humanitarian | Ex. 113 | sympathy_and_support | "RT @portalR7: Tragédia no RS: Dilma chora ao falar sobre vítimas http://t.co/ybxETDmD #R7 #SantaMaria" | Portuguese tweet about Brazil nightclub fire, Dilma crying | IC |
| D25 | humanitarian | Ex. 95 | infrastructure_and_utilities_damage | "After deadly Brazil nightclub fire, safety questions emerge. http://t.co/ah4JK2v2" | Brazil nightclub fire — closest geographic proximity to Argentina | IO |
| D26 | humanitarian | Ex. 6 | infrastructure_and_utilities_damage | "The flood is feared to submerge the bridge roads leading Larkana and Khairpur districts." | Pakistan flood infrastructure — no Argentine geographic relevance | IC |
| D27 | humanitarian | Ex. 49 | infrastructure_and_utilities_damage | "Torrential rains have damaged Kenya's infrastructure, severing road links between Nairobi and Garissa, where the air base of the World Food Programme (WFP) is located." | Africa infrastructure damage — internationally framed | IC |
| D28 | informativeness | Ex. 34 | not_informative | "A tropical cyclone will affect my area. Winds of greater than 100 kph up to 185 kph may be expected in at least 18 hours. #TyphoonHagupit" | Substantive typhoon warning labelled not_informative — clear label inconsistency | OC |
| D29 | informativeness | Ex. 6 | not_informative | "#sobering Helicopter crash into pub in #glasgow! http://t.co/0uYSOocUvu" | Breaking news tweet labelled not_informative | OC |
| D30 | informativeness | Ex. 52 | not_informative | "Bangladesh:palazzo non era per fabbriche: Il progetto del Rana Plaza prevedeva solo 6 piani non 9 o 10 http://t.co/VG9qCqa3xX" | Italian investigative tweet about Rana Plaza building code — labelled not_informative | OC |
| D31 | humanitarian | Ex. 25 | other_relevant_information | "Update on the fertilizer explosion in West, Texas. Estimated 50 to 60 dead, hundreds injured, half of town flattened." | North American industrial explosion — would fit affected_individuals or injured_dead | OO |
| D32 | humanitarian | Ex. 52 | other_relevant_information | "being in a hurricane inside a house with no lights ..." | Personal experience tweet labelled other_relevant_information | OC |
| D33 | humanitarian | Ex. 111 | other_relevant_information | "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" | Completely unrelated home renovations tweet in other_relevant_information | OC |
| D34 | informativeness | Ex. 111 | informative | "RT @cityofcalgary: Acting Fire Chief, Ken Uzeloc, will address the media at Ogden Road and 17 Street S.E. at 10 p.m. #yyc #yycflood" | Official municipal announcement — clear informative label, Canadian context | OO |
| D35 | humanitarian | Ex. 28 | requests_or_needs | "I'M ASKING HELP FOR MY FAMILY WHICH IS VICTIM AND WHICH TAKE REFUGE IN PROVINCE." | Direct help request from disaster victim | OO |
| D36 | humanitarian | Ex. 42 | requests_or_needs | "We have water but we need food. Please in Masson Leogane." | Haiti-context needs request — Global South event | IO |
| D37 | humanitarian | Ex. 90 | requests_or_needs | "Equipped with a power generator and air conditioner, the tents can also house an emergency medical center." | Capability description mislabelled as requests_or_needs — annotation inconsistency | OC |
| D38 | humanitarian | Ex. 98 | requests_or_needs | "AmeriCares solicits donations of medicines, medical supplies, and other relief materials from manufacturers, and delivers them quickly and reliably to indigenous health and welfare professionals in 137 countries around the world." | NGO capability description labelled requests_or_needs — mislabel | OC |
| D39 | humanitarian | Ex. 1 | affected_individual | "@lucilledizon: 517 ilang ilang st. bayanihan vilage cainta rizal, David Bautista +63 905 826 5094. Needs rescue @MMDA @govph #rescuePH" | Tagalog rescue request — non-English, Philippine event, clear label | IF |
| D40 | humanitarian | Ex. 79 | infrastructure_and_utilities_damage | "RT @MoralesForLife: Chocolate Hills, napinsala ng Magnitude 7.2 na lindol #PrayForVisayas Pray For Cebu and Bohol also in Mindanao! http://…" | Tagalog tweet about Philippines earthquake damage | IF |
| D41 | informativeness | Ex. 23 | informative | "#Terremoto: secondo Il Foglio &egrave; un Castigo di Dio - foto http://t.co/GuMvqzl0" | Italian earthquake tweet labelled informative | IF |
| D42 | humanitarian | Ex. 14 | response_efforts | "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" | Clear response effort tweet — CARE NGO involvement | OO |
| D43 | humanitarian | Ex. 3 | disease_related | "Investors Pump Prospects Of Unproven Ebola Treatments: Drugs in development to treat Ebola virus are far from … http://t.co/hv7lcUzha3" | Ebola treatment investor article — disease_related | OO |
| D44 | humanitarian | Ex. 60 | infrastructure_and_utilities_damage | "Colorado floods shut down hundreds of oil and gas wells; recovery will take time: Colorado's oil and... http://t.co/HivwsVtrc8 #Oil #BRK" | North American oil/gas infrastructure damage | IO |
| D45 | informativeness | Ex. 128 | not_informative | "https://t.co/najVJNt4Ip DEATH TOLL Now under Investigation for COVER UP!!! https://t.co/VuGGPYboIv" | Credibility-ambiguous tweet about death toll cover-up labelled not_informative | OO |
| D46 | humanitarian | Ex. 24 | not_humanitarian | "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was." | Political commentary during Hurricane Maria | IC |
| D47 | informativeness | Ex. 31 | informative | "I was told I'm ignorant to think the Boston Bombing wasn't planned by the government to keep our attention away from schemes being planned." | Conspiracy tweet labelled informative | OC |
| D48 | humanitarian | Ex. 33 | disease_related | "Scientists find MERS virus antibodies that may lead to treatments http://t.co/0YAMcmulxD" | MERS treatment research tweet | OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Broad disaster type coverage across humanitarian labels
- **Dimension(s):** IO, OO
- **Observation:** The 15-class humanitarian label schema covers categories directly relevant to Argentine disaster response triage: `affected_individual`, `infrastructure_and_utilities_damage`, `injured_or_dead_people`, `displaced_and_evacuations`, `requests_or_needs`, `response_efforts`, `caution_and_advice`, and `donation_and_volunteering`. These top-level categories map onto the functional needs of Buenos Aires policy makers assessing disaster communication quality regardless of event geography.
- **Deployment relevance:** Argentine emergency management agencies (SINAGIR, AFE) operate within ISCRAM-derived frameworks that recognise these same broad categories. The label schema is thus sufficiently compatible with the international standards Argentine professionals treat as reference points.
- **Datapoint citations:**
  - [D19] Example 16 (humanitarian, train, affected_individual): "Floods kill 3, 75,000 forced from Calgary homes http://t.co/c6OPFjFLkA | AP #news" — straightforward affected-individuals label, clear annotation.
  - [D20] Example 2 (humanitarian, train, caution_and_advice): "As many as 100,000 people could be forced from their homes by heavy flooding in western Canada. Water levels peak today at noon." — clear actionable caution label.
  - [D35] Example 28 (humanitarian, train, requests_or_needs): "I'M ASKING HELP FOR MY FAMILY WHICH IS VICTIM AND WHICH TAKE REFUGE IN PROVINCE." — unambiguous needs signal.
  - [D42] Example 14 (humanitarian, train, response_efforts): "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" — clear response-efforts label.
  - [D43] Example 3 (humanitarian, train, disease_related): "Investors Pump Prospects Of Unproven Ebola Treatments: Drugs in development to treat Ebola virus are far from … http://t.co/hv7lcUzha3" — disease-related label functions.

#### Strength 2: Binary informativeness task provides a usable signal-triage foundation
- **Dimension(s):** OO, OF
- **Observation:** The informativeness config cleanly separates clearly off-topic social chatter from disaster-relevant content across a wide range of events. The not_informative examples in the sample include sports commentary, celebrity gossip, spam, and personal chitchat, while informative examples range from official municipal announcements to direct eyewitness reports.
- **Deployment relevance:** For Buenos Aires policy makers whose first-pass task is filtering noisy signals from informative crisis content, the binary informativeness layer provides a deployable triage function. Although it does not natively score credibility, it operationalises the first step in the downstream credibility pipeline the user envisions.
- **Datapoint citations:**
  - [D16] Example 9 (humanitarian, train, not_humanitarian): "New saying for the day... RG 3 and out - A #Steelers fan at the bar" — unambiguous noise example.
  - [D34] Example 111 (informativeness, train, informative): "RT @cityofcalgary: Acting Fire Chief, Ken Uzeloc, will address the media at Ogden Road and 17 Street S.E. at 10 p.m. #yyc #yycflood" — official institutional announcement correctly labelled informative.
  - [D36] Example 42 (humanitarian, train, requests_or_needs): "We have water but we need food. Please in Masson Leogane." — clear needs signal from Global South context.

#### Strength 3: Multi-event, multi-geography training distribution
- **Dimension(s):** IC, IO
- **Observation:** The 131 humanitarian examples span at least 20 named events across Asia, North America, South Asia, Europe, the Middle East, and Africa, including floods, earthquakes, hurricanes, disease outbreaks, industrial accidents, and building collapses. This breadth means classifiers trained on this data have exposure to diverse disaster communication registers, not just a single event type.
- **Deployment relevance:** Argentine disaster scenarios span floods, windstorms, earthquakes (low risk), and industrial accidents. A classifier trained on event-diverse data is less likely to fail categorically on event types that were absent from a narrower training set, even if Argentine-specific events are not present.
- **Datapoint citations:**
  - [D25] Example 95 (humanitarian, train, infrastructure_and_utilities_damage): "After deadly Brazil nightclub fire, safety questions emerge." — industrial accident type represented.
  - [D27] Example 49 (humanitarian, train, infrastructure_and_utilities_damage): "Torrential rains have damaged Kenya's infrastructure, severing road links between Nairobi and Garissa…" — African flood infrastructure — broad geographic spread.
  - [D44] Example 60 (humanitarian, train, infrastructure_and_utilities_damage): "Colorado floods shut down hundreds of oil and gas wells; recovery will take time…" — oil/gas infrastructure damage relevant to Argentine Vaca Muerta industrial context.

#### Strength 4: Presence of some non-English and non-North-American content
- **Dimension(s):** IC, IF
- **Observation:** The sampled examples include Italian (Ex. 30, 44, 57, 131 in informativeness), French (Ex. 44 humanitarian), Portuguese (Ex. 113 humanitarian), Tagalog (Ex. 1, 79, 93, 128 humanitarian), and multiple Spanish tweets (Ex. 19, 83, 106 humanitarian; Ex. 37, 67, 88, 89, 106, 127 informativeness). Language tags are present, enabling filtering. The CrisisMMD 2017 events add international disaster diversity.
- **Deployment relevance:** While none of the Spanish content is Argentine or Rioplatense, its presence demonstrates the dataset is not exclusively US/UK English and that non-Latin-alphabet and Romance-language registers have been annotated. For a deployment that must handle multilingual input streams, the label schema has at least been exposed to non-English content at the margins.
- **Datapoint citations:**
  - [D21] Example 57 (humanitarian, train, caution_and_advice): "RT @frankowolf1: il comune di Mirandola cerca ing. e arch. contattare Polizia Municipale: 0535/611039, 800/197197 #terremoto" — Italian caution/advice tweet correctly labelled.
  - [D39] Example 1 (humanitarian, train, affected_individual): "@lucilledizon: 517 ilang ilang st. bayanihan vilage cainta rizal, David Bautista +63 905 826 5094. Needs rescue @MMDA @govph #rescuePH" — Tagalog rescue request correctly labelled affected_individual.
  - [D5] Example 89 (informativeness, train, informative): "Declaran tres días de luto nacional por accidente de tren en España: Testigos afirman que el tren… http://t.co/pAcRQGdjFv" — Spanish-language disaster tweet labelled informative.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of Argentine or Rioplatense Spanish content
- **Dimension(s):** IC, IF
- **Observation:** All 271 sampled examples contain zero instances of Argentine events, Argentine institutional actors, or Rioplatense Spanish. The Spanish-language tweets in the sample are Chilean (events: `2014_chile_earthquake`, `2014_chile_earthquake_esp`), Venezuelan (`2012_venezuela_refinery-explosion`), and Spanish (`2013_spain_train-crash_en-mixed`). No lunfardo register, no Argentine agency names (SINAGIR, AFE, SENAPRED), no Buenos Aires Metropolitan Area geography, no Rioplatense voseo constructions, and no Argentine political framing appear anywhere in the sample.
- **Deployment relevance:** The deployment's core channel — Argentine Twitter/X — features Rioplatense Spanish with distinctive lexical, syntactic, and pragmatic features (voseo, lunfardo, political satire, institutional irony) that are entirely absent from the training distribution. A classifier trained on this benchmark will encounter an out-of-distribution linguistic register on every Spanish-language Argentine social media post it processes. This is the single most consequential alignment gap for the deployment.
- **Datapoint citations:**
  - [D2] Example 83 (humanitarian, sympathy_and_support): "RT @FlorrGo: #FuerzaChile ,un 2 de abril ... Que vengan los ingleses a ayudarlos ahora ... A la larga o a la corta ,todo vuelve" — Chilean Spanish, not Argentine; no Rioplatense register.
  - [D3] Example 106 (humanitarian, sympathy_and_support): "Que lindo saber que en mi ciudad bella #Iquique hay gente con un corazón enorme dispuestos a ayudar... Emocionada" — Iquique is in Chile; no Argentine content.
  - [D6] Example 37 (informativeness, informative): "IMPRESIONANTE terremoto Chile camara de seguridad farmacia - NEW VIDEO E...: http://t.co/bkUElKfFUj vía @YouTube" — Chilean earthquake, Chilean Spanish.
  - [D7] Example 127 (informativeness, informative): "RT @marieli_d: Nuevamente se incendia #Amuay http://t.co/AiWlhgy3" — Venezuelan refinery explosion; Venezuelan Spanish.

#### Concern 2: No credibility, misinformation, or source reliability dimension in the output schema
- **Dimension(s):** OO, OF
- **Observation:** Neither the humanitarian nor informativeness config contains any label, score, or metadata field relating to source credibility, institutional authority, misinformation likelihood, or signal reliability. The schema fields are: id, event, source, text, lang, lang_conf, class_label. The `source` field records dataset provenance (e.g., `crisismmd`, `crisisnlp-cf`), not tweet author credibility. No tweet-level credibility metadata is present.
- **Deployment relevance:** The primary output requirement for the Buenos Aires policy-maker cohort is a trustworthiness or reliability score. The benchmark produces only binary informativeness and multi-class humanitarian type labels. This gap is user-acknowledged as requiring downstream construction, but the data itself provides no foundation for learning source credibility signals. Notably, Example D45 (a "DEATH TOLL Now under Investigation for COVER UP!!!" tweet labelled not_informative) and D47 (a conspiracy tweet labelled informative) illustrate that the existing labels do not align with a credibility axis — credible and non-credible content appear on both sides of the informativeness divide.
- **Datapoint citations:**
  - [D45] Example 128 (informativeness, not_informative): "https://t.co/najVJNt4Ip DEATH TOLL Now under Investigation for COVER UP!!! https://t.co/VuGGPYboIv" — credibility-ambiguous sensationalist content labelled not_informative; offers no credibility signal.
  - [D47] Example 31 (informativeness, informative): "I was told I'm ignorant to think the Boston Bombing wasn't planned by the government to keep our attention away from schemes being planned." — conspiracy content labelled informative, illustrating that informativeness ≠ credibility.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport\nSaudi regime executes Indonesian women\nIran exports terrorism" — political conflict content labelled infrastructure damage; no credibility dimension.

---

#### MAJOR

#### Concern 3: Substantial annotation noise and label inconsistency observable in sample
- **Dimension(s):** OC
- **Observation:** Multiple examples in both configs exhibit annotation patterns that would be inconsistent or incorrect by any reasonable standard, suggesting the label quality the deployment would be training/evaluating against is uneven. Specific problems observed: (a) a Chilean Spanish tweet about a cinema film labelled `displaced_and_evacuations`; (b) an NGO capability description labelled `requests_or_needs`; (c) a tent/generator infrastructure description labelled `requests_or_needs`; (d) a substantive typhoon warning labelled `not_informative`; (e) a Long Island home renovations advertisement in `other_relevant_information`; (f) a political conflict tweet labelled `infrastructure_and_utilities_damage`.
- **Deployment relevance:** For a deployment where policy makers need reliable classification outputs to feed a credibility scoring pipeline, noisy ground-truth labels reduce the trustworthiness of any model trained or evaluated on this benchmark. Cross-dataset F1 degradation (14.3%, noted in the YAML) is at least partially explained by these label inconsistencies. Argentine stakeholders calibrating against this benchmark may encounter a noisy signal floor that undermines the pipeline's practical utility.
- **Datapoint citations:**
  - [D1] Example 19 (humanitarian, displaced_and_evacuations): "El trabajo de la mejor Daniela López que conozco en pantalla grande #mataraunhombe #chile #cinema…" — Chilean film discussion labelled displaced_and_evacuations; likely annotation error.
  - [D37] Example 90 (humanitarian, requests_or_needs): "Equipped with a power generator and air conditioner, the tents can also house an emergency medical center." — capability description, not a request; mislabelled.
  - [D38] Example 98 (humanitarian, requests_or_needs): "AmeriCares solicits donations of medicines, medical supplies, and other relief materials from manufacturers, and delivers them quickly and reliably to indigenous health and welfare professionals in 137 countries around the world." — NGO mission statement labelled requests_or_needs; more accurately donation_and_volunteering or response_efforts.
  - [D28] Example 34 (informativeness, not_informative): "A tropical cyclone will affect my area. Winds of greater than 100 kph up to 185 kph may be expected in at least 18 hours. #TyphoonHagupit" — specific quantitative typhoon warning labelled not_informative.
  - [D33] Example 111 (humanitarian, other_relevant_information): "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" — entirely unrelated home renovation content in other_relevant_information.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi\nAl-Qaeda seizes Yemen airport…\nIran exports terrorism" — political/conflict listing labelled infrastructure damage.

#### Concern 4: Informativeness label boundaries are culturally unstable for Argentine social media
- **Dimension(s):** OC, IC
- **Observation:** Several examples labelled `informative` in the sample carry minimal disaster-relevant content by any standard, while content with substantive disaster information is sometimes labelled `not_informative`. The observed boundary appears to conflate "crisis-adjacent" with "informative," accepting sympathetic sentiment tweets, celebrity references, and personal reactions as informative. Argentine Twitter/X discourse is characterised by political satire and institutional irony — content that superficially resembles the `not_informative` patterns in the benchmark but may carry genuine crisis signals.
- **Deployment relevance:** If the Argentine deployment system inherits these ambiguous label boundaries, it risks classifying Argentine political commentary on government crisis response as not_informative (missing real signals) or misclassifying satirical content as informative. This is particularly acute given the noted Argentine norm of political framing in crisis coverage and the dissolution of Télam, which has dispersed official crisis communication signals across a more fragmented landscape.
- **Datapoint citations:**
  - [D11] Example 1 (informativeness, informative): "when the ambushes of this century, hold closes even when life puts you in discomfiture, hold closes even that one of condescends your family, so God will facilitate you shortcoming" — philosophical/religious text with no disaster content, labelled informative.
  - [D12] Example 3 (informativeness, informative): "Sweater weather indeed 🌂 #RubyPH" — weather comment during typhoon labelled informative; near-zero disaster signal.
  - [D13] Example 7 (informativeness, informative): "i hope everyone is safe" — generic sentiment, labelled informative.
  - [D14] Example 83 (informativeness, informative): "This hurricane thingy is looking pretty scary! I'm kinda excited by insane weather..." — personal reaction, labelled informative.
  - [D29] Example 6 (informativeness, not_informative): "#sobering Helicopter crash into pub in #glasgow! http://t.co/0uYSOocUvu" — breaking news tweet labelled not_informative despite containing disaster event reference.
  - [D30] Example 52 (informativeness, not_informative): "Bangladesh:palazzo non era per fabbriche: Il progetto del Rana Plaza prevedeva solo 6 piani non 9 o 10 http://t.co/VG9qCqa3xX" — Italian investigative report on building code violation labelled not_informative.

#### Concern 5: North American and North Atlantic event dominance distorts register and cultural framing
- **Dimension(s):** IC
- **Observation:** The personal_update and not_humanitarian categories are dominated by North American vernacular English: American sports references, US political discourse, and North American cultural referents. Personal_update examples include Sandy-era tweets referencing Joplin tornado and North American colloquial register. The social chatter that the benchmark trains models to recognise as "noise" is specifically North American social noise, not Argentine social noise.
- **Deployment relevance:** Argentine social media "noise" differs structurally from US social media noise: it includes political satire of the Milei government's handling of floods, lunfardo-inflected commentary, references to local institutional actors (AMBA prefectura, Buenos Aires province civil defense), and WhatsApp-style forwarded messages. A classifier trained to recognise US sports commentary as not_informative may misclassify Argentine political satire about disaster response — which could carry real signals about institutional credibility — in either direction.
- **Datapoint citations:**
  - [D17] Example 26 (humanitarian, personal_update): "Tornado watch until 3am. Of course we just got our new garage door today. *sigh*" — North American personal complaint about Joplin tornado watch; this is the register the classifier learns as "personal_update."
  - [D18] Example 11 (humanitarian, personal_update): "RT @tarnsnastylad: They need to name hurricanes better!.. superstorm Sandy? Seriously??.. Sounds like a FUCKING gay wrestler!" — North American vernacular during Sandy.
  - [D46] Example 24 (humanitarian, not_humanitarian): "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was." — US political commentary during Hurricane Maria labelled not_humanitarian; analogue Argentine political commentary on AFE crisis response would face the same classification challenge.

#### Concern 6: Spanish-language examples present carry Chilean/Venezuelan register, not Rioplatense, and show annotation inconsistency
- **Dimension(s):** IC, OC
- **Observation:** The Spanish-language examples in the sample are all from Chilean or Venezuelan events and use standard Chilean/Venezuelan register. One Chilean Spanish tweet (Ex. 88, informativeness: "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores") reflects Chilean political sentiment about foreign aid and is labelled not_informative. Another substantive Spanish tweet with disaster hashtags (Ex. 106, informativeness: "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree.") is also labelled not_informative despite containing a crisis-relevant public warning about aid logistics. This suggests the annotation schema may systematically under-recognise disaster-relevance in Spanish-language content.
- **Deployment relevance:** If Spanish-language disaster warnings are being labelled not_informative in the benchmark, any model trained on this data will be systematically biased against recognising Spanish-language disaster signals — directly undermining the Argentine deployment's core function of triage across Spanish-language social media content.
- **Datapoint citations:**
  - [D9] Example 106 (informativeness, not_informative): "Ojo con el exceso de ayuda por los efectos del #TerremotoenChile porque puede producir mucho más obstáculos de lo que se cree." — crisis-relevant Spanish warning about aid logistics labelled not_informative.
  - [D4] Example 88 (informativeness, not_informative): "#FuerzaChile jaja y piden ayuda jaja que los ayuden los ingleses manga de traidores" — Chilean political sentiment during earthquake, not_informative.
  - [D8] Example 117 (humanitarian, not_humanitarian): "RT @meteomostoles: El tifón #BOPHA,de cat.4 y 947hPa en su centro,va camino de Filipinas.Lleva vientos sostenidos entre 2010 y 249km/h h ..." — Spanish-language meteorological warning about a typhoon labelled not_humanitarian, despite containing specific wind-speed and track data.

---

#### MINOR

#### Concern 7: `other_relevant_information` class is a heterogeneous catch-all with low semantic coherence
- **Dimension(s):** OO, OC
- **Observation:** The `other_relevant_information` class in the humanitarian config functions as a residual bucket containing content ranging from clear factual updates ("PAGASA says typhoon has further weakened") to personal experience tweets ("being in a hurricane inside a house with no lights") to a benefit concert announcement to a completely unrelated home renovations advertisement. This class's semantic incoherence limits its usefulness as a training or evaluation signal.
- **Deployment relevance:** For a deployment trying to classify Argentine crisis communication quality, a 13% catch-all class (166/500 buffer examples are other_relevant_information) that conflates substantive updates with noise will produce unreliable outputs for borderline content — precisely the category most relevant to a credibility scoring task where the interesting cases are not clearly informative or clearly noise.
- **Datapoint citations:**
  - [D32] Example 52 (humanitarian, other_relevant_information): "being in a hurricane inside a house with no lights ..." — personal experience, arguably not crisis-informative.
  - [D31] Example 25 (humanitarian, other_relevant_information): "Update on the fertilizer explosion in West, Texas. Estimated 50 to 60 dead, hundreds injured, half of town flattened." — this appears to be injured_or_dead_people or affected_individual rather than other_relevant_information.
  - [D33] Example 111 (humanitarian, other_relevant_information): "Check out these award winning Long Island renovations: #longisland #suffolk https://t.co/wLnIbOENK9" — entirely unrelated content; should be not_humanitarian.

#### Concern 8: Temporal gap — all events 2010–2017; Argentine institutional landscape has changed materially since 2017
- **Dimension(s):** IC
- **Observation:** All events in the sample span 2010–2017 (oldest: 2011 Joplin tornado; newest: 2017 Hurricane Maria/Irma/Harvey). The Argentine institutional context relevant to the deployment has changed substantially since 2017: Télam was dissolved in July 2024, AFE was created in 2025, and the current political environment (Milei administration) has altered the credibility landscape for official disaster communications.
- **Deployment relevance:** Social media conventions, platform norms (Twitter/X after Musk acquisition), and Argentine institutional credibility signals have all shifted since 2017. A classifier trained on 2010–2017 tweet patterns may misclassify post-2022 content that uses different hashtagging conventions, link formats, and institutional citation patterns.
- **Datapoint citations:**
  - [D17] Example 26 (humanitarian, personal_update): "Tornado watch until 3am." (2011 Joplin) — oldest event; Twitter conventions of 2011 differ from 2024.
  - [D46] Example 24 (humanitarian, not_humanitarian): "RT @eclecticbrotha: @AlGiordano Damn, I forgot how much of a shitshow Bernie's Puerto Rico operation was. https://t.co/DgZMF2qnNl" — 2017 Hurricane Maria, pre-Musk Twitter, pre-Télam dissolution.

#### Concern 9: `lang_conf` field is missing (NA) for many CrisisMMD and AIDR examples, complicating language-stratified filtering
- **Dimension(s):** IF
- **Observation:** A large number of examples from `crisismmd` and `aidr_system` sources have `lang_conf: NA` rather than a numeric confidence score. This means the language detection confidence is unavailable for these examples, making it impossible to filter by language detection reliability. Given that the deployment needs to handle Spanish-language content differently from English content, the absence of confidence scores for a significant subset of examples weakens the language-stratification capability of the dataset.
- **Deployment relevance:** For the Argentine deployment, reliable language identification is prerequisite to routing content to appropriate classifiers (English vs. Spanish models). The NA confidence values in the CrisisMMD and AIDR subsets — which include 2017 events most temporally proximate to the deployment window — reduce confidence in automated language-based routing decisions built on this benchmark's language metadata.
- **Datapoint citations:**
  - [D5] Example 5 (humanitarian, donation_and_volunteering): "#Fox914 encourages you to unite and give to those who are affected... #FloodSL #srilanka #colombo #kandy #lka https://t.co/iLgsSCJ06b" — `lang_conf: NA` from crisismmd source.
  - [D42] Example 14 (humanitarian, response_efforts): "#Tacloban has 49 evacuation centers now sheltering over 30,000 people + @care is helping respond to #typhoonhagupit http://t.co/ePE9MsdpTh" — `lang_conf: NA` from crisisnlp-volunteers source.
  - [D10] Example 102 (humanitarian, infrastructure_and_utilities_damage): "Middle East right now:\nIS about to seize Ramadi…" — `lang_conf: NA` from aidr_system source.

---

### Content Coverage Summary

The 271 sampled examples reveal a dataset that is predominantly English-language (~88% of sampled examples), drawn from North American and global events spanning 2010–2017, with a strong concentration in US hurricanes (Sandy, Harvey, Irma, Maria), Philippines typhoons, Nepal earthquake, Pakistan floods, and Joplin tornado. The humanitarian config represents 15 classes with notable imbalance: `not_humanitarian` and `other_relevant_information` together account for the majority of buffer-sampled examples (366/500), consistent with the documented 37.4% not_humanitarian rate. Non-English content is present but sparse: Italian (3–4 examples), French (1), Portuguese (1), Tagalog (4–5), and Spanish (6–8 examples), all from non-Argentine events. The Spanish content is exclusively Chilean and Venezuelan.

Register is predominantly short-form social media (Twitter), ranging from professional news retweets to personal social chatter, with some longer structured text from the DRD (Figure Eight) dataset representing more formal humanitarian situation reports. The DRD examples are notably different in register from tweets — they read as structured field reports or aid request forms — introducing within-benchmark register heterogeneity. The `other_relevant_information` class functions as a heterogeneous residual category. Label quality is uneven, with observable annotation errors in both configs that reduce confidence in benchmark scores as indicators of real-world classification capability.

No Argentine, Rioplatense Spanish, Buenos Aires-specific, or Pampa/Patagonia/Río de la Plata content appears in the sample. The hazard types represented (North Atlantic hurricanes, South Asian floods, Philippines typhoons, North American tornadoes) do not include pampero windstorms, sudestada events, ENSO-driven droughts, or urban flash floods in dense Latin American metropolitan settings.

---

### Limitations

1. **Sample size per class:** The stratified buffer over 15 humanitarian classes produces small per-class samples (2–25 examples for rare classes like `displaced_and_evacuations`, `missing_and_found_people`, `personal_update`). Annotation quality and label consistency observations for these rare classes are based on 2–4 examples and should be treated as directional, not definitive.

2. **Train split only:** All examples are from the train split. Test and dev split distributions, label quality, and language composition are not directly inspected and may differ.

3. **No access to raw tweet metadata:** The dataset provides text, event, source, lang, and class_label, but not tweet author metadata (account type, follower count, verified status), timestamps, or geolocation — all relevant to the deployment's credibility scoring aspiration. The absence of these fields from the schema is a structural limitation of the dataset, not a sampling artefact.

4. **Language detection accuracy unverified:** The `lang` field relies on Google Cloud Language Detection API. Misdetections (e.g., short tweets, code-switched content) cannot be verified from the text alone for non-Latin-script or mixed-language examples.

5. **CrisisMMD multimodal data:** CrisisMMD was originally a multimodal dataset (tweets + images). The HF dataset appears to contain only the text component. Image-based disaster signals from CrisisMMD are not inspectable or evaluated here.

6. **Informativeness label semantics vary by source dataset:** The informativeness label maps from different original schemas (relevant/not-relevant in DSM; informative/not-informative in CrisisLex). The observed label inconsistencies in the informativeness config may partly reflect this multi-source mapping rather than annotation error within any single source.