import { useState } from 'react'
import { getReviewExport, type Deployment, type Requirements, type RequirementsReview, type RunAccess, type SupportedText } from './api'
import { QUESTIONS } from './deployment'
import { GroundingForm } from './GroundingForm'

const SUMMARY_FIELDS = [
  ['workflow', 'Workflow'], ['primary_user', 'Primary user'], ['input_types', 'Input types'],
  ['output_types', 'Output types'], ['authority', 'Authority'],
] as const satisfies ReadonlyArray<readonly [keyof Requirements, string]>

export function SupportedValue({ value }: { value: SupportedText }) {
  return <div className="requirements-value">
    <p className="review-preserve">{value.text ?? 'Unknown — not specified in the answers.'}</p>
    {value.evidence.length > 0 && <ul className="requirements-evidence" aria-label="Supporting quotations">
      {value.evidence.map((source, index) => {
        const answerIndex = QUESTIONS.findIndex(question => question.id === source.answer_id)
        return <li key={index}><a href={`#original-answer-${source.answer_id}`}>
          Answer {answerIndex + 1}: {QUESTIONS[answerIndex].title}
        </a><blockquote className="review-preserve">{source.quote}</blockquote></li>
      })}
    </ul>}
  </div>
}

export function RequirementsResults({ review, run, busy, onCancel, onRestart, onGround }: {
  review: RequirementsReview; run: RunAccess; busy: boolean; onCancel: () => void; onRestart: () => void
  onGround: (apiKey: string) => Promise<boolean>
}) {
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const active = ['preparing', 'running'].includes(review.status)
  const requirements = review.requirements

  async function download() {
    setDownloading(true)
    setDownloadError('')
    try {
      const url = URL.createObjectURL(await getReviewExport(run))
      const link = document.createElement('a')
      link.href = url
      link.download = `requirements-${run.run_id}.json`
      link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (e) {
      setDownloadError(e instanceof Error ? e.message : 'Could not download requirements. Please try again.')
    } finally { setDownloading(false) }
  }

  return <div className="requirements-results">
    <section className="review-panel review-progress" aria-live="polite">
      <h2>{active ? 'Extracting requirements' : review.status === 'completed' ? 'Your extracted requirements are ready' : review.status === 'cancelled' ? 'Extraction stopped' : 'Extraction interrupted'}</h2>
      <p className="review-intro" role={review.status === 'failed' ? 'alert' : undefined}>{review.message}</p>
      {active && <><progress aria-label="Requirements extraction in progress" />
        <p>GPT-6 Luna extracts requirements from your six answers. This is one paid model call.</p></>}
      {review.status === 'completed' && <p>Source references and exact quotations have been checked. Review whether the interpretation matches your intended deployment.</p>}
      {review.status === 'failed' && <p>No validated requirements are available. Your original answers remain available below and in the export.</p>}
      <div className="review-actions">
        {active ? <button type="button" className="secondary" disabled={busy} onClick={onCancel}>Stop extraction</button>
          : <button type="button" className="secondary" disabled={busy} onClick={onRestart}>Start another run</button>}
        <button type="button" className="secondary" disabled={downloading} onClick={() => void download()}>{downloading ? 'Downloading…' : 'Download requirements JSON'}</button>
      </div>
      {active && <p className="help">Stopping cancels the pending extraction. A request already sent may still incur charges.</p>}
      <p className="help">Progress is saved so you can return later. Download the JSON for a separate copy of the original answers and extraction details.</p>
      {downloadError && <p className="review-error" role="alert">{downloadError}</p>}
    </section>

    {review.status === 'completed' && requirements && (requirements.task_facets.length > 0
      ? <GroundingForm busy={busy} onGround={onGround} />
      : <p className="review-panel">No task facets were extracted to ground with O*NET. Start another run and clarify the tasks in your deployment answers.</p>)}
    <RequirementsContent requirements={requirements} />
  </div>
}

export function RequirementsContent({ requirements }: { requirements: Requirements | null }) {
  return <>
    {requirements && <>
      <section className="review-panel requirements-summary" aria-labelledby="requirements-summary-title">
        <h2 id="requirements-summary-title">Deployment summary</h2>
        {SUMMARY_FIELDS.map(([field, label]) => <section key={field}><h3>{label}</h3><SupportedValue value={requirements[field]} /></section>)}
      </section>
      <section aria-labelledby="requirements-facets-title">
        <h2 id="requirements-facets-title">Task facets</h2>
        {requirements.task_facets.length === 0 && <p>No supported task facets were extracted.</p>}
        {requirements.task_facets.map((facet, index) => <article className="review-panel requirements-facet" id={`facet-${facet.facet_id}`} key={facet.facet_id} aria-labelledby={`facet-title-${facet.facet_id}`}>
          <div className="review-result-title"><h3 id={`facet-title-${facet.facet_id}`}>Task {index + 1}</h3>
            <span className={`review-confidence ${facet.essential === true ? 'review-confidence-high' : 'review-confidence-insufficient'}`}>
              {facet.essential == null ? 'Essential status unknown' : facet.essential ? 'Essential' : 'Not essential'}
            </span></div>
          <SupportedValue value={facet.task} />
          <h4>Required input evidence</h4><SupportedValue value={facet.required_input_evidence} />
          <h4>Required output behavior</h4><SupportedValue value={facet.required_output_behavior} />
        </article>)}
      </section>
      <section className="review-panel" aria-labelledby="requirements-coverage-title">
        <h2 id="requirements-coverage-title">Explicit coverage requirements</h2>
        <p className="help">These requirements describe the collection of benchmark items to select.</p>
        {requirements.coverage_requirements.length === 0 ? <p>No explicit collection coverage requirements were stated.</p>
          : requirements.coverage_requirements.map((coverage, index) => <section className="requirements-coverage" key={index}>
            <h3>Coverage requirement {index + 1}</h3><SupportedValue value={coverage.requirement} />
            <p><strong>Minimum items:</strong> {coverage.minimum_items ?? 'Unspecified'}</p>
            {coverage.facet_ids.length > 0 ? <p><strong>Applies to: </strong>{coverage.facet_ids.map((id, facetIndex) => {
              const taskIndex = requirements.task_facets.findIndex(facet => facet.facet_id === id)
              return <span key={id}>{facetIndex > 0 && ', '}<a href={`#facet-${id}`}>Task {taskIndex + 1}</a></span>
            })}</p> : <p>Applies to the whole collection.</p>}
          </section>)}
      </section>
      <section className="review-panel" aria-labelledby="requirements-unknowns-title">
        <h2 id="requirements-unknowns-title">Unresolved details</h2>
        {requirements.unresolved_details.length > 0 ? <ul>{requirements.unresolved_details.map((detail, index) => <li className="review-preserve" key={index}>{detail}</li>)}</ul>
          : <p>No unresolved details were reported by the extraction.</p>}
      </section>
    </>}
  </>
}

export function DeploymentAnswers({ deployment }: { deployment: Deployment }) {
  return <section className="review-panel requirements-original" aria-labelledby="requirements-original-title">
    <h2 id="requirements-original-title">Original deployment answers</h2>
    {QUESTIONS.map((question, index) => <section key={question.id} id={`original-answer-${question.id}`}>
      <h3>Answer {index + 1}: {question.title}</h3>
      <p className="review-preserve">{deployment[question.id] || 'No answer supplied.'}</p>
    </section>)}
  </section>
}
