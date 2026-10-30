import { appPath } from '../paths'

export const DIMENSIONS = [
  ['input_ontology', 'Input ontology'], ['input_content', 'Input content'], ['input_form', 'Input form'],
  ['output_ontology', 'Output ontology'], ['output_content', 'Output content'], ['output_form', 'Output form'],
] as const

export interface Deployment {
  task: string; users: string; inputs: string; outputs: string; success: string; constraints: string
}
export interface EvidenceRef { answer_id: keyof Deployment; quote: string }
export interface SupportedText { text: string | null; evidence: EvidenceRef[] }
export interface TaskFacet {
  facet_id: string; task: SupportedText; required_input_evidence: SupportedText
  required_output_behavior: SupportedText; essential: boolean | null
}
export interface CoverageRequirement {
  facet_ids: string[]; minimum_items: number | null; requirement: SupportedText
}
export interface Requirements {
  workflow: SupportedText; primary_user: SupportedText; input_types: SupportedText
  output_types: SupportedText; authority: SupportedText; task_facets: TaskFacet[]
  coverage_requirements: CoverageRequirement[]; unresolved_details: string[]
}
export interface ExtractionPolicy {
  version: number; model: string; reasoning_effort: string; max_output_tokens: number
  prompt: string; output_schema: Record<string, unknown>; response_id?: string; response_model?: string
}
export interface SamplingPolicy {
  version: number; method: string; seed: number; items_per_benchmark: number
}
export interface RetrievalPolicy {
  version: number; method: 'qwen3_embedding'; model: string; max_tokens: number; similarity: 'dot_product'
  [key: string]: unknown
}
export interface Catalog {
  model: string; reasoning_effort: string; max_output_tokens: number
  retrieval_policy: RetrievalPolicy; default_retrieve_k: number; max_retrieve_k: number
  branches: Record<string, string>; dataset_access_configured: boolean; table_count: number; source_rows: number
  sampling: SamplingPolicy; sample_max_items: number
  missing_item_tables: Array<{ branch: string; benchmark: string }>
  benchmarks: Array<{ id: string; name: string; table_count: number; source_rows: number; sample_max_items: number }>
}
export type ReviewRequest = { deployment: Deployment } & (
  { mode: 'requirements'; run_name?: string } | { mode?: 'item_review'; retrieve_k: number; retrieval_query?: string }
)
export interface RunAccess { run_id: string; run_secret: string }
export type LegacyConfidence = 'high' | 'medium' | 'low' | 'insufficient'
// Earlier reports keep their original labels; new assessments use numbers.
export type Confidence = number | null | LegacyConfidence
export interface DimensionScore {
  score: number | null; confidence: Confidence; confidence_rationale: string
  justification: string; evidence: string[]; information_gaps: string[]
}
export interface ReviewedItem {
  evidence_hash: string; rank?: number; status: string; overall_score?: number | null; error?: string
  retrieval_rank?: number; retrieval_score?: number; exact_match?: boolean
  compatibility_score?: number | null; scored_dimensions?: number; needs_review?: boolean
  assessment?: Record<string, DimensionScore>
  evidence: { item: { content: string | null; grading_criterion: unknown }; [key: string]: unknown }
  sources: Array<{ repo: string; branch: string; commit: string; benchmark: string; items_path: string; item_id: string; row: number }>
}
export interface Review {
  run_id: string; status: 'preparing' | 'running' | 'completed' | 'cancelled' | 'failed'; message: string
  mode?: 'item_review'
  model: string; reasoning_effort: string; deployment: Deployment
  scope: { benchmarks: string[]; table_count: number; source_rows: number; branches: Record<string, string>; sample_only: boolean; sampling: SamplingPolicy; sample_max_items: number; retrieve_k?: number }
  indexed_items?: number; retrieved_items?: number; retrieval_policy?: RetrievalPolicy; retrieval_query?: string
  scoring_policy: { version: number; formula: string; confidence_role?: string; confidence_scale?: string; needs_review_rule?: string;
    ranking_floor?: number; compatibility_formula?: string; interpretation?: string;
    missing_dimensions?: string; no_scored_dimensions?: string; neutral_score?: number; confidence_weights?: Record<LegacyConfidence, number> }
  source_rows: number; total: number; processed: number; complete: number; needs_review: number; errors: number
  ranked?: number; unranked?: number
  sample_complete: boolean; prepared_benchmarks: number; pagination: { page: number; page_size: number; total_pages: number }
  usage: Record<string, number>; ranked_items: ReviewedItem[]; unranked_items?: ReviewedItem[]; failed_items: ReviewedItem[]
}
export interface ResultMetadata {
  export_version: number; run_name: string | null; created_at: string; finished_at: string | null
  exported_at?: string; result_state: 'partial' | 'stage_complete' | 'frozen'; usage_scope: 'current_run'
}
export interface RequirementsReview {
  run_id: string; status: Review['status']; message: string; mode: 'requirements'
  model: string; reasoning_effort: string; deployment: Deployment; requirements: Requirements | null
  extraction: ExtractionPolicy | null; usage: Record<string, number>
  metadata?: ResultMetadata
}
export interface OnetCandidate {
  doc_id: string; kind: string; name: string; text: string; occupation_id: string | null
  dense_rank: number | null; bm25_rank: number | null; rrf_score: number
}
export interface OnetRecordMapping {
  record_id: string; supporting_passage: string
  applicability: 'applicable' | 'partially_applicable' | 'not_applicable'
  rationale: string; search_terms: string[]
}
export interface OnetFacetResult {
  facet_id: string; query: string; candidates: OnetCandidate[]; status: 'complete' | 'error'
  mapping: { facet_id: string; records: OnetRecordMapping[]; refinements: SupportedText[]; unresolved_details: string[] } | null
  error?: string; response_id?: string; response_model?: string; usage?: Record<string, number>
}
export interface GroundingReview extends Omit<RequirementsReview, 'mode'> {
  mode: 'grounding'; source_run_id: string
  grounding: { retrieval: Record<string, unknown> | null; mapping: ExtractionPolicy; facets: OnetFacetResult[] } | null
}
export interface BenchmarkQuery {
  facet_id: string; query: string; onet_record_ids: string[]; search_terms: string[]
  refinements: SupportedText[]; candidate_count?: number
}
export interface CandidateQueue { queue_id: string; facet_id: string; source: string | null; item_count: number }
export interface BenchmarkRetrievalReview extends Omit<GroundingReview, 'mode'> {
  mode: 'retrieval'
  retrieval: {
    policy: Record<string, unknown> | null
    scope: { repo: string; branches: Record<string, string>; benchmarks: string[]; table_count: number; source_rows: number; sample_only: false }
    stats: { source_rows?: number; total_items?: number; indexed_items?: number; contentless_items?: number; [key: string]: unknown }
    queries: BenchmarkQuery[]; queues: CandidateQueue[]
  } | null
}
export interface BenchmarkCandidate {
  item_id: string; evidence_hash: string; question_text?: string | null; search_text: string; evidence: Record<string, unknown>
  sources: Array<{ benchmark: string; branch: string; [key: string]: unknown }>
  rank: number; dense_rank: number | null; bm25_rank: number | null
  dense_score: number | null; bm25_score: number | null; rrf_score: number
}
export interface CandidatePage {
  queue_id: string; facet_id: string; page: number; page_size: number; total_pages: number; total_items: number
  items: BenchmarkCandidate[]
}
export type ValidityDimension = typeof DIMENSIONS[number][0]
export interface ScreeningRating {
  score: number | null; evidence: string[]; justification: string; information_gaps: string[]
}
export interface ScreeningAssessment {
  task: { status: 'matched' | 'no_match' | 'unresolved'; decision: string | null; matched_facet_ids: string[]
    evidence: string[]; justification: string; information_gaps: string[] }
  ratings: Record<ValidityDimension, ScreeningRating>
  coverage: Array<{ requirement_index: number; satisfied: boolean | null; evidence: string[]; justification: string; information_gaps: string[] }>
}
export interface ScreenedItem extends BenchmarkCandidate {
  acquisition: { queue_id: string; facet_id: string }; status: 'complete' | 'error'
  assessment?: ScreeningAssessment; gate?: { status: 'pass' | 'fail' | 'unresolved'; reasons: string[] }
  error?: string; usage?: Record<string, number>; screened_run_id?: string
  evidence_adjustments?: Array<{ field: string; returned_quote: string; source_quote: string }>
}
export interface ScreeningReview extends Omit<BenchmarkRetrievalReview, 'mode'> {
  mode: 'screening'
  screening: {
    policy: { version: number; initial_budget: number; gated_dimensions: ValidityDimension[]; minimum_score: number; [key: string]: unknown }
    model: ExtractionPolicy
    allocation: { budget: number; allocated: number; shortfall: number
      allocations: Array<{ queue_id: string; facet_id: string; target: number; allocated: number }>
      items: Array<{ item_id: string; queue_id: string; facet_id: string }> }
    items: ScreenedItem[]
  } | null
}
export interface SelectionInput { allocated: number; screened: number; errors: number; pending: number }
export interface SelectionReview extends Omit<ScreeningReview, 'mode'> {
  mode: 'selection'; selection_input: SelectionInput; selection_run_id: string | null
  selection: {
    policy: Record<string, unknown>; limit: number; eligible_count: number; selected_count: number; selected_item_ids: string[]
    items: Array<{ item_id: string; quality_score: number; rating_sum: number; matched_facet_ids: string[]; coverage_requirement_indices: number[] }>
    total_quality: number
    task_coverage: Array<{ facet_id: string; minimum: number; eligible_count: number; selected_count: number; shortfall: number }>
    quota_coverage: Array<{ requirement_index: number; minimum_items: number | null; eligible_count: number; selected_count: number; shortfall: number | null }>
    constraints_feasible: boolean; fully_satisfied: boolean; gaps: string[]; unresolved_requirement_indices: number[]
    excluded_counts: Record<string, number>; solver: Record<string, unknown>
  } | null
}
export interface AdaptiveRequest {
  seed?: number; max_cost_usd?: number | null; input_price_per_million?: number | null
  cached_input_price_per_million?: number | null; output_price_per_million?: number | null
}
export interface AdaptiveSettings extends Required<AdaptiveRequest> {
  candidate_limit: number; batch_size: number; exploration_rate: number
}
export interface QueueStatistics {
  queue_id: string; facet_id: string; source: string | null; successes: number; failures: number
  alpha: number; beta: number; estimated_yield: number; coverage_weight?: number; priority?: number; remaining?: number
}
export interface AdaptiveBatch {
  number: number; kind: 'initial' | 'adaptive'; status: 'committed' | 'pending'
  queue_id: string | null; facet_id: string | null; source: string | null; exploration: boolean | null
  item_ids: string[]; outcomes: Array<{ item_id: string; facet_id: string; source_names: string[]; retained: boolean }>
  selected_item_ids: string[]; unresolved_item_ids?: string[]; priorities?: QueueStatistics[]
}
export interface AdaptiveReview extends Omit<SelectionReview, 'mode'> {
  mode: 'adaptive'
  adaptive: {
    version: number; policy: Record<string, unknown>; settings: AdaptiveSettings; batches: AdaptiveBatch[]
    initial_selection?: SelectionReview['selection']; initial_selection_run_id?: string | null
    queue_statistics: QueueStatistics[]
    attempts: Array<{ item_id: string; status: string; usage: Record<string, number> | null; cost_usd: number | null; reserved_usd: number | null }>
    cost: { spent_usd: number | null; reserved_usd: number | null; unknown_attempts: number; scope: 'adaptive_screening' }
    frozen: boolean; stop_reason: 'candidate_limit' | 'queues_exhausted' | 'cost_limit' | null
    screened_count: number; acquired_count: number
  } | null
}
export type RunResult = Review | RequirementsReview | GroundingReview | BenchmarkRetrievalReview | ScreeningReview | SelectionReview | AdaptiveReview

