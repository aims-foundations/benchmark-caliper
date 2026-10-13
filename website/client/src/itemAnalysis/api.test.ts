import { afterEach, expect, it, vi } from 'vitest'
import { AnalysisApiError, classify, createRun, download, getRun } from './api'

afterEach(() => vi.unstubAllGlobals())

it('sends the API key in a header and keeps it outside the request body and URL', async () => {
  const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ run_id: 'test', run_secret: 'private' })))
  vi.stubGlobal('fetch', fetch)
  await createRun('mmlu', 'generate', 'sk-secret')
  expect(fetch).toHaveBeenCalledWith('/api/item-analysis/runs', expect.objectContaining({
    method: 'POST', headers: { 'Content-Type': 'application/json', 'X-OpenAI-Key': 'sk-secret' },
    body: JSON.stringify({ example_id: 'mmlu', specification_mode: 'generate' }),
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
