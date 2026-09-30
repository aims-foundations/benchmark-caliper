import { useEffect, useState, type FormEvent } from 'react'
import { SiteHeader } from '../components/SiteHeader'
import { SiteFooter } from '../components/SiteFooter'
import { appPath } from '../paths'
import * as api from './api'
import { Criteria } from './Criteria'
import { Results } from './Results'
import type { AnalysisRun, Artifact, Catalog, RunAccess, RunScope, SpecificationMode } from './types'
import './itemAnalysis.css'

const STORAGE_KEY = 'item_analysis_run_v1'
const ACTIVE_STATUSES = ['preparing', 'generating', 'running']
const FILE_NAMES: Record<Artifact, string> = { spec: 'classifier_spec.json', items: 'items.csv', summary: 'summary.json', report: 'report.html', review: 'review.csv' }

function restoreRun(): RunAccess | null {
  try {
    const saved = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || 'null')
    return saved && typeof saved.run_id === 'string' && typeof saved.run_secret === 'string'
      ? { run_id: saved.run_id, run_secret: saved.run_secret } : null
  } catch { return null }
}

function KeyInput({ value, onChange }: { value: string; onChange: (key: string) => void }) {
  return <div className="ia-key"><label className="ia-field"><span>Anthropic API key</span>
    <input type="password" autoComplete="off" spellCheck={false} maxLength={512} placeholder="sk-ant-…" value={value} onChange={event => onChange(event.target.value)} required />
  </label><p className="ia-small">Used for paid model calls. Kept in memory for this tab; re-enter it after a refresh.</p></div>
}

function runTitle(run: AnalysisRun): string {
  const titles = { preparing: 'Preparing your benchmark', generating: 'Writing the classification criteria', ready: 'Your criteria are ready',
    running: 'Reading the items', checkpoint: 'Pause here for a human review', complete: 'Your analysis is ready', cancelled: 'Analysis stopped', failed: 'This run needs attention' }
  return titles[run.status]
}

