import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemReview } from './ItemReview'
import * as api from './api'

vi.mock('./api', async importOriginal => ({
  ...await importOriginal<typeof import('./api')>(),
  getCatalog: vi.fn(), startReview: vi.fn(), getReview: vi.fn(), cancelReview: vi.fn(),
}))

const catalog: api.Catalog = { model: 'gpt-6-luna', reasoning_effort: 'high', max_output_tokens: 25000,
  requires_hf_token: false, max_items_per_table: 10, branches: { main: 'a', migration: 'b' },
  benchmarks: [{ id: 'matharena', name: 'MathArena', table_count: 2 }, { id: 'afrimedqa', name: 'AfriMed-QA', table_count: 1 }] }
const completed: api.Review = {
  run_id: 'test-run', status: 'completed', message: 'Sample review complete.', model: 'gpt-6-luna', reasoning_effort: 'high',
  deployment: { task: '', users: '', inputs: '', outputs: '', success: '', constraints: '' },
  scope: { benchmarks: ['matharena'], items_per_table: 2, branches: { main: 'a' }, sample_only: true },
  source_rows: 6, total: 4, processed: 4, complete: 0, unresolved: 4, errors: 0,
  usage: { input_tokens: 100, output_tokens: 200 }, ranked_items: [], unresolved_items: [],
}

beforeEach(() => {
  vi.clearAllMocks()
  sessionStorage.clear()
  localStorage.clear()
  vi.mocked(api.getCatalog).mockResolvedValue(catalog)
  vi.mocked(api.startReview).mockResolvedValue({ run_id: 'test-run', run_secret: 'temporary-access' })
  vi.mocked(api.getReview).mockResolvedValue(completed)
})

it('collects deployment details, previews scope, and starts a paid review only on submission', async () => {
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key'), 'sk-test-private')
  await user.click(screen.getByRole('button', { name: 'Continue to deployment' }))
  await user.click(screen.getByRole('button', { name: 'Use mathematics tutor example' }))
  await user.click(screen.getByRole('button', { name: 'Review sample and settings' }))
  expect(screen.getByText('Up to 6 source rows')).toBeInTheDocument()
  expect(api.startReview).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Start paid review' }))
  await screen.findByRole('heading', { name: 'Your sample review is ready' })
  expect(api.startReview).toHaveBeenCalledWith(expect.objectContaining({
    items_per_table: 2, benchmarks: ['matharena', 'afrimedqa'],
    deployment: expect.objectContaining({ task: expect.stringContaining('mathematics tutor') }),
  }), 'sk-test-private', '')
  expect(sessionStorage.getItem('item_review_run_v1')).not.toContain('sk-test-private')
  expect(localStorage.length).toBe(0)
  expect(screen.getByText(/4 unresolved/)).toBeInTheDocument()
})

it('requires dataset access when the server has no Hugging Face token', async () => {
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, requires_hf_token: true })
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key'), 'sk-test-private')
  expect(screen.getByRole('button', { name: 'Continue to deployment' })).toBeDisabled()
  await user.type(screen.getByLabelText('Hugging Face read token'), 'hf_test_private')
  expect(screen.getByRole('button', { name: 'Continue to deployment' })).toBeEnabled()
})

it('restores progress with a run token and supports stopping an active review', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...completed, status: 'running', processed: 1 })
  vi.mocked(api.cancelReview).mockResolvedValue({ ...completed, status: 'cancelled', processed: 1 })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Reviewing evaluation items' })
  await user.click(screen.getByRole('button', { name: 'Stop review' }))
  await waitFor(() => expect(screen.getByRole('heading', { name: 'Review stopped' })).toBeInTheDocument())
  expect(api.cancelReview).toHaveBeenCalledWith({ run_id: 'test-run', run_secret: 'temporary-access' })
})
