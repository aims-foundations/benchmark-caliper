/**
 * Backend API client.
 *
 * The Anthropic API key travels in the X-Anthropic-Key header; never in
 * the URL, never in the body, never in a cookie. The pipeline run is a
 * multipart POST that streams Server-Sent Events back; we expose it as an
 * async iterable so callers can render progress as it arrives.
 *
 * See website/SECURITY.md item 1 for the verifiable claims this enforces.
 */

export interface Question {
  id: string
  dimension: string
  question: string
}

export type PipelineEvent =
  | { type: 'step-started'; step: string; total?: number }
  | { type: 'step-progress'; step: string; completed: number; total: number }
  | { type: 'step-completed'; step: string; output?: Record<string, unknown> }
  | { type: 'awaiting-answers'; runId: string; slug: string }
  | {
      type: 'extract-complete'
      runId: string
      pageCount: number
      selectedExamples: string[]
    }
  | {
      type: 'region-complete'
      runId: string
      selectedTemplates: string[]
      webSearchUsed: boolean
    }
  | {
      type: 'run-complete'
      runId: string
      slug?: string
      email?: {
        requested: boolean
        sent?: boolean
        fallback?: boolean
        error?: string | null
      }
    }
  | { type: 'error'; errorClass: string; runId?: string }

export interface AnswerInput {
  apiKey: string
  runId: string
  deploymentDescription: string
  metadata: string
  questions: Question[]
  answers: Array<{ id: string; answer: string }>
  optedInFull: boolean
  /** If set, the report-ready email is sent to this address at run end. */
  email?: string | null
  /** Hint that the caller intends to POST /auto-run next. Server is symmetric on this flag today. */
  autoRun?: boolean
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export interface RunInput {
  apiKey: string
  pdfFile: File
  deploymentDescription: string
  optedInFull: boolean
}

/**
 * POST /api/runs as multipart, stream the SSE response, and yield each
 * decoded event. Throws ApiError on non-2xx; otherwise yields until the
 * stream closes.
 */
export async function* runPipeline(
  input: RunInput,
  signal?: AbortSignal,
): AsyncGenerator<PipelineEvent> {
  const formData = new FormData()
  formData.append('pdf', input.pdfFile)
  formData.append('deployment_description', input.deploymentDescription)
  formData.append('opted_in_full', String(input.optedInFull))

  const response = await fetch('/api/runs', {
    method: 'POST',
    headers: { 'X-Anthropic-Key': input.apiKey },
    body: formData,
    signal,
  })

  if (!response.ok) {
    const text = await response.text().catch(() => '')
    throw new ApiError(response.status, text || response.statusText)
  }

  if (!response.body) {
    throw new ApiError(0, 'no response body')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })

    // Each SSE event ends with a blank line.
    let sep = buffer.indexOf('\n\n')
    while (sep !== -1) {
      const chunk = buffer.slice(0, sep)
      buffer = buffer.slice(sep + 2)
      const event = parseEvent(chunk)
      if (event) yield event
      sep = buffer.indexOf('\n\n')
    }
  }
}

export interface ExtractInput {
  apiKey: string
  runId: string
  /** Optional. If omitted the server reuses the PDF stashed on /api/runs. */
  pdfFile?: File
  /** Optional. If provided, the synthesis step uses it for priority hints. */
  elicitationSummary?: string
}

/**
 * POST /api/runs/{runId}/extract, stream Step 3a (per-page extract +
 * consolidate) events including per-page progress.
 */
