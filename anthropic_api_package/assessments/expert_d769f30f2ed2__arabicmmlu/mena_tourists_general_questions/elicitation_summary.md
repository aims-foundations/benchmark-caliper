## Use Case
An AI assistant helps non-Arab tourists and expats visiting eight Arabic-speaking countries (Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, KSA) answer general questions about Arabic language, history, and geography — at roughly the level of knowledge covered in school curricula. The system is not intended to handle practical travel logistics, etiquette, or real-time local customs.

## Target Population
Geography: Eight MENA countries — Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, Saudi Arabia. Sub-national variation exists (e.g., distinct Moroccan vs. Levantine vs. Gulf contexts) but users are international visitors, not residents. Language(s): Primary interaction in Arabic (Arabic learners using MSA); English and other languages potentially supported but would require additional validation. Role: Tourists and expats seeking educational-level knowledge about the Arab world. Demographics: Non-native Arabic speakers, likely varied nationalities, with some basic-to-intermediate Arabic language competence.

## Elicitation Responses

Q1 [IO]: Your users are tourists and expats visiting specific countries — Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, and KSA. Should the system handle practical, on-the-ground knowledge that foreigners typically need, such as local dialect phrases, tourist etiquette, religious customs, or navigating local transport and markets? Are there categories of questions you expect frequently that go beyond formal history and geography?
A1: The system is scoped to school-curriculum-level general knowledge (history, geography, Arabic language). Dialectal phrases, tourist etiquette, religious customs, and practical navigation are acknowledged as frequently expected but fall outside the intended scope; other benchmarks (e.g., MADAR) address dialectal Arabic separately.

Q2 [IC]: Does the system need to reflect country-specific cultural nuances accurately, or is a pan-Arab generalized framing acceptable?
A2: Pan-Arab generalized framing is broadly acceptable given shared religious and linguistic culture across the region, but the system should flag content that is country-specific rather than silently generalizing it.

Q3 [OO]: When answering history or geography questions where different countries hold competing official or cultural positions, should the system give a single answer, acknowledge multiple perspectives, or tailor the answer by country?
A3: The system should explicitly acknowledge multiple perspectives and note that different countries hold different positions, signaling to the user that the topic is contested and potentially sensitive.

Q4 [IF]: Will users interact in Arabic or another language, and what is the expected modality distribution?
A4: The benchmark is in Arabic, targeting Arabic learners who will prompt in MSA. English and other languages may be supported but would require separate training and cross-lingual evaluation; this is outside the current benchmark scope.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers MSA school-curriculum content, but the deployment spans eight countries including Morocco and Palestine, which have historically distinct educational curricula and are underrepresented or absent in ArabicMMLU's source countries; practical travel knowledge is explicitly out of scope but the school-knowledge framing still leaves coverage gaps for country-specific topics. |
| IC | MODERATE | Pan-Arab framing is acceptable per the user, reducing the risk of country-specific content mismatch, but contested historical content (e.g., Palestinian narratives, 1948 war) and the benchmark's "transferred from different cultural context" sourcing flag introduce some construct-irrelevant variance. |
| IF | MODERATE | The deployment is text-only and the benchmark is text-only, which aligns well; however, users are non-native Arabic speakers interacting in MSA, and the benchmark's MSA register may not match the learner-level Arabic actually produced by tourists, creating a signal-distribution gap. |
| OO | HIGH | The deployment explicitly requires multi-perspective acknowledgment of contested historical and civic questions, but ArabicMMLU uses a single-correct-answer MCQ format — this structural mismatch means the benchmark's output taxonomy cannot capture the pluralistic framing the deployment requires. |
| OC | MODERATE | ArabicMMLU was constructed with native Arabic speaker collaboration across several target countries, which is a positive signal; however, Morocco and Palestine are either absent or underrepresented as source countries, and annotation pools for contested historical content may not reflect the full range of regional stakeholder perspectives. |
| OF | HIGH | The benchmark produces discrete MCQ labels, but the deployment requires open-ended, explanatory, multi-perspective natural-language responses — this is a direct mismatch in output form that the benchmark cannot evaluate as-is. |

## Flagged Gaps

1. **Morocco coverage**: ArabicMMLU sources questions from Jordan, Egypt, UAE, Lebanon, Saudi Arabia, and others, but Morocco is listed as a deployment target and its distinct Maghrebi curriculum, French-influenced educational tradition, and Darija-adjacent cultural framing are likely absent from the benchmark. Downstream search should investigate whether any ArabicMMLU tasks or question pools are sourced from Moroccan educational materials.

2. **Palestine coverage**: Palestine is a deployment target with historically distinct and politically sensitive educational narratives (1948, occupation, statehood). It is unclear whether ArabicMMLU includes Palestinian-sourced questions or whether Palestinian perspectives on shared historical events are represented. This is a critical gap given the multi-perspective output requirement.

3. **Kuwait coverage**: Kuwait is a deployment target; its presence in ArabicMMLU's eight source countries should be verified, as the benchmark lists Jordan, Egypt, UAE, Lebanon, and Saudi Arabia prominently but Kuwait is ambiguous in the metadata.

4. **MSA vs. learner-level Arabic input mismatch**: The benchmark assumes fluent MSA input, but the actual user population consists of Arabic learners whose prompts may be grammatically imperfect or code-switched. Whether the evaluated system handles learner-register Arabic robustly is not captured by this benchmark.

5. **Multi-perspective / open-ended output evaluation**: The benchmark cannot assess whether the system correctly acknowledges contested topics or provides appropriately nuanced multi-country framings, since it scores only single correct MCQ labels. Downstream search should identify any Arabic-language benchmarks or evaluation frameworks designed for open-ended, multi-perspective historical/civic question answering.

6. **Cross-lingual capability for non-Arabic users**: English and other language interactions are anticipated but untested by this benchmark. Downstream search should identify cross-lingual or translation-augmented evaluation suites that cover Arabic-to-English knowledge transfer for the specific subject domains (history, geography, language) in the deployment.