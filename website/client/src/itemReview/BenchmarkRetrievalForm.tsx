import type { FormEvent } from 'react'
import type { Catalog } from './api'

export function BenchmarkRetrievalForm({ catalog, busy, onRetrieve }: {
  catalog: Catalog; busy: boolean; onRetrieve: () => Promise<boolean>
}) {
  function submit(event: FormEvent) {
    event.preventDefault()
    if (!busy && catalog.dataset_access_configured && catalog.table_count > 0) void onRetrieve()
  }

  return <form className="review-panel" onSubmit={submit} aria-labelledby="benchmark-retrieval-start-title">
    <p className="eyebrow">Step 4 · Retrieve benchmark items</p>
    <h2 id="benchmark-retrieval-start-title">Find candidates for each task</h2>
    <p>Your extracted tasks and supported O*NET vocabulary guide local meaning-based and keyword search across the whole Measurement Data Bank on its main branch. Every field of every item row is included, with all benchmark collections and releases in scope.</p>
    <p><strong>{catalog.benchmarks.length} benchmark collections · {catalog.source_rows.toLocaleString()} source rows · whole bank</strong></p>
    <details>
      <summary>Browse all {catalog.benchmarks.length} benchmark collections</summary>
      <ul className="review-catalog">{catalog.benchmarks.map(benchmark => <li key={benchmark.id}>
        <strong>{benchmark.name}</strong><span>{benchmark.source_rows.toLocaleString()} source rows</span>
      </li>)}</ul>
    </details>
    <p className="help">The first local index build can take time. The index is cached for later searches. Complete candidate rows are fetched from Hugging Face and kept with this run’s results. Rows are combined only when every field matches exactly, including identifiers, and all source references are preserved.</p>
    <p>Retrieval makes no paid model calls and needs no OpenAI key. The result is an ordered set of candidates for later review; it does not assess relevance or select a final benchmark.</p>
    {!catalog.dataset_access_configured && <p className="review-error" role="alert">Dataset access is not configured on this server. Your requirements and O*NET mappings remain available.</p>}
    <button type="submit" disabled={busy || !catalog.dataset_access_configured || catalog.table_count === 0}>{busy ? 'Starting…' : 'Retrieve benchmark items'}</button>
  </form>
}
