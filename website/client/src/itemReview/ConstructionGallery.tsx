import { useCallback, useEffect, useRef, useState, type ReactNode } from 'react'
import { SiteHeader } from '../components/SiteHeader'
import { SiteFooter } from '../components/SiteFooter'
import { appPath } from '../paths'
import { DIMENSIONS, getPublishedReviewPackage, type AdaptiveReview, type PackageDownloadProgress, type PreparedPackage, type ScreenedItem, type ScreeningRating, type SelectionReview } from './api'
import { DeploymentAnswers, RequirementsContent } from './RequirementsResults'
import { GroundingContent } from './GroundingResults'
import { PIPELINE_STEPS } from './StepSection'
import './ConstructionGallery.css'

type Artifact = { filename: string; bytes: number; sha256?: string }
export interface ConstructionExample {
  id: string; title: string; description: string; run_id: string; result_state: string
  assessed_count: number; selected_count: number; coverage_complete: boolean
  artifacts: { report: Artifact; summary_report?: Artifact; items: Artifact; results: Artifact; package: Artifact & PreparedPackage }
}
export interface ConstructionItemSummary {
  item_id: string; index: number; question_preview: string; status: 'complete' | 'error'
  gate: 'pass' | 'fail' | 'unresolved' | null; matched_facet_ids: string[]; sources: string[]
  selected: boolean; initial: boolean; quality_score: number | null
}
export interface ConstructionComposition {
  selected_count: number
  sources: { name: string; count: number; percentage: number }[]
  unknown_source_count: number
  tasks: { facet_id: string; label: string; count: number }[]
  coverage: { requirement_index: number; label: string; minimum_items: number | null; selected_count: number; shortfall: number | null }[]
  question_text: { available_count: number; distinct_count: number; missing_count: number; overlaps: { item_ids: string[] }[] }
  formats: { counts: { label: string; count: number }[]; unknown_count: number; basis: string | null }
}
export interface ConstructionSnapshot { entry: ConstructionExample; review: AdaptiveReview; items: ConstructionItemSummary[]; composition?: ConstructionComposition }
const examplePath = (id: string) => `/api/item-review/examples/${encodeURIComponent(id)}`
export const constructionExampleLink = (id: string) => appPath(`/items?example=${encodeURIComponent(id)}`)
const selectedItemAnchor = (itemId: string) => `selected-item-${itemId}`

