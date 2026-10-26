import { useState } from 'react'
import { getReviewExport, type RunAccess, type SelectionReview, type AdaptiveRequest } from './api'
import { ScreeningForm } from './ScreeningForm'
import { ScreeningItem } from './ScreeningResults'
import { SelectionForm } from './SelectionForm'
import { AdaptiveForm } from './AdaptiveForm'

export function SelectionResults({ review, run, busy, onCancel, onRestart, onSelect, onScreen, onAdapt }: {
  review: SelectionReview; run: RunAccess; busy: boolean; onCancel: () => void; onRestart: () => void
  onSelect: () => Promise<boolean>; onScreen: (apiKey: string) => Promise<boolean>
  onAdapt: (apiKey: string, body: AdaptiveRequest) => Promise<boolean>
}) {
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const active = ['preparing', 'running'].includes(review.status)
  const selection = review.selection
  const input = review.selection_input
  const previous = !!selection && (review.status !== 'completed' || (review.selection_run_id != null && review.selection_run_id !== review.run_id))
  const remaining = input.errors + input.pending

  async function download() {
    setDownloading(true)
    setDownloadError('')
    try {
      const url = URL.createObjectURL(await getReviewExport(run))
      const link = document.createElement('a')
      link.href = url
      link.download = `benchmark-selection-${run.run_id}.json`
      link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (error) {
      setDownloadError(error instanceof Error ? error.message : 'Could not download selection results. Please try again.')
    } finally { setDownloading(false) }
  }

  return <div className="selection-results screening-results">
    <section className="review-panel review-progress" aria-live="polite">
      <h2>{active ? 'Selecting the benchmark collection' : review.status === 'cancelled' ? 'Selection stopped' : review.status === 'failed' ? 'Selection interrupted'
        : previous ? 'Previous selection retained' : selection?.fully_satisfied ? 'Your candidate collection is ready' : 'Selection has coverage gaps'}</h2>
      <p className="review-intro" role={review.status === 'failed' ? 'alert' : undefined}>{review.message}</p>
      <p>The collection has a shared limit of 30 items across all tasks. Selection runs locally without model calls.</p>
      <p>{input.screened} valid assessments · {input.errors} assessment errors · {input.pending} pending items from {input.allocated} initial allocations</p>
      {remaining > 0 && <p className="selection-notice">This selection uses the valid assessments available so far. Initial screening still has pending items or assessment errors.</p>}
      {previous && <p className="selection-notice"><strong>Previous selection retained.</strong> This run has not produced a new completed selection. The collection and coverage below belong to the earlier result.</p>}
      {selection && !selection.fully_satisfied && <div className="selection-notice" role="status">
        <strong>Coverage remains incomplete.</strong>
        {!selection.constraints_feasible && <p>The available eligible items cannot satisfy all numeric coverage requirements within the collection limit.</p>}
        {selection.gaps.length > 0 ? <ul>{selection.gaps.map((gap, index) => <li className="review-preserve" key={index}>{gap}</li>)}</ul>
          : <p>Some coverage requirements remain unmet or unresolved.</p>}
      </div>}
      {selection && <>
        <dl className="screening-totals">
          <div><dt>Selected items</dt><dd>{selection.selected_count} / {selection.limit}</dd></div>
          <div><dt>Eligible items</dt><dd>{selection.eligible_count}</dd></div>
          <div><dt>Total quality Q</dt><dd>{selection.total_quality.toFixed(2)}</dd></div>
        </dl>
        <p>Q is the mean of input ontology, input content, input form, and output ontology scores for each item.
          {selection.selected_count > 0 && ` The selected items have an average Q of ${(selection.total_quality / selection.selected_count).toFixed(2)} / 5.`}</p>
      </>}
      {active && <progress aria-label="Collection selection in progress" />}
      <div className="review-actions">
        {active ? <button type="button" className="secondary" disabled={busy} onClick={onCancel}>Stop selection</button>
          : <button type="button" className="secondary" disabled={busy} onClick={onRestart}>Start another run</button>}
        <button type="button" className="secondary" disabled={downloading} onClick={() => void download()}>{downloading ? 'Downloading…' : 'Download selection JSON'}</button>
      </div>
      <p className="help">Progress is saved so you can return later. The export includes the selected collection, coverage findings, selection settings, and the original requirements and screening evidence.</p>
      {downloadError && <p className="review-error" role="alert">{downloadError}</p>}
    </section>

    <SelectedCollection review={review} previous={previous} />
    {!active && remaining > 0 && <ScreeningForm busy={busy} onScreen={onScreen} remaining={remaining} retained={input.screened} />}
    {!active && <SelectionForm busy={busy} onSelect={onSelect} input={input} />}
    {!active && review.status === 'completed' && selection && !previous && remaining === 0 && <AdaptiveForm busy={busy} onAdapt={onAdapt} />}
  </div>
}


export function SelectedCollection({ review, previous = false, idPrefix = 'selection' }: {
  review: Pick<SelectionReview, 'run_id' | 'requirements' | 'screening' | 'selection' | 'selection_run_id'>; previous?: boolean; idPrefix?: string
}) {
  const selection = review.selection
  const screenedItems = new Map(review.screening?.items.map(item => [item.item_id, item]))
  const taskName = (id: string) => {
    const index = review.requirements?.task_facets.findIndex(facet => facet.facet_id === id) ?? -1
    return index >= 0 ? `Task ${index + 1}` : id
  }
  return <>
    {selection && <>
      <section className="review-panel" aria-labelledby={`${idPrefix}-task-coverage-title`}>
        <h2 id={`${idPrefix}-task-coverage-title`}>Task coverage</h2>
        <p>The collection needs at least one selected item for every task. Items count toward the tasks they actually test.</p>
        <div className="screening-table-scroll"><table className="screening-allocation">
          <thead><tr><th scope="col">Task</th><th scope="col">Minimum</th><th scope="col">Eligible</th><th scope="col">Selected</th><th scope="col">Shortfall</th></tr></thead>
          <tbody>{selection.task_coverage.map(coverage => <tr key={coverage.facet_id}>
            <th scope="row"><a href={`#facet-${coverage.facet_id}`}>{taskName(coverage.facet_id)}</a></th>
            <td>{coverage.minimum}</td><td>{coverage.eligible_count}</td><td>{coverage.selected_count}</td><td>{coverage.shortfall}</td>
          </tr>)}</tbody>
        </table></div>
      </section>
      <section className="review-panel" aria-labelledby={`${idPrefix}-quota-coverage-title`}>
        <h2 id={`${idPrefix}-quota-coverage-title`}>Coverage requirements in this collection</h2>
        {selection.quota_coverage.length === 0 && <p>No explicit collection coverage requirements were stated.</p>}
        {selection.quota_coverage.map(coverage => <section className="selection-coverage" key={coverage.requirement_index}>
          <h3>Coverage requirement {coverage.requirement_index + 1}</h3>
          <p className="review-preserve">{review.requirements?.coverage_requirements[coverage.requirement_index]?.requirement.text}</p>
          <p><strong>Minimum items:</strong> {coverage.minimum_items ?? 'Unresolved'} · <strong>Eligible:</strong> {coverage.eligible_count} · <strong>Selected:</strong> {coverage.selected_count} · <strong>Shortfall:</strong> {coverage.shortfall ?? 'Unresolved'}</p>
          {(coverage.minimum_items == null || selection.unresolved_requirement_indices.includes(coverage.requirement_index)) && <p className="selection-notice">This requirement remains unresolved and cannot be claimed as satisfied.</p>}
        </section>)}
      </section>
      <section aria-labelledby={`${idPrefix}-items-title`}>
        <h2 id={`${idPrefix}-items-title`}>{previous ? 'Previously selected collection' : 'Selected collection'}</h2>
        {selection.items.length === 0 && <p className="review-panel">No eligible items were selected. Review the coverage gaps and screening evidence.</p>}
        {selection.items.map((item, index) => {
          const screened = screenedItems.get(item.item_id)
          return screened ? <ScreeningItem key={item.item_id} item={screened} index={index} review={review} taskName={taskName} label="Selected item" qualityScore={item.quality_score} idPrefix={`${idPrefix}-item`} />
            : <p className="review-panel" key={item.item_id}>The preserved screening evidence for selected item {item.item_id} is unavailable.</p>
        })}
      </section>
      <section className="review-panel"><h2>Selection settings</h2>
        <details><summary>Inspect selection policy, exclusions, and solver result</summary>
          <pre>{JSON.stringify({ policy: selection.policy, excluded_counts: selection.excluded_counts, solver: selection.solver, selection_run_id: review.selection_run_id }, null, 2)}</pre>
        </details>
      </section>
    </>}
  </>
}
