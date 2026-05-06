## Use Case
An AI translation system converts official government documents — agricultural input subsidy notices, land-use policy updates, and credit-scheme terms from federal and regional bureaus — into Amharic for use by farmer cooperative leaders and rural microfinance clients (e.g., ACSI, ADCSI borrowers) in the Amhara region of Ethiopia. The deployment operates at document level and must handle specialized bureaucratic, agricultural, and financial terminology accurately.

## Target Population
Geography: Amhara region, Ethiopia (rural and peri-urban areas served by agricultural cooperatives and microfinance institutions). Sub-national cohort: farmer cooperative leaders and rural microfinance clients, including ACSI/ADCSI borrowers. Language: Amharic (primary target language; source documents may originate in Amharic or other Ethiopian official registers). Occupation/role: cooperative extension leaders interpreting binding policy and loan documents; smallholder farmers and borrowers acting on subsidy and credit terms. Demographic relevance: predominantly rural, varying literacy levels, reliance on trusted administrative vocabulary already established through prior government communications.

## Elicitation Responses

Q1 [IO]: The benchmark under assessment may cover specific document genres that differ from your deployment's targets. Your deployment targets agricultural input subsidy notices, land-use policy updates, and credit-scheme terms — genres with distinctive bureaucratic phrasing, legal terminology, and numbered clause structures. Are there document types in your deployment that combine legal/regulatory language with agricultural or financial jargon in ways that may differ substantially from the benchmark's coverage?
A1: The benchmark's evaluation data (Flores-200) covers health and IT domains; the deployer acknowledges it does not cover agricultural domains. The deployer does not expect substantial structural differences at the document level, but does anticipate domain-specific terminology in agriculture that the benchmark has not explicitly evaluated.

Q2 [IC]: Government and lender documents in Amhara often carry culturally specific concepts — cooperative membership tiers, traditional land-tenure categories, regionally named subsidy schemes. Would your target documents contain terminology like these that requires locally grounded Amharic equivalents rather than direct transliterations or generic terms?
A2: The deployer confirms culturally specific concepts exist but notes that Ethiopian agricultural land-tenure terminology has been substantially standardized through federal and regional proclamations, which have replaced many traditional local terms with official administrative vocabulary. Some domain-specific terms remain that may not appear in general-purpose translation benchmarks.

Q3 [OC]: For your deployment, who should be the authority on whether an Amharic translation of a subsidy notice or loan agreement is correct and trustworthy — federal bureau translators, regional bureau staff, cooperative extension workers, or the farmer leaders and borrowers themselves?
A3: The deployer considers domain-trained federal bureau translators as the primary authority; in their absence, regional bureau staff and cooperative extension workers are acceptable fallbacks. The deployer implicitly treats the cooperative leaders and borrowers as end-consumers of translation rather than validation authorities, though administrative vocabulary familiar to those users matters for practical uptake.

Q4 [OF]: Do target users need translated output that preserves the original document structure — numbered clauses, tables of subsidy rates, signature blocks — or is flowing prose acceptable? Must layout be mirrored exactly for legal and administrative compliance?
A4: The deployer's answer is modality-contingent: if the model is multimodal and can process document layout, full structural preservation (tables, numbered clauses, etc.) is expected; if the model is text-only, flowing prose translation is acceptable. This deployment uses a text-only model (NLLB), so prose output without layout preservation is considered acceptable.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | Flores-200 evaluation data covers health and IT domains, not agricultural policy or financial/credit genres, creating a direct coverage gap for the deployment's core document types. |
| IC | HIGH | Deployment involves normatively consequential content (binding subsidy and loan terms) and the benchmark contains no validated agricultural or Ethiopian bureaucratic content; federally standardized terminology partially mitigates but does not eliminate culturally specific instantiation risk. |
| IF | LOWER | Both benchmark and deployment are text-only; no script, infrastructure, or modality mismatch — Amharic (Ethiopic script) is present in NLLB's 200-language scope. |
| OO | HIGH | NLLB/Flores-200 scores translation quality against general-domain held-out sentences; no output scoring rubric exists for domain-consistent rendering of agricultural jargon, subsidy eligibility conditions, or loan penalty clauses, meaning metric scores may not reflect fitness for this use case. |
| OC | HIGH | Flores-200 reference translations were produced by professional translators against general-domain sentences; ground-truth labels are not annotated by domain-trained Ethiopian agricultural or financial translation specialists, creating a clear annotator-population mismatch for this deployment. |
| OF | LOWER | User confirmed that flowing prose text output is acceptable given a text-only model; the benchmark's text output format aligns with this relaxed requirement, reducing structural format mismatch risk. |

## Flagged Gaps

1. **Agricultural and financial domain coverage in Flores-200**: The benchmark's held-out sentences are drawn from health and IT domains (Wikinews/WikiMatrix heritage). Downstream search should investigate whether any Flores-200 or NLLB evaluation extensions have added Ethiopian agricultural, land-tenure, or microfinance content, or whether alternative MT benchmarks cover these domains in Amharic.

2. **Ethiopic-script Amharic translation quality at document level**: NLLB reports sentence-level BLEU/chrF scores; the deployment is document-level. Search should find evidence on NLLB's document-level coherence for Amharic, including terminology consistency across clauses — critical for subsidy eligibility conditions and loan agreements.

3. **Ethiopian federal and regional administrative vocabulary coverage**: Federally standardized land and credit terminology (per Ethiopian proclamations) may or may not be present in NLLB's training corpora. Search should investigate what Ethiopian-government-domain parallel data, if any, was included in NLLB's CCAligned or mC4-derived training sets, and whether known mistranslations of official Ethiopian administrative terms have been documented.

4. **Annotator provenance for Amharic in Flores-200**: The deployer identified federal bureau translators as the appropriate validation authority. Search should determine who translated the Amharic portion of Flores-200 (professional generalist translators vs. domain specialists), what quality controls were applied, and whether any post-publication audits of Amharic translation quality exist.

5. **Sub-national Amhara regional variation**: Amhara encompasses diverse agro-ecological zones (highland, lowland) and distinct cooperative/microfinance administrative structures (e.g., ACSI vs. ADCSI service areas). The benchmark treats Amharic as a monolithic target language. Search should assess whether NLLB evaluation data or training corpora reflect regional administrative register differences within Amhara.

6. **Toxicity and mistranslation risk in binding legal documents**: NLLB includes a toxicity benchmark, but no evidence exists that it covers false precision in legal/financial clauses (e.g., penalty amounts, eligibility cutoffs). Search should identify any documented cases of NLLB mistranslating numerical or conditional legal content in low-resource African languages.