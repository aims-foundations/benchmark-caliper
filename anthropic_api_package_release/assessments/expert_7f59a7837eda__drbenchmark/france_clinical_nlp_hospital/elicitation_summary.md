## Use Case
A hospital-facing clinical NLP system processes unstructured French clinical notes to perform POS tagging, NER, multi-label pathology classification, and temporal entity extraction. Outputs are mapped to standardized medical classification axes (e.g., ICD-10/PMSI) to auto-generate patient clinical profiles that help clinicians summarize medical histories and prioritize care. The system is evaluated against DrBenchmark, a French biomedical NLP benchmark built ground-up for the French biomedical domain.

## Target Population
Primary geography: Metropolitan France (hospital settings). Potential future extension to French overseas territories (highest-priority gap, given distinct tropical pathology profiles). Language: French (standard medical register). Users: hospital clinicians, physicians, and nursing staff who act on system outputs for life-critical decisions. Patient documentation is moderately clean and follows standard medical terminology, though common clinical shorthand is present.

## Elicitation Responses

Q1 [IO]: The benchmark sources clinical cases primarily from metropolitan France. Does the deployment also serve French-speaking health systems outside mainland France — Belgium, Switzerland, Quebec, or French overseas territories — where terminology, coding conventions, or disease prevalence may differ?
A1: The system is currently scoped to Metropolitan France, so off-the-shelf use elsewhere would be risky due to divergent terminology and coding standards. If adaptation were needed, French overseas territories would be the top priority, as they have distinct disease patterns (e.g., tropical pathologies) absent from mainland training data.

Q2 [OC]: The system maps pathologies to standardized classification axes. Would the benchmark's annotators — likely academic biomedical NLP researchers rather than practicing clinicians — be considered authoritative by the hospital staff acting on these outputs, especially for ambiguous or multi-morbid cases?
A2: The system is acknowledged as a "Silver Standard" clinical support tool, not an authoritative classifier. Its ICD-10 mappings may not perfectly align with specific hospital coding conventions or complex case nuances. Physicians and nurses retain final decision-making authority; the system provides a synthesized starting point for their expert adjudication.

Q3 [IC]: Clinical notes in active hospital use often contain heavy abbreviations, dictation errors, and institution-specific shorthand. Does the patient documentation resemble well-formed academic case write-ups, or raw informal clinician notes?
A3: The system performs best on relatively clean, standard-terminology documentation and has moderate resilience to common abbreviations and shorthand. Excessively noisy or institution-specific notes would require additional pre-processing (custom glossaries, normalization modules) before the system can reliably capture severity and temporal signals.

Q4 [OO]: Does the system output a single authoritative label per entity or multiple candidate classifications with confidence signals — and how does the benchmark's scoring align with this behavior?
A4: The system outputs multiple candidate labels with associated confidence scores, allowing clinicians to adjudicate between plausible classification axes. High-uncertainty entities are flagged for manual review. This multi-label-with-confidence behavior is essential for multi-morbid cases but may not be fully reflected in how DrBenchmark scores classification tasks.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | Benchmark is ground-up French biomedical and aligns well with Metropolitan France deployment, but tropical/overseas-territory pathology categories are structurally absent, creating a bounded but real gap. |
| IC | HIGH | The system processes normatively consequential clinical data (severity signals, temporal entities for care prioritization), and benchmark instances drawn from academic/published sources may not represent the moderate-noise, shorthand-laden notes present in active hospital use. |
| IF | LOWER | Both deployment and benchmark are text-only in standard French; no modality mismatch, no low-resource script issues, and infrastructure alignment is assumed within French hospital IT. |
| OO | HIGH | The deployment requires multi-label output with confidence scores and uncertainty flagging, whereas typical benchmark classification scoring uses single-label accuracy or macro-F1 — a structural mismatch that may mask performance on the clinician-adjudication behavior the system actually needs. |
| OC | HIGH | Ground-truth labels carry "Silver Standard" status and were validated by academic NLP annotators rather than practicing hospital clinicians; for ambiguous or multi-morbid mappings, label authority is explicitly questioned by the deployer, and the annotator pool is unlikely to reflect hospital coding specialists. |
| OF | MODERATE | The benchmark outputs labels and scores, which partially matches deployment needs, but the deployment additionally requires ranked candidate lists with calibrated confidence and uncertainty flags — output granularity the benchmark's evaluation protocol does not directly measure. |

## Flagged Gaps

1. **Tropical and overseas-territory pathology coverage**: DrBenchmark's clinical sources are drawn from metropolitan French institutions. Pathology categories prevalent in French overseas territories (e.g., dengue, chikungunya, malaria, sickle-cell disease at population scale) are almost certainly absent from the benchmark's ontology. Downstream web search should verify whether any DrBenchmark tasks include DOM-TOM clinical corpora or tropical medicine sources.

2. **Hospital coding specialist vs. academic annotator authority**: The deployer explicitly flags that benchmark labels may not align with hospital-specific PMSI coding conventions. Web search should investigate the annotator profiles and adjudication protocols used for DrBenchmark's classification tasks — specifically whether any labels were validated by practicing clinicians or medical coders rather than NLP researchers.

3. **Multi-label confidence calibration scoring**: DrBenchmark likely scores multi-label classification with standard metrics (e.g., micro/macro-F1) rather than evaluating confidence calibration, uncertainty flagging, or ranked-candidate quality. Web search should confirm what scoring protocol DrBenchmark uses for its classification tasks and whether any calibration or ranking metrics are reported.

4. **Noise robustness and documentation register gap**: The benchmark's clinical case sources (academic write-ups, clinical trial reports) are likely more formally written than the moderately noisy hospital notes the deployment processes. Web search should check whether any DrBenchmark tasks use raw EHR discharge summaries or dictation-sourced notes, versus edited/published clinical cases, to quantify this register mismatch.

5. **Silver Standard label propagation**: The deployer's own system rests on silver-standard annotations. Web search should clarify the annotation methodology for DrBenchmark's NER and classification tasks — whether labels were human-adjudicated by domain experts, automatically derived, or crowd-sourced — as this directly affects whether benchmark OC scores are meaningful for the deployment context.