import { appPath } from '../paths'

export const DIMENSIONS = [
  ['input_ontology', 'Input ontology'], ['input_content', 'Input content'], ['input_form', 'Input form'],
  ['output_ontology', 'Output ontology'], ['output_content', 'Output content'], ['output_form', 'Output form'],
] as const

export interface Deployment {
  task: string; users: string; inputs: string; outputs: string; success: string; constraints: string
}
export interface SamplingPolicy {
  version: number; method: string; seed: number; items_per_benchmark: number
}
export interface Catalog {
  model: string; reasoning_effort: string; max_output_tokens: number
  branches: Record<string, string>; dataset_access_configured: boolean; table_count: number; source_rows: number
  sampling: SamplingPolicy; sample_max_items: number
  missing_item_tables: Array<{ branch: string; benchmark: string }>
  benchmarks: Array<{ id: string; name: string; table_count: number; source_rows: number; sample_max_items: number }>
}
export interface ReviewRequest { deployment: Deployment }
export interface RunAccess { run_id: string; run_secret: string }
export type Confidence = 'high' | 'medium' | 'low' | 'insufficient'
export interface DimensionScore {
  score: number | null; confidence: Confidence; confidence_rationale: string
  justification: string; evidence: string[]; information_gaps: string[]
}
export interface ReviewedItem {
  evidence_hash: string; rank?: number; status: string; overall_score?: number | null; error?: string
  compatibility_score?: number | null; scored_dimensions?: number; needs_review?: boolean
  assessment?: Record<string, DimensionScore>
  evidence: { item: { content: string | null; grading_criterion: unknown }; [key: string]: unknown }
  sources: Array<{ repo: string; branch: string; commit: string; benchmark: string; items_path: string; item_id: string; row: number }>
}
export interface Review {
  run_id: string; status: 'preparing' | 'running' | 'completed' | 'cancelled' | 'failed'; message: string
  model: string; reasoning_effort: string; deployment: Deployment
  scope: { benchmarks: string[]; table_count: number; source_rows: number; branches: Record<string, string>; sample_only: boolean; sampling: SamplingPolicy; sample_max_items: number }
  scoring_policy: { version: number; neutral_score: number; confidence_weights: Record<Confidence, number>; formula: string }
  source_rows: number; total: number; processed: number; complete: number; needs_review: number; errors: number
  sample_complete: boolean; prepared_benchmarks: number; pagination: { page: number; page_size: number; total_pages: number }
  usage: Record<string, number>; ranked_items: ReviewedItem[]; failed_items: ReviewedItem[]
}

async function fetchResponse(path: string, options: RequestInit = {}): Promise<Response> {
  const response = await fetch(appPath(`/api/item-review${path}`), { cache: 'no-store', ...options })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    const message = typeof body.detail === 'string' ? body.detail : `Request failed (${response.status}). Check your entries and try again.`
    throw new Error(message)
  }
  return response
}

const request = async <T,>(path: string, options?: RequestInit): Promise<T> => (await fetchResponse(path, options)).json()

export const getCatalog = (signal?: AbortSignal) => request<Catalog>('/catalog', { signal })
export const startReview = (body: ReviewRequest, apiKey: string) => request<RunAccess>('/runs', {
  method: 'POST', headers: { 'Content-Type': 'application/json', 'X-OpenAI-Key': apiKey }, body: JSON.stringify(body),
})
export const getReview = (run: RunAccess, page = 1, signal?: AbortSignal) => request<Review>(`/runs/${run.run_id}?page=${page}`, {
  headers: { 'X-Review-Token': run.run_secret }, signal,
})
export const getReviewExport = async (run: RunAccess) => (await fetchResponse(`/runs/${run.run_id}/export`, {
  headers: { 'X-Review-Token': run.run_secret },
})).blob()
export const cancelReview = (run: RunAccess) => request<Review>(`/runs/${run.run_id}/cancel`, {
  method: 'POST', headers: { 'X-Review-Token': run.run_secret },
})
