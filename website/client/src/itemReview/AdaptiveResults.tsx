import { useState } from 'react'
import { getReviewExport, type AdaptiveRequest, type AdaptiveReview, type RunAccess } from './api'
import { AdaptiveForm } from './AdaptiveForm'
import { RequirementsContent } from './RequirementsResults'
import { SelectedCollection } from './SelectionResults'

const STOP_REASONS = {
  candidate_limit: 'The total candidate limit was reached.',
  queues_exhausted: 'No unseen candidates remain in the saved retrieval queues.',
  cost_limit: 'The additional screening cost ceiling was reached, or cannot cover the next reserved call.',
}

export function AdaptiveResults({ review, run, busy, onCancel, onRestart, onAdapt }: {
  review: AdaptiveReview; run: RunAccess; busy: boolean; onCancel: () => void; onRestart: () => void
  onAdapt: (apiKey: string, body: AdaptiveRequest) => Promise<boolean>
}) {
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const active = ['preparing', 'running'].includes(review.status)
  const adaptive = review.adaptive
  const selection = review.selection
  const frozen = adaptive?.frozen === true && review.status === 'completed'
  const unresolvedCount = adaptive?.batches.reduce((count, batch) => count + (batch.unresolved_item_ids?.length ?? 0), 0) ?? 0
  const taskName = (id: string | null) => {
    const index = review.requirements?.task_facets.findIndex(facet => facet.facet_id === id) ?? -1
    return index >= 0 ? `Task ${index + 1}` : id ?? 'Initial allocation'
  }

  async function download() {
    setDownloading(true)
    setDownloadError('')
    try {
      const url = URL.createObjectURL(await getReviewExport(run))
      const link = document.createElement('a')
      link.href = url
      link.download = `adaptive-benchmark-${run.run_id}.json`
      link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (error) {
      setDownloadError(error instanceof Error ? error.message : 'Could not download adaptive results. Please try again.')
    } finally { setDownloading(false) }
  }

  return <div className="selection-results screening-results adaptive-results">
    <section className="review-panel review-progress" aria-live="polite">
      <p className="eyebrow">Step 7 · Adaptive screening</p>
      <h2>{active ? 'Improving the benchmark collection' : frozen ? 'Benchmark collection frozen' : review.status === 'cancelled' ? 'Adaptive screening stopped' : 'Adaptive screening interrupted'}</h2>
      <p className="review-intro" role={review.status === 'failed' ? 'alert' : undefined}>{review.message}</p>
      <p>The collection has a shared limit of 30 items across all tasks. Screening uses up to 160 distinct candidates in total, including the initial screening.</p>
      {adaptive && <>
        <dl className="screening-totals">
          <div><dt>Assessed candidates</dt><dd>{adaptive.screened_count} / {adaptive.settings.candidate_limit}</dd></div>
          <div><dt>Selected items</dt><dd>{selection?.selected_count ?? 0} / 30</dd></div>
          <div><dt>Completed adaptive batches</dt><dd>{adaptive.batches.filter(batch => batch.kind === 'adaptive' && batch.status === 'committed').length}</dd></div>
        </dl>
        <p>{adaptive.acquired_count} distinct candidates acquired · {review.selection_input.errors} assessment errors · {review.selection_input.pending} pending assessments</p>
        {frozen && adaptive.stop_reason && <p className="selection-notice"><strong>Stopping reason:</strong> {STOP_REASONS[adaptive.stop_reason]}</p>}
        {frozen && unresolvedCount > 0 && <p className="selection-notice">The last batch included {unresolvedCount} acquired candidates without valid assessments. Its valid assessments were incorporated into selection; the remaining errors or pending items were excluded from queue outcomes and do not count as selection failures.</p>}
      </>}
      {!frozen && selection && <p className="selection-notice"><strong>Last accepted collection.</strong> The items and coverage below reflect the latest completed selection. Pending batch outcomes have not been committed. This collection is not frozen.</p>}
      {selection && !selection.fully_satisfied && <div className="selection-notice" role="status">
        <strong>Coverage remains incomplete.</strong>
        {selection.gaps.length > 0 ? <ul>{selection.gaps.map((gap, index) => <li className="review-preserve" key={index}>{gap}</li>)}</ul> : <p>Some coverage requirements remain unmet or unresolved.</p>}
        <p>Stopping does not lower the original requirements.</p>
      </div>}
      {selection && <p>Total quality Q: {selection.total_quality.toFixed(2)}. {selection.selected_count > 0 && `Average Q: ${(selection.total_quality / selection.selected_count).toFixed(2)} / 5.`} Q is the mean of the four gated dimension scores for each selected item.</p>}
      {active && <progress max={adaptive?.settings.candidate_limit ?? 160} value={adaptive?.screened_count ?? 0} aria-label="Candidates assessed across initial and adaptive screening" />}
      <div className="review-actions">
        {active ? <button type="button" className="secondary" disabled={busy} onClick={onCancel}>Stop adaptive screening</button>
          : <button type="button" className="secondary" disabled={busy} onClick={onRestart}>Start another run</button>}
        <button type="button" className="secondary" disabled={downloading} onClick={() => void download()}>{downloading ? 'Downloading…' : 'Download adaptive JSON'}</button>
      </div>
      {active && <p className="help">Stopping preserves completed assessments and the last accepted collection. Requests already sent may still incur charges.</p>}
      <p className="help">Results expire one hour after this run ends. The export includes selected items, screening evidence, coverage gaps, queue decisions, and batch history.</p>
      {downloadError && <p className="review-error" role="alert">{downloadError}</p>}
    </section>

    {adaptive && <>
      <section className="review-panel"><h2>Queue statistics</h2>
        <p>Estimated yield = (1 + successes) / (2 + successes + failures). A success is a newly screened item retained immediately after its batch. Later replacements do not rewrite earlier outcomes.</p>
        <p>Priority is estimated yield multiplied by the coverage weight. Each decision chooses the highest priority with 80% probability, or an available queue uniformly at random with 20% probability.</p>
        <div className="screening-table-scroll"><table className="screening-allocation">
          <thead><tr><th scope="col">Queue</th><th scope="col">Success / failure</th><th scope="col">Beta</th><th scope="col">Yield</th><th scope="col">Coverage weight</th><th scope="col">Priority</th><th scope="col">Remaining</th></tr></thead>
          <tbody>{adaptive.queue_statistics.map(queue => <tr key={queue.queue_id}>
            <th scope="row">{taskName(queue.facet_id)} · {queue.source ?? 'All sources'}</th>
            <td>{queue.successes} / {queue.failures}</td><td>Beta({queue.alpha}, {queue.beta})</td><td>{queue.estimated_yield.toFixed(3)}</td>
            <td>{queue.coverage_weight?.toFixed(3) ?? '—'}</td><td>{queue.priority?.toFixed(3) ?? '—'}</td><td>{queue.remaining ?? '—'}</td>
          </tr>)}</tbody>
        </table></div>
      </section>
      <section className="review-panel"><h2>Batch history</h2>
        <p>Each new batch takes up to eight unseen candidates in saved retrieval order. Queue updates are recorded only after screening and selection finish.</p>
        {adaptive.batches.map(batch => <details key={batch.number} className="adaptive-batch">
          <summary>{batch.kind === 'initial' ? 'Initial screening' : `Batch ${batch.number}`} · {batch.item_ids.length} candidates · {batch.status === 'committed' ? 'Committed' : 'Pending'}</summary>
          {batch.kind === 'adaptive' && <p>{taskName(batch.facet_id)} · {batch.source ?? 'All sources'} · {batch.exploration ? 'Random exploration' : 'Highest priority'}</p>}
          {batch.status === 'committed' ? <p>{batch.outcomes.filter(outcome => outcome.retained).length} newly screened items retained after this batch; {batch.selected_item_ids.length} items in the resulting collection.</p>
            : <p>This batch is incomplete. Its outcomes have not updated queue statistics.</p>}
          {!!batch.unresolved_item_ids?.length && <p className="selection-notice">Only this batch’s {batch.outcomes.length} valid assessments contributed selection outcomes. Its {batch.unresolved_item_ids.length} unresolved candidates are not counted as selection failures.</p>}
          <pre>{JSON.stringify(batch, null, 2)}</pre>
        </details>)}
      </section>
      <section className="review-panel"><h2>Adaptive screening cost</h2>
        {adaptive.settings.input_price_per_million == null ? <p>No additional screening cost ceiling was configured. Token usage is recorded without an assumed dollar price.</p> : <>
          <p>Estimated spent: ${adaptive.cost.spent_usd?.toFixed(4) ?? 'Unknown'} · Reserved: ${adaptive.cost.reserved_usd?.toFixed(4) ?? 'Unknown'} · Ceiling: {adaptive.settings.max_cost_usd == null ? 'Not set' : `$${adaptive.settings.max_cost_usd.toFixed(4)}`}</p>
          <p>Prices per million tokens: input ${adaptive.settings.input_price_per_million}, cached input ${adaptive.settings.cached_input_price_per_million}, output ${adaptive.settings.output_price_per_million}. These are the supplied base rates for prompts up to 272,000 input tokens.</p>
          <p className="help">Cached input means cache reads. Cache writes use 1.25× the input price for 30 minutes or 2.5× for 12 hours, replacing the ordinary input charge for those tokens. Reservations include the default 30-minute write rate.</p>
          <p className="help">Requests above 272,000 input tokens use 2× all input and cache rates and 1.5× the output rate for the whole request. Reservations use the input estimate to select this tier; returned usage determines the settled tier.</p>
          <p className="help">This covers Step 7 calls and retries only. Earlier calls are excluded. Reservations and reported usage estimate cost; they do not guarantee the final provider invoice.</p>
        </>}
        {adaptive.cost.unknown_attempts > 0 && <p className="selection-notice">Usage is unknown for {adaptive.cost.unknown_attempts} attempts. Those attempts may still incur charges.</p>}
        <details><summary>Inspect adaptive settings, policy, and call usage</summary><pre>{JSON.stringify({ policy: adaptive.policy, settings: adaptive.settings, cost: adaptive.cost, attempts: adaptive.attempts }, null, 2)}</pre></details>
      </section>
    </>}
    <SelectedCollection review={review} />
    {!active && !frozen && adaptive && <AdaptiveForm busy={busy} onAdapt={onAdapt} settings={adaptive.settings} />}
    <RequirementsContent requirements={review.requirements} deployment={review.deployment} />
  </div>
}