function CompositionSummary({ composition, selected }: { composition: ConstructionComposition; selected: ConstructionItemSummary[] }) {
  const { selected_count: count, sources, tasks, formats, coverage, question_text: questions } = composition
  const representedTasks = tasks.filter(task => task.count > 0)
  const sourceAssignments = sources.reduce((sum, source) => sum + source.count, 0)
  const taskAssignments = tasks.reduce((sum, task) => sum + task.count, 0)
  return <section className="review-panel construction-composition" aria-labelledby="construction-composition">
    <h2 id="construction-composition">Composition of the selected items</h2>
    {count === 0 ? <p>No items were selected, so there is no selected collection to summarize.</p> : <>
      <p>The selected collection draws on {sources.length} recorded source {sources.length === 1 ? 'benchmark' : 'benchmarks'} and represents {representedTasks.length} deployment {representedTasks.length === 1 ? 'task' : 'tasks'}. Question format is a separate property; a composite collection can contain multiple choice questions.</p>
      <div className="construction-composition-tables">
        <div className="construction-table"><table><caption>Source benchmarks</caption><thead><tr><th scope="col">Source</th><th scope="col">Selected items</th><th scope="col">Share</th></tr></thead><tbody>
          {sources.map(source => <tr key={source.name}><th scope="row">{source.name}</th><td>{source.count}</td><td>{source.percentage.toLocaleString(undefined, { maximumFractionDigits: 1 })}%</td></tr>)}
          {composition.unknown_source_count > 0 && <tr><th scope="row">Source not recorded</th><td>{composition.unknown_source_count}</td><td>{(composition.unknown_source_count / count * 100).toLocaleString(undefined, { maximumFractionDigits: 1 })}%</td></tr>}
        </tbody></table></div>
        <div className="construction-table"><table><caption>Deployment tasks</caption><thead><tr><th scope="col">Task</th><th scope="col">Selected items</th></tr></thead><tbody>
          {tasks.map(task => <tr key={task.facet_id}><th scope="row"><a href={`#facet-${task.facet_id}`}>{task.label}</a></th><td>{task.count}</td></tr>)}
        </tbody></table></div>
      </div>
      {(sourceAssignments + composition.unknown_source_count > count || taskAssignments > count) && <p>An item can belong to more than one source benchmark or deployment task, so these counts can exceed the number of selected items. Source shares use all {count} selected items as the denominator.</p>}
      <h3>Question formats</h3>
      {formats.counts.length > 0 && <ul>{formats.counts.map(format => <li key={format.label}>{format.label}: {format.count} {format.count === 1 ? 'item' : 'items'}.</li>)}</ul>}
      {formats.unknown_count > 0 && <p>{formats.unknown_count} selected {formats.unknown_count === 1 ? 'item has' : 'items have'} no reviewed format annotation.</p>}
      {formats.basis && <p>Format review: {formats.basis}</p>}
      <h3>Additional coverage requirements</h3>
      {coverage.length === 0 ? <p>No additional coverage requirements were recorded.</p> : <ul>{coverage.map(requirement => <li key={requirement.requirement_index}><span className="review-preserve">{requirement.label}</span>{' '}
        {requirement.minimum_items == null ? `${requirement.selected_count} qualifying ${requirement.selected_count === 1 ? 'item' : 'items'}. No numeric minimum was specified.` : `${requirement.selected_count} qualifying ${requirement.selected_count === 1 ? 'item' : 'items'} against a minimum of ${requirement.minimum_items}.`}{' '}
        {requirement.shortfall == null ? 'The coverage finding remains unresolved.' : requirement.shortfall > 0 ? `${requirement.shortfall} more ${requirement.shortfall === 1 ? 'item is' : 'items are'} needed.` : 'This requirement is met.'}
      </li>)}</ul>}
      <h3>Question text overlap</h3>
      <p>{questions.missing_count === 0 ? `${count} selected ${count === 1 ? 'row contains' : 'rows contain'} ${questions.distinct_count} distinct question ${questions.distinct_count === 1 ? 'text' : 'texts'} after normalizing whitespace.` : `${questions.available_count} of ${count} selected rows have question text available, with ${questions.distinct_count} distinct question ${questions.distinct_count === 1 ? 'text' : 'texts'} after normalizing whitespace. ${questions.missing_count} ${questions.missing_count === 1 ? 'row could' : 'rows could'} not be compared.`}</p>
      {questions.overlaps.length > 0 && <ul>{questions.overlaps.map((overlap, index) => <li key={index}>Same question text: {overlap.item_ids.map((id, itemIndex) => {
        const selectedIndex = selected.findIndex(item => item.item_id === id)
        return <span key={id}>{itemIndex > 0 && ', '}{selectedIndex >= 0 ? <a href={`#${encodeURIComponent(selectedItemAnchor(id))}`}>Selected item {selectedIndex + 1}</a> : 'Item unavailable'}</span>
      })}.</li>)}</ul>}
      <p>The comparison keeps wording, punctuation, and letter case. It does not measure whether differently worded questions test the same content.</p>
      <p>This text comparison does not change the whole row identity rule used during selection.</p>
    </>}
  </section>
}

async function publicJson<T>(path: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(appPath(path), { cache: 'no-store', signal })
  if (!response.ok) throw new Error(response.status === 404 ? 'This published example is unavailable.' : 'The published results could not be loaded. Please try again.')
  return response.json()
}

