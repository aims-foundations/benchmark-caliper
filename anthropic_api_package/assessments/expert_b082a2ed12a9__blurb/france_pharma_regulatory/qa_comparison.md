# Q&A Comparison: Original (DrBenchmark) vs Cleaned (for BLURB)

Tuple: `france_pharma_regulatory`

---

## Q1 [IO]

**Original:**
The benchmark covers **biomedical NER and STS tasks drawn from sources like scientific literature and clinical cases**, but pharmaceutical regulatory documents have distinctive text types — Summary of Product Characteristics (SmPCs), patient information leaflets, patent claims, and Common Technical Document (CTD) modules. Are these document genres central to your use case, and does the system need to handle the highly formulaic, legally constrained language specific to EU regulatory submissions rather than clinical or research prose?

**Cleaned:**
**The benchmark under assessment covers a set of biomedical NLP tasks**, but pharmaceutical regulatory documents have distinctive text types — Summary of Product Characteristics (SmPCs), patient information leaflets, patent claims, and Common Technical Document (CTD) modules. Are these document genres central to your use case, and does the system need to handle the highly formulaic, legally constrained language specific to EU regulatory submissions rather than clinical or research prose?

**Delta:** Replaced `"covers biomedical NER and STS tasks drawn from sources like scientific literature and clinical cases"` with `"covers a set of biomedical NLP tasks"` — removed DrBenchmark-specific task types (NER, STS) and data sources (scientific literature, clinical cases). BLURB has different task composition.

**A1 (verbatim):**
The pharmaceutical regulatory documents are central to this use case. While SmPCs and leaflets use more formulaic language than research prose, the underlying task of extracting chemical compounds, dosages, and safety warnings remains consistent. The system handles this structured language as a foundational engine. For highly specialized formats like CTD modules, we can apply regulatory-specific templates to ensure the model meets the strict professional standards required for official submissions.

---

## Q2 [IC]

**Original:**
For your NER use case, regulatory drug labeling uses a very specific vocabulary: INN (International Nonproprietary Names), ATC codes, excipient nomenclature, posology expressions (e.g., '2 comprimés par jour chez l'adulte'), and contraindication phrasing governed by EMA templates. Are these entity types and phrasings representative of what the system must detect, or does your labeling work involve entity categories or expression patterns that diverge significantly from standard clinical or research text?

**Cleaned:**
For your NER use case, regulatory drug labeling uses a very specific vocabulary: INN (International Nonproprietary Names), ATC codes, excipient nomenclature, posology expressions (e.g., '2 comprimés par jour chez l'adulte'), and contraindication phrasing governed by EMA templates. Are these entity types and phrasings representative of what the system must detect, or does your labeling work involve entity categories or expression patterns that diverge significantly from standard clinical or research text?

**Delta:** No change (question was already deployment-focused — NER, entity types, and regulatory vocabulary are all deployment-side specifics, not benchmark properties).

**A2 (verbatim):**
Yes, these specific entities and phrasings are exactly what the system is designed to detect.

---

## Q3 [OO]

**Original:**
For semantic textual similarity in your compliance workflow, two safety warnings might be judged 'equivalent' by a general **biomedical STS scorer** yet still be non-equivalent under EMA or ANSM regulatory standards — for example, differing only in a dose threshold or a contraindicated population qualifier. Does your system need a scoring function sensitive to regulatory equivalence (where small lexical differences have legal consequence), rather than general semantic proximity, and would a borderline score trigger automatic rejection or only flag for human review?

**Cleaned:**
For semantic textual similarity in your compliance workflow, two safety warnings might be judged 'equivalent' by a general **biomedical STS scorer** yet still be non-equivalent under EMA or ANSM regulatory standards — for example, differing only in a dose threshold or a contraindicated population qualifier. Does your system need a scoring function sensitive to regulatory equivalence (where small lexical differences have legal consequence), rather than general semantic proximity, and would a borderline score trigger automatic rejection or only flag for human review?

**Delta:** No change. "Biomedical STS scorer" here is used as a generic contrast point (general-purpose vs regulatory-specific scoring), not as an assertion about the benchmark's specific tasks.

**A3 (verbatim):**
The system is specifically designed for regulatory equivalence, recognizing that minor lexical changes, like dose thresholds, carry significant legal weight. While general semantic proximity is a baseline, the scoring function treats these specific discrepancies as critical mismatches. Borderline scores or inconsistencies in these high-stakes areas will flag the document for human review but not automatically reject them.

---

## Q4 [OC]

**Original:**
Ground-truth labels in **biomedical benchmarks** are typically annotated by clinical or research professionals. For your regulatory compliance context, the authoritative judgment on whether a named entity is correctly identified or two statements are semantically equivalent may rest with regulatory affairs specialists or legal experts rather than clinicians. Are the annotation norms your team relies on — e.g., EMA SmPC guidelines, ANSM circulars — likely to align with labels produced by **biomedical NLP annotators**, or do you foresee systematic disagreements on borderline cases?

**Cleaned:**
Ground-truth labels in **biomedical benchmarks** are typically annotated by clinical or research professionals. For your regulatory compliance context, the authoritative judgment on whether a named entity is correctly identified or two statements are semantically equivalent may rest with regulatory affairs specialists or legal experts rather than clinicians. Are the annotation norms your team relies on — e.g., EMA SmPC guidelines, ANSM circulars — likely to align with labels produced by **biomedical NLP annotators**, or do you foresee systematic disagreements on borderline cases?

**Delta:** No change. "Biomedical benchmarks" and "biomedical NLP annotators" are used generically — they describe a class of benchmarks, not DrBenchmark specifically. The deployment-side regulatory framing is the core of the question.

**A4 (verbatim):**
A significant overlap is expected for core technical entities, but systematic disagreements are likely on borderline cases. Biomedical NLP annotators might prioritize clinical relevance over the rigid legal constraints.
