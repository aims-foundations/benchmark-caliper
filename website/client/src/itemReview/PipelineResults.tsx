import type { AdaptiveRequest, AdaptiveReview, Catalog, RunAccess } from './api'
import { BenchmarkRetrievalContent, BenchmarkRetrievalResults } from './BenchmarkRetrievalResults'
import { GroundingContent, GroundingResults } from './GroundingResults'
import { DeploymentAnswers, RequirementsContent, RequirementsResults } from './RequirementsResults'
import { initialScreeningItems, ScreeningContent, ScreeningItem, ScreeningResults } from './ScreeningResults'
import { SelectedCollection, SelectionResults } from './SelectionResults'
import { AdaptiveResults } from './AdaptiveResults'
import { GroundingForm } from './GroundingForm'
import { BenchmarkRetrievalForm } from './BenchmarkRetrievalForm'
import { ScreeningForm } from './ScreeningForm'
import { SelectionForm } from './SelectionForm'
import { AdaptiveForm } from './AdaptiveForm'
import { ResultPackage } from './ResultPackage'
import { StepSection, stepNumber } from './StepSection'
import { nextStepNumber, type PipelineReview } from './pipelineProgress'

const STATUS = { preparing: 'In progress', running: 'In progress', completed: 'Ready for review', cancelled: 'Stopped', failed: 'Interrupted' }

interface PipelineActions {
  busy: boolean
  onCancel: () => void
  onRestart: () => void
  onGround: (apiKey: string) => Promise<boolean>
  onRetrieve: () => Promise<boolean>
  onScreen: (apiKey: string) => Promise<boolean>
  onSelect: () => Promise<boolean>
  onAdapt: (apiKey: string, body: AdaptiveRequest) => Promise<boolean>
}

interface PipelineProps {
  review: PipelineReview; run: RunAccess; catalog: Catalog | null; actions: PipelineActions
}

function CurrentResults({ review, run, catalog, actions }: PipelineProps) {
  const shared = { run, busy: actions.busy, onCancel: actions.onCancel, onRestart: actions.onRestart }
  switch (review.mode) {
    case 'requirements': return <RequirementsResults review={review} {...shared} />
    case 'grounding': return <GroundingResults review={review} {...shared} onGround={actions.onGround} />
    case 'retrieval': return <BenchmarkRetrievalResults review={review} {...shared} catalog={catalog} onRetrieve={actions.onRetrieve} />
    case 'screening': return <ScreeningResults review={review} {...shared} onScreen={actions.onScreen} />
    case 'selection': return <SelectionResults review={review} {...shared} onSelect={actions.onSelect} />
    case 'adaptive': return <AdaptiveResults review={review} {...shared} onAdapt={actions.onAdapt} />
  }
}

function NextStepForm({ review, catalog, actions }: Omit<PipelineProps, 'run'>) {
  const { busy } = actions
  switch (review.mode) {
    case 'requirements': return <GroundingForm busy={busy} onGround={actions.onGround} />
    case 'grounding': return catalog && <BenchmarkRetrievalForm busy={busy} catalog={catalog} onRetrieve={actions.onRetrieve} />
    case 'retrieval': return <ScreeningForm busy={busy} onScreen={actions.onScreen} />
    case 'screening': {
      const items = initialScreeningItems(review.screening)
      return <SelectionForm busy={busy} onSelect={actions.onSelect} input={{
        allocated: review.screening?.allocation.allocated ?? 0,
        screened: items.filter(item => item.status === 'complete').length,
        errors: items.filter(item => item.status === 'error').length,
        pending: Math.max(0, (review.screening?.allocation.allocated ?? 0) - items.length),
      }} />
    }
    case 'selection': return <AdaptiveForm busy={busy} onAdapt={actions.onAdapt} />
    case 'adaptive': return null
  }
}

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

export function PipelineResults({ review, run, catalog, actions }: PipelineProps) {
  const current = stepNumber(review.mode)
  const next = nextStepNumber(review, catalog)
  const screeningRemaining = review.mode === 'selection' && !['preparing', 'running'].includes(review.status)
    ? review.selection_input.errors + review.selection_input.pending : 0
  const initialCount = review.mode === 'adaptive'
    ? review.adaptive?.initial_selection?.selected_count ?? review.adaptive?.batches.find(batch => batch.kind === 'initial')?.selected_item_ids.length
    : undefined
  return <div className="pipeline-results">
    <p className="pipeline-order-note">{next ? 'Start the next step above your saved results.' : 'The latest step is shown first.'} Each step keeps its results and controls together, with your original deployment goal at the bottom.</p>
    {next && <StepSection step={next} ready status={next === 4 && (!catalog?.dataset_access_configured || !catalog.table_count) ? 'Setup required' : 'Ready to start'}>
      <NextStepForm review={review} catalog={catalog} actions={actions} />
    </StepSection>}
    <StepSection step={current} current status={STATUS[review.status]}>
      <CurrentResults review={review} run={run} catalog={catalog} actions={actions} />
      <ResultPackage review={review} run={run} />
    </StepSection>

    {review.mode === 'adaptive' && <StepSection step={6}
      summary={initialCount == null ? 'Original selection before adaptive screening' : `${count(initialCount, 'item')} in the initial collection`}>
      <InitialSelection review={review} />
    </StepSection>}

    {current > 5 && 'screening' in review && review.screening && <StepSection step={5}
      summary={`${count(initialScreeningItems(review.screening).filter(item => item.status === 'complete').length, 'valid assessment')} from ${count(review.screening.allocation.allocated, 'initially allocated candidate')}`}>
      <ScreeningContent review={review} historical />
      {screeningRemaining > 0 && review.mode === 'selection' && <ScreeningForm busy={actions.busy} onScreen={actions.onScreen}
        remaining={screeningRemaining} retained={review.selection_input.screened} />}
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
