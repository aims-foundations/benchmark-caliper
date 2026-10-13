import { appPath } from '../paths'
import type { AnalysisRun, Artifact, Catalog, RunAccess, RunScope, SpecificationMode } from './types'

export class AnalysisApiError extends Error {
  constructor(message: string, readonly status: number) { super(message) }
}

async function response(path: string, options: RequestInit = {}): Promise<Response> {
  const result = await fetch(appPath(`/api/item-analysis${path}`), { cache: 'no-store', ...options })
  if (!result.ok) {
    const body = await result.json().catch(() => ({}))
    throw new AnalysisApiError(typeof body.detail === 'string' ? body.detail : `Request failed (${result.status}). Please try again.`, result.status)
  }
  return result
}

async function json<T>(path: string, options: RequestInit = {}): Promise<T> {
  return (await response(path, options)).json()
}

const runPath = (run: RunAccess) => `/runs/${encodeURIComponent(run.run_id)}`
const accessHeader = (run: RunAccess) => ({ 'X-Review-Token': run.run_secret })

export const getCatalog = (signal?: AbortSignal) => json<Catalog>('/catalog', { signal })
export const createRun = (exampleId: string, mode: SpecificationMode, apiKey: string) => json<AnalysisRun & RunAccess>('/runs', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', ...(apiKey ? { 'X-OpenAI-Key': apiKey } : {}) },
  body: JSON.stringify({ example_id: exampleId, specification_mode: mode }),
})
export const getRun = (run: RunAccess, page: number, signal?: AbortSignal) => json<AnalysisRun>(`${runPath(run)}?page=${page}`, {
  headers: accessHeader(run), signal,
})
export const classify = (run: RunAccess, scope: RunScope, apiKey: string) => json<AnalysisRun>(`${runPath(run)}/classify`, {
  method: 'POST', headers: { ...accessHeader(run), 'X-OpenAI-Key': apiKey, 'Content-Type': 'application/json' },
  body: JSON.stringify({ scope }),
})
export const cancelRun = (run: RunAccess) => json<AnalysisRun>(`${runPath(run)}/cancel`, {
  method: 'POST', headers: accessHeader(run),
})
export const download = async (run: RunAccess, artifact: Artifact) => (await response(`${runPath(run)}/download/${artifact}`, {
  headers: accessHeader(run),
})).blob()
