import { useEffect, useRef, useState, type FormEvent } from 'react'
import { SiteHeader } from '../components/SiteHeader'
import { SiteFooter } from '../components/SiteFooter'
import { appPath } from '../paths'
import { cancelReview, getCatalog, getReview, startReview, startGrounding, startBenchmarkRetrieval, startScreening, startSelection, type Catalog, type Deployment, type RunResult, type RunAccess } from './api'
import { Results } from './Results'
import { RequirementsResults } from './RequirementsResults'
import { GroundingResults } from './GroundingResults'
import { BenchmarkRetrievalResults } from './BenchmarkRetrievalResults'
import { ScreeningResults } from './ScreeningResults'
import { SelectionResults } from './SelectionResults'
import { QUESTIONS } from './deployment'

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
  const [retrieveK, setRetrieveK] = useState('20')
  const [retrievalQuery, setRetrievalQuery] = useState('')
  const [page, setPage] = useState(1)
  const [access, setAccess] = useState<RunAccess | null>(savedRun)
  const [review, setReview] = useState<RunResult | null>(null)
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
    getCatalog(controller.signal).then(data => {
      setCatalog(data)
      setRetrieveK(String(data.default_retrieve_k))
    }).catch(e => {
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
    if (!apiKey.trim()) return
    setError('')
    setStep('deployment')
  }

  async function start(mode: 'item_review' | 'requirements' = 'item_review') {
    if (busy || !apiKey.trim()) return
    if (mode === 'item_review' && (!catalog?.dataset_access_configured || !validRetrieveK)) return
    setBusy(true)
    setError('')
    try {
      const run = await startReview(mode === 'requirements' ? { deployment, mode }
        : { deployment, retrieve_k: Number(retrieveK), ...(retrievalQuery.trim() ? { retrieval_query: retrievalQuery } : {}) }, apiKey.trim())
      // The OpenAI key stays in React memory only and is cleared once handed off.
      setApiKey('')
      try { sessionStorage.setItem(RUN_STORAGE, JSON.stringify(run)) } catch { /* current tab still works */ }
      setAccess(run)
      setReview(null)
      setPage(1)
    } catch (e) { setError(e instanceof Error ? e.message : 'Could not start the run.') }
    finally { setBusy(false) }
  }

  async function ground(key: string): Promise<boolean> {
    if (!access || busy) return false
    setBusy(true)
    setError('')
    try {
      const run = await startGrounding(access, key)
      try { sessionStorage.setItem(RUN_STORAGE, JSON.stringify(run)) } catch { /* current tab still works */ }
      setReview(null)
      setAccess(run)
      setPage(1)
      return true
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Could not start O*NET grounding.')
      return false
    } finally { setBusy(false) }
  }

  async function retrieve(): Promise<boolean> {
    if (!access || busy || !catalog?.dataset_access_configured || catalog.table_count === 0) return false
    setBusy(true)
    setError('')
    try {
      const run = await startBenchmarkRetrieval(access)
      try { sessionStorage.setItem(RUN_STORAGE, JSON.stringify(run)) } catch { /* current tab still works */ }
      setReview(null)
      setAccess(run)
      setPage(1)
      return true
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Could not start benchmark retrieval.')
      return false
    } finally { setBusy(false) }
  }

  async function screen(key: string): Promise<boolean> {
    if (!access || busy) return false
    setBusy(true)
    setError('')
    try {
      const run = await startScreening(access, key)
      try { sessionStorage.setItem(RUN_STORAGE, JSON.stringify(run)) } catch { /* current tab still works */ }
      setReview(null)
      setAccess(run)
      setPage(1)
      return true
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Could not start initial screening.')
      return false
    } finally { setBusy(false) }
  }

  async function select(): Promise<boolean> {
    if (!access || busy) return false
    setBusy(true)
    setError('')
    try {
      const run = await startSelection(access)
      try { sessionStorage.setItem(RUN_STORAGE, JSON.stringify(run)) } catch { /* current tab still works */ }
      setReview(null)
      setAccess(run)
      setPage(1)
      return true
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Could not start collection selection.')
      return false
    } finally { setBusy(false) }
  }

  function submitDeployment(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const submitter = (e.nativeEvent as SubmitEvent).submitter
    if (submitter instanceof HTMLButtonElement && submitter.value === 'requirements') void start('requirements')
    else setStep('confirm')
  }

  async function stop() {
    if (!access) return
    setBusy(true)
    try { setReview(await cancelReview(access)); setPage(1); setError('') }
    catch { setError('Could not confirm cancellation. The run may still be running; please try stopping it again.') }
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
  const validRetrieveK = !!catalog && Number.isInteger(Number(retrieveK)) && Number(retrieveK) >= 1 && Number(retrieveK) <= catalog.max_retrieve_k

  return <div className="rd-root item-review-site">
    <SiteHeader />
    <div className="item-review-hero"><header className="rd-container">
      <a className="review-back" href={appPath('/')}><span aria-hidden="true">← </span>Choose an evaluation</a>
      <div className="review-hero-heading"><div><p className="eyebrow">Goal-conditioned auditing <span className="review-badge">Demo</span></p>
        <h1>Find tests that fit.</h1></div>
        <p>Describe your deployment, inspect extracted requirements, or retrieve and assess candidate test items.</p></div>
    </header></div>
    <main className="rd-container item-review-main">
      <div className="review-layout">
        <aside className="review-guide">
          <p className="eyebrow">Your review</p>
          <ol className="review-steps">
            {['Connect your key', 'Describe deployment', 'Choose an action', 'Inspect results'].map((label, i) => <li key={label}
              aria-current={(access ? 3 : ['access', 'deployment', 'confirm'].indexOf(step)) === i ? 'step' : undefined}>
              <span>{String(i + 1).padStart(2, '0')}</span>{label}</li>)}
          </ol>
          {!access && <div className="review-guide-note"><p className="eyebrow">The framework</p><strong>Start with your deployment.</strong>
            <div className="review-guide-dimensions"><span>Input</span><span>Output</span><p>Ontology · Content · Form</p></div>
            <p>Extract requirements to inspect your goal, or use local retrieval and six-dimension item assessment.</p>
            <small>Extraction and item assessment use paid GPT-6 Luna calls.</small>
          </div>}
        </aside>
        <div className="review-workspace" ref={workspace} tabIndex={-1}>
          {error && <div className="review-error" role="alert">{error}
            {!catalog && <p><button className="secondary" onClick={() => window.location.reload()}>Reload page</button></p>}
          </div>}
          {!catalog && !error && <p role="status">Loading the demo…</p>}

          {!access && catalog && step === 'access' && <form onSubmit={moveToDeployment} className="review-panel">
            <p className="eyebrow">01 · Connect</p><h2>Connect your OpenAI API key</h2>
            <p className="review-intro">Bring your own key to extract requirements from your deployment answers or assess a shortlist of benchmark items. You’ll choose an action before any paid calls begin.</p>
            {!catalog.dataset_access_configured && <div className="review-error" role="alert">Dataset access is not configured on this server. Requirements extraction is available; item retrieval and assessment are unavailable.</div>}
            <label className="review-field"><span>OpenAI API key</span><input type="password" autoComplete="off" spellCheck={false} maxLength={512}
              value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder="sk-…" required /></label>
            <div className="review-access-note"><strong>Your OpenAI key stays temporary.</strong><p>We send it to our backend and hold it in memory during your review. It is never saved to browser storage or our database.</p></div>
            <p className="help">Requirements extraction sends your six answers to OpenAI in one paid call. Item review retrieves locally from {catalog.benchmarks.length} benchmark collections, then sends your deployment description and shortlisted item evidence to OpenAI for paid assessment.</p>
            <button type="submit" disabled={!apiKey.trim()}>Continue to deployment</button>
          </form>}

          {!access && catalog && step === 'deployment' && <form className="review-panel review-deployment" onSubmit={submitDeployment}>
            <p className="eyebrow">02 · Your deployment</p><h2>What are you building?</h2>
            <p className="review-intro">Help us understand the real setting. Your answers guide what a relevant test should measure.</p>
            <div className="review-example"><div><strong>Need a starting point?</strong><p>Fill in a mathematics tutor scenario, then make it your own. Filling the form is free.</p></div>
              <button type="button" className="secondary" disabled={busy} onClick={() => setDeployment(EXAMPLE)}>Use mathematics tutor example</button></div>
            <div className="review-questions">{QUESTIONS.map((q, i) => <div className={`review-question review-question-${q.id}`} key={q.id}>
              <span className="review-question-number" aria-hidden="true">{String(i + 1).padStart(2, '0')}</span>
              <div className="review-field"><label htmlFor={`deployment-${q.id}`}>{q.title}</label><p id={`hint-${q.id}`}>{q.hint}</p>
              <textarea id={`deployment-${q.id}`} aria-describedby={`hint-${q.id}`} placeholder={q.id === 'task' ? 'For example, an AI tutor helping secondary-school students learn mathematics…' : 'Describe what matters for your setting…'}
                value={deployment[q.id]} onChange={e => setDeployment({ ...deployment, [q.id]: e.target.value })}
                rows={3} required={q.id !== 'constraints'} disabled={busy} />
              </div>
            </div>)}</div>
            <p className="help">If a detail is unknown, say “unspecified.” The extraction or assessment will record the resulting uncertainty.</p>
            <p className="review-paid-note">Extract requirements starts one paid GPT-6 Luna call using your six answers. The preview shows the deployment summary, task facets, source quotations, coverage requirements, and unresolved details.</p>
            <div className="review-actions"><button type="button" className="secondary" disabled={busy} onClick={() => setStep('access')}>Back</button>
              <button type="submit" name="action" value="requirements" disabled={busy}>{busy ? 'Starting…' : 'Extract requirements'}</button>
              <button type="submit" className="secondary" name="action" value="item_review" disabled={busy}>Review catalog and settings</button></div>
          </form>}

          {!access && catalog && step === 'confirm' && <section className="review-panel">
            <p className="eyebrow">03 · Review and run</p><h2>Retrieve candidates, then assess the shortlist</h2>
            <p className="review-intro">The demo selects up to {catalog.sampling.items_per_benchmark} distinct items from every benchmark collection. Local retrieval narrows this sample to your chosen shortlist; GPT-6 Luna then assesses each shortlisted item across all six validity dimensions.</p>
            <div className="review-scope"><p className="eyebrow">Available for local retrieval</p><strong>Up to {catalog.sample_max_items.toLocaleString()} <span>items</span></strong>
              <p>{catalog.benchmarks.length} benchmark collections · {catalog.table_count} item tables · {Object.keys(catalog.branches).length} branches</p>
              <p>The fixed random seed makes the sample reproducible. Duplicate evidence gets one chance of selection and is indexed once, with every source preserved. Both branches contribute when a benchmark has distinct items in each.</p>
              <div className="review-run-facts"><span>Local Qwen3 retrieval</span><span>GPT-6 Luna · High reasoning</span><span>One judgment per shortlisted item</span></div>
              <p className="help">The full catalog contains {catalog.source_rows.toLocaleString()} source rows. The review uses selected item text, reference answers, and available metadata. Referenced images and audio are not inspected.</p></div>
            <details><summary>Browse all {catalog.benchmarks.length} benchmark collections</summary>
              <ul className="review-catalog">{catalog.benchmarks.map(b => <li key={b.id}><strong>{b.name}</strong><span>up to {b.sample_max_items} sampled · {b.source_rows.toLocaleString()} source rows</span></li>)}</ul>
            </details>
            <div className="review-field"><label htmlFor="retrieve-k">Maximum items to assess</label>
              <p className="help" id="retrieve-k-hint">Choose 1–{catalog.max_retrieve_k} items. A smaller shortlist reduces paid assessments; the default is {catalog.default_retrieve_k}.</p>
              <input id="retrieve-k" type="number" min={1} max={catalog.max_retrieve_k} step={1} value={retrieveK}
                aria-describedby="retrieve-k-hint" onChange={e => setRetrieveK(e.target.value)} required />
            </div>
            <div className="review-field"><label htmlFor="retrieval-query">Reference question (optional)</label>
              <p className="help" id="retrieval-query-hint">Paste an exact question or describe a question to retrieve similar items. Leave this blank to use your deployment description. The deployment still guides all six validity judgments.</p>
              <textarea id="retrieval-query" rows={4} value={retrievalQuery} maxLength={100000}
                aria-describedby="retrieval-query-hint" placeholder="Paste the question you want to find, or describe a relevant evaluation item…"
                onChange={e => setRetrievalQuery(e.target.value)} />
            </div>
            <details><summary>How retrieval selects the shortlist</summary>
              <p>Qwen3-Embedding-0.6B runs locally. Query and item embeddings are normalized and compared using dot products, with up to {catalog.retrieval_policy.max_tokens.toLocaleString()} tokens per text. Longer text is truncated for embedding; the original item evidence remains available for assessment.</p>
              <p>Exact question text matches are selected first, followed by the most similar items. Semantic similarity helps find candidates; it does not establish that related questions, numbers, or answer choices are equivalent.</p>
              <p>The final report ranks the assessed shortlist by its confidence-adjusted six-dimension validity score, independently of retrieval rank. Relevant items outside the sample or shortlist may be missed.</p>
            </details>
            <details><summary>How the sample is selected</summary>
              <p>Each benchmark contributes up to {catalog.sampling.items_per_benchmark} distinct items, or all its items if fewer are available. Items are drawn from across the collection after identical evidence and context are combined.</p>
              <p>We reserve a place for distinct evidence from each branch when available, then fill the remaining places randomly. Seed {catalog.sampling.seed} and the pinned dataset versions keep the selection consistent across deployment descriptions.</p>
              <p>Sample preparation makes no model calls and is cached for later reviews. Rankings describe this sample and may miss rare item types in the full catalog.</p>
            </details>
            {catalog.missing_item_tables.length > 0 && <p className="help">{catalog.missing_item_tables.length} branch directories have no formatted item table and cannot supply items.</p>}
            <details><summary>Your deployment description</summary>{QUESTIONS.map(q => <section key={q.id}><h4>{q.title}</h4><p className="review-preserve">{deployment[q.id] || 'Unspecified'}</p></section>)}</details>
            <p className="help">The review continues if this tab closes. Use Stop review to cancel. Results are kept in temporary server storage for one hour after completion and are discarded on a server restart. Download all results to keep them.</p>
            <p className="review-paid-note">Starting authorizes paid GPT-6 Luna assessments for up to {validRetrieveK ? Number(retrieveK) : 'your chosen number of'} retrieved items after local retrieval completes.</p>
            {!catalog.dataset_access_configured && <p className="review-error" role="alert">Dataset access is not configured on this server. Return to your deployment to extract requirements.</p>}
            <div className="review-actions"><button type="button" className="secondary" onClick={() => setStep('deployment')} disabled={busy}>Edit deployment</button>
              <button type="button" onClick={() => void start()} disabled={busy || !catalog.dataset_access_configured || catalog.table_count === 0 || !validRetrieveK}>{busy ? 'Starting…' : 'Retrieve and assess shortlist'}</button></div>
          </section>}

          {access && review?.mode === 'requirements' && <RequirementsResults review={review} run={access} busy={busy} onCancel={() => void stop()} onRestart={restart} onGround={ground} />}
          {access && review?.mode === 'grounding' && <GroundingResults review={review} run={access} catalog={catalog} busy={busy} onCancel={() => void stop()} onRestart={restart} onGround={ground} onRetrieve={retrieve} />}
          {access && review?.mode === 'retrieval' && <BenchmarkRetrievalResults key={access.run_id} review={review} run={access} catalog={catalog} busy={busy} onCancel={() => void stop()} onRestart={restart} onRetrieve={retrieve} onScreen={screen} />}
          {access && review?.mode === 'screening' && <ScreeningResults key={access.run_id} review={review} run={access} busy={busy} onCancel={() => void stop()} onRestart={restart} onScreen={screen} onSelect={select} />}
          {access && review?.mode === 'selection' && <SelectionResults key={access.run_id} review={review} run={access} busy={busy} onCancel={() => void stop()} onRestart={restart} onScreen={screen} onSelect={select} />}
          {access && review?.mode !== 'requirements' && review?.mode !== 'grounding' && review?.mode !== 'retrieval' && review?.mode !== 'screening' && review?.mode !== 'selection' && <>
            <section className="review-panel review-progress" aria-live="polite"><p className="eyebrow">04 · Results</p>
              <h2>{!review ? 'Connecting to your run' : review.status === 'preparing' ? 'Preparing and retrieving candidate items' : review.status === 'running' ? 'Assessing shortlisted items' : review.status === 'completed' ? 'Your item review is ready' : review.status === 'cancelled' ? 'Review stopped' : 'Review interrupted'}</h2>
              <p className="review-intro">{review?.message || 'Connecting to your review…'}</p>
              {review && review.status === 'preparing' && <><progress max={review.scope.source_rows || 1} value={review.source_rows} aria-label="Source rows considered for sampling" /><p>{review.prepared_benchmarks.toLocaleString()} of {review.scope.benchmarks.length.toLocaleString()} benchmark collections prepared · {review.source_rows.toLocaleString()} source rows considered · no paid model calls yet</p></>}
              {review && review.status === 'preparing' && <p className="help">Preparing the local index and retrieving candidates. Paid judgments start after the shortlist is selected.</p>}
              {review?.indexed_items != null && review.retrieved_items != null && <p>{review.indexed_items.toLocaleString()} sampled items indexed · {review.retrieved_items.toLocaleString()} items shortlisted</p>}
              {review && review.status !== 'preparing' && <><progress max={review.total || 1} value={review.processed} aria-label="Shortlisted items assessed" /><p>{review.processed.toLocaleString()} of {review.total.toLocaleString()} shortlisted items assessed</p></>}
              {active ? <button type="button" className="secondary" onClick={() => void stop()} disabled={busy}>Stop review</button> : <button type="button" className="secondary" onClick={restart}>Start another review</button>}
              {active && <p className="help">Stopping cancels pending assessments. Requests already sent may still incur charges.</p>}
              {error && <button type="button" className="link" onClick={restart}>Forget this review and return to setup</button>}
            </section>
            {review && <Results review={review} run={access} onPageChange={setPage} />}
          </>}
        </div>
      </div>
      <section className="review-privacy"><h2>Data and privacy</h2>
        <p>Your OpenAI API key is held in memory for the active review and is never saved to our database or browser storage. A separate temporary access token is stored in this tab so you can reload your results. Deployment answers stay in server memory; item results use private temporary server files. These are deleted one hour after the review ends or during a normal server shutdown. Results cannot be resumed after a server restart. Reusable dataset indexes, samples, and source metadata are cached separately, without your deployment answers or API key. OpenAI processes the submitted text under its own API data policies.</p>
      </section>
    </main><SiteFooter />
  </div>
}
