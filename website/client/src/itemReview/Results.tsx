import { useState } from 'react'
import { DIMENSIONS, getReviewExport, type Confidence, type LegacyConfidence, type Review, type ReviewedItem, type RunAccess } from './api'

const CONFIDENCE_LABELS: Record<LegacyConfidence, string> = {
  high: 'High confidence', medium: 'Medium confidence', low: 'Low confidence', insufficient: 'Insufficient evidence',
}

function ConfidenceBadge({ confidence }: { confidence: Confidence }) {
  const kind = confidence == null ? 'insufficient' : typeof confidence === 'number' ? 'numeric' : confidence
  const label = confidence == null ? 'Insufficient evidence' : typeof confidence === 'number'
    ? `Confidence ${confidence.toFixed(2)}` : CONFIDENCE_LABELS[confidence]
  return <span className={`review-confidence review-confidence-${kind}`}>{label}</span>
}

function ItemCard({ item, scoringVersion }: { item: ReviewedItem; scoringVersion: number }) {
  const legacy = scoringVersion < 3
  const adjusted = scoringVersion >= 5
  const noEvidence = item.scored_dimensions === 0
  const partial = item.scored_dimensions != null && item.scored_dimensions > 0 && item.scored_dimensions < 6
  return <article className="review-result" aria-label={item.rank ? `Item ${item.rank}` : item.assessment ? 'Item without a score' : 'Item assessment failed'}>
    <header className="review-result-header">
      <div className="review-result-source">{item.rank && <span className="review-rank">{String(item.rank).padStart(2, '0')}</span>}
        <span>{item.sources[0]?.benchmark ?? 'Evaluation item'}</span></div>
      {item.needs_review && <span className="review-confidence review-confidence-low">{noEvidence ? 'No scorable evidence' : 'Check evidence gaps'}</span>}
    </header>
    <div className="review-item-overview">
      <div className="review-item-question"><h3 className="eyebrow">Evaluation item</h3>
        <div className="review-item-text" tabIndex={0} role="region" aria-label="Full evaluation item">
          {item.evidence.item.content || 'This item has no text content.'}
        </div>
      </div>
      <aside className="review-score-panel" aria-label="Item score">
        <p className="eyebrow">{noEvidence ? legacy ? 'Neutral baseline' : 'No score' : legacy || adjusted ? 'Ranking score' : 'Compatibility score'}</p>
        <p className="review-score">{item.overall_score == null ? '—' : <>{item.overall_score.toFixed(2)}<span> / 5</span></>}</p>
        {item.assessment && <><p className="review-score-caption">{noEvidence ? legacy ? 'Not evidence of compatibility' : 'Insufficient evidence' : legacy || adjusted ? 'Adjusted for confidence' : partial ? 'Partial assessment' : 'Mean across six dimensions'}</p>
          <dl>{legacy && <div><dt>Unadjusted mean</dt><dd>{item.compatibility_score?.toFixed(2) ?? '—'}</dd></div>}
            {adjusted && item.compatibility_score != null && <div><dt>Compatibility mean</dt><dd>{item.compatibility_score.toFixed(2)} / 5</dd></div>}
            <div><dt>Dimensions scored</dt><dd>{item.scored_dimensions} / 6</dd></div></dl></>}
      </aside>
    </div>
    {item.error && <p className="review-error" role="status">{item.error}</p>}
    {item.assessment && <div className="review-assessment">
      <div className="review-assessment-heading"><h4>Validity dimensions</h4></div>
      <div className="review-dimensions">
        {DIMENSIONS.map(([id, label]) => {
          const dimension = item.assessment![id]
          return <div key={id} className="review-dimension">
            <span className="review-dimension-name">{label}</span>
            <strong>{dimension.score ?? '—'}<small>{dimension.score == null ? ' No score' : ' / 5'}</small></strong>
            <ConfidenceBadge confidence={dimension.confidence} />
          </div>
        })}
      </div>
      <details className="review-evidence"><summary>Assessment details</summary>
        {DIMENSIONS.map(([id, label]) => {
          const dimension = item.assessment![id]
          return <section className="review-dimension-detail" key={id}>
            <div className="review-dimension-detail-heading"><h4>{label}</h4>
              <span className="review-detail-score">{dimension.score == null ? 'No score' : `${dimension.score} / 5`}</span></div>
            <p>{dimension.justification}</p>
            <div className="review-detail-confidence"><ConfidenceBadge confidence={dimension.confidence} />
              <p>{dimension.confidence_rationale}</p></div>
            {dimension.evidence.length > 0 && <><h5>Supporting evidence</h5><ul>{dimension.evidence.map((e, i) => <li key={i}>{e}</li>)}</ul></>}
            {dimension.information_gaps.length > 0 && <div className="review-gap"><h5>Information gaps</h5><ul>{dimension.information_gaps.map((e, i) => <li key={i}>{e}</li>)}</ul></div>}
          </section>
        })}
      </details>
    </div>}
    <details className="review-source-detail"><summary>Source and reference answer</summary>
      <ul className="review-provenance">{item.sources.map((source, i) => <li key={i}>
        {source.benchmark} · {source.branch} · row {source.row}<br />
        Item ID: <code>{source.item_id}</code><br />Commit: <code>{source.commit}</code>
      </li>)}</ul>
      <pre>{JSON.stringify(item.evidence.item.grading_criterion, null, 2)}</pre>
    </details>
  </article>
}

