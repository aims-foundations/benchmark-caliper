## Use Case
An automated logic-checking tool for US undergraduate introductory logic courses that classifies natural-language arguments as valid, invalid, or indeterminate based on deductive entailment. The system must handle both propositional connectives and first-order predicate logic (quantifiers, basic predicate structure), strictly within classical logic.

## Target Population
US university undergraduates enrolled in introductory formal reasoning courses; English-speaking, no specialized logic background assumed. Problems are drawn from a custom course packet styled after Hurley's *Concise Introduction to Logic*, featuring constrained syntactic templates alongside some natural-language paraphrases. No sub-national or demographic variation is a primary concern; the population is functionally uniform in language and educational context.

## Elicitation Responses

Q1 [IO]: FOLIO covers first-order logic deductive reasoning broadly, but introductory undergraduate logic courses vary in scope. Does your course focus primarily on propositional logic, predicate/first-order logic, or a mix? Are modal logic, temporal reasoning, or probabilistic arguments in scope, or strictly classical deductive logic?
A1: The course covers both propositional and predicate/first-order logic (with FOL as the second-half focus), strictly within classical deductive logic. Quantifiers, connectives, and basic predicate structure are all in scope; modal, temporal, and probabilistic reasoning are not.

Q2 [OO]: Your tool outputs one of three labels — valid, invalid, or indeterminate. Does your course treat 'indeterminate' as a single category, or does it distinguish between e.g. undecidable formulas vs. conclusions not entailed but not contradicted either?
A2: 'Indeterminate' means the premises are consistent with both the conclusion and its negation — neither entailment nor contradiction. Undecidable formulas are not in scope. The rubric treats valid, invalid (premises entail the negation of the conclusion), and indeterminate as three fully distinct, non-collapsed categories.

Q3 [IC]: Are students' problems drawn from a specific textbook or problem set with a constrained syntactic style that might differ from FOLIO's sentence patterns?
A3: Problems come from a custom course packet modeled on Hurley's style, featuring heavily templated sentence forms (e.g., "All A are B," "If P then Q," "Some A is not B"). Natural-language paraphrases are introduced later in the term but remain a secondary register; the dominant style is syntactically controlled and pedagogically stylized.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | FOLIO's FOL scope aligns well with the course's second-half focus, but the benchmark may underrepresent purely propositional problems that constitute the course's first half, creating a coverage gap for that sub-domain. |
| IC | HIGH | The deployment uses highly constrained, template-driven sentence patterns (Hurley-style) while FOLIO uses expert-authored naturalistic text; surface-form mismatch may introduce construct-irrelevant difficulty or inflate/deflate apparent model capability on course-representative inputs. |
| IF | LOWER | Both benchmark and deployment are text-only, English, standard Latin script — no modality or infrastructure mismatch. |
| OO | HIGH | FOLIO's native output space is true/false/unknown and may not map cleanly onto the deployment's three-way valid/invalid/indeterminate scheme, especially since 'invalid' in the course requires premises to *entail the negation* (not merely fail to entail the conclusion), a stricter and distinct condition from FOLIO's 'false' label. |
| OC | MODERATE | FOLIO is expert-annotated with FOL-engine verification, which strengthens label reliability for clear cases, but the three-way label mapping (see OO) means some ground-truth labels may be systematically misaligned with the course rubric's definitions, even if individually correct under FOLIO's own scheme. |
| OF | LOWER | Both benchmark and deployment produce a categorical label from a small fixed set; the output form is well-matched. |

## Flagged Gaps

1. **Valid/Invalid/Indeterminate label mapping**: FOLIO's label ontology (true/false/unknown) does not straightforwardly correspond to the course's three-way scheme. Specifically, the course's "invalid" requires that the premises *entail the negation of the conclusion*, whereas FOLIO's "false" label may simply mean the conclusion does not follow. Downstream search should investigate FOLIO's exact annotation protocol for the "false" category to determine whether this distinction is preserved in the ground truth.

2. **Propositional logic coverage**: FOLIO is built around FOL and may have sparse or no coverage of purely propositional arguments (no quantifiers). Because the course's first half is propositional, the benchmark may systematically undertest a significant portion of what the tool must handle. Search should verify the proportion of FOLIO examples that are quantifier-free or propositional-only.

3. **Templated/pedagogical sentence style**: The deployment's dominant input register is Hurley-style templates ("All A are B," "Some A is not B," "If P then Q"), which are syntactically more constrained and formulaic than FOLIO's annotator-authored prose. It is unclear whether FOLIO contains a sufficient proportion of examples in this register to be predictive of model performance on course-packet inputs. Search should investigate whether FOLIO or any related FOL benchmark explicitly samples from formal-logic textbook problem styles.

4. **Indeterminate/unknown example frequency**: The benchmark should be checked for the base rate of "unknown/indeterminate" examples — if this category is rare in FOLIO relative to the course's problem distribution, accuracy metrics will be dominated by the valid/invalid split and may not reliably predict model performance on the indeterminate cases the rubric explicitly tests.

5. **Negation-as-failure vs. explicit contradiction**: Because the course strictly defines "invalid" as entailment of the negation (not merely absence of entailment), search should investigate whether FOLIO's construction methodology verifies the "false" label via an FOL prover that confirms entailment of the negation, or merely the absence of entailment of the conclusion.