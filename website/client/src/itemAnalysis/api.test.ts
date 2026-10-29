import { afterEach, expect, it, vi } from 'vitest'
import { AnalysisApiError, classify, createAssessmentRun, createDirectRun, createRun, discardRun, download, downloadPackage, getAssessment, getDirectSetup, getRun, searchSources } from './api'

afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers() })

const directContext = { benchmark: 'MathDial', deployment: 'India tutoring', task_requirements: 'Arithmetic', answer_requirements: 'Hints' }

it('discovers direct-context sources with no credentials or assessment request', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  await getDirectSetup(directContext, 'test split')
  expect(fetch).toHaveBeenCalledExactlyOnceWith('/api/item-analysis/direct/setup', expect.objectContaining({
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...directContext, q: 'test split' }),
  }))
})

it('binds a direct context to its confirmed dataset while keeping the paid key in the header', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  await createDirectRun(directContext, { benchmark_confirmed: true, source_id: 'databank:sha:mathdial', source_revision: 'sha' }, 'sk-private')
  const [url, request] = fetch.mock.calls[0]
  expect(url).toBe('/api/item-analysis/runs/from-context')
  expect(request.headers).toEqual({ 'X-OpenAI-Key': 'sk-private' })
  expect(JSON.parse(request.body.get('context_json'))).toEqual(directContext)
  expect(request.body.get('benchmark_confirmed')).toBe('true')
  expect(request.body.get('source_revision')).toBe('sha')
  expect(Array.from(request.body.keys())).not.toContain('assessment_id')
  expect(Array.from(request.body.values()).join(' ')).not.toContain('sk-private')
})

it('sends explicit pilot review acknowledgment for direct full classification', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  await classify({ run_id: 'direct-run', run_secret: 'private' }, 'all', 'sk-private', true)
  expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({ scope: 'all', pilot_review_confirmed: true })
})

it('loads the linked assessment without model calls or credentials', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  await getAssessment({ kind: 'gallery', id: 'expert__mmlu' })
  expect(fetch).toHaveBeenCalledWith('/api/item-analysis/assessment?kind=gallery&id=expert__mmlu', expect.objectContaining({ cache: 'no-store' }))
})

it('uploads items with the original assessment reference and keeps the key out of the body', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  const file = new File(['item_id,content\n1,Question'], 'items.csv', { type: 'text/csv' })
  await createAssessmentRun({ kind: 'run', id: 'original-run' }, { items_file: file, benchmark_confirmed: true }, 'sk-private')
  const [url, request] = fetch.mock.calls[0]
  expect(url).toBe('/api/item-analysis/runs/from-assessment')
  expect(request.headers).toEqual({ 'X-OpenAI-Key': 'sk-private' })
  expect(Array.from(request.body.keys())).toEqual(['assessment_kind', 'assessment_id', 'benchmark_confirmed', 'items_file'])
  expect(request.body.get('benchmark_confirmed')).toBe('true')
  expect(request.body.get('assessment_id')).toBe('original-run')
  expect(await request.body.get('items_file').text()).toContain('Question')
})

it('searches Data Bank metadata for the same assessment without a key or model call', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  await searchSources({ kind: 'run', id: 'original-run' }, 'MMLU / test')
  expect(fetch).toHaveBeenCalledWith('/api/item-analysis/sources?kind=run&id=original-run&q=MMLU+%2F+test', expect.objectContaining({ cache: 'no-store' }))
  expect(fetch.mock.calls[0][1].headers).toBeUndefined()
  expect(fetch.mock.calls[0][1].method).toBeUndefined()
})

it('binds explicit benchmark confirmation to the selected Data Bank snapshot', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  await createAssessmentRun({ kind: 'run', id: 'original-run' }, { source_id: 'databank:revision:mmlu', source_revision: 'revision', benchmark_confirmed: true }, 'sk-private')
  const [, request] = fetch.mock.calls[0]
  expect(request.body.get('source_id')).toBe('databank:revision:mmlu')
  expect(request.body.get('source_revision')).toBe('revision')
  expect(request.body.get('benchmark_confirmed')).toBe('true')
  expect(Array.from(request.body.values()).join(' ')).not.toContain('sk-private')
})