async function download(run: RunAccess) {
  const url = URL.createObjectURL(await getReviewExport(run))
  const link = document.createElement('a')
  link.href = url
  link.download = `item-review-${run.run_id}.json`
  link.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

export function Results({ review, run, onPageChange }: { review: Review; run: RunAccess; onPageChange: (page: number) => void }) {
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const weights = review.scoring_policy.confidence_weights
  const legacy = review.scoring_policy.version < 3
  const adjusted = review.scoring_policy.version >= 5
  const unranked = review.unranked_items ?? []
  async function downloadAll() {
    setDownloading(true)
    setDownloadError('')
    try { await download(run) }
    catch (e) { setDownloadError(e instanceof Error ? e.message : 'Could not download results. Please try again.') }
    finally { setDownloading(false) }
  }
  return <section className="review-results" aria-label="Review results">
    <div className="review-result-title"><h2>Ranked sample items</h2>
      <button type="button" className="secondary" disabled={downloading} onClick={() => void downloadAll()}>{downloading ? 'Downloading…' : 'Download all results'}</button>
    </div>
    {downloadError && <p className="review-error" role="alert">{downloadError}</p>}
    <div className="review-result-stats">
      <div><strong>{review.ranked ?? review.complete}</strong><span>Items ranked</span></div>
      <div><strong>{review.needs_review}</strong><span>{review.scoring_policy.version >= 4 ? 'Evidence gaps or missing scores' : 'Low confidence or missing scores'}</span></div>
      <div><strong>{review.errors}</strong><span>Failed assessments</span></div>
    </div>
    <details className="review-ranking-help"><summary>How to read these scores</summary>
      <p>Compatibility runs from 1 (mismatch) to 5 (strong alignment). The model also reports confidence, supporting evidence, and information gaps for each dimension.</p>
      {legacy && weights ? <><p>This report uses an earlier scoring policy: scores are pulled toward {review.scoring_policy.neutral_score} with weights of {weights.high} (high), {weights.medium} (medium), and {weights.low} (low confidence). Missing scores contribute {review.scoring_policy.neutral_score}.</p>
        <p>These weights are an uncalibrated heuristic. The unadjusted mean includes only scored dimensions.</p></> : adjusted ? <>
        <p>The ranking score averages <code>1 + confidence × (compatibility − 1)</code> across all six dimensions. Lower confidence discounts support for a higher rank; it never raises a dimension’s contribution.</p>
        <p>Missing dimensions contribute 1 to ranking only; their compatibility remains unknown. The compatibility mean uses scored dimensions only. Items with no scores remain unranked.</p>
        <p>Confidence runs from 0 to 1 and describes evidence support. This adjustment is a conservative ranking heuristic, not a calibrated probability or statistical lower bound.</p></> : <>
        <p>Items are ranked by the mean of their available compatibility scores. Confidence describes evidence support and does not change the score; it is not a calibrated probability.{review.scoring_policy.version >= 4 && ' The model reports it from 0 to 1, with higher values indicating stronger support.'}</p>
        <p>Missing dimensions are excluded. Compare dimension coverage when choosing items: a high mean based on fewer dimensions may omit important unknowns. Items with no scores remain unranked.</p></>}
    </details>
    <div className="review-results-order"><p>Highest score first{review.status === 'running' && ' · Updating as items finish'}</p>
      {review.pagination.page > 1 && <button type="button" className="link" onClick={() => onPageChange(1)}>Back to top scores</button>}</div>
    {review.ranked_items.map(item => <ItemCard key={item.evidence_hash} item={item} scoringVersion={review.scoring_policy.version} />)}
    {unranked.length > 0 && <section className="review-unranked"><h2>Items without scores</h2>
      <p className="help">Evidence was insufficient to score any dimension.</p>
      {unranked.map(item => <ItemCard key={item.evidence_hash} item={item} scoringVersion={review.scoring_policy.version} />)}
    </section>}
    {review.failed_items.length > 0 && <section className="review-failed"><h2>Failed assessments</h2>
      {review.failed_items.map(item => <ItemCard key={item.evidence_hash} item={item} scoringVersion={review.scoring_policy.version} />)}
    </section>}
    {review.pagination.total_pages > 1 && <nav className="review-pagination" aria-label="Result pages">
      <button type="button" className="secondary" disabled={review.pagination.page === 1} onClick={() => onPageChange(review.pagination.page - 1)}>Previous page</button>
      <span>Page {review.pagination.page.toLocaleString()} of {review.pagination.total_pages.toLocaleString()}</span>
      <button type="button" className="secondary" disabled={review.pagination.page === review.pagination.total_pages} onClick={() => onPageChange(review.pagination.page + 1)}>Next page</button>
    </nav>}
    <p className="help">Reported usage: {(review.usage.input_tokens ?? 0).toLocaleString()} input tokens and {(review.usage.output_tokens ?? 0).toLocaleString()} output tokens, including internal reasoning.</p>
  </section>
}
