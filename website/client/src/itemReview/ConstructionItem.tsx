import { useEffect, useRef, useState } from 'react'
import { appPath } from '../paths'
import { DIMENSIONS, type AdaptiveReview, type ScreenedItem, type ScreeningRating } from './api'
import type { ConstructionItemSummary } from './constructionTypes'
import { ItemContent } from './ItemContent'
import { ItemMetadata } from './ItemMetadata'
import './ConstructionItems.css'

const taskLabel = (review: AdaptiveReview, id: string) => review.requirements?.task_facets.find(facet => facet.facet_id === id)?.task.text ?? id

function Evidence({ finding }: { finding: Pick<ScreeningRating, 'justification' | 'evidence' | 'information_gaps'> }) {
  return <><p className="review-preserve">{finding.justification}</p>
    {finding.evidence.length > 0 && <><h5>Model provided item evidence</h5><ul>{finding.evidence.map((passage, index) => <li className="review-preserve" key={index}>{passage}</li>)}</ul></>}
    {finding.information_gaps.length > 0 && <><h5>Information gaps</h5><ul>{finding.information_gaps.map((gap, index) => <li className="review-preserve" key={index}>{gap}</li>)}</ul></>}
  </>
}

function Assessment({ item, review, summary, step }: { item: ScreenedItem; review: AdaptiveReview; summary: ConstructionItemSummary; step?: 5 | 6 | 7 }) {
  const assessment = item.assessment
  return <div className="construction-assessment-body">
    <ItemContent text={item.question_text} />
    <div className="construction-open-metadata"><ItemMetadata summary={summary} review={review} step={step} /></div>
    {item.status === 'error' ? <><h4>Assessment could not be completed</h4><p className="review-error">{item.error}</p><p>This item has no eligibility decision.</p></> : assessment && <>
      <h4>Task identified during screening</h4><p className="review-preserve">{assessment.task.decision}</p>
      <p><strong>Task match:</strong> {assessment.task.status === 'matched' ? 'Matched to a deployment task' : assessment.task.status === 'no_match' ? 'No deployment task matched' : 'Unresolved'}</p>
      {assessment.task.matched_facet_ids.length > 0 && <ul>{assessment.task.matched_facet_ids.map(id => <li key={id}><a href={`#facet-${id}`}>{taskLabel(review, id)}</a></li>)}</ul>}
      <h4>Eligibility result</h4><p>{item.gate?.status === 'pass' ? 'Eligible' : item.gate?.status === 'fail' ? 'Not eligible' : 'Unresolved'}</p>
      <ul>{item.gate?.reasons.map((reason, index) => <li className="review-preserve" key={index}>{reason}</li>)}</ul>
      <h4>Screening ratings</h4><dl className="screening-ratings">{DIMENSIONS.map(([key, label]) => <div key={key}><dt>{label}</dt><dd>{assessment.ratings[key].score == null ? 'Unknown' : `${assessment.ratings[key].score} / 5`}</dd></div>)}</dl>
      <p className="construction-rating-note">Eligibility requires a task match and scores of at least {review.screening?.policy.minimum_score ?? 3} for input ontology, input content, input form, and output ontology. Output content and output form are reported separately.</p>
      <details><summary>Screening explanations and supporting evidence</summary>
        <section><h4>Task match</h4><Evidence finding={assessment.task} /></section>
        {DIMENSIONS.map(([key, label]) => <section key={key}><h4>{label}</h4><Evidence finding={assessment.ratings[key]} /></section>)}
      </details>
      <details><summary>Additional coverage findings ({assessment.coverage.length})</summary>{assessment.coverage.length === 0 ? <p>No additional coverage findings were recorded.</p> : assessment.coverage.map(finding => <section key={finding.requirement_index}><h4>Coverage requirement {finding.requirement_index + 1}: {finding.satisfied == null ? 'Unresolved' : finding.satisfied ? 'Satisfied' : 'Not satisfied'}</h4><p className="review-preserve">{review.requirements?.coverage_requirements[finding.requirement_index]?.requirement.text}</p><Evidence finding={finding} /></section>)}</details>
    </>}
    <details><summary>Full item record and sources</summary><h4>Item record</h4><pre>{JSON.stringify(item.evidence, null, 2)}</pre><h4>Sources and acquisition</h4><pre>{JSON.stringify({ item_id: item.item_id, sources: item.sources, acquisition: item.acquisition, evidence_hash: item.evidence_hash }, null, 2)}</pre><h4>Full assessment record</h4><pre>{JSON.stringify(item, null, 2)}</pre></details>
  </div>
}