it.each(['mmlu', 'gsm8k', 'toxigen', 'toxigen-south-asia'])('sends the selected %s context in the body and keeps the API key in a header', async exampleId => {
  const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'test', run_secret: 'private' })))
  vi.stubGlobal('fetch', fetch)
  await createRun(exampleId, 'generate', 'sk-secret')
  expect(fetch).toHaveBeenCalledWith('/api/item-analysis/runs', expect.objectContaining({
    method: 'POST', headers: { 'Content-Type': 'application/json', 'X-OpenAI-Key': 'sk-secret' },
    body: JSON.stringify({ example_id: exampleId, specification_mode: 'generate' }),
  }))
})

it('omits an API-key header for a supplied specification', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  await createRun('illustrative', 'provided', '')
  expect(fetch.mock.calls[0][1].headers).not.toHaveProperty('X-OpenAI-Key')
})

it('classifies with the OpenAI key and run secret in headers', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  await classify({ run_id: 'test', run_secret: 'private-run' }, 'pilot', 'sk-private')
  expect(fetch).toHaveBeenCalledWith('/api/item-analysis/runs/test/classify', expect.objectContaining({
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Review-Token': 'private-run', 'X-OpenAI-Key': 'sk-private' },
    body: JSON.stringify({ scope: 'pilot' }),
  }))
})

it('downloads artifacts with the run secret in a header, never a URL', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response('item_id,label\n1,2'))
  vi.stubGlobal('fetch', fetch)
  const blob = await download({ run_id: 'test', run_secret: 'private-secret' }, 'items')
  expect(await blob.text()).toContain('item_id,label')
  expect(fetch).toHaveBeenCalledWith('/api/item-analysis/runs/test/download/items', expect.objectContaining({ headers: { 'X-Review-Token': 'private-secret' } }))
})

it('preserves HTTP status so an expired run can stop polling', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: 'This run expired.' }), { status: 404 })))
  await expect(getRun({ run_id: 'expired', run_secret: 'token' }, 1)).rejects.toEqual(new AnalysisApiError('This run expired.', 404))
})

it('downloads the package with its descriptive server filename and only the private access header', async () => {
  const fetch = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' })))
    .mockResolvedValueOnce(new Response('ZIP fixture', { headers: {
      'Content-Disposition': "attachment; filename*=UTF-8''MathDial%20pilot%20results.zip",
    } }))
  vi.stubGlobal('fetch', fetch)
  const result = await downloadPackage({ run_id: 'test', run_secret: 'private-secret' })
  expect(result.filename).toBe('MathDial pilot results.zip')
  expect(await result.blob.text()).toBe('ZIP fixture')
  expect(fetch).toHaveBeenNthCalledWith(1, '/api/item-analysis/runs/test/package', expect.objectContaining({ method: 'POST', headers: { 'X-Review-Token': 'private-secret' } }))
  expect(fetch).toHaveBeenNthCalledWith(2, '/api/item-analysis/runs/test/package?prepared=true', expect.objectContaining({ headers: { 'X-Review-Token': 'private-secret' } }))
})

it('waits for background preparation with short authenticated status requests before downloading', async () => {
  vi.useFakeTimers()
  const fetch = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' })))
    .mockResolvedValueOnce(new Response('ZIP fixture'))
  vi.stubGlobal('fetch', fetch)
  const progress = vi.fn()
  const pending = downloadPackage({ run_id: 'test', run_secret: 'private-secret' }, progress)
  await vi.advanceTimersByTimeAsync(999)
  expect(fetch).toHaveBeenCalledTimes(1)
  expect(progress).toHaveBeenCalledExactlyOnceWith('preparing')
  await vi.advanceTimersByTimeAsync(1001)
  expect((await pending).filename).toBe('caliper-results.zip')
  expect(fetch.mock.calls.map(([url]) => url)).toEqual([
    '/api/item-analysis/runs/test/package', '/api/item-analysis/runs/test/package/status',
    '/api/item-analysis/runs/test/package/status', '/api/item-analysis/runs/test/package?prepared=true',
  ])
  for (const [url, request] of fetch.mock.calls) {
    expect(url).not.toContain('private-secret')
    expect(request.headers).toEqual({ 'X-Review-Token': 'private-secret' })
  }
  expect(progress.mock.calls).toEqual([['preparing'], ['downloading']])
})

