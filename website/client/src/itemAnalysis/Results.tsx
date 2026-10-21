import { classifierName, labelName, readable } from './Criteria'
import type { AnalysisRun, Artifact, Classifier, Item } from './types'

const DIMENSIONS = ['input_ontology', 'input_content', 'input_form', 'output_ontology', 'output_content', 'output_form']
const ARTIFACTS: [Artifact, string][] = [['items', 'Item labels CSV'], ['summary', 'Summary JSON'], ['report', 'HTML report'], ['review', 'Human review CSV']]

function text(value: unknown): string {
  return typeof value === 'string' ? value : value == null ? 'Not supplied' : JSON.stringify(value)
}

function contentText(value: unknown): string {
  if (value == null) return ''
  if (typeof value === 'string') return value
  if (Array.isArray(value)) return value.map(contentText).filter(Boolean).join('\n\n')
  if (typeof value === 'object') {
    const message = value as Record<string, unknown>
    if (typeof message.role === 'string' && 'content' in message) {
      return `${message.role}:\n${contentText(message.content)}`
    }
    return JSON.stringify(value, null, 2)
  }
  return String(value)
}

function ItemCard({ item, classifiers, demo, classifierNames }: { item: Item; classifiers: Classifier[]; demo: boolean; classifierNames?: Record<string, string> }) {
  const completed = item.status === 'complete'
  const content = contentText(item.content)
  return <details className="ia-item">
    <summary><span><small>{item.item_id}</small><strong>{content || 'No item text available'}</strong></span>
      <span className={`ia-tag ${completed ? '' : 'ia-tag-muted'}`}>{completed ? demo ? 'Example judgment shown' : 'Classified' : item.status === 'error' ? 'Failed' : 'Pending'}</span>
    </summary>
    <div className="ia-item-body"><p className="ia-item-text">{content}</p>
      <p className="ia-reference"><strong>Reference answer</strong> {text(item.reference_answer)}</p>
      {item.error && <p className="ia-error">{item.error}</p>}
      {completed && classifiers.map(classifier => {
        const judgment = item.labels?.[classifier.id]
        return <section key={classifier.id} className="ia-judgment"><div className="ia-judgment-heading">
          <h4>{classifierName(classifier.id, classifierNames)}</h4><span>{!classifier.applicable ? 'Not applicable' : judgment ? labelName(classifier, judgment.label) : 'Unknown'}</span></div>
          {judgment && classifier.applicable && <><p>{judgment.justification}</p>
            {judgment.matched_category_ids && <p className="ia-small">Matched categories: {judgment.matched_category_ids.join(', ') || 'None'}</p>}
            {!!judgment.scope_exclusion_source_ids?.length && <p className="ia-small">Scope exclusion sources: {judgment.scope_exclusion_source_ids.join(', ')}</p>}
            {!!judgment.evidence?.length && <ul className="ia-evidence">{judgment.evidence.map((evidence, i) => <li key={i}>{evidence}</li>)}</ul>}</>}
        </section>
      })}
      {!completed && !item.error && <p className="ia-small">{demo ? 'This example will be included after the pilot review.' : 'This item has not been classified yet.'}</p>}
    </div>
  </details>
}

