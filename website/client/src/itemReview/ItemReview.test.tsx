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
  dataset_access_configured: true, table_count: 4, source_rows: 1200, missing_item_tables: [], branches: { main: 'a', migration: 'b' },
  sampling: { version: 1, method: 'seeded_hash_with_branch_coverage', seed: 20260925, items_per_benchmark: 50 }, sample_max_items: 150,
  benchmarks: [{ id: 'matharena', name: 'MathArena', table_count: 2, source_rows: 300, sample_max_items: 50 }, { id: 'coding', name: 'Coding', table_count: 1, source_rows: 500, sample_max_items: 50 }, { id: 'customer_support', name: 'Customer Support', table_count: 1, source_rows: 400, sample_max_items: 50 }] }
const completed: api.Review = {
  run_id: 'test-run', status: 'completed', message: 'Sample review complete.', model: 'gpt-6-luna', reasoning_effort: 'high',
  deployment: { task: '', users: '', inputs: '', outputs: '', success: '', constraints: '' },
  scope: { benchmarks: ['matharena', 'coding', 'customer_support'], table_count: 4, source_rows: 1200, branches: { main: 'a', migration: 'b' }, sample_only: true,
    sampling: catalog.sampling, sample_max_items: 150 },
  sample_complete: true, prepared_benchmarks: 3, pagination: { page: 1, page_size: 20, total_pages: 1 },
  scoring_policy: { version: 5, formula: '1 + sum(confidence * (score - 1) for scored dimensions) / 6; no scored dimensions yields null' },
  source_rows: 6, total: 4, processed: 4, complete: 4, needs_review: 4, errors: 0,
  ranked: 4, unranked: 0, usage: { input_tokens: 100, output_tokens: 200 }, ranked_items: [], unranked_items: [], failed_items: [],
}

beforeEach(() => {
  vi.clearAllMocks()
  sessionStorage.clear()
  localStorage.clear()
  vi.mocked(api.getCatalog).mockResolvedValue(catalog)
  vi.mocked(api.startReview).mockResolvedValue({ run_id: 'test-run', run_secret: 'temporary-access' })
  vi.mocked(api.getReview).mockResolvedValue(completed)
})

it('explains the fixed broad sample and starts only on submission', async () => {
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key'), 'sk-test-private')
  expect(screen.queryByLabelText('Hugging Face read token')).not.toBeInTheDocument()
  expect(screen.queryByText(/Hugging Face dataset access/)).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Continue to deployment' }))
  await user.click(screen.getByRole('button', { name: 'Use mathematics tutor example' }))
  await user.click(screen.getByRole('button', { name: 'Review catalog and settings' }))
  expect(screen.getByText(/Up to 150/)).toHaveTextContent('Up to 150 items')
  expect(screen.getByText(/fixed random seed/)).toBeVisible()
  expect(screen.getByText(/1,200/)).toHaveTextContent('1,200 source rows')
  expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
  expect(screen.queryByRole('checkbox')).not.toBeInTheDocument()
  await user.click(screen.getByText('Browse all 3 benchmark collections'))
  expect(screen.getByText('Customer Support')).toBeVisible()
  expect(api.startReview).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Start sampled review' }))
  await screen.findByRole('heading', { name: 'Your item review is ready' })
  expect(api.startReview).toHaveBeenCalledWith({
    deployment: expect.objectContaining({ task: expect.stringContaining('mathematics tutor') }),
  }, 'sk-test-private')
  expect(sessionStorage.getItem('item_review_run_v1')).not.toContain('sk-test-private')
  expect(localStorage.length).toBe(0)
  expect(screen.getByText('Evidence gaps or missing scores').parentElement).toHaveTextContent('4')
})

it('reports missing server dataset access without asking visitors for another key', async () => {
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, dataset_access_configured: false })
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key'), 'sk-test-private')
  expect(screen.getByRole('alert')).toHaveTextContent('Dataset access is not configured on this server.')
  expect(screen.queryByLabelText('Hugging Face read token')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Continue to deployment' })).toBeDisabled()
  expect(api.startReview).not.toHaveBeenCalled()
})

it('restores progress with a run token and supports stopping an active review', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...completed, status: 'running', processed: 1 })
  vi.mocked(api.cancelReview).mockResolvedValue({ ...completed, status: 'cancelled', processed: 1 })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Reviewing sampled items' })
  await user.click(screen.getByRole('button', { name: 'Stop review' }))
  await waitFor(() => expect(screen.getByRole('heading', { name: 'Review stopped' })).toBeInTheDocument())
  expect(api.cancelReview).toHaveBeenCalledWith({ run_id: 'test-run', run_secret: 'temporary-access' })
})
