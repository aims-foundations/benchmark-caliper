import type { ReactNode } from 'react'
import type { AdaptiveReview, Catalog, Review, RunAccess, RunResult } from './api'
import { BenchmarkRetrievalContent } from './BenchmarkRetrievalResults'
import { GroundingContent } from './GroundingResults'
import { DeploymentAnswers, RequirementsContent } from './RequirementsResults'
import { initialScreeningItems, ScreeningContent, ScreeningItem } from './ScreeningResults'
import { SelectedCollection } from './SelectionResults'
import { StepSection, stepNumber } from './StepSection'

type PipelineReview = Exclude<RunResult, Review>
const STATUS = { preparing: 'In progress', running: 'In progress', completed: 'Ready for review', cancelled: 'Stopped', failed: 'Interrupted' }

function count(value: number, singular: string, plural = `${singular}s`): string {
  return `${value} ${value === 1 ? singular : plural}`
}

function InitialSelection({ review }: { review: AdaptiveReview }) {
  const initial = review.adaptive?.initial_selection
  if (initial) return <>
    <p className="help">This is the collection selected before adaptive screening. Step 7 shows the updated collection.</p>
    {initial.gaps.length > 0 && <div className="selection-notice"><strong>Coverage gaps at initial selection</strong>
      <ul>{initial.gaps.map((gap, index) => <li key={index}>{gap}</li>)}</ul></div>}
    <SelectedCollection review={{ ...review, selection: initial, selection_run_id: review.adaptive?.initial_selection_run_id ?? null }} idPrefix="initial-selection" />
  </>

  // Older runs saved initial membership in batch zero, but not its coverage
  // report. Do not relabel today's adaptive selection as the earlier result.
  const batch = review.adaptive?.batches.find(entry => entry.kind === 'initial')
  const items = new Map(review.screening?.items.map(item => [item.item_id, item]))
  const taskName = (id: string) => {
    const index = review.requirements?.task_facets.findIndex(facet => facet.facet_id === id) ?? -1
    return index >= 0 ? `Task ${index + 1}` : id
  }
  return <div className="screening-results">
    <p className="selection-notice">This older run saved the initial selected item IDs, but not a separate initial coverage report. The items below show the original membership; updated coverage is shown in Step 7.</p>
    {batch ? <>
      <p>{count(batch.selected_item_ids.length, 'item')} selected before adaptive screening.</p>
      {batch.selected_item_ids.map((id, index) => {
        const item = items.get(id)
        return item ? <ScreeningItem key={id} item={item} index={index} review={review} taskName={taskName} label="Initially selected item" idPrefix="initial-selection-item" />
          : <p key={id}>Saved initial item: <code>{id}</code>. Its assessment is unavailable.</p>
      })}
    </> : <p>No initial collection membership was saved for this run.</p>}
  </div>
}

export function PipelineResults({ review, run, catalog, children }: {
  review: PipelineReview; run: RunAccess; catalog: Catalog | null; children: ReactNode
}) {
  const current = stepNumber(review.mode)
  const initialCount = review.mode === 'adaptive'
    ? review.adaptive?.initial_selection?.selected_count ?? review.adaptive?.batches.find(batch => batch.kind === 'initial')?.selected_item_ids.length
    : undefined
  return <div className="pipeline-results">
    <p className="pipeline-order-note">Latest step first. Earlier results follow below, with your original deployment goal at the bottom.</p>
    <StepSection step={current} current status={STATUS[review.status]}>{children}</StepSection>

    {review.mode === 'adaptive' && <StepSection step={6}
      summary={initialCount == null ? 'Original selection before adaptive screening' : `${count(initialCount, 'item')} in the initial collection`}>
      <InitialSelection review={review} />
    </StepSection>}

    {current > 5 && 'screening' in review && review.screening && <StepSection step={5}
      summary={`${count(initialScreeningItems(review.screening).filter(item => item.status === 'complete').length, 'valid assessment')} from ${count(review.screening.allocation.allocated, 'initially allocated candidate')}`}>
      <ScreeningContent review={review} historical />
    </StepSection>}

    {current > 4 && 'retrieval' in review && review.retrieval && <StepSection step={4}
      summary={`${count(review.retrieval.queries.length, 'task query', 'task queries')}; ${count(review.retrieval.queues.length, 'saved candidate queue')}`}>
      <BenchmarkRetrievalContent review={review} run={run} catalog={catalog} />
    </StepSection>}

    {current > 3 && 'grounding' in review && review.grounding && <StepSection step={3}
      summary={`${count(review.grounding.facets.filter(facet => facet.status === 'complete').length, 'task mapping')} saved`}>
      <GroundingContent review={review} />
    </StepSection>}

    {current > 2 && review.requirements && <StepSection step={2}
      summary={`${count(review.requirements.task_facets.length, 'task')}; ${count(review.requirements.coverage_requirements.length, 'collection coverage requirement')}`}>
      <RequirementsContent requirements={review.requirements} />
    </StepSection>}

    <StepSection step={1} status="Original answers" summary="The six answers used to start this pipeline">
      <DeploymentAnswers deployment={review.deployment} />
    </StepSection>
  </div>
}
