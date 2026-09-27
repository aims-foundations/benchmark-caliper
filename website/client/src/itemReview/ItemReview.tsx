import { useEffect, useRef, useState, type FormEvent } from 'react'
import { SiteHeader } from '../components/SiteHeader'
import { SiteFooter } from '../components/SiteFooter'
import { appPath } from '../paths'
import { cancelReview, getCatalog, getReview, startReview, type Catalog, type Deployment, type Review, type RunAccess } from './api'
import { Results } from './Results'

const RUN_STORAGE = 'item_review_run_v1'
const EMPTY: Deployment = { task: '', users: '', inputs: '', outputs: '', success: '', constraints: '' }
const EXAMPLE: Deployment = {
  task: 'An AI mathematics tutor helping secondary-school students with algebra and geometry.',
  users: 'English-speaking secondary-school students. No specific country or curriculum is assumed.',
  inputs: 'Text questions and typed mathematical expressions, with follow-up questions in a conversation.',
  outputs: 'Correct answers with clear, age-appropriate explanations and useful follow-up questions.',
  success: 'Both mathematical correctness and a helpful explanation of the reasoning are required.',
  constraints: 'Text only. The tutor does not receive images or audio. Check misleading or incorrect explanations.',
}
const QUESTIONS: Array<{ id: keyof Deployment; title: string; hint: string }> = [
  { id: 'task', title: 'What will the AI system do?', hint: 'Describe its task, domain, and the setting where people will use it.' },
  { id: 'users', title: 'Who will use it?', hint: 'Include relevant users, languages, locations, and expertise. Say when a detail is unspecified.' },
  { id: 'inputs', title: 'What inputs will it receive?', hint: 'Describe text, images, audio, tools, and whether users can ask follow-up questions.' },
  { id: 'outputs', title: 'What should its responses look like?', hint: 'Describe the expected language, format, explanation, decision, or other output.' },
  { id: 'success', title: 'What counts as a successful response?', hint: 'What should an evaluation measure: correctness, helpfulness, safe refusal, or other outcomes?' },
  { id: 'constraints', title: 'What constraints or failures matter? (optional)', hint: 'Include situations the system must handle carefully, or capabilities outside its scope.' },
]

function savedRun(): RunAccess | null {
  try {
    const run = JSON.parse(sessionStorage.getItem(RUN_STORAGE) || 'null')
    return run && typeof run.run_id === 'string' && typeof run.run_secret === 'string' ? run : null
  } catch { return null }
}

