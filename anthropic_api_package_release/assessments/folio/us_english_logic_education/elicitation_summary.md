## Use Case
A US educational platform is building an LLM-powered tool for American logic students that both determines the validity of logical arguments and produces step-by-step, pedagogically clear reasoning traces. The tool must serve at minimum two student registers (introductory and advanced) and handle translation from natural-language arguments into formal logical form.

## Target Population
United States, no sub-national differentiation specified. English-speaking undergraduate students enrolled in introductory and intermediate logic courses. Curriculum anchored to widely used US textbooks (e.g., Barwise & Etchemendy's *Language, Proof and Logic*), with pedagogy centered on Fitch-style natural deduction.

## Elicitation Responses

Q1 [OF]: FOLIO produces binary correctness labels (true/false/uncertain) as outputs, but your deployment requires step-by-step reasoning traces that students can follow. How detailed and structured should these explanations be, and would explanations differ between introductory and advanced students?
A1: The deployment needs numbered deduction steps that explicitly cite which premises are used at each step, paired with plain-English summaries of the logical move (e.g., "applying modus ponens to premises 2 and 4"). Introductory students get natural-language-heavy explanations with minimal notation; advanced students need quantifiers, predicates, and inference-rule names. Ideally the tool supports both registers, or a single layered explanation combining prose and formal annotations.

Q2 [OO]: Does the platform commit to a specific proof method, and must explanations follow the canonical reasoning path or can alternative valid paths be accepted?
A2: The canonical framework is Fitch-style natural deduction, matching mainstream US intro logic textbooks. Alternative valid reasoning paths are acceptable so long as every inference step is explicit and rule-justified — unexplained leaps to conclusions are not acceptable. For invalid arguments, the expected output is a countermodel or counterexample rather than a failed proof attempt.

Q3 [IO]: Which logical domains must the tool handle, and are there argument types that pure FOL exercises might not capture?
A3: The tool must handle propositional logic, predicate/FOL, and argument reconstruction from natural English. Modal logic and inductive reasoning are out of scope for this tool (fallacy identification is a planned separate module). Students regularly encounter arguments with implicit premises and multi-step chains drawn from everyday or quasi-legal scenarios, so the tool must support natural-language-to-logical-form translation, not just operate on pre-formalized premises.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | FOLIO's FOL deductive scope covers the core of the deployment's needs, but the tool must also handle propositional logic and natural-language argument reconstruction with implicit premises — categories FOLIO does not emphasize — creating a moderate coverage gap. |
| IC | MODERATE | FOLIO's examples are expert-annotated with formal FOL premises, whereas the deployment involves everyday and quasi-legal natural-language arguments with implicit premises; some FOLIO instances may be too artificial or too narrowly formalized to reflect the argument types students encounter. |
| IF | LOWER | Both FOLIO and the deployment are text-only, English-language, high-resource — no modality or script mismatch. |
| OO | HIGH | FOLIO's output space is a three-way classification label (true/false/uncertain), which is entirely misaligned with the deployment's required output: structured, rule-justified, register-differentiated proof traces and countermodels; the scoring function cannot directly evaluate explanation quality or pedagogical fidelity. |
| OC | MODERATE | FOLIO's ground-truth labels are verified by a FOL inference engine and expert annotators, making correctness labels reliable for deductive validity; however, no ground-truth exists for what constitutes a pedagogically acceptable explanation, particularly for the Fitch-style natural deduction register the curriculum requires. |
| OF | HIGH | The benchmark outputs a single label; the deployment requires multi-step natural-language and/or formally annotated proof traces differentiated by student level, plus countermodels for invalid arguments — this is a fundamental output-form mismatch that FOLIO cannot directly evaluate. |

## Flagged Gaps

1. **Explanation-quality evaluation**: FOLIO has no mechanism to assess whether a reasoning trace is pedagogically clear, correctly cites premises, or uses Fitch-style rule names. Downstream search should investigate whether any logic-reasoning benchmark includes rubrics or reference traces for step-by-step explanation quality (e.g., NaturalProofs, ProofWriter, or educational NLP benchmarks).

2. **Propositional logic coverage**: FOLIO is purely FOL-based. The deployment explicitly requires propositional logic (sentential logic) handling. Search should identify whether FOLIO or companion datasets include propositional-only problems, or whether a separate benchmark (e.g., LogiQA, bAbI, RuleTaker) better covers this layer.

3. **Natural-language-to-logical-form translation**: Students present arguments with implicit premises in natural English, and the tool must reconstruct the logical form before reasoning. FOLIO provides NL-FOL translation as a secondary task, but search should assess how well FOLIO's translation examples cover implicit-premise cases and everyday/quasi-legal argument structures versus the formal, explicit-premise style dominant in the dataset.

4. **Countermodel generation**: For invalid arguments, the deployment requires countermodels or counterexamples. FOLIO labels arguments as false/uncertain but does not require or evaluate countermodel construction. Search should identify whether any benchmark evaluates counterexample generation for FOL or propositional logic.

5. **Fitch-style natural deduction alignment**: The curriculum is specifically anchored to Fitch-style proof systems (Barwise & Etchemendy). Search should investigate whether FOLIO's FOL annotations use a compatible inference-rule vocabulary, or whether the formal structure of FOLIO proofs would need translation to match what students are taught.

6. **Register differentiation**: The deployment must produce outputs tuned to introductory versus advanced students. No existing benchmark metadata indicates FOLIO addresses multi-register explanation generation; search should check whether any logic-evaluation framework includes difficulty-stratified explanation rubrics or student-facing output standards.