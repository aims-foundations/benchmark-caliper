import { appPath } from '../paths'

export const DIMENSIONS = [
  ['input_ontology', 'Input ontology'], ['input_content', 'Input content'], ['input_form', 'Input form'],
  ['output_ontology', 'Output ontology'], ['output_content', 'Output content'], ['output_form', 'Output form'],
] as const

export interface Deployment {
  task: string; users: string; inputs: string; outputs: string; success: string; constraints: string
}
export interface Catalog {
  model: string; reasoning_effort: string; max_output_tokens: number
  branches: Record<string, string>; requires_hf_token: boolean; max_items_per_table: number
  benchmarks: Array<{ id: string; name: string; table_count: number }>
}
export interface ReviewRequest { deployment: Deployment; benchmarks: string[]; items_per_table: number; top_k: number }
export interface RunAccess { run_id: string; run_secret: string }
export interface DimensionScore { score: number | null; justification: string; evidence: string[]; information_gaps: string[] }
export interface ReviewedItem {
  evidence_hash: string; rank?: number; status: string; overall_score?: number | null; error?: string
  assessment?: Record<string, DimensionScore>
  evidence: { item: { content: string | null; grading_criterion: unknown }; [key: string]: unknown }
  sources: Array<{ repo: string; branch: string; commit: string; benchmark: string; items_path: string; item_id: string; row: number }>
}
export interface Review {
  run_id: string; status: 'preparing' | 'running' | 'completed' | 'cancelled' | 'failed'; message: string
  model: string; reasoning_effort: string; deployment: Deployment
  scope: { benchmarks: string[]; items_per_table: number; branches: Record<string, string>; sample_only: boolean }
  source_rows: number; total: number; processed: number; complete: number; unresolved: number; errors: number
  usage: Record<string, number>; ranked_items: ReviewedItem[]; unresolved_items: ReviewedItem[]
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(appPath(`/api/item-review${path}`), { cache: 'no-store', ...options })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    const message = typeof body.detail === 'string' ? body.detail : `Request failed (${response.status}). Check your entries and try again.`
    throw new Error(message)
  }
  return response.json() as Promise<T>
}

export const getCatalog = (signal?: AbortSignal) => request<Catalog>('/catalog', { signal })
export const startReview = (body: ReviewRequest, apiKey: string, hfToken: string) => request<RunAccess>('/runs', {
  method: 'POST', headers: { 'Content-Type': 'application/json', 'X-OpenAI-Key': apiKey,
    ...(hfToken ? { 'X-HuggingFace-Key': hfToken } : {}) }, body: JSON.stringify(body),
})
export const getReview = (run: RunAccess, signal?: AbortSignal) => request<Review>(`/runs/${run.run_id}`, {
  headers: { 'X-Review-Token': run.run_secret }, signal,
})
export const cancelReview = (run: RunAccess) => request<Review>(`/runs/${run.run_id}/cancel`, {
  method: 'POST', headers: { 'X-Review-Token': run.run_secret },
})
