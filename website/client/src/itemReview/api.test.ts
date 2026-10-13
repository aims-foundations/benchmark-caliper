import { afterEach, expect, it, vi } from 'vitest'
import { startReview, getReview } from './api'

afterEach(() => vi.unstubAllGlobals())

it('sends only the OpenAI key in headers and polls with a separate run secret', async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'a', run_secret: 'access' })))
  vi.stubGlobal('fetch', fetchMock)
  const input = { deployment: { task: 'Tutor', users: 'Students', inputs: 'Text', outputs: 'Text', success: 'Correct', constraints: '' } }
  await startReview(input, 'sk-secret')
  const [url, options] = fetchMock.mock.calls[0]
  expect(url).toBe('/api/item-review/runs')
  expect(options.headers).toEqual({ 'Content-Type': 'application/json', 'X-OpenAI-Key': 'sk-secret' })
  expect(options.body).not.toContain('secret')
  fetchMock.mockResolvedValue(new Response(JSON.stringify({ status: 'running' })))
  await getReview({ run_id: 'a', run_secret: 'access' })
  expect(fetchMock.mock.calls[1][1].headers).toEqual({ 'X-Review-Token': 'access' })
})
