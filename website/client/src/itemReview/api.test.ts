import { afterEach, expect, it, vi } from 'vitest'
import { startReview, getReview } from './api'

afterEach(() => vi.unstubAllGlobals())

it('sends provider keys only in headers and polls with a separate run secret', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'a', run_secret: 'access' })))
  vi.stubGlobal('fetch', fetchMock)
  const input = { deployment: { task: 'Tutor', users: 'Students', inputs: 'Text', outputs: 'Text', success: 'Correct', constraints: '' },
    benchmarks: ['matharena'], items_per_table: 2, top_k: 10 }
  await startReview(input, 'sk-secret', 'hf_secret')
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe('/api/item-review/runs')
  expect(options.headers['X-OpenAI-Key']).toBe('sk-secret')
  expect(options.headers['X-HuggingFace-Key']).toBe('hf_secret')
  expect(options.body).not.toContain('secret')
  fetchMock.mockResolvedValue(new Response(JSON.stringify({ status: 'running' })))
  await getReview({ run_id: 'a', run_secret: 'access' })
  expect(fetchMock.mock.calls[1][1].headers).toEqual({ 'X-Review-Token': 'access' })
})