export async function* extractPaper(
  input: ExtractInput,
  signal?: AbortSignal,
): AsyncGenerator<PipelineEvent> {
  const formData = new FormData()
  if (input.pdfFile) {
    formData.append('pdf', input.pdfFile)
  }
  if (input.elicitationSummary) {
    formData.append('elicitation_summary', input.elicitationSummary)
  }

  const response = await fetch(
    `/api/runs/${encodeURIComponent(input.runId)}/extract`,
    {
      method: 'POST',
      headers: { 'X-Anthropic-Key': input.apiKey },
      body: formData,
      signal,
    },
  )

  if (!response.ok) {
    const text = await response.text().catch(() => '')
    throw new ApiError(response.status, text || response.statusText)
  }
  if (!response.body) {
    throw new ApiError(0, 'no response body')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let sep = buffer.indexOf('\n\n')
    while (sep !== -1) {
      const chunk = buffer.slice(0, sep)
      buffer = buffer.slice(sep + 2)
      const event = parseEvent(chunk)
      if (event) yield event
      sep = buffer.indexOf('\n\n')
    }
  }
}

export interface ScoreInput {
  apiKey: string
  runId: string
  paperSummary: string
  benchmarkYaml: string
  regionYaml: string
  elicitationSummary: string
}

/**
 * POST /api/runs/{runId}/score. Streams Step 7 (the lone Opus call).
 */
export async function* scoreValidity(
  input: ScoreInput,
  signal?: AbortSignal,
): AsyncGenerator<PipelineEvent> {
  const response = await fetch(
    `/api/runs/${encodeURIComponent(input.runId)}/score`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Anthropic-Key': input.apiKey,
      },
      body: JSON.stringify({
        paper_summary: input.paperSummary,
        benchmark_yaml: input.benchmarkYaml,
        region_yaml: input.regionYaml,
        elicitation_summary: input.elicitationSummary,
      }),
      signal,
    },
  )

  if (!response.ok) {
    const text = await response.text().catch(() => '')
    throw new ApiError(response.status, text || response.statusText)
  }
  if (!response.body) {
    throw new ApiError(0, 'no response body')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let sep = buffer.indexOf('\n\n')
    while (sep !== -1) {
      const chunk = buffer.slice(0, sep)
      buffer = buffer.slice(sep + 2)
      const event = parseEvent(chunk)
      if (event) yield event
      sep = buffer.indexOf('\n\n')
    }
  }
}

export interface RegionInput {
  apiKey: string
  runId: string
  elicitationSummary: string
  benchmarkYaml: string
  skipWebSearch?: boolean
}

/**
 * POST /api/runs/{runId}/region. Streams Steps 4a, 4b, and 5
 * (web-search enrichment, optional). JSON request body — no PDF.
 */
export async function* generateRegion(
  input: RegionInput,
  signal?: AbortSignal,
): AsyncGenerator<PipelineEvent> {
  const response = await fetch(
    `/api/runs/${encodeURIComponent(input.runId)}/region`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Anthropic-Key': input.apiKey,
      },
      body: JSON.stringify({
        elicitation_summary: input.elicitationSummary,
        benchmark_yaml: input.benchmarkYaml,
        skip_web_search: input.skipWebSearch ?? false,
      }),
      signal,
    },
  )

  if (!response.ok) {
    const text = await response.text().catch(() => '')
    throw new ApiError(response.status, text || response.statusText)
  }
  if (!response.body) {
    throw new ApiError(0, 'no response body')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let sep = buffer.indexOf('\n\n')
    while (sep !== -1) {
      const chunk = buffer.slice(0, sep)
      buffer = buffer.slice(sep + 2)
      const event = parseEvent(chunk)
      if (event) yield event
      sep = buffer.indexOf('\n\n')
    }
  }
}

/**
 * POST /api/runs/{runId}/email → store the report-ready email address.
 *
 * Called by the UI after the user fills in the email + mode form.
 * Pass null to clear an existing address.
 */
export async function setRunEmail(
  runId: string,
  email: string | null,
): Promise<void> {
  const r = await fetch(
    `/api/runs/${encodeURIComponent(runId)}/email`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    },
  )
  if (!r.ok && r.status !== 204) {
    const text = await r.text().catch(() => '')
    throw new ApiError(r.status, text || r.statusText)
  }
}

