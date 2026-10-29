import { afterEach, expect, it, vi } from 'vitest'
import { startReview, startGrounding, startBenchmarkRetrieval, startScreening, startSelection, startAdaptive, getCandidates, getReview, getReviewPackage, ReviewRequestError } from './api'

afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers() })

it.each([502, 503, 504])('identifies a proxy %s response without blaming the supplied answers', async status => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('<html>Bad gateway</html>', { status })))
  const request = getReview({ run_id: 'running', run_secret: 'private' })
  await expect(request).rejects.toBeInstanceOf(ReviewRequestError)
  await expect(request).rejects.toMatchObject({ status, message: `The server could not respond (${status}). Please try again shortly.`, hasServerDetail: false })
})

it('retains a specific server error and does not automatically repeat a paid action', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: 'The mapping provider is unavailable.' }), { status: 503 }))
  vi.stubGlobal('fetch', fetchMock)
  await expect(startGrounding({ run_id: 'extracted', run_secret: 'private' }, 'sk-secret')).rejects.toMatchObject({
    status: 503, message: 'The mapping provider is unavailable.', hasServerDetail: true,
  })
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it('keeps input validation errors distinct from server failures', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('', { status: 400 })))
  await expect(getReview({ run_id: 'invalid', run_secret: 'private' })).rejects.toMatchObject({
    status: 400, message: 'Request failed (400). Check your entries and try again.',
  })
})

it('sends only the OpenAI key in headers and polls with a separate run secret', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'a', run_secret: 'access' })))
  vi.stubGlobal('fetch', fetchMock)
  const input = { deployment: { task: 'Tutor', users: 'Students', inputs: 'Text', outputs: 'Text', success: 'Correct', constraints: '' }, retrieve_k: 20, retrieval_query: 'What is 2 + 2?' }
  await startReview(input, 'sk-secret')
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe('/api/item-review/runs')
  expect(options.headers).toEqual({ 'Content-Type': 'application/json', 'X-OpenAI-Key': 'sk-secret' })
  expect(options.body).not.toContain('secret')
  expect(JSON.parse(options.body)).toEqual(input)
  fetchMock.mockResolvedValue(new Response(JSON.stringify({ status: 'running' })))
  await getReview({ run_id: 'a', run_secret: 'access' })
  expect(fetchMock.mock.calls[1][1].headers).toEqual({ 'X-Review-Token': 'access' })
})

it('sends extraction mode with only the original answers in the request body', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'a', run_secret: 'access' })))
  vi.stubGlobal('fetch', fetchMock)
  const deployment = { task: '  Tutor\n', users: 'Students', inputs: 'Text', outputs: 'Text', success: 'Correct', constraints: '' }
  await startReview({ deployment, mode: 'requirements' }, 'sk-secret')
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe('/api/item-review/runs')
  expect(options.headers).toEqual({ 'Content-Type': 'application/json', 'X-OpenAI-Key': 'sk-secret' })
  expect(JSON.parse(options.body)).toEqual({ deployment, mode: 'requirements' })
  expect(options.body).not.toContain('sk-secret')
})

it('starts grounding with the source run token and fresh API key without resending requirements', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'ground', run_secret: 'new-access' })))
  vi.stubGlobal('fetch', fetchMock)
  expect(await startGrounding({ run_id: 'extracted', run_secret: 'access' }, 'sk-secret')).toEqual({ run_id: 'ground', run_secret: 'new-access' })
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe('/api/item-review/runs/extracted/ground')
  expect(options.method).toBe('POST')
  expect(options.headers).toEqual({ 'X-Review-Token': 'access', 'X-OpenAI-Key': 'sk-secret' })
  expect(options.body).toBeUndefined()
})

it('starts whole-bank retrieval with an empty body and only the source run token', async () => {
  const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(new Response(JSON.stringify({ run_id: 'retrieve', run_secret: 'new-access' }))))
  vi.stubGlobal('fetch', fetchMock)
  const run = { run_id: 'grounded', run_secret: 'access' }
  await startBenchmarkRetrieval(run)
  expect(fetchMock.mock.calls[0]).toEqual(['/api/item-review/runs/grounded/retrieve', {
    cache: 'no-store', method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Review-Token': 'access' }, body: '{}',
  }])
})

