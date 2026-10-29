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

export const createDirectRun = (context: DirectContext, dataset: ConfirmedDataset, apiKey = '') => {
  const body = new FormData()
  body.set('context_json', JSON.stringify(context))
  body.set('benchmark_confirmed', String(dataset.benchmark_confirmed))
  if (dataset.source_id) body.set('source_id', dataset.source_id)
  if (dataset.source_revision) body.set('source_revision', dataset.source_revision)
  if (dataset.items_file) body.set('items_file', dataset.items_file)
  return json<AnalysisRun & RunAccess>('/runs/from-context', {
    method: 'POST', headers: apiKey ? { 'X-OpenAI-Key': apiKey } : {}, body,
  })
}

export const createAssessmentRun = (assessment: AssessmentReference, dataset: ConfirmedDataset, apiKey = '') => {
  const body = new FormData()
  body.set('assessment_kind', assessment.kind)
  body.set('assessment_id', assessment.id)
  body.set('benchmark_confirmed', String(dataset.benchmark_confirmed))
  if (dataset.source_id) body.set('source_id', dataset.source_id)
  if (dataset.source_revision) body.set('source_revision', dataset.source_revision)
  if (dataset.items_file) body.set('items_file', dataset.items_file)
  return json<AnalysisRun & RunAccess>('/runs/from-assessment', {
    method: 'POST', headers: apiKey ? { 'X-OpenAI-Key': apiKey } : {}, body,
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

export const discardRun = async (run: RunAccess): Promise<void> => {
  await response(runPath(run), { method: 'DELETE', headers: accessHeader(run) })
}

export type PackageDownloadProgress = 'preparing' | 'downloading'
type PackageStatus = {
  status: 'not_started' | 'preparing' | 'ready' | 'failed'
  message: string
  error_status?: number
}

function waitForPackagePoll(signal: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    signal.throwIfAborted()
    const timer = setTimeout(() => { signal.removeEventListener('abort', abort); resolve() }, 1000)
    function abort() { clearTimeout(timer); reject(signal.reason) }
    signal.addEventListener('abort', abort, { once: true })
  })
}

export const downloadPackage = async (run: RunAccess, onProgress?: (progress: PackageDownloadProgress) => void, signal?: AbortSignal): Promise<{ blob: Blob; filename: string }> => {
  const controller = new AbortController()
  const abort = () => controller.abort(signal?.reason)
  signal?.addEventListener('abort', abort, { once: true })
  if (signal?.aborted) abort()
  const timeout = setTimeout(() => controller.abort(new Error('Package preparation is taking longer than expected. Please try downloading again; your saved results are unchanged.')), 15 * 60 * 1000)
  let result: Response
  try {
    onProgress?.('preparing')
    const options = { headers: accessHeader(run), signal: controller.signal }
    let status = await json<PackageStatus>(`${runPath(run)}/package`, { ...options, method: 'POST' })
    while (status.status === 'preparing') {
      await waitForPackagePoll(controller.signal)
      status = await json<PackageStatus>(`${runPath(run)}/package/status`, options)
    }
    if (status.status !== 'ready') {
      throw new AnalysisApiError(status.message || 'Package preparation was interrupted. Please try downloading again; your saved results are unchanged.', status.error_status || 409)
    }
    clearTimeout(timeout)
    onProgress?.('downloading')
    result = await response(`${runPath(run)}/package?prepared=true`, options)
    const blob = await result.blob()
    return { blob, filename: packageFilename(result) }
  } finally {
    clearTimeout(timeout)
    signal?.removeEventListener('abort', abort)
  }
}

function packageFilename(result: Response): string {
  const disposition = result.headers.get('Content-Disposition') || ''
  const encoded = disposition.match(/filename\*=UTF-8''([^;]+)/i)?.[1]
  const quoted = disposition.match(/filename="([^"]+)"/i)?.[1]
  const unquoted = disposition.match(/filename=([^;]+)/i)?.[1]
  let filename = quoted || unquoted?.trim() || 'caliper-results.zip'
  if (encoded) { try { filename = decodeURIComponent(encoded) } catch { /* Use the fallback filename. */ } }
  filename = filename.split(/[\\/]/).pop()?.replace(/[\u0000-\u001f\u007f]/g, '') || 'caliper-results.zip'
  return filename
}
