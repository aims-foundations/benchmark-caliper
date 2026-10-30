import { useCallback, useEffect, useRef, useState, type KeyboardEvent } from 'react'
import { SiteHeader } from '../components/SiteHeader'
import { SiteFooter } from '../components/SiteFooter'
import { appPath } from '../paths'
import { getPublishedReviewPackage, type PackageDownloadProgress, type ScreenedItem } from './api'
import { ConstructionSteps } from './ConstructionSteps'
import { ConstructionItems } from './ConstructionItems'
import type { ConstructionComposition, ConstructionExample, ConstructionItemSummary, ConstructionSnapshot } from './constructionTypes'
import './ConstructionGallery.css'

export type { ConstructionComposition, ConstructionExample, ConstructionItemSummary, ConstructionSnapshot } from './constructionTypes'
const examplePath = (id: string) => `/api/item-review/examples/${encodeURIComponent(id)}`
export const constructionExampleLink = (id: string) => appPath(`/items?example=${encodeURIComponent(id)}`)
const selectedItemAnchor = (itemId: string) => `selected-item-${itemId}`

function CompositionSummary({ composition, selected }: { composition: ConstructionComposition; selected: ConstructionItemSummary[] }) {
  const { selected_count: count, sources, tasks, coverage, question_text: questions } = composition
  const representedTasks = tasks.filter(task => task.count > 0)
  const sourceAssignments = sources.reduce((sum, source) => sum + source.count, 0)
  const taskAssignments = tasks.reduce((sum, task) => sum + task.count, 0)
  return <section className="review-panel construction-composition" aria-labelledby="construction-composition">
    <h2 id="construction-composition">Composition of the selected items</h2>
    {count === 0 ? <p>No items were selected, so there is no selected collection to summarize.</p> : <>
      <p>This collection combines {sources.length} recorded source {sources.length === 1 ? 'benchmark' : 'benchmarks'} across {representedTasks.length} deployment {representedTasks.length === 1 ? 'task' : 'tasks'}.</p>
      <div className="construction-composition-tables">
        <div className="construction-table"><table><caption>Source benchmarks</caption><thead><tr><th scope="col">Benchmark</th><th scope="col">Selected items</th><th scope="col">Share</th></tr></thead><tbody>
          {sources.map(source => <tr key={source.name}><th scope="row">{source.name}</th><td>{source.count}</td><td>{source.percentage.toLocaleString(undefined, { maximumFractionDigits: 1 })}%</td></tr>)}
          {composition.unknown_source_count > 0 && <tr><th scope="row">Benchmark not recorded</th><td>{composition.unknown_source_count}</td><td>{(composition.unknown_source_count / count * 100).toLocaleString(undefined, { maximumFractionDigits: 1 })}%</td></tr>}
        </tbody></table></div>
        <div className="construction-table"><table><caption>Deployment tasks</caption><thead><tr><th scope="col">Task</th><th scope="col">Selected items</th></tr></thead><tbody>
          {tasks.map(task => <tr key={task.facet_id}><th scope="row"><a href={`#facet-${task.facet_id}`}>{task.label}</a></th><td>{task.count}</td></tr>)}
        </tbody></table></div>
      </div>
      {(sourceAssignments + composition.unknown_source_count > count || taskAssignments > count) && <p>An item can belong to more than one source benchmark or deployment task, so these counts can exceed the number of selected items. Source shares use all {count} selected items as the denominator.</p>}
      <details className="construction-composition-details"><summary>Inspect composition details</summary>
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
      </details>
    </>}
  </section>
}