export class ReviewRequestError extends Error {
  constructor(readonly status: number, message: string, readonly hasServerDetail = false) {
    super(message)
    this.name = 'ReviewRequestError'
  }
}

async function fetchResponse(path: string, options: RequestInit = {}): Promise<Response> {
  const response = await fetch(appPath(`/api/item-review${path}`), { cache: 'no-store', ...options })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    const fallback = response.status >= 500
      ? `The server could not respond (${response.status}). Please try again shortly.`
      : `Request failed (${response.status}). Check your entries and try again.`
    const hasServerDetail = typeof body?.detail === 'string'
    const message = hasServerDetail ? body.detail : fallback
    throw new ReviewRequestError(response.status, message, hasServerDetail)
  }
  return response
}

const request = async <T,>(path: string, options?: RequestInit): Promise<T> => (await fetchResponse(path, options)).json()

export const getCatalog = (signal?: AbortSignal) => request<Catalog>('/catalog', { signal })
export const startReview = (body: ReviewRequest, apiKey: string) => request<RunAccess>('/runs', {
  method: 'POST', headers: { 'Content-Type': 'application/json', 'X-OpenAI-Key': apiKey }, body: JSON.stringify(body),
})
export const startGrounding = (run: RunAccess, apiKey: string) => request<RunAccess>(`/runs/${run.run_id}/ground`, {
  method: 'POST', headers: { 'X-Review-Token': run.run_secret, 'X-OpenAI-Key': apiKey },
})
export const startBenchmarkRetrieval = (run: RunAccess) => request<RunAccess>(`/runs/${run.run_id}/retrieve`, {
  method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Review-Token': run.run_secret },
  body: JSON.stringify({}),
})
export const startScreening = (run: RunAccess, apiKey: string) => request<RunAccess>(`/runs/${run.run_id}/screen`, {
  method: 'POST', headers: { 'X-Review-Token': run.run_secret, 'X-OpenAI-Key': apiKey },
})
export const startSelection = (run: RunAccess) => request<RunAccess>(`/runs/${run.run_id}/select`, {
  method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Review-Token': run.run_secret }, body: JSON.stringify({}),
})
export const startAdaptive = (run: RunAccess, apiKey: string, body: AdaptiveRequest) => request<RunAccess>(`/runs/${run.run_id}/adapt`, {
  method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Review-Token': run.run_secret, 'X-OpenAI-Key': apiKey }, body: JSON.stringify(body),
})
export const getCandidates = (run: RunAccess, queueId: string, page = 1, signal?: AbortSignal) => request<CandidatePage>(
  `/runs/${run.run_id}/candidates?${new URLSearchParams({ queue_id: queueId, page: String(page) })}`,
  { headers: { 'X-Review-Token': run.run_secret }, signal },
)
export const getReview = (run: RunAccess, page = 1, signal?: AbortSignal) => request<RunResult>(`/runs/${run.run_id}?page=${page}`, {
  headers: { 'X-Review-Token': run.run_secret }, signal,
})
export const getReviewExport = async (run: RunAccess) => (await fetchResponse(`/runs/${run.run_id}/export`, {
  headers: { 'X-Review-Token': run.run_secret },
})).blob()
export type PackageDownloadProgress = { phase: 'preparing' } | { phase: 'downloading'; receivedBytes: number; totalBytes: number }
export type PreparedPackage = { package_id: string; bytes: number; filename: string; chunk_bytes: number }
type PackageStatus = Partial<PreparedPackage> & {
  status: 'not_started' | 'preparing' | 'ready' | 'failed'
  message: string
  error_status?: number
}

