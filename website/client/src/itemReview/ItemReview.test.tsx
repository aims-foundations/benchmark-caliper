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
  retrieval_policy: { version: 1, method: 'qwen3_embedding', model: 'Qwen/Qwen3-Embedding-0.6B', max_tokens: 8192, similarity: 'dot_product' },
  default_retrieve_k: 20, max_retrieve_k: 100,
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

it('explains the sample and paid shortlist, and starts only on submission', async () => {
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
  expect(screen.getByLabelText('Maximum items to assess')).toHaveValue(20)
  expect(screen.getByText(/Starting authorizes paid GPT-6 Luna assessments/)).toHaveTextContent('up to 20 retrieved items')
  await user.click(screen.getByRole('button', { name: 'Retrieve and assess shortlist' }))
  await screen.findByRole('heading', { name: 'Your item review is ready' })
  expect(api.startReview).toHaveBeenCalledWith({
    deployment: expect.objectContaining({ task: expect.stringContaining('mathematics tutor') }),
    retrieve_k: 20,
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
  await screen.findByRole('heading', { name: 'Assessing shortlisted items' })
  await user.click(screen.getByRole('button', { name: 'Stop review' }))
  await waitFor(() => expect(screen.getByRole('heading', { name: 'Review stopped' })).toBeInTheDocument())
  expect(api.cancelReview).toHaveBeenCalledWith({ run_id: 'test-run', run_secret: 'temporary-access' })
})

it('bounds paid judgments and preserves an optional exact reference question', async () => {
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key'), 'sk-test-private')
  await user.click(screen.getByRole('button', { name: 'Continue to deployment' }))
  await user.click(screen.getByRole('button', { name: 'Use mathematics tutor example' }))
  await user.click(screen.getByRole('button', { name: 'Review catalog and settings' }))
  const limit = screen.getByLabelText('Maximum items to assess')
  const submit = screen.getByRole('button', { name: 'Retrieve and assess shortlist' })
  for (const invalid of ['0', '101', '1.5']) {
    await user.clear(limit)
    await user.type(limit, invalid)
    expect(submit).toBeDisabled()
  }
  await user.clear(limit)
  expect(submit).toBeDisabled()
  await user.type(limit, '5')
  const query = '  Solve 2x + 3 = 7. Explain your reasoning.  '
  await user.type(screen.getByLabelText('Reference question (optional)'), query)
  expect(screen.getByText(/Starting authorizes paid GPT-6 Luna assessments/)).toHaveTextContent('up to 5 retrieved items')
  await user.click(screen.getByText('How retrieval selects the shortlist'))
  expect(screen.getByText(/up to 8,192 tokens per text/)).toBeVisible()
  expect(screen.getByText(/Exact question text matches are selected first/)).toBeVisible()
  await user.click(submit)
  await screen.findByRole('heading', { name: 'Your item review is ready' })
  expect(api.startReview).toHaveBeenCalledWith({ deployment: expect.any(Object), retrieve_k: 5, retrieval_query: query }, 'sk-test-private')
})
