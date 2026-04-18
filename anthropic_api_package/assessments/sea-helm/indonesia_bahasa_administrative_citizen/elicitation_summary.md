## Use Case
An Indonesian central government ministry's digital services division is evaluating LLMs to power a public-facing Bahasa Indonesia chatbot that answers citizen questions about administrative procedures — KTP applications, DJP Online tax filing, business registration, and permit renewals. The chatbot must handle step-by-step procedural instruction, document prerequisite checking, error recovery, and referral to the correct government office, and must operate across formal and informal registers of Bahasa Indonesia.

## Target Population
Indonesian citizens nationwide, with expected concentration in urban Java (Jakarta, Surabaya, Yogyakarta area); also must serve users in outer islands including East Nusa Tenggara and eastern Indonesia. Language: Bahasa Indonesia in formal and informal registers, including Javanese-influenced, Sundanese-influenced, and Betawi-inflected phrasing on the input side. Users range from low-education, non-urban citizens to urban professionals; the chatbot is a public service with explicit accessibility KPIs. Counterpart evaluators include Dukcapil and DJP civil servants, ministry legal/policy experts, and ordinary citizens who have navigated administrative procedures.

## Elicitation Responses

Q1 [IO]: Does the deployment require step-by-step procedural instruction, form-field disambiguation, error recovery, and referral to the correct government office, and which of these are most critical?
A1: All four are critical, with step-by-step procedural instruction and error recovery ranked highest — most citizen contacts occur after something went wrong (rejection, missing documents, unregistered NIK). Referral to the correct agency (Dukcapil vs. Imigrasi vs. DJP vs. OSS-RBA) is also essential due to frequent jurisdictional confusion. A fifth interaction type was added: pre-application document prerequisite checking (what to bring, format requirements, e-materai), which prevents most rejections.

Q2 [IC]: Does the chatbot need to handle regional procedural variation (kelurahan/kabupaten-level), or only standardized national-level guidance?
A2: Regional variation is unavoidable — permit requirements and KTP registration steps differ materially between DKI Jakarta (Jakipedia/JakEVO), Sleman, Makassar, and rural kabupaten. At minimum the system must not present Jakarta-specific steps as universally applicable. The user explicitly doubts SEA-HELM captures pemda-level procedural knowledge for Indonesian administrative contexts.

Q3 [OO]: Does the evaluation need to distinguish factually plausible but procedurally incorrect or outdated responses from fully regulation-compliant ones?
A3: Yes — this is the central evaluation requirement. A plausible but outdated answer (e.g., the pre-Coretax DJP e-Filing flow or pre-UU Adminduk KTP rules) is worse than a non-answer because it creates ministerial liability. For recently changed regulations, the correct behavior is to cite the regulation or SE number, timestamp the guidance, and route to the official channel rather than improvise. PP 71/2019 compliance on data handling is also a requirement.

Q4 [IC]: Should the chatbot handle informal and regionally flavored Bahasa Indonesia input, or only standard formal Indonesian?
A4: There is an explicit comprehension-vs-generation asymmetry requirement: the system must understand informal and regional-inflected input (e.g., Betawi slang, Sundanese-inflected phrasing, casual queries like "bang gimana caranya urus KTP ilang") on the comprehension side, but must produce consistent, polite, plain formal Bahasa Indonesia on the output side. The user is uncertain whether SEA-HELM evaluates this asymmetry.

