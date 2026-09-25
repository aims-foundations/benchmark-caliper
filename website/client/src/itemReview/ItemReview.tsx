import { useEffect, useState, type FormEvent } from 'react'
import { SiteHeader } from '../components/SiteHeader'
import { SiteFooter } from '../components/SiteFooter'
import { MatrixBackdrop } from '../components/MatrixBackdrop'
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
  const [hfToken, setHfToken] = useState('')
  const [deployment, setDeployment] = useState<Deployment>(EMPTY)
  const [benchmarks, setBenchmarks] = useState(['matharena', 'afrimedqa'])
  const [limit, setLimit] = useState(2)
  const [access, setAccess] = useState<RunAccess | null>(savedRun)
  const [review, setReview] = useState<Review | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

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
        const latest = await getReview(access!, controller.signal)
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
  }, [access])

  function moveToDeployment(e: FormEvent) {
    e.preventDefault()
    if (!apiKey.trim() || (catalog?.requires_hf_token && !hfToken.trim())) return
    setError('')
    setStep('deployment')
  }

  async function start() {
    setBusy(true)
    setError('')
    try {
      const run = await startReview({ deployment, benchmarks, items_per_table: limit, top_k: 10 }, apiKey.trim(), hfToken.trim())
      // Credentials stay in React memory only and are cleared once handed off.
      setApiKey('')
      setHfToken('')
      try { sessionStorage.setItem(RUN_STORAGE, JSON.stringify(run)) } catch { /* current tab still works */ }
      setAccess(run)
    } catch (e) { setError(e instanceof Error ? e.message : 'Could not start the review.') }
    finally { setBusy(false) }
  }

  async function stop() {
    if (!access) return
    setBusy(true)
    try { setReview(await cancelReview(access)); setError('') }
    catch { setError('Could not confirm cancellation. The review may still be running; try Stop review again.') }
    finally { setBusy(false) }
  }

  function restart() {
    try { sessionStorage.removeItem(RUN_STORAGE) } catch { /* no persistent storage */ }
    setAccess(null)
    setReview(null)
    setError('')
    setStep('access')
  }

  const maxRows = (catalog?.benchmarks.filter(b => benchmarks.includes(b.id)).reduce((total, b) => total + b.table_count, 0) ?? 0) * limit
  const active = access && (!review || ['preparing', 'running'].includes(review.status))

  return <div className="rd-root">
    <SiteHeader />
    <div className="rd-page-hero item-review-hero"><MatrixBackdrop /><header className="rd-container">
      <p className="eyebrow">AIMS · Goal-conditioned auditing <span className="review-badge">Demo</span></p>
      <h1 className="rd-page-title">Find tests that fit.</h1>
      <p className="rd-lead">Describe your AI deployment. Review evaluation items through six dimensions of validity.</p>
      <div className="hero-actions"><a className="rd-btn" href={appPath('/')}>Choose an evaluation</a></div>
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
          <div className="review-guide-note"><strong>One item. Six perspectives.</strong>
            <p>Input and output, each examined through ontology, content, and form.</p>
            <p>GPT-6 Luna · High reasoning effort</p>
          </div>
        </aside>
        <div className="review-workspace">
          {error && <div className="review-error" role="alert">{error}
            {!catalog && <p><button className="secondary" onClick={() => window.location.reload()}>Reload page</button></p>}
          </div>}
          {!catalog && !error && <p role="status">Loading the demo…</p>}

          {!access && catalog && step === 'access' && <form onSubmit={moveToDeployment} className="review-panel">
            <p className="eyebrow">01 · Access</p><h2>Connect your OpenAI API key</h2>
            <p>Your key pays for the item assessments. We send it to our backend to call OpenAI, keep it in memory while your review runs, and never save it to browser storage or our database.</p>
            <label className="review-field"><span>OpenAI API key</span><input type="password" autoComplete="off" spellCheck={false} maxLength={512}
              value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder="sk-…" required /></label>
            <details open={catalog.requires_hf_token} className="review-dataset-access"><summary>Hugging Face dataset access{catalog.requires_hf_token ? ' · required' : ' · optional override'}</summary>
              <p>This dataset requires an authorized Hugging Face account. {catalog.requires_hf_token ? 'The demo server has no dataset token configured. Enter a read token from an account with measurement-db access.' : 'The server has dataset access configured. You can supply your own read token if needed.'}</p>
              <p><a href="https://huggingface.co/datasets/aims-foundations/measurement-db" target="_blank" rel="noreferrer">Open measurement-db</a></p>
              <label className="review-field"><span>Hugging Face read token</span><input type="password" autoComplete="off" spellCheck={false} maxLength={512}
                value={hfToken} onChange={e => setHfToken(e.target.value)} placeholder="hf_…" required={catalog.requires_hf_token} /></label>
            </details>
            <p className="help">The first demo reviews a small text sample from MathArena and AfriMed-QA. Your deployment description and selected item evidence are sent to OpenAI when you start the paid review.</p>
            <button type="submit" disabled={!apiKey.trim() || (catalog.requires_hf_token && !hfToken.trim())}>Continue to deployment</button>
          </form>}

          {!access && catalog && step === 'deployment' && <form className="review-panel" onSubmit={e => { e.preventDefault(); setStep('confirm') }}>
            <p className="eyebrow">02 · Deployment</p><h2>What are you building?</h2>
            <p>These questions define what makes an item relevant. Be concrete where possible; unknown details can stay unspecified.</p>
            <button type="button" className="secondary" onClick={() => setDeployment(EXAMPLE)}>Use mathematics tutor example</button>
            {QUESTIONS.map(q => <label className="review-field" key={q.id}><span>{q.title}</span><small>{q.hint}</small>
              <textarea value={deployment[q.id]} onChange={e => setDeployment({ ...deployment, [q.id]: e.target.value })}
                rows={3} required={q.id !== 'constraints'} minLength={q.id === 'task' ? 10 : q.id === 'constraints' ? 0 : 3} maxLength={q.id === 'task' ? 4000 : 2000} />
            </label>)}
            <div className="review-actions"><button type="button" className="secondary" onClick={() => setStep('access')}>Back</button><button type="submit">Review sample and settings</button></div>
          </form>}

          {!access && catalog && step === 'confirm' && <section className="review-panel">
            <p className="eyebrow">03 · Review and run</p><h2>Choose a small starting sample</h2>
            <p>This is a deterministic preview using the first items in each selected table. It does not search the full dataset or provide a representative sample.</p>
            <fieldset className="review-benchmarks"><legend>Evaluation items</legend>{catalog.benchmarks.map(b => <label className="checkbox" key={b.id}>
              <input type="checkbox" checked={benchmarks.includes(b.id)} onChange={e => setBenchmarks(e.target.checked ? [...benchmarks, b.id] : benchmarks.filter(id => id !== b.id))} />
              <span>{b.name} <small>({b.table_count} {b.table_count === 1 ? 'table' : 'tables'})</small></span>
            </label>)}</fieldset>
            <label className="review-field"><span>Items from each table</span><select value={limit} onChange={e => setLimit(Number(e.target.value))}>
              {[1, 2, 5, 10].map(n => <option key={n} value={n}>{n}</option>)}
            </select></label>
            <div className="review-scope"><strong>Up to {maxRows} source rows</strong><p>Identical items with identical context are assessed once. Each distinct item uses one GPT-6 Luna call with high reasoning effort. API charges apply to your key.</p>
              <p>The catalog includes both measurement-db branches. MathArena appears in both; AfriMed-QA is in the migration branch. Images and audio are not inspected in this demo.</p></div>
            <details><summary>Your deployment description</summary>{QUESTIONS.map(q => <section key={q.id}><h4>{q.title}</h4><p className="review-preserve">{deployment[q.id] || 'Unspecified'}</p></section>)}</details>
            <p className="help">The review continues if this tab closes. Use Stop review to cancel. Results are held in server memory for one hour after completion and disappear on a server restart. Download the JSON to keep them.</p>
            <div className="review-actions"><button type="button" className="secondary" onClick={() => setStep('deployment')} disabled={busy}>Edit deployment</button>
              <button type="button" onClick={() => void start()} disabled={busy || benchmarks.length === 0}>{busy ? 'Starting…' : 'Start paid review'}</button></div>
          </section>}

          {access && <>
            <section className="review-panel review-progress" aria-live="polite"><p className="eyebrow">04 · Results</p>
              <h2>{!review || review.status === 'preparing' ? 'Preparing your sample' : review.status === 'running' ? 'Reviewing evaluation items' : review.status === 'completed' ? 'Your sample review is ready' : review.status === 'cancelled' ? 'Review stopped' : 'Review interrupted'}</h2>
              <p>{review?.message || 'Connecting to your review…'}</p>
              {review && <><progress max={review.total || 1} value={review.processed} aria-label="Items assessed" /><p>{review.processed} of {review.total} distinct items assessed · {review.source_rows} source rows</p></>}
              {active ? <button type="button" className="secondary" onClick={() => void stop()} disabled={busy}>Stop review</button> : <button type="button" className="secondary" onClick={restart}>Start another review</button>}
              {active && <p className="help">You can return in this tab while the review runs. Stopping prevents further calls; an in-flight request may still incur charges.</p>}
              {error && <button type="button" className="link" onClick={restart}>Forget this review and return to setup</button>}
            </section>
            {review && <Results review={review} />}
          </>}
        </div>
      </div>
      <section className="review-privacy"><h2>Data and privacy</h2>
        <p>OpenAI and Hugging Face keys are held in memory for the active review and are never saved to our database or browser storage. A separate temporary access token is stored in this tab so you can reload your results. Deployment answers and assessments are held in server memory for one hour after completion; source dataset files may be cached on the server. OpenAI processes the submitted text under its own API data policies.</p>
      </section>
    </main><SiteFooter />
  </div>
}