/**
 * POST /api/runs/{runId}/auto-run → kick off the auto-pipeline as a
 * background task. The server already has the API key + PDF + email
 * from earlier calls, so this needs no body and no headers. Returns
 * once the task is enqueued; observe progress via subscribeRunEvents
 * and the final report via fetchReport (or wait for the email).
 */
export async function startAutoRun(runId: string): Promise<void> {
  const r = await fetch(
    `/api/runs/${encodeURIComponent(runId)}/auto-run`,
    { method: 'POST' },
  )
  if (!r.ok && r.status !== 202) {
    const text = await r.text().catch(() => '')
    throw new ApiError(r.status, text || r.statusText)
  }
}

/**
 * GET /api/runs/{runId}/events (SSE) → tail an in-flight auto-run.
 *
 * We use plain fetch + ReadableStream (not EventSource) so that the
 * stream uses the same connection management as the rest of the API
 * client. The endpoint emits ids; if the caller passes `lastEventId`,
 * the server replays buffered events after that id before tailing live.
 */
export async function* subscribeRunEvents(
  runId: string,
  opts: { lastEventId?: string; signal?: AbortSignal } = {},
): AsyncGenerator<PipelineEvent> {
  const headers: Record<string, string> = { Accept: 'text/event-stream' }
  if (opts.lastEventId) headers['Last-Event-ID'] = opts.lastEventId

  const response = await fetch(
    `/api/runs/${encodeURIComponent(runId)}/events`,
    { method: 'GET', headers, signal: opts.signal },
  )
  if (!response.ok) {
    const text = await response.text().catch(() => '')
    throw new ApiError(response.status, text || response.statusText)
  }
  if (!response.body) {
    throw new ApiError(0, 'no response body')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let sep = buffer.indexOf('\n\n')
    while (sep !== -1) {
      const chunk = buffer.slice(0, sep)
      buffer = buffer.slice(sep + 2)
      const event = parseEvent(chunk)
      if (event) yield event
      sep = buffer.indexOf('\n\n')
    }
  }
}

export interface ReportResponse {
  runId: string
  slug: string
  scoring: Record<string, unknown>
  raw: string
}

/**
 * GET /api/runs/{runId}/report → the final scoring + slug for the
 * landing page reached from the email link.
 */
export async function fetchReport(runId: string): Promise<ReportResponse> {
  const r = await fetch(`/api/runs/${encodeURIComponent(runId)}/report`)
  if (!r.ok) {
    const text = await r.text().catch(() => '')
    throw new ApiError(r.status, text || r.statusText)
  }
  const data = await r.json()
  return {
    runId: String(data.run_id ?? runId),
    slug: String(data.slug ?? ''),
    scoring:
      data.scoring && typeof data.scoring === 'object'
        ? (data.scoring as Record<string, unknown>)
        : {},
    raw: typeof data.raw === 'string' ? data.raw : '',
  }
}

/**
 * GET /api/runs/{runId}/export → the full record we have for this run.
 *
 * The endpoint takes no auth beyond the runId itself; if you can hold a
 * valid runId you can fetch its data. UUID4 makes the id unguessable.
 */
export async function exportRun(runId: string): Promise<unknown> {
  const r = await fetch(`/api/runs/${encodeURIComponent(runId)}/export`)
  if (!r.ok) {
    const text = await r.text().catch(() => '')
    throw new ApiError(r.status, text || r.statusText)
  }
  return r.json()
}

/**
 * DELETE /api/runs/{runId} → hard-delete rows + blobs.
 */
export async function deleteRun(runId: string): Promise<void> {
  const r = await fetch(`/api/runs/${encodeURIComponent(runId)}`, {
    method: 'DELETE',
  })
  if (!r.ok && r.status !== 204) {
    const text = await r.text().catch(() => '')
    throw new ApiError(r.status, text || r.statusText)
  }
}

