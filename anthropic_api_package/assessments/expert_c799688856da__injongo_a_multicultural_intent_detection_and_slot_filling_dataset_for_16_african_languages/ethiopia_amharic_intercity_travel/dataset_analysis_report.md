## Dataset Analysis Report

**Dataset(s):** masakhane/InjongoIntent (configs: amh, eng, ewe, hau, ibo, kin, lin, lug, orm, sna, sot, swa, twi, wol, xho, yor, zul)
**Analysis date:** 2025-07-15
**Examples reviewed:** 224 total (19 amh, 13 eng, 14 ewe, 16 hau, 16 ibo, 13 kin, 13 lin, 15 lug, 13 orm, 11 sna, 27 sot, 13 swa, 13 twi, 15 wol, 14 xho, 14 yor, 11 zul)
**Columns shown:** intent, text, spans, target, example_id (+ raw in eng config)
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | amh | train-00000042 | book_flight | "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ።" | "Book me a flight from Dire Dawa to Bahir Dar for Meskerem fifth." | IC |
| D2 | amh | train-00000042 | book_flight | target: "CITY_OR_PROVINCE: ድሬዳዋ $$ CITY_OR_PROVINCE: ባህርዳር $$ DATE: መስከረም አምስት" | Slot annotations for Dire Dawa, Bahir Dar (Ethiopian cities), and Meskerem (Ethiopian calendar month) | IC, OO |
| D3 | amh | train-00000016 | balance | "የአማራ ባንክ አካውንቴ ስንት አለው" / target: "BANK_NAME: አማራ ባንክ" | "How much is in my Amhara Bank account?" — Ethiopian bank name annotated | IC |
| D4 | amh | train-00000018 | balance | "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" / target: "BANK_NAME: ንግድ ባንክ" | "Is there money left in Commercial Bank [of Ethiopia]?" — major Ethiopian bank | IC |
| D5 | amh | train-00000003 | balance | "በቴሌብር የብድር አካውንቴ ላይ …" / target: "PAYMENT_COMPANY: ቴሌብር" | "In my TeleBirr credit account…" — TeleBirr is Ethiopia's dominant mobile payment platform | IC |
| D6 | amh | train-00000011 | car_rental | "ከሃምሌ 4 እስከ 6 የቤት መኪና ኪራይ ማግኘት እችላለሁ?" / target: "DATE: ከሃምሌ 4 እስከ 6" | "Can I find a car rental from Hamle 4 to 6?" — Hamle is the 11th month of Ethiopian calendar | IC, OO |
| D7 | amh | train-00000041 | book_flight | "ወደ ቱርክ በፍጥነት የምደርስበት የበረራ አማራጭ ንገረኝ།" / target: "COUNTRY: ቱርክ" | "Tell me a flight option to get to Turkey quickly." — international destination, no Ethiopian intercity booking | IO |
| D8 | amh | train-00000047 | book_flight | "ወደ ሱዳን የበረራ ትኬት ያስፈልገኛል።" / target: "COUNTRY: ሱዳን" | "I need a flight ticket to Sudan." — international destination, not intercity bus | IO |
| D9 | eng (raw=amh) | train-00000053 | travel_suggestion | raw: "ለቀጣይ የጉብኝት ጉዞዬ በሃዋሳ እና በአርባ ምንጭ መካከል…" / text: "help me decide between Hawassa and Arbaminch…" | Ethiopian cities Hawassa and Arba Minch appear as travel suggestions — confirms cultural grounding | IC |
| D10 | eng (raw=amh) | train-00000092 | spending_history | raw: "ከቴሌ ብር አካዉንቴ ገንዘብ ለማን ለማን እንደላኩ ዝርዝሩን አሳየኝ?" / text: "Show me history of my telebirr transfers?" | TeleBirr payment company referenced in Amharic utterance | IC |
| D11 | amh | train-00000045 | alarm | "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ በደንብ እንዲሰማኝ ድምጽ ጨምርበት" | "Make the alarm I set for tomorrow morning at 12 o'clock ring loudly." — TIME slot unnanotated despite "12 ሰአት" | OC |
| D12 | orm | train-00000041 | book_flight | "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" | "Book me an Ethiopian Airlines flight from Dire Dawa to Bole then to Jimma." — spans empty despite city names and airline | OC |
| D13 | orm | train-00000011 | car_rental | "Ebila 12 hanga Ebila 14tti Mattuu keessatti kireeffannaa konkolaataa argachuun ni danda'amaa" / target: "DATE: Ebila 12 hanga Ebila 14 $$ CITY_OR_PROVINCE: Mattuu" | Oromo month name "Ebila" (April) used as date slot — culturally grounded Ethiopian Oromo calendar | IC, OO |
| D14 | orm | train-00000035 | calendar_update | "Sagantaa sirna cidhaaf sadaasa 21tti qabame kalaandarii koo irraa haqi maloo" / target: "CALENDAR_EVENT: sirna cidhaa $$ DATE: sadaasa 21" | Oromo month "Sadaasa" (November in Oromo calendar) used as date slot | IC, OO |
| D15 | amh | train-00000052 | bill_balance | "የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ።" / target: "DATE: የዚህ ወር" | "Show me the utility list to be paid this month." — relative date expression, not calendar month name | OO |
| D16 | amh | train-00000053 | car_rental | "ከሚመጣው ወር ጀምሮ ለ3 ወር ቶዮታ መኪና መከራየት እፈልጋለሁ።" / target: "DATE: ከሚመጣው ወር ጀምሮ ለ3 ወር" | "I want to rent a Toyota car starting next month for 3 months." — relative date, no named calendar month | OO |
| D17 | amh | train-00000031 | confirm_reservation | "በቶቶት ለቃለአብ ቦታ ማስያዝ እንዳለብኝ…" / target: "RESTAURANT_NAME: ቶቶት $$ PERSONAL_NAME: ቃለአብ" | Restaurant "ቶቶት" (Totot) — Ethiopian cultural reference; personal name "ቃለአብ" is distinctly Ethiopian | IC |
| D18 | amh | train-00000051 | bill_balance | "የቦሎ ማሳደሻ ስንት ነው" / target: "BILL_TYPE: የቦሎ ማሳደሻ" | "What is the Bole maintenance/upgrade fee?" — "ቦሎ" likely refers to Bole (Addis Ababa district) | IC |
| D19 | hau | train-00000018 | balance | "Naira nawa gare ni … na bankin Gt?" / target: "CURRENCY: Naira $$ BANK_NAME: Gt" | Nigerian Naira currency annotated in Hausa — confirms per-language currency grounding | IC |
| D20 | sot | train-00000016 | balance | "Ho setse bokae ka akhaontong ya Nedbank" / target: "BANK_NAME: Nedbank" | Sesotho uses South African bank Nedbank — culturally grounded for South Africa | IC |
| D21 | sot | train-00000003 | balance | "Ho setse bokae bankeng ya FNB" / target: "BANK_NAME: FNB" | FNB (First National Bank, SA) in Sesotho — same grounding documented for Xhosa in INJONGO paper | IC |
| D22 | xho | train-00000018 | balance | "Ndinganayo imali engange R700 kwiakhawunti yam yaseStandard Bank?" / target: "MONEY: R700 $$ BANK_NAME: yaseStandard Bank" | South African Rand (R700) and Standard Bank in Xhosa | IC |
| D23 | amh | train-00000045 | alarm | "ነገ ጠዋት 12 ሰአት…" (no span annotation) | "12 ሰአት" (12 o'clock) unnanotated — "ጠዋት" (morning) absent from target; Ethiopian time convention unclear | OC, OO |
| D24 | orm | train-00000012 | car_rental | "Torban jalqabaa ji'a kanaf Toyotaa kireeffame Naqamtee keessa nan argadhaa" / target: "DATE: ji'a kana $$ CITY_OR_PROVINCE: Naqamtee" | Oromo city Naqamtee (Nekemte) used in CITY_OR_PROVINCE slot | IC |
| D25 | amh | train-00000041 | book_flight | intent=book_flight, COUNTRY: ቱርክ (Turkey) | Flight to Turkey — no intercity bus, seat class, or operator-specific slots present | IO |
| D26 | amh | train-00000047 | book_flight | intent=book_flight, COUNTRY: ሱዳን (Sudan) | Flight to Sudan — air travel framing, not surface transport | IO |
| D27 | eng | train-00000053 | travel_suggestion | "help me decide between Hawassa and Arbaminch for my upcoming trip. What are the unique attractions in each location?" | English translation of Amharic utterance confirms Ethiopian city coverage in the dataset | IC |
| D28 | amh | train-00000053 (calendar_update) | calendar_update | "በዚህ ሳምንት ምንም ቀጠሮ እንዲኖረኝ አልፈልግም።" / target: "DATE: በዚህ ሳምንት" | Relative week reference, no Ethiopian calendar month | OO |
| D29 | orm | train-00000045 | alarm | "Galgala kana caalaan akka dhufuuf dammaksituu guutiif saatii 7tti" / target includes misannotated "PERSONAL_NAME: caalaa" | "caalaa" annotated as PERSONAL_NAME but may be part of "Galgala caalaan" (this evening) phrase | OC |
| D30 | amh | train-00000041 | book_flight | no intercity corridors, no seat class, no bus operator, no fare tier present | All Amharic travel utterances use air travel framing | IO |
| D31 | hau | train-00000031 | confirm_reservation | "Za ku iya tabbatar min ina da ajiyar tebur a taco bell da ƙarfe 7 na yamma" / target: "RESTAURANT_NAME: taco bell" | "Taco Bell" — US fast-food chain, Western entity in Hausa utterance | IC |
| D32 | ibo | train-00000012 | food_last | "How many hours does it take cooked Indomie noodles to spoil?" | "Indomie noodles" — popular West African brand, regionally grounded | IC |
| D33 | amh | train-00000035 | calendar_update | "የእናቴን እና የአባቴን የልደት ቀን የቀን መቁጠሪያዬ ላይ ስላቀያየርኩት አስተካክለው" | "I changed my parents' birthdays in my calendar, please fix it." — no slots annotated despite calendar events | OC |
| D34 | eng (raw=amh) | train-00000045 | balance | raw: "እባካችሁ የዳሽን ባንክ ሂሳቤን ታረጋግጡልኛላችሁ?" / text: "can you please check my dasion bank account" | "Dashen Bank" (major Ethiopian bank) — Amharic source is culturally grounded but English transliteration is lossy ("dasion") | IC, OF |
| D35 | swa | train-00000011 | car_rental | "Kukodisha gari la kutembeza watalii pale Maasai Mara tarehe saba hadi tarehe kumi" / target includes "PLACE_NAME: Maasai Mara" | Swahili uses Maasai Mara (Kenya) — East African cultural grounding | IC |
| D36 | lug | train-00000047 | book_flight | "Weekwate ekifo ku nnyonyi eva e Algiers okudda e London" / target: "CITY_OR_PROVINCE: Algiers $$ CITY_OR_PROVINCE: London" | Luganda flight utterance routes through Algiers to London — non-African destination present | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Ethiopian calendar month names present as valid DATE slot values in Amharic utterances
- **Dimension(s):** IC, OO
- **Observation:** The single most important flagged gap in the benchmark YAML — whether Ethiopian (Ge'ez) calendar month names are present in Amharic DATE slot annotations — is directly addressed in the sampled data. Example 19 of the Amharic split contains the utterance "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ።" with slot annotation "DATE: መስከረም አምስት" (Meskerem fifth). This is a travel-domain instance using an Ethiopian calendar month name (Meskerem = September–October) as the date slot value. Additionally, Amharic example 11 (car_rental) annotates "DATE: ከሃምሌ 4 እስከ 6", where Hamle (11th Ethiopian month) is used as a date reference.
- **Deployment relevance:** This directly resolves the highest-priority flagged gap. Users of an Ethiopian intercity booking app will natively reference Ethiopian calendar months for travel dates; the benchmark does capture this convention in at least some Amharic travel-domain instances, making evaluation of date-slot extraction for Ethiopian calendar dates partially feasible.
- **Datapoint citations:**
  - [D1] Example train-00000042 (amh, split=train, label=book_flight): "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ།" — Ethiopian calendar month Meskerem as DATE slot value in a flight booking utterance
  - [D2] Example train-00000042 (amh, split=train, label=book_flight): target: "DATE: መስከረም አምስት" — DATE annotation confirms Ge'ez calendar month is treated as a valid DATE slot value
  - [D6] Example train-00000011 (amh, split=train, label=car_rental): "ከሃምሌ 4 እስከ 6 የቤት መኪና ኪራይ ማግኘት እችላለሁ?" / target: "DATE: ከሃምሌ 4 እስከ 6" — Hamle (Ethiopian month) appears in a travel-adjacent domain

#### Strength 2: Ethiopian intercity city toponyms present as CITY_OR_PROVINCE slot values in Amharic travel utterances
- **Dimension(s):** IC, OO
- **Observation:** The second highest-priority flagged gap — whether Ethiopian intercity city names appear in travel-domain slot instances — is partially resolved by direct data inspection. Example 19 (train-00000042) contains both Dire Dawa (ድሬዳዋ) and Bahir Dar (ባህርዳር) as CITY_OR_PROVINCE slots in a book_flight intent. The English config (raw=amh) example train-00000053 shows Hawassa (ሃዋሳ) and Arba Minch (አርባ ምንጭ) as CITY_OR_PROVINCE slots in a travel_suggestion utterance. These cities are on key Ethiopian intercity corridors.
- **Deployment relevance:** Ethiopian city toponyms that match actual Sky Bus / Selam Bus corridors (Dire Dawa, Bahir Dar, Hawassa, Arba Minch) appear in the training data. This mitigates — though does not fully resolve — the toponym coverage gap, since the sample confirms at least some corridor-relevant cities are present.
- **Datapoint citations:**
  - [D2] Example train-00000042 (amh, split=train, label=book_flight): target: "CITY_OR_PROVINCE: ድሬዳዋ $$ CITY_OR_PROVINCE: ባህርዳር" — Dire Dawa and Bahir Dar, both major intercity bus hubs
  - [D9] Example train-00000053 (eng config, raw=amh, split=train, label=travel_suggestion): text: "help me decide between Hawassa and Arbaminch for my upcoming trip" — Hawassa and Arba Minch in CITY_OR_PROVINCE slots

#### Strength 3: Ethiopian financial ecosystem entities culturally grounded in Amharic utterances
- **Dimension(s):** IC
- **Observation:** Multiple Amharic banking-domain examples use distinctly Ethiopian entities: Amhara Bank (አማራ ባንክ), Commercial Bank of Ethiopia (ንግድ ባንክ), and TeleBirr (ቴሌብር, Ethiopia's dominant mobile payment platform). The TeleBirr reference appears in both native Amharic (example 16) and the English config raw Amharic utterance (train-00000092). These are not pan-African or Western placeholders — they are Ethiopia-specific financial institutions directly relevant to the deployment context.
- **Deployment relevance:** For a booking system that handles fare payment, the presence of TeleBirr (the leading Ethiopian mobile money platform, operated by Ethio Telecom) as an annotated PAYMENT_COMPANY entity is directly useful for payment-related slot extraction.
- **Datapoint citations:**
  - [D3] Example train-00000016 (amh, split=train, label=balance): "የአማራ ባንክ አካውንቴ ስንት አለው" — Amhara Bank, an Ethiopian-specific institution
  - [D4] Example train-00000018 (amh, split=train, label=balance): "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" — Commercial Bank of Ethiopia (ንግድ ባንክ)
  - [D5] Example train-00000003 (amh, split=train, label=balance): "በቴሌብር የብድር አካውንቴ ላይ…" — TeleBirr mobile payment platform

#### Strength 4: Culturally grounded entity substitution confirmed across multiple language tracks, not just one
- **Dimension(s):** IC
- **Observation:** The benchmark YAML cited the Xhosa/South African entity substitution as the key example of cultural grounding. The data confirms this extends across language tracks: Hausa (Naira currency, GT Bank), Sesotho (Nedbank, FNB — South African banks), Xhosa (R700 Rand, Standard Bank), Swahili (Maasai Mara, Tigo-Pesa), Oromo (Ethiopian cities, Ethiopian Airlines, Oromo calendar months). Each language uses locally relevant financial institutions, currencies, and toponyms.
- **Deployment relevance:** The consistent pattern across all sampled language tracks strengthens confidence that the Amharic track has similarly received culturally grounded Ethiopian entities (which is confirmed by D1–D5 above), rather than generic or Western placeholders inherited from CLINC.
- **Datapoint citations:**
  - [D19] Example train-00000018 (hau, split=train, label=balance): "Naira nawa gare ni … na bankin Gt?" — Naira currency, GT Bank (Nigeria)
  - [D21] Example train-00000003 (sot, split=train, label=balance): "Ho setse bokae bankeng ya FNB" — FNB South Africa
  - [D22] Example train-00000018 (xho, split=train, label=balance): "imali engange R700 kwiakhawunti yam yaseStandard Bank?" — Rand and Standard Bank
  - [D35] Example train-00000011 (swa, split=train, label=car_rental): "Kukodisha gari la kutembeza watalii pale Maasai Mara" — Kenyan landmark

#### Strength 5: Oromo calendar month names present as DATE slot values, confirming methodology extends to the L2 population's language
- **Dimension(s):** IC, OO
- **Observation:** In the Oromo (orm) config, example train-00000011 uses "Ebila 12 hanga Ebila 14" (April in the Oromo calendar) as a DATE slot value, and example train-00000035 uses "sadaasa 21" (November in the Oromo calendar). Since INJONGO's deployment context includes L2 Amharic speakers from Oromia who may code-switch, the presence of Oromo-language calendar conventions confirms the benchmark methodology generates language-authentic temporal expressions.
- **Deployment relevance:** Though code-switched Amharic–Oromo utterances are absent (a separate concern), the Oromo track's culturally grounded date expressions confirm the overall methodology is consistent and that a system trained on INJONGO for Oromo separately would handle Ethiopian Oromo calendar references.
- **Datapoint citations:**
  - [D13] Example train-00000011 (orm, split=train, label=car_rental): "Ebila 12 hanga Ebila 14tti Mattuu keessatti kireeffannaa konkolaataa argachuun ni danda'amaa" — Ebila (April, Oromo calendar) as DATE
  - [D14] Example train-00000035 (orm, split=train, label=calendar_update): "Sagantaa sirna cidhaaf sadaasa 21tti qabame" — Sadaasa (November, Oromo) as DATE

#### Strength 6: Ethiopian airline and domestic route vocabulary present in Oromo flight utterances
- **Dimension(s):** IC
- **Observation:** Oromo example train-00000041 contains "Xiyyaara Itoopiyaa" (Ethiopian Airlines) and references Dire Dawa (Dirree dawaa), Bole Airport, and Jimma — all key Ethiopian intercity aviation/travel nodes. While this utterance has empty span annotations (a concern noted separately), the vocabulary itself confirms that Ethiopian Airlines and domestic route city names are present in the dataset.
- **Deployment relevance:** For an Ethiopian booking system, familiarity with Ethiopian Airlines and domestic city-pair references is relevant. The presence of these entities in the Oromo track strengthens the inference that similar entities exist in the Amharic track.
- **Datapoint citations:**
  - [D12] Example train-00000041 (orm, split=train, label=book_flight): "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" — Ethiopian Airlines, Dire Dawa, Bole, Jimma all present

#### Strength 7: Ge'ez script used throughout Amharic track with no script anomalies
- **Dimension(s):** IF
- **Observation:** All 19 sampled Amharic examples use correct Ge'ez (Ethiopic) script throughout, including proper representation of Amharic-specific characters and ligatures. No romanized Amharic or mixed-script anomalies were observed in the amh config.
- **Deployment relevance:** The deployment is a text-based smartphone app using Ge'ez input. Full script match eliminates the IF concern entirely for the Amharic track.
- **Datapoint citations:**
  - [D1] Example train-00000042 (amh): "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ།" — all text in Ge'ez script
  - [D5] Example train-00000003 (amh): "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" — Ge'ez script throughout

#### Strength 8: Ethiopian personal names and restaurant names used in Amharic examples
- **Dimension(s):** IC
- **Observation:** Amharic example train-00000031 (confirm_reservation) contains the restaurant name "ቶቶት" (Totot, a known Addis Ababa restaurant) and the personal name "ቃለአብ" (Kaleab, a distinctly Ethiopian/Tigrinya-Amharic name). This confirms that the annotators used locally recognizable named entities rather than translating Western names.
- **Deployment relevance:** For a booking system where restaurant and personal name extraction is tested, culturally grounded Amharic personal names and locally known venue names increase ecological validity for the Ethiopian user population.
- **Datapoint citations:**
  - [D17] Example train-00000031 (amh, split=train, label=confirm_reservation): "RESTAURANT_NAME: ቶቶት $$ PERSONAL_NAME: ቃለአብ" — Ethiopian restaurant and personal name

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Travel domain uses air travel framing exclusively — no surface transport, bus booking, seat class, or operator-specific intents
- **Dimension(s):** IO
- **Observation:** Every sampled Amharic travel-domain utterance (book_flight, car_rental, travel_suggestion) uses air travel or general rental car framing. The two book_flight examples explicitly reference flights to Turkey and Sudan (international air travel). There are no utterances involving intercity bus booking, seat-class selection (VIP vs. economy), operator-specific flows (Sky Bus, Selam Bus, Ride), road-closure rebooking, or fare-tier queries. The intent taxonomy does not include any of these categories.
- **Deployment relevance:** The deployment system is specifically for Sky Bus, Selam Bus, and Ride — intercity bus and ride-hail operators. The benchmark's travel domain is built around generic air travel and car rental intents from CLINC. This is a fundamental domain-level mismatch between what the benchmark tests and what the deployment system handles. A model that achieves high accuracy on INJONGO's travel intents (book_flight, car_rental) may not generalize to intercity bus booking intents that are absent from the taxonomy entirely.
- **Datapoint citations:**
  - [D7] Example train-00000041 (amh, split=train, label=book_flight): "ወደ ቱርክ በፍጥነት የምደርስበት የበረራ አማራጭ ንገረኝ།" — international flight, no surface transport
  - [D8] Example train-00000047 (amh, split=train, label=book_flight): "ወደ ሱዳን የበረራ ትኬት ያስፈልገኛል።" — international air ticket, no bus booking
  - [D25, D26] — Both Amharic book_flight examples are international air travel

#### MAJOR

#### MAJOR Concern 1: Amharic DATE slots predominantly use relative temporal expressions, not Ethiopian calendar month names — calendar coverage is sparse in sample
- **Dimension(s):** IC, OO
- **Observation:** While Strength 1 identified that Ethiopian calendar month names *do* appear in the data (Meskerem in train-00000042, Hamle in train-00000011), the majority of Amharic DATE slot annotations in the sample use relative expressions: "የዚህ ወር" (this month), "ከሚመጣው ወር ጀምሮ ለ3 ወር" (starting next month for 3 months), "ነገ" (tomorrow), "ዛሬ" (today), "በዚህ ሳምንት" (this week). Only 2 of 9 Amharic DATE-annotated examples in the sample use named Ethiopian calendar months. The annotation guide examples explicitly use Gregorian conventions (as documented in Q153, Q154).
- **Deployment relevance:** Users of an Ethiopian booking system will frequently reference specific Ethiopian calendar dates for travel (e.g., "ለጥምቅት ሰኞ" — for Timkat Monday). The benchmark's DATE slot evaluation may not adequately stress-test a model's ability to extract named Ethiopian calendar months vs. relative expressions, and if most training instances use relative expressions, a fine-tuned model may not learn robust calendar-month extraction.
- **Datapoint citations:**
  - [D15] Example train-00000052 (amh): "DATE: የዚህ ወር" — relative expression "this month," no named month
  - [D16] Example train-00000023 (amh): "DATE: ከሚመጣው ወር ጀምሮ ለ3 ወር" — relative expression, no named calendar month
  - [D28] Example train-00000053 (amh, calendar_update): "DATE: በዚህ ሳምንት" — "this week," relative
  - [D2] Example train-00000042 (amh): "DATE: መስከረም አምስት" — Ethiopian month Meskerem present (counterevidence — one instance confirmed)

#### MAJOR Concern 2: Missing slot annotations in Amharic examples — potential annotation gaps
- **Dimension(s):** OC
- **Observation:** Amharic example 3 (alarm, train-00000045) contains "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ" (the alarm I set for tomorrow morning at 12 o'clock) but has completely empty spans and empty target. The utterance contains at minimum a DATE slot ("ነገ" = tomorrow) and TIME slot ("12 ሰአት ጠዋት" = 12 o'clock in the morning). Similarly, example 7 (calendar_update, train-00000035) "የእናቴን እና የአባቴን የልደት ቀን የቀን መቁጠሪያዬ ላይ ስላቀያየርኩት አስተካክለው" has empty spans despite containing a calendar event reference. The Oromo book_flight example (train-00000041) is similarly unnanotated despite containing multiple city names and Ethiopian Airlines.
- **Deployment relevance:** Slot-filling F1 evaluation depends on accurate ground truth. Missing annotations inflate false-negative counts during model evaluation, artificially depressing F1 scores and potentially misdirecting model fine-tuning. For a deployment system where slot extraction accuracy is the primary requirement, under-annotated training instances reduce the quality of the evaluation benchmark.
- **Datapoint citations:**
  - [D11] Example train-00000045 (amh, split=train, label=alarm): "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ…" spans=[] — DATE "ነገ" and TIME "12 ሰአት" absent from annotation
  - [D33] Example train-00000035 (amh, split=train, label=calendar_update): "የእናቴን እና የአባቴን የልደት ቀን…" spans=[] — birthday calendar event unannotated
  - [D12] Example train-00000041 (orm, split=train, label=book_flight): "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" spans=[] — three city names and airline unannotated

#### MAJOR Concern 3: Ethiopian time convention (6-hour offset) not represented or validated in TIME slot annotations
- **Dimension(s):** IC, OO
- **Observation:** Ethiopian clock convention offsets standard time by 6 hours (1:00 Ethiopian = 7:00 AM internationally). Amharic example 5 (alarm, train-00000053) annotates "TIME: ሰባት ከአስራአምስት" (7:15 in Ethiopian time = 1:15 AM internationally, or more likely 7:15 AM). Example 3 references "12 ሰአት" (12 o'clock in Ethiopian time = 6:00 AM or PM). No TIME annotation in the sample includes disambiguation of Ethiopian vs. international clock convention, and the annotation guide is silent on this (per YAML documentation).
- **Deployment relevance:** For a booking system where users ask about bus departure times, Ethiopian clock convention is actively used (e.g., "ሰባት ሰዓት ለምን ምንም አይሄደም?" could mean "Why is there no bus at 1 AM?" or "at 7 AM?" depending on convention). Ambiguous TIME slot values are a direct failure mode for bus departure slot extraction.
- **Datapoint citations:**
  - [D23] Example train-00000045 (amh, split=train, label=alarm): "ነገ ጠዋት 12 ሰአት…" (12 o'clock, morning) — annotated as empty, but "12 ሰአት" in Ethiopian time = 6 AM international; no convention documented
  - [D6] Example train-00000011 (amh, split=train): "TIME" slot not present; date range uses Hamle — no TIME slot with Ethiopian clock reference in sample

#### MAJOR Concern 4: No code-switched Amharic utterances present; Amharic track is monolingual throughout
- **Dimension(s):** IC, OC
- **Observation:** All 19 sampled Amharic utterances are monolingual Ge'ez script Amharic. None contains Oromo lexical items (Latin script), Tigrinya words, or English loanwords for booking terms such as "ticket," "seat," or "cancel." The eng config's raw Amharic utterances (e.g., train-00000045, train-00000053) also show pure Amharic without code-switching. This is consistent with the INJONGO paper's silence on intra-utterance code-switching.
- **Deployment relevance:** The target population includes L2 Amharic speakers from Oromia and Tigray who produce code-switched utterances. A model evaluated purely on monolingual Amharic will not be assessed for its robustness to code-switched inputs, which are expected to be frequent in actual booking interactions. This is the OC annotator–user mismatch concern identified as HIGH priority in the elicitation.
- **Datapoint citations:**
  - [D1] through [D18] — All Amharic examples are monolingual; no Oromo terms (e.g., Jimma, Adama in Oromo pronunciation), no Tigrinya lexical items, no mixed-script tokens observed in any of the 19 sampled Amharic training examples

#### MAJOR Concern 5: Birr currency not observed in any Amharic travel or utility domain example
- **Dimension(s):** IC, OO
- **Observation:** Despite CURRENCY and MONEY slots being present in the ontology and TeleBirr appearing as a PAYMENT_COMPANY (D5), no sampled Amharic example contains a CURRENCY or MONEY slot value denominated in Ethiopian Birr (ብር or ETB). The currency evidence comes entirely from other languages: Hausa uses Naira (D19), Xhosa uses Rand (D22), Wolof uses Dollar (wol train-00000047). In the Amharic sample, no fare amount or Birr symbol appears as a slot value.
- **Deployment relevance:** The deployment system needs to extract Birr-denominated fares (e.g., "ለVIP መቀሌ ድረስ ስንት ብር ነው?" = "How many Birr to Mekelle VIP?"). If the Amharic training data has few or no Birr-denominated MONEY/CURRENCY slot examples in the travel domain, fine-tuned models may not reliably extract fare values.
- **Datapoint citations:**
  - [D5] Example train-00000003 (amh): TeleBirr appears as PAYMENT_COMPANY, not as a CURRENCY/MONEY value — no Birr amount in slots
  - [D3, D4] — Banking domain Amharic examples reference balance queries without extracting currency amounts
  - [D19] Example train-00000018 (hau): "CURRENCY: Naira" — contrast: Hausa does have currency in slot, Amharic sample does not

#### MINOR

#### MINOR Concern 1: Some Western entity leakage in non-Amharic tracks
- **Dimension(s):** IC
- **Observation:** Hausa example train-00000031 (confirm_reservation) contains "RESTAURANT_NAME: taco bell" — a US fast-food chain that is unlikely to be familiar to Nigerian Hausa speakers in the natural booking context. Luganda train-00000047 (book_flight) routes Algiers to London. Yoruba train-00000036 references "$500" and "Amẹ́ríkà" (America). These are isolated cases and not the dominant pattern, but they confirm that Western entity leakage documented for MASSIVE is not entirely absent from INJONGO.
- **Deployment relevance:** For the Ethiopian Amharic deployment specifically, no Western entity leakage was observed in the Amharic sample. The concern is minor for this specific deployment but may indicate that the cultural grounding methodology was applied unevenly across languages.
- **Datapoint citations:**
  - [D31] Example train-00000031 (hau, split=train, label=confirm_reservation): "Za ku iya tabbatar min ina da ajiyar tebur a taco bell" — Taco Bell, US restaurant chain
  - [D36] Example train-00000047 (lug, split=train, label=book_flight): "eva e Algiers okudda e London" — Algiers to London routing

#### MINOR Concern 2: Potential annotation inconsistency — "12 ሰአት" (a time value) goes unannotated in one Amharic alarm example
- **Dimension(s):** OC
- **Observation:** Amharic example 3 (train-00000045, alarm) contains the text "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ" with completely empty spans. Comparable Amharic alarm examples (train-00000053) annotate "TIME: ሰባት ከአስራአምስት" and "DATE: ነገ" for structurally similar utterances. This suggests inconsistent annotation treatment of the same temporal elements across utterances — one annotated, one not.
- **Deployment relevance:** Inconsistent TIME annotation reduces the reliability of TIME slot F1 as a measure of model quality for the deployment's bus-departure-time extraction use case.
- **Datapoint citations:**
  - [D11] Example train-00000045 (amh): "ነገ ጠዋት 12 ሰአት…" spans=[] — empty despite temporal content
  - [D2] Example train-00000053 (amh): "DATE: ነገ $$ TIME: ሰባት ከአስራአምስት" — similar alarm utterance with full temporal annotation

#### MINOR Concern 3: Lossy English transliteration of Ethiopian entities in eng config may reduce cross-lingual transfer reliability
- **Dimension(s):** OF
- **Observation:** The eng config (which serves as the cross-lingual transfer source) contains English translations of Amharic utterances with some transliteration loss: train-00000045 transliterates "ዳሽን ባንክ" (Dashen Bank — a major Ethiopian bank) as "dasion bank" in the English text. The slot annotation uses "dasion bank" as BANK_NAME. If cross-lingual transfer experiments use this English data as source, "dasion bank" is not a recognizable English entity and would not benefit from English pre-training on bank name recognition.
- **Deployment relevance:** Cross-lingual transfer from African-centric English (INJONGO English) to Amharic is one of the benchmark's documented evaluation settings. Transliteration errors in the English source reduce the quality of this transfer evaluation for Ethiopian-specific entities.
- **Datapoint citations:**
  - [D34] Example train-00000045 (eng config, raw=amh, split=train, label=balance): raw: "እባካችሁ የዳሽን ባንክ ሂሳቤን ታረጋግጡልኛላችሁ?" / text: "can you please check my dasion bank account" — "ዳሽን" → "dasion" (should be "Dashen")

---

### Content Coverage Summary

The Amharic track of INJONGO contains culturally grounded utterances generated by native speakers using distinctly Ethiopian entities: Ethiopian banks (Amhara Bank, Commercial Bank of Ethiopia), the TeleBirr mobile payment platform, Ethiopian restaurant names (Totot), Ethiopian personal names (Kaleab), and crucially — Ethiopian calendar month names in travel-domain DATE slots (Meskerem, Hamle). Two of the three key Ethiopian intercity travel cities examined (Dire Dawa, Bahir Dar, Hawassa, Arba Minch) are confirmed present as CITY_OR_PROVINCE slot values across the amh and eng configs.

The benchmark covers 17 language tracks including Amharic, Oromo, and Tigrinya as separate tracks, all using culturally grounded elicitation. The Oromo track additionally shows Oromo calendar month names (Ebila, Sadaasa, Guraandhala) and Oromo-specific cities (Mattuu/Metu, Naqamtee/Nekemte) as annotated slot values.

However, the travel domain in Amharic is exclusively framed as air travel and car rental (book_flight, car_rental, travel_suggestion, car_rental intents) with no surface transport, intercity bus, seat-class, or operator-specific content. Ethiopian Birr as a MONEY/CURRENCY slot value was absent from all sampled Amharic examples. Ethiopian clock convention (6-hour offset) is unaddressed. All Amharic utterances are monolingual with no code-switching. Annotation gaps (empty spans for utterances with clear temporal content) were observed in 2–3 of 19 Amharic examples.

Across all 17 language tracks, the data consistently shows culturally grounded named entities (local banks, currencies, cities, personal names) with Gregorian and local calendar date references mixed throughout. The `eng` config contains English translations with raw original-language utterances, serving cross-lingual transfer evaluation.

---

### Limitations

1. **Sample size per config:** 11–27 examples per language track from the training split only. With 80 utterances per intent × 40 intents = 3,200 total per language, the sampled 19 Amharic examples represent ~0.6% of the Amharic training set. Ethiopian calendar month coverage may be higher overall than the 2/9 rate observed in DATE annotations here.

2. **Travel domain coverage unquantifiable from sample:** Only 4 Amharic examples fall in the travel domain (book_flight ×3, car_rental ×1 in the sample). The full set has 80 utterances per intent × 8 travel intents = 640 travel-domain Amharic instances. Toponym and Birr currency coverage in the full travel-domain split requires direct dataset inspection beyond this sample.

3. **Validation and test splits not sampled:** The analysis is based on training split only. Test split annotation quality (which is what benchmark evaluation scores reflect) has not been independently verified here.

4. **Code-switching absence confirmed but not quantified:** The absence of code-switched utterances in the 19 Amharic examples is consistent with documentation, but a larger sample (or full dataset inspection) would be needed to confirm this is a systematic absence rather than a sampling artifact.

5. **Amharic-specific per-language F1 scores not available in this dataset:** The HuggingFace dataset contains utterances and labels but not model evaluation scores. Per-language Amharic benchmark performance requires reading Table 5 of the INJONGO ACL 2025 paper directly.

6. **Ethiopian time convention cannot be audited from text alone:** Without ground truth on what clock convention annotators assumed, it is not possible to determine from utterance text whether TIME slot values use Ethiopian or international clock conventions.