/**
 * Tests for the BYOK request shape and the SSE event stream.
 *
 * The API key must travel in the X-Anthropic-Key header and never appear
 * in the URL or request body. The stream must decode SSE events into the
 * typed PipelineEvent shape.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import {
  runPipeline,
  submitAnswers,
  extractPaper,
  generateRegion,
  scoreValidity,
  exportRun,
  deleteRun,
  ApiError,
  type PipelineEvent,
} from './api'

interface CapturedCall {
  url: string
  init: RequestInit
}

function fakePdf(): File {
  const bytes = new Uint8Array([0x25, 0x50, 0x44, 0x46]) // "%PDF"
  return new File([bytes], 'paper.pdf', { type: 'application/pdf' })
}

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

const SAMPLE_BODY =
  'event: step-started\ndata: {"step":"0-slug"}\n\n' +
  'event: step-completed\ndata: {"step":"0-slug","output":{"slug":"test_slug"}}\n\n' +
  'event: step-started\ndata: {"step":"1-metadata"}\n\n' +
  'event: step-completed\ndata: {"step":"1-metadata","output":{"metadata":"..."}}\n\n' +
  'event: step-started\ndata: {"step":"2-questions"}\n\n' +
  'event: step-completed\ndata: {"step":"2-questions","output":{"questions":[{"id":"Q1","dimension":"IC","question":"?"}],"metadata":"...","run_id":"abc","slug":"test_slug"}}\n\n' +
  'event: awaiting-answers\ndata: {"run_id":"abc","slug":"test_slug"}\n\n'

const SUMMARY_BODY =
  'event: step-started\ndata: {"step":"2-summary"}\n\n' +
  'event: step-completed\ndata: {"step":"2-summary","output":{"summary":"## Use Case\\nfoo","run_id":"abc"}}\n\n' +
  'event: run-complete\ndata: {"run_id":"abc"}\n\n'

describe('runPipeline', () => {
  let originalFetch: typeof fetch

  beforeEach(() => {
    originalFetch = globalThis.fetch
  })

  afterEach(() => {
    globalThis.fetch = originalFetch
  })

  function mockFetch(
    response: Response,
  ): { calls: CapturedCall[]; spy: ReturnType<typeof vi.fn> } {
    const calls: CapturedCall[] = []
    const spy = vi.fn(async (url: unknown, init: unknown) => {
      calls.push({ url: String(url), init: init as RequestInit })
      return response
    })
    globalThis.fetch = spy as unknown as typeof fetch
    return { calls, spy }
  }

  it('sends key in X-Anthropic-Key header, not URL or body', async () => {
    const { calls } = mockFetch(makeStreamingResponse(SAMPLE_BODY))
    const fakeKey = 'sk-ant-LEAK_TEST_KEY_xyz'

    const events: PipelineEvent[] = []
    for await (const e of runPipeline({
      apiKey: fakeKey,
      pdfFile: fakePdf(),
      deploymentDescription: 'description',
      optedInFull: true,
    })) {
      events.push(e)
    }

    expect(calls).toHaveLength(1)
    const { url, init } = calls[0]
    expect(url).not.toContain('sk-ant-')
    expect(url).not.toContain('LEAK_TEST')

    const headers = init.headers as Record<string, string>
    expect(headers['X-Anthropic-Key']).toBe(fakeKey)

    // FormData body must not contain the key in any field.
    const body = init.body as FormData
    for (const [, value] of body.entries()) {
      const stringified = typeof value === 'string' ? value : ''
      expect(stringified).not.toContain('sk-ant-')
      expect(stringified).not.toContain('LEAK_TEST')
    }
  })

  it('uses POST and multipart/form-data', async () => {
    const { calls } = mockFetch(makeStreamingResponse(SAMPLE_BODY))
    for await (const _ of runPipeline({
      apiKey: 'sk-ant-test',
      pdfFile: fakePdf(),
      deploymentDescription: 'd',
      optedInFull: false,
    })) {
      // drain
    }
    expect(calls[0].init.method).toBe('POST')
    expect(calls[0].init.body).toBeInstanceOf(FormData)
    const fd = calls[0].init.body as FormData
    expect(fd.get('deployment_description')).toBe('d')
    expect(fd.get('opted_in_full')).toBe('false')
    expect(fd.get('pdf')).toBeInstanceOf(File)
  })

  it('does not include credentials/cookies on the request', async () => {
    const { calls } = mockFetch(makeStreamingResponse(SAMPLE_BODY))
    for await (const _ of runPipeline({
      apiKey: 'sk-ant-test',
      pdfFile: fakePdf(),
      deploymentDescription: 'd',
      optedInFull: false,
    })) {
      // drain
    }
    expect(calls[0].init.credentials).not.toBe('include')
  })

  it('decodes SSE events into typed PipelineEvent values', async () => {
    mockFetch(makeStreamingResponse(SAMPLE_BODY))
    const events: PipelineEvent[] = []
    for await (const e of runPipeline({
      apiKey: 'sk-ant-test',
      pdfFile: fakePdf(),
      deploymentDescription: 'd',
      optedInFull: true,
    })) {
      events.push(e)
    }
    expect(events).toHaveLength(7)
    expect(events[0]).toEqual({ type: 'step-started', step: '0-slug' })
    expect(events[1]).toEqual({
      type: 'step-completed',
      step: '0-slug',
      output: { slug: 'test_slug' },
    })
    const last = events[events.length - 1]
    expect(last).toEqual({
      type: 'awaiting-answers',
      runId: 'abc',
      slug: 'test_slug',
    })
  })

  it('handles SSE chunks split across read boundaries', async () => {
    // Emit each event as its own chunk to simulate slow streaming.
    const encoder = new TextEncoder()
    const chunks = SAMPLE_BODY.split('\n\n')
      .filter((c) => c.trim())
      .map((c) => c + '\n\n')
    const body = new ReadableStream<Uint8Array>({
      start(controller) {
        for (const chunk of chunks) {
          controller.enqueue(encoder.encode(chunk))
        }
        controller.close()
      },
    })
    mockFetch(
      new Response(body, {
        status: 200,
        headers: { 'Content-Type': 'text/event-stream' },
      }),
    )

    const events: PipelineEvent[] = []
    for await (const e of runPipeline({
      apiKey: 'sk-ant-test',
      pdfFile: fakePdf(),
      deploymentDescription: 'd',
      optedInFull: true,
    })) {
      events.push(e)
    }
    expect(events).toHaveLength(7)
  })

  it('throws ApiError on non-2xx response', async () => {
    mockFetch(new Response('upstream call failed', { status: 502 }))
    await expect(
      (async () => {
        for await (const _ of runPipeline({
          apiKey: 'sk-ant-test',
          pdfFile: fakePdf(),
          deploymentDescription: 'd',
          optedInFull: true,
        })) {
          // drain
        }
      })(),
    ).rejects.toBeInstanceOf(ApiError)
  })

  describe('submitAnswers', () => {
    function answerInput(apiKey = 'sk-ant-test') {
      return {
        apiKey,
        runId: 'run-123',
        deploymentDescription: 'desc',
        metadata: 'meta',
        questions: [{ id: 'Q1', dimension: 'IC', question: 'q?' }],
        answers: [{ id: 'Q1', answer: 'a' }],
        optedInFull: true,
      }
    }

    it('POSTs to /api/runs/{runId}/answers as JSON with key in header only', async () => {
      const { calls } = mockFetch(makeStreamingResponse(SUMMARY_BODY))
      const fakeKey = 'sk-ant-LEAK_ANSWERS_KEY'
      for await (const _ of submitAnswers(answerInput(fakeKey))) {
        // drain
      }
      const { url, init } = calls[0]
      expect(url).toBe('/api/runs/run-123/answers')
      expect(init.method).toBe('POST')
      const headers = init.headers as Record<string, string>
      expect(headers['Content-Type']).toBe('application/json')
      expect(headers['X-Anthropic-Key']).toBe(fakeKey)
      expect(url).not.toContain('sk-ant-')
      expect(url).not.toContain('LEAK_ANSWERS_KEY')
      expect(init.body as string).not.toContain('sk-ant-')
      expect(init.body as string).not.toContain('LEAK_ANSWERS_KEY')
    })

    it('encodes the runId in the URL path', async () => {
      const { calls } = mockFetch(makeStreamingResponse(SUMMARY_BODY))
      const input = { ...answerInput(), runId: 'a/b c?' }
      for await (const _ of submitAnswers(input)) {
        // drain
      }
      // encodeURIComponent("a/b c?") => "a%2Fb%20c%3F"
      expect(calls[0].url).toBe('/api/runs/a%2Fb%20c%3F/answers')
    })

    it('decodes step-completed and run-complete events from the stream', async () => {
      mockFetch(makeStreamingResponse(SUMMARY_BODY))
      const events: PipelineEvent[] = []
      for await (const e of submitAnswers(answerInput())) {
        events.push(e)
      }
      expect(events.map((e) => e.type)).toEqual([
        'step-started',
        'step-completed',
        'run-complete',
      ])
      const completed = events[1]
      expect(completed.type).toBe('step-completed')
      if (completed.type === 'step-completed') {
        expect(completed.output?.summary).toContain('Use Case')
      }
    })

    it('throws ApiError on non-2xx response', async () => {
      mockFetch(new Response('conflict', { status: 409 }))
      await expect(
        (async () => {
          for await (const _ of submitAnswers(answerInput())) {
            // drain
          }
        })(),
      ).rejects.toBeInstanceOf(ApiError)
    })
  })

  describe('extractPaper', () => {
    function fakePdfFile(): File {
      return new File([new Uint8Array([0x25, 0x50, 0x44, 0x46])], 'paper.pdf', {
        type: 'application/pdf',
      })
    }

    const STREAM =
      'event: step-started\ndata: {"step":"3a-extract","total":2}\n\n' +
      'event: step-progress\ndata: {"step":"3a-extract","completed":1,"total":2}\n\n' +
      'event: step-progress\ndata: {"step":"3a-extract","completed":2,"total":2}\n\n' +
      'event: step-completed\ndata: {"step":"3a-extract"}\n\n' +
      'event: step-started\ndata: {"step":"3a-consolidate"}\n\n' +
      'event: step-completed\ndata: {"step":"3a-consolidate","output":{"paper_summary":"## Metadata\\n..."}}\n\n' +
      'event: step-started\ndata: {"step":"3b-select"}\n\n' +
      'event: step-completed\ndata: {"step":"3b-select","output":{"selected":["helm.yaml"]}}\n\n' +
      'event: step-started\ndata: {"step":"3b-synthesize"}\n\n' +
      'event: step-completed\ndata: {"step":"3b-synthesize","output":{"benchmark_yaml":"name: synthesized\\n"}}\n\n' +
      'event: extract-complete\ndata: {"run_id":"r1","page_count":2,"selected_examples":["helm.yaml"]}\n\n'

    it('POSTs multipart to /api/runs/{id}/extract with key in header only', async () => {
      const { calls } = mockFetch(makeStreamingResponse(STREAM))
      const fakeKey = 'sk-ant-EXTRACT_LEAK_xyz'
      for await (const _ of extractPaper({
        apiKey: fakeKey,
        runId: 'r1',
        pdfFile: fakePdfFile(),
      })) {
        // drain
      }
      const { url, init } = calls[0]
      expect(url).toBe('/api/runs/r1/extract')
      expect(init.method).toBe('POST')
      expect(
        (init.headers as Record<string, string>)['X-Anthropic-Key'],
      ).toBe(fakeKey)
      expect(url).not.toContain('sk-ant-')
      expect(url).not.toContain('EXTRACT_LEAK')
      expect(init.body).toBeInstanceOf(FormData)
    })

    it('decodes step-progress events with completed/total numbers', async () => {
      mockFetch(makeStreamingResponse(STREAM))
      const events: PipelineEvent[] = []
      for await (const e of extractPaper({
        apiKey: 'sk-ant-test',
        runId: 'r1',
        pdfFile: fakePdfFile(),
      })) {
        events.push(e)
      }
      const progress = events.filter((e) => e.type === 'step-progress')
      expect(progress).toHaveLength(2)
      expect(progress[1]).toEqual({
        type: 'step-progress',
        step: '3a-extract',
        completed: 2,
        total: 2,
      })

      const last = events[events.length - 1]
      expect(last).toEqual({
        type: 'extract-complete',
        runId: 'r1',
        pageCount: 2,
        selectedExamples: ['helm.yaml'],
      })
    })

    it('passes elicitation_summary in the FormData when provided', async () => {
      const { calls } = mockFetch(makeStreamingResponse(STREAM))
      for await (const _ of extractPaper({
        apiKey: 'sk-ant-test',
        runId: 'r1',
        pdfFile: fakePdfFile(),
        elicitationSummary: '## Use Case\nBahasa admin chatbot.',
      })) {
        // drain
      }
      const fd = calls[0].init.body as FormData
      expect(fd.get('elicitation_summary')).toBe(
        '## Use Case\nBahasa admin chatbot.',
      )
    })

    it('omits elicitation_summary when not provided', async () => {
      const { calls } = mockFetch(makeStreamingResponse(STREAM))
      for await (const _ of extractPaper({
        apiKey: 'sk-ant-test',
        runId: 'r1',
        pdfFile: fakePdfFile(),
      })) {
        // drain
      }
      const fd = calls[0].init.body as FormData
      expect(fd.get('elicitation_summary')).toBeNull()
    })

    it('throws ApiError on 409', async () => {
      mockFetch(new Response('wrong status', { status: 409 }))
      await expect(
        (async () => {
          for await (const _ of extractPaper({
            apiKey: 'sk-ant-test',
            runId: 'r1',
            pdfFile: fakePdfFile(),
          })) {
            // drain
          }
        })(),
      ).rejects.toBeInstanceOf(ApiError)
    })
  })

  describe('generateRegion', () => {
    const STREAM =
      'event: step-started\ndata: {"step":"4a-template"}\n\n' +
      'event: step-completed\ndata: {"step":"4a-template","output":{"selected":["southeast_asia.yaml"]}}\n\n' +
      'event: step-started\ndata: {"step":"4b-synthesize"}\n\n' +
      'event: step-completed\ndata: {"step":"4b-synthesize","output":{"region_scaffold":"name: scaffold\\n"}}\n\n' +
      'event: step-started\ndata: {"step":"5-web-search"}\n\n' +
      'event: step-completed\ndata: {"step":"5-web-search","output":{"region_yaml":"name: enriched\\n"}}\n\n' +
      'event: region-complete\ndata: {"run_id":"r1","selected_templates":["southeast_asia.yaml"],"web_search_used":true}\n\n'

    it('POSTs JSON to /api/runs/{id}/region with key in header only', async () => {
      const { calls } = mockFetch(makeStreamingResponse(STREAM))
      const fakeKey = 'sk-ant-REGION_LEAK_xyz'
      for await (const _ of generateRegion({
        apiKey: fakeKey,
        runId: 'r1',
        elicitationSummary: 'summary',
        benchmarkYaml: 'name: t',
      })) {
        // drain
      }
      const { url, init } = calls[0]
      expect(url).toBe('/api/runs/r1/region')
      expect(init.method).toBe('POST')
      const headers = init.headers as Record<string, string>
      expect(headers['Content-Type']).toBe('application/json')
      expect(headers['X-Anthropic-Key']).toBe(fakeKey)
      expect(url).not.toContain('sk-ant-')
      expect(init.body as string).not.toContain('sk-ant-')
      expect(init.body as string).not.toContain('REGION_LEAK')
    })

    it('decodes region-complete event with templates and webSearchUsed', async () => {
      mockFetch(makeStreamingResponse(STREAM))
      const events: PipelineEvent[] = []
      for await (const e of generateRegion({
        apiKey: 'sk-ant-test',
        runId: 'r1',
        elicitationSummary: 'summary',
        benchmarkYaml: 'name: t',
      })) {
        events.push(e)
      }
      const last = events[events.length - 1]
      expect(last).toEqual({
        type: 'region-complete',
        runId: 'r1',
        selectedTemplates: ['southeast_asia.yaml'],
        webSearchUsed: true,
      })
    })

    it('passes skip_web_search through the request body', async () => {
      const { calls } = mockFetch(makeStreamingResponse(STREAM))
      for await (const _ of generateRegion({
        apiKey: 'sk-ant-test',
        runId: 'r1',
        elicitationSummary: 'summary',
        benchmarkYaml: 'name: t',
        skipWebSearch: true,
      })) {
        // drain
      }
      const body = JSON.parse(calls[0].init.body as string) as Record<
        string,
        unknown
      >
      expect(body.skip_web_search).toBe(true)
    })

    it('throws ApiError on 409', async () => {
      mockFetch(new Response('wrong status', { status: 409 }))
      await expect(
        (async () => {
          for await (const _ of generateRegion({
            apiKey: 'sk-ant-test',
            runId: 'r1',
            elicitationSummary: 's',
            benchmarkYaml: 'b',
          })) {
            // drain
          }
        })(),
      ).rejects.toBeInstanceOf(ApiError)
    })
  })

  describe('scoreValidity', () => {
    const STREAM =
      'event: step-started\ndata: {"step":"7-score"}\n\n' +
      'event: step-completed\ndata: {"step":"7-score","output":{"scoring":{"input_ontology":{"score":3}},"raw":"{...}"}}\n\n' +
      'event: run-complete\ndata: {"run_id":"r1"}\n\n'

    function input(apiKey = 'sk-ant-test') {
      return {
        apiKey,
        runId: 'r1',
        paperSummary: 'paper',
        benchmarkYaml: 'bench',
        regionYaml: 'region',
        elicitationSummary: 'elicit',
      }
    }

    it('POSTs JSON to /api/runs/{id}/score with key in header only', async () => {
      const { calls } = mockFetch(makeStreamingResponse(STREAM))
      const fakeKey = 'sk-ant-SCORE_LEAK_xyz'
      for await (const _ of scoreValidity(input(fakeKey))) {
        // drain
      }
      const { url, init } = calls[0]
      expect(url).toBe('/api/runs/r1/score')
      expect(init.method).toBe('POST')
      const headers = init.headers as Record<string, string>
      expect(headers['Content-Type']).toBe('application/json')
      expect(headers['X-Anthropic-Key']).toBe(fakeKey)
      expect(url).not.toContain('sk-ant-')
      expect(init.body as string).not.toContain('sk-ant-')
      expect(init.body as string).not.toContain('SCORE_LEAK')
    })

    it('decodes step-completed with the parsed scoring object', async () => {
      mockFetch(makeStreamingResponse(STREAM))
      const events: PipelineEvent[] = []
      for await (const e of scoreValidity(input())) {
        events.push(e)
      }
      const completed = events[1]
      expect(completed.type).toBe('step-completed')
      if (completed.type === 'step-completed') {
        const out = completed.output as Record<string, unknown>
        expect((out.scoring as Record<string, unknown>).input_ontology).toEqual({
          score: 3,
        })
      }
    })

    it('throws ApiError on 409', async () => {
      mockFetch(new Response('wrong status', { status: 409 }))
      await expect(
        (async () => {
          for await (const _ of scoreValidity(input())) {
            // drain
          }
        })(),
      ).rejects.toBeInstanceOf(ApiError)
    })
  })

  describe('exportRun', () => {
    it('GETs /api/runs/{id}/export and returns parsed JSON', async () => {
      const { calls } = mockFetch(
        new Response(
          JSON.stringify({ run: { run_id: 'r1' }, steps: [], blobs: [] }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        ),
      )
      const data = (await exportRun('r1')) as { run: { run_id: string } }
      expect(data.run.run_id).toBe('r1')
      expect(calls[0].url).toBe('/api/runs/r1/export')
      expect(calls[0].init?.method ?? 'GET').toBe('GET')
    })

    it('throws ApiError on 404', async () => {
      mockFetch(new Response('not found', { status: 404 }))
      await expect(exportRun('missing')).rejects.toBeInstanceOf(ApiError)
    })
  })

  describe('deleteRun', () => {
    it('DELETEs /api/runs/{id}', async () => {
      const { calls } = mockFetch(new Response(null, { status: 204 }))
      await deleteRun('r1')
      expect(calls[0].url).toBe('/api/runs/r1')
      expect(calls[0].init.method).toBe('DELETE')
    })

    it('throws ApiError on 404', async () => {
      mockFetch(new Response('not found', { status: 404 }))
      await expect(deleteRun('missing')).rejects.toBeInstanceOf(ApiError)
    })

    it('encodes the runId in the URL path', async () => {
      const { calls } = mockFetch(new Response(null, { status: 204 }))
      await deleteRun('a/b c?')
      expect(calls[0].url).toBe('/api/runs/a%2Fb%20c%3F')
    })
  })

  it('decodes pipeline error events from a 200 stream', async () => {
    const errBody =
      'event: step-started\ndata: {"step":"0-slug"}\n\n' +
      'event: error\ndata: {"error_class":"RuntimeError","run_id":"abc"}\n\n'
    mockFetch(makeStreamingResponse(errBody))

    const events: PipelineEvent[] = []
    for await (const e of runPipeline({
      apiKey: 'sk-ant-test',
      pdfFile: fakePdf(),
      deploymentDescription: 'd',
      optedInFull: true,
    })) {
      events.push(e)
    }
    expect(events[events.length - 1]).toEqual({
      type: 'error',
      errorClass: 'RuntimeError',
      runId: 'abc',
    })
  })
})
