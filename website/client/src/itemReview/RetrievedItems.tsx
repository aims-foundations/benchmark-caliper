import './RetrievedItems.css'
import { useEffect, useState } from 'react'
import { appPath } from '../paths'
import type { BenchmarkCandidate } from './api'
import type { ConstructionSnapshot } from './constructionTypes'
import { ItemContent } from './ItemContent'

type RetrievedSummary = {
  item_id: string; rank: number; queue_rank: number; dense_rank: number | null; bm25_rank: number | null
  dense_score: number | null; bm25_score: number | null; rrf_score: number
  question_preview: string; sources: string[]
}
type RetrievedPage = {
  queue_id: string; facet_id: string; source: string | null; page: number; page_size: number
  total: number; total_pages: number; unique_candidate_count: number; items: RetrievedSummary[]
}

function RetrievedCard({ summary, queueId, exampleId }: { summary: RetrievedSummary; queueId: string; exampleId: string }) {
  const [open, setOpen] = useState(false)
  const [record, setRecord] = useState<BenchmarkCandidate | null>(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  useEffect(() => {
    if (!open || record) return
    const controller = new AbortController()
    setError('')
    const query = new URLSearchParams({ queue_id: queueId })
    fetch(appPath(`/api/item-review/examples/${encodeURIComponent(exampleId)}/retrieved/${encodeURIComponent(summary.item_id)}?${query}`), { signal: controller.signal, cache: 'no-store' })
      .then(async response => {
        if (!response.ok) throw new Error('This saved item could not be loaded. Please try again.')
        return response.json() as Promise<BenchmarkCandidate>
      })
      .then(result => { if (!controller.signal.aborted) setRecord(result) })
      .catch(problem => { if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'This saved item could not be loaded.') })
    return () => controller.abort()
  }, [open, record, attempt, exampleId, queueId, summary.item_id])
  return <details className="construction-retrieved-card" onToggle={event => setOpen(event.currentTarget.open)}>
    <summary>
      <span className="construction-retrieved-rank">Retrieved item {summary.queue_rank}</span>
      {!open && <>
        <strong>{summary.question_preview ? summary.question_preview.replace(/…$/, '...') : 'Open this item to inspect the saved source row.'}</strong>
        <span className="construction-retrieved-source">Benchmark: {summary.sources.join(', ') || 'Not recorded'}</span>
        <span className="construction-retrieved-source">Task ranking: {summary.rank}. Meaning search rank: {summary.dense_rank ?? 'Not ranked'}. Keyword search rank: {summary.bm25_rank ?? 'Not ranked'}.</span>
      </>}
      <span className="construction-expand-hint">{open ? 'Close item details' : 'Inspect this item'}</span>
    </summary>
    {open && <div className="construction-retrieved-body">
      {record ? <>
        <ItemContent text={record.question_text} />
        <div className="construction-open-metadata">
          <span className="construction-retrieved-source">Benchmark: {summary.sources.join(', ') || 'Not recorded'}</span>
          <span className="construction-retrieved-source">Task ranking: {summary.rank}. Meaning search rank: {summary.dense_rank ?? 'Not ranked'}. Keyword search rank: {summary.bm25_rank ?? 'Not ranked'}.</span>
        </div>
        <details><summary>Retrieval scores and source records</summary>
          <dl className="construction-retrieved-scores">
            <div><dt>Combined ranking score</dt><dd>{record.rrf_score}</dd></div>
            <div><dt>Meaning search score</dt><dd>{record.dense_score ?? 'Not ranked'}</dd></div>
            <div><dt>Keyword search score</dt><dd>{record.bm25_score ?? 'Not ranked'}</dd></div>
          </dl>
          <p>Item ID: <code>{record.item_id}</code></p>
          <pre>{JSON.stringify(record.sources, null, 2)}</pre>
        </details>
        <details><summary>Full item record</summary><pre>{JSON.stringify(record.evidence, null, 2)}</pre></details>
        <details><summary>Full row text used for search</summary><pre>{record.search_text}</pre></details>
      </> : error ? <><p role="alert">{error}</p><button type="button" className="secondary" onClick={() => setAttempt(value => value + 1)}>Try loading this item again</button></> : <p role="status">Loading the saved item…</p>}
    </div>}
  </details>
}