export function ConstructionGallery({ exampleId }: { exampleId?: string }) {
  const [examples, setExamples] = useState<ConstructionExample[] | null>(null)
  const [snapshot, setSnapshot] = useState<ConstructionSnapshot | null>(null)
  const [error, setError] = useState('')
  useEffect(() => {
    const controller = new AbortController()
    setError(''); setSnapshot(null); setExamples(null)
    const load = exampleId
      ? publicJson<ConstructionSnapshot>(examplePath(exampleId), controller.signal).then(result => { if (!controller.signal.aborted) setSnapshot(result) })
      : publicJson<{ examples: ConstructionExample[] }>('/api/item-review/examples', controller.signal).then(result => { if (!controller.signal.aborted) setExamples(result.examples) })
    load.catch(problem => { if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'The published results could not be loaded.') })
    return () => controller.abort()
  }, [exampleId])

  return <div className="rd-root item-review-site construction-gallery">
    <SiteHeader />
    <header className="item-review-hero"><div className="rd-container">
      <a className="review-back" href={appPath(exampleId ? '/items?gallery=1' : '/items')}>{exampleId ? 'All benchmark examples' : 'Return to benchmark construction'}</a>
      <p className="eyebrow">Benchmark construction examples</p>
      <h1>{snapshot?.entry.title ?? (exampleId ? 'Published benchmark example' : 'From deployment goals to benchmark items')}</h1>
      <p className="construction-lead">{snapshot?.entry.description ?? 'Explore completed runs, inspect the evidence behind each selection, and follow the results through the construction pipeline.'}</p>
      <a href={appPath('/items')}>Build a benchmark for your deployment</a>
    </div></header>
    <main className="rd-container construction-main review-workspace">
      {error && <p role="alert" className="review-error">{error}</p>}
      {!error && !snapshot && !examples && <p role="status">Loading published results…</p>}
      {examples && <section aria-label="Published benchmark examples" className="construction-cards">
        {examples.length === 0 && <p>No benchmark examples have been published yet.</p>}
        {examples.map(entry => <article className="review-panel" key={entry.id}>
          <h2><a href={constructionExampleLink(entry.id)}>{entry.title}</a></h2>
          <p>{entry.description}</p>
          <dl className="construction-facts"><div><dt>Items assessed</dt><dd>{entry.assessed_count}</dd></div><div><dt>Items selected</dt><dd>{entry.selected_count}</dd></div></dl>
          <p>{entry.coverage_complete ? 'All stated coverage requirements were met.' : 'Some coverage requirements remain unmet.'}</p>
          <a href={constructionExampleLink(entry.id)}>Explore this example</a>
        </article>)}
      </section>}
      {snapshot && <PublishedConstruction key={snapshot.entry.id} snapshot={snapshot} />}
    </main>
    <SiteFooter />
  </div>
}

function Coverage({ review, selection }: { review: AdaptiveReview; selection: SelectionReview['selection'] }) {
  if (!selection) return <p>No selection was recorded for this stage.</p>
  const taskName = (id: string) => review.requirements?.task_facets.find(facet => facet.facet_id === id)?.task.text ?? id
  return <>
    <div className="construction-table"><table><caption>Task coverage</caption><thead><tr><th scope="col">Task</th><th scope="col">Required</th><th scope="col">Selected</th><th scope="col">Shortfall</th></tr></thead><tbody>
      {selection.task_coverage.map(task => <tr key={task.facet_id}><th scope="row"><a href={`#facet-${task.facet_id}`}>{taskName(task.facet_id)}</a></th><td>{task.minimum}</td><td>{task.selected_count}</td><td>{task.shortfall}</td></tr>)}
    </tbody></table></div>
    <h3>Additional coverage requirements</h3>
    {selection.quota_coverage.length === 0 && <p>No additional numeric coverage requirements were recorded.</p>}
    {selection.quota_coverage.map(quota => <section className="construction-quota" key={quota.requirement_index}>
      <p className="review-preserve">{review.requirements?.coverage_requirements[quota.requirement_index]?.requirement.text}</p>
      <dl className="construction-facts"><div><dt>Required</dt><dd>{quota.minimum_items ?? 'Unresolved'}</dd></div><div><dt>Selected</dt><dd>{quota.selected_count}</dd></div><div><dt>Shortfall</dt><dd>{quota.shortfall ?? 'Unresolved'}</dd></div></dl>
    </section>)}
    {!selection.fully_satisfied && <><h3>Remaining coverage gaps</h3><ul>
      {selection.task_coverage.filter(task => task.shortfall > 0).map(task => <li key={task.facet_id}>{taskName(task.facet_id)} needs {task.shortfall} more selected {task.shortfall === 1 ? 'item' : 'items'}.</li>)}
      {selection.quota_coverage.filter(quota => quota.shortfall == null || quota.shortfall > 0).map(quota => <li key={quota.requirement_index}>Coverage requirement {quota.requirement_index + 1} {quota.shortfall == null ? 'remains unresolved.' : `needs ${quota.shortfall} more selected ${quota.shortfall === 1 ? 'item' : 'items'}.`}</li>)}
    </ul></>}
    {selection.gaps.length > 0 && <details><summary>Original coverage findings</summary><ul>{selection.gaps.map((gap, index) => <li className="review-preserve" key={index}>{gap}</li>)}</ul></details>}
  </>
}

