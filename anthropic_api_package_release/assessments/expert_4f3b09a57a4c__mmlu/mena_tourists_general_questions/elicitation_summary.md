## Use Case
An AI assistant helps non-Arab tourists and expats visiting eight Arab countries (Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, KSA) answer general questions about Arabic language, history, and geography. The system covers school-level educational knowledge rather than practical on-the-ground guidance. It is evaluated using MMLU, a US-centric English-language benchmark covering 57 academic subjects.

## Target Population
Geography: Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, Saudi Arabia — spanning North Africa, the Levant, and the Gulf. Sub-national cohort: Not specified; coverage spans eight nationally distinct Arab contexts. Language(s): Primarily English-language users, with a secondary cohort of Arabic-learning foreigners who may prompt in Arabic. Occupation/role: Non-Arab tourists and expats with general curiosity about the region's language, history, and geography. Relevant demographics: Multilingual users, potentially from a very wide range of source countries; limited Arabic literacy expected for most users.

## Elicitation Responses

Q1 [IO]: Your users are tourists and expats visiting specific countries — Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, and KSA. Should the system handle practical, on-the-ground knowledge that foreigners typically need, such as local dialect phrases, common tourist etiquette, local religious customs, or navigating local transport and markets? Are there categories of questions you expect frequently that go beyond formal history and geography?
A1: Dialectal phrase support would be useful but is out of scope for MMLU; the system focuses on school-level general knowledge (history, geography, language basics). Practical etiquette, religious customs, and transport guidance are frequently expected by users but are outside the intended system scope.

Q2 [IC]: Does the system need to reflect country-specific cultural nuances accurately, or is a pan-Arab generalized framing acceptable?
A2: Pan-Arab generalization is generally acceptable given shared religion and language, but the system should flag and distinguish content that is specific to particular countries rather than silently treating it as universal.

Q3 [OO]: When the system answers history or geography questions where countries hold different official or cultural positions, should it present a single answer, acknowledge multiple perspectives, or tailor its answer to the country visited?
A3: The system should acknowledge multiple perspectives and explicitly note when a topic is contested or politically sensitive across different countries, rather than presenting a single authoritative answer.

Q4 [IF]: Will users interact in English, Arabic, or both? What input-language coverage is needed from the benchmark?
A4: The primary interaction language is English, but Arabic-learning foreigners may prompt in Arabic, making Arabic-language evaluation relevant. Other languages may be supported but would require separate benchmarking of cross-lingual capabilities beyond MMLU's scope.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MMLU's 57 subjects are anchored in US academic curricula and contain minimal coverage of Arab history, regional geography, or Arabic language — the core domains this system serves. |
| IC | HIGH | MMLU's content is US-sourced and culturally transferred with no porting; specific Arab-country historical narratives, contested events (e.g., 1948 war), and country-level distinctions are almost certainly absent or framed from a non-Arab perspective. |
| IF | MODERATE | The deployment is text-only matching MMLU's modality, but a meaningful user sub-cohort will query in Arabic while MMLU is English-only, creating a language-signal mismatch for that cohort. |
| OO | HIGH | MMLU uses single-answer MCQ scoring, but the deployment requires acknowledging multiple valid perspectives on contested historical and political topics; the benchmark's binary correct/incorrect scoring is structurally misaligned with the system's intended output behavior. |
| OC | HIGH | MMLU ground-truth labels were annotated by a US-centric academic population; for Arab history and geography questions, label correctness as judged by regional stakeholders (especially on contested narratives like Palestinian history) may diverge substantially. |
| OF | MODERATE | Both MMLU and the deployment use text-based interaction, but MMLU's MCQ label output does not match the open-ended explanatory responses the deployed system produces, limiting direct transfer of scoring. |

## Flagged Gaps

1. **Arab-region subject coverage in MMLU**: MMLU has no dedicated subject categories for Arab history, Middle Eastern geography, or Arabic language. Downstream search should investigate whether any of the 57 MMLU subjects (e.g., world history, global facts) contain sufficient Arab-region content to be meaningful, or whether coverage is negligible.

2. **Arabic-language input capability**: MMLU is English-only. The deployment anticipates Arabic-learning users prompting in Arabic. Search should identify whether any Arabic-language MMLU variants (e.g., ArabicMMLU, ACVA, or similar) exist and how they compare in regional cultural grounding.

3. **Palestinian and Levantine historical narratives**: Palestinian history involves highly contested framing across Jordan, Lebanon, Israel, and international bodies. MMLU's US academic framing is unlikely to reflect Palestinian or pan-Arab perspectives. This gap needs targeted evidence.

4. **Country-level distinctions within the Arab world**: The deployment spans eight countries with distinct colonial histories, legal systems, and cultural identities (e.g., Moroccan Amazigh heritage, Gulf monarchical civic identity, Egyptian Coptic minority context). MMLU's pan-Western generalization cannot differentiate these; search should assess whether any supplementary benchmarks cover sub-regional Arab diversity.

5. **Gulf-specific and Maghreb-specific knowledge**: UAE, Kuwait, and KSA have distinct social and legal norms (e.g., kafala system, Vision 2030, tribal governance) that differ from Levantine or North African contexts. Morocco's Amazigh-Arabic bilingual cultural identity is unlikely to appear in MMLU. These subpopulations are probable blind spots.

6. **Contested history scoring**: For questions where multiple legitimate historical perspectives exist (e.g., 1948 war, Lebanese Civil War, Western Sahara), MMLU's single-label MCQ format cannot capture the multi-perspective output the system is designed to produce. Search should investigate whether any Arab-focused benchmarks use multi-label or free-response scoring for contested historical content.