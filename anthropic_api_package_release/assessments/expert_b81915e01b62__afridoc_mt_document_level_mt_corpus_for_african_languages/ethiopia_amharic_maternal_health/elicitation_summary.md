## Use Case
An AI-powered machine translation system converts English-language clinical practice guidelines, vaccination schedules, and maternal-health booklets into Amharic for distribution by Ethiopia's Ministry of Health. The primary consumers are health workers and patients across Ethiopia's regional health bureaus, who will produce and act on these translated materials.

## Target Population
Geography: Ethiopia, spanning multiple regional health bureaus including Tigray, Oromia, Amhara, and Somali regions. Language: Amharic (primary target); regional register variation is acknowledged. Occupational roles: clinical translators, Amharic-speaking physicians, community health extension workers, and semi-literate patients. The authoritative ground-truth judges are MOH-trained clinical translators or Amharic-speaking physicians; approved terminology resources include MOH and EFDA glossaries.

## Elicitation Responses

Q1 [IO]: The benchmark covers health documents, but clinical practice guidelines, vaccination schedules, and maternal-health booklets have specific structural features — numbered protocols, dosage tables, immunization timetables, warning boxes, and administrative forms. Does your deployment need to handle these structured document types, or is it primarily narrative/prose health content? Are there other document formats common in Ethiopian ministry-of-health materials that you'd consider critical to cover?
A1: The deployment can reasonably be scoped to prose/narrative health content since the benchmark draws from WHO articles; highly structured document types (tables, timetables, administrative forms) are considered out of scope for this evaluation. The user accepts that focus on general health prose is appropriate.

Q2 [IC]: Ethiopian clinical and maternal-health documents often reference locally specific content: Ethiopian calendar dates, endemic diseases prevalent in Ethiopia by region, local nutrition guidance, or Ethiopia-specific referral pathways. Would your source documents contain this kind of Ethiopia-specific clinical content, and would a system trained on more generic health text be expected to handle it correctly?
A2: The benchmark's WHO-sourced documents are unlikely to contain Ethiopia-specific clinical content. The user accepts that generic health-text training should suffice for general translation tasks (including date conversion), and believes models trained on general health corpora can handle endemic-disease terminology translation adequately.

Q3 [OC]: Whose judgment should be authoritative for ground-truth translation quality — MOH-trained clinical translators, Amharic-speaking physicians, health extension workers, or patients? Do regional Amharic registers and health terminology vary enough across bureaus that a single Addis Ababa-based translator's choices would not be trusted equally across Tigray, Oromia, or Somali regions?
A3: MOH-trained clinical translators are the preferred ground-truth authority; Amharic-speaking physicians are an acceptable fallback. Regional register variation across bureaus is implicitly acknowledged but not deeply explored — no clear resolution was offered for whether Addis Ababa-centric translations would be uniformly accepted across all regional bureaus.

Q4 [OO]: Which success criteria govern translation quality — faithfulness to source meaning, terminological consistency across a full document, readability for semi-literate patients, or compliance with MOH-approved glossaries?
A4: The team prioritizes a multi-metric approach combining automatic MT metrics, faithfulness to source meaning, terminological consistency across the document, and compliance with MOH and EFDA approved glossaries. Both MOH and EFDA glossaries exist and are available as reference resources.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | The benchmark was ground-up designed for African languages including Amharic, and the user has scoped deployment to prose health content that aligns with the WHO-sourced benchmark corpus; structured document types are out of scope, reducing the category-coverage gap. |
| IC | HIGH | The benchmark lacks Ethiopia-specific clinical content (local disease patterns, referral pathways, calendar systems), and while the user accepts generic coverage for now, this gap introduces construct-irrelevant variance for a deployment serving real MOH distribution in a highly contextual health environment. |
| IF | LOWER | Both benchmark and deployment are text-only in Amharic, a language the benchmark explicitly includes; no modality or script mismatch is present. |
| OO | HIGH | The deployment requires compliance with MOH/EFDA-approved glossaries and document-level terminological consistency as primary scoring criteria, but the benchmark's scoring functions may not operationalize these institutional standards, creating a mismatch in what "correct translation" means. |
| OC | HIGH | Ground-truth labels in the benchmark may not have been produced by MOH-trained clinical translators or Amharic-speaking physicians; the user explicitly named these as the authoritative population, and annotator-population mismatch in a sensitive health domain poses direct risk to label validity. |
| OF | LOWER | Both the benchmark and deployment use text output; the MCQ-vs-open-ended distinction does not apply here, and the document-level translation format of the benchmark matches the deployment's document translation need. |

## Flagged Gaps

1. **Annotator identity and credentials in AFRIDOC-MT**: Downstream search should investigate who produced the Amharic reference translations in the benchmark — whether they are MOH-credentialed clinical translators, general Amharic translators, or academics. This is the single most consequential OC gap given the user's explicit authority hierarchy.

2. **MOH and EFDA glossary conformance in benchmark scoring**: The benchmark's evaluation protocol should be examined for whether it incorporates any Ethiopia-specific approved terminology lists. If scoring is purely automatic (BLEU, chrF, COMET), it will not capture compliance with MOH/EFDA glossaries — a primary success criterion for this deployment.

3. **Regional Amharic register variation**: The user did not resolve whether Addis Ababa-centric Amharic translations are trusted equally in Tigray, Oromia, and Somali regional bureaus. Search should investigate documented variation in Amharic health terminology or dialect differences across these bureaus that could affect deployment validity beyond what a single national-level reference translation captures.

4. **WHO-source document representativeness for Ethiopian MOH materials**: The benchmark's health documents are sourced from WHO articles. Search should determine whether WHO clinical language and document structures align sufficiently with Ethiopia MOH distribution materials, or whether key document genres (vaccination schedules, maternal-health booklets) are systematically absent.

5. **Ethiopian calendar and locally endemic disease terminology**: Even though the user accepted generic coverage as sufficient, downstream search should verify whether existing Amharic MT benchmarks or models have documented failure modes on Ethiopian-calendar date expressions or terminology for diseases like kala-azar, given the deployment's real-world clinical stakes.