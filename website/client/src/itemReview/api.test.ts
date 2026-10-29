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

const packageMetadata = { status: 'ready', package_id: 'zip-version-1', bytes: 11, filename: 'medical-goal.zip', chunk_bytes: 1048576 }
const readyPackage = (overrides: Record<string, unknown> = {}) => new Response(JSON.stringify({ ...packageMetadata, ...overrides }))
const packagePiece = (body: string, offset = 0, headers: Record<string, string> = {}) => new Response(body, {
  headers: { 'Content-Type': 'application/octet-stream', 'Content-Length': String(new Blob([body]).size),
    'X-Package-Id': packageMetadata.package_id, 'X-Package-Offset': String(offset), ...headers },
})
const packageAccess = { run_id: 'run', run_secret: 'private-access' }

it('prepares and downloads a package with the private run token and the ready filename', async () => {
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage()).mockResolvedValueOnce(packagePiece('zip-content'))
  vi.stubGlobal('fetch', fetchMock)
  const result = await getReviewPackage(packageAccess)
  expect(fetchMock.mock.calls[0]).toEqual(['/api/item-review/runs/run/package', {
    cache: 'no-store', method: 'POST', headers: { 'X-Review-Token': 'private-access' }, signal: expect.any(AbortSignal),
  }])
  expect(fetchMock.mock.calls[1]).toEqual(['/api/item-review/runs/run/package/chunk?package_id=zip-version-1&offset=0', {
    cache: 'no-store', headers: { 'X-Review-Token': 'private-access' }, signal: expect.any(AbortSignal),
  }])
  expect(result.filename).toBe('medical-goal.zip')
  expect(result.blob.type).toBe('application/zip')
  expect(await result.blob.text()).toBe('zip-content')
})

it('preserves a valid Unicode ZIP filename supplied by the server', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValueOnce(readyPackage({ filename: 'étude.zip' })).mockResolvedValueOnce(packagePiece('zip-content')))
  expect((await getReviewPackage(packageAccess)).filename).toBe('étude.zip')
})

it.each([
  { package_id: undefined }, { package_id: '' }, { bytes: undefined }, { bytes: 0 }, { bytes: -1 }, { bytes: 1.5 },
  { bytes: Number.MAX_SAFE_INTEGER + 1 }, { chunk_bytes: undefined }, { chunk_bytes: 0 }, { chunk_bytes: 2.5 }, { chunk_bytes: 1048577 },
  { filename: undefined }, { filename: '../report.zip' }, { filename: 'report.html' }, { filename: 'bad\n.zip' },
])('rejects incomplete or unsafe prepared package metadata %j without transferring', async overrides => {
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage(overrides))
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage(packageAccess)).rejects.toThrow('incomplete package information')
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it('accepts exact bytes when a proxy omits Content-Length', async () => {
  const response = packagePiece('zip-content')
  response.headers.delete('Content-Length')
  vi.stubGlobal('fetch', vi.fn().mockResolvedValueOnce(readyPackage()).mockResolvedValueOnce(response))
  expect(await (await getReviewPackage(packageAccess)).blob.text()).toBe('zip-content')
})

it('reports unavailable review access before treating its error body as a download', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: 'Review not found or access token is invalid. Reopen the review in the browser where it was started.' }), { status: 404 })))
  await expect(getReviewPackage(packageAccess)).rejects.toThrow('Review not found or access token is invalid')
})

it('polls preparation before transfer and sends credentials only in headers', async () => {
  vi.useFakeTimers()
  const fetchMock = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
    .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'preparing' })))
    .mockResolvedValueOnce(readyPackage())
    .mockResolvedValueOnce(packagePiece('zip-content'))
  vi.stubGlobal('fetch', fetchMock)
  const controller = new AbortController()
  const progress = vi.fn()
  const result = getReviewPackage({ ...packageAccess, run_id: 'run/id' }, progress, controller.signal)
  await vi.advanceTimersByTimeAsync(1000)
  expect(fetchMock).toHaveBeenCalledTimes(2)
  expect(progress.mock.calls).toEqual([[{ phase: 'preparing' }]])
  await vi.advanceTimersByTimeAsync(1000)
  expect(await (await result).blob.text()).toBe('zip-content')
  expect(progress.mock.calls).toEqual([[{ phase: 'preparing' }],
    [{ phase: 'downloading', receivedBytes: 0, totalBytes: 11 }], [{ phase: 'downloading', receivedBytes: 11, totalBytes: 11 }]])
  expect(fetchMock.mock.calls.map(([url]) => url)).toEqual([
    '/api/item-review/runs/run%2Fid/package', '/api/item-review/runs/run%2Fid/package/status',
    '/api/item-review/runs/run%2Fid/package/status', '/api/item-review/runs/run%2Fid/package/chunk?package_id=zip-version-1&offset=0',
  ])
  for (const [, options] of fetchMock.mock.calls) expect(options.headers).toEqual({ 'X-Review-Token': 'private-access' })
})

