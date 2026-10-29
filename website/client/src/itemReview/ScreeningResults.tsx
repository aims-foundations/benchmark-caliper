import { useState } from 'react'
import { DIMENSIONS, getReviewExport, type ScreenedItem, type ScreeningReview, type RunAccess } from './api'
import { ScreeningForm } from './ScreeningForm'
import { ItemDetails } from './ItemDetails'

function EvidenceNotes({ evidence, justification, information_gaps }: { evidence: string[]; justification: string; information_gaps: string[] }) {
  return <>
    <p className="review-preserve">{justification}</p>
    {evidence.length > 0 && <div><h5>Supporting item evidence</h5>{evidence.map((quote, index) => <blockquote className="review-preserve" key={index}>{quote}</blockquote>)}</div>}
    {information_gaps.length > 0 && <div><h5>Information gaps</h5><ul>{information_gaps.map((gap, index) => <li className="review-preserve" key={index}>{gap}</li>)}</ul></div>}
  </>
}

export function ScreeningItem({ item, index, review, taskName, label = 'Screened item', qualityScore, idPrefix = 'screened' }: {
  item: ScreenedItem; index: number; review: Pick<ScreeningReview, 'run_id' | 'requirements' | 'screening'>; taskName: (facetId: string) => string
  label?: string; qualityScore?: number; idPrefix?: string
}) {
  const assessment = item.assessment
  const gateLabel = item.gate?.status === 'pass' ? 'Pass' : item.gate?.status === 'fail' ? 'Fail' : 'Unresolved'
  return <article className="review-panel screening-item" aria-labelledby={`${idPrefix}-${item.item_id}`}>
    <div className="review-result-title"><h3 id={`${idPrefix}-${item.item_id}`}>{label} {index + 1}</h3>
      <span className={`review-confidence screening-${item.status === 'error' ? 'error' : item.gate?.status ?? 'unresolved'}`}>
        {item.status === 'error' ? 'Assessment error' : `Screening gate: ${gateLabel}`}
      </span></div>
    {qualityScore != null && <p className="selection-quality"><strong>Quality Q: {qualityScore.toFixed(2)} / 5</strong></p>}
    <p className="help"><strong>Acquired from:</strong> {taskName(item.acquisition.facet_id)} queue · <strong>Sources:</strong> {[...new Set(item.sources.map(source => source.benchmark))].join(', ')}</p>
    {item.screened_run_id && item.screened_run_id !== review.run_id && <p className="help">Retained assessment from an earlier screening run.</p>}
    <ItemDetails question={item.question_text}>
      {item.status === 'error' ? <div className="review-error" role="alert"><p className="review-preserve">{item.error || 'No valid assessment was returned for this item.'}</p><p>This is an assessment error; the item has no screening gate decision.</p></div>
        : assessment && <>
          <h4>Task actually tested</h4>
          <p className="review-preserve">{assessment.task.decision ?? 'The tested decision is unresolved.'}</p>
          <p><strong>Task match:</strong> {assessment.task.status === 'matched' ? 'Matched' : assessment.task.status === 'no_match' ? 'No deployment task matched' : 'Unresolved'}</p>
          {assessment.task.matched_facet_ids.length > 0 && <p><strong>Matched deployment tasks: </strong>{assessment.task.matched_facet_ids.map((id, taskIndex) => <span key={id}>
            {taskIndex > 0 && ', '}<a href={`#facet-${id}`}>{taskName(id)}</a>
          </span>)}</p>}
          {item.gate && <section><h4>Screening gate: {gateLabel}</h4><ul>{item.gate.reasons.map((reason, reasonIndex) => <li className="review-preserve" key={reasonIndex}>{reason}</li>)}</ul></section>}
          <dl className="screening-ratings">{DIMENSIONS.map(([key, label]) => <div key={key}>
            <dt>{label}<small>{review.screening?.policy.gated_dimensions.includes(key) ? 'Gate dimension' : 'Reported dimension'}</small></dt>
            <dd>{assessment.ratings[key].score == null ? 'Unknown' : `${assessment.ratings[key].score} / 5`}</dd>
          </div>)}</dl>
          <details><summary>Inspect task interpretation and six validity ratings</summary>
            <section className="screening-explanation"><h4>Task interpretation</h4><EvidenceNotes {...assessment.task} /></section>
            {DIMENSIONS.map(([key, label]) => <section className="screening-explanation" key={key}>
              <h4>{label}: {assessment.ratings[key].score == null ? 'Unknown' : `${assessment.ratings[key].score} / 5`}</h4>
              <EvidenceNotes {...assessment.ratings[key]} />
            </section>)}
          </details>
          <details><summary>Inspect coverage requirements ({assessment.coverage.length})</summary>
            {assessment.coverage.length === 0 && <p>No explicit coverage requirements were assessed for this item.</p>}
            {assessment.coverage.map(coverage => <section className="screening-explanation" key={coverage.requirement_index}>
              <h4>Coverage requirement {coverage.requirement_index + 1}: {coverage.satisfied == null ? 'Unresolved' : coverage.satisfied ? 'Satisfied' : 'Not satisfied'}</h4>
              <p className="review-preserve">{review.requirements?.coverage_requirements[coverage.requirement_index]?.requirement.text}</p>
              <EvidenceNotes {...coverage} />
            </section>)}
          </details>
        </>}
      <details><summary>Inspect original row and sources</summary>
        <p className="help">Item ID: <code>{item.item_id}</code> · Evidence hash: <code>{item.evidence_hash}</code></p>
        <h4>Original item evidence</h4><pre>{JSON.stringify(item.evidence, null, 2)}</pre>
        {item.evidence_adjustments && item.evidence_adjustments.length > 0 && <>
          <h4>Evidence quotation formatting</h4>
          <p>Only leading or trailing whitespace was removed from these returned quotations. Each resulting quotation matches the original item exactly. Internal spacing, punctuation, and wording were preserved.</p>
          {item.evidence_adjustments.map((adjustment, adjustmentIndex) => <div key={adjustmentIndex}>
            <p><strong>Assessment field:</strong> <code>{adjustment.field}</code></p>
            <p>Returned quotation</p><pre>{JSON.stringify(adjustment.returned_quote)}</pre>
            <p>Verified source quotation</p><pre>{JSON.stringify(adjustment.source_quote)}</pre>
          </div>)}
        </>}
        <h4>Full row text used for retrieval</h4><pre>{item.search_text}</pre>
        <h4>Source provenance</h4><pre>{JSON.stringify(item.sources, null, 2)}</pre>
        <h4>Acquisition details</h4><pre>{JSON.stringify({ ...item.acquisition, retrieval_rank: item.rank, screened_run_id: item.screened_run_id, usage: item.usage }, null, 2)}</pre>
      </details>
    </ItemDetails>
  </article>
}

