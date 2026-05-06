## Dataset Analysis Report

**Dataset(s):** masakhane/InjongoIntent (config: amh primary; configs eng, ewe, hau, ibo, kin, lin, lug, orm, sna, sot, swa, twi, wol, xho, yor, zul reviewed for cross-language comparison)
**Analysis date:** 2025-07-28
**Examples reviewed:** 232 total across 17 language configs (19 amh train, 13 eng train, and 11–27 examples per remaining 15 configs)
**Columns shown:** intent, text, spans, target, example_id; eng config additionally has `raw`
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | amh | train-00000044 | bill_balance | "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — BILL_TYPE: ለመብራት | "How much do I need to pay for electricity per month?" — electricity utility bill query in Amharic | IO, IC |
| D2 | amh | train-00000016 | balance | "የአማራ ባንክ አካውንቴ ስንት አለው" — BANK_NAME: አማራ ባንክ | "How much is in my Amara Bank account?" — Ethiopian bank (Amara Bank) named as BANK_NAME slot | IC, OO |
| D3 | amh | train-00000018 | balance | "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" — BANK_NAME: ንግድ ባንክ | "Is there money remaining at Commercial Bank?" — CBE (Commercial Bank of Ethiopia) named | IC, OO |
| D4 | amh | train-00000003 | balance | "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" — PAYMENT_COMPANY: ቴሌብር | "What is the remaining balance on my Telebirr loan account?" — Telebirr named as PAYMENT_COMPANY | IC, OO |
| D5 | amh | train-00000042 | book_flight | "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ።" — CITY_OR_PROVINCE: ድሬዳዋ, ባህርዳር | "Book me a flight from Dire Dawa to Bahir Dar for the fifth of Meskerem." — Ethiopian cities and Ethiopian calendar month | IC, OO |
| D6 | amh | train-00000011 | car_rental | "ከሃምሌ 4 እስከ 6 የቤት መኪና ኪራይ ማግኘት እችላለሁ?" — DATE: ከሃምሌ 4 እስከ 6 | "Can I get a home car rental from Hamle 4 to 6?" — Ethiopian calendar month (Hamle) used for DATE slot | IC, IF |
| D7 | amh | train-00000051 | bill_balance | "የቦሎ ማሳደሻ ስንት ነው መክፈል የሚኖርብኝ?" — BILL_TYPE: የቦሎ ማሳደሻ | "How much do I need to pay for Bole road expansion?" — bill query referencing Bole (Addis Ababa neighborhood) | IC, IO |
| D8 | amh | train-00000052 | bill_balance | "የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ።" — DATE: የዚህ ወር | "Show me the list of utility expenses to be paid this month." — direct utility bill balance query | IO |
| D9 | amh | train-00000031 | confirm_reservation | "በቶቶት ለቃለአብ ቦታ ማስያዝ እንዳለብኝ መሞከር እና ማረጋገጥ እፈልጋለሁ" — RESTAURANT_NAME: ቶቶት, PERSONAL_NAME: ቃለአብ | "I want to try and confirm that I should book a spot at Totot for Kaleab." — Ethiopian restaurant and personal name | IC |
| D10 | eng | train-00000045 | balance | raw: "እባካችሁ የዳሽን ባንክ ሂሳቤን ታረጋግጡልኛላችሁ?" text: "can you please check my dasion bank account" — BANK_NAME: dasion bank | Original Amharic cites Dashen Bank; English translation renders "dasion" (spelling error) — shows transliteration degradation in eng config | IC, IF |
| D11 | eng | train-00000092 | spending_history | raw: "ከቴሌ ብር አካዉንቴ ገንዘብ ለማን ለማን እንደላኩ ዝርዝሩን አሳየኝ?" text: "Show me history of my telebirr transfers?" — PAYMENT_COMPANY: telebirr | Telebirr confirmed in Amharic source utterance as code-switched reference; PAYMENT_COMPANY slot correctly labeled | IC, OO |
| D12 | eng | train-00000053 | travel_suggestion | raw: "ለቀጣይ የጉብኝት ጉዞዬ በሃዋሳ እና በአርባ ምንጭ መካከል እንድመርጥ…" text: "help me decide between Hawassa and Arbaminch…" — CITY_OR_PROVINCE: Hawassa, Arbaminch | Ethiopian regional cities (Hawassa, Arba Minch) correctly identified in travel context | IC |
| D13 | orm | train-00000041 | book_flight | "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" — no spans | Oromo: "Book me a flight from Dire Dawa to Bole then to Jimma on Ethiopian Airlines" — Bole airport and Dire Dawa named, spans incorrectly empty | IC, OC |
| D14 | orm | train-00000044 | bill_balance | "Yeroo darbe tajaajila humna ibsaa meeqan kanfale naaf himi mee" — BILL_TYPE: tajaajila humna ibsaa | Oromo: "Tell me how much I paid for electricity service last time" — electricity bill query paralleling Ethiopian utility context | IO |
| D15 | amh | train-00000045 | alarm | "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ በደንብ እንዲሰማኝ ድምጽ ጨምርበት" — spans: [] | "Increase the volume of the alarm I set for 12 o'clock tomorrow morning so I can hear it well." — TIME and DATE slots present in text but no spans annotated | OC |
| D16 | amh | train-00000035 | calendar_update | "የእናቴን እና የአባቴን የልደት ቀን የቀን መቁጠሪያዬ ላይ ስላቀያየርኩት አስተካክለው" — spans: [] | "Fix it because I changed my mother's and father's birthday on my calendar." — CALENDAR_EVENT-like content but no spans annotated | OC |
| D17 | lug | train-00000044 | bill_balance | "Obukuumi n'amasannyalaze nteekeddwa kubisasula ddi?" — BILL_TYPE: Obukuumi, amasannyalaze | Luganda: "When do I need to pay the water and electricity bills?" — two BILL_TYPE slots; "amasannyalaze" = electricity | IO |
| D18 | kin | train-00000044 | bill_balance | "Mu bisanzwe nakwishyura fagitire y'amafaranga angahe ku mazi n'umuriro" — BILL_TYPE: mazi n'umuriro | Kinyarwanda: "How much do I normally pay for water and electricity bills?" — utility billing domain confirmed | IO |
| D19 | amh | train-00000044 (config amh) | bill_balance | "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" | No METER_ID, UTILITY_ACCOUNT_NUMBER, or STS_TOKEN slots present anywhere in Amharic sample | OO |
| D20 | amh | train-00000041 | book_flight | "ወደ ቱርክ በፍጥነት የምደርስበት የበረራ አማራጭ ንገረኝ።" — COUNTRY: ቱርክ | "Tell me a flight option to Turkey quickly." — Travel domain; no utility-specific intents observed in 19 Amharic samples | IO |
| D21 | sot | train-00000044 | bill_balance | "Ke hloka bokae ho lefa karete ya Edgars" — spans: [] | Sesotho: "How much do I need to pay the Edgars card?" — Edgars is South African retail credit card; no slots annotated despite implied BILL_TYPE/SHOPPING_ITEM | OC |
| D22 | hau | train-00000015 | confirm_reservation | "Za ku iya tabbatar min ina da ajiyar tebur a taco bell da ƙarfe 7 na yamma" — RESTAURANT_NAME: taco bell | Hausa: "Can you confirm I have a table reservation at Taco Bell at 7 PM?" — Western fast food chain in culturally-specific dataset | IC |
| D23 | eng | train-00000164 | restaurant_reservation | raw: "miateŋu kpɔ teƒe le nuɖuƒe aɖe le Adidogoméa?" text: "Can you make a reservation in this restaurant in Adidogomé?" — CITY_OR_PROVINCE: Adidogomé | Ewe source utterance; English eng config translates with non-standard place name (Adidogomé, Togo) | IC |
| D24 | amh | (all 19 examples) | various | All 19 Amharic examples use Ethiopic script without any romanized characters or Latin-script code-switching | No code-switched (Amharic + English intrasentential) utterances observed in 19 Amharic train examples | IC |
| D25 | amh | train-00000003 | balance | "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" | Intent is `balance` not a utility-specific intent; Telebirr loan balance query in banking domain | IO |
| D26 | orm | train-00000008 | book_flight | "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" — no spans annotated | Oromo flight booking utterance involving Dire Dawa, Bole (Addis Ababa airport), Jimma, Ethiopian Airlines — slot spans missing | OC |
| D27 | amh | train-00000023 | car_rental | "ከሚመጣው ወር ጀምሮ ለ3 ወር ቶዮታ መኪና መከራየት እፈልጋለሁ።" — DATE: ከሚመጣው ወር ጀምሮ ለ3 ወር | "I want to rent a Toyota car for 3 months starting next month." — Arabic numeral "3" mixed with Ethiopic in DATE span | IF |
| D28 | lin | train-00000044 | bill_balance | "Niongo ya snel ezali 2000 FC Yebisa ngai soki nakosi" — PAYMENT_COMPANY: snel, MONEY: 2000 FC | Lingala: "SNEL bill is 2000 FC, tell me if I've paid" — SNEL is the DRC national electricity utility; utility company annotated as PAYMENT_COMPANY | OO |
| D29 | amh | train-00000036 | balance | "የእኔ የወጭ አካውንት ቀሪ ሂሳብ ስንት እንደሆነ ሊነግሩኝ ይችላሉ።" — ACCOUNT_TYPE: የወጭ አካውንት | "Can you tell me the remaining balance of my expense account?" — formal polite register (ሊነግሩኝ ይችላሉ) | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Amharic utility-adjacent bill balance intents with electricity-specific BILL_TYPE slots
- **Dimension(s):** IO, IC
- **Observation:** The Amharic split contains direct electricity bill balance queries with correctly annotated BILL_TYPE slots. Example D1 ("በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — "How much do I need to pay for electricity per month?") annotates "ለመብራት" (for electricity/light) as BILL_TYPE. Example D8 ("የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ།" — "Show me this month's utility expenses list") annotates "የዚህ ወር" as DATE. These utterances are structurally identical to what an EEU chatbot user would produce for a bill_balance intent.
- **Deployment relevance:** EEU and AAWSA billing chatbots require robust `bill_balance` intent detection with electricity-specific BILL_TYPE slots. The Amharic data directly provides labeled training examples for this pattern.
- **Datapoint citations:**
  - [D1] Example train-00000044 (amh, split=train, label=bill_balance): "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — electricity (ለመብራት) tagged as BILL_TYPE
  - [D8] Example train-00000052 (amh, split=train, label=bill_balance): "የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ።" — utility expense list query with DATE slot correctly annotated

#### Strength 2: Ethiopian-specific financial institutions confirmed as named entity values in Amharic split
- **Dimension(s):** IC, OO
- **Observation:** The Amharic examples include Ethiopian banks as BANK_NAME values: "አማራ ባንክ" (Amara Bank, D2) and "ንግድ ባንክ" (Commercial Bank of Ethiopia, D3). Critically, Telebirr — Ethiopia's dominant mobile money platform used to pay utility bills — appears as a PAYMENT_COMPANY slot in D4 ("በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።"). This resolves one of the flagged gaps from the web search findings, which could not confirm Telebirr's presence in the dataset.
- **Deployment relevance:** The deployment specification requires robust Telebirr slot-filling as a high-priority payment company value. Its confirmed presence in Amharic training data means models fine-tuned on INJONGO will have at least some exposure to this entity.
- **Datapoint citations:**
  - [D4] Example train-00000003 (amh, split=train, label=balance): "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" — PAYMENT_COMPANY: ቴሌብር — Telebirr confirmed as PAYMENT_COMPANY value
  - [D2] Example train-00000016 (amh, split=train, label=balance): "የአማራ ባንክ አካውንቴ ስንት አለው" — BANK_NAME: አማራ ባንክ — Ethiopian bank confirmed as BANK_NAME
  - [D3] Example train-00000018 (amh, split=train, label=balance): "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" — BANK_NAME: ንግድ ባንክ — CBE confirmed as BANK_NAME

#### Strength 3: Ethiopian regional cities and Ethiopian calendar system used in Amharic slot values
- **Dimension(s):** IC
- **Observation:** The Amharic split uses Ethiopian-specific geographic entities and the Ethiopian calendar. D5 names Dire Dawa (ድሬዳዋ) and Bahir Dar (ባህርዳር) as CITY_OR_PROVINCE slot values, while D6 uses the Ethiopian calendar month Hamle (ሃምሌ) and D5 uses Meskerem (መስከረም) as DATE slot values. The eng config corroborates this: D12 identifies Hawassa and Arba Minch as CITY_OR_PROVINCE values in an Amharic-sourced utterance.
- **Deployment relevance:** Ethiopian utility accounts and user queries reference regional capitals (Dire Dawa, Hawassa) that are confirmed deployment cities. The use of the Ethiopian calendar is directly relevant because users will phrase temporal references using Amharic calendar month names, not Gregorian months.
- **Datapoint citations:**
  - [D5] Example train-00000042 (amh, split=train, label=book_flight): "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ።" — CITY_OR_PROVINCE: ድሬዳዋ, ባህርዳር; DATE uses Ethiopian month Meskerem
  - [D6] Example train-00000011 (amh, split=train, label=car_rental): "ከሃምሌ 4 እስከ 6 የቤት መኪና ኪራይ ማግኘት እችላለሁ?" — DATE: ከሃምሌ 4 እስከ 6 — Ethiopian calendar month Hamle
  - [D12] Example train-00000053 (eng, split=train, label=travel_suggestion): raw "ለቀጣይ የጉብኝት ጉዞዬ በሃዋሳ እና በአርባ ምንጭ መካከል…" — Hawassa and Arbaminch confirmed as city entities

#### Strength 4: Telebirr confirmed in eng config from an Amharic source utterance, resolving a flagged gap
- **Dimension(s):** IC, OO
- **Observation:** The eng config (which contains English translations of utterances from all 16 African language annotators as practice utterances) contains an Amharic-sourced utterance (raw: "ከቴሌ ብር አካዉንቴ ገንዘብ ለማን ለማን እንደላኩ ዝርዝሩን አሳየኝ?" / text: "Show me history of my telebirr transfers?") with PAYMENT_COMPANY: telebirr labeled. The raw Amharic also shows intra-word spacing variation ("ቴሌ ብር" vs "ቴሌብር") that reflects real user variation.
- **Deployment relevance:** The web search flagged Telebirr's presence in INJONGO as unresolved (gap_id 8). This example resolves part of the gap: Telebirr appears both in the Amharic config (D4) and in the eng config's Amharic-sourced practice utterances, confirming it is a represented entity value in training data.
- **Datapoint citations:**
  - [D11] Example train-00000092 (eng, split=train, label=spending_history): raw "ከቴሌ ብር አካዉንቴ ገንዘብ ለማን ለማን እንደላኩ ዝርዝሩን አሳየኝ?" text "Show me history of my telebirr transfers?" — PAYMENT_COMPANY: telebirr confirmed in Amharic-sourced utterance

#### Strength 5: Ethiopic script confirmed functional in dataset with correct character rendering
- **Dimension(s):** IF
- **Observation:** All 19 Amharic examples render Ethiopic script correctly, including complex fidel characters, compound characters, and diacritics. Example D29 ("የእኔ የወጭ አካውንት ቀሪ ሂሳብ ስንት እንደሆነ ሊነግሩኝ ይችላሉ།") demonstrates polite register markers. No garbled characters, replacement characters (U+FFFD), or encoding artifacts were observed in the sampled Amharic data.
- **Deployment relevance:** Telegram transmits Ethiopic Unicode reliably, and the deployment specifies full Ethiopic script. Confirmed rendering fidelity means the benchmark data is compatible with Telegram-based deployment inputs at the character level, at least for the sampled examples.
- **Datapoint citations:**
  - [D29] Example train-00000036 (amh, split=train, label=balance): "የእኔ የወጭ አካውንት ቀሪ ሂሳብ ስንት እንደሆነ ሊነግሩኝ ይችላሉ።" — complex Ethiopic characters render without artifacts
  - [D5] Example train-00000042 (amh, split=train, label=book_flight): "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ།" — place names and calendar month rendered correctly in Ethiopic

#### Strength 6: Utility domain appears across multiple languages, including electricity and water bill references
- **Dimension(s):** IO
- **Observation:** The `bill_balance` intent includes utility-specific BILL_TYPE values across languages. Luganda D17 annotates electricity ("amasannyalaze") and water ("Obukuumi") as two separate BILL_TYPE spans. Kinyarwanda D18 labels "mazi n'umuriro" (water and electricity) as a single BILL_TYPE span. Lingala D28 annotates SNEL (DRC national electricity utility) as PAYMENT_COMPANY. These cross-language examples confirm the utility domain is operationally populated with electricity and water billing intents.
- **Deployment relevance:** The presence of electricity and water utility queries across multiple language splits confirms that the `bill_balance` intent is not an empty or generic category — it contains real utility billing content that transfers to the Ethiopian deployment context.
- **Datapoint citations:**
  - [D17] Example train-00000044 (lug, split=train, label=bill_balance): "Obukuumi n'amasannyalaze nteekeddwa kubisasula ddi?" — BILL_TYPE: Obukuumi (water), amasannyalaze (electricity)
  - [D18] Example train-00000044 (kin, split=train, label=bill_balance): "Mu bisanzwe nakwishyura fagitire y'amafaranga angahe ku mazi n'umuriro" — BILL_TYPE: mazi n'umuriro (water and electricity)
  - [D28] Example train-00000044 (lin, split=train, label=bill_balance): "Niongo ya snel ezali 2000 FC Yebisa ngai soki nakosi" — PAYMENT_COMPANY: snel; MONEY: 2000 FC

#### Strength 7: Formal polite register in Amharic consistent with urban utility customer service interactions
- **Dimension(s):** IC
- **Observation:** Several Amharic utterances use formal polite Amharic grammatical register. D29 uses "ሊነግሩኝ ይችላሉ" (polite second-person plural form, equivalent to formal "you can tell me"), which is consistent with how urban Ethiopian users address formal service systems. D3 uses "አለ" as a balance query without explicit pronoun, matching natural Amharic speech patterns.
- **Deployment relevance:** The deployment context specifies that Addis Ababa users interact with formal service institutions using deferential but direct register. The presence of formal polite forms in training data means models will see appropriate formal register examples during fine-tuning.
- **Datapoint citations:**
  - [D29] Example train-00000036 (amh, split=train, label=balance): "የእኔ የወጭ አካውንት ቀሪ ሂሳብ ስንት እንደሆነ ሊነግሩኝ ይችላሉ።" — formal polite register (ሊነግሩኝ ይችላሉ)
  - [D3] Example train-00000018 (amh, split=train, label=balance): "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" — natural Amharic query without over-formalized structure

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: No METER_ID, UTILITY_ACCOUNT_NUMBER, KEBELE, or STS_TOKEN slot types exist in the 23-slot ontology — confirmed by data inspection
- **Dimension(s):** OO
- **Observation:** Inspection of all 19 Amharic examples confirms that the slot taxonomy, as implemented, has no slot types for meter identifiers, utility account numbers, STS tokens, or Ethiopian administrative sub-units (kebele, woreda, sub-city). The 23 slot types available (ACCOUNT_TYPE, BANK_NAME, BILL_TYPE, CITY_OR_PROVINCE, CURRENCY, DATE, MONEY, NUMBER, PAYMENT_COMPANY, PLACE_NAME, TIME, etc.) cannot capture these critical deployment-required entities. D19 makes this concrete: the bill_balance utterance D1 ("በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?") has no slots for meter or account reference, and no examples in the 19-sample Amharic set contain meter IDs, account numbers, or kebele references.
- **Deployment relevance:** The core functionality of an EEU prepaid meter top-up chatbot requires extracting METER_ID and STS_TOKEN from user input. The core functionality of an AAWSA chatbot requires extracting UTILITY_ACCOUNT_NUMBER and kebele-level address. None of these can be evaluated or trained using INJONGO's existing slot ontology. This is a fundamental structural gap that requires augmentation of the slot taxonomy before INJONGO can support the full deployment task.
- **Datapoint citations:**
  - [D19] Observation across all 19 amh train examples: no METER_ID, UTILITY_ACCOUNT_NUMBER, KEBELE, or STS_TOKEN spans appear in any of the 19 Amharic examples reviewed — confirmed absence of deployment-critical slot types
  - [D1] Example train-00000044 (amh, split=train, label=bill_balance): "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — utility bill query with only DATE and BILL_TYPE slots; no mechanism to annotate meter or account reference

#### CRITICAL Concern 2: Zero code-switched (Amharic-English) utterances observed in the 19 Amharic training examples
- **Dimension(s):** IC
- **Observation:** All 19 sampled Amharic examples are monolingual Ethiopic script. Not a single example contains English words, English morphology grafted onto Amharic roots, or mixed-script tokens. This is consistent with the YAML documentation's confirmed gap (gap_id 2: "code-switching was not an explicit design criterion"). By contrast, the deployment specification states that "code-switching with English is common and increasing, especially among younger generations" and that "technical/domain vocabulary (e.g., 'meter', 'top-up', 'token', 'balance') frequently borrowed or switched to English." D24 documents this absence explicitly.
- **Deployment relevance:** If the benchmark's Amharic split lacks code-switched utterances and the deployment population produces them with high frequency (especially for utility-specific English-origin technical vocabulary like "token", "top-up", "balance"), then benchmark evaluation scores will overestimate actual deployment performance. A model that achieves 93% accuracy on monolingual INJONGO Amharic may perform substantially worse on naturalistic Amharic-English mixed input.
- **Datapoint citations:**
  - [D24] All 19 amh train examples reviewed: "ነገ ጠዋት 12 ሰአት…", "ንግድ ባንክ ላይ…", "በቴሌብር…" — zero Latin-script tokens, zero English insertions in any of 19 Amharic examples
  - [D4] Example train-00000003 (amh, split=train, label=balance): "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" — Telebirr written in full Ethiopic (ቴሌብር), not as Latin-script "Telebirr" as deployed users would commonly type

#### CRITICAL Concern 3: No deployment-specific utility intents observed — prepaid meter top-up, outage reporting, STS token query, and load-shedding schedule absent from sampled Amharic data
- **Dimension(s):** IO
- **Observation:** The 19 Amharic samples span intents: bill_balance (3), alarm (3), balance (4), book_flight (3), cancel_reservation (2), calendar_update (2), car_rental (2), confirm_reservation (1). No `meter_top_up`, `outage_report`, `token_query`, `power_schedule_query`, `account_registration`, or analogous utility-specific intents appear. The `bill_balance` intent is present and utility-relevant (D1, D8), but the prepaid meter top-up workflow — the primary use case for EEU chatbot interactions — is not represented. D20 confirms that travel and general banking intents dominate over utility-specific ones in the sample.
- **Deployment relevance:** The deployment elicitation identified prepaid meter top-up, outage reporting, and load-shedding schedule queries as the three core use cases. The absence of these as distinct intent categories means INJONGO cannot directly train or evaluate the system's primary tasks. The paper itself acknowledges that the 5-domain/40-intent taxonomy "misses some other domains essential for real-world applications."
- **Datapoint citations:**
  - [D20] Example train-00000041 (amh, split=train, label=book_flight): "ወደ ቱርክ በፍጥነት የምደርስበት የበረራ አማራጭ ንገረኝ።" — travel intent in Amharic split, illustrating domain distribution
  - [D8] Example train-00000052 (amh, split=train, label=bill_balance): "የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ།" — closest to deployment use case but scoped to bill balance inquiry, not top-up or outage

---

#### MAJOR

#### MAJOR Concern 4: Annotation quality issues — missing spans on utterances with clearly extractable entities
- **Dimension(s):** OC
- **Observation:** Multiple examples across languages have empty span targets despite containing entity-rich text. D15 (amh, alarm): "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ በደንብ እንዲሰማኝ ድምጽ ጨምርበት" clearly contains DATE (ነገ = tomorrow) and TIME (12 ሰአት = 12 o'clock) but spans are empty. D16 (amh, calendar_update): "የእናቴን እና የአባቴን የልደት ቀን" contains CALENDAR_EVENT and PERSONAL_NAME candidates but no spans annotated. D13 (orm, book_flight): "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" contains CITY_OR_PROVINCE values (Dirree dawaa = Dire Dawa, Boolee = Bole, jimmaa = Jimma) and an implied carrier name but has no spans. D21 (sot, bill_balance): "Ke hloka bokae ho lefa karete ya Edgars" contains an implied BILL_TYPE/SHOPPING_ITEM (Edgars card) but is annotated empty.
- **Deployment relevance:** Missing spans on entity-rich utterances directly reduce the quality signal for slot-filling F1 evaluation and fine-tuning. If the Amharic split contains similar under-annotated examples at scale (the sample rate is ~1%), slot-filling models trained on INJONGO may learn to under-predict spans, harming deployment performance on the extraction tasks most critical to the EEU/AAWSA workflow.
- **Datapoint citations:**
  - [D15] Example train-00000045 (amh, split=train, label=alarm): "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ በደንብ እንዲሰማኝ ድምጽ ጨምርበት" — spans empty despite clear DATE (ነገ) and TIME (12 ሰአት) candidates
  - [D16] Example train-00000035 (amh, split=train, label=calendar_update): "የእናቴን እና የአባቴን የልደት ቀን የቀን መቁጠሪያዬ ላይ ስላቀያየርኩት አስተካክለው" — spans empty despite CALENDAR_EVENT content
  - [D13] Example train-00000041 (orm, split=train, label=book_flight): "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" — spans empty despite 3 city names identifiable

#### MAJOR Concern 5: Ground-truth label authority mismatch — Amharic annotations by pan-African crowdworkers, not Ethiopian utility domain experts
- **Dimension(s):** OC
- **Observation:** The deployment specification states that "correct extraction should be validated by the respective utility's customer service agents (Ethiopian Electric Utility or Addis Ababa Water billing staff)." No evidence in the sampled data or documentation confirms that Amharic annotators had domain familiarity with Ethiopian utility billing. The web search confirmed this gap explicitly (gap_id 3: "NOT FOUND"). The annotator pool was managed through a Kenya-based logistics company at per-country rates. The Amharic examples sampled (D1, D7, D8) contain utility-relevant content, but their BILL_TYPE slot boundaries and values reflect general native-speaker intuition, not EEU/AAWSA billing terminology conventions.
- **Deployment relevance:** For a deployment where ground truth is defined by utility agents (e.g., whether "ለመብራት" correctly maps to the BILL_TYPE that EEU's billing system recognizes, or whether informal Addis Ababa neighborhood references in PLACE_NAME slots match official utility account address fields), the benchmark's crowdworker annotations may systematically diverge from the authoritative ground truth. This could manifest as false positive slot extractions in production.
- **Datapoint citations:**
  - [D7] Example train-00000051 (amh, split=train, label=bill_balance): "የቦሎ ማሳደሻ ስንት ነው መክፈል የሚኖርብኝ?" — BILL_TYPE: የቦሎ ማሳደሻ — "Bole upgrade/road expansion" billed to resident; whether this maps to an EEU/AAWSA billing category cannot be confirmed without domain expert review
  - [D1] Example train-00000044 (amh, split=train, label=bill_balance): "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — BILL_TYPE: ለመብራት — electricity payment query annotated by general native speaker, not EEU billing staff

#### MAJOR Concern 6: `bill_balance` intent conflates utility bill queries with unrelated payment queries across the dataset
- **Dimension(s):** IO, OO
- **Observation:** The `bill_balance` intent is used heterogeneously across language configs. In Amharic (D1, D8), it maps to electricity utility bill queries. In Hausa D28-equivalent (hau config), it covers GOTV (cable TV) subscription: "Zaka iya sanar da ni nawa ne kuɗin gotv ɗin wata biyu?" In Twi, it covers telecel fiber bills. In Zulu, it covers electricity ("sagesi") and phone bills. In Sesotho (D21), it covers a retail credit card (Edgars). This heterogeneity means `bill_balance` as an intent label covers a wide range of billing contexts that may not all be relevant or may require disambiguation in an EEU/AAWSA deployment.
- **Deployment relevance:** An EEU chatbot trained on INJONGO's `bill_balance` intent would learn from examples spanning cable TV, retail credit, mobile phone bills, and utility bills. In a deployment scoped exclusively to electricity and water utilities, this may introduce noise in intent classification precision, or require post-processing to distinguish utility billing from general billing.
- **Datapoint citations:**
  - [D1] Example train-00000044 (amh, split=train, label=bill_balance): "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — electricity utility bill
  - [D22] Example train-00000052 (hau, split=train, label=bill_balance): "Zaka iya sanar da ni nawa ne kuɗin gotv ɗin wata biyu?" — GOTV cable TV bill — same intent label, different domain

#### MAJOR Concern 7: Transliteration degradation in eng config reduces reliability of cross-lingual transfer evaluation for Amharic
- **Dimension(s):** IF, OC
- **Observation:** The eng config contains English translations of utterances from all 16 African languages' annotators as practice utterances. D10 shows an Amharic-sourced utterance where "ዳሽን ባንክ" (Dashen Bank, a major Ethiopian bank) is translated as "dasion bank" — a misspelling that would introduce noise in English-side training data. The BANK_NAME slot value in English ("dasion bank") does not match the correct romanization ("Dashen Bank") and would not be recognized by an English-language model as a known Ethiopian bank.
- **Deployment relevance:** Cross-lingual transfer from the INJONGO English split to Amharic is a documented evaluation setup. If the English-side training data contains transliteration errors for Ethiopian entities, zero-shot transfer experiments may underestimate Amharic-centric model performance or produce incorrect entity extractions in translate-test settings.
- **Datapoint citations:**
  - [D10] Example train-00000045 (eng, split=train, label=balance): raw "እባካችሁ የዳሽን ባንክ ሂሳቤን ታረጋግጡልኛላችሁ?" text "can you please check my dasion bank account" — BANK_NAME: dasion bank — "ዳሽን" (Dashen) mistransliterated as "dasion"

#### MAJOR Concern 8: Amharic-specific Fleiss' Kappa scores not surfaced; Amharic pre-review annotation quality unknown
- **Dimension(s):** OC
- **Observation:** The YAML documentation and web search both flag that Amharic-specific Kappa scores from Table 3 were not accessible (gap_id 7: "NOT FOUND"). The paper reports a range of 0.618–0.934 pre-review across all languages. The two largest pre-to-post improvements were Sesotho (+0.327) and Zulu (+0.294). It is unknown where Amharic falls within this range. The sampled data shows concerning annotation gaps (D15, D16) with empty spans on entity-rich utterances, suggesting potential annotation inconsistency.
- **Deployment relevance:** For a deployment relying on INJONGO Amharic slot-filling labels as ground truth for model training and evaluation, unknown pre-review annotation quality represents unquantified uncertainty. If Amharic had a pre-review Kappa closer to 0.618 (like Zulu) rather than 0.934, the reviewed annotations may have involved substantial disagreement resolution that could systematically diverge from the utility-domain interpretation needed for EEU/AAWSA deployment.
- **Datapoint citations:**
  - [D15] Example train-00000045 (amh, split=train, label=alarm): "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ" — empty spans despite identifiable DATE and TIME — consistent with annotation inconsistency
  - [D16] Example train-00000035 (amh, split=train, label=calendar_update): "የእናቴን እና የአባቴን የልደት ቀን" — empty spans despite CALENDAR_EVENT content

---

#### MINOR

#### MINOR Concern 9: Arabic numeral mixing in Amharic DATE spans alongside Ethiopic text — not explicitly addressed
- **Dimension(s):** IF
- **Observation:** D27 (amh, car_rental): "ከሚመጣው ወር ጀምሮ ለ3 ወር ቶዮታ መኪና መከራየት እፈልጋለሁ།" uses Arabic numeral "3" embedded within an otherwise Ethiopic-script Amharic utterance. The DATE span annotation covers "ከሚመጣው ወር ጀምሮ ለ3 ወር" including the numeral. This confirms that mixed-numeral usage appears in the dataset, but it is an incidental occurrence rather than a systematically designed feature.
- **Deployment relevance:** Ethiopian utility users may mix Ethiopic numerals (፩፪፫), Western Arabic numerals (1 2 3), and numeral words in Amharic, particularly in meter IDs, account numbers, and payment amounts. The benchmark's casual handling of numeral mixing (no dedicated slot type, incidental inclusion) means tokenizer and extraction behavior on numeral-heavy utility inputs cannot be assessed from the benchmark alone.
- **Datapoint citations:**
  - [D27] Example train-00000023 (amh, split=train, label=car_rental): "ከሚመጣው ወር ጀምሮ ለ3 ወር ቶዮታ መኪና መከራየት እፈልጋለሁ།" — DATE span includes Arabic numeral "3" embedded in Ethiopic text

#### MINOR Concern 10: Some Western cultural entities remain in the dataset despite the cultural grounding mandate
- **Dimension(s):** IC
- **Observation:** D22 (hau, confirm_reservation): "Za ku iya tabbatar min ina da ajiyar tebur a taco bell da ƙarfe 7 na yamma" annotates "taco bell" as RESTAURANT_NAME — a Western fast-food chain with no presence in Nigeria or most of Sub-Saharan Africa. This is a residual Western entity despite the dataset's stated cultural grounding mandate.
- **Deployment relevance:** For the Amharic Ethiopian deployment specifically, this observation is lower severity since the RESTAURANT_NAME slot type is not relevant to EEU/AAWSA chatbot interactions. However, it confirms that the cultural grounding mandate was not fully enforced across all language splits, which marginally reduces confidence in the broader cultural validity claim.
- **Datapoint citations:**
  - [D22] Example train-00000031 (hau, split=train, label=confirm_reservation): "Za ku iya tabbatar min ina da ajiyar tebur a taco bell da ƙarfe 7 na yamma" — RESTAURANT_NAME: taco bell — Western chain in Hausa-language African context

#### MINOR Concern 11: Utility entity annotated as PAYMENT_COMPANY rather than a utility-specific slot type in Lingala
- **Dimension(s):** OO
- **Observation:** D28 (lin, bill_balance): "Niongo ya snel ezali 2000 FC Yebisa ngai soki nakosi" annotates SNEL (Société Nationale d'Électricité, DRC's national electricity utility) as PAYMENT_COMPANY. While this is a reasonable annotation under the existing 23-slot ontology, it conflates a utility service provider with a payment company, potentially causing confusion when similar Ethiopian entities (EEU, AAWSA) appear in utterances.
- **Deployment relevance:** In an Ethiopian deployment, EEU and AAWSA are utility providers, not payment companies. If the model learns from cross-lingual examples where utility companies are labeled PAYMENT_COMPANY, it may incorrectly classify Ethiopian utility references. This is a minor ontological ambiguity that could affect cross-lingual transfer quality.
- **Datapoint citations:**
  - [D28] Example train-00000044 (lin, split=train, label=bill_balance): "Niongo ya snel ezali 2000 FC Yebisa ngai soki nakosi" — PAYMENT_COMPANY: snel — national electricity utility labeled as payment company

---

### Content Coverage Summary

The 19 Amharic training examples reviewed span 8 intent categories: bill_balance, alarm, balance, book_flight, cancel_reservation, calendar_update, car_rental, and confirm_reservation. All utterances are monolingual Ethiopic script with natural Amharic register. Ethiopian-specific entities are well-represented: Telebirr (ቴሌብር) appears as PAYMENT_COMPANY, Ethiopian banks (Amara Bank, Commercial Bank of Ethiopia) appear as BANK_NAME, Ethiopian regional cities (Dire Dawa, Bahir Dar) appear as CITY_OR_PROVINCE, and Ethiopian calendar months (Hamle, Meskerem) appear as DATE values. The utility domain is touched by bill_balance intents referencing electricity (ለመብራት) and general utility expenses, but there is no representation of the deployment's primary intents: prepaid meter top-up, outage reporting, STS token entry, or load-shedding schedule queries. The 23-slot ontology, while useful for general banking, travel, and household intents, lacks all deployment-critical slot types (METER_ID, UTILITY_ACCOUNT_NUMBER, KEBELE, STS_TOKEN). No code-switched Amharic-English utterances were observed in the 19 Amharic samples, despite this being a confirmed high-priority deployment requirement. Across the 16 non-Amharic language configs, the dataset shows strong cultural grounding with local payment companies (Flooz in Ewe, Orange Money and SNEL in Lingala, MoMo in Kinyarwanda, Tigo-Pesa in Swahili), local banks, and locally appropriate geographic entities, reinforcing that the cultural grounding principle was applied. Annotation quality shows some gaps, with empty span annotations on utterances containing identifiable entities (most notably in Amharic, Oromo, and Sesotho examples), suggesting some under-annotation that may reduce slot-filling training signal.

---

### Limitations

1. **Sample size per language:** Only 19 Amharic training examples were reviewed out of 2,240 total (0.85%). Patterns observed (absence of code-switching, absence of meter/account intents) are consistent with design documentation but cannot be claimed as exhaustive — rare phenomena in the full corpus may not appear in the sample.

2. **Test and validation splits not inspected:** Only training split examples were sampled. Evaluation results on INJONGO are reported on test splits; annotation quality in the test split cannot be assessed from the training sample.

3. **Utility-domain intent distribution unknown:** The 19 Amharic examples include only 3 bill_balance instances. The full distribution across all 40 intents (80 per intent = 8 utility-domain intents × 80 = ~640 utility examples in Amharic) cannot be assessed from the sample. The actual utility domain content (including any outage or top-up adjacent intents) may differ from what the sample shows.

4. **Telebirr coverage depth unquantifiable:** While Telebirr was confirmed as present in both the Amharic config (D4) and the eng config (D11), the frequency of its appearance as a PAYMENT_COMPANY value across the full 2,240 Amharic training examples cannot be determined from two instances. It may appear only rarely.

5. **Annotation spans use byte offsets, not character offsets:** The `spans` field uses `start_byte` and `limit_byte`. For Ethiopic script, multi-byte UTF-8 characters mean character and byte positions diverge. This was not independently verified against the raw text in the sample, but annotation correctness was inferred from the `target` field string values.

6. **Non-Amharic configs reviewed only partially:** The 15 non-Amharic configs were reviewed primarily to contextualize the Amharic data and cross-linguistic ontology observations. Language-specific validity claims for other languages are outside the deployment scope and not fully assessed here.

7. **Unicode normalization form (NFC vs. NFD) not determinable from rendered output:** Character rendering appeared correct, but whether the underlying bytes use NFC or NFD normalization cannot be verified through text inspection alone and requires direct encoding analysis of the raw parquet files.