it('requests a candidate page using the opaque queue ID and private run token', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ items: [] })))
  vi.stubGlobal('fetch', fetchMock)
  await getCandidates({ run_id: 'retrieve', run_secret: 'access' }, 'task/all + other', 2)
  const [url, options] = fetchMock.mock.calls[0]
  const parsed = new URL(url, 'https://example.test')
  expect(parsed.searchParams.get('queue_id')).toBe('task/all + other')
  expect(parsed.searchParams.get('page')).toBe('2')
  expect(options.headers).toEqual({ 'X-Review-Token': 'access' })
  expect(options.cache).toBe('no-store')
})

it('starts screening with the private source token and fresh API key, without resending evidence', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'screen', run_secret: 'screen-access' })))
  vi.stubGlobal('fetch', fetchMock)
  await startScreening({ run_id: 'retrieve', run_secret: 'source-access' }, 'sk-private')
  expect(fetchMock.mock.calls[0]).toEqual(['/api/item-review/runs/retrieve/screen', {
    cache: 'no-store', method: 'POST', headers: { 'X-Review-Token': 'source-access', 'X-OpenAI-Key': 'sk-private' },
  }])
})

it('starts collection selection with only the source token and an empty JSON body', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'select', run_secret: 'select-access' })))
  vi.stubGlobal('fetch', fetchMock)
  await startSelection({ run_id: 'screen', run_secret: 'screen-access' })
  expect(fetchMock.mock.calls[0]).toEqual(['/api/item-review/runs/screen/select', {
    cache: 'no-store', method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Review-Token': 'screen-access' }, body: '{}',
  }])
})


it('starts adaptive screening with an explicit budget and private credentials only in headers', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'adapt', run_secret: 'adapt-access' })))
  vi.stubGlobal('fetch', fetchMock)
  const body = { seed: 2, max_cost_usd: 5, input_price_per_million: 1, cached_input_price_per_million: 0, output_price_per_million: 3 }
  await startAdaptive({ run_id: 'select', run_secret: 'select-access' }, 'sk-private', body)
  expect(fetchMock.mock.calls[0]).toEqual(['/api/item-review/runs/select/adapt', {
    cache: 'no-store', method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Review-Token': 'select-access', 'X-OpenAI-Key': 'sk-private' }, body: JSON.stringify(body),
  }])
})

it('resumes adaptive screening with an empty body to preserve its original settings', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'adapt-resume', run_secret: 'resume-access' })))
  vi.stubGlobal('fetch', fetchMock)
  await startAdaptive({ run_id: 'adapt', run_secret: 'adapt-access' }, 'sk-fresh', {})
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe('/api/item-review/runs/adapt/adapt')
  expect(options.body).toBe('{}')
  expect(options.headers['X-OpenAI-Key']).toBe('sk-fresh')
  expect(options.headers['X-Review-Token']).toBe('adapt-access')
})

it('prepares and downloads a package with the private run token and the server filename', async () => {
  const fetchMock = vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' }))).mockResolvedValueOnce(new Response('zip-content', {
    headers: { 'Content-Type': 'application/zip', 'Content-Disposition': 'attachment; filename="medical-goal-adaptive-20261025.zip"' },
  }))
  vi.stubGlobal('fetch', fetchMock)
  const result = await getReviewPackage({ run_id: 'adapt', run_secret: 'private-access' })
  expect(fetchMock.mock.calls[0]).toEqual(['/api/item-review/runs/adapt/package', {
    cache: 'no-store', method: 'POST', headers: { 'X-Review-Token': 'private-access' }, signal: expect.any(AbortSignal),
  }])
  expect(fetchMock.mock.calls[1]).toEqual(['/api/item-review/runs/adapt/package?prepared=true', {
    cache: 'no-store', headers: { 'X-Review-Token': 'private-access' }, signal: expect.any(AbortSignal),
  }])
  expect(result.filename).toBe('medical-goal-adaptive-20261025.zip')
  expect(await result.blob.text()).toBe('zip-content')
})

it.each([
  ["attachment; filename*=UTF-8''%C3%A9tude.zip", 'étude.zip'],
  ['attachment; filename="../report.zip"', 'benchmark-results-run.zip'],
  ['attachment; filename="report.html"', 'benchmark-results-run.zip'],
  ["attachment; filename*=UTF-8''%broken; filename=plain.zip", 'plain.zip'],
  ['', 'benchmark-results-run.zip'],
])('handles a package filename header %s', async (header, expected) => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' })))
    .mockResolvedValueOnce(new Response('zip', { headers: { 'Content-Disposition': header } })))
  const result = await getReviewPackage({ run_id: 'run', run_secret: 'private' })
  expect(result.filename).toBe(expected)
})

