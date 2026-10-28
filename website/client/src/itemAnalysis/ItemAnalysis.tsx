import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react'
import { SiteHeader } from '../components/SiteHeader'
import { SiteFooter } from '../components/SiteFooter'
import { appPath } from '../paths'
import * as api from './api'
import { SixScoreWorkflow, isSixScoreRun } from './SixScoreWorkflow'
import { PreparedContext } from './PreparedContext'
import { ContextValidation } from './ContextValidation'
import { ItemJudgments, ProcessingCounts, ResultExports, SummaryFindings, type ItemFilter } from './Results'
import { ITEM_STEPS, PipelineNavigation, StageSection } from './PipelineStages'
import { useItemInspection } from './useItemInspection'
import { BenchmarkConfirmation } from './BenchmarkConfirmation'
import { assessmentStorageKey, clearStoredValue, restoreAccess, saveAccess } from './accessStorage'
import { saveBlob, viewReport } from './downloads'
import type { AnalysisRun, Artifact, AssessmentReference, AssessmentSetup, AssessmentSource, Catalog, ConfirmedDataset, DirectContext, Example, RunAccess, RunScope, SpecificationMode } from './types'
import './itemAnalysis.css'

const ACTIVE_STATUSES = ['preparing', 'generating', 'running']
const FILE_NAMES: Record<Artifact, string> = { spec: 'classifier_spec.json', items: 'items.csv', summary: 'summary.json', report: 'report.html', review: 'review.csv' }

function KeyInput({ value, onChange }: { value: string; onChange: (key: string) => void }) {
  return <div className="ia-key"><label className="ia-field"><span>OpenAI API key</span>
    <input type="password" autoComplete="off" spellCheck={false} maxLength={512} placeholder="sk-…" value={value} onChange={event => onChange(event.target.value)} required />
  </label><p className="ia-small">Used for paid model calls. Kept in memory for this tab; re-enter it after a refresh.</p></div>
}

function DatasetSource({ example }: { example: Example }) {
  if (!example.source_url && !example.source_revision) return null
  return <p className="ia-dataset-source">
    {example.source_url && <a href={example.source_url} target="_blank" rel="noreferrer">View dataset on Hugging Face ↗</a>}
    {example.source_revision && <span>Snapshot <code title={example.source_revision}>{example.source_revision.slice(0, 12)}</code></span>}
  </p>
}

interface Props {
  assessment?: AssessmentReference
  directContext?: DirectContext
  initialSetup?: AssessmentSetup
  onEditContext?: () => void
  onStatusChange?: (status: 'pending' | 'in_progress' | 'complete') => void
}

export function ItemAnalysis(props: Props) {
  return <AnalysisView key={props.assessment ? `${props.assessment.kind}:${props.assessment.id}` : 'legacy'} {...props} />
}

