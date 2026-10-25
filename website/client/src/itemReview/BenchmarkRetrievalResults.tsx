import { useEffect, useState } from 'react'
import { getCandidates, getReviewExport, type BenchmarkRetrievalReview, type CandidatePage, type Catalog, type RunAccess } from './api'
import { BenchmarkRetrievalForm } from './BenchmarkRetrievalForm'
import { RequirementsContent, SupportedValue } from './RequirementsResults'
import { ScreeningForm } from './ScreeningForm'

function CandidateBrowser({ review, run, catalog }: { review: BenchmarkRetrievalReview; run: RunAccess; catalog: Catalog | null }) {
  const queues = review.retrieval?.queues ?? []
  const [selectedQueue, setSelectedQueue] = useState('')
  const [page, setPage] = useState(1)
  const [result, setResult] = useState<CandidatePage | null>(null)
  const [error, setError] = useState('')
  const [retry, setRetry] = useState(0)
  const queueId = queues.find(queue => queue.queue_id === selectedQueue)?.queue_id ?? queues[0]?.queue_id

  useEffect(() => {
    if (!queueId) return
    const controller = new AbortController()
    setResult(null)
    setError('')
    getCandidates(run, queueId, page, controller.signal).then(data => {
      if (!controller.signal.aborted) setResult(data)
    }).catch(error => {
      if (!controller.signal.aborted) setError(error instanceof Error ? error.message : 'Could not load candidates.')
    })
    return () => controller.abort()
  }, [run, queueId, page, retry])

  if (!queueId) return null
  const facetIds = [...new Set(queues.map(queue => queue.facet_id))]
  return <section className="review-panel" aria-labelledby="retrieval-candidates-title">
    <h2 id="retrieval-candidates-title">Candidate items</h2>
    <p>Browse the combined ranking for a task or its subset from one collection. An item can appear in several task queues. These are retrieval ranks, not validity scores or final selections.</p>
    <div className="review-field"><label htmlFor="candidate-queue">Candidate queue</label>
      <select id="candidate-queue" value={queueId} onChange={event => { setSelectedQueue(event.target.value); setPage(1) }}>
        {facetIds.map(id => <optgroup key={id} label={`Task ${(review.requirements?.task_facets.findIndex(facet => facet.facet_id === id) ?? -1) + 1}`}>
          {queues.filter(queue => queue.facet_id === id).map(queue => <option key={queue.queue_id} value={queue.queue_id}>
            {queue.source == null ? 'Whole bank' : catalog?.benchmarks.find(benchmark => benchmark.id === queue.source)?.name ?? queue.source} · {queue.item_count.toLocaleString()} items
          </option>)}
        </optgroup>)}
      </select>
    </div>
    {error && <div className="review-error" role="alert"><p>{error}</p><button type="button" className="secondary" onClick={() => setRetry(value => value + 1)}>Retry loading candidates</button></div>}
    {!result && !error && <p role="status">Loading candidate items…</p>}
    {result && <>
      <p>{result.total_items.toLocaleString()} candidate items in this queue.</p>
      {result.items.length === 0 && <p>No candidates are available in this queue.</p>}
      {result.items.map(item => <article key={item.item_id} className="retrieval-candidate" aria-labelledby={`candidate-${item.item_id}`}>
        <h3 id={`candidate-${item.item_id}`}>Candidate {item.rank}</h3>
        <p className="review-preserve">{item.question_text || 'This item has no separately labeled question. Its full source row is available below.'}</p>
        <p><strong>Sources:</strong> {[...new Set(item.sources.map(source => source.benchmark))].join(', ') || 'No source label supplied'}</p>
        <p className="help">Combined rank: {item.rank} · Meaning search rank: {item.dense_rank ?? 'Not ranked'} · Keyword rank: {item.bm25_rank ?? 'Not ranked'}</p>
        <details><summary>Inspect full item evidence and sources</summary>
          <p className="help">Item ID: <code>{item.item_id}</code> · Evidence hash: <code>{item.evidence_hash}</code></p>
          <p className="help">Combined ranking score: {item.rrf_score.toFixed(6)} · Meaning score: {item.dense_score ?? 'Not ranked'} · Keyword score: {item.bm25_score ?? 'Not ranked'}</p>
          <h4>Full row text used for search</h4><pre>{item.search_text}</pre>
          <h4>Original item evidence</h4><pre>{JSON.stringify(item.evidence, null, 2)}</pre>
          <h4>Source provenance</h4><pre>{JSON.stringify(item.sources, null, 2)}</pre>
        </details>
      </article>)}
      {result.total_pages > 1 && <nav className="review-actions" aria-label="Candidate pages">
        <button type="button" className="secondary" disabled={result.page <= 1} onClick={() => setPage(result.page - 1)}>Previous candidates</button>
        <span>Page {result.page} of {result.total_pages}</span>
        <button type="button" className="secondary" disabled={result.page >= result.total_pages} onClick={() => setPage(result.page + 1)}>Next candidates</button>
      </nav>}
    </>}
  </section>
}