export function ItemReview() {
  const [catalog, setCatalog] = useState<Catalog | null>(null)
  const [step, setStep] = useState<'access' | 'deployment' | 'confirm'>('access')
  const [apiKey, setApiKey] = useState('')
  const [deployment, setDeployment] = useState<Deployment>(EMPTY)
  const [page, setPage] = useState(1)
  const [access, setAccess] = useState<RunAccess | null>(savedRun)
  const [review, setReview] = useState<Review | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const workspace = useRef<HTMLDivElement>(null)
  const previousStage = useRef('access')
  const stage = access ? 'results' : step

  useEffect(() => {
    if (previousStage.current !== stage) {
      workspace.current?.focus({ preventScroll: true })
      workspace.current?.scrollIntoView?.({ block: 'start' })
    }
    previousStage.current = stage
  }, [stage])

  useEffect(() => {
    const controller = new AbortController()
    getCatalog(controller.signal).then(setCatalog).catch(e => {
      if (!controller.signal.aborted) setError(e instanceof Error ? e.message : 'Could not load the demo catalog.')
    })
    return () => controller.abort()
  }, [])

  useEffect(() => {
    if (!access) return
    const controller = new AbortController()
    let timer: ReturnType<typeof setTimeout>
    async function poll() {
      try {
        const latest = await getReview(access!, page, controller.signal)
        if (controller.signal.aborted) return
        setReview(latest)
        setError('')
        if (['preparing', 'running'].includes(latest.status)) timer = setTimeout(() => void poll(), 2000)
      } catch (e) {
        if (!controller.signal.aborted) {
          setError(e instanceof Error ? e.message : 'Could not load progress. Your review may still be running.')
          timer = setTimeout(() => void poll(), 5000)
        }
      }
    }
    void poll()
    return () => { controller.abort(); clearTimeout(timer) }
  }, [access, page])

  function moveToDeployment(e: FormEvent) {
    e.preventDefault()
    if (!apiKey.trim() || !catalog?.dataset_access_configured) return
    setError('')
    setStep('deployment')
  }

  async function start() {
    setBusy(true)
    setError('')
    try {
      const run = await startReview({ deployment }, apiKey.trim())
      // The OpenAI key stays in React memory only and is cleared once handed off.
      setApiKey('')
      try { sessionStorage.setItem(RUN_STORAGE, JSON.stringify(run)) } catch { /* current tab still works */ }
      setAccess(run)
      setPage(1)
    } catch (e) { setError(e instanceof Error ? e.message : 'Could not start the review.') }
    finally { setBusy(false) }
  }

  async function stop() {
    if (!access) return
    setBusy(true)
    try { setReview(await cancelReview(access)); setPage(1); setError('') }
    catch { setError('Could not confirm cancellation. The review may still be running; try Stop review again.') }
    finally { setBusy(false) }
  }

  function restart() {
    try { sessionStorage.removeItem(RUN_STORAGE) } catch { /* no persistent storage */ }
    setAccess(null)
    setReview(null)
    setError('')
    setStep('access')
    setPage(1)
  }

  const active = access && (!review || ['preparing', 'running'].includes(review.status))

  return <div className="rd-root item-review-site">
    <SiteHeader />
    <div className="item-review-hero"><header className="rd-container">
      <a className="review-back" href={appPath('/')}><span aria-hidden="true">← </span>Choose an evaluation</a>
      <div className="review-hero-heading"><div><p className="eyebrow">Goal-conditioned auditing <span className="review-badge">Demo</span></p>
        <h1>Find tests that fit.</h1></div>
        <p>From your deployment context to relevant evaluation items, with evidence behind every judgment.</p></div>
    </header></div>
    <main className="rd-container item-review-main">
      <div className="review-layout">
        <aside className="review-guide">
          <p className="eyebrow">Your review</p>
          <ol className="review-steps">
            {['Connect your key', 'Describe deployment', 'Review and run', 'Inspect results'].map((label, i) => <li key={label}
              aria-current={(access ? 3 : ['access', 'deployment', 'confirm'].indexOf(step)) === i ? 'step' : undefined}>
              <span>{String(i + 1).padStart(2, '0')}</span>{label}</li>)}
          </ol>
          <div className="review-guide-note"><p className="eyebrow">The framework</p><strong>One item.<br />Six perspectives.</strong>
            <div className="review-guide-dimensions"><span>Input</span><span>Output</span><p>Ontology · Content · Form</p></div>
            <p>Every score includes a confidence judgment and the evidence behind it.</p>
            <small>GPT-6 Luna · High reasoning</small>
          </div>
        </aside>
        <div className="review-workspace" ref={workspace} tabIndex={-1}>
          {error && <div className="review-error" role="alert">{error}
            {!catalog && <p><button className="secondary" onClick={() => window.location.reload()}>Reload page</button></p>}
          </div>}
          {!catalog && !error && <p role="status">Loading the demo…</p>}

          {!access && catalog && step === 'access' && <form onSubmit={moveToDeployment} className="review-panel">
            <p className="eyebrow">01 · Connect</p><h2>Connect your OpenAI API key</h2>
            <p className="review-intro">Bring your own key to assess a broad, reproducible sample against your deployment. You’ll review the sample design and confirm before any paid calls begin.</p>
            {!catalog.dataset_access_configured && <div className="review-error" role="alert">Dataset access is not configured on this server. Please contact the site maintainer or try again later.</div>}
            <label className="review-field"><span>OpenAI API key</span><input type="password" autoComplete="off" spellCheck={false} maxLength={512}
              value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder="sk-…" required /></label>
            <div className="review-access-note"><strong>Your OpenAI key stays temporary.</strong><p>We send it to our backend and hold it in memory during your review. It is never saved to browser storage or our database.</p></div>
            <p className="help">The sample draws from {catalog.benchmarks.length} benchmark collections across both measurement-db branches. Starting a paid review sends your deployment description and selected item evidence to OpenAI.</p>
            <button type="submit" disabled={!apiKey.trim() || !catalog.dataset_access_configured}>Continue to deployment</button>
          </form>}

          {!access && catalog && step === 'deployment' && <form className="review-panel review-deployment" onSubmit={e => { e.preventDefault(); setStep('confirm') }}>
            <p className="eyebrow">02 · Your deployment</p><h2>What are you building?</h2>
            <p className="review-intro">Help us understand the real setting. Your answers guide what a relevant test should measure.</p>
            <div className="review-example"><div><strong>Need a starting point?</strong><p>Fill in a mathematics tutor scenario, then make it your own. Filling the form is free.</p></div>
              <button type="button" className="secondary" onClick={() => setDeployment(EXAMPLE)}>Use mathematics tutor example</button></div>
            <div className="review-questions">{QUESTIONS.map((q, i) => <div className={`review-question review-question-${q.id}`} key={q.id}>
              <span className="review-question-number" aria-hidden="true">{String(i + 1).padStart(2, '0')}</span>
              <div className="review-field"><label htmlFor={`deployment-${q.id}`}>{q.title}</label><p id={`hint-${q.id}`}>{q.hint}</p>
              <textarea id={`deployment-${q.id}`} aria-describedby={`hint-${q.id}`} placeholder={q.id === 'task' ? 'For example, an AI tutor helping secondary-school students learn mathematics…' : 'Describe what matters for your setting…'}
                value={deployment[q.id]} onChange={e => setDeployment({ ...deployment, [q.id]: e.target.value })}
                rows={3} required={q.id !== 'constraints'} minLength={q.id === 'task' ? 10 : q.id === 'constraints' ? 0 : 3} maxLength={q.id === 'task' ? 4000 : 2000} />
              </div>
            </div>)}</div>
            <p className="help">If a detail is unknown, say “unspecified.” The assessment will record the resulting uncertainty.</p>
            <div className="review-actions"><button type="button" className="secondary" onClick={() => setStep('access')}>Back</button><button type="submit">Review catalog and settings</button></div>
          </form>}

          {!access && catalog && step === 'confirm' && <section className="review-panel">
            <p className="eyebrow">03 · Review and run</p><h2>Review a broad item sample</h2>
            <p className="review-intro">The demo selects up to {catalog.sampling.items_per_benchmark} distinct items from every benchmark collection, then assesses each selected item across the six validity dimensions.</p>
            <div className="review-scope"><p className="eyebrow">Included in your review</p><strong>Up to {catalog.sample_max_items.toLocaleString()} <span>items</span></strong>
              <p>{catalog.benchmarks.length} benchmark collections · {catalog.table_count} item tables · {Object.keys(catalog.branches).length} branches</p>
              <p>The fixed random seed makes the sample reproducible. Duplicate evidence gets one chance of selection and is assessed once, with every source preserved. Both branches contribute when a benchmark has distinct items in each.</p>
              <div className="review-run-facts"><span>GPT-6 Luna</span><span>High reasoning</span><span>One call per distinct item</span></div>
              <p className="help">The full catalog contains {catalog.source_rows.toLocaleString()} source rows. The review uses selected item text, reference answers, and available metadata. Referenced images and audio are not inspected.</p></div>
            <details><summary>Browse all {catalog.benchmarks.length} benchmark collections</summary>
              <ul className="review-catalog">{catalog.benchmarks.map(b => <li key={b.id}><strong>{b.name}</strong><span>up to {b.sample_max_items} sampled · {b.source_rows.toLocaleString()} source rows</span></li>)}</ul>
            </details>
            <details><summary>How the sample is selected</summary>
              <p>Each benchmark contributes up to {catalog.sampling.items_per_benchmark} distinct items, or all its items if fewer are available. Items are drawn from across the collection after identical evidence and context are combined.</p>
              <p>We reserve a place for distinct evidence from each branch when available, then fill the remaining places randomly. Seed {catalog.sampling.seed} and the pinned dataset versions keep the selection consistent across deployment descriptions.</p>
              <p>Sample preparation makes no model calls and is cached for later reviews. Rankings describe this sample and may miss rare item types in the full catalog.</p>
            </details>
            {catalog.missing_item_tables.length > 0 && <p className="help">{catalog.missing_item_tables.length} branch directories have no formatted item table and cannot supply items.</p>}
            <details><summary>Your deployment description</summary>{QUESTIONS.map(q => <section key={q.id}><h4>{q.title}</h4><p className="review-preserve">{deployment[q.id] || 'Unspecified'}</p></section>)}</details>
            <p className="help">The review continues if this tab closes. Use Stop review to cancel. Results are kept in temporary server storage for one hour after completion and are discarded on a server restart. Download all results to keep them.</p>
            <p className="review-paid-note">Starting authorizes paid model calls for the selected sample after preparation completes.</p>
            <div className="review-actions"><button type="button" className="secondary" onClick={() => setStep('deployment')} disabled={busy}>Edit deployment</button>
              <button type="button" onClick={() => void start()} disabled={busy || catalog.table_count === 0}>{busy ? 'Starting…' : 'Start sampled review'}</button></div>
          </section>}

          {access && <>
            <section className="review-panel review-progress" aria-live="polite"><p className="eyebrow">04 · Results</p>
              <h2>{!review || review.status === 'preparing' ? 'Preparing the item sample' : review.status === 'running' ? 'Reviewing sampled items' : review.status === 'completed' ? 'Your item review is ready' : review.status === 'cancelled' ? 'Review stopped' : 'Review interrupted'}</h2>
              <p className="review-intro">{review?.message || 'Connecting to your review…'}</p>
              {review && review.status === 'preparing' && <><progress max={review.scope.source_rows || 1} value={review.source_rows} aria-label="Source rows considered for sampling" /><p>{review.prepared_benchmarks.toLocaleString()} of {review.scope.benchmarks.length.toLocaleString()} benchmark collections prepared · {review.source_rows.toLocaleString()} source rows considered · no model calls yet</p></>}
              {review && review.status !== 'preparing' && <><progress max={review.total || 1} value={review.processed} aria-label="Sampled items assessed" /><p>{review.processed.toLocaleString()} of {review.total.toLocaleString()} distinct sampled items assessed</p></>}
              {active ? <button type="button" className="secondary" onClick={() => void stop()} disabled={busy}>Stop review</button> : <button type="button" className="secondary" onClick={restart}>Start another review</button>}
              {active && <p className="help">You can return in this tab while the review runs. Stopping prevents further calls; an in-flight request may still incur charges.</p>}
              {error && <button type="button" className="link" onClick={restart}>Forget this review and return to setup</button>}
            </section>
            {review && <Results review={review} run={access} onPageChange={setPage} />}
          </>}
        </div>
      </div>
      <section className="review-privacy"><h2>Data and privacy</h2>
        <p>Your OpenAI API key is held in memory for the active review and is never saved to our database or browser storage. A separate temporary access token is stored in this tab so you can reload your results. Deployment answers stay in server memory; assessment results use private temporary server files. These are deleted one hour after the review ends or during a normal server shutdown. Results cannot be resumed after a server restart. The reusable dataset sample and source metadata are cached separately, without your deployment answers or API key. OpenAI processes the submitted text under its own API data policies.</p>
      </section>
    </main><SiteFooter />
  </div>
}
