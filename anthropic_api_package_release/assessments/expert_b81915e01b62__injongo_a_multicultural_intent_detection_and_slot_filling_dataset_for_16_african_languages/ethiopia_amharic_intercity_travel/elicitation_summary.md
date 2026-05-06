## Use Case
An Amharic-language conversational booking system for three Ethiopian intercity/ride-hail operators (Sky Bus, Selam Bus, Ride), handling intent detection and slot-filling for routes, fares, and seat changes via smartphone apps. The system will be evaluated against the INJONGO benchmark, a ground-up African-language intent and slot-filling dataset.

## Target Population
Ethiopian inter-regional commuters and travelers using smartphone apps; primarily Amharic speakers but including L2 Amharic speakers from other Ethiopian ethnic groups (Oromo, Tigrinya, etc.) who code-switch. Geography spans multiple Ethiopian regions and intercity corridors. Urban Addis Ababa users are likely over-represented in any annotator pool, but the actual user base includes travelers from Amhara, Oromia, Tigray, and other regions.

## Elicitation Responses

Q1 [IO]: Does the system need to handle intents specific to Ethiopian intercity travel — e.g., route queries between regional cities, holiday-surge bookings (Timkat, Meskel), operator-specific seat classes, or rebooking due to road closures?
A1: The user acknowledges INJONGO covers general domains but considers Ethiopian bus/ride-share booking flows broadly comparable. The expectation is that the system handles all standard travel scenarios without requiring a heavily expanded, operator-specific intent taxonomy.

Q2 [IC]: Will users' slot values reflect Ethiopian-specific conventions — Amharic city names/abbreviations, Ethiopian calendar dates (Meskerem, Tikimt), and fares quoted in Birr with local pricing tiers — and does the system need to extract these correctly?
A2: Yes — users' natural utterances are expected to follow these conventions (local city names, Ethiopian calendar, Birr-denominated fares), and correct slot extraction of these values is a system requirement.

Q3 [OC]: Are there systematic phrasing differences across the commuter population — e.g., code-switching with Oromo or Tigrinya words for routes or city names — that a single native-Amharic annotator profile might not capture?
A3: Yes, code-switching is anticipated, particularly Amharic mixed with other Ethiopian languages, though the extent is uncertain and was not specifically controlled for in INJONGO's curation.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | The user accepts INJONGO's general travel intents as broadly sufficient, but operator-specific flows (rebooking on road closures, seat-class selection) and Ethiopian holiday demand patterns remain unchecked against the benchmark's intent set. |
| IC | HIGH | Users will produce slot values in Ethiopian calendar dates, Amharic city names/abbreviations, and Birr-denominated fares — none of which are likely represented in INJONGO's travel-domain slot instances, creating direct construct-irrelevant variance in slot-filling evaluation. |
| IF | LOWER | Deployment is text-only on smartphones, matching INJONGO's text input modality and Amharic script coverage exactly. |
| OO | MODERATE | INJONGO's 40-intent taxonomy was designed ground-up with African contexts, which is a strength, but the travel subdomain's intent granularity for long-distance bus booking (vs. generic travel) has not been verified against operator booking flows. |
| OC | HIGH | Annotators were native Amharic speakers, but the actual user base includes L2 Amharic speakers who code-switch with Oromo or Tigrinya; this annotator–user mismatch is likely to reduce label validity for code-switched or regionally accented slot expressions. |
| OF | LOWER | The benchmark's label output (intent class + slot tags) matches the deployment's structured output requirements for a task-oriented dialogue system. |

## Flagged Gaps

1. **Ethiopian calendar slot coverage**: INJONGO's slot types (23 total) should be audited to confirm whether date slots accommodate the Ethiopian calendar (Ge'ez months: Meskerem, Tikimt, Hidar, etc.) or assume Gregorian dates only — a direct failure mode for travel-date extraction.

2. **Ethiopian city/toponym coverage in slots**: Slot-filling instances should be checked for the presence of Ethiopian intercity route toponyms (e.g., Hawassa, Mekelle, Gondar, Dire Dawa, Jimma) in the travel domain, versus generic or pan-African city references.

3. **Code-switching (Amharic–Oromo, Amharic–Tigrinya)**: INJONGO does include Oromo and Tigrinya as separate languages but does not appear to cover intra-utterance code-switching. Downstream web search should investigate whether any Ethiopian NLP benchmark addresses Amharic–Oromo or Amharic–Tigrinya code-switched travel utterances.

4. **Annotator demographic profile for INJONGO Amharic subset**: The benchmark's ground-up design is a strength, but the specific annotator profile (regional origin, urban/rural, L1 vs. L2 Amharic) for the Amharic portion is not disclosed in the metadata. Web search should surface the INJONGO paper's annotator section to assess representativeness for non-Addis commuters.

5. **Operator-specific intent gaps**: Sky Bus, Selam Bus, and Ride may have proprietary flows (seat-class upgrades, platform-specific cancellation policies, agent-assisted rebooking) not represented in any generic travel intent set. A gap analysis between INJONGO's travel intent list and the three operators' actual booking APIs is recommended.

6. **Birr fare tiers and pricing utterances**: Ethiopian fare conventions (e.g., VIP vs. economy on long-haul buses) may produce slot values outside INJONGO's training distribution; web search should check whether any Ethiopian e-commerce or transport NLP corpus covers fare-slot extraction in Amharic.