export function BenchmarkRetrievalResults({ review, run, catalog, busy, onCancel, onRestart, onRetrieve, onScreen }: {
  review: BenchmarkRetrievalReview; run: RunAccess; catalog: Catalog | null; busy: boolean
  onCancel: () => void; onRestart: () => void; onRetrieve: () => Promise<boolean>
  onScreen: (apiKey: string) => Promise<boolean>
}) {
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const active = ['preparing', 'running'].includes(review.status)
  const retrieval = review.retrieval
  const facets = review.requirements?.task_facets ?? []
  const completedQueries = retrieval?.queries.filter(query => typeof query.candidate_count === 'number').length ?? 0
  const canRetry = facets.length > 0 && facets.every(facet => review.grounding?.facets.some(mapping => mapping.facet_id === facet.facet_id && mapping.status === 'complete' && mapping.mapping != null))

  async function download() {
    setDownloading(true)
    setDownloadError('')
    try {
      const url = URL.createObjectURL(await getReviewExport(run))
      const link = document.createElement('a')
      link.href = url
      link.download = `benchmark-retrieval-${run.run_id}.json`
      link.click()
      setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (error) {
      setDownloadError(error instanceof Error ? error.message : 'Could not download retrieval results. Please try again.')
    } finally { setDownloading(false) }
  }

  return <div className="retrieval-results">
    <section className="review-panel review-progress" aria-live="polite">
      <p className="eyebrow">Step 4 · Retrieve benchmark items</p>
      <h2>{active ? 'Retrieving benchmark candidates' : review.status === 'completed' ? 'Your benchmark candidates are ready' : review.status === 'cancelled' ? 'Retrieval stopped' : 'Retrieval interrupted'}</h2>
      <p className="review-intro" role={review.status === 'failed' ? 'alert' : undefined}>{review.message}</p>
      <p>Local meaning-based and keyword search makes no paid model calls. Candidates await relevance screening and benchmark selection in later steps.</p>
      {retrieval && <>
        <p>{retrieval.scope.benchmarks.length} benchmark collections · {retrieval.scope.source_rows.toLocaleString()} source rows · whole main-branch bank</p>
        <p>{(retrieval.stats.source_rows ?? 0).toLocaleString()} source rows read · {(retrieval.stats.total_items ?? 0).toLocaleString()} distinct full rows · {(retrieval.stats.indexed_items ?? 0).toLocaleString()} searchable items · {(retrieval.stats.contentless_items ?? 0).toLocaleString()} items without searchable row data</p>
        <p>{completedQueries} of {facets.length} task queries completed.</p>
        {active && <progress max={facets.length || 1} value={completedQueries} aria-label="Task queries completed" />}
      </>}
      {active && <p className="help">The first index build can take time; cached indexes are reused. Stopping retains queues from completed task queries.</p>}
      {['cancelled', 'failed'].includes(review.status) && <p>Completed task queues remain available below and in the export. You can retry using the retained requirements and O*NET mappings.</p>}
      <div className="review-actions">
        {active ? <button type="button" className="secondary" disabled={busy} onClick={onCancel}>Stop retrieval</button>
          : <button type="button" className="secondary" disabled={busy} onClick={onRestart}>Start another run</button>}
        <button type="button" className="secondary" disabled={downloading} onClick={() => void download()}>{downloading ? 'Downloading…' : 'Download retrieval JSON'}</button>
      </div>
      <p className="help">Results expire one hour after the run ends. The JSON export includes all completed candidate rankings and their evidence, original answers, requirements, and O*NET mappings.</p>
      {downloadError && <p className="review-error" role="alert">{downloadError}</p>}
    </section>
    {review.status === 'completed' && retrieval?.queues.some(queue => queue.source == null && queue.item_count > 0) && <ScreeningForm busy={busy} onScreen={onScreen} />}
    {retrieval && <section className="review-panel" aria-labelledby="retrieval-queries-title">
      <h2 id="retrieval-queries-title">Task search queries</h2>
      {retrieval.queries.length === 0 && <p>No task query has completed yet.</p>}
      {retrieval.queries.map(query => <details key={query.facet_id}>
        <summary>Task {facets.findIndex(facet => facet.facet_id === query.facet_id) + 1} · {query.candidate_count == null ? 'Awaiting retrieval' : `${query.candidate_count.toLocaleString()} candidates`}</summary>
        <p className="review-preserve">{query.query}</p>
        <h3>Supported O*NET vocabulary</h3>
        {query.search_terms.length > 0 ? <ul>{query.search_terms.map(term => <li key={term}>{term}</li>)}</ul> : <p>No O*NET vocabulary was added; the query uses the extracted task.</p>}
        {query.onet_record_ids.length > 0 && <p className="help">O*NET records: {query.onet_record_ids.join(', ')}</p>}
        {query.refinements.length > 0 && <><h3>Refinements supported by your answers</h3>{query.refinements.map((value, index) => <SupportedValue key={index} value={value} />)}</>}
      </details>)}
      {retrieval.policy && <details><summary>Inspect retrieval settings and scope</summary><pre>{JSON.stringify({ policy: retrieval.policy, scope: retrieval.scope }, null, 2)}</pre></details>}
    </section>}
    <CandidateBrowser review={review} run={run} catalog={catalog} />
    {review.status === 'completed' && retrieval && retrieval.queues.length === 0 && <p className="review-panel">No searchable candidates were found in the bank.</p>}
    {!active && canRetry && catalog && <BenchmarkRetrievalForm catalog={catalog} busy={busy} onRetrieve={onRetrieve} />}
    <RequirementsContent requirements={review.requirements} deployment={review.deployment} />
  </div>
}
