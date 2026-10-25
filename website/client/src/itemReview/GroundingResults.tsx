import { useState } from 'react'
import { getReviewExport, type GroundingReview, type OnetCandidate, type OnetRecordMapping, type RunAccess } from './api'
import { GroundingForm } from './GroundingForm'
import { RequirementsContent, SupportedValue } from './RequirementsResults'

function RecordMapping({ record, candidates }: { record: OnetRecordMapping; candidates: OnetCandidate[] }) {
  const candidate = candidates.find(item => item.doc_id === record.record_id)
  return <section className="grounding-record">
    <h4>{candidate?.name ?? record.record_id}</h4>
    <p className="help"><strong>Record ID:</strong> <code>{record.record_id}</code></p>
    <p><strong>Applicability:</strong> {record.applicability === 'applicable' ? 'Applicable' : record.applicability === 'partially_applicable' ? 'Partially applicable' : 'Not applicable'}</p>
    <blockquote className="review-preserve">{record.supporting_passage}</blockquote>
    <p className="review-preserve">{record.rationale}</p>
    {record.search_terms.length > 0 && <><h5>Supported search vocabulary</h5><ul>{record.search_terms.map((term, index) => <li key={index}>{term}</li>)}</ul></>}
  </section>
}

export function GroundingResults({ review, run, busy, onCancel, onRestart, onGround }: {
  review: GroundingReview; run: RunAccess; busy: boolean; onCancel: () => void; onRestart: () => void
  onGround: (apiKey: string) => Promise<boolean>
}) {
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const active = ['preparing', 'running'].includes(review.status)
  const facets = review.grounding?.facets ?? []
  const complete = facets.filter(facet => facet.status === 'complete').length
  const total = review.requirements?.task_facets.length ?? 0

  async function download() {
    setDownloading(true)
    setDownloadError('')
    try {
      const url = URL.createObjectURL(await getReviewExport(run))
      const link = document.createElement('a')
      link.href = url
      link.download = `onet-grounding-${run.run_id}.json`
      link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (error) {
      setDownloadError(error instanceof Error ? error.message : 'Could not download grounding. Please try again.')
    } finally { setDownloading(false) }
  }

  return <div className="grounding-results">
    <section className="review-panel review-progress" aria-live="polite">
      <p className="eyebrow">Step 3 · O*NET grounding</p>
      <h2>{active ? 'Finding supporting O*NET passages' : review.status === 'completed' ? 'Your O*NET grounding is ready' : review.status === 'cancelled' ? 'Grounding stopped' : 'Grounding interrupted'}</h2>
      <p className="review-intro" role={review.status === 'failed' ? 'alert' : undefined}>{review.message}</p>
      <p>{complete} of {total} task facets mapped.</p>
      {active && <><progress max={total || 1} value={complete} aria-label="Task facets mapped" />
        <p>Local keyword and meaning-based search finds candidate passages. GPT-6 Luna checks applicability in one paid call per task facet.</p></>}
      <p>The supplied O*NET catalog covers healthcare occupations. An unmatched task keeps its original requirements without added vocabulary.</p>
      {review.status === 'completed' && <p>Record IDs and supporting quotations have been checked. Review whether each mapping fits your deployment before using its vocabulary.</p>}
      {['failed', 'cancelled'].includes(review.status) && <p>Completed mappings remain available below and in the export. You can start a new grounding run using the same extracted requirements.</p>}
      <div className="review-actions">
        {active ? <button type="button" className="secondary" disabled={busy} onClick={onCancel}>Stop grounding</button>
          : <button type="button" className="secondary" disabled={busy} onClick={onRestart}>Start another run</button>}
        <button type="button" className="secondary" disabled={downloading} onClick={() => void download()}>{downloading ? 'Downloading…' : 'Download grounding JSON'}</button>
      </div>
      {active && <p className="help">Stopping cancels pending mapping calls. A request already sent may still incur charges.</p>}
      <p className="help">Results expire one hour after the run ends. Download the JSON to keep the original answers, requirements, retrieval candidates, and mapping details.</p>
      {downloadError && <p className="review-error" role="alert">{downloadError}</p>}
    </section>

    {facets.length > 0 && <section aria-labelledby="grounding-facets-title">
      <h2 id="grounding-facets-title">O*NET mappings</h2>
      {facets.map(facet => {
        const taskIndex = review.requirements?.task_facets.findIndex(task => task.facet_id === facet.facet_id) ?? -1
        const task = review.requirements?.task_facets[taskIndex]
        const adopted = facet.mapping?.records.filter(record => record.applicability !== 'not_applicable') ?? []
        const rejected = facet.mapping?.records.filter(record => record.applicability === 'not_applicable') ?? []
        return <article className="review-panel grounding-facet" key={facet.facet_id} aria-labelledby={`grounding-title-${facet.facet_id}`}>
          <h3 id={`grounding-title-${facet.facet_id}`}>Mapping for task {taskIndex + 1}</h3>
          <p className="review-preserve">{task?.task.text}</p>
          <a href={`#facet-${facet.facet_id}`}>View extracted task and source evidence</a>
          {facet.status === 'error' && <p className="review-error" role="alert">{facet.error || 'This task has no validated mapping.'}</p>}
          {facet.status === 'complete' && adopted.length === 0 && <p>No applicable O*NET record was adopted for this task. Its extracted requirements remain unchanged.</p>}
          {adopted.map(record => <RecordMapping key={record.record_id} record={record} candidates={facet.candidates} />)}
          {!!facet.mapping?.refinements.length && <section><h4>Refinements supported by your answers</h4>
            {facet.mapping.refinements.map((refinement, index) => <SupportedValue key={index} value={refinement} />)}</section>}
          {!!facet.mapping?.unresolved_details.length && <section><h4>Unresolved mapping details</h4><ul>
            {facet.mapping.unresolved_details.map((detail, index) => <li className="review-preserve" key={index}>{detail}</li>)}</ul></section>}
          {rejected.length > 0 && <details><summary>Records considered but not adopted ({rejected.length})</summary>
            {rejected.map(record => <RecordMapping key={record.record_id} record={record} candidates={facet.candidates} />)}</details>}
          <details><summary>Inspect retrieval candidates ({facet.candidates.length})</summary>
            <h4>Search query</h4><p className="review-preserve">{facet.query}</p>
            <ol className="grounding-candidates">{facet.candidates.map(candidate => <li key={candidate.doc_id}>
              <strong>{candidate.name}</strong><p className="help"><code>{candidate.doc_id}</code> · {candidate.kind}{candidate.occupation_id && ` · Occupation ${candidate.occupation_id}`}</p>
              <p className="review-preserve">{candidate.text}</p>
              <p className="help">Meaning search rank: {candidate.dense_rank ?? 'Not ranked'} · Keyword rank: {candidate.bm25_rank ?? 'Not ranked'} · Combined ranking score: {candidate.rrf_score.toFixed(4)}</p>
            </li>)}</ol>
          </details>
        </article>
      })}
    </section>}
    {!active && review.requirements && (review.requirements.task_facets.length > 0
      ? <GroundingForm busy={busy} onGround={onGround} />
      : <p className="review-panel">No task facets are available to ground with O*NET. Start another run and clarify the tasks in your deployment answers.</p>)}
    <RequirementsContent requirements={review.requirements} deployment={review.deployment} />
  </div>
}
