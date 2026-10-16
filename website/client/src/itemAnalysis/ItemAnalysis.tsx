import { useEffect, useState, type FormEvent } from 'react'
import { SiteHeader } from '../components/SiteHeader'
import { SiteFooter } from '../components/SiteFooter'
import { appPath } from '../paths'
import * as api from './api'
import { Criteria } from './Criteria'
import { Results } from './Results'
import { BenchmarkConfirmation } from './BenchmarkConfirmation'
import { assessmentStorageKey, restoreAccess } from './accessStorage'
import type { AnalysisRun, Artifact, AssessmentReference, AssessmentSetup, Catalog, ConfirmedDataset, DirectContext, Example, RunAccess, RunScope, SpecificationMode } from './types'
import './itemAnalysis.css'

const ACTIVE_STATUSES = ['preparing', 'generating', 'running']
const FILE_NAMES: Record<Artifact, string> = { spec: 'classifier_spec.json', items: 'items.csv', summary: 'summary.json', report: 'report.html', review: 'review.csv' }

function KeyInput({ value, onChange }: { value: string; onChange: (key: string) => void }) {
  return <div className="ia-key"><label className="ia-field"><span>OpenAI API key</span>
    <input type="password" autoComplete="off" spellCheck={false} maxLength={512} placeholder="sk-…" value={value} onChange={event => onChange(event.target.value)} required />
  </label><p className="ia-small">Used for paid model calls. Kept in memory for this tab; re-enter it after a refresh.</p></div>
}

