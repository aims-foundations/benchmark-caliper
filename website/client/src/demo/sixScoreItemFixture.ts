/** Illustrative six-score judgments over the unchanged, attributed MathDial records. */
import { buildDemoItemAnalysisRun, DEMO_ITEM_ANALYSIS_ITEMS, DEMO_ITEM_ANALYSIS_SPEC, DEMO_ITEM_ANALYSIS_PILOT_SIZE } from './itemAnalysisFixture'
import { SCORE_DIMENSIONS } from '../itemAnalysis/SixScoreTable'
import rubric from './sixScoreRubric.json'
import { CLASSIFIER_NAMES } from '../itemAnalysis/Criteria'
import type { AnalysisRun, Classifier, ClassifierSummary, DimensionAssessment, Specification } from '../itemAnalysis/types'

const sharedSourceIds = new Set(['deployment_description.txt', 'elicitation_summary.md'])
export const DEMO_SIX_SCORE_SPEC: Specification = {
  analysis_type: 'six_scores', schema_version: 'caliper_item_context_v1', rubric_version: 'caliper_item_rubric_v1',
  benchmark: DEMO_ITEM_ANALYSIS_SPEC.benchmark, deployment: DEMO_ITEM_ANALYSIS_SPEC.deployment,
  deployment_description: DEMO_ITEM_ANALYSIS_SPEC.deployment, analysis_basis: 'benchmark_assessment', assessment_status: 'complete',
  dataset_profile: structuredClone(DEMO_ITEM_ANALYSIS_SPEC.dataset_profile),
  source_registry: Object.fromEntries(Object.entries(DEMO_ITEM_ANALYSIS_SPEC.source_registry || {}).filter(([id]) => sharedSourceIds.has(id))),
  source_roles: Object.fromEntries(Object.entries(DEMO_ITEM_ANALYSIS_SPEC.source_roles || {}).filter(([id]) => sharedSourceIds.has(id))),
  classifiers: rubric as Classifier[],
}
function assessment(score: number | null, justification: string, evidence: string[], information_gaps: string[] = []): DimensionAssessment {
  return { score, justification: `Illustrative judgment: ${justification}`, evidence, information_gaps }
}
export function buildSixScoreDemoRun(scope: 'pilot' | 'sample'): AnalysisRun {
  const original = buildDemoItemAnalysisRun(scope)
  const items = structuredClone(DEMO_ITEM_ANALYSIS_ITEMS).map((item, index) => {
    delete item.labels
    if (scope === 'pilot' && index >= DEMO_ITEM_ANALYSIS_PILOT_SIZE) return { ...item, status: 'pending' }
    const record = item.original_record
    return { ...item, status: 'complete', dimensions: {
      input_ontology: assessment(4, 'This mathematical-error tutoring task is relevant to the stated curriculum-agnostic teaching goal. A single dialogue does not establish benchmark-wide coverage.', [record.question, 'elicitation_summary.md']),
      input_content: assessment(null, 'The scenario is visible, but its realism for the target teachers and students has not been established by the bundled evidence.', [record.question], ['Target-teacher judgments of scenario realism.']),
      input_form: assessment(4, 'The English text dialogue aligns with the English-fluent tutoring setting, with uncertainty about the deployed interface and available conversation history.', [record.conversation.split('|EOM|')[0], 'deployment_description.txt'], ['Exact interface and conversation-history requirements.']),
      output_ontology: assessment(null, 'The supplied teacher-move tags do not establish the grading rules or how those rules capture tutor acceptability.', [record.conversation.split('|EOM|')[0]], ['Complete pedagogical grading criteria and their weighting.']),
      output_content: assessment(null, 'The mathematical reference solution alone cannot establish the pedagogical acceptability of a tutoring response.', [record.ground_truth], ['Target-teacher judgments or supported reference responses for pedagogical quality.']),
      output_form: assessment(4, 'The visible teacher responses use natural-language text suitable for the described tutoring application. Exact response-format requirements are not supplied.', [record.conversation.split('|EOM|')[0], 'deployment_description.txt'], ['Exact deployment response-format requirements.']),
    } }
  })
  const completed = items.filter(item => item.status === 'complete')
  const classifiers: ClassifierSummary[] = DEMO_SIX_SCORE_SPEC.classifiers.map(dimension => {
    const counts: Record<string, number> = Object.fromEntries([1, 2, 3, 4, 5].map(score => [String(score), 0]))
    let unknown = 0
    for (const item of completed) {
      const score = item.dimensions?.[dimension.id as keyof typeof item.dimensions]?.score
      if (score == null) unknown += 1
      else counts[String(score)] += 1
    }
    const known = completed.length - unknown
    return { ...dimension, counts, known, unknown, valid_judgments: completed.length, errors: 0, pending: 0,
      percentages_among_known: Object.fromEntries(Object.entries(counts).map(([score, count]) => [score, known ? count / known * 100 : null])) }
  })
  const summary = { ...original.summary! }
  delete summary.fixed_catalog_version
  return { ...original, analysis_type: 'six_scores', spec: structuredClone(DEMO_SIX_SCORE_SPEC), items,
    completed_judgments: completed.length * 6,
    summary: { ...summary, analysis_type: 'six_scores', schema_version: 'caliper_item_context_v1', report_schema_version: 'caliper_item_report_v3', rubric_version: 'caliper_item_rubric_v1', classifiers, dimensions: classifiers,
      experiment: { classifier_count: 6, selected_items: completed.length, completed_item_classifier_judgments: completed.length * 6, expected_item_classifier_judgments: completed.length * 6 },
      specification: { note: 'Authored illustrative scores, not model outputs or expert annotations. The original benchmark assessment remains separate.' } },
  }
}
export const DEMO_SIX_SCORE_NAMES = Object.fromEntries(SCORE_DIMENSIONS.map(id => [id, CLASSIFIER_NAMES[id]]))
