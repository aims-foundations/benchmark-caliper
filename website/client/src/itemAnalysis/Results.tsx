import { SixScoreTable } from './SixScoreTable'
import { classifierName, labelName, readable } from './Criteria'
import { dimensionAverages } from './sixScoreSummary'
import type { AnalysisRun, Artifact, Classifier, Item } from './types'

const DIMENSIONS = ['input_ontology', 'input_content', 'input_form', 'output_ontology', 'output_content', 'output_form']
const ARTIFACTS: [Artifact, string][] = [['spec', 'Criteria JSON'], ['items', 'Item labels CSV'], ['summary', 'Summary JSON'], ['report', 'HTML report']]
const DESCRIPTIONS: Record<string, string> = {
  input_ontology: 'Which tasks, skills, or situations required by the deployment does each input represent?',
  input_content: 'Do the input’s details or assumptions introduce a supported conflict with the intended task or deployment?',
  output_ontology: 'Do the benchmark’s answer categories and scoring rules fit the decisions required in the deployment?',
  output_content: 'Does this item’s reference answer or annotation conflict with a supported standard for the target context?',
}
const PAGE_SIZE = 20
export type ItemFilter = { kind: 'all' | 'flagged' | 'uncertain' | 'retry'; classifierId?: string }
const FILTERS: [ItemFilter['kind'], string][] = [['all', 'All items'], ['flagged', 'Flagged items'], ['uncertain', 'Uncertain items'], ['retry', 'Items needing retry']]

type ResultsProps = {
  run: AnalysisRun
  page: number
  setPage: (page: number) => void
  onDownload: (artifact: Artifact) => void
  onViewReport?: () => void
  onDownloadPackage?: () => void
  downloading: Artifact | 'package' | 'view' | null
  pageLoading: boolean
  demo?: boolean
  classifierNames?: Record<string, string>
}

export function matchesItemFilter(item: Item, filter: ItemFilter, classifiers: Classifier[] = []): boolean {
  if (filter.kind === 'all') return true
  if (filter.kind === 'retry') return filter.classifierId
    ? !!item.classifier_errors?.[filter.classifierId]
    : item.status === 'error' || Object.keys(item.classifier_errors || {}).length > 0
  if (item.dimensions) return Object.entries(item.dimensions).some(([id, assessment]) => (!filter.classifierId || filter.classifierId === id) && (filter.kind === 'uncertain' ? assessment.score === null : assessment.score !== null && assessment.score <= 2))
  return Object.entries(item.labels || {}).some(([id, judgment]) => {
    if (filter.classifierId && id !== filter.classifierId) return false
    const classifier = classifiers.find(candidate => candidate.id === id)
    if (classifier?.applicable === false) return false
    if (filter.kind === 'uncertain') return judgment.label === null || ['insufficient_evidence', 'unknown'].includes(String(judgment.label))
    return ['issue_identified', 'no_match'].includes(String(judgment.label)) || (classifier?.operation === 'flag' && String(judgment.label) === '1')
  })
}

function text(value: unknown): string {
  return typeof value === 'string' ? value : value == null ? 'Not supplied' : JSON.stringify(value)
}

function contentText(value: unknown): string {
  if (value == null) return ''
  if (typeof value === 'string') return value
  if (Array.isArray(value)) return value.map(contentText).filter(Boolean).join('\n\n')
  if (typeof value === 'object') {
    const message = value as Record<string, unknown>
    if (typeof message.role === 'string' && 'content' in message) return `${message.role}:\n${contentText(message.content)}`
    return JSON.stringify(value, null, 2)
  }
  return String(value)
}

function shortExplanation(value: string): string {
  if (value.length <= 260) return value
  const sentence = value.slice(0, 260).match(/^.*?[.!?](?:\s|$)/)?.[0]?.trim()
  return sentence && sentence.length >= 60 ? sentence : `${value.slice(0, 257).replace(/\s+\S*$/, '')}…`
}