function runTitle(run: AnalysisRun): string {
  const titles = { preparing: 'Preparing your benchmark', generating: 'Writing the classification criteria', ready: 'Your criteria are ready',
    running: 'Reading the items', checkpoint: 'Pause here for a human review', complete: 'Your analysis is ready', cancelled: 'Analysis stopped', failed: 'This run needs attention' }
  return titles[run.status]
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
  const [error, setError] = useState('')
  const [pollError, setPollError] = useState('')
  const [pollVersion, setPollVersion] = useState(0)
  const [catalogVersion, setCatalogVersion] = useState(0)
  const [downloading, setDownloading] = useState<Artifact | null>(null)
  const [privacyOpen, setPrivacyOpen] = useState(false)
  const [pilotReviewed, setPilotReviewed] = useState(false)
  const direct = assessment?.kind === 'direct'

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
        const latest = await api.getRun(access!, page, controller.signal)
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
  }, [access, page, pollVersion, assessment?.kind, assessment?.id])

  async function start(event: FormEvent) {
    event.preventDefault()
    const selected = catalog?.examples.find(entry => entry.id === exampleId)
    if (busy) return
    if (assessment) {
      if (!setup || !apiKey.trim() || !confirmedDataset) return
    } else if (!selected?.available || (mode === 'provided' && selected.supplied_spec_available === false) || (mode === 'generate' && !apiKey.trim())) return
    setBusy(true)
    setError('')
    try {
      const result = directContext
        ? await api.createDirectRun(directContext, confirmedDataset!, apiKey.trim())
        : assessment
        ? await api.createAssessmentRun(assessment, confirmedDataset!, apiKey.trim())
        : await api.createRun(exampleId, mode, mode === 'generate' ? apiKey.trim() : '')
      if (assessment && (result.assessment?.kind !== assessment.kind || result.assessment.id !== assessment.id)) {
        throw new api.AnalysisApiError('The returned item analysis does not match this context. Confirm the context again.', 409)
      }
      const nextAccess = { run_id: result.run_id, run_secret: result.run_secret }
      // Persist only the run's access token. API keys never enter browser storage.
      try { sessionStorage.setItem(storageKey, JSON.stringify(nextAccess)) } catch { /* The current tab can still use the run. */ }
      setRun(result)
      setPage(1)
      setAccess(nextAccess)
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : 'Could not start this analysis.')
      if (assessment && problem instanceof api.AnalysisApiError && problem.status === 409) {
        setConfirmedDataset(null)
        setSetup(null)
        setCatalogVersion(value => value + 1)
      }
    }
    finally { setBusy(false) }
  }

  async function classify(scope: RunScope) {
    if (!access || !apiKey.trim() || busy) return
    if (direct && scope === 'all' && !pilotReviewed) return
    setBusy(true)
    setError('')
    try {
      setRun(await (direct && scope === 'all'
        ? api.classify(access, scope, apiKey.trim(), pilotReviewed)
        : api.classify(access, scope, apiKey.trim())))
      setPage(1)
      setPollVersion(value => value + 1)
    } catch (problem) { setError(problem instanceof Error ? problem.message : 'Could not start classification.') }
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
    } catch { setError('Could not confirm the stop. Try again; the run may still be processing.') }
    finally { setBusy(false) }
  }

  function reset() {
    try { sessionStorage.removeItem(storageKey) } catch { /* Storage may be disabled. */ }
    setAccess(null)
    setRun(null)
    setApiKey('')
    setConfirmedDataset(null)
    setSetup(null)
    setError('')
    setPollError('')
    setPage(1)
    setPilotReviewed(false)
  }

  async function download(artifact: Artifact) {
    if (!access || downloading) return
    setDownloading(artifact)
    try {
      const blob = await api.download(access, artifact)
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = FILE_NAMES[artifact]
      document.body.appendChild(link)
      link.click()
      link.remove()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (problem) { setError(problem instanceof Error ? problem.message : 'Could not download this file.') }
    finally { setDownloading(null) }
  }

  const example = run?.example || catalog?.examples.find(value => value.id === exampleId)
  const active = !!run && ACTIVE_STATUSES.includes(run.status)
  const pilotSize = Math.min(setup?.checkpoint_size || catalog?.checkpoint_size || 100, run?.total || example?.item_count || 100)
  const stage = !access ? 0 : !run?.spec || (run.status === 'ready' && !run.processed) ? 1 : 2
  const canClassify = !!run?.spec && !active && !pollError && ['ready', 'checkpoint', 'cancelled', 'failed'].includes(run.status)
  const scope: RunScope = run?.can_continue ? 'all' : 'pilot'
  const remaining = run ? Math.max(0, (scope === 'all' ? run.total : pilotSize) - run.complete) : pilotSize
  const incompleteResults = !!assessment && run?.status === 'complete' && (run.complete < run.total || run.errors > 0)
  const runMessage = run?.status === 'failed' ? run.failure?.message || run.error || run.message : run?.message

  return <div className={assessment ? 'item-analysis-site ia-embedded' : 'rd-root item-analysis-site'}>
    {!assessment && <><SiteHeader />
    <header className="ia-hero"><div className="rd-container">
      <a className="ia-back" href={appPath('/')}><span aria-hidden="true">← </span>Benchmark Caliper</a>
      <div className="ia-hero-row"><div><p className="ia-eyebrow">Item-level validity analysis <span className="ia-badge">Demo</span></p>
        <h1>Look closer at<br />your benchmark.</h1></div>
        <p>Turn an assessment into clear questions.<br className="ia-desktop-break" /> Apply them to individual items, then explore<br className="ia-desktop-break" /> the evidence behind the numbers.</p></div>
    </div></header></>}

    <section id={assessment ? 'item-analysis' : undefined} className={assessment ? 'ia-main' : 'rd-container ia-main'} aria-label="Item analysis">
      {assessment && <div className="ia-integrated-heading"><p className="ia-eyebrow">{direct ? 'Starting from your requirements' : 'Next pipeline stage'}</p><h2>Item analysis</h2>
        <p>{direct ? 'Generate item criteria from your deployment, task, and answer requirements. Review a pilot before classifying the full dataset.' : 'Apply the findings above to the benchmark’s items. Review the criteria and initial classifications, then complete the full dataset to finish this assessment.'}</p>
        {direct && <p className="ia-assessment-not-run"><strong>Benchmark assessment: Not run.</strong> This path analyzes items against your requirements and does not produce benchmark-level validity scores.</p>}
        {onEditContext && <button type="button" className="ia-text-button" disabled={busy || active} onClick={onEditContext}>Edit context and start again</button>}
      </div>}
      <ol className="ia-steps" aria-label="Item analysis steps">{[assessment ? 'Confirm the benchmark' : 'Choose a context', 'Review the criteria', 'Classify and inspect'].map((label, index) =>
        <li key={label} aria-current={stage === index ? 'step' : undefined} data-done={stage > index || undefined}><span>{index + 1}</span>{label}</li>)}</ol>
      {(error || pollError) && <div className="ia-error" role="alert"><p>{error || pollError}</p>
        {!(assessment ? setup || access : catalog) && <button className="ia-secondary" onClick={() => { setError(''); setCatalogVersion(value => value + 1) }}>{assessment ? 'Retry loading assessment' : 'Retry loading benchmarks'}</button>}
        {pollError && <div className="ia-actions"><button className="ia-secondary" onClick={() => setPollVersion(value => value + 1)}>Retry connection</button><button className="ia-secondary" onClick={reset}>Start a new analysis</button></div>}
      </div>}
      {!(assessment ? setup : catalog) && !access && !error && <p role="status">{assessment ? 'Connecting your benchmark assessment…' : 'Loading benchmarks…'}</p>}

      {assessment && !access && setup && <form className="ia-panel ia-linked-setup" onSubmit={start} aria-busy={busy}>
        <h3>Continue with {setup.assessment.benchmark_name || setup.assessment.benchmark}</h3>
        <p>{direct ? 'Your deployment, task requirements, and answer requirements will be used to generate the item criteria.' : 'The scores and deployment context from this report will be used to generate the item criteria.'}</p>
        <details className="ia-context"><summary>{direct ? 'Context and requirements' : 'Deployment context carried forward'}</summary><p>{setup.assessment.deployment}</p></details>
        <fieldset className="ia-linked-controls" disabled={busy}>
        <BenchmarkConfirmation assessment={assessment} setup={setup} directContext={directContext} confirmed={confirmedDataset} onConfirm={dataset => { setConfirmedDataset(dataset); if (dataset) setError('') }} />
        {confirmedDataset && <div className="ia-confirmed-next-step">
          <KeyInput value={apiKey} onChange={setApiKey} />
          <button className="ia-primary" type="submit" disabled={busy || !apiKey.trim()}>{busy ? 'Starting…' : 'Generate item criteria'}<span aria-hidden="true"> →</span></button>
          <p className="ia-small ia-cost-note">This stage uses your OpenAI key. Generating criteria starts paid model calls; review the criteria before starting item classification.</p>
        </div>}
        </fieldset>
      </form>}

      {!assessment && !access && catalog && <div className="ia-setup"><form className="ia-panel" onSubmit={start}>
        <p className="ia-eyebrow">Choose a benchmark</p><h2>A benchmark. A real use case.</h2>
        <p className="ia-muted">Select a benchmark and its assessment context. Each analysis uses that context to generate criteria and inspect the benchmark’s items.</p>
        <label className="ia-field"><span>Benchmark and assessment context</span><select value={exampleId} onChange={event => { setExampleId(event.target.value); setMode('generate') }}>
          {catalog.examples.map(entry => <option key={entry.id} value={entry.id}>{entry.title}{!entry.available ? ' — unavailable' : ''}</option>)}
        </select></label>
        {example && <div className="ia-context"><div className="ia-context-top"><strong>{example.item_count.toLocaleString()} items</strong><span>{example.source_label}</span></div>
          {example.assessment_title && <p><strong>Assessment context:</strong> {example.assessment_title}</p>}
          <p>{example.description}</p><details><summary>Deployment context</summary><p>{example.deployment}</p><DatasetSource example={example} /></details></div>}
        {example && !example.available && <p className="ia-error" role="status">{example.unavailable_reason || 'This dataset is not available on the server yet. The site maintainer needs to configure dataset access.'}</p>}
        <fieldset className="ia-mode" disabled={!example?.available}><legend>Classification criteria</legend>
          <label><input type="radio" name="specification" value="generate" checked={mode === 'generate'} onChange={() => setMode('generate')} /><span><strong>Generate with GPT-6 Luna</strong><small>Create criteria from the assessment and dataset evidence.</small></span></label>
          <label><input type="radio" name="specification" value="provided" checked={mode === 'provided'} disabled={example?.supplied_spec_available === false} onChange={() => setMode('provided')} /><span><strong>Use supplied criteria</strong><small>{example?.supplied_spec_available === false ? 'No supplied criteria for this context. Generate criteria from its assessment to continue.' : 'Inspect the supplied specification without a model call.'}</small></span></label>
        </fieldset>
        {mode === 'generate' && example?.available && <KeyInput value={apiKey} onChange={setApiKey} />}
        <button className="ia-primary" type="submit" disabled={busy || !example?.available || (mode === 'generate' && !apiKey.trim())}>
          {busy ? 'Starting…' : mode === 'generate' ? 'Generate criteria with GPT-6 Luna' : 'Load supplied criteria'}<span aria-hidden="true"> →</span>
        </button>
        <p className="ia-small ia-cost-note">{!example?.available ? 'Dataset access is managed by the website. No Hugging Face key is needed from visitors.' : mode === 'generate' ? 'Starts a paid GPT-6 Luna request. Item classification begins separately.' : 'No API key needed to inspect criteria and browse the items.'}</p>
      </form><aside className="ia-guide"><p className="ia-eyebrow">A closer reading</p>
        <div className="ia-guide-graphic" aria-hidden="true"><span className="ia-sheet"><i /><i /><i /></span><span className="ia-graphic-arrow">→</span><span className="ia-item-grid">{Array.from({ length: 9 }, (_, index) => <i key={index} />)}</span></div>
        <h3>From a finding<br />to a measured pattern.</h3><p>Caliper identifies possible validity issues. This analysis checks individual items to see how often each property appears.</p>
        <ol><li><strong>Write the questions</strong><span>GPT-6 Luna translates the original assessment into specific criteria.</span></li><li><strong>Read each item</strong><span>GPT-6 Luna applies those criteria and records its evidence.</span></li><li><strong>Count and inspect</strong><span>Explore the distributions and review individual judgments.</span></li></ol>
        <p className="ia-guide-note">{example && example.item_count <= 100 ? `Classify all ${example.item_count} example items, then inspect the judgments and export the results.` : 'Start with 100 items, review the results, then continue through the full snapshot.'}</p>
      </aside></div>}

      {access && !run && !pollError && <p role="status">Restoring your analysis…</p>}
      {run && <div className="ia-run">
        <section className="ia-panel ia-run-status" aria-label="Run progress"><div className="ia-section-heading"><div>
          <p className="ia-eyebrow">{run.example.title}</p><h2>{incompleteResults ? 'Some items still need classification' : direct && run.status === 'complete' ? 'Item analysis complete' : runTitle(run)}</h2></div>
          <span className={`ia-tag ${active ? 'ia-tag-active' : ''}`}>{active ? 'In progress' : run.status === 'checkpoint' ? 'Review checkpoint' : incompleteResults ? 'Incomplete' : run.status === 'complete' ? 'Finished' : 'Your analysis'}</span></div>
          <p className={run.status === 'failed' ? 'ia-error' : 'ia-muted'} role="status">{runMessage}</p>
          {run.status === 'failed' && run.failure && <p className="ia-small">Error reference: <code>{run.failure.stage}/{run.failure.code}</code></p>}
          {run.status === 'checkpoint' && <p className="ia-small">Inspect the labels and evidence below, then continue through all remaining items to complete the {direct ? 'item analysis' : 'assessment'}. To regenerate the criteria, start a new item analysis so all items use the same instructions.</p>}
          {run.status === 'running' && <><progress max={run.scope === 'pilot' ? pilotSize : run.total} value={run.processed} aria-label="Classification progress" />
            <p className="ia-small">{run.processed.toLocaleString()} processed · {run.complete.toLocaleString()} classified · {run.errors.toLocaleString()} failed · {run.total.toLocaleString()} in snapshot</p></>}
          {run.status !== 'failed' && run.error && run.error !== runMessage && <p className="ia-error">{run.error}</p>}
          <div className="ia-run-meta">{run.example.assessment_title && <span>Assessment context: {run.example.assessment_title}</span>}<span>{run.example.source_label}</span><span>{run.total.toLocaleString()} items</span></div>
          <div className="ia-actions">{active ? <button className="ia-secondary" onClick={() => void stop()} disabled={busy}>Stop analysis</button> :
            <button className="ia-text-button" onClick={reset} disabled={busy}>Start a new analysis</button>}
            {run.spec && <button className="ia-text-button" disabled={downloading !== null} onClick={() => void download('spec')}>Download criteria ↓</button>}</div>
          <details className="ia-source"><summary>Context and usage</summary><p>{run.example.deployment}</p>
            <p>{run.example.description}</p><DatasetSource example={run.example} />
            {run.model && <p className="ia-small">Model: <code>{run.model.model_id}</code> · {run.model.provider} · {run.model.reasoning_effort} reasoning effort.</p>}
            <p className="ia-small">Model usage: {(run.usage?.input_tokens || 0).toLocaleString()} input tokens · {(run.usage?.output_tokens || 0).toLocaleString()} output tokens.</p></details>
        </section>

        {run.spec && <Criteria spec={run.spec} metadata={run.summary?.specification} direct={direct} />}

        {canClassify && <form className="ia-classify-panel" onSubmit={event => { event.preventDefault(); void classify(scope) }}>
          <div><p className="ia-eyebrow">{scope === 'all' ? 'Complete the snapshot' : 'Try the criteria'}</p>
            <h2>{scope === 'all' ? 'Classify the remaining items' : `Classify ${pilotSize < run.total ? `the first ${pilotSize}` : `all ${pilotSize}`} items`}</h2>
            <p className="ia-small">{scope === 'all' ? 'Continue with the same criteria. Completed judgments are preserved.' : pilotSize < run.total ? 'The run pauses after this pilot for your review.' : 'This small example fits in a single run.'} Up to {remaining.toLocaleString()} paid GPT-6 Luna item requests; malformed responses may be retried.</p></div>
          <div>{direct && scope === 'all' && <label className="ia-pilot-review"><input type="checkbox" checked={pilotReviewed} onChange={event => setPilotReviewed(event.target.checked)} /><span>I have reviewed the pilot labels, evidence, and criteria</span></label>}
            <KeyInput value={apiKey} onChange={setApiKey} /><button type="submit" className="ia-primary" disabled={busy || !apiKey.trim() || (direct && scope === 'all' && !pilotReviewed)}>
            {busy ? 'Starting…' : scope === 'all' ? 'Continue through all items' : ['cancelled', 'failed'].includes(run.status) ? 'Resume classification' : `Classify ${pilotSize} items with GPT-6 Luna`}</button></div>
        </form>}

        {run.spec && <Results run={run} page={page} setPage={setPage} onDownload={artifact => void download(artifact)} downloading={downloading} pageLoading={pageLoading} />}
      </div>}
      <details className="ia-privacy" id="item-analysis-privacy" open={privacyOpen} onToggle={event => setPrivacyOpen(event.currentTarget.open)}><summary>{assessment ? 'About your key and item data' : 'About your key and this demo'}</summary>
        <p>Your OpenAI key is sent to the server for model calls and held in memory while a phase runs. This page never writes it to browser storage. A run access token is kept in this tab’s session storage so you can refresh and return to the results.</p>
        <p>Source items, criteria, and model judgments are kept privately for this run and expire one hour after it ends, or when the server restarts. Download the files you need before leaving. Datasets are labelled with their source; illustrative items are for demonstrating the workflow.</p>
      </details>
    </section>
    {!assessment && <SiteFooter onPrivacyClick={() => { setPrivacyOpen(true); document.getElementById('item-analysis-privacy')?.scrollIntoView({ block: 'center', behavior: 'smooth' }) }} />}
  </div>
}