function waitForPackagePoll(signal: AbortSignal, milliseconds = 1000): Promise<void> {
  return new Promise((resolve, reject) => {
    signal.throwIfAborted()
    const timer = setTimeout(() => { signal.removeEventListener('abort', abort); resolve() }, milliseconds)
    function abort() { clearTimeout(timer); reject(signal.reason) }
    signal.addEventListener('abort', abort, { once: true })
  })
}

function preparedPackage(status: PackageStatus): PreparedPackage {
  if (typeof status.package_id !== 'string' || !status.package_id
      || !Number.isSafeInteger(status.bytes) || status.bytes! <= 0
      || !Number.isSafeInteger(status.chunk_bytes) || status.chunk_bytes! <= 0 || status.chunk_bytes! > 1048576
      || typeof status.filename !== 'string' || !status.filename
      || /[/\\\x00-\x1f\x7f]/.test(status.filename) || !status.filename.toLowerCase().endsWith('.zip')) {
    throw new ReviewRequestError(502, 'The server returned incomplete package information. Your saved results are unchanged. Please try downloading again.', true)
  }
  return status as PreparedPackage
}

class PackagePieceError extends Error {
  constructor(message: string, readonly retryable: boolean) { super(message) }
}

async function packagePiece(path: string, prepared: PreparedPackage, offset: number, headers: Record<string, string>, signal: AbortSignal): Promise<Blob> {
  const expectedBytes = Math.min(prepared.chunk_bytes, prepared.bytes - offset)
  const query = new URLSearchParams({ package_id: prepared.package_id, offset: String(offset) })
  for (let attempt = 0; ; attempt++) {
    signal.throwIfAborted()
    const controller = new AbortController()
    const abort = () => controller.abort(signal.reason)
    signal.addEventListener('abort', abort, { once: true })
    const timeout = setTimeout(() => controller.abort(new DOMException('Package transfer timed out.', 'TimeoutError')), 45000)
    let failure: unknown
    try {
      const response = await fetchResponse(`${path}/chunk?${query}`, { headers, signal: controller.signal })
      if (response.status !== 200 || response.headers.get('X-Package-Id') !== prepared.package_id
          || response.headers.get('X-Package-Offset') !== String(offset)) {
        throw new PackagePieceError('The downloaded package piece did not match the requested package.', false)
      }
      const blob = await response.blob()
      const contentLength = response.headers.get('Content-Length')
      if ((contentLength !== null && contentLength !== String(expectedBytes)) || blob.size !== expectedBytes) {
        throw new PackagePieceError('The connection returned an incomplete package piece.', true)
      }
      return blob
    } catch (error) {
      if (signal.aborted) throw signal.reason
      failure = controller.signal.aborted ? controller.signal.reason : error
    } finally {
      clearTimeout(timeout)
      signal.removeEventListener('abort', abort)
    }
    if (failure instanceof ReviewRequestError && failure.status === 412) {
      throw new ReviewRequestError(412, 'The prepared package changed or is no longer available. Your saved results are unchanged. Please try downloading again.', true)
    }
    const retryable = failure instanceof PackagePieceError ? failure.retryable
      : failure instanceof ReviewRequestError ? [429, 502, 503, 504].includes(failure.status)
        : failure instanceof TypeError || (failure instanceof DOMException && ['NetworkError', 'TimeoutError'].includes(failure.name))
    if (!retryable || attempt === 2) throw failure
    await waitForPackagePoll(signal, 500 * (attempt + 1))
  }
}