Q5 [OC]: Who should be the authoritative judge of chatbot response quality, and are technically correct but inaccessible answers considered failures?
A5: A three-tier evaluator model is required: civil servants (Dukcapil, DJP) for procedural correctness, ministry legal staff for regulatory compliance, and ordinary citizens for practical usability. Responses that are technically accurate but written in impenetrable bureaucratic Indonesian are explicitly classified as failures; accessibility for low-education and non-Jakarta users is a stated KPI. The user identified a concrete gap: if SEA-HELM annotators were predominantly university-educated Jakarta residents, that population mismatch would undermine label validity for this deployment.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | SEA-HELM's task taxonomy covers NLU/NLG/NLR and cultural prompts but contains no pillar for government administrative procedure types (error recovery, prerequisite checking, jurisdictional referral) that are this deployment's primary use cases; the cultural pillar covers only Filipino (KALAHI), not Indonesian procedural contexts. |
| IC | HIGH | The deployment requires pemda-level regional procedural variation that SEA-HELM almost certainly does not capture; benchmark content is general Indonesian rather than DJP/Dukcapil/OSS-RBA domain content; the informal-to-formal comprehension asymmetry (Betawi, Sundanese-inflected input) is not evidenced in benchmark construction materials. |
| IF | MODERATE | Both deployment and benchmark are text-only in Bahasa Indonesia with Latin script, reducing signal mismatch; however, SEA-HELM's IFEval and LINDSEA were built for standard written Indonesian and may not reflect conversational, regionally inflected input forms citizens will actually use. |
| OO | HIGH | SEA-HELM's output taxonomy (culturally relevant/irrelevant for KALAHI; win-rate for MTBench; binary forced-choice for LINDSEA) does not include a regulatory-compliance dimension — the deployment requires distinguishing plausible-but-outdated from currently compliant answers, a scoring category absent from the benchmark. |
| OC | HIGH | SEA-HELM annotators are described as predominantly university students recruited via public advertisement in Singapore; the deployment's authoritative judges are a three-tier mix of civil servants, legal experts, and low-education non-Jakarta citizens — a substantial population mismatch for labeling procedural correctness and plain-language accessibility. |
| OF | MODERATE | Deployment output is open-ended conversational text in formal Bahasa Indonesia, while SEA-HELM uses a mix of MCQ (LINDSEA), win-rate (MTBench), and instruction-following verifiers — these formats do not directly measure the citation-and-deferral behavior required when guidance is outdated or legally sensitive. |

## Flagged Gaps

1. **Pemda-level procedural content absent from benchmark**: SEA-HELM contains no Indonesian-language administrative procedure content specific to kelurahan, kabupaten, or provincial flows. Downstream search should investigate whether any existing Indonesian-language benchmark covers Dukcapil, DJP Online (including post-Coretax migration), OSS-RBA, or Imigrasi procedures.

2. **No regulatory-compliance scoring dimension**: The deployment's most critical failure mode — a plausible but outdated or legally non-compliant answer — has no analog in SEA-HELM's output taxonomy. Search should identify whether any government-chatbot or legal-QA benchmark has implemented regulation-version-aware scoring or citation-quality metrics in Indonesian.

3. **Indonesian cultural pillar gap**: SEA-HELM's SEA Culture pillar (KALAHI) covers only Filipino daily-life situations; there is no equivalent Indonesian cultural dataset in the current benchmark release. Search should determine whether an Indonesian-language cultural evaluation component is planned or exists in the SEA-HELM roadmap or in parallel efforts (e.g., IndoNLU, IndoCulture).

4. **Annotator population mismatch for accessibility KPI**: SEA-HELM annotators are predominantly Singapore-based university students; the deployment requires labels validated by low-education, non-Jakarta citizens as a primary usability measure. Search should investigate annotator demographic details available on request (per Q20), and whether any Indonesian government digital-service evaluation has used citizen-panel annotation.

5. **Informal-register comprehension evaluation**: The deployment requires the model to correctly interpret Betawi slang, Sundanese-inflected Indonesian, and casual phrasing on the input side. SEA-HELM's LINDSEA and IFEval target standard formal Indonesian; search should examine whether Indonesian colloquial or dialect-inflected comprehension benchmarks exist (e.g., from ITB, UI, or BRIN NLP groups).

6. **Outer-island and eastern Indonesia subpopulation coverage**: The user notes that guidance must not be Jakarta-centric for users in East Nusa Tenggara and similar regions. SEA-HELM does not specify sub-national Indonesian regional representation in its content. Search should identify whether benchmark datapoints were sourced from or validated by communities outside Java.

7. **Post-Coretax and recent regulatory change coverage**: DJP's transition to Coretax and ongoing Adminduk amendments mean any static benchmark risks encoding outdated procedural knowledge. Search should investigate whether SEA-HELM or companion benchmarks have a versioning or timestamp mechanism for regulatory content, and what the benchmark's data cut-off date implies for Indonesian tax and ID procedure accuracy.