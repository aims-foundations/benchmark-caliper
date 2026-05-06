## Use Case
An environmental scientist based in Mymensingh, Bangladesh wants to assess the agricultural and environmental science knowledge of LLMs (frontier models vs. small/regional models) across South Asian contexts — including flood-plain farming in the Bangladesh delta, dry-land cropping in Telangana, and coastal aquaculture in Andhra Pradesh. The benchmark (MMLU) is being evaluated for its validity as a measure of this region-specific, multilingual agricultural knowledge.

## Target Population
- **Geography:** South Asia broadly; primary user anchor is Mymensingh, Bangladesh (Brahmaputra-Jamuna delta region); secondary contexts include Telugu-speaking Telangana and Andhra Pradesh, India
- **Sub-national cohort:** Mymensingh district Bengali speakers (distinct from Dhaka or West Bengal Bengali); Telugu-speaking agrarian communities in Telangana/Andhra Pradesh
- **Languages:** Bangladeshi Bengali (Mymensingh dialect), standard Bengali (Indian and Bangladeshi variants), Telugu, and English as a query/evaluation medium
- **Occupation/Role:** Environmental scientist and researcher; downstream knowledge concerns also extend to farmers and agronomists in both Bangladesh and South India
- **Demographic details:** Cross-border context with geo-political sensitivity (Bangladesh–India water-sharing and agricultural agreements); multi-ethnic, multi-linguistic, multi-national population with divergent agricultural practice traditions

## Elicitation Responses

Q1 [IO]: Your deployment targets agricultural and environmental science knowledge across South Asian regions — including flood-plain farming in the Brahmaputra-Jamuna delta near Mymensingh, dry-land cropping in Telangana, or coastal aquaculture in Andhra Pradesh. Does the benchmark's subject coverage adequately represent the agro-ecological, soil, crop, and climate-specific knowledge your scientist actually needs, or are those agricultural subdomains largely absent from the benchmark's subject taxonomy?
A1: The benchmark contains only surface-level agricultural knowledge about parts of India; depth-level subject knowledge for the specific agro-ecological subdomains (delta flood-plain farming, haor wetland ecology, dry-land Telugu region cropping) is largely absent from MMLU's subject taxonomy.

Q2 [IC]: Your deployment involves Bengali as spoken in Mymensingh — a dialect with distinct vocabulary and phonological patterns. Would benchmark content reflect standard or Indian-leaning Bengali rather than Bangladeshi/Mymensingh variants? Would dialect-specific agricultural terminology (local crop names, land-tenure terms, irrigation vocabulary) be represented?
A2: The benchmark content defaults to fairly standard Bengali wording with possible implicit Indian Bengali stylistic leanings; dialect-specific agricultural terminology from the Mymensingh/Bangladeshi context is absent, and including it would make the benchmark more robust.

Q3 [OC]: For agricultural and environmental science questions relevant to Bangladesh — haor wetland ecology, boro rice cultivation cycles, flood management under Bangladesh's river systems — would answer keys derived from a non-Bangladeshi annotation context be considered authoritative by Mymensingh-based scientists? Are there cases where the correct answer for a Bangladeshi context would differ from the benchmark's marked answer?
A3: There is potential for divergent correct answers, particularly around cross-border water-sharing agreements and associated geopolitical sentiment between Bangladesh and India — those differing perspectives should be captured gracefully. Indian-exam-derived answers would be considered authoritative in some limited cases, but the core concern is that agricultural and practice differences between regions are not adequately captured or differentiated in ground-truth labels.

Q4 [IF]: Will LLMs being evaluated receive queries in regional South Asian languages, in English, or a mix? Is the Mymensingh scientist expected to query in standard Bengali script, colloquial Bangladeshi Bengali, or English?
A4: Queries should include Indian regional languages (notably Telugu) as well as Bengali in both its Indian and Bangladeshi varieties — the evaluation is explicitly multilingual and not English-only, which is a direct mismatch with MMLU's English-only input design.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MMLU's 57-subject taxonomy has no dedicated agro-ecological or South Asian regional agricultural subdomains; depth-level coverage of delta farming, haor ecology, or Telugu dry-land cropping is confirmed absent by the user. |
| IC | HIGH | Benchmark content carries US/Western defaults and lacks Bangladeshi or Telugu regional agricultural terminology, crop names, land-tenure vocabulary, and delta-specific environmental concepts confirmed missing by the user. |
| IF | HIGH | The deployment explicitly requires multilingual queries (Telugu, Bangladeshi Bengali, Indian Bengali) whereas MMLU is English-only text input — a direct modality/language mismatch confirmed by the user. |
| OO | HIGH | MMLU's output taxonomy (MCQ label selection across generic subjects) does not map onto region-specific agricultural knowledge assessment; legitimate pluralism exists in cross-border agronomic and water-management practice interpretations. |
| OC | HIGH | Ground-truth labels were not validated by South Asian or Bangladeshi agronomists; the user confirms that cross-border water/agricultural agreement questions could yield divergent correct answers depending on national perspective, and that practice differences are not reflected in answer keys. |
| OF | MODERATE | MMLU's MCQ label output format partially aligns with evaluation needs, but the deployment may benefit from open-ended generation to capture nuanced agricultural practice differences; the user did not specifically flag output form as a primary concern. |

## Flagged Gaps

1. **Mymensingh dialect Bengali agricultural terminology:** No evidence that MMLU or any standard benchmark includes Mymensingh-accented or Bangladeshi-variant Bengali agricultural vocabulary (local crop names, haor/beel wetland terms, boro/aman/aus rice cultivation cycles, char-land farming terminology). Web search should investigate whether any South Asian agricultural NLP benchmark covers Bangladeshi Bengali at dialect level.

2. **Telugu-medium agricultural content:** MMLU is English-only; there is no Telugu-language input coverage. Web search should identify whether Telugu-language agricultural or environmental science benchmarks exist (e.g., IndicGLUE, AI4Bharat datasets, or Telugu-specific agri-knowledge corpora).

3. **Haor and floodplain ecology subject coverage:** MMLU lacks depth in Bangladesh-specific agro-ecology (haor wetlands, Sylhet basin, Brahmaputra-Jamuna char agriculture, saline intrusion in coastal Bangladesh). Downstream search should identify whether any environmental science benchmark covers these sub-regional ecosystems.

4. **Cross-border geopolitical framing in answer keys:** Questions touching on Bangladesh–India water agreements (Ganges/Farakka, Teesta), shared river basin management, or comparative farming policy may have politically contingent correct answers. No MMLU annotation controls for this. Search should investigate whether any benchmark explicitly handles cross-border South Asian agri-policy pluralism.

5. **Indian regional language agricultural benchmarks:** For Telugu-speaking Telangana/Andhra contexts, search should identify domain-specific agricultural LLM benchmarks in Telugu or other Dravidian languages, and whether any capture dry-land farming systems, Rabi/Kharif cropping patterns specific to the Deccan plateau.

6. **Sub-national India granularity:** The deployment spans multiple Indian states (Telangana, Andhra Pradesh) with distinct agro-climatic zones; MMLU does not differentiate at sub-national Indian level. Search should flag whether any India-ported benchmark distinguishes state-level or agro-climatic zone-level agricultural knowledge.

7. **Region-specific LLM evaluation evidence:** The deployment compares frontier models against region-specific LLMs (e.g., potential BanglaLM, IndicBERT-style models). Search should investigate what evaluation infrastructure exists for Bangladeshi Bengali and South Indian language models on agricultural domain tasks.