async function publicJson<T>(path: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(appPath(path), { cache: 'no-store', signal })
  if (!response.ok) throw new Error(response.status === 404 ? 'These saved results are unavailable.' : 'The published results could not be loaded. Please try again.')
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
    <main className="rd-container construction-main review-workspace">
      <header className="construction-header">
        <nav className="construction-context" aria-label="Gallery navigation">
          <a href={appPath(exampleId ? '/items?gallery=1' : '/items')}>
            <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="m10 4-4 4 4 4" /></svg>
            {exampleId ? 'Benchmark gallery' : 'Benchmark construction'}
          </a>
          {exampleId && <a href={appPath('/items')}>Build a benchmark</a>}
        </nav>
        <h1>{snapshot?.entry.title ?? (exampleId ? 'Saved benchmark run' : 'Benchmark gallery')}</h1>
        <p className="construction-lead">{exampleId ? 'Review the selected questions and see how this collection was built.' : 'Browse saved benchmark runs, their selected items, and how each collection was built.'}</p>
      </header>
      {error && <p role="alert" className="review-error">{error}</p>}
      {!error && !snapshot && !examples && <p role="status">Loading published results…</p>}
      {examples && <section aria-label="Saved benchmark runs" className="construction-cards">
        {examples.length === 0 && <p>No benchmark runs have been published yet.</p>}
        {examples.map(entry => <article className="review-panel" key={entry.id}>
          <h2><a href={constructionExampleLink(entry.id)}>{entry.title}</a></h2>
          <p>{entry.description}</p>
          <dl className="construction-facts"><div><dt>Items assessed</dt><dd>{entry.assessed_count}</dd></div><div><dt>Items selected</dt><dd>{entry.selected_count}</dd></div></dl>
          <p>{entry.coverage_complete ? 'All stated coverage requirements were met.' : 'Some coverage requirements remain unmet.'}</p>
          <a href={constructionExampleLink(entry.id)}>View results</a>
        </article>)}
      </section>}
      {snapshot && <PublishedConstruction key={snapshot.entry.id} snapshot={snapshot} />}
    </main>
    <SiteFooter />
  </div>
}

type GalleryView = 'overview' | 'steps' | 'items'
type BrowsePhase = 'all' | 'initial' | 'adaptive'
type GalleryRoute = { view: GalleryView; step: number; phase: BrowsePhase | null; focusedItemId?: string; target?: string }
const views: { id: GalleryView; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'steps', label: 'How it was built' },
  { id: 'items', label: 'Browse items' },
]