function resultCounts(run: AnalysisRun) {
  const classifierCount = run.spec?.classifiers.filter(classifier => classifier.applicable).length || 0
  const saved = run.completed_judgments ?? run.summary?.experiment?.completed_item_classifier_judgments ?? run.summary?.classifiers.reduce((total, classifier) => total + (classifier.valid_judgments ?? ((classifier.known || 0) + (classifier.unknown || 0))), 0) ?? 0
  const remaining = run.scope ? run.remaining_judgments?.[run.scope] : undefined
  const expected = remaining !== undefined ? saved + remaining : run.summary?.experiment?.expected_item_classifier_judgments ?? (run.scope === 'all' ? run.total : run.processed) * classifierCount
  const selected = remaining !== undefined && classifierCount ? Math.round(expected / classifierCount) : run.summary?.experiment?.selected_items ?? (run.scope === 'all' ? run.total : run.processed)
  const missing = Math.max(0, expected - saved)
  const failed = run.summary?.classifiers.reduce((total, classifier) => total + (classifier.errors || 0) + (classifier.invalid || 0), 0) || 0
  return { selected, saved, expected, missing, failed }
}

export function ProcessingCounts({ run, demo = false }: { run: AnalysisRun; demo?: boolean }) {
  const { selected, saved, expected, missing, failed } = resultCounts(run)
  const active = ['preparing', 'generating', 'running'].includes(run.status)
  return <div className="ia-processing-counts" aria-label="Classification processing counts">
    <div className="ia-stats ia-result-stats"><div><strong>{selected.toLocaleString()}</strong><span>Selected items</span><small>of {run.total.toLocaleString()} in the {demo ? 'demo sample' : 'snapshot'}</small></div>
      <div><strong>{saved.toLocaleString()}</strong><span>Saved classifier judgments</span><small>of {expected.toLocaleString()} expected</small></div>
      <div><strong>{run.complete.toLocaleString()}</strong><span>{demo ? 'Demo items complete' : 'Items fully classified'}</span><small>{run.errors.toLocaleString()} {run.errors === 1 ? 'item' : 'items'} needing retry</small></div>
      <div><strong>{missing.toLocaleString()}</strong><span>Missing classifier judgments</span><small>{active ? 'Pending or awaiting retry' : `${failed.toLocaleString()} failed or invalid ${failed === 1 ? 'dimension' : 'dimensions'}`}</small></div></div>
    <p className="ia-small">{saved} completed item-classifier judgments across {run.spec?.classifiers.length || 0} classifiers.</p>
    <p className="ia-small">These counts describe processing progress. They do not measure scientific validity or human-review completion.</p>
  </div>
}

