import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemAnalysis } from './ItemAnalysis'
import { ItemJudgments, matchesItemFilter } from './Results'
import { buildSixScoreDemoRun } from '../demo/sixScoreItemFixture'
import * as api from './api'
import type { AnalysisRun, Item } from './types'

vi.mock('./api', async original => ({ ...await original<typeof import('./api')>(), getCatalog: vi.fn(), createRun: vi.fn(), getRun: vi.fn(), classify: vi.fn(), cancelRun: vi.fn() }))
const access = { run_id: 'six-score-test', run_secret: 'private-token' }
function readyRun(): AnalysisRun {
  const run = buildSixScoreDemoRun('sample')
  return { ...run, run_id: access.run_id, status: 'ready', processed: 0, complete: 0, scope: null, completed_judgments: 0,
    remaining_judgments: { pilot: 24, all: 60 }, remaining_requests: { pilot: 4, all: 10 },
    items: run.items.map(item => ({ ...item, status: 'pending', dimensions: undefined })) }
}
beforeEach(() => {
  vi.clearAllMocks(); localStorage.clear(); sessionStorage.clear()
  const ready = readyRun()
  vi.mocked(api.getCatalog).mockResolvedValue({ examples: [ready.example], checkpoint_size: 4 })
  vi.mocked(api.getRun).mockResolvedValue(ready)
  vi.mocked(api.createRun).mockResolvedValue({ ...ready, ...access })
})

it('prepares context without a key then starts one scoring request per item for all items', async () => {
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await user.click(await screen.findByRole('button', { name: 'Prepare shared context' }))
  await screen.findByRole('button', { name: 'Analyze items' })
  expect(api.createRun).toHaveBeenCalledWith(readyRun().example.id, 'generate', '')
  expect(api.classify).not.toHaveBeenCalled()
  expect(within(screen.getByRole('navigation', { name: 'Item analysis steps' })).getAllByRole('link')).toHaveLength(3)
  expect(screen.getByText(/10 primary scoring calls remaining/)).toBeVisible()
  expect(screen.getByRole('radio', { name: 'All 10 items' })).toBeChecked()
  expect(screen.getByRole('button', { name: 'Analyze items' })).toBeDisabled()
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-scoring-only')
  const running: AnalysisRun = { ...readyRun(), status: 'running', scope: 'all' }
  vi.mocked(api.classify).mockResolvedValue(running)
  vi.mocked(api.getRun).mockResolvedValue(running)
  await user.click(screen.getByRole('button', { name: 'Analyze items' }))
  expect(api.classify).toHaveBeenCalledExactlyOnceWith(access, 'all', 'sk-scoring-only')
  expect(screen.getByRole('progressbar', { name: 'Item scoring progress' })).toHaveAttribute('max', '10')
  expect(localStorage.getItem('item_analysis_run_v1')).not.toContain('sk-scoring-only')
})

it('restores a stopped full run and prevents shrinking its scope to a pilot', async () => {
  localStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...readyRun(), status: 'cancelled', scope: 'all', processed: 1, complete: 1 })
  render(<ItemAnalysis />)
  expect(await screen.findByRole('radio', { name: 'All 10 items' })).toBeChecked()
  expect(screen.getByRole('radio', { name: 'First 4 items' })).toBeDisabled()
  expect(screen.getByRole('button', { name: 'Continue analysis' })).toBeDisabled()
  expect(api.classify).not.toHaveBeenCalled()
})

it('keeps unknown judgments distinct from pending items and retryable processing failures', async () => {
  const run = buildSixScoreDemoRun('sample')
  const scored = run.items[0]
  const failed: Item = { ...scored, item_id: 'failed', dimensions: undefined, status: 'error', error: 'Response validation failed.' }
  const pending: Item = { ...scored, item_id: 'pending', dimensions: undefined, status: 'pending' }
  run.items = [scored, failed, pending]
  const user = userEvent.setup()
  render(<ItemJudgments run={run} page={1} setPage={() => {}} pageLoading={false} />)
  expect(screen.getByRole('button', { name: `${scored.item_id} · Output Content: Unknown` })).toBeEnabled()
  expect(screen.getByRole('button', { name: 'failed · Output Content: Needs retry' })).toBeEnabled()
  expect(screen.getByRole('button', { name: 'pending · Output Content: Pending' })).toBeEnabled()
  await user.click(screen.getByRole('button', { name: `${scored.item_id} · Output Content: Unknown` }))
  const details = screen.getByRole('region', { name: 'Selected score details' })
  expect(details).toHaveAttribute('aria-live', 'polite')
  expect(details).toHaveTextContent('Target-teacher judgments')
  expect(details).toHaveTextContent(String(scored.reference_answer).replace(/\s+/g, ' ').trim())
  await user.click(screen.getByRole('button', { name: 'failed · Output Content: Needs retry' }))
  expect(details).toHaveTextContent('Response validation failed.')
  expect(matchesItemFilter(scored, { kind: 'uncertain' })).toBe(true)
  expect(matchesItemFilter(failed, { kind: 'uncertain' })).toBe(false)
  expect(matchesItemFilter(pending, { kind: 'uncertain' })).toBe(false)
  expect(matchesItemFilter(failed, { kind: 'retry' })).toBe(true)
  const low: Item = { ...scored, dimensions: { input_ontology: { score: 2, justification: 'Task mismatch.', evidence: [], information_gaps: [] } } }
  expect(matchesItemFilter(low, { kind: 'flagged', classifierId: 'input_ontology' })).toBe(true)
  expect(matchesItemFilter(low, { kind: 'flagged', classifierId: 'input_content' })).toBe(false)
})

it('can choose a pilot and continue through all items without a review acknowledgment', async () => {
  localStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await user.click(await screen.findByRole('radio', { name: 'First 4 items' }))
  expect(screen.getByText(/4 primary scoring calls remaining/)).toBeVisible()
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-pilot')
  const checkpoint: AnalysisRun = { ...readyRun(), status: 'checkpoint', processed: 4, complete: 4, scope: 'pilot', can_continue: true,
    remaining_judgments: { pilot: 0, all: 36 }, remaining_requests: { pilot: 0, all: 6 } }
  vi.mocked(api.classify).mockResolvedValue(checkpoint)
  vi.mocked(api.getRun).mockResolvedValue(checkpoint)
  await user.click(screen.getByRole('button', { name: 'Analyze items' }))
  await waitFor(() => expect(api.classify).toHaveBeenCalledWith(access, 'pilot', 'sk-pilot'))
  await user.click(screen.getByRole('radio', { name: 'All 10 items' }))
  expect(screen.queryByRole('checkbox')).not.toBeInTheDocument()
  expect(screen.getByText(/6 primary scoring calls remaining/)).toBeVisible()
  expect(screen.getByRole('button', { name: 'Continue analysis' })).toBeEnabled()
})
