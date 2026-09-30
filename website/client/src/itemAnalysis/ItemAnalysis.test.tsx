import { beforeEach, expect, it, vi } from 'vitest'
import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemAnalysis } from './ItemAnalysis'
import * as api from './api'
import type { AnalysisRun, Catalog } from './types'

vi.mock('./api', async original => ({ ...await original<typeof import('./api')>(),
  getCatalog: vi.fn(), createRun: vi.fn(), getRun: vi.fn(), classify: vi.fn(), cancelRun: vi.fn(), download: vi.fn(),
}))

const example = { id: 'illustrative', title: 'Exam preparation example', description: 'Authored examples for demonstrating the workflow.', item_count: 10,
  benchmark: 'illustrative', deployment: 'Hindi-medium exam preparation.', source_label: 'Illustrative teaching items', available: true, supplied_spec_available: true }
const catalog: Catalog = { examples: [example], checkpoint_size: 100 }
const access = { run_id: 'run-123', run_secret: 'private-run-token' }
const ready: AnalysisRun = {
  run_id: access.run_id, status: 'ready', message: 'Criteria are ready for inspection.', example,
  spec: { benchmark: 'illustrative', deployment: example.deployment, classifiers: [{ id: 'IC.region_fit', component: 'input_content', operation: 'ordinal', applicable: true,
    criterion: 'Assess the item’s regional relevance.', ordinal_anchors: { '1': 'Region relevant', '2': 'Region neutral', '3': 'Region misaligned' } }] },
  summary: { total_items: 10, completed_items: 0, error_items: 0, pending_items: 10, complete_snapshot: false, classifiers: [] },
  processed: 0, total: 10, complete: 0, errors: 0, items: [{ item_id: 'example-1', content: 'What is 2 + 2?', reference_answer: '4', status: 'pending' }],
  pagination: { page: 1, total_pages: 1 }, usage: { input_tokens: 0, output_tokens: 0 }, can_continue: false, scope: null,
}

beforeEach(() => {
  vi.clearAllMocks()
  sessionStorage.clear()
  localStorage.clear()
  vi.mocked(api.getCatalog).mockResolvedValue(catalog)
  vi.mocked(api.createRun).mockResolvedValue({ ...ready, ...access })
  vi.mocked(api.getRun).mockResolvedValue(ready)
})

it('loads supplied criteria without a key and labels unscored illustrative items honestly', async () => {
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  expect(await screen.findByRole('radio', { name: /Generate with Sonnet/ })).toBeChecked()
  expect(screen.getByText('Illustrative teaching items')).toBeVisible()
  await user.click(screen.getByRole('radio', { name: /Use example criteria/ }))
  expect(screen.queryByLabelText('Anthropic API key')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: /Load example criteria/ }))
  await screen.findByRole('heading', { name: 'Your criteria are ready' })
  expect(api.createRun).toHaveBeenCalledWith('illustrative', 'provided', '')
  expect(api.classify).not.toHaveBeenCalled()
  expect(screen.getByRole('button', { name: 'Classify 10 items with Haiku' })).toBeDisabled()
  expect(screen.getByText('Pending')).toBeVisible()
  expect(screen.queryByRole('heading', { name: 'What the items show' })).not.toBeInTheDocument()
  await user.click(screen.getByText('Regional relevance'))
  expect(screen.getByText('Assess the item’s regional relevance.')).toBeVisible()
})

it('generates with Sonnet, then explicitly starts Haiku without persisting the API key', async () => {
  const user = userEvent.setup()
  vi.mocked(api.classify).mockResolvedValue({ ...ready, status: 'running', scope: 'pilot' })
  render(<ItemAnalysis />)
  await user.type(await screen.findByLabelText('Anthropic API key'), 'sk-ant-private')
  await user.click(screen.getByRole('button', { name: /Generate criteria with Sonnet/ }))
  await screen.findByRole('heading', { name: 'Your criteria are ready' })
  expect(api.createRun).toHaveBeenCalledWith('illustrative', 'generate', 'sk-ant-private')
  expect(api.classify).not.toHaveBeenCalled()
  expect(JSON.parse(sessionStorage.getItem('item_analysis_run_v1')!)).toEqual(access)
  expect(localStorage.length).toBe(0)
  await user.click(screen.getByRole('button', { name: 'Classify 10 items with Haiku' }))
  expect(api.classify).toHaveBeenCalledWith(access, 'pilot', 'sk-ant-private')
  expect(sessionStorage.getItem('item_analysis_run_v1')).not.toContain('sk-ant-private')
})

