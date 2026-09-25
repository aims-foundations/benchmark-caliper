import { DIMENSIONS, type Review, type ReviewedItem } from './api'

function ItemCard({ item }: { item: ReviewedItem }) {
  return (
    <article className="review-result">
      <div className="review-result-title">
        <h3>{item.rank ? `#${item.rank} · ` : ''}{item.sources[0]?.benchmark}</h3>
        <span className="review-score">{item.overall_score == null ? 'Unranked' : `${item.overall_score.toFixed(2)} / 5`}</span>
      </div>
      <p className="review-item-text">{item.evidence.item.content || 'This item has no text content.'}</p>
      {item.error && <p role="status">{item.error}</p>}
      {item.assessment && (
        <>
          <div className="review-dimensions">
            {DIMENSIONS.map(([id, label]) => <div key={id}><span>{label}</span><strong>{item.assessment?.[id]?.score ?? 'Unknown'}</strong></div>)}
          </div>
          <details><summary>Review scores and supporting evidence</summary>
            {DIMENSIONS.map(([id, label]) => {
              const dimension = item.assessment?.[id]
              return dimension && <section className="review-dimension-detail" key={id}>
                <h4>{label} · {dimension.score ?? 'Unknown'}</h4>
                <p>{dimension.justification}</p>
                {dimension.evidence.length > 0 && <><strong>Evidence</strong><ul>{dimension.evidence.map((e, i) => <li key={i}>{e}</li>)}</ul></>}
                {dimension.information_gaps.length > 0 && <><strong>Information gaps</strong><ul>{dimension.information_gaps.map((e, i) => <li key={i}>{e}</li>)}</ul></>}
              </section>
            })}
          </details>
        </>
      )}
      <details><summary>Item provenance and reference answer</summary>
        <ul className="review-provenance">{item.sources.map((source, i) => <li key={i}>
          {source.benchmark} · {source.branch} · row {source.row}<br />
          Item ID: <code>{source.item_id}</code><br />
          Commit: <code>{source.commit}</code>
        </li>)}</ul>
        <pre>{JSON.stringify(item.evidence.item.grading_criterion, null, 2)}</pre>
      </details>
    </article>
  )
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
  return <section aria-label="Review results">
    <div className="review-result-title"><h2>Ranked evaluation items</h2>
      <button type="button" className="secondary" onClick={() => download(review)}>Download results</button>
    </div>
    <p className="help">{review.complete} ranked · {review.unresolved} unresolved · {review.errors} failed. These results cover the selected sample only.
      The overall score is the mean of all six dimensions; inspect individual scores and evidence before choosing a test.</p>
    {review.ranked_items.length === 0 && <p>No items have a complete six-dimension assessment yet.</p>}
    {review.ranked_items.map(item => <ItemCard key={item.evidence_hash} item={item} />)}
    {review.unresolved_items.length > 0 && <section className="review-unresolved"><h2>Items needing further review</h2>
      <p>Missing evidence and failed assessments are retained here. They are not treated as low-scoring items.</p>
      {review.unresolved_items.map(item => <ItemCard key={item.evidence_hash} item={item} />)}
    </section>}
    <p className="help">Reported usage: {(review.usage.input_tokens ?? 0).toLocaleString()} input tokens and {(review.usage.output_tokens ?? 0).toLocaleString()} output tokens, including internal reasoning.</p>
  </section>
}
