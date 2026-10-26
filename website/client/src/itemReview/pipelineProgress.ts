import type { Catalog, Review, RunResult } from './api'
import type { StepNumber } from './StepSection'

export type PipelineReview = Exclude<RunResult, Review>

export function nextStepNumber(review: PipelineReview, catalog: Catalog | null): StepNumber | null {
  if (['preparing', 'running'].includes(review.status)) return null
  switch (review.mode) {
    case 'requirements':
      return review.status === 'completed' && review.requirements?.task_facets.length ? 3 : null
    case 'grounding':
      return review.status === 'completed' && review.requirements?.task_facets.length && catalog ? 4 : null
    case 'retrieval':
      return review.status === 'completed' && review.retrieval?.queues.some(queue => queue.source == null && queue.item_count > 0) ? 5 : null
    case 'screening':
      // Selection may use available valid assessments after a stopped stage.
      return review.screening ? 6 : null
    case 'selection':
      return review.status === 'completed' && review.selection
        && (review.selection_run_id == null || review.selection_run_id === review.run_id)
        && review.selection_input.errors + review.selection_input.pending === 0 ? 7 : null
    case 'adaptive':
      return null
  }
}
