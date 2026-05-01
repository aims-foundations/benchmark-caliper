## Use Case
A pharmaceutical document management system applies NER and semantic textual similarity (STS) models to French drug labeling and scientific abstracts, extracting fine-grained entities (chemical compounds, dosages, safety warnings) and verifying semantic consistency across regulatory documents (SmPCs, patient leaflets, patents). Outputs determine whether documentation meets EU/French regulatory standards for official submission or is flagged for manual revision.

## Target Population
Regulatory affairs specialists, pharmacologists, and legal experts at pharmaceutical companies or government health agencies operating under EU and French regulatory frameworks (EMA, ANSM). The deployment targets French-language regulatory documents, though the benchmark is English-only. End users are highly trained professionals, not general public; literacy and modality format are not concerns, but domain-specific precision is paramount.

## Elicitation Responses

Q1 [IO]: The benchmark covers biomedical NLP tasks broadly, but pharmaceutical regulatory documents (SmPCs, patient leaflets, patent claims, CTD modules) use highly formulaic, legally constrained language distinct from clinical or research prose. Are these document genres and their specialized language central to the use case?
A1: Regulatory documents are central. The formulaic language of SmPCs and leaflets is handled as a structural baseline, and regulatory-specific templates are applied for highly specialized formats like CTD modules. The underlying extraction tasks (compounds, dosages, safety warnings) are considered consistent across document types.

Q2 [IC]: The system must detect very specific regulatory entity types and phrasings — INNs, ATC codes, excipient nomenclature, posology expressions (including French-language phrasing like "2 comprimés par jour"), and EMA-template-governed contraindication language. Do these diverge significantly from standard clinical or research text?
A2: These specific entity types and phrasing patterns are precisely what the system is designed to detect, confirming close alignment between the deployment's entity ontology and the regulatory vocabulary.

Q3 [OO]: For STS-based compliance checking, regulatory equivalence differs from general semantic proximity — small lexical differences (e.g., dose thresholds, contraindicated population qualifiers) carry legal consequence under EMA/ANSM standards. Does the scoring function need to be sensitive to this, and do borderline scores trigger automatic rejection or human review?
A3: The system is explicitly designed for regulatory equivalence, treating specific discrepancies (dose thresholds, population qualifiers) as critical mismatches rather than minor semantic variation. Borderline or inconsistent scores flag the document for human review but do not trigger automatic rejection.

Q4 [OC]: Ground-truth labels in biomedical benchmarks are annotated by clinical or research professionals. Regulatory compliance judgments are governed by EMA/ANSM guidelines and legal norms, potentially producing systematic disagreements with biomedical NLP annotators on borderline cases. Is this misalignment expected?
A4: Significant overlap is expected for core technical entities, but systematic disagreements are anticipated on borderline cases, where biomedical NLP annotators are likely to prioritize clinical relevance over rigid legal constraints — a meaningful annotation-norm mismatch.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | BLURB covers general biomedical NLP tasks (clinical/research prose) and lacks document-genre categories specific to regulatory submissions (SmPCs, CTD modules, patent claims), which constitute the core input type in this deployment. |
| IC | HIGH | The deployment requires INN nomenclature, ATC codes, posology expressions, and EMA-template phrasing in French — entity types and linguistic patterns unlikely to appear in BLURB's English clinical/research corpora, creating substantial construct-irrelevant variance. |
| IF | HIGH | The deployment operates on French-language regulatory documents, but BLURB is English-only with no porting strategy; this language mismatch is a foundational external validity problem for every benchmark task. |
| OO | HIGH | BLURB's STS scoring reflects general biomedical semantic proximity, whereas the deployment requires a regulatory-equivalence decision function where small lexical differences (dose thresholds, population qualifiers) are legally determinative — a qualitatively different output ontology. |
| OC | HIGH | BLURB annotations are produced by biomedical/clinical professionals whose norms diverge from EMA/ANSM regulatory standards; the user explicitly anticipates systematic disagreements on borderline cases, directly undermining label validity for this use case. |
| OF | MODERATE | Both benchmark and deployment use text-in / label-or-text-out formats, so the representational form broadly matches; however, the deployment's human-review flagging workflow introduces a threshold-sensitivity requirement not captured by standard benchmark scoring metrics. |

## Flagged Gaps

1. **Language gap (French vs. English):** BLURB is exclusively English; the deployment targets French regulatory text. Downstream search should investigate whether any French biomedical or regulatory NLP benchmarks exist (e.g., CAS, QUAERO, or CLEF eHealth datasets) that cover French pharmaceutical language and could supplement or replace BLURB for this deployment.

2. **Regulatory document genre coverage:** BLURB does not include SmPCs, patient information leaflets, CTD module prose, or EMA-formatted patent claims. Search should investigate whether any NLP benchmark or annotated corpus specifically covers EU regulatory submission document types, including EMA or national competent authority (e.g., ANSM) document corpora.

3. **Regulatory NER entity types:** Standard biomedical NER benchmarks (including those in BLURB) typically cover genes, diseases, chemicals, and species — not INNs, ATC codes, excipient lists, or posology expressions as defined by EMA SmPC templates. Search should identify whether any labeled dataset exists for regulatory-specific NER, particularly covering EU pharmaceutical nomenclature.

4. **Regulatory STS / equivalence scoring:** No established benchmark appears to operationalize regulatory equivalence as a scoring criterion. Search should investigate whether EMA or ANSM have published annotated corpora or consistency-checking tools for safety warning equivalence, and whether any academic work has formalized regulatory STS distinct from clinical STS.

5. **Annotator population mismatch:** BLURB annotators are drawn from biomedical research communities. The deployment's ground-truth authority rests with regulatory affairs specialists and legal experts. Search should investigate whether inter-annotator agreement studies exist comparing these two annotator populations on pharmaceutical NLP tasks, and whether any regulatory-expert-annotated NER or STS dataset has been published.

6. **EMA/ANSM normative alignment:** The scoring thresholds and equivalence judgments in the deployment are governed by EMA SmPC guidelines and ANSM circulars. Search should determine whether any benchmark has been explicitly validated against these regulatory frameworks, or whether validation studies of NLP tools in EU regulatory contexts have been published in regulatory science or pharmacovigilance literature.