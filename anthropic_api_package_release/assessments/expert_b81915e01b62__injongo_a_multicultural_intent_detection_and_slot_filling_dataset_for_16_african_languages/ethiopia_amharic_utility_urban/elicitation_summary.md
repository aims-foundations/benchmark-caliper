## Use Case
Amharic-language chatbots deployed via Telegram and SMS for Ethiopian Electric Utility and Addis Ababa Water, handling prepaid meter top-ups, outage reports, and bill disputes for urban Ethiopian households. The system must perform intent detection and slot-filling (meter IDs, account numbers, payment amounts, addresses) in naturalistic Amharic, including code-switched input with English.

## Target Population
Urban households in Addis Ababa and regional capitals (e.g., Dire Dawa, Hawassa, Mekelle), primarily Amharic-speaking but with significant code-switching with English, particularly among younger users. Users interact over Telegram (primary, full Ethiopic script) and SMS (secondary). Authoritative ground truth for slot-filling is defined by utility customer service agents and billing staff at Ethiopian Electric Utility and Addis Ababa Water.

## Elicitation Responses

Q1 [IO]: The benchmark covers a general 'utility' domain across many African contexts. Does this deployment require intents beyond what a pan-African utility dataset might include — e.g., Ethiopia-specific prepaid meter codes, tiered pricing disputes, power-shedding schedules, or informal neighborhood reporting?
A1: Major differences are not expected, but there are likely gaps around Ethiopian-specific payment methods and some scenario-specific intents unique to the Ethiopian utility context.

Q2 [IC]: Users interact via Telegram and SMS in Amharic that may include informal abbreviations, Ethiopic/Arabic numeral mixing, code-switching with English or Oromo, and SMS shorthand. Does the deployment data look like this?
A2: Yes — code-switching with English is common and increasing, especially among younger generations across Ethiopia. The system is expected to handle Amharic-English code-switching robustly.

Q3 [OC]: For slot-filling correctness (meter numbers, account IDs, addresses, payment amounts), whose judgment determines the ground truth — utility agents, billing staff, or community-level conventions?
A3: Correct extraction should be validated by the respective utility's customer service agents (Ethiopian Electric Utility or Addis Ababa Water billing staff), not community-level conventions.

Q4 [IF]: SMS may corrupt or strip Ethiopic (Ge'ez) script; do users romanize Amharic on SMS, and must the system handle both romanized and full Ethiopic representations?
A4: Telegram is dominant in Ethiopia and users predominantly use full Ethiopic script. The recommendation is to handle full Ethiopic script only and not invest in romanized Amharic support.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark's pan-African utility domain likely underrepresents Ethiopia-specific intents (payment methods, local top-up workflows), and the user confirmed some scenario-specific gaps exist even if major structural differences are few. |
| IC | HIGH | Code-switching between Amharic and English is confirmed as a frequent and growing pattern in the target population, which a dataset authored by native speakers across 16 African languages may not capture at sufficient density for Ethiopian urban Telegram users. |
| IF | MODERATE | Deployment is text-only in full Ethiopic script on Telegram, matching the benchmark's text modality; however, Ge'ez script is lower-resource and the confirmed exclusion of romanized input narrows the signal distribution the system must handle, warranting a check on whether benchmark instances reflect natural Telegram-style Ethiopic encoding. |
| OO | MODERATE | The benchmark was ground-up designed by African native speakers with a utility domain included, reducing gross category mismatch; however, the 40-intent taxonomy may not align with the specific intent hierarchy used by Ethiopian Electric Utility and Addis Ababa Water's customer service workflows. |
| OC | HIGH | Ground-truth slot-filling labels should be validated by Ethiopian utility agents, but the benchmark's annotator pool is pan-African and not specific to Ethiopian utility billing conventions; informal address references (kebele names, neighborhood designations) may diverge from the official slot values in the dataset. |
| OF | LOWER | Both the benchmark and deployment use label-based output (intent classification + slot extraction) in text; no modality mismatch exists and the deployment does not require speech or open-ended generation. |

## Flagged Gaps

1. **Ethiopian-specific payment method intents**: The benchmark's utility domain was designed pan-African; downstream search should investigate whether INJONGO's intent taxonomy includes prepaid/STS token top-up workflows, mobile-money platforms common in Ethiopia (e.g., Telebirr, CBE Birr), or whether these are absent and require augmentation.

2. **Amharic-English code-switching coverage**: The benchmark contains 3,200 Amharic instances, but it is unclear whether these include intra-sentential code-switching with English. Downstream search should determine the proportion of code-switched utterances in INJONGO's Amharic split and whether code-switching was an explicit design criterion for the Amharic subset.

3. **Regional capital dialect and Oromo interference**: Users in Dire Dawa, Hawassa, and Mekelle may produce Amharic with Oromo or Tigrinya substrate influence. INJONGO covers Oromo and Tigrinya separately; it is unknown whether the Amharic split reflects this regional variation or defaults to Addis Ababa prestige Amharic.

4. **Informal address and kebele slot values**: Ethiopian utility accounts reference kebele numbers and informal neighborhood names that may not align with any standardized slot ontology in a pan-African dataset. Downstream search should check whether INJONGO's address-type slots cover Ethiopian administrative sub-unit naming conventions.

5. **Ethiopic script encoding fidelity on Telegram**: Telegram transmits Ethiopic Unicode reliably, but the benchmark's text instances may have been collected via different interfaces. Downstream search should confirm whether INJONGO's Amharic data uses normalized Unicode Ge'ez or has encoding inconsistencies that could affect tokenizer compatibility with deployment inputs.

6. **Annotator representativeness for utility slot-filling**: The benchmark's annotation was done by native speakers, but it is unclear whether the Amharic annotators had domain familiarity with Ethiopian utility billing terminology. Downstream search should investigate whether utility-domain utterances in the Amharic split were validated by agents or billing staff, or only by general native-speaker crowdworkers.