export function ConstructionItem({ summary, item, review, exampleId, selectedIndex, onLoad, focused = false, step }: {
  summary: ConstructionItemSummary; item?: ScreenedItem; review: AdaptiveReview; exampleId: string
  selectedIndex: number; onLoad: (item: ScreenedItem) => void; focused?: boolean; step?: 5 | 6 | 7
}) {
  const [open, setOpen] = useState(false)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const element = useRef<HTMLDetailsElement>(null)
  useEffect(() => { if (focused && element.current) { element.current.open = true; setOpen(true); element.current.scrollIntoView?.({ block: 'start' }) } }, [focused])
  useEffect(() => {
    if (!open || item) return
    const controller = new AbortController()
    setError('')
    fetch(appPath(`/api/item-review/examples/${encodeURIComponent(exampleId)}/items/${encodeURIComponent(summary.item_id)}`), { cache: 'no-store', signal: controller.signal })
      .then(async response => { if (!response.ok) throw new Error('This item could not be loaded. Please try again.'); return response.json() as Promise<ScreenedItem> })
      .then(result => { if (!controller.signal.aborted) onLoad(result) })
      .catch(problem => { if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'This item could not be loaded.') })
    return () => controller.abort()
  }, [open, item, summary.item_id, exampleId, onLoad, attempt])
  // Older snapshots have no preview classification. Avoid presenting their raw
  // instruction prefix as the question; an already loaded decision is clearer.
  const previewKind = summary.preview_kind ?? (item?.assessment ? 'decision' : 'unavailable')
  const savedPreview = previewKind === 'unavailable' ? 'Open the item content to inspect the question.' : summary.preview_kind ? summary.question_preview : item?.assessment?.task.decision ?? 'Open the item content to inspect the question.'
  const preview = savedPreview.endsWith('…') ? savedPreview.slice(0, -1) + '...' : savedPreview
  return <details ref={element} className="construction-item construction-browser-item" id={step ? `step-${step}-item-${summary.item_id}` : `${summary.selected ? 'selected' : 'screened'}-item-${summary.item_id}`} onToggle={event => setOpen(event.currentTarget.open)}>
    <summary>
      <span className="construction-item-label">{summary.selected ? `Selected item ${selectedIndex + 1}` : `Screened item ${summary.index + 1}`}</span>
      {!open && (step ? <>
        <span className="construction-preview-label">{previewKind === 'decision' ? 'Task identified during screening' : 'Item content'}</span>{' '}<strong>{preview}</strong>
        <ItemMetadata summary={summary} review={review} step={step} />
      </> : <>
        <span className="construction-card-excerpt"><span className="construction-preview-label">{previewKind === 'decision' ? 'Task identified during screening' : 'Item content'}</span>{' '}<strong>{preview}</strong></span>
        <span className="construction-card-facts"><span><b>Benchmark:</b> {summary.sources.length ? summary.sources.join(', ') : 'Not recorded'}</span><span><b>Quality Q:</b> {summary.quality_score == null ? 'Not available' : `${summary.quality_score.toFixed(2)} / 5`}</span></span>
      </>)}
      {(open || step) && <span className="construction-expand-hint">{open ? 'Close item details' : 'Inspect this item'}</span>}
    </summary>
    {open && (item ? <Assessment item={item} review={review} summary={summary} step={step} /> : error ? <div className="construction-assessment-body"><p role="alert">{error}</p><button type="button" onClick={() => setAttempt(value => value + 1)}>Try loading this item again</button></div> : <p className="construction-item-loading" role="status">Loading the full item and assessment…</p>)}
  </details>
}