function ItemCard({ item, index, classifiers, demo, classifierNames }: { item: Item; index: number; classifiers: Classifier[]; demo: boolean; classifierNames?: Record<string, string> }) {
  const completed = item.status === 'complete'
  const hasJudgments = !!Object.keys(item.labels || {}).length
  const content = contentText(item.content)
  return <details className="ia-item">
    <summary><span><small>Item {index}</small><strong>{content || 'No item text available'}</strong></span>
      <span className={`ia-tag ${completed ? '' : 'ia-tag-muted'}`}>{completed ? demo ? 'Example judgment shown' : 'Classified' : item.status === 'error' ? 'Needs retry' : hasJudgments ? 'Partly classified' : 'Pending'}</span>
    </summary>
    <div className="ia-item-body">{content.length > 800 ? <details className="ia-long-text"><summary>Read full item text</summary><p className="ia-item-text">{content}</p></details> : <p className="ia-item-text">{content}</p>}
      <details className="ia-reference-details"><summary>Reference answer</summary><p className="ia-reference">{text(item.reference_answer)}</p></details>
      {item.error && <p className="ia-error">{item.error}</p>}
      <div className="ia-item-judgments">{(!demo || completed || hasJudgments || item.status === 'error') && classifiers.map(classifier => {
        const judgment = item.labels?.[classifier.id]
        const failure = item.classifier_errors?.[classifier.id]
        const explanation = judgment ? shortExplanation(judgment.justification) : ''
        return <section key={classifier.id} className="ia-judgment"><div className="ia-judgment-heading">
          <h4>{classifierName(classifier.id, classifierNames)}</h4><span>{!classifier.applicable ? 'Not applicable' : judgment ? labelName(classifier, judgment.label) : failure ? 'Needs retry' : 'Pending'}</span></div>
          {failure && !judgment && <p className="ia-error">{failure}</p>}
          {judgment && classifier.applicable && <><p>{explanation}</p>
            {(!!judgment.evidence?.length || explanation !== judgment.justification) && <details className="ia-judgment-evidence"><summary>Evidence and full explanation</summary>
              {explanation !== judgment.justification && <p>{judgment.justification}</p>}
              {!!judgment.evidence?.length && <ul className="ia-evidence">{judgment.evidence.map((evidence, i) => <li key={i}>{evidence}</li>)}</ul>}
            </details>}
            {(judgment.matched_category_ids || !!judgment.scope_exclusion_source_ids?.length) && <details className="ia-technical-details"><summary>Category and source references</summary>
              {judgment.matched_category_ids && <p className="ia-small">Matched categories: {judgment.matched_category_ids.join(', ') || 'None'}</p>}
              {!!judgment.scope_exclusion_source_ids?.length && <p className="ia-small">Scope exclusion sources: {judgment.scope_exclusion_source_ids.join(', ')}</p>}
            </details>}
          </>}
          {!judgment && !failure && classifier.applicable && <p>{demo ? 'No authored judgment is shown for this dimension yet.' : 'No judgment has been saved for this dimension yet.'}</p>}
        </section>
      })}</div>
      {!completed && hasJudgments && <p className="ia-small">Completed classifier judgments are saved. Continuing reuses them and assesses only the remaining dimensions.</p>}
      {!completed && !hasJudgments && !item.error && <p className="ia-small">{demo ? 'This example will be included after the pilot review.' : 'This item has not been classified yet.'}</p>}
      <details className="ia-technical-details"><summary>Item identifier</summary><code>{item.item_id}</code></details>
    </div>
  </details>
}

