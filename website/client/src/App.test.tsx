/**
 * App-level integration tests for the multipart + SSE flow.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { App } from './App'

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
  })

  afterEach(() => {
    globalThis.fetch = originalFetch
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

  it('summary view delete button calls API and shows deleted phase', async () => {
    const user = userEvent.setup()
    const fakeKey = 'sk-ant-test'

    const calls: Array<{ url: string; method: string }> = []
    globalThis.fetch = vi.fn(async (url: unknown, init: unknown) => {
      const u = String(url)
      const i = (init as RequestInit) ?? {}
      calls.push({ url: u, method: i.method ?? 'GET' })
      if (u.endsWith('/answers')) return makeStreamingResponse(SUMMARY_STREAM)
      if (u.startsWith('/api/runs/run-x') && i.method === 'DELETE') {
        return new Response(null, { status: 204 })
      }
      return makeStreamingResponse(HAPPY_STREAM)
    }) as unknown as typeof fetch

    // Stub confirm() to auto-accept.
    const originalConfirm = window.confirm
    window.confirm = () => true

    try {
      render(<App />)
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

      await user.click(
        screen.getByRole('button', { name: /delete from server/i }),
      )

      await waitFor(() =>
        expect(
          screen.getByRole('heading', { name: /run deleted/i }),
        ).toBeInTheDocument(),
      )
      expect(
        calls.some(
          (c) => c.method === 'DELETE' && c.url === '/api/runs/run-x',
        ),
      ).toBe(true)
    } finally {
      window.confirm = originalConfirm
    }
  })

  it('summary view delete is gated on user confirmation', async () => {
    const user = userEvent.setup()
    const fakeKey = 'sk-ant-test'

    const calls: Array<{ url: string; method: string }> = []
    globalThis.fetch = vi.fn(async (url: unknown, init: unknown) => {
      const u = String(url)
      const i = (init as RequestInit) ?? {}
      calls.push({ url: u, method: i.method ?? 'GET' })
      if (u.endsWith('/answers')) return makeStreamingResponse(SUMMARY_STREAM)
      return makeStreamingResponse(HAPPY_STREAM)
    }) as unknown as typeof fetch

    const originalConfirm = window.confirm
    window.confirm = () => false // user cancels

    try {
      render(<App />)
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

      await user.click(
        screen.getByRole('button', { name: /delete from server/i }),
      )

      // Still on summary page; no DELETE call was issued.
      expect(
        screen.getByRole('heading', { name: /elicitation summary/i }),
      ).toBeInTheDocument()
      expect(calls.some((c) => c.method === 'DELETE')).toBe(false)
    } finally {
      window.confirm = originalConfirm
    }
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
    await user.type(screen.getByLabelText(/email address/i), 'test@example.org')
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
    expect(screen.getByText('2')).toBeInTheDocument()
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
    await user.type(screen.getByLabelText(/email address/i), 'test@example.org')
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
      if (u.endsWith('/score')) return makeStreamingResponse(SCORE_STREAM)
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
    await user.type(screen.getByLabelText(/email address/i), 'test@example.org')
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

    // Score validity →
    await user.click(
      screen.getByRole('button', { name: /score validity/i }),
    )

    await waitFor(() =>
      expect(
        screen.getByRole('heading', { name: /validity scoring/i }),
      ).toBeInTheDocument(),
    )

    // Per-dimension scores are visible.
    expect(screen.getByText(/Input Ontology/i)).toBeInTheDocument()
    expect(screen.getByText('3 / 5')).toBeInTheDocument()
    expect(screen.getByText('4 / 5')).toBeInTheDocument()

    // The /score call carried the BYOK key.
    const scoreCall = calls.find((c) => c.url.endsWith('/score'))
    expect(scoreCall).toBeDefined()
    expect(scoreCall?.method).toBe('POST')
    expect(scoreCall?.headers['X-Anthropic-Key']).toBe(fakeKey)
    expect(scoreCall?.url).not.toContain('sk-ant-')
    expect(scoreCall?.body as string).not.toContain('sk-ant-')
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