export function Results({ run, page, setPage, onDownload, downloading, pageLoading, demo = false, classifierNames }: {
  run: AnalysisRun
  page: number
  setPage: (page: number) => void
  onDownload: (artifact: Artifact) => void
  downloading: Artifact | null
  pageLoading: boolean
  demo?: boolean
  classifierNames?: Record<string, string>
}) {
  const summary = run.summary
  const generic = run.spec?.fixed_catalog_version === 'caliper_generic_items_v1'
  const active = ['preparing', 'generating', 'running'].includes(run.status)
  return <section className="ia-results" aria-label="Analysis results">
    {active && <p className="ia-small">Summary statistics and exports update when this phase finishes. You can inspect completed item judgments below.</p>}
    {summary && run.processed > 0 && !active && <>
      <div className="ia-section-heading"><div><p className="ia-eyebrow">From findings to counts</p><h2>What the items show</h2></div>
        <span>{summary.complete_snapshot ? demo ? 'Full demo sample' : 'Full snapshot' : demo ? 'Demo pilot results' : 'Partial results'}</span></div>
      <div className="ia-stats"><div><strong>{run.complete.toLocaleString()}</strong><span>{demo ? 'Demo judgments shown' : 'Items classified'}</span></div>
        <div><strong>{run.total.toLocaleString()}</strong><span>{demo ? 'Items in demo sample' : 'Items in snapshot'}</span></div>
        <div><strong>{run.errors.toLocaleString()}</strong><span>Failed assessments</span></div></div>
      <p className="ia-small">{demo ? 'Percentages describe all valid authored walkthrough judgments, including insufficient evidence, in this bundled sample only. They are not model outputs or estimates for the full MathDial benchmark. Operational failures and pending examples are excluded.' : generic ? 'Percentages include all valid judgments, including insufficient evidence. Invalid responses, operational failures, and pending items are excluded. No issue identified is a bounded finding, not proof of benchmark validity. Human review is needed to check accuracy.' : 'Percentages describe model judgments among known labels. Unknowns, failures, and pending items are excluded. Human review is needed to check accuracy.'}</p>
      <p className="ia-small">{summary.experiment?.completed_item_classifier_judgments ?? summary.classifiers.reduce((total, classifier) => total + (classifier.valid_judgments ?? ((classifier.known || 0) + (classifier.unknown || 0))), 0)} completed item-classifier judgments across {run.spec?.classifiers.length || 0} classifiers.</p>
      <div className="ia-distributions">{summary.classifiers.filter(c => c.applicable).map(classifier => <article key={classifier.id} className="ia-distribution">
        <h3>{classifierName(classifier.id, classifierNames)}</h3>
        <p className="ia-small">{(classifier.determinate_judgments ?? classifier.known ?? 0).toLocaleString()} {generic ? 'sufficient evidence' : 'known labels'} · {(classifier.insufficient_evidence ?? classifier.unknown ?? 0).toLocaleString()} {generic ? 'insufficient evidence' : 'unknown'} · {(classifier.invalid || 0).toLocaleString()} invalid</p>
        <div className="ia-bars">{Object.entries(classifier.counts || {}).map(([label, count]) => {
          const pct = generic ? classifier.percentages_among_valid?.[label] : classifier.percentages_among_known?.[label]
          return <div className="ia-bar-row" key={label}><div className="ia-bar-label"><span>{labelName(classifier, label)}</span>
            <span>{count.toLocaleString()} <small>{pct == null ? '—' : `${pct.toFixed(1)}%`}</small></span></div>
            <div className="ia-bar-track" aria-hidden="true"><span style={{ width: `${pct || 0}%` }} /></div></div>
        })}</div>
        {classifier.category_counts && <div><h4>Required-category matches</h4><ul>{Object.entries(classifier.category_counts).map(([id, count]) => <li key={id}>{id}: {count}</li>)}</ul><p className="ia-small">An item may match multiple categories. These counts describe the selected items; they do not establish omitted categories in the full benchmark.</p></div>}
        <p className="ia-small ia-distribution-note">{(classifier.errors || 0).toLocaleString()} failed · {(classifier.pending || 0).toLocaleString()} pending</p>
      </article>)}</div>
    </>}

    {run.assessment?.kind === 'direct' && <div className="ia-original"><strong>Benchmark assessment: Not run.</strong><p className="ia-small">These item judgments use the supplied deployment, task, and answer requirements. No benchmark-level validity scores were generated.</p></div>}
    {run.assessment?.kind !== 'direct' && !!summary?.original_assessment && <details className="ia-original"><summary>Original six-dimension assessment</summary>
      <p className="ia-small">These are the original benchmark-level judgments. Item statistics do not change these scores.</p>
      <div className="ia-original-grid">{DIMENSIONS.map(dimension => {
        const assessment = summary.original_assessment?.[dimension]
        return <div key={dimension}><h3>{readable(dimension)}</h3><strong>{typeof assessment?.score === 'number' ? `${assessment.score} / 5` : 'Not scored'}</strong>
          {(assessment?.justification || assessment?.reasoning) && <p>{assessment.justification || assessment.reasoning}</p>}</div>
      })}</div>
    </details>}

    <div className="ia-section-heading ia-item-heading"><div><p className="ia-eyebrow">Trace every judgment</p><h2>Explore the items</h2></div>
      <span>{demo ? `${run.total} bundled examples` : '20 per page'}</span></div>
    <div className="ia-items" aria-busy={pageLoading}>{run.items.map(item => <ItemCard key={item.item_id} item={item} classifiers={run.spec?.classifiers || []} demo={demo} classifierNames={classifierNames} />)}</div>
    {!run.items.length && <p className="ia-small">Items will appear when preparation finishes.</p>}
    {run.pagination.total_pages > 1 && <nav className="ia-pagination" aria-label="Item pages">
      <button type="button" className="ia-secondary" disabled={page <= 1 || pageLoading} onClick={() => setPage(page - 1)}>Previous</button>
      <span>Page {page} of {run.pagination.total_pages.toLocaleString()}</span>
      <button type="button" className="ia-secondary" disabled={page >= run.pagination.total_pages || pageLoading} onClick={() => setPage(page + 1)}>Next</button>
    </nav>}
    {summary && <div className="ia-exports"><h3>Take the results with you</h3><div>{ARTIFACTS.map(([artifact, label]) => <button key={artifact} type="button" className="ia-secondary"
      onClick={() => onDownload(artifact)} disabled={downloading !== null || active || (artifact === 'review' && generic && !(summary.experiment?.selected_items))}>{downloading === artifact ? 'Downloading…' : label}<span aria-hidden="true"> ↓</span></button>)}</div>
      <p className="ia-small">{demo ? 'Downloads cover this bundled demo sample only and include source and judgment provenance. The human review worksheet omits example judgments for independent review.' : 'The human review worksheet omits model predictions for independent review.'}</p></div>}
  </section>
}