export function ItemJudgments({ run, page, setPage, pageLoading, demo = false, classifierNames, filter = { kind: 'all' }, onFilterChange, filteredItems, filterLoading = false }: {
  run: AnalysisRun; page: number; setPage: (page: number) => void; pageLoading: boolean; demo?: boolean; classifierNames?: Record<string, string>
  filter?: ItemFilter; onFilterChange?: (filter: ItemFilter) => void; filteredItems?: Item[]; filterLoading?: boolean
}) {
  const sixScores = run.analysis_type === 'six_scores' || run.spec?.schema_version === 'caliper_item_context_v1'
  const filtering = filter.kind !== 'all'
  const localMatches = run.items.filter(item => matchesItemFilter(item, filter, run.spec?.classifiers))
  const matches = filteredItems ?? localMatches
  const items = filtering ? matches.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE) : run.items
  const totalPages = filtering ? Math.max(1, Math.ceil(matches.length / PAGE_SIZE)) : run.pagination.total_pages
  const loading = pageLoading || filterLoading
  const active = ['preparing', 'generating', 'running'].includes(run.status)
  const completeFilter = filteredItems !== undefined || run.pagination.total_pages <= 1
  return <div className="ia-item-results">
    <div className="ia-section-heading ia-item-heading"><h3>Explore the items</h3><span>{demo ? `${run.total} bundled examples` : '20 per page'}</span></div>
    <p className="ia-small">{sixScores ? 'Select any score to inspect the complete item, reference answer, grading criteria, and supporting evidence.' : <>Open an item to compare its {run.spec?.classifiers.length === 4 ? 'four ' : ''}judgments. Each judgment has a short explanation; evidence and longer text are expandable.</>}</p>
    {onFilterChange && <div className="ia-item-filters" role="group" aria-label="Filter item judgments">{FILTERS.map(([kind, name]) => <button type="button" key={kind} className="ia-filter-button"
      aria-pressed={filter.kind === kind} disabled={active} onClick={() => onFilterChange({ kind })}>{sixScores && kind === 'flagged' ? 'Low scores (1–2)' : sixScores && kind === 'uncertain' ? 'Unknown scores' : name}</button>)}</div>}
    {filtering && <p className="ia-filter-summary" role="status">{filterLoading ? 'Searching selected items across all pages…' : `${matches.length.toLocaleString()} matching ${matches.length === 1 ? 'item' : 'items'}${completeFilter ? ' across selected items' : ' on the loaded page'}.`}
      {filter.classifierId && <> Dimension: <strong>{classifierName(filter.classifierId, classifierNames)}</strong>.</>}
      {onFilterChange && <button type="button" className="ia-text-button" onClick={() => onFilterChange({ kind: 'all' })}>Clear filter</button>}
    </p>}
    {filter.kind === 'flagged' && <p className="ia-small">{sixScores ? 'Low scores identify substantial or fundamental mismatches for closer inspection.' : 'Flags include a required-category non-match or an identified issue. They are classifier findings for inspection, not confirmed scientific errors.'}</p>}
    {filter.kind === 'uncertain' && <p className="ia-small">Uncertain means a saved judgment reports insufficient evidence or an unknown label. Items awaiting classification are separate.</p>}
    <div className="ia-items" aria-busy={loading}>{sixScores && run.spec ? <SixScoreTable items={filterLoading ? [] : items} spec={run.spec} loading={loading} /> : !filterLoading && items.map((item, index) => <ItemCard key={item.item_id} item={item} index={(page - 1) * PAGE_SIZE + index + 1} classifiers={run.spec?.classifiers || []} demo={demo} classifierNames={classifierNames} />)}</div>
    {!items.length && !loading && <p className="ia-small">{filtering ? 'No saved items match this filter.' : 'Items will appear when preparation finishes.'}</p>}
    {totalPages > 1 && !filterLoading && <nav className="ia-pagination" aria-label="Item pages">
      <button type="button" className="ia-secondary" disabled={page <= 1 || loading} onClick={() => setPage(page - 1)}>Previous</button>
      <span>Page {page} of {totalPages.toLocaleString()}</span>
      <button type="button" className="ia-secondary" disabled={page >= totalPages || loading} onClick={() => setPage(page + 1)}>Next</button>
    </nav>}
  </div>
}

function OriginalAssessment({ run }: { run: AnalysisRun }) {
  if (run.assessment?.kind === 'direct') return <details className="ia-original"><summary>Benchmark assessment: Not run.</summary><p className="ia-small">These item judgments use the supplied deployment, task, and answer requirements. No benchmark-level validity scores were generated.</p></details>
  if (!run.summary?.original_assessment) return null
  return <details className="ia-original"><summary>Original six-dimension assessment</summary>
    <p className="ia-small">These are the original benchmark-level judgments. Item statistics do not change these scores.</p>
    <div className="ia-original-grid">{DIMENSIONS.map(dimension => {
      const assessment = run.summary?.original_assessment?.[dimension]
      return <div key={dimension}><h3>{readable(dimension)}</h3><strong>{typeof assessment?.score === 'number' ? `${assessment.score} / 5` : 'Not scored'}</strong>
        {(assessment?.justification || assessment?.reasoning) && <p>{assessment.justification || assessment.reasoning}</p>}</div>
    })}</div>
  </details>
}