export function RetrievedItems({ snapshot }: { snapshot: ConstructionSnapshot }) {
  const facets = snapshot.review.requirements?.task_facets ?? []
  const queues = snapshot.review.retrieval?.queues ?? []
  const [selectedFacet, setSelectedFacet] = useState('')
  const [source, setSource] = useState('')
  const [page, setPage] = useState(1)
  const [result, setResult] = useState<RetrievedPage | null>(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const facetId = facets.find(facet => facet.facet_id === selectedFacet)?.facet_id ?? facets[0]?.facet_id
  const taskQueues = queues.filter(queue => queue.facet_id === facetId)
  const queue = taskQueues.find(queue => (queue.source ?? '') === source) ?? taskQueues.find(queue => queue.source == null)
  const queueId = queue?.queue_id
  useEffect(() => {
    setResult(null)
    setError('')
    if (!queueId) return
    const controller = new AbortController()
    const query = new URLSearchParams({ queue_id: queueId, page: String(page), page_size: '10' })
    fetch(appPath(`/api/item-review/examples/${encodeURIComponent(snapshot.entry.id)}/retrieved?${query}`), { signal: controller.signal, cache: 'no-store' })
      .then(async response => {
        if (!response.ok) throw new Error('The saved retrieval list could not be loaded. Please try again.')
        return response.json() as Promise<RetrievedPage>
      })
      .then(data => { if (!controller.signal.aborted) setResult(data) })
      .catch(problem => { if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'The saved retrieval list could not be loaded.') })
    return () => controller.abort()
  }, [snapshot.entry.id, queueId, page, attempt])
  return <section className="construction-retrieved-items" aria-labelledby="construction-retrieved-title">
    <h3 id="construction-retrieved-title">Retrieved items</h3>
    <p>Browse the saved rankings for each task. Open an item to read its content and source evidence.</p>
    {result && <p>{result.unique_candidate_count.toLocaleString()} distinct items were retrieved across all tasks. Items shared by several task lists appear in each relevant list.</p>}
    <div className="construction-retrieved-filters">
      <label>Task<select value={facetId ?? ''} onChange={event => { setSelectedFacet(event.target.value); setSource(''); setPage(1) }}>
        {facets.map((facet, index) => <option key={facet.facet_id} value={facet.facet_id}>Task {index + 1}: {facet.task.text ?? facet.facet_id}</option>)}
      </select></label>
      <label>Benchmark<select value={queue?.source ?? ''} onChange={event => { setSource(event.target.value); setPage(1) }}>
        {taskQueues.map(queue => <option key={queue.queue_id} value={queue.source ?? ''}>{queue.source ?? 'All benchmarks'} ({queue.item_count.toLocaleString()})</option>)}
      </select></label>
    </div>
    {!queueId ? <p>No retrieved items are recorded for this task.</p> : error ? <><p role="alert">{error}</p><button type="button" className="secondary" onClick={() => setAttempt(value => value + 1)}>Retry loading retrieved items</button></> : !result ? <p role="status">Loading retrieved items…</p> : <>
      <p role="status">{result.total.toLocaleString()} items in this list. {result.total > 0 && <>Showing {(result.page - 1) * result.page_size + 1} to {Math.min(result.page * result.page_size, result.total)}.</>}</p>
      {result.items.map(item => <RetrievedCard key={`${queueId}:${item.item_id}`} summary={item} queueId={queueId} exampleId={snapshot.entry.id} />)}
      {result.items.length === 0 && <p>No candidates are available in this saved list.</p>}
      {result.total_pages > 1 && <nav className="construction-retrieved-pagination" aria-label="Retrieved item pages">
        <button type="button" className="secondary" disabled={result.page <= 1} onClick={() => setPage(result.page - 1)}>Previous items</button>
        <label>Page<select value={result.page} onChange={event => setPage(Number(event.target.value))}>{Array.from({ length: result.total_pages }, (_, index) => <option key={index + 1} value={index + 1}>{index + 1} of {result.total_pages}</option>)}</select></label>
        <button type="button" className="secondary" disabled={result.page >= result.total_pages} onClick={() => setPage(result.page + 1)}>Next items</button>
      </nav>}
    </>}
  </section>
}