it('reports a background preparation failure without requesting an incomplete file', async () => {
  vi.useFakeTimers()
  const fetch = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'failed', message: 'Storage is full. Your results remain saved.', error_status: 507 })))
  vi.stubGlobal('fetch', fetch)
  const pending = expect(downloadPackage({ run_id: 'test', run_secret: 'private-secret' })).rejects.toEqual(new AnalysisApiError('Storage is full. Your results remain saved.', 507))
  await vi.advanceTimersByTimeAsync(1000)
  await pending
  expect(fetch).toHaveBeenCalledTimes(2)
})

it('can retry the same cached package after a failed transfer and sanitizes the filename', async () => {
  const failedTransfer = new Response('ZIP fixture')
  vi.spyOn(failedTransfer, 'blob').mockRejectedValue(new TypeError('Failed to fetch'))
  const fetch = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' })))
    .mockResolvedValueOnce(failedTransfer)
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' })))
    .mockResolvedValueOnce(new Response('ZIP fixture', { headers: { 'Content-Disposition': "attachment; filename*=UTF-8''..%2Fresults%00.zip" } }))
  vi.stubGlobal('fetch', fetch)
  const run = { run_id: 'test', run_secret: 'private-secret' }
  await expect(downloadPackage(run)).rejects.toThrow('Failed to fetch')
  const result = await downloadPackage(run)
  expect(result.filename).toBe('results.zip')
  expect(await result.blob.text()).toBe('ZIP fixture')
  expect(fetch.mock.calls.map(([url]) => url)).toEqual([
    '/api/item-analysis/runs/test/package', '/api/item-analysis/runs/test/package?prepared=true',
    '/api/item-analysis/runs/test/package', '/api/item-analysis/runs/test/package?prepared=true',
  ])
})

it('stops waiting when the page leaves without cancelling the saved server job', async () => {
  vi.useFakeTimers()
  const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
  vi.stubGlobal('fetch', fetch)
  const controller = new AbortController()
  const pending = expect(downloadPackage({ run_id: 'test', run_secret: 'private-secret' }, undefined, controller.signal)).rejects.toMatchObject({ name: 'AbortError' })
  await vi.advanceTimersByTimeAsync(0)
  controller.abort()
  await pending
  await vi.advanceTimersByTimeAsync(2000)
  expect(fetch).toHaveBeenCalledTimes(1)
  expect(vi.getTimerCount()).toBe(0)
})

it('limits preparation waiting and explains that retrying preserves saved results', async () => {
  vi.useFakeTimers()
  const fetch = vi.fn().mockImplementation(async () => new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
  vi.stubGlobal('fetch', fetch)
  const pending = expect(downloadPackage({ run_id: 'test', run_secret: 'private-secret' })).rejects.toThrow('Please try downloading again; your saved results are unchanged.')
  await vi.advanceTimersByTimeAsync(15 * 60 * 1000)
  await pending
  expect(fetch.mock.calls.some(([url]) => url.includes('prepared=true'))).toBe(false)
  expect(vi.getTimerCount()).toBe(0)
})

it('discards a saved run using authenticated DELETE and handles an empty response', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response(null, { status: 204 }))
  vi.stubGlobal('fetch', fetch)
  await discardRun({ run_id: 'test', run_secret: 'private-secret' })
  expect(fetch).toHaveBeenCalledExactlyOnceWith('/api/item-analysis/runs/test', expect.objectContaining({ method: 'DELETE', headers: { 'X-Review-Token': 'private-secret' } }))
})

it('prepares direct and assessment context without sending any provider key', async () => {
  const fetch = vi.fn().mockImplementation(async () => new Response('{}'))
  vi.stubGlobal('fetch', fetch)
  const dataset = { benchmark_confirmed: true as const, source_id: 'source', source_revision: 'revision' }
  await createDirectRun(directContext, dataset)
  await createAssessmentRun({ kind: 'run', id: 'assessment' }, dataset)
  for (const [, request] of fetch.mock.calls) expect(request.headers).not.toHaveProperty('X-OpenAI-Key')
})