export function DimensionAverages({ run, demo = false }: { run: AnalysisRun; demo?: boolean }) {
  if (!(run.analysis_type === 'six_scores' || run.spec?.schema_version === 'caliper_item_context_v1') || !run.summary) return null
  const summary = run.summary
  const selected = summary.experiment?.selected_items ?? summary.total_items
  const evaluated = typeof summary.experiment?.selected_completed_items === 'number' ? summary.experiment.selected_completed_items : summary.completed_items
  const scope = summary.complete_snapshot ? demo ? 'Full demo sample' : 'Full snapshot' : selected < summary.total_items ? 'Selected items' : 'Partial results'
  return <section className="ia-dimension-averages" aria-labelledby="ia-dimension-averages-title">
    <div className="ia-section-heading"><h3 id="ia-dimension-averages-title">Average item scores</h3><span className="ia-tag">{scope}</span></div>
    <p className="ia-small">{evaluated.toLocaleString()} of {selected.toLocaleString()} selected items evaluated, from {summary.total_items.toLocaleString()} items in the {demo ? 'demo sample' : 'prepared snapshot'}. Averages use all evaluated items in this run, regardless of the item table’s page or filter.</p>
    <div className="ia-average-table-scroll"><table className="ia-average-table" aria-label="Dimension averages and benchmark scores">
      <thead><tr><th scope="col">Dimension</th><th scope="col">Item average</th><th scope="col">Items included</th><th scope="col">Benchmark score</th></tr></thead>
      <tbody>{dimensionAverages(run).map(dimension => <tr key={dimension.id}>
        <th scope="row">{classifierName(dimension.id)}</th>
        <td><strong>{dimension.mean === null ? 'Unknown' : `${dimension.mean.toFixed(2)} / 5`}</strong>{dimension.mean === null && <small>No numeric scores</small>}</td>
        <td>{dimension.known.toLocaleString()} numeric<small>{dimension.unknown.toLocaleString()} Unknown</small></td>
        <td>{dimension.benchmark}</td>
      </tr>)}</tbody>
    </table></div>
    <p className="ia-small">Each average is the sum of numeric scores divided by their count for that dimension. Unknown, failed, and pending items are excluded. Item averages describe the evaluated items; the original benchmark scores assess the benchmark as a whole.</p>
    {demo && <p className="ia-small">These averages describe authored illustrative scores, not model outputs or estimates for the full benchmark.</p>}
  </section>
}

