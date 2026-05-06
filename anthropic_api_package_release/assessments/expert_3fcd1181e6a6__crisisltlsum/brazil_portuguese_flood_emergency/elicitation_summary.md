## Use Case
An AI system that summarizes social media posts (tweets and Facebook posts in Brazilian Portuguese) during flood events to support emergency coordination. The primary users are disaster response coordinators at Defesa Civil and humanitarian NGOs who need to track evolving humanitarian and infrastructure needs across affected municipalities in Rio Grande do Sul, Brazil.

## Target Population
Geography: Rio Grande do Sul state, Brazil; sub-national focus on affected municipalities and bairros during the 2024 flood emergency. Language: Brazilian Portuguese (informal and semi-formal registers, including regional Gaúcho vocabulary and Brazilian emergency jargon). Occupation: Emergency coordinators, field coordinators, social analysts, and domain-expert analysts working in inter-operational humanitarian response teams. Note: Q4's answer referenced Ecuador and Ecuadorian Spanish, which appears to be a cross-contamination from a different deployment context; the assessment treats the primary deployment as Brazilian Portuguese / Rio Grande do Sul as stated in the deployment description.

## Elicitation Responses
Q1 [IO]: The benchmark covers four crisis types (wildfires, local fires, traffic, storms). Do flood-specific dynamics — river level progression, dam/levee failures, isolated communities, multi-municipality rescue coordination, landslides, shelter capacity, supply logistics — need to be tracked, and are there recurring sub-types Defesa Civil would expect the system to surface?
A1: Yes, definitively. The benchmark's crisis typology does not cover the flood-specific and large-scale humanitarian dynamics relevant to this use case. Coordinators focus on social and humanitarian crises affecting large populations, especially when impacts exceed local response capacity — a scale and type distinct from the benchmark's local, infrastructure-bounded US events.

Q2 [IC]: The benchmark uses US crisis tweets with US emergency terminology and geographic conventions. Would coordinators find summaries inadequate if they missed bairro- or municipality-level location references or misread Brazilian Portuguese crisis vocabulary (e.g., 'alagamento', 'ilhado', 'Defesa Civil')?
A2: Yes. Coordinators would expect the system to anchor events to Rio Grande do Sul–specific geographic entities (municipalities, bairros, rivers such as Jacuí and Guaíba) and local emergency terminology. Summaries that fail to resolve these local references would be operationally inadequate.

Q3 [OC]: Who should judge whether a summary is correct or useful — Defesa Civil coordinators, NGO staff, affected residents — and would these groups disagree on information priorities (rescue needs vs. supply shortages vs. road access)?
A3: Judgment would fall to an inter-operational team combining multiple roles: field coordinators, social analysts, and domain-expert analysts — not a single stakeholder type. This multi-perspective judgment panel reflects the reality that different operational priorities (rescue, logistics, shelter, road access) must all be represented in ground-truth evaluation.

Q4 [OF]: Do coordinators need summaries structured by geographic unit, timeline-ordered per event, or a structured format (e.g., situation report, prioritized action list) that plugs into existing coordination tools — or is a free-flowing paragraph usable?
A4: The answer indicated that the operational language environment would involve informal and semi-formal registers and that a system trained only on English social media (and possibly fine-tuned on local Spanish) would miss local characteristics of the target social media data. This confirms that output form must accommodate the register and linguistic specificity of the source data; the benchmark's English-only, US-crisis abstractive summaries would not transfer cleanly to the operational workflow.

## Dimension Priority Weights
| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark's four crisis types (wildfires, local fires, traffic, storms) entirely omit large-scale flood dynamics, humanitarian coordination across municipalities, and the social-crisis framing that Defesa Civil coordinators explicitly require. |
| IC | HIGH | Benchmark instances are US English tweets with US geographic and emergency conventions; deployment data is Brazilian Portuguese social media with local place names, Gaúcho register, and Brazilian emergency jargon that the benchmark's content does not represent. |
| IF | MODERATE | Both deployment and benchmark are text-only; however, the deployment mixes Twitter and Facebook posts (differing platform conventions and post structures) while the benchmark is Twitter-only, creating a partial input-form mismatch. |
| OO | HIGH | The benchmark's output taxonomy (timeline extraction + abstractive summary) was designed around bounded local US events; the deployment requires surfacing large-scale humanitarian needs (rescue, shelter, supply, road access) across multiple municipalities, a structurally different output ontology. |
| OC | HIGH | Ground-truth summaries were written by English-speaking US-crisis annotators; the deployment requires inter-operational judgment by multi-role Brazilian emergency professionals, making annotator-population mismatch severe and systematic. |
| OF | HIGH | The benchmark produces free-form abstractive paragraph summaries of single events; coordinators need geographically anchored, multi-municipality tracking outputs, potentially in structured situation-report formats, representing a significant output-form mismatch for operational integration. |

## Flagged Gaps
1. **Flood-specific crisis ontology**: No evidence that CrisisLTLSum covers large-scale flood events, dam/levee failure dynamics, river-level progression, or multi-municipality humanitarian coordination. Downstream search should investigate whether any crisis NLP benchmarks cover Brazilian floods or comparable large-scale South American disaster events.

2. **Brazilian Portuguese social media language**: The benchmark is English-only with no porting strategy. Downstream search should investigate coverage of Brazilian Portuguese in crisis NLP datasets, including handling of informal Gaúcho vocabulary, mixed registers, and Brazilian emergency jargon ('alagamento', 'enchente', 'ilhado', 'Defesa Civil', 'resgate').

3. **Rio Grande do Sul geographic entity resolution**: Coordinators require municipality- and bairro-level geographic anchoring. Search should investigate whether any NER or geo-parsing resources exist for Rio Grande do Sul place names (municipalities, bairros, rivers like Jacuí and Guaíba) in the crisis NLP literature.

4. **Facebook post structure vs. Twitter**: The deployment ingests Facebook posts alongside tweets; the benchmark is Twitter-only. Search should investigate whether platform-specific post structure (length, threading, shared content) affects summarization quality in crisis contexts.

5. **Inter-operational judgment standards**: Ground truth requires multi-role annotator panels (field coordinators, social analysts, domain experts). Search should investigate whether any crisis summarization benchmarks have used inter-operational or multi-stakeholder annotation protocols, especially in non-English or Global South contexts.

6. **Output format for operational integration**: The benchmark's abstractive paragraph format may not match the structured situation-report or municipality-segmented formats used by Defesa Civil. Search should investigate what output structures Brazilian or Latin American civil defense agencies use in practice and whether any summarization benchmarks target those formats.

7. **Cross-contamination note — Ecuador reference in Q4**: The user's Q4 answer referenced Ecuador and Ecuadorian Spanish, suggesting possible confusion with a parallel deployment assessment. If the actual deployment scope includes Ecuador or other Latin American countries, this would introduce additional sub-national and linguistic gaps (indigenous language entity names, Andean regional jargon) that should be investigated separately.