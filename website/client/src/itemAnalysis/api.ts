import { appPath } from '../paths'
import type { AnalysisRun, Artifact, AssessmentReference, AssessmentSetup, Catalog, ConfirmedDataset, DirectContext, RunAccess, RunScope, SourceDiscovery, SpecificationMode } from './types'

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
export const getAssessment = (assessment: AssessmentReference, signal?: AbortSignal) =>
  json<AssessmentSetup>(`/assessment?${new URLSearchParams({ kind: assessment.kind, id: assessment.id })}`, { signal })
export const searchSources = (assessment: AssessmentReference, query: string, signal?: AbortSignal) =>
  json<SourceDiscovery>(`/sources?${new URLSearchParams({ kind: assessment.kind, id: assessment.id, q: query })}`, { signal })
export const getDirectSetup = (context: DirectContext, query = '', signal?: AbortSignal) =>
  json<AssessmentSetup>('/direct/setup', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...context, q: query }), signal,
  })

export const createDirectRun = (context: DirectContext, dataset: ConfirmedDataset, apiKey: string) => {
  const body = new FormData()
  body.set('context_json', JSON.stringify(context))
  body.set('benchmark_confirmed', String(dataset.benchmark_confirmed))
  if (dataset.source_id) body.set('source_id', dataset.source_id)
  if (dataset.source_revision) body.set('source_revision', dataset.source_revision)
  if (dataset.items_file) body.set('items_file', dataset.items_file)
  return json<AnalysisRun & RunAccess>('/runs/from-context', {
    method: 'POST', headers: { 'X-OpenAI-Key': apiKey }, body,
  })
}

export const createAssessmentRun = (assessment: AssessmentReference, dataset: ConfirmedDataset, apiKey: string) => {
  const body = new FormData()
  body.set('assessment_kind', assessment.kind)
  body.set('assessment_id', assessment.id)
  body.set('benchmark_confirmed', String(dataset.benchmark_confirmed))
  if (dataset.source_id) body.set('source_id', dataset.source_id)
  if (dataset.source_revision) body.set('source_revision', dataset.source_revision)
  if (dataset.items_file) body.set('items_file', dataset.items_file)
  return json<AnalysisRun & RunAccess>('/runs/from-assessment', {
    method: 'POST', headers: { 'X-OpenAI-Key': apiKey }, body,
  })
}
export const createRun = (exampleId: string, mode: SpecificationMode, apiKey: string) => json<AnalysisRun & RunAccess>('/runs', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', ...(apiKey ? { 'X-OpenAI-Key': apiKey } : {}) },
  body: JSON.stringify({ example_id: exampleId, specification_mode: mode }),
})
export const getRun = (run: RunAccess, page: number, signal?: AbortSignal) => json<AnalysisRun>(`${runPath(run)}?page=${page}`, {
  headers: accessHeader(run), signal,
})
export const classify = (run: RunAccess, scope: RunScope, apiKey: string, pilotReviewConfirmed?: boolean) => json<AnalysisRun>(`${runPath(run)}/classify`, {
  method: 'POST', headers: { ...accessHeader(run), 'X-OpenAI-Key': apiKey, 'Content-Type': 'application/json' },
  body: JSON.stringify({ scope, ...(pilotReviewConfirmed === undefined ? {} : { pilot_review_confirmed: pilotReviewConfirmed }) }),
})
export const cancelRun = (run: RunAccess) => json<AnalysisRun>(`${runPath(run)}/cancel`, {
  method: 'POST', headers: accessHeader(run),
})
export const download = async (run: RunAccess, artifact: Artifact) => (await response(`${runPath(run)}/download/${artifact}`, {
  headers: accessHeader(run),
})).blob()