it('reports unavailable review access before treating its error body as a download', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: 'Review not found or access token is invalid. Reopen the review in the browser where it was started.' }), { status: 404 })))
  await expect(getReviewPackage({ run_id: 'missing', run_secret: 'private' })).rejects.toThrow('Review not found or access token is invalid')
})

it('polls preparation before transfer and sends credentials only in headers', async () => {
  vi.useFakeTimers()
  const fetchMock = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'preparing' })))
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' })))
    .mockResolvedValueOnce(new Response('prepared zip'))
  vi.stubGlobal('fetch', fetchMock)
  const controller = new AbortController()
  const progress = vi.fn()
  const result = getReviewPackage({ run_id: 'run/id', run_secret: 'private-access' }, progress, controller.signal)
  await vi.advanceTimersByTimeAsync(1000)
  expect(fetchMock).toHaveBeenCalledTimes(2)
  expect(progress.mock.calls).toEqual([['preparing']])
  await vi.advanceTimersByTimeAsync(1000)
  expect(await (await result).blob.text()).toBe('prepared zip')
  expect(progress.mock.calls).toEqual([['preparing'], ['downloading']])
  expect(fetchMock.mock.calls.map(([url]) => url)).toEqual([
    '/api/item-review/runs/run%2Fid/package', '/api/item-review/runs/run%2Fid/package/status',
    '/api/item-review/runs/run%2Fid/package/status', '/api/item-review/runs/run%2Fid/package?prepared=true',
  ])
  for (const [, options] of fetchMock.mock.calls) {
    expect(options.headers).toEqual({ 'X-Review-Token': 'private-access' })
    expect(options.signal).toBe(controller.signal)
  }
})

it('stops waiting and polling when its browser request is aborted', async () => {
  vi.useFakeTimers()
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
  vi.stubGlobal('fetch', fetchMock)
  const controller = new AbortController()
  const result = getReviewPackage({ run_id: 'run', run_secret: 'private' }, undefined, controller.signal)
  const rejection = expect(result).rejects.toMatchObject({ name: 'AbortError' })
  await vi.advanceTimersByTimeAsync(0)
  controller.abort()
  await rejection
  await vi.advanceTimersByTimeAsync(10000)
  expect(fetchMock).toHaveBeenCalledTimes(1)
  expect(vi.getTimerCount()).toBe(0)
})

it('does not start preparation for an already aborted request', async () => {
  const fetchMock = vi.fn()
  vi.stubGlobal('fetch', fetchMock)
  const controller = new AbortController()
  controller.abort()
  await expect(getReviewPackage({ run_id: 'run', run_secret: 'private' }, undefined, controller.signal)).rejects.toMatchObject({ name: 'AbortError' })
  expect(fetchMock).not.toHaveBeenCalled()
})

it.each(['failed', 'not_started'])('reports %s preparation without transferring or repeating the request', async status => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ status, message: 'Package preparation was interrupted. Your saved results are unchanged.', error_status: 503 })))
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage({ run_id: 'run', run_secret: 'private' })).rejects.toMatchObject({ status: 503, message: 'Package preparation was interrupted. Your saved results are unchanged.' })
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it.each(['preparing', 'downloading'] as const)('explains a connection failure while %s without retrying requests', async phase => {
  const fetchMock = vi.fn()
  if (phase === 'downloading') fetchMock.mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' })))
  fetchMock.mockRejectedValueOnce(new TypeError('Failed to fetch'))
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage({ run_id: 'run', run_secret: 'private' })).rejects.toThrow(`The connection was interrupted while ${phase} the results package. Your saved results are unchanged. Please try downloading again.`)
  expect(fetchMock).toHaveBeenCalledTimes(phase === 'preparing' ? 1 : 2)
})

it('reports an interrupted ZIP response body as a download failure', async () => {
  const response = new Response('zip')
  vi.spyOn(response, 'blob').mockRejectedValueOnce(new TypeError('NetworkError'))
  const fetchMock = vi.fn().mockResolvedValueOnce(new Response(JSON.stringify({ status: 'ready' }))).mockResolvedValueOnce(response)
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage({ run_id: 'run', run_secret: 'private' })).rejects.toThrow('connection was interrupted while downloading')
  expect(fetchMock).toHaveBeenCalledTimes(2)
})