function Evidence({ finding }: { finding: Pick<ScreeningRating, 'justification' | 'evidence' | 'information_gaps'> }) {
  return <><p className="review-preserve">{finding.justification}</p>
    {finding.evidence.length > 0 && <><h5>Model provided item evidence</h5><ul>{finding.evidence.map((passage, index) => <li className="review-preserve" key={index}>{passage}</li>)}</ul></>}
    {finding.information_gaps.length > 0 && <><h5>Information gaps</h5><ul>{finding.information_gaps.map((gap, index) => <li className="review-preserve" key={index}>{gap}</li>)}</ul></>}
  </>
}

function FullAssessment({ item, review }: { item: ScreenedItem; review: AdaptiveReview }) {
  const assessment = item.assessment
  return <div className="construction-assessment-body">
    <h4>Original item</h4><p className="review-preserve">{item.question_text || 'No separately labeled question is recorded. Inspect the complete original row below.'}</p>
    {item.status === 'error' ? <p className="review-error">{item.error}</p> : assessment && <>
      <h4>Task actually tested</h4><p className="review-preserve">{assessment.task.decision}</p>
      <p><strong>Task match:</strong> {assessment.task.status === 'matched' ? 'Matched' : assessment.task.status === 'no_match' ? 'No deployment task matched' : 'Unresolved'}</p>
      {assessment.task.matched_facet_ids.length > 0 && <ul>{assessment.task.matched_facet_ids.map(id => <li key={id}><a href={`#facet-${id}`}>{review.requirements?.task_facets.find(facet => facet.facet_id === id)?.task.text ?? id}</a></li>)}</ul>}
      <Evidence finding={assessment.task} />
      <h4>Screening decision</h4><ul>{item.gate?.reasons.map((reason, index) => <li className="review-preserve" key={index}>{reason}</li>)}</ul>
      <dl className="screening-ratings">{DIMENSIONS.map(([key, label]) => <div key={key}><dt>{label}</dt><dd>{assessment.ratings[key].score == null ? 'Unknown' : `${assessment.ratings[key].score} / 5`}</dd></div>)}</dl>
      <details><summary>Six rating explanations and evidence</summary>{DIMENSIONS.map(([key, label]) => <section key={key}><h4>{label}</h4><Evidence finding={assessment.ratings[key]} /></section>)}</details>
      <details><summary>Coverage findings ({assessment.coverage.length})</summary>{assessment.coverage.map(finding => <section key={finding.requirement_index}><h4>Coverage requirement {finding.requirement_index + 1}: {finding.satisfied == null ? 'Unresolved' : finding.satisfied ? 'Satisfied' : 'Not satisfied'}</h4><p className="review-preserve">{review.requirements?.coverage_requirements[finding.requirement_index]?.requirement.text}</p><Evidence finding={finding} /></section>)}</details>
    </>}
    <details><summary>Complete original row and provenance</summary><h4>Original row</h4><pre>{JSON.stringify(item.evidence, null, 2)}</pre><h4>Sources and acquisition</h4><pre>{JSON.stringify({ item_id: item.item_id, sources: item.sources, acquisition: item.acquisition, evidence_hash: item.evidence_hash }, null, 2)}</pre><h4>Full assessment record</h4><pre>{JSON.stringify(item, null, 2)}</pre></details>
  </div>
}

function GalleryItem({ summary, item, review, exampleId, onLoad, label = 'Screened item', anchorId }: { summary: ConstructionItemSummary; item?: ScreenedItem; review: AdaptiveReview; exampleId: string; onLoad: (item: ScreenedItem) => void; label?: string; anchorId?: string }) {
  const [open, setOpen] = useState(false)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  useEffect(() => {
    if (!open || item) return
    const controller = new AbortController()
    setError('')
    publicJson<ScreenedItem>(`${examplePath(exampleId)}/items/${encodeURIComponent(summary.item_id)}`, controller.signal)
      .then(result => { if (!controller.signal.aborted) onLoad(result) })
      .catch(problem => { if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'This item could not be loaded.') })
    return () => controller.abort()
  }, [open, item, summary.item_id, exampleId, onLoad, attempt])
  const decision = summary.status === 'error' ? 'Assessment error' : summary.gate === 'pass' ? 'Passed screening' : summary.gate === 'fail' ? 'Failed screening' : 'Unresolved screening'
  return <details className="construction-item" id={anchorId} onToggle={event => setOpen(event.currentTarget.open)}>
    <summary><span className="construction-item-label">{label} {summary.index + 1}{summary.selected && <span className="construction-selected">Selected</span>}</span><strong>{summary.question_preview || 'Item with no separately labeled question'}</strong><span className="construction-item-meta">{decision}. Sources: {summary.sources.join(', ')}.{summary.quality_score != null && ` Quality: ${summary.quality_score.toFixed(2)} / 5.`}</span></summary>
    {open && (item ? <FullAssessment item={item} review={review} /> : error ? <div className="construction-assessment-body"><p role="alert">{error}</p><button type="button" onClick={() => setAttempt(value => value + 1)}>Try loading this item again</button></div> : <p role="status">Loading the full item and assessment…</p>)}
  </details>
}

