import type { AdaptiveReview } from './api'
import type { ConstructionItemSummary } from './constructionTypes'

export function ItemMetadata({ summary, review, step }: {
  summary: ConstructionItemSummary; review: AdaptiveReview; step?: 5 | 6 | 7
}) {
  const taskName = (id: string) => review.requirements?.task_facets.find(facet => facet.facet_id === id)?.task.text ?? id
  const eligibility = summary.status === 'error' ? 'Assessment error' : summary.gate === 'pass' ? 'Eligible' : summary.gate === 'fail' ? 'Not eligible' : 'Eligibility unresolved'
  return <>
    <span className="construction-item-context">
      <span><b>Benchmark</b> {summary.sources.length ? summary.sources.join(', ') : 'Not recorded'}</span>
      <span><b>Matched deployment tasks</b> {summary.matched_facet_ids.length ? summary.matched_facet_ids.map(taskName).join('; ') : summary.status === 'error' ? 'No completed assessment' : 'No matched deployment task recorded'}</span>
    </span>
    <span className="construction-item-statuses">
      <span><b>Eligibility:</b> {eligibility}</span>
      {step === 6 ? <span><b>Initial collection:</b> Selected</span> : step !== 5 && <span><b>Final collection:</b> {summary.selected ? 'Selected' : 'Not selected'}</span>}
      {(step == null || step === 7) && <span><b>Screened in:</b> {summary.initial ? 'Step 5' : 'Step 7'}</span>}
      {summary.quality_score != null && step !== 5 && <span><b>Quality Q:</b> {summary.quality_score.toFixed(2)} / 5</span>}
    </span>
  </>
}