/**
 * POST /api/runs/{runId}/answers, stream Step 2-summary events.
 *
 * Stateless server-side: the client sends back the metadata, the questions,
 * and the user's answers. Same BYOK header discipline as runPipeline.
 */
export async function* submitAnswers(
  input: AnswerInput,
  signal?: AbortSignal,
): AsyncGenerator<PipelineEvent> {
  const response = await fetch(`/api/runs/${encodeURIComponent(input.runId)}/answers`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Anthropic-Key': input.apiKey,
    },
    body: JSON.stringify({
      deployment_description: input.deploymentDescription,
      metadata: input.metadata,
      questions: input.questions,
      answers: input.answers,
      opted_in_full: input.optedInFull,
      email: input.email ?? null,
      auto_run: input.autoRun ?? false,
    }),
    signal,
  })

  if (!response.ok) {
    const text = await response.text().catch(() => '')
    throw new ApiError(response.status, text || response.statusText)
  }

  if (!response.body) {
    throw new ApiError(0, 'no response body')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let sep = buffer.indexOf('\n\n')
    while (sep !== -1) {
      const chunk = buffer.slice(0, sep)
      buffer = buffer.slice(sep + 2)
      const event = parseEvent(chunk)
      if (event) yield event
      sep = buffer.indexOf('\n\n')
    }
  }
}

function parseEvent(chunk: string): PipelineEvent | null {
  let name = ''
  let data = ''
  for (const line of chunk.split('\n')) {
    if (line.startsWith('event: ')) name = line.slice(7)
    else if (line.startsWith('data: ')) data += line.slice(6)
  }
  if (!name) return null
  let payload: Record<string, unknown>
  try {
    payload = JSON.parse(data) as Record<string, unknown>
  } catch {
    return null
  }
  switch (name) {
    case 'step-started':
      return {
        type: 'step-started',
        step: String(payload.step),
        total:
          typeof payload.total === 'number' ? payload.total : undefined,
      }
    case 'step-progress':
      return {
        type: 'step-progress',
        step: String(payload.step),
        completed: Number(payload.completed),
        total: Number(payload.total),
      }
    case 'extract-complete':
      return {
        type: 'extract-complete',
        runId: String(payload.run_id),
        pageCount: Number(payload.page_count),
        selectedExamples: Array.isArray(payload.selected_examples)
          ? (payload.selected_examples as unknown[]).map(String)
          : [],
      }
    case 'region-complete':
      return {
        type: 'region-complete',
        runId: String(payload.run_id),
        selectedTemplates: Array.isArray(payload.selected_templates)
          ? (payload.selected_templates as unknown[]).map(String)
          : [],
        webSearchUsed: Boolean(payload.web_search_used),
      }
    case 'step-completed':
      return {
        type: 'step-completed',
        step: String(payload.step),
        output: payload.output as Record<string, unknown> | undefined,
      }
    case 'awaiting-answers':
      return {
        type: 'awaiting-answers',
        runId: String(payload.run_id),
        slug: String(payload.slug),
      }
    case 'run-complete': {
      const rawEmail = (payload as { email?: unknown }).email
      let email: { requested: boolean; sent?: boolean; fallback?: boolean; error?: string | null } | undefined
      if (rawEmail && typeof rawEmail === 'object') {
        const e = rawEmail as Record<string, unknown>
        email = {
          requested: Boolean(e.requested),
          sent: typeof e.sent === 'boolean' ? e.sent : undefined,
          fallback: typeof e.fallback === 'boolean' ? e.fallback : undefined,
          error: typeof e.error === 'string' ? e.error : null,
        }
      }
      return {
        type: 'run-complete',
        runId: String(payload.run_id),
        slug: payload.slug !== undefined ? String(payload.slug) : undefined,
        email,
      }
    }
    case 'error':
      return {
        type: 'error',
        errorClass: String(payload.error_class ?? 'Unknown'),
        runId: payload.run_id ? String(payload.run_id) : undefined,
      }
    default:
      return null
  }
}