function AnalysisView({ assessment, directContext, initialSetup, onEditContext, onStatusChange }: Props) {
  const storageKey = assessmentStorageKey(assessment)
  const [catalog, setCatalog] = useState<Catalog | null>(null)
  const [setup, setSetup] = useState<AssessmentSetup | null>(initialSetup || null)
  const [confirmedDataset, setConfirmedDataset] = useState<ConfirmedDataset | null>(null)
  const [exampleId, setExampleId] = useState('')
  const [mode, setMode] = useState<SpecificationMode>('generate')
  const [apiKey, setApiKey] = useState('')
  const [access, setAccess] = useState<RunAccess | null>(() => restoreAccess(storageKey))
  const [run, setRun] = useState<AnalysisRun | null>(null)
  const [page, setPage] = useState(1)
  const [pageLoading, setPageLoading] = useState(false)
  const [busy, setBusy] = useState(false)
  const [starting, setStarting] = useState(false)
  const [startDelayed, setStartDelayed] = useState(false)
  const [error, setError] = useState('')
  const [errorFocusVersion, setErrorFocusVersion] = useState(0)
  const [pollError, setPollError] = useState('')
  const [pollVersion, setPollVersion] = useState(0)
  const [catalogVersion, setCatalogVersion] = useState(0)
  const [downloading, setDownloading] = useState<Artifact | 'package' | 'view' | null>(null)
  const [discardRequested, setDiscardRequested] = useState(false)
  const [privacyOpen, setPrivacyOpen] = useState(false)
  const [pilotReviewed, setPilotReviewed] = useState(false)
  const [viewedStep, setViewedStep] = useState<number | null>(null)
  const [filter, setFilter] = useState<ItemFilter>({ kind: 'all' })
  const [selectionPreview, setSelectionPreview] = useState<{ count: number | null; title: string }>({ count: null, title: '' })
  const onSelectionChange = useCallback((source: AssessmentSource | null, file: File | null) => {
    setSelectionPreview({ count: source?.item_count ?? null, title: source?.title || file?.name || '' })
  }, [])
  const requestedPage = filter.kind === 'all' ? page : 1
  useEffect(() => { setViewedStep(null) }, [run?.status])
  const progressRef = useRef<HTMLDivElement>(null)
  const errorRef = useRef<HTMLDivElement>(null)
  const focusStartedRun = useRef(false)
  const direct = assessment?.kind === 'direct'

  useEffect(() => {
    if (!starting) return
    const timer = setTimeout(() => setStartDelayed(true), 15000)
    return () => clearTimeout(timer)
  }, [starting])

  useEffect(() => {
    if (!focusStartedRun.current || !progressRef.current) return
    focusStartedRun.current = false
    progressRef.current.focus({ preventScroll: true })
    progressRef.current.scrollIntoView({ block: 'start' })
  }, [run?.run_id])

  useEffect(() => {
    if (!errorFocusVersion || !errorRef.current) return
    errorRef.current.focus({ preventScroll: true })
    errorRef.current.scrollIntoView({ block: 'start' })
  }, [errorFocusVersion])

  function showRequestError(message: string) {
    setError(message)
    setErrorFocusVersion(value => value + 1)
  }

  useEffect(() => {
    if (assessment) return
    const controller = new AbortController()
    api.getCatalog(controller.signal).then(value => {
      if (controller.signal.aborted) return
      setCatalog(value)
      // Keep MMLU visible even when server access needs attention; never silently
      // replace the real benchmark with the small teaching example.
      setExampleId(current => current || value.examples.find(example => example.id === 'mmlu')?.id || value.examples[0]?.id || '')
      setError('')
    }).catch(problem => { if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'Could not load the benchmarks.') })
    return () => controller.abort()
  }, [catalogVersion, assessment?.kind, assessment?.id])

  useEffect(() => {
    if (!assessment || access || setup) return
    const controller = new AbortController()
    const request = directContext ? api.getDirectSetup(directContext, '', controller.signal) : api.getAssessment(assessment, controller.signal)
    request.then(value => {
      if (controller.signal.aborted) return
      if (value.assessment.kind !== assessment.kind || value.assessment.id !== assessment.id) {
        throw new api.AnalysisApiError('The context has changed. Edit the context to start a new item analysis.', 409)
      }
      setSetup(value)
    }).catch(problem => {
      if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'Could not load the benchmark assessment.')
    })
    return () => controller.abort()
  }, [assessment?.kind, assessment?.id, access, catalogVersion, setup, directContext])

  useEffect(() => {
    const complete = run?.status === 'complete' && run.total > 0 && run.complete === run.total && run.errors === 0
    onStatusChange?.(complete ? 'complete' : access ? 'in_progress' : 'pending')
  }, [access, run?.status, run?.total, run?.complete, run?.errors, onStatusChange])

  useEffect(() => {
    if (!access) return
    const controller = new AbortController()
    let timer: ReturnType<typeof setTimeout> | undefined
    let failures = 0
    setPageLoading(true)
    async function poll() {
      try {
        const latest = await api.getRun(access!, requestedPage, controller.signal)
        if (controller.signal.aborted) return
        if (assessment && (latest.assessment?.kind !== assessment.kind || latest.assessment.id !== assessment.id)) {
          throw new api.AnalysisApiError('This item analysis belongs to another assessment.', 409)
        }
        setRun(latest)
        setPollError('')
        setPageLoading(false)
        failures = 0
        if (ACTIVE_STATUSES.includes(latest.status)) timer = setTimeout(() => void poll(), 1000)
      } catch (problem) {
        if (controller.signal.aborted) return
        setPageLoading(false)
        failures += 1
        const expired = problem instanceof api.AnalysisApiError && [401, 403, 404, 409, 410].includes(problem.status)
        setPollError(expired ? 'This run is no longer available. Start a new analysis to continue.' :
          failures < 3 ? 'Connection interrupted. Reconnecting to your run…' : 'Could not reconnect. Your run may still be processing; retry to check its progress.')
        if (!expired && failures < 3) timer = setTimeout(() => void poll(), failures * 2000)
      }
    }
    void poll()
    return () => { controller.abort(); if (timer) clearTimeout(timer) }
  }, [access, requestedPage, pollVersion, assessment?.kind, assessment?.id])

  async function start(event: FormEvent) {
    event.preventDefault()
    const selected = catalog?.examples.find(entry => entry.id === exampleId)
    if (busy) return
    if (assessment) {
      if (!setup || !confirmedDataset) return
    } else if (!selected?.available) return
    setBusy(true)
    setStarting(true)
    setStartDelayed(false)
    setError('')
    try {
      const result = directContext
        ? await api.createDirectRun(directContext, confirmedDataset!)
        : assessment
        ? await api.createAssessmentRun(assessment, confirmedDataset!)
        : await api.createRun(exampleId, 'generate', '')
      if (assessment && (result.assessment?.kind !== assessment.kind || result.assessment.id !== assessment.id)) {
        throw new api.AnalysisApiError('The returned item analysis does not match this context. Confirm the context again.', 409)
      }
      const nextAccess = { run_id: result.run_id, run_secret: result.run_secret }
      // Persist only the run's access token. API keys never enter browser storage.
      saveAccess(storageKey, nextAccess)
      focusStartedRun.current = true
      setRun(result)
      setPage(1)
      setAccess(nextAccess)
    } catch (problem) {
      showRequestError(problem instanceof Error ? problem.message : 'Could not start this analysis.')
      if (assessment && problem instanceof api.AnalysisApiError && problem.status === 409) {
        setConfirmedDataset(null)
        setSetup(null)
        setCatalogVersion(value => value + 1)
      }
    }
    finally { setBusy(false); setStarting(false) }
  }

  async function classify(scope: RunScope) {
    if (!access || !apiKey.trim() || busy) return
    if (!isSixScoreRun(run) && direct && scope === 'all' && !pilotReviewed) return
    setFilter({ kind: 'all' })
    setViewedStep(null)
    setBusy(true)
    setError('')
    try {
      setRun(await (!isSixScoreRun(run) && direct && scope === 'all'
        ? api.classify(access, scope, apiKey.trim(), pilotReviewed)
        : api.classify(access, scope, apiKey.trim())))
      setPage(1)
      setPollVersion(value => value + 1)
    } catch (problem) { showRequestError(problem instanceof Error ? problem.message : 'Could not start classification.') }
    finally { setBusy(false) }
  }

  async function stop() {
    if (!access || busy) return
    setBusy(true)
    try {
      setRun(await api.cancelRun(access))
      setError('')
      setPage(1)
      setPollVersion(value => value + 1)
    } catch { showRequestError('Could not confirm the stop. Try again; the run may still be processing.') }
    finally { setBusy(false) }
  }

  function reset() {
    clearStoredValue(storageKey)
    setAccess(null)
    setRun(null)
    setApiKey('')
    setConfirmedDataset(null)
    setSetup(null)
    setError('')
    setPollError('')
    setPage(1)
    setPilotReviewed(false)
    setDiscardRequested(false)
    setViewedStep(null)
    setFilter({ kind: 'all' })
    focusStartedRun.current = false
  }

  async function discard() {
    if (!access || busy) return
    setBusy(true)
    try {
      await api.discardRun(access)
      reset()
      if (direct) onEditContext?.()
    } catch (problem) { showRequestError(problem instanceof Error ? problem.message : 'Could not discard this analysis. Your saved results remain available.') }
    finally { setBusy(false) }
  }

  async function download(artifact: Artifact) {
    if (!access || downloading) return
    setDownloading(artifact)
    try {
      const blob = await api.download(access, artifact)
      saveBlob(blob, FILE_NAMES[artifact])
    } catch (problem) { showRequestError(problem instanceof Error ? problem.message : 'Could not download this file.') }
    finally { setDownloading(null) }
  }

  async function openReport() {
    if (!access || downloading) return
    setDownloading('view')
    try { await viewReport(() => api.download(access, 'report')) }
    catch (problem) { showRequestError(problem instanceof Error ? problem.message : 'Could not open the report.') }
    finally { setDownloading(null) }
  }

  async function downloadPackage() {
    if (!access || downloading) return
    setDownloading('package')
    try {
      const result = await api.downloadPackage(access)
      saveBlob(result.blob, result.filename)
    } catch (problem) { showRequestError(problem instanceof Error ? problem.message : 'Could not download the results package.') }
    finally { setDownloading(null) }
  }

  const example = run?.example || catalog?.examples.find(value => value.id === exampleId)
  const active = !!run && ACTIVE_STATUSES.includes(run.status)
  useEffect(() => {
    if (active && filter.kind !== 'all') { setFilter({ kind: 'all' }); setPage(1) }
  }, [active, filter.kind])
  const datasetCount = run && run.total > 0 ? run.total : assessment ? selectionPreview.count : example?.item_count ?? null
  const pilotSize = Math.min(setup?.checkpoint_size || catalog?.checkpoint_size || 100, datasetCount || 100)
  const canClassify = !!run?.spec && !active && !pollError && ['ready', 'checkpoint', 'cancelled', 'failed'].includes(run.status)
  const scope: RunScope = run?.can_continue ? 'all' : 'pilot'
  const remaining = run ? Math.max(0, (scope === 'all' ? run.total : pilotSize) - run.complete) : pilotSize
  const classifierCount = run?.spec?.classifiers.filter(classifier => classifier.applicable).length || 4
  const remainingRequests = run?.remaining_judgments?.[scope] ?? remaining * classifierCount
  const target = run?.scope === 'all' || run?.status === 'complete' ? run.total : pilotSize
  const selectedComplete = !!run?.spec && !active && run.complete === target && run.errors === 0
  const pilotComplete = selectedComplete && run?.scope === 'pilot'
  const fullComplete = !!run?.spec && !active && run.total > 0 && run.complete === run.total && run.errors === 0
  const findingsReady = !!run?.summary && run.processed > 0 && !active
  const dataConfirmed = !!access || (assessment ? !!confirmedDataset : !!example?.available)
  const validationFailure = !run?.spec && run?.failure?.stage === 'specification'
  const automaticStep = !access ? assessment && dataConfirmed ? 2 : 1 : !run ? 1
    : ['preparing', 'generating'].includes(run.status) ? 2 : !run.spec ? validationFailure ? 3 : 2
    : run.status === 'ready' ? 3 : selectedComplete || (findingsReady && run.status === 'checkpoint') ? 5 : 4
  const currentStep = viewedStep ?? automaticStep
  const statuses = [
    dataConfirmed ? !assessment && !access ? 'Dataset selected' : 'Confirmed' : 'Needs confirmation',
    run?.spec ? 'Context saved' : run && ['preparing', 'generating'].includes(run.status) ? 'Preparing' : run?.status === 'failed' ? 'Needs attention' : 'Not started',
    run?.spec ? 'Checks passed · interpretation unreviewed' : validationFailure ? 'Needs attention' : 'Waiting for context',
    pilotComplete ? 'Pilot complete' : fullComplete ? 'Full dataset classified' : run?.status === 'running' ? 'Classifying' : run?.processed ? 'Partial results saved' : run?.spec ? 'Ready to start' : 'Waiting for specification',
    findingsReady ? 'Findings available' : active && run?.processed ? 'Updates when classification pauses' : 'Waiting for judgments',
    run?.spec ? active ? 'Exports after phase ends' : 'Export available' : 'Waiting for results',
  ]
  const inspection = useItemInspection(access, run, filter, pilotSize)
  function navigate(step: number) {
    setViewedStep(step)
    requestAnimationFrame(() => {
      const section = document.getElementById(`ia-step-${step}`)
      section?.focus({ preventScroll: true })
      section?.scrollIntoView({ block: 'start', behavior: 'auto' })
    })
  }
  function inspect(nextFilter: ItemFilter) {
    setFilter(nextFilter)
    setPage(1)
    navigate(4)
  }
  const nextLink = (step: number, label: string) => <button type="button" className="ia-text-button" onClick={() => navigate(step)}>{label} →</button>
  const runMessage = run?.status === 'failed' ? run.failure?.message || run.error || run.message : run?.message
  const classificationMessage = pilotComplete
    ? `Pilot complete: ${run!.complete.toLocaleString()}/${target.toLocaleString()} selected items classified.`
    : fullComplete ? `Full dataset classified: ${run!.complete.toLocaleString()}/${run!.total.toLocaleString()} items in the prepared snapshot.`
    : run?.status === 'running' ? `Classifying ${run.scope === 'all' ? 'the full prepared dataset' : 'the selected pilot'}. Completed judgments are saved as they arrive.`
    : run?.processed ? `Classification paused: ${run.complete.toLocaleString()}/${target.toLocaleString()} selected items fully classified. Saved judgments are retained.`
    : 'No item judgments have been produced yet.'

  const contextContent = <>        {!(assessment ? setup : catalog) && !access && !error && <p role="status">{assessment ? 'Connecting your benchmark assessment…' : 'Loading benchmarks…'}</p>}
        {run ? <><h3>{run.example.title}</h3>{run.example.assessment_title && <p className="ia-small">Assessment context: {run.example.assessment_title}</p>}
          <dl className="ia-data-facts"><div><dt>Benchmark</dt><dd>{run.example.benchmark}</dd></div><div><dt>Deployment</dt><dd>{run.example.deployment}</dd></div></dl>
          <p className="ia-small">{run.example.source_label}</p><details className="ia-technical-details"><summary>Dataset source and snapshot metadata</summary><p>{run.example.description}</p><DatasetSource example={run.example} /></details></>
          : assessment && setup ? <><h3>{setup.assessment.benchmark_name || setup.assessment.benchmark}</h3>
            <p><strong>Deployment:</strong> {setup.assessment.deployment}</p>
            {directContext && <details className="ia-context"><summary>Original task and answer requirements</summary><p><strong>Task:</strong> {directContext.task_requirements}</p><p><strong>Answer:</strong> {directContext.answer_requirements}</p></details>}
            <fieldset className="ia-linked-controls" disabled={busy}><BenchmarkConfirmation assessment={assessment} setup={setup} directContext={directContext} confirmed={confirmedDataset}
              onSelectionChange={onSelectionChange} onConfirm={dataset => { setConfirmedDataset(dataset); if (dataset) setError('') }} /></fieldset></>
          : catalog && <><label className="ia-field"><span>Benchmark and assessment context</span><select value={exampleId} onChange={event => { setExampleId(event.target.value); setMode('generate') }}>
            {catalog.examples.map(entry => <option key={entry.id} value={entry.id}>{entry.title}{!entry.available ? ' — unavailable' : ''}</option>)}</select></label>
            {example && <><p><strong>Deployment:</strong> {example.deployment}</p><p className="ia-small">{example.description}</p><details className="ia-technical-details"><summary>Dataset source and snapshot metadata</summary><p>{example.source_label}</p><DatasetSource example={example} /></details></>}
            {example && !example.available && <><p className="ia-error">{example.unavailable_reason || 'This dataset is not available on the server yet.'}</p><p className="ia-small">Dataset access is managed by the website. No Hugging Face key is needed from visitors.</p></>}</>}
        <dl className="ia-sample-facts"><div><dt>{run?.scope ? 'Selected sample' : !run || isSixScoreRun(run) ? 'Optional pilot' : 'Planned pilot'}</dt><dd>{run?.scope ? `${target.toLocaleString()} items · ${run.scope === 'all' ? 'full prepared dataset' : 'pilot'}` : datasetCount == null ? `Up to ${pilotSize} items, once the file is prepared` : `${pilotSize.toLocaleString()} items`}</dd></div>
          <div><dt>Full dataset size (prepared snapshot)</dt><dd>{datasetCount == null ? 'Available after preparation for uploaded files; see source details for a catalog selection.' : `${datasetCount.toLocaleString()} items`}</dd></div></dl>
        {selectionPreview.title && !run && <p className="ia-small">Selected source: {selectionPreview.title}</p>}
        <p className="ia-small">The full dataset here means the loaded snapshot or uploaded file. It may be a subset of the published benchmark. Findings apply to the selected items.</p></>
  const requestErrors = (error || pollError) && <div className="ia-error ia-request-error" role="alert" ref={errorRef} tabIndex={-1}><p>{error || pollError}</p>
    {!(assessment ? setup || access : catalog) && <button className="ia-secondary" onClick={() => { setError(''); setCatalogVersion(value => value + 1) }}>Retry loading context</button>}
    {pollError && <div className="ia-actions"><button className="ia-secondary" onClick={() => setPollVersion(value => value + 1)}>Retry connection</button><button className="ia-secondary" onClick={reset}>Start a new analysis</button></div>}
  </div>
  if (!run || isSixScoreRun(run)) return <div className={assessment ? 'item-analysis-site ia-embedded' : 'rd-root item-analysis-site'}>
    {!assessment && <SiteHeader />}
    <section id={assessment ? 'item-analysis' : undefined} className={assessment ? 'ia-main' : 'rd-container ia-main'} aria-label="Item analysis">
      <div className="ia-integrated-heading"><p className="ia-eyebrow">Item-level analysis</p><h2>Six scores for every item</h2>
        <p>Use your deployment context to assess each item across Input Ontology, Content, and Form, and Output Ontology, Content, and Form.</p>
        {direct && <p className="ia-assessment-not-run"><strong>Benchmark assessment: Not run.</strong> Item scores use your deployment requirements.</p>}
        {onEditContext && <button className="ia-text-button" disabled={busy || active} onClick={onEditContext}>Edit context and start again</button>}
      </div>
      {run && <div ref={progressRef} tabIndex={-1} role="region" aria-label="Run progress"><p className="ia-small">{run.message}</p></div>}
      {access && !run ? <>{requestErrors}<p role="status">Restoring your saved analysis…</p>
        <p className="ia-small">Starting again replaces this browser’s shortcut without deleting saved server results. If the previous analysis is still running, starting again does not stop it.</p>
        {!pollError && <button type="button" className="ia-secondary" disabled={busy} onClick={reset}>Start a new analysis</button>}
      </> : <SixScoreWorkflow run={run} context={contextContent} canPrepare={dataConfirmed && !access} onPrepare={() => void start({ preventDefault() {} } as FormEvent)}
        busy={busy} starting={starting} startDelayed={startDelayed} apiKey={apiKey} onKeyChange={setApiKey} pilotSize={pilotSize} canAnalyze={canClassify} onAnalyze={scope => void classify(scope)} onStop={() => void stop()}
        page={page} setPage={setPage} pageLoading={pageLoading} filter={filter} onFilterChange={next => { setFilter(next); setPage(1) }} filteredItems={filter.kind === 'all' ? undefined : inspection.items}
        filterLoading={inspection.loading} inspectionError={inspection.error} retryInspection={inspection.retry} onDownload={artifact => void download(artifact)} onViewReport={() => void openReport()}
        onDownloadPackage={() => void downloadPackage()} downloading={downloading} errors={requestErrors} management={<>
          <p className="ia-small">Saved results can be reopened in this browser. Download a package to keep a separate copy.</p>
          <details className="ia-source"><summary>Run metadata and usage</summary><p>Run: {run?.run_id}</p>{run?.model && <p>Model: {run.model.model_id}</p>}<p>{run?.usage?.input_tokens || 0} input tokens · {run?.usage?.output_tokens || 0} output tokens</p></details>
          <details className="ia-source"><summary>Manage this saved analysis</summary><p>Starting again removes this browser’s shortcut. Download the results first to keep a copy.</p>
            <button className="ia-text-button" disabled={busy || active} onClick={reset}>Start a new analysis</button><button className="ia-text-button" disabled={busy || active} onClick={() => setDiscardRequested(true)}>Discard saved analysis</button>
            {discardRequested && <div role="group" aria-label="Confirm discard"><p>Delete this analysis and its saved files from the server?</p><button className="ia-secondary" disabled={busy} onClick={() => void discard()}>Delete analysis permanently</button><button className="ia-text-button" onClick={() => setDiscardRequested(false)}>Keep analysis</button></div>}
          </details>
        </>} />}
      <details className="ia-privacy" id="item-analysis-privacy" open={privacyOpen} onToggle={event => setPrivacyOpen(event.currentTarget.open)}><summary>About your key and item data</summary><p>Your API key stays in memory and is never saved to browser storage. A private run token lets you return to saved results. Source items, shared context, and scores are saved on the server.</p></details>
    </section>
    {!assessment && <SiteFooter onPrivacyClick={() => { setPrivacyOpen(true); document.getElementById('item-analysis-privacy')?.scrollIntoView?.({ block: 'center' }) }} />}
  </div>

  return <div className={assessment ? 'item-analysis-site ia-embedded' : 'rd-root item-analysis-site'}>
    {!assessment && <><SiteHeader />
      <header className="ia-hero"><div className="rd-container"><a className="ia-back" href={appPath('/')}>← Benchmark Caliper</a>
        <div className="ia-hero-row"><div><p className="ia-eyebrow">Item-level analysis</p><h1>From context<br />to item findings.</h1></div>
          <p>Follow the six steps below. Review a pilot, inspect the evidence, and keep a record for independent human review.</p></div></div></header></>}
    <section id={assessment ? 'item-analysis' : undefined} className={assessment ? 'ia-main' : 'rd-container ia-main'} aria-label="Item analysis">
      {assessment && <div className="ia-integrated-heading"><p className="ia-eyebrow">{direct ? 'Starting from your requirements' : 'Continuing your benchmark assessment'}</p><h2>Item analysis</h2>
        <p>Follow the data, prepared context, Python checks, and four item judgments into summary findings. A completed pilot can be reviewed and exported; classifying the remaining dataset is optional.</p>
        {direct && <p className="ia-assessment-not-run"><strong>Benchmark assessment: Not run.</strong> This path uses your requirements and does not produce benchmark-level validity scores.</p>}
        {onEditContext && <button type="button" className="ia-text-button" disabled={busy || active} onClick={onEditContext}>Edit context and start again</button>}
      </div>}
      <aside className="ia-historical-analysis" aria-labelledby="ia-historical-title">
        <h3 id="ia-historical-title">You reopened an earlier item analysis</h3>
        <p>This saved run keeps its original pipeline and results format. New analyses use six scores per item and three steps: Context &amp; items, Analyze, and Results.</p>
        <p className="ia-small">Download the results package in step 6 before starting again to keep a copy. Starting again replaces this browser’s shortcut without deleting the saved analysis from the server.</p>
        {active && <p>Stop this analysis before starting a new one. Completed results stay saved.</p>}
        <div className="ia-actions">
          {active && <button type="button" className="ia-secondary" disabled={busy} onClick={() => void stop()}>Stop this analysis</button>}
          <button type="button" className="ia-primary" disabled={busy || active} onClick={reset}>Start a new six-score analysis</button>
        </div>
      </aside>
      <PipelineNavigation current={currentStep} statuses={statuses} onNavigate={navigate} />
      {(error || pollError) && <div className="ia-error ia-request-error" role="alert" ref={errorRef} tabIndex={-1}><p>{error || pollError}</p>
        {!(assessment ? setup || access : catalog) && <button className="ia-secondary" onClick={() => { setError(''); setCatalogVersion(value => value + 1) }}>{assessment ? 'Retry loading assessment' : 'Retry loading benchmarks'}</button>}
        {pollError && <div className="ia-actions"><button className="ia-secondary" onClick={() => setPollVersion(value => value + 1)}>Retry connection</button><button className="ia-secondary" onClick={reset}>Start a new analysis</button></div>}
      </div>}
      <div className="ia-current-view" ref={progressRef} tabIndex={-1} role="region" aria-label="Run progress">
        <p className="ia-eyebrow">Current step {currentStep} of 6</p><h2>{ITEM_STEPS[currentStep - 1]}</h2>
        {access && !run && !pollError && <p role="status">Restoring your saved analysis…</p>}
        {run && <p className="ia-small">Saved results remain available when you pause. Viewing a step does not start model calls or mark human review complete.</p>}
      </div>

      <StageSection step={1} current={currentStep} status={statuses[0]} initiallyOpen={!run}
        purpose="Confirm which benchmark items and deployment this analysis will describe."
        input="Benchmark assessment or deployment requirements, and a dataset source or upload."
        output={dataConfirmed ? 'The confirmed dataset and deployment, with a pilot planned before any optional full-dataset run.' : 'A confirmed dataset and deployment, ready for context preparation.'}
        next={dataConfirmed ? nextLink(2, 'Prepare or review classifier context') : 'Review the source and confirm the dataset below before preparing context.'}>
        {contextContent}
      </StageSection>

      <StageSection step={2} current={currentStep} status={statuses[1]} initiallyOpen={!run?.spec}
        purpose="Prepare the deployment-specific context that the four fixed classifiers will use."
        input="Confirmed deployment requirements, benchmark evidence, and dataset profile."
        output={run?.spec ? 'Saved requirements, category definitions, four context blocks, sources, and evidence gaps.' : 'Requirements, category definitions, four context blocks, sources, and evidence gaps will appear here.'}
        next={run?.spec ? nextLink(3, 'Review Python checks and the resulting specification') : dataConfirmed ? 'Prepare the context below, then review the generated interpretation and its evidence.' : nextLink(1, 'Confirm the data first')}>
        {!access && dataConfirmed && <form className="ia-prepare-form" onSubmit={start}><fieldset className="ia-linked-controls" disabled={busy}>
          {!assessment && <fieldset className="ia-mode"><legend>Classification criteria</legend>
            <label><input type="radio" name="specification" checked={mode === 'generate'} onChange={() => setMode('generate')} /><span><strong>Prepare with GPT-6 Luna</strong><small>Organize sourced context for the four fixed rubric classifiers.</small></span></label>
            <label><input type="radio" name="specification" checked={mode === 'provided'} disabled={example?.supplied_spec_available === false} onChange={() => setMode('provided')} /><span><strong>Use supplied criteria</strong><small>{example?.supplied_spec_available === false ? 'No supplied context is available. Prepare sourced context from its assessment to continue.' : 'Inspect the supplied specification without a model call.'}</small></span></label></fieldset>}
          {(assessment || mode === 'generate') && <KeyInput value={apiKey} onChange={setApiKey} />}
          <button className="ia-primary" type="submit" disabled={busy || (!!assessment || mode === 'generate') && !apiKey.trim()}>{busy ? 'Starting…' : assessment ? 'Prepare classifier context' : mode === 'generate' ? 'Prepare context with GPT-6 Luna' : 'Load supplied criteria'}<span aria-hidden="true"> →</span></button>
          {starting && <p className="ia-start-status" role="status">{startDelayed ? 'Still waiting for the server to confirm this run. We’ll show progress here when it responds.' : 'Starting item analysis. Waiting for the server to confirm your run…'}</p>}
          <p className="ia-small">{!assessment && mode === 'provided' ? 'Loading supplied criteria makes no paid calls.' : 'Preparing context starts paid model calls. Item classification begins separately in step 4.'}</p>
        </fieldset></form>}
        {run && !run.spec && <><p role="status" className={run.status === 'failed' ? 'ia-error' : ''}>{validationFailure && ['invalid_json', 'schema', 'evidence', 'deployment', 'provenance', 'task_grounding'].includes(run.failure?.code || '') ? 'Context preparation did not produce an accepted specification. The reported validation issue is in step 3.' : runMessage}</p>
          {['preparing', 'generating'].includes(run.status) && <><progress aria-label="Context preparation in progress" /><button type="button" className="ia-secondary" disabled={busy} onClick={() => void stop()}>Stop analysis</button></>}
          {run.failure && <details className="ia-technical-details"><summary>Preparation error reference</summary><code>{run.failure.stage}/{run.failure.code}</code></details>}</>}
        {run?.spec && <PreparedContext spec={run.spec} metadata={run.summary?.specification} direct={direct} />}
        {!run && !dataConfirmed && <p>Context preparation becomes available after you confirm the data and deployment.</p>}
      </StageSection>

      <StageSection step={3} current={currentStep} status={statuses[2]} initiallyOpen={!run?.processed}
        purpose="Understand the automatic checks and review the specification accepted for classification."
        input="Prepared context, frozen source records, and the four fixed classifier definitions."
        output={run?.spec ? 'An accepted classifier specification. Scientific correctness has not been established.' : 'An accepted specification or a reported preparation issue; no verdict is available yet.'}
        next={run?.spec ? nextLink(4, 'Review the context, then start item classification') : validationFailure ? 'Inspect the reported issue and return to context preparation. Start a new analysis if the inputs need revision.' : 'Wait for context preparation; Python checks run automatically.'}>
        {run ? <ContextValidation run={run} /> : <p>Python checks required structure, source references, run consistency, and the fixed classifier definitions after preparation. Passing these checks does not establish scientific correctness.</p>}
      </StageSection>

      <StageSection step={4} current={currentStep} status={statuses[3]} initiallyOpen={!!run?.spec && !findingsReady}
        purpose="Apply each classifier independently and inspect the judgments saved for each item."
        input="The accepted specification and selected pilot or full prepared dataset."
        output={run?.processed ? 'Saved item judgments, explanations, evidence, and separate records of failed or pending dimensions.' : 'Four judgments per item, with explanations and evidence; no judgments are available yet.'}
        next={findingsReady ? nextLink(5, 'Review summary findings for this selection') : run?.status === 'running' ? 'Wait for this phase to finish, or stop it to review the saved partial results.' : run?.spec ? 'Start or resume classification below when you are ready.' : nextLink(3, 'Review the specification first')}>
        {run?.spec ? <><h3 aria-live="polite">{classificationMessage}</h3>
          {selectedComplete && <p className="ia-small">{pilotComplete && run.total > pilotSize ? `The remaining ${(run.total - pilotSize).toLocaleString()} items are outside this pilot. Classifying them is optional.` : 'This completes item processing for the selected dataset.'}</p>}
          {run.status === 'running' && <progress max={target * classifierCount} value={run.completed_judgments ?? run.complete * classifierCount} aria-label="Classification progress" />}
          {run.status === 'running' && <button type="button" className="ia-secondary" onClick={() => void stop()} disabled={busy}>Stop analysis</button>}
          {['failed', 'cancelled'].includes(run.status) && <p className={run.status === 'failed' ? 'ia-error' : 'ia-small'}>{runMessage}</p>}
          <ProcessingCounts run={run} />
          {canClassify && <form className="ia-classify-panel" onSubmit={event => { event.preventDefault(); void classify(scope) }}>
            <div><h3>{scope === 'all' ? 'Optional: classify the remaining items' : `Classify ${pilotSize} selected items`}</h3>
              <p className="ia-small">{scope === 'all' ? 'You can keep the pilot as your result and proceed to review or export. Continue only if you want findings for the full prepared dataset.' : 'Classification pauses after this selection so you can inspect the results.'} Saved judgments are reused.</p>
              <p className="ia-small">{remainingRequests.toLocaleString()} primary GPT-6 Luna classifier requests remain. Each item uses {classifierCount} separate requests. Repairs and retries can add paid calls.</p></div>
            <div>{direct && scope === 'all' && <label className="ia-pilot-review"><input type="checkbox" checked={pilotReviewed} onChange={event => setPilotReviewed(event.target.checked)} /><span>I have reviewed the pilot labels, evidence, and criteria</span></label>}
              {direct && scope === 'all' && <p className="ia-small">This acknowledgment does not record independent human annotation or agreement.</p>}
              <KeyInput value={apiKey} onChange={setApiKey} /><button type="submit" className="ia-primary" disabled={busy || !apiKey.trim() || (direct && scope === 'all' && !pilotReviewed)}>{busy ? 'Starting…' : scope === 'all' ? 'Continue through all items' : ['cancelled', 'failed'].includes(run.status) ? 'Resume classification' : `Classify ${pilotSize} items with GPT-6 Luna`}</button></div>
          </form>}
          {inspection.error ? <div className="ia-error" role="alert"><p>{inspection.error}</p><button type="button" className="ia-secondary" onClick={inspection.retry}>Retry item inspection</button><button type="button" className="ia-text-button" onClick={() => inspect({ kind: 'all' })}>Show all items</button></div>
            : <ItemJudgments run={run} page={page} setPage={setPage} pageLoading={pageLoading} filter={filter} onFilterChange={inspect}
              filteredItems={filter.kind === 'all' ? undefined : inspection.items} filterLoading={inspection.loading} />}
        </> : <p>Item classification becomes available after Python accepts the specification. It starts only when you choose to run it with your API key.</p>}
      </StageSection>

      <StageSection step={5} current={currentStep} status={statuses[4]} initiallyOpen={findingsReady}
        purpose="Understand what each dimension found in the selected items and inspect findings that need attention."
        input="Valid saved item judgments from the completed or paused classification phase."
        output={findingsReady ? 'Four label distributions for the selection, with links to flagged and uncertain items.' : 'Label distributions will be available after classification pauses or finishes.'}
        next={findingsReady ? nextLink(6, 'Keep and share results') : nextLink(4, 'Continue to item classification')}>
        {run && findingsReady ? <SummaryFindings run={run} onInspect={inspect} /> : <p>{active ? 'Summary findings update when the current phase pauses or finishes. Step 4 shows live processing counts and saved item judgments.' : 'No summary findings are available yet. Processing counts belong to step 4; they do not establish scientific validity.'}</p>}
      </StageSection>

      <StageSection step={6} current={currentStep} status={statuses[5]} initiallyOpen={findingsReady}
        purpose="Keep a portable record of the analysis and share its findings."
        input="Saved context, item judgments, and summary findings."
        output="A readable report, complete results package, and individual data files."
        next={run?.spec ? 'View the report or download the results for later use and sharing.' : 'Prepare context and classify a selection to produce results.'}>
        {run?.spec ? <ResultExports run={run} onDownload={artifact => void download(artifact)} onViewReport={() => void openReport()} onDownloadPackage={() => void downloadPackage()} downloading={downloading} />
          : <p>The report, complete results package, item files, and classifier specification will be grouped here when available.</p>}
        {run && <><p className="ia-small ia-saved-note">{run.retention?.automatic_expiry && run.retention.expires_at
          ? `Results are saved until ${new Date(run.retention.expires_at).toLocaleString()}. Download a package to keep a separate copy.`
          : 'No automatic expiry is configured for this run. Return in this browser to review or continue; saved judgments are reused.'}</p>
          <details className="ia-source"><summary>Run metadata and usage</summary><dl className="ia-provenance"><div><dt>Run identifier</dt><dd><code>{run.run_id}</code></dd></div>
            {run.created_at && <div><dt>Created</dt><dd>{new Date(run.created_at).toLocaleString()}</dd></div>}{run.updated_at && <div><dt>Last saved</dt><dd>{new Date(run.updated_at).toLocaleString()}</dd></div>}</dl>
            {run.model && <p className="ia-small">Model: {run.model.model_id} · {run.model.provider} · {run.model.reasoning_effort} reasoning effort.</p>}
            <p className="ia-small">Recorded usage: {(run.usage?.input_tokens || 0).toLocaleString()} input tokens · {(run.usage?.output_tokens || 0).toLocaleString()} output tokens.</p></details>
          <details className="ia-source"><summary>Manage this saved analysis</summary><p>Starting another analysis removes this browser’s shortcut to the current run. Download its package first if you want to keep a copy. Discarding deletes the server copy.</p>
            <div className="ia-actions"><button type="button" className="ia-text-button" onClick={reset} disabled={busy || active}>Start a new analysis</button><button type="button" className="ia-text-button" onClick={() => setDiscardRequested(true)} disabled={busy || active}>Discard saved analysis</button></div>
            {discardRequested && <div className="ia-discard" role="group" aria-label="Confirm discard"><p>Delete this analysis and its saved files from the server?</p><button type="button" className="ia-secondary" disabled={busy} onClick={() => void discard()}>Delete analysis permanently</button><button type="button" className="ia-text-button" disabled={busy} onClick={() => setDiscardRequested(false)}>Keep analysis</button></div>}</details>
        </>}
      </StageSection>
      <details className="ia-privacy" id="item-analysis-privacy" open={privacyOpen} onToggle={event => setPrivacyOpen(event.currentTarget.open)}><summary>About your key and item data</summary>
        <p>Your OpenAI key is held in memory for model calls and never written to browser storage. This browser keeps a private run access token so you can return later; enter your API key again only to make further model calls.</p>
        <p>Source items, context, and judgments remain saved across server restarts when the server’s storage is retained. Clearing browser storage removes your access shortcut. Download the complete package for an independent copy.</p></details>
    </section>
    {!assessment && <SiteFooter onPrivacyClick={() => { setPrivacyOpen(true); document.getElementById('item-analysis-privacy')?.scrollIntoView({ block: 'center', behavior: 'smooth' }) }} />}
  </div>
}