export function ItemAnalysis() {
  const [catalog, setCatalog] = useState<Catalog | null>(null)
  const [exampleId, setExampleId] = useState('')
  const [mode, setMode] = useState<SpecificationMode>('generate')
  const [apiKey, setApiKey] = useState('')
  const [access, setAccess] = useState<RunAccess | null>(restoreRun)
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

  useEffect(() => {
    const controller = new AbortController()
    api.getCatalog(controller.signal).then(value => {
      if (controller.signal.aborted) return
      setCatalog(value)
      setExampleId(current => current || value.examples.find(example => example.available)?.id || '')
      setError('')
    }).catch(problem => { if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'Could not load the examples.') })
    return () => controller.abort()
  }, [catalogVersion])

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
        setRun(latest)
        setPollError('')
        setPageLoading(false)
        failures = 0
        if (ACTIVE_STATUSES.includes(latest.status)) timer = setTimeout(() => void poll(), 1000)
      } catch (problem) {
        if (controller.signal.aborted) return
        setPageLoading(false)
        failures += 1
        const expired = problem instanceof api.AnalysisApiError && [401, 403, 404, 410].includes(problem.status)
        setPollError(expired ? 'This run is no longer available. Start a new analysis to continue.' :
          failures < 3 ? 'Connection interrupted. Reconnecting to your run…' : 'Could not reconnect. Your run may still be processing; retry to check its progress.')
        if (!expired && failures < 3) timer = setTimeout(() => void poll(), failures * 2000)
      }
    }
    void poll()
    return () => { controller.abort(); if (timer) clearTimeout(timer) }
  }, [access, page, pollVersion])

  async function start(event: FormEvent) {
    event.preventDefault()
    if (busy || !exampleId || (mode === 'generate' && !apiKey.trim())) return
    setBusy(true)
    setError('')
    try {
      const result = await api.createRun(exampleId, mode, mode === 'generate' ? apiKey.trim() : '')
      const nextAccess = { run_id: result.run_id, run_secret: result.run_secret }
      // Persist only the run's access token. API keys never enter browser storage.
      try { sessionStorage.setItem(STORAGE_KEY, JSON.stringify(nextAccess)) } catch { /* The current tab can still use the run. */ }
      setRun(result)
      setPage(1)
      setAccess(nextAccess)
    } catch (problem) { setError(problem instanceof Error ? problem.message : 'Could not start this analysis.') }
    finally { setBusy(false) }
  }

  async function classify(scope: RunScope) {
    if (!access || !apiKey.trim() || busy) return
    setBusy(true)
    setError('')
    try {
      setRun(await api.classify(access, scope, apiKey.trim()))
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
    try { sessionStorage.removeItem(STORAGE_KEY) } catch { /* Storage may be disabled. */ }
    setAccess(null)
    setRun(null)
    setApiKey('')
    setError('')
    setPollError('')
    setPage(1)
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
  const pilotSize = Math.min(catalog?.checkpoint_size || 100, run?.total || example?.item_count || 100)
  const stage = !access ? 0 : !run?.spec || (run.status === 'ready' && !run.processed) ? 1 : 2
  const canClassify = !!run?.spec && !active && !pollError && ['ready', 'checkpoint', 'cancelled', 'failed'].includes(run.status)
  const scope: RunScope = run?.can_continue ? 'all' : 'pilot'
  const remaining = run ? Math.max(0, (scope === 'all' ? run.total : pilotSize) - run.complete) : pilotSize

  return <div className="rd-root item-analysis-site">
    <SiteHeader />
    <header className="ia-hero"><div className="rd-container">
      <a className="ia-back" href={appPath('/')}><span aria-hidden="true">← </span>Benchmark Caliper</a>
      <div className="ia-hero-row"><div><p className="ia-eyebrow">Item-level validity analysis <span className="ia-badge">Demo</span></p>
        <h1>Look closer at<br />your benchmark.</h1></div>
        <p>Turn an assessment into clear questions.<br className="ia-desktop-break" /> Apply them to individual items, then explore<br className="ia-desktop-break" /> the evidence behind the numbers.</p></div>
    </div></header>

    <main className="rd-container ia-main">
      <ol className="ia-steps" aria-label="Analysis steps">{['Choose a context', 'Review the criteria', 'Explore the results'].map((label, index) =>
        <li key={label} aria-current={stage === index ? 'step' : undefined} data-done={stage > index || undefined}><span>{index + 1}</span>{label}</li>)}</ol>
      {(error || pollError) && <div className="ia-error" role="alert"><p>{error || pollError}</p>
        {!catalog && <button className="ia-secondary" onClick={() => { setError(''); setCatalogVersion(value => value + 1) }}>Retry loading examples</button>}
        {pollError && <div className="ia-actions"><button className="ia-secondary" onClick={() => setPollVersion(value => value + 1)}>Retry connection</button><button className="ia-secondary" onClick={reset}>Start a new analysis</button></div>}
      </div>}
      {!catalog && !access && !error && <p role="status">Loading examples…</p>}

      {!access && catalog && <div className="ia-setup"><form className="ia-panel" onSubmit={start}>
        <p className="ia-eyebrow">Start with an example</p><h2>A benchmark. A real use case.</h2>
        <p className="ia-muted">Choose a prepared context to try the complete workflow.</p>
        <label className="ia-field"><span>Benchmark example</span><select value={exampleId} onChange={event => { setExampleId(event.target.value); setMode('generate') }}>
          {catalog.examples.map(entry => <option key={entry.id} value={entry.id} disabled={!entry.available}>{entry.title}{!entry.available ? ' — unavailable' : ''}</option>)}
        </select></label>
        {example && <div className="ia-context"><div className="ia-context-top"><strong>{example.item_count.toLocaleString()} items</strong><span>{example.source_label}</span></div>
          <p>{example.description}</p><details><summary>Deployment context</summary><p>{example.deployment}</p></details></div>}
        <fieldset className="ia-mode"><legend>Classification criteria</legend>
          <label><input type="radio" name="specification" value="generate" checked={mode === 'generate'} onChange={() => setMode('generate')} /><span><strong>Generate with Sonnet</strong><small>Create criteria from the assessment and dataset evidence.</small></span></label>
          <label><input type="radio" name="specification" value="provided" checked={mode === 'provided'} disabled={example?.supplied_spec_available === false} onChange={() => setMode('provided')} /><span><strong>Use example criteria</strong><small>Inspect the supplied specification without a model call.</small></span></label>
        </fieldset>
        {mode === 'generate' && <KeyInput value={apiKey} onChange={setApiKey} />}
        <button className="ia-primary" type="submit" disabled={busy || !example?.available || (mode === 'generate' && !apiKey.trim())}>
          {busy ? 'Starting…' : mode === 'generate' ? 'Generate criteria with Sonnet' : 'Load example criteria'}<span aria-hidden="true"> →</span>
        </button>
        <p className="ia-small ia-cost-note">{mode === 'generate' ? 'Starts a paid Sonnet request. Item classification begins separately.' : 'No API key needed to inspect criteria and browse the items.'}</p>
      </form><aside className="ia-guide"><p className="ia-eyebrow">A closer reading</p>
        <div className="ia-guide-graphic" aria-hidden="true"><span className="ia-sheet"><i /><i /><i /></span><span className="ia-graphic-arrow">→</span><span className="ia-item-grid">{Array.from({ length: 9 }, (_, index) => <i key={index} />)}</span></div>
        <h3>From a finding<br />to a measured pattern.</h3><p>Caliper identifies possible validity issues. This analysis checks individual items to see how often each property appears.</p>
        <ol><li><strong>Write the questions</strong><span>Sonnet translates the original assessment into specific criteria.</span></li><li><strong>Read each item</strong><span>Haiku applies those criteria and records its evidence.</span></li><li><strong>Count and inspect</strong><span>Explore the distributions and review individual judgments.</span></li></ol>
        <p className="ia-guide-note">{example && example.item_count <= 100 ? `Classify all ${example.item_count} example items, then inspect the judgments and export the results.` : 'Start with 100 items, review the results, then continue through the full snapshot.'}</p>
      </aside></div>}

      {access && !run && !pollError && <p role="status">Restoring your analysis…</p>}
      {run && <div className="ia-run">
        <section className="ia-panel ia-run-status" aria-label="Run progress"><div className="ia-section-heading"><div>
          <p className="ia-eyebrow">{run.example.title}</p><h2>{runTitle(run)}</h2></div>
          <span className={`ia-tag ${active ? 'ia-tag-active' : ''}`}>{active ? 'In progress' : run.status === 'checkpoint' ? 'Review checkpoint' : run.status === 'complete' ? 'Finished' : 'Your analysis'}</span></div>
          <p className="ia-muted" role="status">{run.message}</p>
          {run.status === 'checkpoint' && <p className="ia-small">Inspect the labels and evidence below before continuing. If the criteria need changes, update them and start a new run so all items use the same instructions.</p>}
          {run.status === 'running' && <><progress max={run.scope === 'pilot' ? pilotSize : run.total} value={run.processed} aria-label="Classification progress" />
            <p className="ia-small">{run.processed.toLocaleString()} processed · {run.complete.toLocaleString()} classified · {run.errors.toLocaleString()} failed · {run.total.toLocaleString()} in snapshot</p></>}
          {run.error && <p className="ia-error">{run.error}</p>}
          <div className="ia-run-meta"><span>{run.example.source_label}</span><span>{run.total.toLocaleString()} items</span></div>
          <div className="ia-actions">{active ? <button className="ia-secondary" onClick={() => void stop()} disabled={busy}>Stop analysis</button> :
            <button className="ia-text-button" onClick={reset} disabled={busy}>Start a new analysis</button>}
            {run.spec && <button className="ia-text-button" disabled={downloading !== null} onClick={() => void download('spec')}>Download criteria ↓</button>}</div>
          <details className="ia-source"><summary>Context and usage</summary><p>{run.example.deployment}</p>
            <p>{run.example.description}</p><p className="ia-small">Model usage: {(run.usage?.input_tokens || 0).toLocaleString()} input tokens · {(run.usage?.output_tokens || 0).toLocaleString()} output tokens.</p></details>
        </section>

        {run.spec && <Criteria spec={run.spec} metadata={run.summary?.specification} />}

        {canClassify && <form className="ia-classify-panel" onSubmit={event => { event.preventDefault(); void classify(scope) }}>
          <div><p className="ia-eyebrow">{scope === 'all' ? 'Complete the snapshot' : 'Try the criteria'}</p>
            <h2>{scope === 'all' ? 'Ready to read the remaining items?' : `Classify ${pilotSize < run.total ? `the first ${pilotSize}` : `all ${pilotSize}`} items`}</h2>
            <p className="ia-small">{scope === 'all' ? 'Continue with the same criteria. Completed judgments are preserved.' : pilotSize < run.total ? 'The run pauses after this pilot for your review.' : 'This small example fits in a single run.'} Up to {remaining.toLocaleString()} paid Haiku item requests; malformed responses may be retried.</p></div>
          <div><KeyInput value={apiKey} onChange={setApiKey} /><button type="submit" className="ia-primary" disabled={busy || !apiKey.trim()}>
            {busy ? 'Starting…' : scope === 'all' ? 'Continue through all items' : ['cancelled', 'failed'].includes(run.status) ? 'Resume classification' : `Classify ${pilotSize} items with Haiku`}</button></div>
        </form>}

        {run.spec && <Results run={run} page={page} setPage={setPage} onDownload={artifact => void download(artifact)} downloading={downloading} pageLoading={pageLoading} />}
      </div>}
      <details className="ia-privacy" id="item-analysis-privacy" open={privacyOpen} onToggle={event => setPrivacyOpen(event.currentTarget.open)}><summary>About your key and this demo</summary>
        <p>Your Anthropic key is sent to the server for model calls and held in memory while a phase runs. This page never writes it to browser storage. A run access token is kept in this tab’s session storage so you can refresh and return to the results.</p>
        <p>Source items, criteria, and model judgments are kept privately for this run and expire one hour after it ends, or when the server restarts. Download the files you need before leaving. Example datasets are labelled with their source; illustrative items are for demonstrating the workflow.</p>
      </details>
    </main>
    <SiteFooter onPrivacyClick={() => { setPrivacyOpen(true); document.getElementById('item-analysis-privacy')?.scrollIntoView({ block: 'center', behavior: 'smooth' }) }} />
  </div>
}