export function ScreeningResults({ review, run, busy, onCancel, onRestart, onScreen }: {
  review: ScreeningReview; run: RunAccess; busy: boolean; onCancel: () => void; onRestart: () => void; onScreen: (apiKey: string) => Promise<boolean>
}) {
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const active = ['preparing', 'running'].includes(review.status)
  const screening = review.screening
  const allocation = screening?.allocation
  const items = initialScreeningItems(screening)
  const complete = items.filter(item => item.status === 'complete').length
  const errors = items.filter(item => item.status === 'error').length
  const remaining = Math.max(0, (allocation?.allocated ?? 0) - complete)
  const completedTitle = remaining > 0 ? 'Initial screening needs attention' : 'Your initial screening is ready'
  async function download() {
    setDownloading(true)
    setDownloadError('')
    try {
      const url = URL.createObjectURL(await getReviewExport(run))
      const link = document.createElement('a')
      link.href = url
      link.download = `initial-screening-${run.run_id}.json`
      link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (error) {
      setDownloadError(error instanceof Error ? error.message : 'Could not download screening results. Please try again.')
    } finally { setDownloading(false) }
  }

  return <div className="screening-results">
    <section className="review-panel review-progress" aria-live="polite">
      <h2>{active ? 'Screening initial candidates' : review.status === 'completed' ? completedTitle : review.status === 'cancelled' ? 'Screening stopped' : 'Screening interrupted'}</h2>
      <p className="review-intro" role={review.status === 'failed' ? 'alert' : undefined}>{review.message}</p>
      <p>{items.length} of {allocation?.allocated ?? 0} allocated items processed · {complete} valid assessments · {errors} assessment errors</p>
      {active && <progress max={allocation?.allocated || 1} value={items.length} aria-label="Initial items processed" />}
      <dl className="screening-totals">{(['pass', 'fail', 'unresolved'] as const).map(status => <div key={status}>
        <dt>{status === 'pass' ? 'Passed gate' : status === 'fail' ? 'Failed gate' : 'Unresolved gate'}</dt>
        <dd>{items.filter(item => item.status === 'complete' && item.gate?.status === status).length}</dd>
      </div>)}</dl>
      <p>Passing requires a matched deployment task and scores of at least {screening?.policy.minimum_score ?? 3} for input ontology, input content, input form, and output ontology. All six dimensions are reported. Coverage findings are recorded separately.</p>
      <p>The screening results support later benchmark selection. No final benchmark has been selected.</p>
      <div className="review-actions">
        {active ? <button type="button" className="secondary" disabled={busy} onClick={onCancel}>Stop screening</button>
          : <button type="button" className="secondary" disabled={busy} onClick={onRestart}>Start another run</button>}
        <button type="button" className="secondary" disabled={downloading} onClick={() => void download()}>{downloading ? 'Downloading…' : 'Download screening JSON'}</button>
      </div>
      {active && <p className="help">Stopping retains completed assessments. A request already sent may still incur charges.</p>}
      <p className="help">Progress is saved so you can return later. The export retains original answers, requirements, grounding, retrieval, allocation, assessments, and screening settings.</p>
      {downloadError && <p className="review-error" role="alert">{downloadError}</p>}
    </section>
    {!active && remaining > 0 && <ScreeningForm busy={busy} onScreen={onScreen} remaining={remaining} retained={complete} />}
    <ScreeningContent review={review} />
  </div>
}


export function initialScreeningItems(screening: ScreeningReview['screening']): ScreenedItem[] {
  const items = new Map(screening?.items.map(item => [item.item_id, item]))
  return (screening?.allocation.items ?? []).flatMap(({ item_id }) => {
    const item = items.get(item_id)
    return item ? [item] : []
  })
}

export function ScreeningContent({ review, historical = false }: {
  review: Pick<ScreeningReview, 'run_id' | 'requirements' | 'screening' | 'usage'>; historical?: boolean
}) {
  const screening = review.screening
  const allocation = screening?.allocation
  const items = initialScreeningItems(screening)
  const taskName = (id: string) => {
    const index = review.requirements?.task_facets.findIndex(facet => facet.facet_id === id) ?? -1
    return index >= 0 ? `Task ${index + 1}` : id
  }
  return <div className="screening-results">
    {allocation && <section className="review-panel" aria-labelledby="screening-allocation-title">
      <h2 id="screening-allocation-title">Initial screening allocation</h2>
      <p>Budget: {allocation.budget} distinct items · Allocated: {allocation.allocated} · Shortfall: {allocation.shortfall}</p>
      <p>Places are distributed as evenly as the available task queues allow, with overlapping items counted once.</p>
      {allocation.shortfall > 0 && <p>There are {allocation.shortfall} fewer distinct candidates than the initial budget allows.</p>}
      <div className="screening-table-scroll"><table className="screening-allocation"><thead><tr><th scope="col">Task queue</th><th scope="col">Target</th><th scope="col">Allocated</th></tr></thead>
        <tbody>{allocation.allocations.map(queue => <tr key={queue.queue_id}>
          <th scope="row"><a href={`#facet-${queue.facet_id}`}>{taskName(queue.facet_id)}</a></th><td>{queue.target}</td><td>{queue.allocated}</td>
        </tr>)}</tbody></table></div>
    </section>}
    {items.length > 0 && <section aria-labelledby="screened-items-title">
      <h2 id="screened-items-title">Item screening results</h2><p>Items follow the initial allocation order.</p>
      {items.map((item, index) => <ScreeningItem key={item.item_id} item={item} index={index} review={review} taskName={taskName} />)}
    </section>}
    {screening && <section className="review-panel"><h2>Screening settings</h2>
      <p>{screening.model.model} · {screening.model.reasoning_effort} reasoning · {screening.model.max_output_tokens.toLocaleString()} maximum output tokens</p>
      <details><summary>Inspect screening prompt and output schema</summary><h3>Prompt instructions</h3><pre>{screening.model.prompt}</pre>
        <h3>Output schema</h3><pre>{JSON.stringify(screening.model.output_schema, null, 2)}</pre></details>
      <details><summary>{historical ? 'Inspect screening policy' : 'Inspect screening policy and current run usage'}</summary>
        <p>{historical ? 'Usage for each assessment is retained with its item.' : 'Usage here covers this run’s calls. Retained assessments keep their original usage with each item.'}</p>
        <pre>{JSON.stringify({ policy: screening.policy, ...(!historical ? { usage: review.usage } : {}) }, null, 2)}</pre></details>
    </section>}
  </div>
}