async function transferPackage(path: string, metadata: Partial<PreparedPackage>, headers: Record<string, string>, signal: AbortSignal, onProgress?: (progress: PackageDownloadProgress) => void): Promise<{ blob: Blob; filename: string }> {
  const prepared = preparedPackage({ ...metadata, status: 'ready', message: '' })
  const pieces: Blob[] = []
  let receivedBytes = 0
  onProgress?.({ phase: 'downloading', receivedBytes, totalBytes: prepared.bytes })
  while (receivedBytes < prepared.bytes) {
    const piece = await packagePiece(path, prepared, receivedBytes, headers, signal)
    signal.throwIfAborted()
    pieces.push(piece)
    receivedBytes += piece.size
    onProgress?.({ phase: 'downloading', receivedBytes, totalBytes: prepared.bytes })
  }
  return { blob: new Blob(pieces, { type: 'application/zip' }), filename: prepared.filename }
}

export async function getPublishedReviewPackage(exampleId: string, metadata: PreparedPackage, onProgress?: (progress: PackageDownloadProgress) => void, signal?: AbortSignal): Promise<{ blob: Blob; filename: string }> {
  const activeSignal = signal ?? new AbortController().signal
  try {
    return await transferPackage(`/examples/${encodeURIComponent(exampleId)}/package`, metadata, {}, activeSignal, onProgress)
  } catch (error) {
    if (activeSignal.aborted) throw activeSignal.reason
    if (error instanceof ReviewRequestError && error.status === 412) throw new Error('The published package has changed. Reload this page before downloading again.')
    throw new Error('The package download was interrupted. The saved results remain available. Please try downloading again.')
  }
}

