import { classifierName, labelName, readable } from './Criteria'
import type { AnalysisRun, Artifact, Classifier, Item } from './types'

const DIMENSIONS = ['input_ontology', 'input_content', 'input_form', 'output_ontology', 'output_content', 'output_form']
const ARTIFACTS: [Artifact, string][] = [['items', 'Item labels CSV'], ['summary', 'Summary JSON'], ['report', 'HTML report'], ['review', 'Human review CSV']]

function text(value: unknown): string {
  return typeof value === 'string' ? value : value == null ? 'Not supplied' : JSON.stringify(value)
}

function ItemCard({ item, classifiers }: { item: Item; classifiers: Classifier[] }) {
  const completed = item.status === 'complete'
  return <details className="ia-item">
    <summary><span><small>{item.item_id}</small><strong>{item.content || 'No item text available'}</strong></span>
      <span className={`ia-tag ${completed ? '' : 'ia-tag-muted'}`}>{completed ? 'Classified' : item.status === 'error' ? 'Failed' : 'Pending'}</span>
    </summary>
    <div className="ia-item-body"><p className="ia-item-text">{item.content}</p>
      <p className="ia-reference"><strong>Reference answer</strong> {text(item.reference_answer)}</p>
      {item.error && <p className="ia-error">{item.error}</p>}
      {completed && classifiers.map(classifier => {
        const judgment = item.labels?.[classifier.id]
        return <section key={classifier.id} className="ia-judgment"><div className="ia-judgment-heading">
          <h4>{classifierName(classifier.id)}</h4><span>{!classifier.applicable ? 'Not applicable' : judgment ? labelName(classifier, judgment.label) : 'Unknown'}</span></div>
          {judgment && classifier.applicable && <><p>{judgment.justification}</p>
            {!!judgment.evidence?.length && <ul className="ia-evidence">{judgment.evidence.map((evidence, i) => <li key={i}>{evidence}</li>)}</ul>}</>}
        </section>
      })}
      {!completed && !item.error && <p className="ia-small">This item has not been classified yet.</p>}
    </div>
  </details>
}

export function Results({ run, page, setPage, onDownload, downloading, pageLoading }: {
  run: AnalysisRun
  page: number
  setPage: (page: number) => void
  onDownload: (artifact: Artifact) => void
  downloading: Artifact | null
  pageLoading: boolean
}) {
  const summary = run.summary
  const active = ['preparing', 'generating', 'running'].includes(run.status)
  return <section className="ia-results" aria-label="Analysis results">
    {active && <p className="ia-small">Summary statistics and exports update when this phase finishes. You can inspect completed item judgments below.</p>}
    {summary && run.processed > 0 && !active && <>
      <div className="ia-section-heading"><div><p className="ia-eyebrow">From findings to counts</p><h2>What the items show</h2></div>
        <span>{summary.complete_snapshot ? 'Full snapshot' : 'Partial results'}</span></div>
      <div className="ia-stats"><div><strong>{run.complete.toLocaleString()}</strong><span>Items classified</span></div>
        <div><strong>{run.total.toLocaleString()}</strong><span>Items in snapshot</span></div>
        <div><strong>{run.errors.toLocaleString()}</strong><span>Failed assessments</span></div></div>
      <p className="ia-small">Percentages describe model judgments among known labels. Unknowns, failures, and pending items are excluded. Human review is needed to check accuracy.</p>
      <div className="ia-distributions">{summary.classifiers.filter(c => c.applicable).map(classifier => <article key={classifier.id} className="ia-distribution">
        <h3>{classifierName(classifier.id)}</h3>
        <p className="ia-small">{(classifier.known || 0).toLocaleString()} known labels · {(classifier.unknown || 0).toLocaleString()} unknown · {(classifier.invalid || 0).toLocaleString()} invalid</p>
        <div className="ia-bars">{Object.entries(classifier.counts || {}).map(([label, count]) => {
          const pct = classifier.percentages_among_known?.[label]
          return <div className="ia-bar-row" key={label}><div className="ia-bar-label"><span>{labelName(classifier, label)}</span>
            <span>{count.toLocaleString()} <small>{pct == null ? '—' : `${pct.toFixed(1)}%`}</small></span></div>
            <div className="ia-bar-track" aria-hidden="true"><span style={{ width: `${pct || 0}%` }} /></div></div>
        })}</div>
        <p className="ia-small ia-distribution-note">{(classifier.errors || 0).toLocaleString()} failed · {(classifier.pending || 0).toLocaleString()} pending</p>
      </article>)}</div>
    </>}

    {!!summary?.original_assessment && <details className="ia-original"><summary>Original six-dimension assessment</summary>
      <p className="ia-small">These are the original benchmark-level judgments. Item statistics do not change these scores.</p>
      <div className="ia-original-grid">{DIMENSIONS.map(dimension => {
        const assessment = summary.original_assessment?.[dimension]
        return <div key={dimension}><h3>{readable(dimension)}</h3><strong>{typeof assessment?.score === 'number' ? `${assessment.score} / 5` : 'Not scored'}</strong>
          {(assessment?.justification || assessment?.reasoning) && <p>{assessment.justification || assessment.reasoning}</p>}</div>
      })}</div>
    </details>}

    <div className="ia-section-heading ia-item-heading"><div><p className="ia-eyebrow">Trace every judgment</p><h2>Explore the items</h2></div>
      <span>20 per page</span></div>
    <div className="ia-items" aria-busy={pageLoading}>{run.items.map(item => <ItemCard key={item.item_id} item={item} classifiers={run.spec?.classifiers || []} />)}</div>
    {!run.items.length && <p className="ia-small">Items will appear when preparation finishes.</p>}
    {run.pagination.total_pages > 1 && <nav className="ia-pagination" aria-label="Item pages">
      <button type="button" className="ia-secondary" disabled={page <= 1 || pageLoading} onClick={() => setPage(page - 1)}>Previous</button>
      <span>Page {page} of {run.pagination.total_pages.toLocaleString()}</span>
      <button type="button" className="ia-secondary" disabled={page >= run.pagination.total_pages || pageLoading} onClick={() => setPage(page + 1)}>Next</button>
    </nav>}
    {summary && <div className="ia-exports"><h3>Take the results with you</h3><div>{ARTIFACTS.map(([artifact, label]) => <button key={artifact} type="button" className="ia-secondary"
      onClick={() => onDownload(artifact)} disabled={downloading !== null || active}>{downloading === artifact ? 'Downloading…' : label}<span aria-hidden="true"> ↓</span></button>)}</div>
      <p className="ia-small">The human review worksheet omits model predictions for independent review.</p></div>}
  </section>
}
