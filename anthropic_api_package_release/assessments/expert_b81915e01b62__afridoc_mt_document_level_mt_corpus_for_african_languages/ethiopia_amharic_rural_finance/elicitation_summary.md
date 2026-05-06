## Use Case
A machine translation system translates official agricultural input subsidy notices, land-use policy updates, and credit-scheme terms issued by federal and regional bureaus into Amharic. The deployment serves cooperative leaders and rural microfinance clients in Amhara region who must correctly interpret binding government and lender documents. The benchmark under evaluation (AFRIDOC-MT) covers document-level MT for health and IT news domains, translated from English into five African languages including Amharic.

## Target Population
Geography: Amhara region, Ethiopia (sub-national; rural and peri-urban cooperative and microfinance contexts).
Languages: Amharic (primary target); source documents in Amharic or Ethiopian government-register language from federal/regional bureaus.
Roles: Farmer cooperative leaders, rural microfinance clients (ACSI, ADCSI borrowers), and potentially cooperative extension workers who mediate document interpretation.
Relevant demographics: Largely rural adult population with variable literacy levels; familiar with prior government communications and their characteristic administrative vocabulary; subject to proclamation-derived land and credit terminology rather than traditional local terminology in formal documents.

## Elicitation Responses

Q1 [IO]: The benchmark covers health and IT news documents. Your deployment targets agricultural input subsidy notices, land-use policy updates, and credit-scheme terms — genres with distinctive bureaucratic phrasing, legal terminology, and numbered clause structures. Are there document types in your deployment that combine legal/regulatory language with agricultural or financial jargon in ways that differ substantially from health or tech reporting? For example, do your documents include itemized eligibility conditions, penalty clauses, or seasonal deadlines that require consistent terminology across long stretches of text?
A1: The user acknowledges the domain gap (health/IT vs. agriculture/finance/policy) but believes document-level structural demands are broadly similar across genres. The main concern is that certain agricultural domain-specific terminologies will not be represented in the benchmark's training or evaluation data, even if discourse-coherence requirements are comparable.

Q2 [IC]: Government and lender documents in Amhara often carry culturally specific concepts — such as cooperative membership tiers, traditional land-tenure categories (e.g., rist), or regionally named subsidy schemes. Would your target documents contain terminology like these that requires locally grounded Amharic equivalents rather than direct transliterations or generic terms?
A2: The user agrees that culturally specific concepts exist, but notes that in contemporary Ethiopian agricultural and land-tenure contexts, formal documents draw primarily from federal and regional proclamation-derived terminology rather than traditional local terms. The operative vocabulary is thus legally standardized, though it may still be unfamiliar to rural end-users.

Q3 [OC]: For your deployment, who should be the authority on whether an Amharic translation of a subsidy notice or loan agreement is correct and trustworthy?
A3: The user identifies domain-trained federal bureau translators as the preferred ground-truth authority. In their absence, regional bureau staff and cooperative extension workers are acceptable surrogates. The answer implies a professional-administrative annotator standard rather than end-user farmer judgment, though usability by cooperative leaders remains an implicit requirement.

Q4 [OF]: Do target users need translated output that preserves the original document structure (numbered clauses, tables, signature blocks), or is flowing prose acceptable?
A4: Format requirements are contingent on model modality: multimodal models should preserve tables and document layout; text-only models may produce flowing prose. Structural fidelity is preferred where technically feasible but is not an absolute requirement when the model is text-only.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark's domain coverage (health, IT news) does not include agricultural policy, land-use regulation, or credit-scheme documents, meaning the benchmark's test-case category distribution is systematically misaligned with the deployment's document genres, even if discourse-structural demands are comparable. |
| IC | HIGH | Agricultural proclamation-derived terminology, subsidy scheme names, credit-condition phrasing, and land-tenure vocabulary are absent from health/IT benchmark instances; these specialized terms are the exact content where translation errors have binding legal and financial consequences for end-users. |
| IF | LOWER | Both the benchmark and the deployment are text-only; the target language (Amharic) is present in the benchmark and uses Ethiopic script, which the benchmark explicitly covers; no modality mismatch is introduced. |
| OO | MODERATE | The benchmark's output evaluation is designed around document-level coherence and translation adequacy in health and IT contexts; scoring rubrics may not capture domain-specific terminological consistency (e.g., stable rendering of proclamation terms across clauses), which is the critical coherence requirement for legal-administrative documents. |
| OC | HIGH | The benchmark was designed for health and IT domains with its own annotator pool; ground-truth labels for agricultural/financial Amharic translation would ideally come from federal bureau translators or domain-trained regional staff — a population that almost certainly differs from the benchmark's annotators, risking label mismatch on domain-specific correctness judgments. |
| OF | MODERATE | The benchmark evaluates document-level text translation, which broadly matches the text-only deployment scenario; however, the deployment's preference for structure preservation (tables, numbered clauses) when feasible is not assessed by a text-only benchmark, leaving a partial gap for multimodal or format-sensitive use cases. |

## Flagged Gaps

1. **Agricultural and regulatory domain absence**: The benchmark contains zero agricultural policy, land-use, or credit-scheme documents. Downstream search should investigate whether any Amharic MT benchmark or evaluation dataset covers Ethiopian government regulatory genres (e.g., input subsidy proclamations, cooperative proclamations, MFI loan agreements), and whether AFRIDOC-MT's Amharic translators had any domain exposure to these text types.

2. **Proclamation-register Amharic terminology**: Ethiopian federal and regional proclamations use a distinct formal register in Amharic that differs from everyday or health-domain language. Flagged for investigation: whether the benchmark's Amharic reference translations reflect this register, and whether any terminology glossaries (e.g., from the Ministry of Agriculture, ATA, or regional bureaus) exist that could serve as a domain-specific evaluation anchor.

3. **Annotator domain expertise**: The user specifies that federal bureau translators are the preferred authority. Search should surface information on who translated the Amharic documents in AFRIDOC-MT, their institutional affiliation, and whether they have agricultural or legal translation backgrounds — this directly affects OC validity.

4. **Amhara sub-regional variation**: The target population is specifically in Amhara region, which has its own regional bureau terminology and Amharic dialect features. The benchmark targets Amharic broadly without specifying regional register. Downstream search should check whether AFRIDOC-MT's Amharic translations reflect a generic/national standard or a specific regional variety, and whether Amhara-specific administrative vocabulary diverges from that standard.

5. **Document structure evaluation**: If the deployment evolves toward multimodal or format-preserving translation (tables, signature blocks, numbered clauses), AFRIDOC-MT's text-only evaluation framework will not measure this capability. Search should identify whether any African-language MT benchmarks evaluate structured-document fidelity, particularly for administrative or legal document types.

6. **Low-literacy end-user accessibility**: Although the formal authority for translation correctness rests with bureau translators, the downstream consumers are rural cooperative members and microfinance clients with variable literacy. No elicitation question directly addressed literacy-level appropriateness of translation outputs. This gap should be flagged for any downstream usability or comprehension evaluation design.