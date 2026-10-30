import { useEffect, useState } from 'react'
import type { ScreenedItem } from './api'
import type { ConstructionSnapshot } from './constructionTypes'
import { ConstructionItem } from './ConstructionItem'
import './ConstructionItems.css'

type Phase = 'all' | 'initial' | 'adaptive'
type Result = 'all' | 'pass' | 'fail' | 'unresolved' | 'error'
type Collection = 'selected' | 'all'

export function ConstructionItems({ snapshot, loadedItems, onLoad, initialPhase, focusedItemId }: {
  snapshot: ConstructionSnapshot; loadedItems: Map<string, ScreenedItem>; onLoad: (item: ScreenedItem) => void
  initialPhase: Phase | null; focusedItemId?: string
}) {
  const { items, review, entry } = snapshot
  const [collection, setCollection] = useState<Collection>(initialPhase == null ? 'selected' : 'all')
  const [result, setResult] = useState<Result>('all')
  const [phase, setPhase] = useState<Phase>(initialPhase ?? 'all')
  const [page, setPage] = useState(1)
  const selectedIds = review.selection?.selected_item_ids ?? items.filter(item => item.selected).map(item => item.item_id)
  const selectedOrder = new Map(selectedIds.map((id, index) => [id, index]))
  useEffect(() => { setPhase(initialPhase ?? 'all'); setCollection(initialPhase == null ? 'selected' : 'all'); setResult('all'); setPage(1) }, [initialPhase])
  useEffect(() => {
    if (!focusedItemId) return
    const target = items.find(item => item.item_id === focusedItemId)
    if (!target) return
    setPhase('all'); setResult('all'); setCollection(target.selected ? 'selected' : 'all')
    const position = target.selected ? selectedIds.indexOf(target.item_id) : items.findIndex(item => item.item_id === target.item_id)
    setPage(Math.floor(Math.max(0, position) / 10) + 1)
    // The saved snapshot is immutable within this mounted browser. Filters may
    // subsequently change without repeatedly jumping back to an earlier link.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [focusedItemId])
  function changeCollection(next: Collection) {
    setCollection(next)
    setResult('all')
    setPhase('all')
    setPage(1)
  }
  // Selected items always show the complete final collection, even if a
  // previous all-items view used a screening-stage or eligibility filter.
  const filtered = items.filter(item => collection === 'selected' ? item.selected
    : (phase === 'all' || item.initial === (phase === 'initial'))
      && (result === 'all' || (result === 'error' ? item.status === 'error' : item.status !== 'error' && (result === 'unresolved' ? item.gate == null || item.gate === 'unresolved' : item.gate === result))))
  if (collection === 'selected') filtered.sort((a, b) => (selectedOrder.get(a.item_id) ?? Infinity) - (selectedOrder.get(b.item_id) ?? Infinity))
  const pages = Math.max(1, Math.ceil(filtered.length / 10))
  const currentPage = Math.min(page, pages)
  const initial = items.filter(item => item.initial).length
  return <section className="construction-item-browser" aria-labelledby="construction-browse-title">
    <h2 id="construction-browse-title">{collection === 'selected' ? `Selected items (${selectedIds.length})` : `All screened items (${items.length})`}</h2>
    <p>{collection === 'selected' ? 'Open an item to read its content, screening ratings, and supporting evidence.' : `The saved records contain ${initial} candidates from Step 5 and ${items.length - initial} added in Step 7.`}</p>
    <div className="construction-collection-switch" role="group" aria-label="Items to show">
      <button type="button" aria-pressed={collection === 'selected'} onClick={() => changeCollection('selected')}>Selected items ({selectedIds.length})</button>
      <button type="button" aria-pressed={collection === 'all'} onClick={() => changeCollection('all')}>All screened items ({items.length})</button>
    </div>
    {collection === 'all' && <>
      <div className="construction-filters construction-browser-filters">
        <label>Eligibility result<select value={result} onChange={event => { setResult(event.target.value as Result); setPage(1) }}><option value="all">All eligibility decisions</option><option value="pass">Eligible</option><option value="fail">Not eligible</option><option value="unresolved">Eligibility unresolved</option><option value="error">Assessment error</option></select></label>
        <label>Screening stage<select value={phase} onChange={event => { setPhase(event.target.value as Phase); setPage(1) }}><option value="all">Both screening stages</option><option value="initial">Step 5 initial screening ({initial})</option><option value="adaptive">Step 7 adaptive screening ({items.length - initial})</option></select></label>
      </div>
      <div className="construction-browser-page"><p role="status">{filtered.length} matching {filtered.length === 1 ? 'item' : 'items'}. Page {currentPage} of {pages}.</p>{pages > 1 && <span>Showing {(currentPage - 1) * 10 + 1} to {Math.min(currentPage * 10, filtered.length)}.</span>}</div>
    </>}
    {filtered.length === 0 && <p>{collection === 'selected' ? 'No items were selected in this saved run.' : 'No items match these filters.'}</p>}
    {filtered.slice((currentPage - 1) * 10, currentPage * 10).map(summary => <ConstructionItem key={summary.item_id} summary={summary} item={loadedItems.get(summary.item_id)} review={review} exampleId={entry.id} selectedIndex={selectedOrder.get(summary.item_id) ?? -1} onLoad={onLoad} focused={focusedItemId === summary.item_id} />)}
    {pages > 1 && <nav className="construction-pagination" aria-label="Item pages"><button type="button" disabled={currentPage === 1} onClick={() => setPage(currentPage - 1)}>Previous items</button><span>Page {currentPage} of {pages}</span><button type="button" disabled={currentPage === pages} onClick={() => setPage(currentPage + 1)}>Next items</button></nav>}
  </section>
}