function GalleryStage({ number, children }: { number: number; children: ReactNode }) {
  const step = PIPELINE_STEPS[number - 1]
  return <details className="construction-stage" id={`construction-step-${number}`}><summary><h2>Step {number}: {step.name}</h2><span>{step.description}</span></summary><div className="construction-stage-body">{children}</div></details>
}

function PublishedConstruction({ snapshot }: { snapshot: ConstructionSnapshot }) {
  const { entry, review, items } = snapshot
  const [loadedItems, setLoadedItems] = useState(() => new Map(review.screening?.items.map(item => [item.item_id, item])))
  const onLoad = useCallback((item: ScreenedItem) => setLoadedItems(previous => new Map(previous).set(item.item_id, item)), [])
  const [filter, setFilter] = useState('all')
  const [phase, setPhase] = useState('all')
  const [page, setPage] = useState(1)
  const [progress, setProgress] = useState<PackageDownloadProgress | null>(null)
  const [downloadError, setDownloadError] = useState('')
  const [copyMessage, setCopyMessage] = useState('')
  const downloadController = useRef<AbortController | null>(null)
  useEffect(() => () => downloadController.current?.abort(), [])
  useEffect(() => {
    function revealTarget(hash: string) {
      let id: string
      try { id = decodeURIComponent(hash.slice(1)) } catch { return }
      const target = document.getElementById(id)
      if (target instanceof HTMLDetailsElement) target.open = true
      for (let parent = target?.parentElement; parent; parent = parent.parentElement) if (parent instanceof HTMLDetailsElement) parent.open = true
      return target
    }
    function reveal() {
      const target = revealTarget(window.location.hash)
      target?.scrollIntoView?.({ block: 'start' })
    }
    function click(event: MouseEvent) {
      const anchor = event.target instanceof Element ? event.target.closest('a[href^="#"]') : null
      if (anchor && event.button === 0 && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey) {
        revealTarget(anchor.getAttribute('href')!)
      }
    }
    window.addEventListener('hashchange', reveal); document.addEventListener('click', click); reveal()
    return () => { window.removeEventListener('hashchange', reveal); document.removeEventListener('click', click) }
  }, [])
  const filtered = items.filter(item => (phase === 'all' || (phase === 'initial') === item.initial) && (filter === 'all' || (filter === 'selected' ? item.selected : filter === 'error' ? item.status === 'error' : item.gate === filter)))
  const pages = Math.max(1, Math.ceil(filtered.length / 10))
  const selected = review.selection?.selected_item_ids.flatMap(id => { const item = items.find(summary => summary.item_id === id); return item ? [item] : [] }) ?? []
  const initial = items.filter(item => item.initial)
  const adaptive = review.adaptive
  const artifactUrl = (name: string) => appPath(`${examplePath(entry.id)}/artifacts/${name}`)
  async function download() {
    if (downloadController.current) return
    const controller = new AbortController(); downloadController.current = controller
    setDownloadError(''); setProgress({ phase: 'downloading', receivedBytes: 0, totalBytes: entry.artifacts.package.bytes })
    try {
      const result = await getPublishedReviewPackage(entry.id, entry.artifacts.package, update => { if (!controller.signal.aborted) setProgress(update) }, controller.signal)
      if (controller.signal.aborted) return
      const url = URL.createObjectURL(result.blob)
      const link = document.createElement('a'); link.href = url; link.download = result.filename; link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (problem) { if (!controller.signal.aborted) setDownloadError(problem instanceof Error ? problem.message : 'The package download was interrupted. Please try again.') }
    finally { if (downloadController.current === controller) { downloadController.current = null; if (!controller.signal.aborted) setProgress(null) } }
  }
  async function copyLink() {
    try { await navigator.clipboard.writeText(new URL(constructionExampleLink(entry.id), window.location.origin).href); setCopyMessage('Link copied.') }
    catch { setCopyMessage('Copy this page’s address from your browser to share the example.') }
  }
  function showInitial() { setFilter('all'); setPhase('initial'); setPage(1) }

  return <>
    <section className="review-panel" aria-labelledby="construction-outcome"><p className="eyebrow">Completed construction</p><h2 id="construction-outcome">The final collection</h2>
      <dl className="construction-facts"><div><dt>Items assessed</dt><dd>{entry.assessed_count}</dd></div><div><dt>Items selected</dt><dd>{entry.selected_count} / {review.selection?.limit ?? 30}</dd></div><div><dt>Required tasks</dt><dd>{review.requirements?.task_facets.length ?? 0}</dd></div><div><dt>Average quality Q</dt><dd>{review.selection?.selected_count ? (review.selection.total_quality / review.selection.selected_count).toFixed(2) : 'Not available'}</dd></div></dl>
      <p>{adaptive?.frozen ? 'The collection is frozen. ' : ''}{adaptive?.stop_reason === 'candidate_limit' ? `Construction stopped at the budget of ${adaptive.settings.candidate_limit} screened candidates.` : adaptive?.stop_reason === 'queues_exhausted' ? 'Construction stopped when the candidate queues were exhausted.' : adaptive?.stop_reason === 'cost_limit' ? 'Construction stopped at the configured cost limit.' : ''}</p>
      <p>Quality Q summarizes fit to the deployment using the mean of the four screening gate ratings: input ontology, input content, input form, and output ontology. It is not a score for the target system.</p>
      <p>Human validation is not included in this saved record.</p>
      <p>{entry.coverage_complete ? 'The selected collection meets all recorded coverage requirements.' : 'The collection covers the tasks shown below, with remaining coverage gaps recorded explicitly.'}</p>
      <Coverage review={review} selection={review.selection} />
      <div className="construction-actions">{entry.artifacts.summary_report && <a href={artifactUrl('summary_report')} target="_blank" rel="noopener noreferrer">Read the report with composition summary</a>}<a href={artifactUrl('report')} target="_blank" rel="noopener noreferrer">Read the original HTML report</a><a href={artifactUrl('items')} download={entry.artifacts.items.filename}>Download selected items CSV</a><a href={artifactUrl('results')} download={entry.artifacts.results.filename}>Download complete JSON</a><button type="button" disabled={progress !== null} onClick={() => void download()}>{progress?.phase === 'downloading' ? `Downloading original package… ${Math.floor(progress.receivedBytes / progress.totalBytes * 100)}%` : 'Download original results package'}</button><button type="button" className="secondary" onClick={() => void copyLink()}>Copy example link</button></div>
      {entry.artifacts.summary_report && <p>The composition summary is available in the gallery and the report with composition summary. The original results package retains the files saved when this run finished.</p>}
      {downloadError && <p className="review-error" role="alert">{downloadError}</p>}{copyMessage && <p role="status">{copyMessage}</p>}
    </section>
    {snapshot.composition && <CompositionSummary composition={snapshot.composition} selected={selected} />}
    <section aria-labelledby="construction-selected"><h2 id="construction-selected">Selected items ({selected.length})</h2><p>Open an item to read the original question, its ratings, supporting evidence, and source record.</p>
      {selected.map((item, index) => <GalleryItem key={item.item_id} summary={{ ...item, index }} item={loadedItems.get(item.item_id)} review={review} exampleId={entry.id} onLoad={onLoad} label="Selected item" anchorId={selectedItemAnchor(item.item_id)} />)}
    </section>
    <section className="review-panel" id="all-assessments" aria-labelledby="construction-assessments"><h2 id="construction-assessments">All screened items ({items.length})</h2><p>Inspect accepted and rejected candidates, including the initial screening batch and later adaptive batches.</p>
      <div className="construction-filters"><label>Screening result<select value={filter} onChange={event => { setFilter(event.target.value); setPage(1) }}><option value="all">All results</option><option value="selected">Selected items</option><option value="pass">Passed screening</option><option value="fail">Failed screening</option><option value="unresolved">Unresolved screening</option><option value="error">Assessment errors</option></select></label><label>Screening stage<select value={phase} onChange={event => { setPhase(event.target.value); setPage(1) }}><option value="all">All stages</option><option value="initial">Initial screening</option><option value="adaptive">Adaptive screening</option></select></label></div>
      <p role="status">{filtered.length} matching items. Page {page} of {pages}.</p>
      {filtered.slice((page - 1) * 10, page * 10).map(item => <GalleryItem key={item.item_id} summary={item} item={loadedItems.get(item.item_id)} review={review} exampleId={entry.id} onLoad={onLoad} />)}
      {filtered.length === 0 && <p>No items match these filters.</p>}
      <nav className="review-pagination" aria-label="Screened item pages"><button type="button" className="secondary" disabled={page === 1} onClick={() => setPage(value => value - 1)}>Previous items</button><span>Page {page} of {pages}</span><button type="button" className="secondary" disabled={page >= pages} onClick={() => setPage(value => value + 1)}>Next items</button></nav>
    </section>
    <section aria-labelledby="construction-stages"><h2 id="construction-stages">Follow the construction pipeline</h2><p>Open each stage to inspect its results, from the final adaptive screening back to the original deployment answers.</p>
      <GalleryStage number={7}><p>{adaptive?.stop_reason === 'candidate_limit' ? 'Construction stopped when the screening budget was reached.' : adaptive?.stop_reason === 'queues_exhausted' ? 'Construction stopped when no unseen candidates remained in the queues.' : adaptive?.stop_reason === 'cost_limit' ? 'Construction stopped at the configured cost limit.' : review.message}</p><p>{items.filter(item => !item.initial).length} additional items were screened after the initial batch.</p>
        <div className="construction-table"><table><caption>Screening batches</caption><thead><tr><th>Batch</th><th>Stage</th><th>Items acquired</th><th>Collection size</th></tr></thead><tbody>{adaptive?.batches.map(batch => <tr key={batch.number}><td>{batch.number}</td><td>{batch.kind === 'initial' ? 'Initial screening' : 'Adaptive screening'}</td><td>{batch.item_ids.length}</td><td>{batch.selected_item_ids.length}</td></tr>)}</tbody></table></div>
        <details><summary>Adaptive settings, queue statistics, and batch records</summary><pre>{JSON.stringify({ settings: adaptive?.settings, policy: adaptive?.policy, queue_statistics: adaptive?.queue_statistics, batches: adaptive?.batches }, null, 2)}</pre></details>
      </GalleryStage>
      <GalleryStage number={6}><p>This is the collection selected after the initial screening, before adaptive screening added further evidence.</p><p>{adaptive?.initial_selection ? `${adaptive.initial_selection.selected_count} items were selected at this stage.` : 'The original selection snapshot is not available in this record.'}</p><Coverage review={review} selection={adaptive?.initial_selection ?? null} /></GalleryStage>
      <GalleryStage number={5}><p>{initial.length} candidates were allocated to the initial screening. {initial.filter(item => item.status === 'complete').length} have valid assessments.</p><p>{initial.filter(item => item.gate === 'pass').length} passed screening. {initial.filter(item => item.gate === 'fail').length} failed screening. {initial.filter(item => item.status === 'error').length} have assessment errors.</p><a href="#all-assessments" onClick={showInitial}>Inspect the initial screening items</a><details><summary>Initial allocation, screening prompt, and output schema</summary><pre>{JSON.stringify({ allocation: review.screening?.allocation, policy: review.screening?.policy, model: review.screening?.model }, null, 2)}</pre></details></GalleryStage>
      <GalleryStage number={4}><p>Benchmark candidates were retrieved for each task and organized into screening queues.</p><p>{review.retrieval?.scope.table_count.toLocaleString()} benchmark collections. {review.retrieval?.scope.source_rows.toLocaleString()} source rows.</p>{review.retrieval?.queries.map((query, index) => <section key={query.facet_id}><h3>Task {index + 1} search query</h3><p className="review-preserve">{query.query}</p><p>{query.candidate_count ?? 'Unknown'} retrieved candidates.</p></section>)}<details><summary>Retrieval settings, bank snapshot, and task queues</summary><pre>{JSON.stringify(review.retrieval, null, 2)}</pre></details></GalleryStage>
      <GalleryStage number={3}><GroundingContent review={review} /></GalleryStage>
      <GalleryStage number={2}><RequirementsContent requirements={review.requirements} /></GalleryStage>
      <GalleryStage number={1}><DeploymentAnswers deployment={review.deployment} /></GalleryStage>
    </section>
  </>
}
