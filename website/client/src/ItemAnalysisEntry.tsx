import { useEffect, useState } from 'react'
import { fetchGallery, type GalleryEntry } from './api'
import { SiteHeader } from './components/SiteHeader'
import { SiteFooter } from './components/SiteFooter'
import { PrivacyNotice } from './components/PrivacyNotice'
import { DirectItemStart } from './itemAnalysis/DirectItemStart'
import { appPath } from './paths'
import './itemAnalysis/itemAnalysis.css'
import './ItemAnalysisEntry.css'

/** Resolve a saved report locally; never fetch a user-supplied URL. */
export function savedReportPath(value: string): string | null {
  let id = value.trim()
  if (!/^[0-9a-fA-F-]{8,64}$/.test(id)) {
    try {
      const url = new URL(id, window.location.origin)
      const allowed = new Set([window.location.hostname, 'aims.stanford.edu', 'aimslab.stanford.edu', 'benchmark-caliper-ffxr.onrender.com'])
      if (!['http:', 'https:'].includes(url.protocol) || !allowed.has(url.hostname) || url.username || url.password) return null
      const match = url.pathname.match(/^(?:\/benchmark-caliper)?\/run\/([0-9a-fA-F-]{8,64})\/?$/)
      if (!match) return null
      id = match[1]
    } catch { return null }
  }
  return appPath(`/run/${id}#item-analysis-stage`)
}

function ExistingAssessment() {
  const [entries, setEntries] = useState<GalleryEntry[]>([])
  const [selectedId, setSelectedId] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [retry, setRetry] = useState(0)
  const [savedLink, setSavedLink] = useState('')
  const selected = entries.find(entry => entry.id === selectedId)
  const savedPath = savedReportPath(savedLink)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError('')
    fetchGallery().then(value => {
      if (!cancelled) { setEntries(value); setLoading(false) }
    }).catch(() => {
      if (!cancelled) { setError('Could not load existing assessments. Retry or open your saved report below.'); setLoading(false) }
    })
    return () => { cancelled = true }
  }, [retry])

  return <section className="ia-entry-existing" aria-label="Use an existing assessment">
    <div className="ia-panel">
      <p className="ia-eyebrow">Reuse the benchmark stage</p>
      <h2>Choose an existing assessment</h2>
      <p>Use its original deployment context, summary, and findings to analyze the items. Opening a report makes no new benchmark model calls.</p>
      {loading && <p role="status">Loading existing assessments…</p>}
      {error && <div className="ia-error" role="alert"><p>{error}</p><button className="ia-secondary" onClick={() => setRetry(value => value + 1)}>Retry loading assessments</button></div>}
      {!loading && !error && (entries.length ? <label className="ia-field"><span>Benchmark and deployment</span>
        <select value={selectedId} onChange={event => setSelectedId(event.target.value)}>
          <option value="">Choose an assessment</option>
          {entries.map(entry => <option key={entry.id} value={entry.id}>{entry.benchmarkName} · {entry.slug.replaceAll('_', ' ')}</option>)}
        </select></label> : <p>No gallery assessments are available. Open a saved report or use a new deployment context.</p>)}
      {selected && <div className="ia-entry-selected"><h3>{selected.benchmarkName}</h3>
        <p className="ia-eyebrow">Original deployment context</p><p>{selected.deploymentDescription || selected.slug.replaceAll('_', ' ')}</p>
        <a className="ia-primary ia-entry-action" href={appPath(`/caliper?assessment=${encodeURIComponent(selected.id)}#item-analysis-stage`)}>Continue to item analysis →</a></div>}
      <p className="ia-small">The report's context stays fixed. Choose “New deployment context” above to analyze items for a different use case.</p>
    </div>
    <div className="ia-panel">
      <p className="ia-eyebrow">Continue your own work</p><h2>Open a saved report</h2>
      <p>Paste a Benchmark Caliper report link or run ID to reuse a benchmark assessment you already completed.</p>
      <label className="ia-field"><span>Saved report link or run ID</span><input value={savedLink} onChange={event => setSavedLink(event.target.value)} maxLength={2048} placeholder="https://…/benchmark-caliper/run/…" autoComplete="off" spellCheck={false} /></label>
      {savedLink.trim() && !savedPath && <p className="ia-error">Enter a valid Benchmark Caliper report link or run ID.</p>}
      {savedPath ? <a className="ia-secondary ia-entry-action" href={savedPath}>Continue from saved report →</a> : <button className="ia-secondary" disabled>Continue from saved report →</button>}
      <p className="ia-small">The report and its deployment context must still be available on the server.</p>
    </div>
  </section>
}

export function ItemAnalysisEntry() {
  const [mode, setMode] = useState<'existing' | 'new'>(() => new URLSearchParams(window.location.search).get('mode') === 'new' ? 'new' : 'existing')
  const [privacy, setPrivacy] = useState(false)
  function selectMode(next: 'existing' | 'new') {
    setMode(next)
    window.history.replaceState(null, '', appPath(`/caliper?start=items&mode=${next}`))
  }
  return <div className="rd-root item-analysis-site ia-entry">
    <SiteHeader />
    <header className="ia-hero"><div className="rd-container">
      <a className="ia-back" href={appPath('/caliper')}>← Benchmark Caliper</a>
      <p className="ia-eyebrow">Benchmark validity analysis</p><h1>Start at item analysis.</h1>
      <p className="ia-entry-lead">Reuse a completed assessment or bring your own deployment context. Start with the items without paying for a new benchmark assessment.</p>
    </div></header>
    <main className="rd-container ia-main">
      <div className="ia-entry-modes" role="group" aria-label="Item analysis starting point">
        <button type="button" aria-pressed={mode === 'existing'} onClick={() => selectMode('existing')}><strong>Use an existing assessment</strong><span>Carry forward its context and benchmark findings.</span></button>
        <button type="button" aria-pressed={mode === 'new'} onClick={() => selectMode('new')}><strong>New deployment context</strong><span>Define your requirements and analyze items directly.</span></button>
      </div>
      <p className="ia-entry-cost">No Anthropic key is needed for either starting point. Generating criteria and classifying items uses your OpenAI key and starts only when you choose to run those steps.</p>
      {mode === 'existing' ? <ExistingAssessment /> : <DirectItemStart />}
      <p className="ia-small ia-entry-demo">Want to explore first? <a href={appPath('/caliper?demo=mathdial&stage=items#item-analysis-stage')}>Try the free item walkthrough</a>.</p>
    </main>
    <SiteFooter onPrivacyClick={() => setPrivacy(true)} />
    {privacy && <div className="modal-overlay" role="dialog" aria-modal="true" aria-label="Privacy notice"><div className="modal-body"><PrivacyNotice onClose={() => setPrivacy(false)} /></div></div>}
  </div>
}
