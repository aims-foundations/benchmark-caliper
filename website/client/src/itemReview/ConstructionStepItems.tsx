import { useCallback, useEffect, useState } from 'react'
import type { ScreenedItem } from './api'
import type { ConstructionSnapshot } from './constructionTypes'
import { ConstructionItem } from './ConstructionItem'
import './ConstructionStepItems.css'

type Result = 'all' | 'pass' | 'fail' | 'unresolved' | 'error'
type Collection = 'selected' | 'adaptive' | 'all'
type Step = 5 | 6 | 7

export function ConstructionStepItems({ snapshot, step }: { snapshot: ConstructionSnapshot; step: Step }) {
  const [loadedItems, setLoadedItems] = useState<Map<string, ScreenedItem>>(() => new Map((snapshot.review.screening?.items ?? []).map(item => [item.item_id, item])))
  const onLoad = useCallback((item: ScreenedItem) => setLoadedItems(current => new Map(current).set(item.item_id, item)), [])
  const [collection, setCollection] = useState<Collection>('selected')
  const [result, setResult] = useState<Result>('all')
  const [page, setPage] = useState(1)
  useEffect(() => { setCollection('selected'); setResult('all'); setPage(1) }, [step, snapshot.entry.id])
  const initialSelection = snapshot.review.adaptive?.initial_selection
  const selection = step === 6 ? initialSelection : snapshot.review.selection
  const selectedIds = selection?.selected_item_ids ?? (step === 7 ? snapshot.items.filter(item => item.selected).map(item => item.item_id) : [])
  const selectedOrder = new Map(selectedIds.map((id, index) => [id, index]))
  const selectedRows = new Map(selection?.items.map(item => [item.item_id, item]) ?? [])
  const initial = snapshot.items.filter(item => item.initial)
  const additional = snapshot.items.filter(item => !item.initial)
  const selectedSummaries = selectedIds.flatMap(id => {
    const summary = snapshot.items.find(item => item.item_id === id)
    return summary ? [{ ...summary, selected: true, quality_score: selectedRows.get(id)?.quality_score ?? summary.quality_score }] : []
  })
  const base = step === 5 ? initial.map(item => ({ ...item, selected: false }))
    : step === 6 || collection === 'selected' ? selectedSummaries
      : collection === 'adaptive' ? additional : snapshot.items
  const filtered = base.filter(item => result === 'all' || (result === 'error' ? item.status === 'error' : item.status !== 'error' && (result === 'unresolved' ? item.gate == null || item.gate === 'unresolved' : item.gate === result)))
  const pages = Math.max(1, Math.ceil(filtered.length / 10))
  const currentPage = Math.min(page, pages)
  const title = step === 5 ? 'Initial screening assessments' : step === 6 ? 'Initial selected items' : 'Final selected items and additional assessments'
  const missingSummaries = selectedIds.length - selectedSummaries.length
  return <section className="construction-inline-items" aria-labelledby={`step-${step}-items-title`}>
    <h3 id={`step-${step}-items-title`}>{title}</h3>
    {step === 6 && !initialSelection ? <p>No initial selection snapshot is available in this saved record.</p>
      : step === 6 && selectedIds.length === 0 ? <p>No items were selected at Step 6.</p>
        : <>
          <div className="construction-filters construction-inline-filters">
            {step === 7 && <label>Items to show<select value={collection} onChange={event => { setCollection(event.target.value as Collection); setResult('all'); setPage(1) }}>
              <option value="selected">Final selected items ({selectedIds.length})</option>
              <option value="adaptive">Additional assessments ({additional.length})</option>
              <option value="all">All assessed candidates ({snapshot.items.length})</option>
            </select></label>}
            {step !== 6 && <label>Eligibility result<select value={result} onChange={event => { setResult(event.target.value as Result); setPage(1) }}>
              <option value="all">All decisions</option><option value="pass">Eligible</option><option value="fail">Not eligible</option><option value="unresolved">Unresolved</option><option value="error">Assessment error</option>
            </select></label>}
          </div>
          <div className="construction-browser-page"><p role="status">{filtered.length === 0 ? 'No items match these filters.' : `${filtered.length} ${filtered.length === 1 ? 'item' : 'items'}. Showing ${(currentPage - 1) * 10 + 1} to ${Math.min(currentPage * 10, filtered.length)}.`}</p>{pages > 1 && <span>Page {currentPage} of {pages}</span>}</div>
          {filtered.slice((currentPage - 1) * 10, currentPage * 10).map(summary => <ConstructionItem key={`${step}-${summary.item_id}`} summary={summary} item={loadedItems.get(summary.item_id)} review={snapshot.review} exampleId={snapshot.entry.id} selectedIndex={selectedOrder.get(summary.item_id) ?? -1} onLoad={onLoad} focused={false} step={step} />)}
          {pages > 1 && <nav className="construction-pagination" aria-label={`Step ${step} item pages`}><button type="button" disabled={currentPage === 1} onClick={() => setPage(currentPage - 1)}>Previous items</button><span>Page {currentPage} of {pages}</span><button type="button" disabled={currentPage === pages} onClick={() => setPage(currentPage + 1)}>Next items</button></nav>}
        </>}
    {missingSummaries > 0 && (step === 6 || collection === 'selected') && <p>{missingSummaries} selected {missingSummaries === 1 ? 'item has' : 'items have'} no item summary in this saved record. The selection record below retains the saved IDs.</p>}
  </section>
}