it('stops waiting and polling when its browser request is aborted', async () => {
  vi.useFakeTimers()
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ status: 'preparing' }), { status: 202 }))
  vi.stubGlobal('fetch', fetchMock)
  const controller = new AbortController()
  const result = getReviewPackage(packageAccess, undefined, controller.signal)
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
  await expect(getReviewPackage(packageAccess, undefined, controller.signal)).rejects.toMatchObject({ name: 'AbortError' })
  expect(fetchMock).not.toHaveBeenCalled()
})

it.each(['failed', 'not_started'])('reports %s preparation without transferring or repeating the request', async status => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ status, message: 'Package preparation was interrupted. Your saved results are unchanged.', error_status: 503 })))
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage(packageAccess)).rejects.toMatchObject({ status: 503, message: 'Package preparation was interrupted. Your saved results are unchanged.' })
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it('explains a preparation connection failure without restarting preparation', async () => {
  const fetchMock = vi.fn().mockRejectedValueOnce(new TypeError('Failed to fetch'))
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage(packageAccess)).rejects.toThrow('The connection was interrupted while preparing the results package. Your saved results are unchanged. Please try downloading again.')
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it('retries only a truncated middle piece and assembles exact bytes with monotonic progress', async () => {
  vi.useFakeTimers()
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage({ bytes: 10, chunk_bytes: 4 }))
    .mockResolvedValueOnce(packagePiece('abcd'))
    .mockResolvedValueOnce(packagePiece('ef', 4, { 'Content-Length': '4' }))
    .mockResolvedValueOnce(packagePiece('efgh', 4))
    .mockResolvedValueOnce(packagePiece('ij', 8))
  vi.stubGlobal('fetch', fetchMock)
  const progress = vi.fn()
  const result = getReviewPackage(packageAccess, progress)
  await vi.runAllTimersAsync()
  expect(await (await result).blob.text()).toBe('abcdefghij')
  expect(fetchMock.mock.calls.slice(1).map(([url]) => new URL(url, 'https://test').searchParams.get('offset'))).toEqual(['0', '4', '4', '8'])
  expect(progress.mock.calls.slice(1).map(([value]) => value.receivedBytes)).toEqual([0, 4, 8, 10])
  expect(vi.getTimerCount()).toBe(0)
})

it('retries a response-body network failure before assembling the package', async () => {
  vi.useFakeTimers()
  const response = packagePiece('zip-content')
  vi.spyOn(response, 'blob').mockRejectedValueOnce(new TypeError('NetworkError'))
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage()).mockResolvedValueOnce(response).mockResolvedValueOnce(packagePiece('zip-content'))
  vi.stubGlobal('fetch', fetchMock)
  const result = getReviewPackage(packageAccess)
  await vi.runAllTimersAsync()
  expect(await (await result).blob.text()).toBe('zip-content')
  expect(fetchMock.mock.calls[1][0]).toBe(fetchMock.mock.calls[2][0])
})

it.each([429, 502, 503, 504])('retries transient HTTP %s pieces without redoing preparation', async status => {
  vi.useFakeTimers()
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage())
    .mockResolvedValueOnce(new Response('', { status })).mockResolvedValueOnce(packagePiece('zip-content'))
  vi.stubGlobal('fetch', fetchMock)
  const result = getReviewPackage(packageAccess)
  await vi.runAllTimersAsync()
  expect(await (await result).blob.text()).toBe('zip-content')
  expect(fetchMock).toHaveBeenCalledTimes(3)
  expect(fetchMock.mock.calls[1][0]).toBe(fetchMock.mock.calls[2][0])
})

it.each([
  { 'X-Package-Id': 'different-version' }, { 'X-Package-Offset': '1' }, { 'X-Package-Id': '' },
] as Record<string, string>[])('rejects a changed or missing piece identity %j without retrying or mixing versions', async headers => {
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage()).mockResolvedValueOnce(packagePiece('zip-content', 0, headers))
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage(packageAccess)).rejects.toThrow('did not match the requested package')
  expect(fetchMock).toHaveBeenCalledTimes(2)
})

