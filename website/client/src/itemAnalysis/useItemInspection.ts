import { useEffect, useState } from 'react'
import { getRun } from './api'
import { matchesItemFilter, type ItemFilter } from './Results'
import type { AnalysisRun, Item, RunAccess } from './types'

/** Inspect saved pages only when requested; this never starts classifier calls. */
export function useItemInspection(access: RunAccess | null, run: AnalysisRun | null, filter: ItemFilter, pilotSize: number) {
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [retry, setRetry] = useState(0)
  const active = !!run && ['preparing', 'generating', 'running'].includes(run.status)
  useEffect(() => {
    setItems([])
    setError('')
    if (!access || !run?.spec || filter.kind === 'all' || active) { setLoading(false); return }
    const controller = new AbortController()
    const selected = run.scope === 'all' ? run.total : Math.min(pilotSize, run.total)
    const pageSize = run.pagination.page_size || 20
    const pages = Math.min(run.pagination.total_pages, Math.ceil(selected / pageSize))
    setLoading(true)
    async function inspect() {
      const found = new Map<string, Item>()
      try {
        for (let first = 1; first <= pages; first += 4) {
          const batch = await Promise.all(Array.from({ length: Math.min(4, pages - first + 1) }, (_, i) =>
            getRun(access!, first + i, controller.signal)))
          if (controller.signal.aborted) return
          for (const saved of batch) {
            if (saved.run_id !== run!.run_id || ['preparing', 'generating', 'running'].includes(saved.status)) {
              throw new Error('The run changed during inspection. Wait for classification to pause, then try again.')
            }
            for (const item of saved.items) if (matchesItemFilter(item, filter, run!.spec!.classifiers)) found.set(item.item_id, item)
          }
        }
        setItems([...found.values()])
      } catch (problem) {
        if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'Could not inspect saved results. Try again.')
      } finally { if (!controller.signal.aborted) setLoading(false) }
    }
    void inspect()
    return () => controller.abort()
    // Page navigation within the matching items must not restart the scan.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [access?.run_id, access?.run_secret, run?.run_id, run?.status, run?.updated_at, run?.scope, filter.kind, filter.classifierId, pilotSize, active, retry])
  return { items, loading, error, retry: () => setRetry(value => value + 1) }
}