it('restores a checkpoint, requires key reentry, and continues through all remaining items', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  const checkpoint: AnalysisRun = { ...ready, status: 'checkpoint', processed: 100, complete: 100, total: 14015, can_continue: true, scope: 'pilot',
    example: { ...example, item_count: 14015, source_label: 'measurement-db MMLU snapshot' } }
  vi.mocked(api.getRun).mockResolvedValue(checkpoint)
  vi.mocked(api.classify).mockResolvedValue({ ...checkpoint, status: 'running', scope: 'all', can_continue: false })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await screen.findByRole('heading', { name: 'Pause here for a human review' })
  expect(screen.getByText('measurement-db MMLU snapshot')).toBeVisible()
  expect(screen.getByLabelText('Anthropic API key')).toHaveValue('')
  expect(screen.getByRole('button', { name: 'Continue through all items' })).toBeDisabled()
  expect(screen.getByText(/13,915 paid Haiku item requests/)).toBeVisible()
  await user.type(screen.getByLabelText('Anthropic API key'), 'sk-ant-returned')
  await user.click(screen.getByRole('button', { name: 'Continue through all items' }))
  expect(api.classify).toHaveBeenCalledWith(access, 'all', 'sk-ant-returned')
  expect(api.createRun).not.toHaveBeenCalled()
})

it('stops an active run and offers a resumable checkpoint', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'running', processed: 2 })
  vi.mocked(api.cancelRun).mockImplementation(async () => {
    const stopped: AnalysisRun = { ...ready, status: 'cancelled', processed: 2 }
    vi.mocked(api.getRun).mockResolvedValue(stopped)
    return stopped
  })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await user.click(await screen.findByRole('button', { name: 'Stop analysis' }))
  await screen.findByRole('heading', { name: 'Analysis stopped' })
  expect(api.cancelRun).toHaveBeenCalledWith(access)
  expect(screen.getByRole('button', { name: 'Resume classification' })).toBeDisabled()
})

it('handles expired runs without starting model calls and supports a fresh analysis', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockRejectedValue(new api.AnalysisApiError('Expired', 404))
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  expect(await screen.findByRole('alert')).toHaveTextContent('This run is no longer available')
  await user.click(screen.getByRole('button', { name: 'Start a new analysis' }))
  await screen.findByRole('heading', { name: 'A benchmark. A real use case.' })
  expect(sessionStorage.getItem('item_analysis_run_v1')).toBeNull()
  expect(api.createRun).not.toHaveBeenCalled()
  expect(api.classify).not.toHaveBeenCalled()
})

it('shows category denominators, unknowns, and item evidence for completed results', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  const completed: AnalysisRun = { ...ready, status: 'complete', processed: 10, complete: 9, errors: 1,
    items: [{ ...ready.items[0], status: 'complete', labels: { 'IC.region_fit': { label: 2, justification: 'Arithmetic does not require regional knowledge.', evidence: ['2 + 2'] } } }],
    summary: { ...ready.summary!, completed_items: 9, error_items: 1, pending_items: 0,
      classifiers: [{ ...ready.spec!.classifiers[0], counts: { '1': 2, '2': 5, '3': 0 }, known: 7, unknown: 2, invalid: 0, errors: 1, pending: 0, percentages_among_known: { '1': 28.571, '2': 71.429, '3': 0 } }] } }
  vi.mocked(api.getRun).mockResolvedValue(completed)
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await screen.findByRole('heading', { name: 'What the items show' })
  expect(screen.getByText('7 known labels · 2 unknown · 0 invalid')).toBeVisible()
  expect(screen.getByText('71.4%')).toBeVisible()
  expect(screen.getByText('1 failed · 0 pending')).toBeVisible()
  await user.click(screen.getByText('What is 2 + 2?', { selector: 'strong' }))
  expect(screen.getByText('Arithmetic does not require regional knowledge.')).toBeVisible()
  expect(screen.getByText('2 + 2')).toBeVisible()
  await waitFor(() => expect(screen.queryByRole('button', { name: 'Continue through all items' })).not.toBeInTheDocument())
})

it('withholds stale aggregate statistics and exports while item classification is running', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'running', processed: 2, complete: 2 })
  render(<ItemAnalysis />)
  await screen.findByRole('heading', { name: 'Reading the items' })
  expect(screen.queryByRole('heading', { name: 'What the items show' })).not.toBeInTheDocument()
  expect(screen.getByText(/Summary statistics and exports update when this phase finishes/)).toBeVisible()
  expect(screen.getByRole('button', { name: 'Item labels CSV' })).toBeDisabled()
  expect(screen.getByRole('button', { name: 'Download criteria ↓' })).toBeEnabled()
})

it('stops automatic polling after three connection failures and offers an explicit retry', async () => {
  vi.useFakeTimers()
  try {
    sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
    vi.mocked(api.getRun).mockRejectedValue(new Error('Network disconnected'))
    render(<ItemAnalysis />)
    await act(async () => {})
    expect(api.getRun).toHaveBeenCalledTimes(1)
    await act(async () => { await vi.advanceTimersByTimeAsync(2000) })
    expect(api.getRun).toHaveBeenCalledTimes(2)
    await act(async () => { await vi.advanceTimersByTimeAsync(4000) })
    expect(api.getRun).toHaveBeenCalledTimes(3)
    await act(async () => { await vi.advanceTimersByTimeAsync(60000) })
    expect(api.getRun).toHaveBeenCalledTimes(3)
    expect(screen.getByRole('alert')).toHaveTextContent('Could not reconnect')
    expect(screen.getByRole('button', { name: 'Retry connection' })).toBeEnabled()
  } finally { vi.useRealTimers() }
})