it('stops on package replacement or cache loss and asks for a fresh download', async () => {
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage({ bytes: 8, chunk_bytes: 4 }))
    .mockResolvedValueOnce(packagePiece('abcd')).mockResolvedValueOnce(new Response('', { status: 412 }))
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage(packageAccess)).rejects.toThrow('prepared package changed or is no longer available. Your saved results are unchanged')
  expect(fetchMock).toHaveBeenCalledTimes(3)
})

it.each([206, 403, 404])('does not retry an unexpected HTTP %s response or accept its body', async status => {
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage())
    .mockResolvedValueOnce(new Response('zip-content', { status, headers: {
      'X-Package-Id': packageMetadata.package_id, 'X-Package-Offset': '0', 'Content-Length': '11',
    } }))
  vi.stubGlobal('fetch', fetchMock)
  await expect(getReviewPackage(packageAccess)).rejects.toThrow('Your saved results are unchanged')
  expect(fetchMock).toHaveBeenCalledTimes(2)
})

it.each(['network', 'length', 'header'] as const)('stops after three attempts for a persistent %s failure without returning partial bytes', async kind => {
  vi.useFakeTimers()
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage({ bytes: 8, chunk_bytes: 4 })).mockResolvedValueOnce(packagePiece('abcd'))
  fetchMock.mockImplementation(() => kind === 'network' ? Promise.reject(new TypeError('Failed to fetch'))
    : Promise.resolve(kind === 'length' ? packagePiece('e', 4, { 'Content-Length': '4' }) : packagePiece('efgh', 4, { 'Content-Length': '3' })))
  vi.stubGlobal('fetch', fetchMock)
  const result = getReviewPackage(packageAccess)
  const rejection = expect(result).rejects.toThrow('Your saved results are unchanged')
  await vi.runAllTimersAsync()
  await rejection
  expect(fetchMock.mock.calls.slice(1).map(([url]) => new URL(url, 'https://test').searchParams.get('offset'))).toEqual(['0', '4', '4', '4'])
  expect(vi.getTimerCount()).toBe(0)
})

it('times out each stalled body read and stops after three bounded attempts', async () => {
  vi.useFakeTimers()
  const signals: AbortSignal[] = []
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage()).mockImplementation((_url, options) => {
    signals.push(options.signal)
    const response = packagePiece('zip-content')
    vi.spyOn(response, 'blob').mockImplementation(() => new Promise((_resolve, reject) => {
      options.signal.addEventListener('abort', () => reject(options.signal.reason), { once: true })
    }))
    return Promise.resolve(response)
  })
  vi.stubGlobal('fetch', fetchMock)
  const result = getReviewPackage(packageAccess)
  const rejection = expect(result).rejects.toThrow('download timed out after three attempts')
  await vi.advanceTimersByTimeAsync(45000)
  expect(signals).toHaveLength(1)
  expect(signals[0].aborted).toBe(true)
  await vi.advanceTimersByTimeAsync(500 + 45000 + 1000 + 45000)
  await rejection
  expect(signals).toHaveLength(3)
  expect(signals.every(signal => signal.aborted)).toBe(true)
  expect(fetchMock).toHaveBeenCalledTimes(4)
  expect(vi.getTimerCount()).toBe(0)
})

it.each(['body', 'backoff'] as const)('aborts an active %s without retrying or creating a partial download', async phase => {
  vi.useFakeTimers()
  const fetchMock = vi.fn().mockResolvedValueOnce(readyPackage()).mockImplementation((_url, options) => {
    if (phase === 'backoff') return Promise.reject(new TypeError('Failed to fetch'))
    const response = packagePiece('zip-content')
    vi.spyOn(response, 'blob').mockImplementation(() => new Promise((_resolve, reject) => {
      options.signal.addEventListener('abort', () => reject(options.signal.reason), { once: true })
    }))
    return Promise.resolve(response)
  })
  vi.stubGlobal('fetch', fetchMock)
  const controller = new AbortController()
  const result = getReviewPackage(packageAccess, undefined, controller.signal)
  const rejection = expect(result).rejects.toMatchObject({ name: 'AbortError' })
  await vi.advanceTimersByTimeAsync(0)
  controller.abort()
  await rejection
  await vi.advanceTimersByTimeAsync(45000)
  expect(fetchMock).toHaveBeenCalledTimes(2)
  expect(vi.getTimerCount()).toBe(0)
})