export const getReviewPackage = async (run: RunAccess, onProgress?: (progress: PackageDownloadProgress) => void, signal?: AbortSignal): Promise<{ blob: Blob; filename: string }> => {
  const activeSignal = signal ?? new AbortController().signal
  const path = `/runs/${encodeURIComponent(run.run_id)}/package`
  const options = { headers: { 'X-Review-Token': run.run_secret }, signal: activeSignal }
  let phase = 'preparing'
  try {
    activeSignal.throwIfAborted()
    onProgress?.({ phase: 'preparing' })
    let status = await request<PackageStatus>(path, { ...options, method: 'POST' })
    while (status.status === 'preparing') {
      await waitForPackagePoll(activeSignal)
      status = await request<PackageStatus>(`${path}/status`, options)
    }
    if (status.status !== 'ready') {
      throw new ReviewRequestError(status.error_status || 409, status.message || 'Package preparation was interrupted. Please try downloading again; your saved results are unchanged.', true)
    }
    phase = 'downloading'
    return await transferPackage(path, status, options.headers, activeSignal, onProgress)
  } catch (error) {
    if (activeSignal.aborted) throw activeSignal.reason
    if (error instanceof ReviewRequestError && error.hasServerDetail) throw error
    const message = error instanceof ReviewRequestError || error instanceof PackagePieceError ? error.message
      : error instanceof TypeError ? `The connection was interrupted while ${phase} the results package.`
        : error instanceof DOMException && error.name === 'TimeoutError' ? 'The package download timed out after three attempts.'
          : `The results package could not finish ${phase}.`
    throw new Error(`${message} Your saved results are unchanged. Please try downloading again.`)
  }
}
export const cancelReview = (run: RunAccess) => request<RunResult>(`/runs/${run.run_id}/cancel`, {
  method: 'POST', headers: { 'X-Review-Token': run.run_secret },
})