export function SummaryFindings({ run, demo = false, classifierNames, onInspect }: { run: AnalysisRun; demo?: boolean; classifierNames?: Record<string, string>; onInspect?: (filter: ItemFilter) => void }) {
  if (run.analysis_type === 'six_scores' || run.spec?.schema_version === 'caliper_item_context_v1') return <div className="ia-summary-findings">
    <p className="ia-small">Distributions describe saved numeric scores for each dimension. Unknown, failed, and pending assessments are counted separately. These are not benchmark-level scores.</p>
    <div className="ia-distributions">{run.summary?.classifiers.map(dimension => {
      const known = dimension.known ?? dimension.determinate_judgments ?? Object.values(dimension.counts || {}).reduce((total, count) => total + count, 0)
      const low = (dimension.counts?.['1'] || 0) + (dimension.counts?.['2'] || 0)
      return <article key={dimension.id} className="ia-distribution"><h3>{classifierName(dimension.id)}</h3><div className="ia-bars">{[1, 2, 3, 4, 5].map(score => {
        const count = dimension.counts?.[String(score)] || 0
        const percentage = known ? count / known * 100 : 0
        return <div key={score} className="ia-bar-row"><div className="ia-bar-label"><span>{score} / 5</span><span>{count} <small>{known ? `${percentage.toFixed(1)}%` : '—'}</small></span></div><div className="ia-bar-track" aria-hidden="true"><span style={{ width: `${percentage}%` }} /></div></div>
      })}</div><p className="ia-small">{known} scored · {dimension.unknown || 0} Unknown · {dimension.errors || 0} failed · {dimension.pending || 0} pending</p>
      {onInspect && <div className="ia-summary-actions"><button className="ia-text-button" disabled={!low} onClick={() => onInspect({ kind: 'flagged', classifierId: dimension.id })}>Inspect low scores ({low})</button><button className="ia-text-button" disabled={!dimension.unknown} onClick={() => onInspect({ kind: 'uncertain', classifierId: dimension.id })}>Inspect Unknown scores ({dimension.unknown || 0})</button></div>}
      </article>
    })}</div><OriginalAssessment run={run} /></div>
  const summary = run.summary
  const generic = run.spec?.fixed_catalog_version === 'caliper_generic_items_v1'
  const active = ['preparing', 'generating', 'running'].includes(run.status)
  const hasFindings = !!summary?.classifiers.some(classifier => (classifier.valid_judgments ?? ((classifier.known || 0) + (classifier.unknown || 0))) > 0 || Object.values(classifier.counts || {}).some(count => count > 0))
  return <div className="ia-summary-findings">
    {active && <p className="ia-small">Summary statistics update when this classification phase finishes. Saved item judgments are available in step 4.</p>}
    {summary && hasFindings && !active && <>
      <div className="ia-section-heading"><h3>What the items show</h3><span className="ia-tag">{summary.complete_snapshot ? demo ? 'Full demo sample' : 'Full snapshot findings' : demo ? 'Demo pilot results' : run.scope === 'pilot' || run.status === 'checkpoint' ? 'Pilot results' : 'Partial results'}</span></div>
      <p className="ia-small">{demo ? 'Percentages describe all valid authored walkthrough judgments, including insufficient evidence, in this bundled sample only. They are not model outputs or estimates for the full MathDial benchmark. Operational failures and pending examples are excluded.' : generic ? 'Each distribution uses the saved valid judgments for that dimension, including insufficient evidence and judgments on partially classified items. Invalid responses, failed dimensions, and pending dimensions are excluded.' : 'Percentages describe model judgments among known labels. Unknowns, failures, and pending items are excluded.'}</p>
      <p className="ia-small">These findings describe the selected items. No issue identified is a bounded finding, not proof of benchmark validity. Human review is needed to check accuracy.</p>
      <div className="ia-distributions">{summary.classifiers.map(classifier => {
        const denominator = generic ? classifier.valid_judgments ?? ((classifier.known || 0) + (classifier.unknown || 0)) : classifier.known ?? 0
        const flags = (classifier.counts?.issue_identified || 0) + (classifier.counts?.no_match || 0) + (classifier.operation === 'flag' ? classifier.counts?.['1'] || 0 : 0)
        const uncertain = classifier.insufficient_evidence ?? classifier.unknown ?? classifier.counts?.insufficient_evidence ?? 0
        return <article key={classifier.id} className="ia-distribution">
          <h3>{classifierName(classifier.id, classifierNames)}</h3>
          <p className="ia-dimension-description">{DESCRIPTIONS[classifier.id] || classifier.question || classifier.criterion || 'Review this classifier’s saved judgments against its stated criterion.'}</p>
          {!classifier.applicable ? <p className="ia-small">Not applicable. {classifier.na_reason}</p> : <>
            <p className="ia-small">Percentages are out of <strong>{denominator.toLocaleString()} {generic ? 'valid judgments' : 'known labels'}</strong> for this dimension.</p>
            <p className="ia-small">{(classifier.determinate_judgments ?? classifier.known ?? 0).toLocaleString()} {generic ? 'sufficient evidence' : 'known labels'} · {uncertain.toLocaleString()} {generic ? 'insufficient evidence' : 'unknown'} · {(classifier.invalid || 0).toLocaleString()} invalid</p>
            <div className="ia-bars">{Object.entries(classifier.counts || {}).map(([label, count]) => {
              const pct = generic ? classifier.percentages_among_valid?.[label] : classifier.percentages_among_known?.[label]
              return <div className="ia-bar-row" key={label}><div className="ia-bar-label"><span>{labelName(classifier, label)}</span>
                <span>{count.toLocaleString()} <small>{pct == null ? '—' : `${pct.toFixed(1)}%`}</small></span></div>
                <div className="ia-bar-track" aria-hidden="true"><span style={{ width: `${pct || 0}%` }} /></div></div>
            })}</div>
            {onInspect && <div className="ia-summary-actions"><button type="button" className="ia-text-button" disabled={!flags} onClick={() => onInspect({ kind: 'flagged', classifierId: classifier.id })}>Inspect flagged items ({flags.toLocaleString()})</button>
              <button type="button" className="ia-text-button" disabled={!uncertain} onClick={() => onInspect({ kind: 'uncertain', classifierId: classifier.id })}>Inspect uncertain items ({uncertain.toLocaleString()})</button></div>}
            {classifier.category_counts && <details className="ia-category-counts"><summary>Required-category matches</summary><ul>{Object.entries(classifier.category_counts).map(([id, count]) => <li key={id}>{run.spec?.input_category_inventory?.categories.find(category => category.id === id)?.name || id}: {count}</li>)}</ul><p className="ia-small">An item may match multiple categories. These counts describe the selected items; they do not establish omitted categories in the full benchmark.</p></details>}
            <details className="ia-technical-details"><summary>Excluded processing counts</summary><p className="ia-small">{(classifier.errors || 0).toLocaleString()} failed · {(classifier.invalid || 0).toLocaleString()} invalid · {(classifier.pending || 0).toLocaleString()} pending</p></details>
          </>}
        </article>
      })}</div>
    </>}
    {!hasFindings && !active && <p className="ia-small">Label distributions will appear after the selected items have saved judgments. Preparing context alone does not produce item findings.</p>}
    <OriginalAssessment run={run} />
  </div>
}

