/**
 * App-level integration tests for the multipart + SSE flow.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { App } from './App'

// The embedded stage has its own API/state tests. Here verify that each
// benchmark entry point supplies the exact assessment and honors completion.
vi.mock('./itemAnalysis/ItemAnalysis', () => ({
  ItemAnalysis: ({ assessment, onStatusChange }: {
    assessment: { kind: 'run' | 'gallery'; id: string }
    onStatusChange?: (status: 'pending' | 'in_progress' | 'complete') => void
  }) => <section aria-label="Embedded item analysis">
    <p data-testid="item-assessment-reference">{assessment.kind}:{assessment.id}</p>
    <button onClick={() => onStatusChange?.('in_progress')}>Finish pilot</button>
    <button onClick={() => onStatusChange?.('complete')}>Finish all items</button>
  </section>,
}))

vi.mock('./itemAnalysis/DemoItemAnalysis', () => ({
  DemoItemAnalysis: ({ onStatusChange }: { onStatusChange?: (status: 'pending' | 'in_progress' | 'complete') => void }) =>
    <section aria-label="Free demo item analysis">
      <button onClick={() => onStatusChange?.('in_progress')}>Finish demo pilot</button>
      <button onClick={() => onStatusChange?.('complete')}>Finish demo sample</button>
    </section>,
}))

vi.mock('./itemAnalysis/SavedItemAnalysis', () => ({
  SavedItemAnalysis: ({ assessmentId, onRunOwnAnalysis }: { assessmentId: string; onRunOwnAnalysis: () => void }) =>
    <section id="item-analysis-stage" aria-label="Saved item analysis">
      <p data-testid="saved-item-assessment-reference">{assessmentId}</p>
      <button onClick={onRunOwnAnalysis}>Run your own analysis</button>
    </section>,
}))

function makeStream(body: string): ReadableStream<Uint8Array> {
  const encoder = new TextEncoder()
  return new ReadableStream<Uint8Array>({
    start(controller) {
      controller.enqueue(encoder.encode(body))
      controller.close()
    },
  })
}

function makeStreamingResponse(body: string): Response {
  return new Response(makeStream(body), {
    status: 200,
    headers: { 'Content-Type': 'text/event-stream' },
  })
}

const HAPPY_STREAM =
  'event: step-started\ndata: {"step":"0-slug"}\n\n' +
  'event: step-completed\ndata: {"step":"0-slug","output":{"slug":"jakarta_admin"}}\n\n' +
  'event: step-started\ndata: {"step":"1-metadata"}\n\n' +
  'event: step-completed\ndata: {"step":"1-metadata","output":{"metadata":"- name: sea-helm"}}\n\n' +
  'event: step-started\ndata: {"step":"2-questions"}\n\n' +
  'event: step-completed\ndata: {"step":"2-questions","output":{"questions":[{"id":"Q1","dimension":"IC","question":"Sample question?"}],"metadata":"- name: sea-helm","run_id":"run-x","slug":"jakarta_admin"}}\n\n' +
  'event: awaiting-answers\ndata: {"run_id":"run-x","slug":"jakarta_admin"}\n\n'

const SUMMARY_STREAM =
  'event: step-started\ndata: {"step":"2-summary"}\n\n' +
  'event: step-completed\ndata: {"step":"2-summary","output":{"summary":"## Use Case\\nIndonesian admin chatbot.","run_id":"run-x"}}\n\n' +
  'event: run-complete\ndata: {"run_id":"run-x"}\n\n'

const SCORE_STREAM =
  'event: step-started\ndata: {"step":"7-score"}\n\n' +
  'event: step-completed\ndata: {"step":"7-score","output":{"scoring":{"input_ontology":{"score":3,"reasoning":"Mixed evidence on cultural categories."},"output_form":{"score":4,"reasoning":"Modality matches deployment."}},"raw":"{...}"}}\n\n' +
  'event: run-complete\ndata: {"run_id":"run-x"}\n\n'

const REGION_STREAM =
  'event: step-started\ndata: {"step":"4a-template"}\n\n' +
  'event: step-completed\ndata: {"step":"4a-template","output":{"selected":["southeast_asia.yaml"]}}\n\n' +
  'event: step-started\ndata: {"step":"4b-synthesize"}\n\n' +
  'event: step-completed\ndata: {"step":"4b-synthesize","output":{"region_scaffold":"name: scaffold\\nliteracy: \\"[NEEDS VERIFICATION]\\"\\n"}}\n\n' +
  'event: step-started\ndata: {"step":"5-web-search"}\n\n' +
  'event: step-completed\ndata: {"step":"5-web-search","output":{"region_yaml":"name: indonesia_admin_chatbot\\nliteracy: 0.96\\n"}}\n\n' +
  'event: region-complete\ndata: {"run_id":"run-x","selected_templates":["southeast_asia.yaml"],"web_search_used":true}\n\n'

// Step 5b runs between the region and score steps. The tests don't supply
// an HF dataset, so the realistic stream is a single da-skipped event.
const DA_STREAM =
  'event: da-skipped\ndata: {"run_id":"run-x","reason":"no hf target resolved"}\n\n'

const EXTRACT_STREAM =
  'event: step-started\ndata: {"step":"3a-extract","total":2}\n\n' +
  'event: step-progress\ndata: {"step":"3a-extract","completed":1,"total":2}\n\n' +
  'event: step-progress\ndata: {"step":"3a-extract","completed":2,"total":2}\n\n' +
  'event: step-completed\ndata: {"step":"3a-extract"}\n\n' +
  'event: step-started\ndata: {"step":"3a-consolidate"}\n\n' +
  'event: step-completed\ndata: {"step":"3a-consolidate","output":{"paper_summary":"## Metadata\\nThe paper covers..."}}\n\n' +
  'event: step-started\ndata: {"step":"3b-select"}\n\n' +
  'event: step-completed\ndata: {"step":"3b-select","output":{"selected":["helm.yaml"]}}\n\n' +
  'event: step-started\ndata: {"step":"3b-synthesize"}\n\n' +
  'event: step-completed\ndata: {"step":"3b-synthesize","output":{"benchmark_yaml":"name: synthesized_run\\nfull_name: Synthesized\\n"}}\n\n' +
  'event: extract-complete\ndata: {"run_id":"run-x","page_count":2,"selected_examples":["helm.yaml"]}\n\n'

function makePdfFile(): File {
  return new File([new Uint8Array([0x25, 0x50, 0x44, 0x46])], 'paper.pdf', {
    type: 'application/pdf',
  })
}

describe('App', () => {
  let originalFetch: typeof fetch

  beforeEach(() => {
    sessionStorage.clear()
    localStorage.clear()
    // Most tests below assume the user has already cleared the consent
    // gate. Tests that exercise the gate explicitly clear this.
    localStorage.setItem('consent_v1', 'yes')
    originalFetch = globalThis.fetch
    globalThis.fetch = vi.fn(async () => new Response(JSON.stringify({ benchmarks: [] }), { status: 200 })) as unknown as typeof fetch
  })

  afterEach(() => {
    vi.useRealTimers()
    globalThis.fetch = originalFetch
    window.history.replaceState(null, '', '/')
  })

  it('shows the key form first when no key is stored', () => {
    render(<App />)
    expect(
      screen.getByRole('heading', { name: /enter your anthropic api key/i }),
    ).toBeInTheDocument()
  })

  it('shows the consent gate first on a fresh browser', async () => {
    localStorage.clear() // reverse the beforeEach default
    render(<App />)
    expect(
      screen.getByRole('heading', { name: /before you start/i }),
    ).toBeInTheDocument()
    // Key form should not yet be visible.
    expect(
      screen.queryByRole('heading', { name: /enter your anthropic api key/i }),
    ).not.toBeInTheDocument()
  })

  it('clicking "I understand" records consent and shows the key form', async () => {
    localStorage.clear()
    const user = userEvent.setup()
    render(<App />)
    await user.click(
      screen.getByRole('button', { name: /i understand/i }),
    )
    expect(localStorage.getItem('consent_v1')).toBe('yes')
    expect(
      screen.getByRole('heading', { name: /enter your anthropic api key/i }),
    ).toBeInTheDocument()
  })

  it('opt-in checkbox is unchecked by default and submits opted_in_full=false', async () => {
    const user = userEvent.setup()
    let captured: FormData | undefined
    globalThis.fetch = vi.fn(async (url: unknown, init: unknown) => {
      const u = String(url)
      const i = init as RequestInit
      if (u === '/api/runs') captured = i.body as FormData
      return makeStreamingResponse(HAPPY_STREAM)
    }) as unknown as typeof fetch

    render(<App />)
    await user.type(screen.getByPlaceholderText('sk-ant-...'), 'sk-ant-test')
    await user.click(screen.getByRole('button', { name: /save key/i }))
    await user.upload(
      screen.getByLabelText(/benchmark paper/i) as HTMLInputElement,
      makePdfFile(),
    )
    await user.type(
      screen.getByLabelText(/deployment description/i),
      'desc',
    )

    const checkbox = screen.getByRole('checkbox', {
      name: /optional.*store my prompts/i,
    })
    expect(checkbox).not.toBeChecked()

    await user.click(screen.getByRole('button', { name: /^run$/i }))
    await waitFor(() => expect(captured).toBeDefined())
    expect((captured as FormData).get('opted_in_full')).toBe('false')
  })

  it('after the user saves a key, the run form appears', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(
      screen.getByPlaceholderText('sk-ant-...'),
      'sk-ant-test',
    )
    await user.click(screen.getByRole('button', { name: /save key/i }))
    expect(
      screen.getByRole('heading', { name: /describe your deployment/i }),
    ).toBeInTheDocument()
  })

  it('runs pipeline → answers questions → renders summary', async () => {
    const user = userEvent.setup()
    const fakeKey = 'sk-ant-FAKE_INTEGRATION_xyz'

    interface CapturedCall {
      url: string
      headers: Record<string, string>
      body: unknown
    }
    const calls: CapturedCall[] = []

    globalThis.fetch = vi.fn(async (url: unknown, init: unknown) => {
      const u = String(url)
      const i = init as RequestInit
      calls.push({
        url: u,
        headers: i.headers as Record<string, string>,
        body: i.body,
      })
      // Route to the right canned stream
      if (u.endsWith('/answers')) {
        return makeStreamingResponse(SUMMARY_STREAM)
      }
      return makeStreamingResponse(HAPPY_STREAM)
    }) as unknown as typeof fetch

    render(<App />)

    // 1. Enter key
    await user.type(screen.getByPlaceholderText('sk-ant-...'), fakeKey)
    await user.click(screen.getByRole('button', { name: /save key/i }))

    // 2. Upload PDF + description, click Run
    await user.upload(
      screen.getByLabelText(/benchmark paper/i) as HTMLInputElement,
      makePdfFile(),
    )
    await user.type(
      screen.getByLabelText(/deployment description/i),
      'Indonesian government chatbot',
    )
    await user.click(screen.getByRole('button', { name: /^run$/i }))

    // 3. Pipeline completes → AnswerForm appears
    await waitFor(() =>
      expect(
        screen.getByRole('heading', {
          name: /answer the elicitation questions/i,
        }),
      ).toBeInTheDocument(),
    )
    expect(screen.getByText(/sample question/i)).toBeInTheDocument()

    // 4. Type an answer and submit
    const answerInput = screen.getByRole('textbox')
    await user.type(answerInput, 'My team supports Bahasa Indonesia.')
    await user.click(screen.getByRole('button', { name: /submit answers/i }))

    // 5. Summary appears
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /elicitation summary/i }),
      ).toBeInTheDocument(),
    )
    expect(screen.getByText(/Indonesian admin chatbot/i)).toBeInTheDocument()
    expect(screen.getByText('jakarta_admin')).toBeInTheDocument()
    expect(screen.getByText('run-x')).toBeInTheDocument()

    // BYOK invariants across both calls
    expect(calls).toHaveLength(2)
    expect(calls[0].url).toContain('/api/runs')
    expect(calls[0].url).not.toContain('/answers')
    expect(calls[1].url).toContain('/api/runs/run-x/answers')

    for (const c of calls) {
      expect(c.headers['X-Anthropic-Key']).toBe(fakeKey)
      expect(c.url).not.toContain('sk-ant-')
      expect(c.url).not.toContain('FAKE_INTEGRATION')
    }

    // First call: FormData body must not contain the key.
    const firstBody = calls[0].body as FormData
    for (const [, value] of firstBody.entries()) {
      const s = typeof value === 'string' ? value : ''
      expect(s).not.toContain('sk-ant-')
      expect(s).not.toContain('FAKE_INTEGRATION')
    }
    // Second call: JSON body must not contain the key.
    const secondBody = calls[1].body as string
    expect(secondBody).not.toContain('sk-ant-')
    expect(secondBody).not.toContain('FAKE_INTEGRATION')
  })

  it('shows an error if the API rejects the request', async () => {
    const user = userEvent.setup()
    globalThis.fetch = vi.fn(
      async () => new Response('upstream failed', { status: 502 }),
    ) as unknown as typeof fetch

    render(<App />)
    await user.type(
      screen.getByPlaceholderText('sk-ant-...'),
      'sk-ant-test',
    )
    await user.click(screen.getByRole('button', { name: /save key/i }))
    await user.upload(
      screen.getByLabelText(/benchmark paper/i) as HTMLInputElement,
      makePdfFile(),
    )
    await user.type(
      screen.getByLabelText(/deployment description/i),
      'desc',
    )
    await user.click(screen.getByRole('button', { name: /^run$/i }))

    await waitFor(() =>
      expect(screen.getByRole('alert')).toBeInTheDocument(),
    )
  })

  it('shows an error if the pipeline emits an error event mid-stream', async () => {
    const user = userEvent.setup()
    const errBody =
      'event: step-started\ndata: {"step":"0-slug"}\n\n' +
      'event: error\ndata: {"error_class":"RuntimeError","run_id":"abc"}\n\n'
    globalThis.fetch = vi.fn(
      async () => makeStreamingResponse(errBody),
    ) as unknown as typeof fetch

    render(<App />)
    await user.type(
      screen.getByPlaceholderText('sk-ant-...'),
      'sk-ant-test',
    )
    await user.click(screen.getByRole('button', { name: /save key/i }))
    await user.upload(
      screen.getByLabelText(/benchmark paper/i) as HTMLInputElement,
      makePdfFile(),
    )
    await user.type(
      screen.getByLabelText(/deployment description/i),
      'desc',
    )
    await user.click(screen.getByRole('button', { name: /^run$/i }))

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument()
      expect(screen.getByRole('alert').textContent).toMatch(/RuntimeError/)
    })
  })

  it('summary view → Extract paper → live page progress → ExtractedView', async () => {
    const user = userEvent.setup()
    const fakeKey = 'sk-ant-test'

    interface CapturedCall {
      url: string
      method: string
      headers: Record<string, string>
      body: unknown
    }
    const calls: CapturedCall[] = []

    globalThis.fetch = vi.fn(async (url: unknown, init: unknown) => {
      const u = String(url)
      const i = (init as RequestInit) ?? {}
      calls.push({
        url: u,
        method: i.method ?? 'GET',
        headers: (i.headers ?? {}) as Record<string, string>,
        body: i.body,
      })
      if (u.endsWith('/extract'))
        return makeStreamingResponse(EXTRACT_STREAM)
      if (u.endsWith('/answers'))
        return makeStreamingResponse(SUMMARY_STREAM)
      return makeStreamingResponse(HAPPY_STREAM)
    }) as unknown as typeof fetch

    render(<App />)

    // 1. key + run + answers → summary
    await user.type(screen.getByPlaceholderText('sk-ant-...'), fakeKey)
    await user.click(screen.getByRole('button', { name: /save key/i }))
    await user.upload(
      screen.getByLabelText(/benchmark paper/i) as HTMLInputElement,
      makePdfFile(),
    )
    await user.type(
      screen.getByLabelText(/deployment description/i),
      'desc',
    )
    await user.click(screen.getByRole('button', { name: /^run$/i }))
    await waitFor(() =>
      expect(
        screen.getByRole('heading', {
          name: /answer the elicitation questions/i,
        }),
      ).toBeInTheDocument(),
    )
    await user.type(screen.getByRole('textbox'), 'answer')
    await user.click(screen.getByRole('button', { name: /submit answers/i }))
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /elicitation summary/i }),
      ).toBeInTheDocument(),
    )

    // 2. Choose step-by-step mode. The server already has the PDF from
    // /api/runs, so extraction starts without asking for another upload.
    await user.click(screen.getByLabelText(/walk me through each step/i))
    await user.click(
      screen.getByRole('button', { name: /start step-by-step/i }),
    )

    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /paper analyzed/i }),
      ).toBeInTheDocument(),
    )

    // Default tab is the paper summary.
    expect(screen.getByText(/the paper covers/i)).toBeInTheDocument()
    // Page count rendered.
    expect(screen.getByText('2', { selector: 'dd' })).toBeInTheDocument()
    // Selected reference appears at least once on the page.
    expect(screen.getAllByText(/helm\.yaml/i).length).toBeGreaterThan(0)

    // Switch to the YAML tab and confirm the synthesized YAML appears.
    await user.click(screen.getByRole('tab', { name: /benchmark yaml/i }))
    expect(
      screen.getByText(/name: synthesized_run/),
    ).toBeInTheDocument()

    // The extract call hit /api/runs/run-x/extract with the BYOK key,
    // and carried the elicitation summary from the prior step.
    const extractCall = calls.find((c) => c.url.endsWith('/extract'))
    expect(extractCall).toBeDefined()
    expect(extractCall?.method).toBe('POST')
    expect(extractCall?.headers['X-Anthropic-Key']).toBe(fakeKey)
    expect(extractCall?.body).toBeInstanceOf(FormData)
    const fd = extractCall?.body as FormData
    expect(fd.get('elicitation_summary')).toContain('Indonesian admin chatbot')
  })

  it('extracted view → Build region context → RegionView with enriched YAML', async () => {
    const user = userEvent.setup()
    const fakeKey = 'sk-ant-test'

    interface CapturedCall {
      url: string
      method: string
      headers: Record<string, string>
      body: unknown
    }
    const calls: CapturedCall[] = []

    globalThis.fetch = vi.fn(async (url: unknown, init: unknown) => {
      const u = String(url)
      const i = (init as RequestInit) ?? {}
      calls.push({
        url: u,
        method: i.method ?? 'GET',
        headers: (i.headers ?? {}) as Record<string, string>,
        body: i.body,
      })
      if (u.endsWith('/dataset-analysis'))
        return makeStreamingResponse(DA_STREAM)
      if (u.endsWith('/region')) return makeStreamingResponse(REGION_STREAM)
      if (u.endsWith('/extract')) return makeStreamingResponse(EXTRACT_STREAM)
      if (u.endsWith('/answers')) return makeStreamingResponse(SUMMARY_STREAM)
      return makeStreamingResponse(HAPPY_STREAM)
    }) as unknown as typeof fetch

    render(<App />)

    // Drive through the elicitation arc
    await user.type(screen.getByPlaceholderText('sk-ant-...'), fakeKey)
    await user.click(screen.getByRole('button', { name: /save key/i }))
    await user.upload(
      screen.getByLabelText(/benchmark paper/i) as HTMLInputElement,
      makePdfFile(),
    )
    await user.type(
      screen.getByLabelText(/deployment description/i),
      'desc',
    )
    await user.click(screen.getByRole('button', { name: /^run$/i }))
    await waitFor(() =>
      expect(
        screen.getByRole('heading', {
          name: /answer the elicitation questions/i,
        }),
      ).toBeInTheDocument(),
    )
    await user.type(screen.getByRole('textbox'), 'answer')
    await user.click(screen.getByRole('button', { name: /submit answers/i }))
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /elicitation summary/i }),
      ).toBeInTheDocument(),
    )

    // Choose step-by-step mode; extraction starts with the stashed PDF.
    await user.click(screen.getByLabelText(/walk me through each step/i))
    await user.click(
      screen.getByRole('button', { name: /start step-by-step/i }),
    )
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /paper analyzed/i }),
      ).toBeInTheDocument(),
    )

    // Click "Build region context →"
    await user.click(
      screen.getByRole('button', { name: /build region context/i }),
    )

    // RegionView appears with the enriched final YAML
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /region context built/i }),
      ).toBeInTheDocument(),
    )
    expect(screen.getByText(/indonesia_admin_chatbot/)).toBeInTheDocument()

    // Toggle to scaffold; the scaffold YAML appears in the tabpanel
    await user.click(screen.getByRole('tab', { name: /scaffold/i }))
    const tabpanel = screen.getByRole('tabpanel')
    expect(tabpanel.textContent).toContain('name: scaffold')
    expect(tabpanel.textContent).toContain('NEEDS VERIFICATION')

    // The /region call carried the BYOK key in a header (not body or URL)
    const regionCall = calls.find((c) => c.url.endsWith('/region'))
    expect(regionCall).toBeDefined()
    expect(regionCall?.headers['X-Anthropic-Key']).toBe(fakeKey)
    expect(regionCall?.url).not.toContain('sk-ant-')
    expect(regionCall?.body as string).not.toContain('sk-ant-')
  })

  it('regioned view → Score validity → ScoringView with per-dimension scores', async () => {
    const user = userEvent.setup()
    const fakeKey = 'sk-ant-test'

    interface CapturedCall {
      url: string
      method: string
      headers: Record<string, string>
      body: unknown
    }
    const calls: CapturedCall[] = []

    globalThis.fetch = vi.fn(async (url: unknown, init: unknown) => {
      const u = String(url)
      const i = (init as RequestInit) ?? {}
      calls.push({
        url: u,
        method: i.method ?? 'GET',
        headers: (i.headers ?? {}) as Record<string, string>,
        body: i.body,
      })
      if (u.endsWith('/compose-prompt')) {
        return new Response(
          JSON.stringify({ composed_prompt: 'COMPOSED PROMPT', run_id: 'run-x' }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        )
      }
      if (u.endsWith('/score')) return makeStreamingResponse(SCORE_STREAM)
      if (u.endsWith('/dataset-analysis'))
        return makeStreamingResponse(DA_STREAM)
      if (u.endsWith('/region')) return makeStreamingResponse(REGION_STREAM)
      if (u.endsWith('/extract')) return makeStreamingResponse(EXTRACT_STREAM)
      if (u.endsWith('/answers')) return makeStreamingResponse(SUMMARY_STREAM)
      return makeStreamingResponse(HAPPY_STREAM)
    }) as unknown as typeof fetch

    render(<App />)

    // Drive through the entire pipeline to the regioned view
    await user.type(screen.getByPlaceholderText('sk-ant-...'), fakeKey)
    await user.click(screen.getByRole('button', { name: /save key/i }))
    await user.upload(
      screen.getByLabelText(/benchmark paper/i) as HTMLInputElement,
      makePdfFile(),
    )
    await user.type(
      screen.getByLabelText(/deployment description/i),
      'desc',
    )
    await user.click(screen.getByRole('button', { name: /^run$/i }))
    await waitFor(() =>
      expect(
        screen.getByRole('heading', {
          name: /answer the elicitation questions/i,
        }),
      ).toBeInTheDocument(),
    )
    await user.type(screen.getByRole('textbox'), 'answer')
    await user.click(screen.getByRole('button', { name: /submit answers/i }))
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /elicitation summary/i }),
      ).toBeInTheDocument(),
    )
    await user.click(screen.getByLabelText(/walk me through each step/i))
    await user.click(
      screen.getByRole('button', { name: /start step-by-step/i }),
    )
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /paper analyzed/i }),
      ).toBeInTheDocument(),
    )
    await user.click(
      screen.getByRole('button', { name: /build region context/i }),
    )
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /region context built/i }),
      ).toBeInTheDocument(),
    )

    // Preview the composed scoring prompt, then authorize the Opus call.
    await user.click(
      screen.getByRole('button', { name: /preview scoring prompt/i }),
    )
    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /review the scoring prompt/i }),
      ).toBeInTheDocument(),
    )
    await user.click(
      screen.getByRole('button', { name: /send to opus/i }),
    )

    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /benchmark validity assessment/i }),
      ).toBeInTheDocument(),
    )

    // Per-dimension scores are visible.
    expect(screen.getByText(/Input Ontology/i)).toBeInTheDocument()
    expect(screen.getByText('3 / 5')).toBeInTheDocument()
    expect(screen.getByText('4 / 5')).toBeInTheDocument()
    expect(screen.getByTestId('item-assessment-reference')).toHaveTextContent('run:run-x')
    expect(window.location.pathname).toBe('/run/run-x')
    expect(screen.getByText('Benchmark assessment ready · item analysis available')).toBeInTheDocument()
    expect(screen.queryByText('Full dataset classified')).not.toBeInTheDocument()

    // A completed pilot remains reviewable and exportable. Full-dataset
    // coverage has a separate processing status and is optional.
    await user.click(screen.getByRole('button', { name: 'Finish pilot' }))
    expect(screen.queryByText('Full dataset classified')).not.toBeInTheDocument()
    expect(screen.getByText('Benchmark assessment ready · item analysis started')).toBeInTheDocument()
    expect(screen.getByText(/Review and export the pilot when it finishes/)).toHaveTextContent('Continuing through the full prepared dataset is optional.')
    expect(screen.getByRole('link', { name: 'Return to item analysis ↓' })).toHaveAttribute('href', '#item-analysis-stage')
    await user.click(screen.getByRole('button', { name: 'Finish all items' }))
    expect(screen.getByText('Full dataset classified')).toBeInTheDocument()
    expect(screen.getByText(/Every item in the prepared dataset has a saved classification/)).toHaveTextContent('Independent human review has not been recorded here.')
    expect(screen.queryByText('Validity analysis complete')).not.toBeInTheDocument()
    expect(screen.getByText('Results ready').closest('li')).toHaveAttribute('aria-current', 'step')

    // The /score call carried the BYOK key.
    const scoreCall = calls.find((c) => c.url.endsWith('/score'))
    expect(scoreCall).toBeDefined()
    expect(scoreCall?.method).toBe('POST')
    expect(scoreCall?.headers['X-Anthropic-Key']).toBe(fakeKey)
    expect(scoreCall?.url).not.toContain('sk-ant-')
    expect(scoreCall?.body as string).not.toContain('sk-ant-')
    // Full pipeline drive-through (answers → extract → region → 5b → score)
    // legitimately runs long; give it headroom over the 5s default.
  }, 15000)

  it('continues automatic benchmark scoring into the matching item stage', async () => {
    const user = userEvent.setup()
    sessionStorage.setItem('anthropic_api_key', 'sk-ant-test')
    globalThis.fetch = vi.fn(async (url: unknown) => {
      const path = String(url)
      if (path === '/api/gallery') return new Response(JSON.stringify({ benchmarks: [] }), { status: 200 })
      if (path.endsWith('/answers')) return makeStreamingResponse(SUMMARY_STREAM)
      if (path.endsWith('/auto-run')) return new Response('{}', { status: 202 })
      if (path.endsWith('/events')) return makeStreamingResponse(SCORE_STREAM)
      return makeStreamingResponse(HAPPY_STREAM)
    }) as unknown as typeof fetch
    render(<App />)
    await user.upload(screen.getByLabelText(/benchmark paper/i), makePdfFile())
    await user.type(screen.getByLabelText(/deployment description/i), 'desc')
    await user.click(screen.getByRole('button', { name: /^run$/i }))
    await screen.findByRole('heading', { name: /answer the elicitation questions/i })
    await user.type(screen.getByRole('textbox'), 'answer')
    await user.click(screen.getByRole('button', { name: /submit answers/i }))
    await user.click(await screen.findByRole('button', { name: /start scoring/i }))
    expect(await screen.findByTestId('item-assessment-reference')).toHaveTextContent('run:run-x')
    expect(window.location.pathname).toBe('/run/run-x')
    expect(screen.getByText('Benchmark assessment ready · item analysis available')).toBeInTheDocument()
  })

  it('continues the prerecorded MathDial benchmark into free demo item analysis', async () => {
    vi.useFakeTimers()
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /try a demo run/i }))
    fireEvent.click(screen.getByRole('button', { name: /run the demo/i }))
    await act(async () => { await vi.advanceTimersByTimeAsync(10_000) })
    fireEvent.click(screen.getByRole('button', { name: /submit answers/i }))
    await act(async () => { await vi.advanceTimersByTimeAsync(10_000) })
    fireEvent.click(screen.getByRole('button', { name: /start scoring/i }))
    await act(async () => { await vi.advanceTimersByTimeAsync(40_000) })
    expect(screen.getByRole('region', { name: 'Free demo item analysis' })).toBeInTheDocument()
    expect(screen.queryByTestId('item-assessment-reference')).not.toBeInTheDocument()
    expect(window.location.pathname).toBe('/caliper')
    expect(new URLSearchParams(window.location.search).get('demo')).toBe('mathdial')
    expect(new URLSearchParams(window.location.search).get('stage')).toBe('items')
    expect(new URLSearchParams(window.location.search).has('assessment')).toBe(false)
    expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
    expect(globalThis.fetch).toHaveBeenCalledTimes(1) // Read-only gallery listing.
    expect(screen.getByText('Results ready').closest('li')).not.toHaveAttribute('aria-current', 'step')
    fireEvent.click(screen.getByRole('button', { name: 'Finish demo pilot' }))
    expect(screen.getByText('Results ready').closest('li')).not.toHaveAttribute('aria-current', 'step')
    fireEvent.click(screen.getByRole('button', { name: 'Finish demo sample' }))
    expect(screen.getByText('Results ready').closest('li')).toHaveAttribute('aria-current', 'step')
  })

  it('restores a free item-demo URL without fetching a live assessment', async () => {
    window.history.replaceState(null, '', '/caliper?demo=mathdial&stage=items')
    const first = render(<App />)
    expect(screen.getByRole('region', { name: 'Free demo item analysis' })).toBeInTheDocument()
    expect(screen.queryByTestId('item-assessment-reference')).not.toBeInTheDocument()
    first.unmount()
    render(<App />)
    expect(screen.getByRole('region', { name: 'Free demo item analysis' })).toBeInTheDocument()
    expect(screen.queryByTestId('item-assessment-reference')).not.toBeInTheDocument()
    expect(vi.mocked(globalThis.fetch).mock.calls.map(([url]) => String(url))).toEqual(['/api/gallery', '/api/gallery'])
  })

  it('opens the free demo directly and can preview its item stage without a key', async () => {
    localStorage.clear()
    window.history.replaceState(null, '', '/caliper?demo=mathdial')
    const user = userEvent.setup()
    render(<App />)
    expect(screen.getByRole('button', { name: /run the demo/i })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: /enter your anthropic api key/i })).not.toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /preview item analysis/i }))
    expect(screen.getByRole('region', { name: 'Free demo item analysis' })).toBeInTheDocument()
    expect(new URLSearchParams(window.location.search).get('stage')).toBe('items')
    expect(vi.mocked(globalThis.fetch).mock.calls.map(([url]) => String(url))).toEqual(['/api/gallery'])
  })

  it('leaves free demo mode when the user selects a gallery assessment', async () => {
    const user = userEvent.setup()
    const entry = { id: 'expert__live-mmlu', benchmark_name: 'Live MMLU', slug: 'live_context', deployment_description: 'A real deployment' }
    globalThis.fetch = vi.fn(async (url: unknown) => new Response(JSON.stringify(String(url) === '/api/gallery'
      ? { benchmarks: [entry] } : { ...entry, scoring: { input_content: { score: 3 } }, raw: '{}' }), { status: 200 })) as unknown as typeof fetch
    window.history.replaceState(null, '', '/caliper?demo=mathdial&stage=items')
    render(<App />)
    await user.click(screen.getByRole('button', { name: 'Finish demo sample' }))
    expect(screen.getByText('Results ready').closest('li')).toHaveAttribute('aria-current', 'step')
    await user.click(await screen.findByRole('button', { name: /Live MMLU A real deployment/ }))
    expect(await screen.findByTestId('item-assessment-reference')).toHaveTextContent('gallery:expert__live-mmlu')
    expect(screen.queryByRole('region', { name: 'Free demo item analysis' })).not.toBeInTheDocument()
    expect(new URLSearchParams(window.location.search).get('assessment')).toBe(entry.id)
    expect(new URLSearchParams(window.location.search).has('demo')).toBe(false)
    expect(screen.getByText('Results ready').closest('li')).not.toHaveAttribute('aria-current', 'step')
  })

  it('opens published gallery results without mounting the private workflow and preserves the existing site layout', async () => {
    const user = userEvent.setup()
    const published = { id: 'gsm8k', benchmark_name: 'GSM8K', slug: 'us_statistics', deployment_description: 'A statistical analysis assistant' }
    const ordinary = { id: 'expert__glue', benchmark_name: 'GLUE', slug: 'english', deployment_description: 'An English assistant' }
    const storageKey = 'item_analysis_run_v1:gallery:gsm8k'
    const access = JSON.stringify({ run_id: 'my-private-run', run_secret: 'private-token' })
    localStorage.setItem(storageKey, access)
    const dimensions = Object.fromEntries(['input_ontology', 'input_content', 'input_form', 'output_ontology', 'output_content', 'output_form'].map(id => [id, { score: 2, justification: 'Saved benchmark reasoning.' }]))
    const fetchSpy = vi.fn(async (url: unknown) => {
      const path = String(url)
      if (path === '/api/gallery') return new Response(JSON.stringify({ benchmarks: [published, ordinary] }))
      const entry = path.endsWith('/gsm8k') ? published : ordinary
      return new Response(JSON.stringify({ ...entry, scoring: { dimensions }, raw: '{}',
        elicitation_summary: '| IO | HIGH | Needed |',
        ...(entry === published ? { item_analysis: { run_id: 'published-run', item_count: 100, total_items: 1319, completed_at: '2026-10-28T19:58:19Z', model: 'saved-model' } } : {}),
      }))
    })
    globalThis.fetch = fetchSpy as typeof fetch
    window.history.replaceState(null, '', '/caliper?assessment=gsm8k#item-analysis-stage')

    render(<App />)
    expect(await screen.findByTestId('saved-item-assessment-reference')).toHaveTextContent('gsm8k')
    expect(screen.queryByRole('region', { name: 'Embedded item analysis' })).not.toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Benchmark Caliper.' })).toBeVisible()
    expect(screen.getByRole('complementary', { name: 'Benchmark gallery' })).toBeVisible()
    expect(document.querySelectorAll('.score-row')).toHaveLength(6)
    expect(screen.getByText('High priority')).toBeVisible()
    expect(screen.getByRole('link', { name: 'Open original benchmark report' })).toHaveAttribute('href', '/api/gallery/gsm8k/review.pdf')
    expect(screen.queryByText('Full dataset classified')).not.toBeInTheDocument()
    expect(document.querySelector('.priority-legend')).not.toBeInTheDocument()
    expect(localStorage.getItem(storageKey)).toBe(access)
    expect(fetchSpy.mock.calls.every(([url]) => String(url).startsWith('/api/gallery'))).toBe(true)

    await user.click(screen.getByRole('button', { name: 'Run your own analysis' }))
    expect(await screen.findByTestId('item-assessment-reference')).toHaveTextContent('gallery:gsm8k')
    expect(screen.getByRole('region', { name: 'Saved item analysis' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'Back to saved item analysis' })).toHaveAttribute('href', '#item-analysis-stage')
    expect(localStorage.getItem(storageKey)).toBe(access)

    await user.click(screen.getByRole('button', { name: /GLUE An English assistant/ }))
    await waitFor(() => expect(screen.getByTestId('item-assessment-reference')).toHaveTextContent('gallery:expert__glue'))
    expect(screen.queryByRole('region', { name: 'Saved item analysis' })).not.toBeInTheDocument()
    expect(screen.getByText('Benchmark assessment ready · item analysis available')).toBeInTheDocument()
    expect(localStorage.getItem(storageKey)).toBe(access)
  })

  it('does not return to a stale replay after exiting the demo', async () => {
    vi.useFakeTimers()
    window.history.replaceState(null, '', '/caliper?demo=mathdial')
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /run the demo/i }))
    await act(async () => { await vi.advanceTimersByTimeAsync(800) })
    fireEvent.click(screen.getByRole('button', { name: /exit demo/i }))
    await act(async () => { await vi.advanceTimersByTimeAsync(90_000) })
    expect(screen.getByRole('heading', { name: /enter your anthropic api key/i })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: /answer the elicitation questions/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('region', { name: 'Free demo item analysis' })).not.toBeInTheDocument()
    expect(new URLSearchParams(window.location.search).has('demo')).toBe(false)
  })

  it.each(['', '?demo=mathdial&stage=items'])('continues the exact saved run into live item analysis despite query %s', async query => {
    const runId = '12345678-abcd-1234-abcd-123456789abc'
    window.history.replaceState(null, '', `/run/${runId}${query}`)
    globalThis.fetch = vi.fn(async (url: unknown) => new Response(JSON.stringify(
      String(url) === '/api/gallery' ? { benchmarks: [] } : {
        run_id: runId, slug: 'saved-deployment', scoring: { input_content: { score: 3 } }, raw: '{}',
        elicitation_summary: '| IC | HIGH | Critical to deployment |',
      },
    ), { status: 200 })) as unknown as typeof fetch

    render(<App />)
    expect(await screen.findByTestId('item-assessment-reference')).toHaveTextContent(`run:${runId}`)
    expect(screen.queryByRole('region', { name: 'Free demo item analysis' })).not.toBeInTheDocument()
    expect(screen.getByText('High priority')).toBeInTheDocument()
    expect(screen.getByText('Benchmark assessment ready · item analysis available')).toBeInTheDocument()
    expect(screen.queryByText('Full dataset classified')).not.toBeInTheDocument()
  })

  it('restores a missing benchmark report from its authenticated item run without new model calls', async () => {
    const runId = '12345678-abcd-1234-abcd-123456789abc'
    window.history.replaceState(null, '', `/run/${runId}`)
    sessionStorage.setItem(`item_analysis_run_v1:run:${runId}`, JSON.stringify({ run_id: 'item-run-live', run_secret: 'secret-token' }))
    const fetchSpy = vi.fn(async (url: unknown) => {
      if (String(url) === '/api/gallery') return new Response(JSON.stringify({ benchmarks: [] }), { status: 200 })
      if (String(url).endsWith('/report')) return new Response('Report expired', { status: 404 })
      return new Response(JSON.stringify({ run_id: 'item-run-live', assessment: {
        kind: 'run', id: runId, benchmark: 'Saved benchmark', deployment: 'Original deployment context',
        scoring: { input_content: { score: 4, reasoning: 'Saved original reasoning' } },
        elicitation_summary: '| IC | HIGH | Critical to deployment |',
      } }), { status: 200 })
    })
    globalThis.fetch = fetchSpy as unknown as typeof fetch
    render(<App />)

    expect(await screen.findByTestId('item-assessment-reference')).toHaveTextContent(`run:${runId}`)
    expect(screen.getByText(/restored the benchmark assessment saved with your item analysis/i)).toBeInTheDocument()
    expect(screen.getByText('Original deployment context')).toBeInTheDocument()
    expect(screen.getByText('High priority')).toBeInTheDocument()
    expect(screen.getByText('4 / 5')).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /download benchmark report pdf/i })).not.toBeInTheDocument()
    expect(fetchSpy).toHaveBeenCalledWith('/api/item-analysis/runs/item-run-live?page=1', expect.objectContaining({ headers: { 'X-Review-Token': 'secret-token' } }))
    expect(fetchSpy.mock.calls).toHaveLength(3) // Gallery, original report, authenticated recovery; no mutation.
  })

  it.each(['different-parent', 'different-kind', 'different-item-run', 'expired-token', 'missing-token'])('does not recover a report with %s', async (scenario) => {
    const runId = '12345678-abcd-1234-abcd-123456789abc'
    window.history.replaceState(null, '', `/run/${runId}`)
    if (scenario !== 'missing-token') sessionStorage.setItem(`item_analysis_run_v1:run:${runId}`, JSON.stringify({ run_id: 'item-run-live', run_secret: 'secret-token' }))
    const fetchSpy = vi.fn(async (url: unknown) => {
      if (String(url) === '/api/gallery') return new Response(JSON.stringify({ benchmarks: [] }), { status: 200 })
      if (String(url).endsWith('/report')) return new Response('Report expired', { status: 404 })
      if (scenario === 'expired-token') return new Response(JSON.stringify({ detail: 'Expired' }), { status: 410 })
      return new Response(JSON.stringify({ run_id: scenario === 'different-item-run' ? 'wrong-item-run' : 'item-run-live', assessment: {
        kind: scenario === 'different-kind' ? 'gallery' : 'run', id: scenario === 'different-parent' ? 'different-parent' : runId,
        benchmark: 'Wrong assessment', deployment: 'Wrong deployment', scoring: { input_content: { score: 5 } },
      } }), { status: 200 })
    })
    globalThis.fetch = fetchSpy as unknown as typeof fetch
    render(<App />)

    expect(await screen.findByRole('heading', { name: 'Report unavailable' })).toBeInTheDocument()
    expect(screen.getByText('This run has already been deleted, or never finished scoring.')).toBeInTheDocument()
    expect(screen.queryByTestId('item-assessment-reference')).not.toBeInTheDocument()
    expect(screen.queryByText('Wrong deployment')).not.toBeInTheDocument()
    expect(fetchSpy.mock.calls).toHaveLength(scenario === 'missing-token' ? 2 : 3)
  })

  it('continues curated assessments by their own IDs and clears completion when switching', async () => {
    const user = userEvent.setup()
    const benchmarks = ['first', 'second'].map((id) => ({
      id: `expert__${id}`, benchmark_name: `${id} benchmark`, slug: `${id}_context`, deployment_description: `${id} deployment`,
    }))
    globalThis.fetch = vi.fn(async (url: unknown) => {
      const current = benchmarks.find((entry) => String(url).endsWith(`/${entry.id}`))
      return new Response(JSON.stringify(String(url) === '/api/gallery' ? { benchmarks } : {
        ...current, scoring: { input_content: { score: 3 } }, raw: '{}',
      }), { status: 200 })
    }) as unknown as typeof fetch

    render(<App />)
    await user.click(await screen.findByRole('button', { name: /first benchmark first deployment/i }))
    expect(await screen.findByTestId('item-assessment-reference')).toHaveTextContent('gallery:expert__first')
    await user.click(screen.getByRole('button', { name: 'Finish all items' }))
    expect(screen.getByText('Full dataset classified')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /second benchmark second deployment/i }))
    await waitFor(() => expect(screen.getByTestId('item-assessment-reference')).toHaveTextContent('gallery:expert__second'))
    expect(window.location.pathname).toBe('/caliper')
    expect(new URLSearchParams(window.location.search).get('assessment')).toBe('expert__second')
    expect(screen.queryByText('Full dataset classified')).not.toBeInTheDocument()
    expect(screen.getByText('Benchmark assessment ready · item analysis available')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /start another benchmark analysis/i }))
    expect(window.location.search).toBe('')
    expect(window.location.pathname).toBe('/caliper')
  })

  it.each(['', '#item-analysis-stage'])('restores the selected gallery assessment and item entry anchor %s', async anchor => {
    window.history.replaceState(null, '', `/caliper?assessment=expert__restored${anchor}`)
    globalThis.fetch = vi.fn(async (url: unknown) => new Response(JSON.stringify(
      String(url) === '/api/gallery' ? { benchmarks: [] } : {
        id: 'expert__restored', benchmark_name: 'Restored benchmark', slug: 'restored_context',
        scoring: { input_content: { score: 3 } }, raw: '{}',
      },
    ), { status: 200 })) as unknown as typeof fetch
    render(<App />)
    expect(await screen.findByTestId('item-assessment-reference')).toHaveTextContent('gallery:expert__restored')
    expect(screen.getByText('Benchmark assessment ready · item analysis available')).toBeInTheDocument()
    expect(globalThis.fetch).toHaveBeenCalledWith('/api/gallery/expert__restored')
    expect(window.location.hash).toBe(anchor)
  })

  it('explains the merged workflow to visitors using the legacy item-analysis link', () => {
    render(<App legacyItemAnalysis />)
    expect(screen.getByText(/item analysis is now part of benchmark validity analysis/i)).toBeInTheDocument()
    expect(screen.getByRole('navigation', { name: 'Benchmark analysis progress' })).toBeInTheDocument()
    expect(screen.queryByTestId('item-assessment-reference')).not.toBeInTheDocument()
  })

  it('"change key" clears storage and returns to the key form', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByPlaceholderText('sk-ant-...'), 'sk-ant-A')
    await user.click(screen.getByRole('button', { name: /save key/i }))
    await user.click(screen.getByRole('button', { name: /change key/i }))

    expect(sessionStorage.getItem('anthropic_api_key')).toBeNull()
    expect(localStorage.getItem('anthropic_api_key')).toBeNull()
    expect(
      screen.getByRole('heading', { name: /enter your anthropic api key/i }),
    ).toBeInTheDocument()
  })
})
