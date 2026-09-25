import { DIMENSIONS, type Confidence, type Review, type ReviewedItem } from './api'

const CONFIDENCE_LABELS: Record<Confidence, string> = {
  high: 'High confidence', medium: 'Medium confidence', low: 'Low confidence', insufficient: 'Insufficient evidence',
}

function ItemCard({ item }: { item: ReviewedItem }) {
  const noEvidence = item.scored_dimensions === 0
  return <article className="review-result" aria-label={`Item ${item.rank ?? 'assessment failed'}`}>
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
        <p className="eyebrow">{noEvidence ? 'Neutral baseline' : 'Ranking score'}</p>
        <p className="review-score">{item.overall_score == null ? '—' : item.overall_score.toFixed(2)}<span> / 5</span></p>
        {item.assessment && <><p className="review-score-caption">{noEvidence ? 'Not evidence of compatibility' : 'Adjusted for confidence'}</p>
          <dl><div><dt>Unadjusted mean</dt><dd>{item.compatibility_score?.toFixed(2) ?? '—'}</dd></div>
            <div><dt>Dimensions scored</dt><dd>{item.scored_dimensions} / 6</dd></div></dl></>}
      </aside>
    </div>
    {item.error && <p className="review-error" role="status">{item.error}</p>}
    {item.assessment && <div className="review-assessment">
      <div className="review-assessment-heading"><h4>Six dimensions of validity</h4><span>Compatibility · Confidence</span></div>
      <div className="review-dimensions">
        {DIMENSIONS.map(([id, label]) => {
          const dimension = item.assessment![id]
          return <div key={id} className="review-dimension">
            <span className="review-dimension-name">{label}</span>
            <strong>{dimension.score ?? '—'}<small>{dimension.score == null ? ' No score' : ' / 5'}</small></strong>
            <span className={`review-confidence review-confidence-${dimension.confidence}`}>{CONFIDENCE_LABELS[dimension.confidence]}</span>
          </div>
        })}
      </div>
      <details className="review-evidence"><summary>Read the scores, confidence, and evidence</summary>
        {DIMENSIONS.map(([id, label]) => {
          const dimension = item.assessment![id]
          return <section className="review-dimension-detail" key={id}>
            <h4>{label} <span>{dimension.score == null ? 'No score' : `${dimension.score} / 5`}</span></h4>
            <p>{dimension.justification}</p>
            <p><strong>{CONFIDENCE_LABELS[dimension.confidence]}:</strong> {dimension.confidence_rationale}</p>
            {dimension.evidence.length > 0 && <><h5>Supporting evidence</h5><ul>{dimension.evidence.map((e, i) => <li key={i}>{e}</li>)}</ul></>}
            {dimension.information_gaps.length > 0 && <div className="review-gap"><h5>What is still unknown</h5><ul>{dimension.information_gaps.map((e, i) => <li key={i}>{e}</li>)}</ul></div>}
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

function download(review: Review) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(review, null, 2)], { type: 'application/json' }))
  const link = document.createElement('a')
  link.href = url
  link.download = `item-review-${review.run_id}.json`
  link.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

export function Results({ review }: { review: Review }) {
  const weights = review.scoring_policy.confidence_weights
  return <section className="review-results" aria-label="Review results">
    <div className="review-result-title"><div><p className="eyebrow">Your evidence shortlist</p><h2>Ranked evaluation items</h2></div>
      <button type="button" className="secondary" onClick={() => download(review)}>Download results</button>
    </div>
    <div className="review-result-stats">
      <div><strong>{review.complete}</strong><span>Items ranked</span></div>
      <div><strong>{review.needs_review}</strong><span>Low confidence or missing scores</span></div>
      <div><strong>{review.errors}</strong><span>Failed assessments</span></div>
    </div>
    <details className="review-ranking-help"><summary>How to read these scores</summary>
      <p>Each dimension receives a compatibility score from 1 (mismatch) to 5 (strong alignment), plus the judge’s confidence and its explanation. The unadjusted mean uses only scored dimensions.</p>
      <p>The ranking score averages all six dimensions after pulling uncertain judgments toward a neutral baseline of {review.scoring_policy.neutral_score}. High, medium, and low confidence have weights of {weights.high}, {weights.medium}, and {weights.low}. A missing dimension contributes the baseline, while its actual score remains unknown.</p>
      <p>For example, a low-confidence 5 contributes 3.6. This is a transparent demo heuristic, not a calibrated probability or a verified validity measure. An item with no scorable evidence gets a neutral baseline, which can rank above an evidenced mismatch; it is not a recommendation. Inspect the evidence before choosing a test.</p>
    </details>
    <p className="review-results-scope">{review.complete > 0 ? `Showing ${review.ranked_items.length} of ${review.complete} ranked items, highest score first.` : 'Assessed items will appear here as the review progresses.'} Results cover your selected sample only.</p>
    {review.ranked_items.map(item => <ItemCard key={item.evidence_hash} item={item} />)}
    {review.failed_items.length > 0 && <section className="review-failed"><h2>Assessments that could not be completed</h2>
      <p>These calls did not produce a valid assessment. No score has been invented for them.</p>
      {review.failed_items.map(item => <ItemCard key={item.evidence_hash} item={item} />)}
    </section>}
    <p className="help">Reported usage: {(review.usage.input_tokens ?? 0).toLocaleString()} input tokens and {(review.usage.output_tokens ?? 0).toLocaleString()} output tokens, including internal reasoning.</p>
  </section>
}