export function ResultExports({ run, onDownload, onViewReport, onDownloadPackage, downloading, demo = false }: Pick<ResultsProps, 'run' | 'onDownload' | 'onViewReport' | 'onDownloadPackage' | 'downloading' | 'demo'>) {
  const sixScores = run.analysis_type === 'six_scores' || run.spec?.schema_version === 'caliper_item_context_v1'
  const active = ['preparing', 'generating', 'running'].includes(run.status)
  const exportsDisabled = downloading !== null || active || !run.summary
  return <div className="ia-export-results">
    <section className="ia-exports" aria-label="Save and share results"><h3>Save and share results</h3>
      <div className="ia-primary-exports">
        {onViewReport && <button type="button" className="ia-primary" onClick={onViewReport} disabled={exportsDisabled}>{downloading === 'view' ? 'Opening report…' : 'View report'}<span aria-hidden="true"> ↗</span></button>}
        {onDownloadPackage && <button type="button" className="ia-secondary" onClick={onDownloadPackage} disabled={exportsDisabled}>{downloading === 'package' ? 'Downloading…' : 'Download complete results package'}<span aria-hidden="true"> ↓</span></button>}
      </div>
      <p className="ia-small">{demo ? 'These files contain the bundled sample and authored example judgments. No live experiment package is created.' : 'View the readable report or keep the complete package for later review and team sharing. It includes the current saved results, including partial progress.'}</p>
      {active && <p className="ia-small">Downloads become available when the current processing phase stops or finishes.</p>}
      <details className="ia-individual-files"><summary>Individual files</summary><div>{ARTIFACTS.map(([artifact, label]) => <button key={artifact} type="button" className="ia-text-button"
        onClick={() => onDownload(artifact)} disabled={artifact === 'spec' ? downloading !== null || !run.spec : exportsDisabled}>{downloading === artifact ? 'Downloading…' : sixScores && artifact === 'items' ? 'Item scores CSV' : sixScores && artifact === 'spec' ? 'Shared context JSON' : label}<span aria-hidden="true"> ↓</span></button>)}</div></details>
    </section>
  </div>
}

/** Compatibility composition for the authored walkthrough and existing consumers. */
export function Results(props: ResultsProps) {
  return <section className="ia-results" aria-label="Analysis results">
    {props.run.summary && props.run.processed > 0 && <ProcessingCounts run={props.run} demo={props.demo} />}
    <ItemJudgments {...props} />
    <SummaryFindings run={props.run} demo={props.demo} classifierNames={props.classifierNames} />
    <DimensionAverages run={props.run} demo={props.demo} />
    <ResultExports {...props} />
  </section>
}
