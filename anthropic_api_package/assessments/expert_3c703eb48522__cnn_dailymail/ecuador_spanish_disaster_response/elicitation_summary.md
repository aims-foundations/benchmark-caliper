## Use Case
An AI system processes Spanish-language tweets about natural disasters in Ecuador to generate timelines that help NGO and international organization analysts (Red Cross, UN OCHA) track how affected populations' needs evolve over time. The system must anchor events to Ecuador-specific geographic and institutional references and summarize content at a level of operational relevance calibrated to humanitarian coordination.

## Target Population
Latin America (Ecuador as primary deployment geography); social and data analysts at NGOs and international organizations fluent in American English and Spanish, potentially speakers of varied Latin American Spanish accents; inter-operational teams including field coordinators, domain experts, and social analysts who collectively judge output quality; affected populations who author tweets in informal to semi-formal Ecuadorian Spanish, potentially mixing Kichwa or other indigenous-language terms in entity names and place references.

## Elicitation Responses

Q1 [IO]: The benchmark under assessment covers a specific set of categories within its task domain. For your Ecuador-focused deployment, are there disaster types your users would prioritize — for example, volcanic eruptions (Cotopaxi, Tungurahua), landslides triggered by La Niña events, floods in coastal regions like Manabí, or earthquake aftershock sequences — that may fall outside the coverage of a general-purpose benchmark? Which crisis types matter most to Red Cross and UN OCHA coordinators in your context?
A1: The deployment focuses on large-scale social and humanitarian crises — those whose impact exceeds local response capacity — rather than any single disaster type. Users would prioritize events by population impact and response-gap severity, not by disaster category alone, meaning coverage must extend to compound and socio-political crises beyond natural hazards.

Q2 [IC]: Benchmarks in this domain often reference geographic markers and institutional handles tied to the cultural context in which they were built. In your deployment, location signals in tweets would reference Ecuadorian administrative units (parroquias, cantones, provincias), local emergency agencies (SGR, Cuerpo de Bomberos), and landmarks familiar to Ecuadorian users. Would your analysts expect the system to correctly anchor events to these local geographic and institutional references, or is rough regional-level geolocation sufficient?
A2: Analysts expect precise anchoring to Ecuador-specific entities — administrative units, local emergency agencies, and institutional actors — not merely rough regional-level geolocation.

Q3 [OC]: The benchmark's ground-truth labels and reference outputs were produced by annotators operating in a different cultural and operational context from your deployment. For your use case, relevance judgments may differ: a tweet about road access to a rural community, or an informal community radio broadcast transcribed into Twitter, might carry high operational value for an NGO coordinator but low value by external annotation standards. Who in your organization would serve as the authoritative judge of tweet relevance and summary quality — field coordinators, social analysts, or affected-community representatives — and do you have access to them for validation?
A3: Judgment authority rests with an inter-operational team rather than any single role; field coordinators, social analysts, and domain experts collectively determine relevance and summary quality. No single annotator archetype captures the authoritative standard.

Q4 [IF]: The benchmark's input signal may be drawn from a language and register different from your deployment context. Your deployment targets Ecuadorian Spanish, which may include code-switching with Kichwa or other indigenous languages, regional slang, informal abbreviations common in disaster contexts, and non-standard orthography in crisis conditions. Would the tweet stream your system processes be predominantly standard written Spanish, or do you expect significant informal register, dialect variation, or indigenous-language mixing?
A4: The input stream is predominantly Ecuadorian Spanish in a mixed informal-to-semi-formal register, with local indigenous-language terms appearing mainly in place and entity names. A system trained only on English social media (even if fine-tuned on generic Spanish) would likely miss dialect-specific and register-specific characteristics of Ecuadorian crisis-time social media.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers general English-language news comprehension via Cloze tasks; it has no coverage of humanitarian crisis taxonomy, Latin American disaster types, or socio-political emergency categories that drive operational relevance for NGO users. |
| IC | HIGH | Benchmark instances use US/UK news articles with Western geographic and institutional references; deployment requires anchoring to Ecuador-specific administrative units, local agencies, and informal disaster-register vocabulary — a profound content mismatch. |
| IF | HIGH | The benchmark is English text drawn from formal news; deployment data is informal-to-semi-formal Ecuadorian Spanish tweets, potentially mixing Kichwa entity names, non-standard orthography, and crisis-specific abbreviations — a language, register, and genre mismatch. |
| OO | HIGH | The benchmark's output ontology is Cloze-style entity fill-in, a classification/retrieval task; the deployment requires temporal timeline generation and operational relevance ranking, which are fundamentally different output structures with no correspondence to the benchmark's category space. |
| OC | HIGH | Benchmark labels were produced by automated conversion of CNN/Daily Mail summaries — non-representative of humanitarian operational judgment; deployment requires inter-operational team validation by field coordinators and domain experts assessing Ecuadorian crisis content. |
| OF | HIGH | The benchmark outputs entity labels (token-level answer fill-in); the deployment requires temporally ordered, narrative-form timeline summaries suited to NGO coordination workflows — the output form is categorically mismatched. |

## Flagged Gaps

1. **Language and dialect coverage**: The benchmark is English-only; downstream search should investigate whether any Spanish-language disaster-tweet benchmarks exist for Latin American or specifically Ecuadorian Spanish, and whether any cover informal register and crisis-time orthographic variation.

2. **Kichwa and indigenous-language entity mixing**: No benchmark metadata indicates coverage of Kichwa or other Ecuadorian indigenous languages appearing as place names or entity tokens in Spanish tweets. Search should probe available NLP resources for Kichwa-Spanish code-switching in social media contexts.

3. **Ecuadorian administrative and institutional entity recognition**: Search should investigate whether named-entity and geolocation benchmarks cover Ecuador's sub-national administrative hierarchy (parroquias, cantones, provincias) and local emergency management actors (SGR, Cuerpo de Bomberos Ecuador).

4. **Humanitarian crisis taxonomy for Latin America**: The benchmark has no humanitarian-operations framing. Search should identify disaster-domain tweet corpora (e.g., TREC-IS, CrisisNLP, HumAID) and assess their coverage of Latin American or Ecuadorian events and socio-political/compound crises.

5. **Timeline generation as an output task**: The benchmark evaluates reading comprehension via entity prediction, not temporal summarization. Search should investigate whether any timeline generation benchmarks exist for disaster response, and whether their annotation methodology could transfer to an inter-operational humanitarian team validation protocol.

6. **Annotator representativeness for inter-operational judgment**: No existing benchmark is likely to have been validated by the type of multi-role inter-operational team described. Search should look for humanitarian NLP annotation frameworks (e.g., UN OCHA or IFRC data-for-good projects) that approximate this validation structure.

7. **Informal social media register in disaster contexts**: Search should investigate whether crisis-tweet benchmarks (e.g., CrisisLex, DISASTER corpora) include Spanish-language data and whether they capture the informal abbreviations and register variation characteristic of Ecuadorian Twitter during emergencies.