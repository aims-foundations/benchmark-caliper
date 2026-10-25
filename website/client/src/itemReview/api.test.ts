import { afterEach, expect, it, vi } from 'vitest'
import { startReview, startGrounding, startBenchmarkRetrieval, getCandidates, getReview } from './api'

afterEach(() => vi.unstubAllGlobals())

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