function routeFromHash(hash: string): GalleryRoute {
  const route: GalleryRoute = { view: 'overview', step: 1, phase: null }
  let target: string
  try { target = decodeURIComponent(hash.replace(/^#/, '')) } catch { return route }
  const stage = /^construction-step-([1-7])$/.exec(target)
  if (stage) return { ...route, view: 'steps', step: Number(stage[1]), target }
  if (target.startsWith('facet-')) return { ...route, view: 'steps', step: 2, target }
  if (target.startsWith('original-answer-')) return { ...route, view: 'steps', step: 1, target }
  const item = /^(selected|screened)-item-(.+)$/.exec(target)
  if (item) return { ...route, view: 'items', phase: item[1] === 'screened' ? 'all' : null, focusedItemId: item[2] }
  if (target === 'items') return { ...route, view: 'items' }
  if (target === 'all-assessments') return { ...route, view: 'items', phase: 'all' }
  if (target === 'initial-assessments') return { ...route, view: 'items', phase: 'initial' }
  if (target === 'adaptive-assessments') return { ...route, view: 'items', phase: 'adaptive' }
  return route
}

function Outcome({ snapshot, navigate }: { snapshot: ConstructionSnapshot; navigate: (hash: string) => void }) {
  const { entry, review, items, composition } = snapshot
  const selection = review.selection
  const quotas = selection?.quota_coverage ?? []
  const unresolvedQuotas = quotas.filter(quota => quota.shortfall == null || quota.shortfall > 0)
  const selected = (selection?.selected_item_ids ?? []).flatMap(id => items.find(item => item.item_id === id) ?? [])
  return <div className="construction-overview">
    <section className="review-panel construction-outcome" aria-labelledby="construction-outcome">
      <h2 id="construction-outcome">The final collection</h2>
      <p className="construction-goal">{review.deployment.task}</p>
      <p>{review.adaptive?.stop_reason === 'candidate_limit'
        ? `Construction stopped at the limit of ${review.adaptive.settings.candidate_limit} screened candidates.`
        : review.adaptive?.stop_reason === 'queues_exhausted' ? 'Construction stopped when the saved candidate queues were exhausted.'
          : review.adaptive?.stop_reason === 'cost_limit' ? 'Construction stopped at the configured cost limit.' : review.message}</p>
      {unresolvedQuotas.length > 0 && <div className="construction-coverage-note"><h3>Additional coverage is still needed</h3>
        {unresolvedQuotas.map(quota => <p key={quota.requirement_index}><span className="review-preserve">{review.requirements?.coverage_requirements[quota.requirement_index]?.requirement.text ?? `Coverage requirement ${quota.requirement_index + 1}`}</span>{' '}
          <strong>{quota.minimum_items == null ? `${quota.selected_count} qualifying items.` : `${quota.selected_count} of ${quota.minimum_items} required items.`} {quota.shortfall == null ? 'Coverage remains unresolved.' : `${quota.shortfall} more are needed.`}</strong>
        </p>)}
      </div>}
      {!entry.coverage_complete && unresolvedQuotas.length === 0 && <p>Some recorded coverage requirements remain unmet. Step 7 contains the final coverage findings.</p>}
      {entry.coverage_complete && <p>The selected items meet all recorded coverage requirements.</p>}
      <div className="construction-actions"><button type="button" onClick={() => navigate('construction-step-1')}>See how this collection was built</button><button type="button" className="secondary" onClick={() => navigate('items')}>Browse selected questions</button></div>
    </section>
    {composition && <CompositionSummary composition={composition} selected={selected} />}
  </div>
}

function RunSummary({ snapshot }: { snapshot: ConstructionSnapshot }) {
  const { entry, review } = snapshot
  const selection = review.selection
  const requiredTasks = selection?.task_coverage.filter(task => task.minimum > 0) ?? []
  const covered = requiredTasks.filter(task => task.selected_count >= task.minimum).length
  const averageQuality = selection && selection.selected_count > 0
    ? selection.total_quality / selection.selected_count : null
  return <section className="construction-run-summary" aria-label="Final collection summary">
    <dl className="construction-facts">
      <div><dt>Items selected</dt><dd>{entry.selected_count}{selection && <span> / {selection.limit}</span>}</dd></div>
      <div><dt>Average quality Q</dt><dd>{averageQuality == null ? 'Not available' : <>{averageQuality.toFixed(2)} <span>/ 5</span></>}</dd></div>
      <div><dt>Candidates assessed</dt><dd>{entry.assessed_count}</dd></div>
      <div><dt>Required tasks covered</dt><dd>{selection ? <>{covered} <span>/ {requiredTasks.length}</span></> : 'Not recorded'}</dd></div>
    </dl>
    <details className="construction-quality-note"><summary>About quality Q</summary>
      <p>Each item’s quality Q is the mean of its input ontology, input content, input form, and output ontology ratings. Average quality Q is the mean across the final selected items and describes their fit to the deployment.</p>
    </details>
  </section>
}

function PublishedConstruction({ snapshot }: { snapshot: ConstructionSnapshot }) {
  const { entry, review } = snapshot
  const [route, setRoute] = useState(() => routeFromHash(window.location.hash))
  const [loadedItems, setLoadedItems] = useState(() => new Map(review.screening?.items.map(item => [item.item_id, item])))
  const onLoad = useCallback((item: ScreenedItem) => setLoadedItems(previous => new Map(previous).set(item.item_id, item)), [])
  const [progress, setProgress] = useState<PackageDownloadProgress | null>(null)
  const [downloadError, setDownloadError] = useState('')
  const [copyMessage, setCopyMessage] = useState('')
  const downloadController = useRef<AbortController | null>(null)
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([])
  useEffect(() => () => downloadController.current?.abort(), [])

  const navigate = useCallback((hash: string) => {
    if (window.location.hash !== `#${hash}`) window.history.pushState(null, '', `#${hash}`)
    setRoute(routeFromHash(`#${hash}`))
  }, [])
  useEffect(() => {
    const sync = () => setRoute(routeFromHash(window.location.hash))
    function followEvidence(event: MouseEvent) {
      const anchor = event.target instanceof Element ? event.target.closest('a[href^="#"]') : null
      if (!anchor?.closest('.construction-main') || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return
      event.preventDefault()
      navigate(anchor.getAttribute('href')!.slice(1))
    }
    window.addEventListener('hashchange', sync)
    window.addEventListener('popstate', sync)
    document.addEventListener('click', followEvidence)
    return () => { window.removeEventListener('hashchange', sync); window.removeEventListener('popstate', sync); document.removeEventListener('click', followEvidence) }
  }, [navigate])
  useEffect(() => {
    if (!route.target) return
    const target = /^construction-step-[1-7]$/.test(route.target)
      ? document.querySelector('.construction-process')
      : document.getElementById(route.target)
    if (target instanceof HTMLDetailsElement) target.open = true
    for (let parent = target?.parentElement; parent; parent = parent.parentElement) if (parent instanceof HTMLDetailsElement) parent.open = true
    target?.scrollIntoView?.({ block: 'start' })
  }, [route])

  function selectView(view: GalleryView) { navigate(view === 'steps' ? `construction-step-${route.step}` : view === 'items' ? 'items' : 'overview') }
  function tabKey(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const next = event.key === 'ArrowRight' ? (index + 1) % views.length : event.key === 'ArrowLeft' ? (index + views.length - 1) % views.length : event.key === 'Home' ? 0 : event.key === 'End' ? views.length - 1 : null
    if (next == null) return
    event.preventDefault(); selectView(views[next].id); tabRefs.current[next]?.focus()
  }
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
    catch { setCopyMessage('Copy this page’s address from your browser to share these results.') }
  }

  return <>
    <RunSummary snapshot={snapshot} />
    <div className="construction-toolbar">
      <div className="construction-view-tabs" role="tablist" aria-label="Explore this benchmark run">{views.map((view, index) => <button key={view.id} ref={element => { tabRefs.current[index] = element }} id={`gallery-tab-${view.id}`} role="tab" type="button" aria-selected={route.view === view.id} aria-controls={`gallery-panel-${view.id}`} tabIndex={route.view === view.id ? 0 : -1} onClick={() => selectView(view.id)} onKeyDown={event => tabKey(event, index)}>{view.label}</button>)}</div>
      <div className="construction-sharing">
        <details className="construction-downloads"><summary>Download results<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="m4 6 4 4 4-4" /></svg></summary><div>
          {entry.artifacts.summary_report && <a href={artifactUrl('summary_report')} target="_blank" rel="noopener noreferrer">Read the report with composition summary</a>}
          <a href={artifactUrl('items')} download={entry.artifacts.items.filename}>Download selected items CSV</a>
          <a href={artifactUrl('results')} download={entry.artifacts.results.filename}>Download complete JSON</a>
          <a href={artifactUrl('report')} target="_blank" rel="noopener noreferrer">Read the original HTML report</a>
          <button type="button" disabled={progress !== null} onClick={() => void download()}>{progress?.phase === 'downloading' ? `Downloading original package… ${Math.floor(progress.receivedBytes / progress.totalBytes * 100)}%` : progress ? 'Preparing original package…' : 'Download original results package'}</button>
          <p>The original package contains the files saved when this run finished. The report with composition summary includes the later descriptive summary.</p>
        </div></details>
        <button type="button" className="construction-copy-link" onClick={() => void copyLink()}>Copy link</button>
      </div>
    </div>
    {downloadError && <p className="review-error" role="alert">{downloadError}</p>}{copyMessage && <p role="status">{copyMessage}</p>}
    {views.map(view => <div key={view.id} id={`gallery-panel-${view.id}`} role="tabpanel" aria-labelledby={`gallery-tab-${view.id}`} hidden={route.view !== view.id} tabIndex={0} className="construction-view-panel">
      {route.view === view.id && (view.id === 'overview' ? <Outcome snapshot={snapshot} navigate={navigate} />
        : view.id === 'steps' ? <ConstructionSteps snapshot={snapshot} step={route.step} onStepChange={step => navigate(`construction-step-${step}`)} />
          : <ConstructionItems snapshot={snapshot} loadedItems={loadedItems} onLoad={onLoad} initialPhase={route.phase} focusedItemId={route.focusedItemId} />)}
    </div>)}
  </>
}
