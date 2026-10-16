import { beforeEach, expect, it, vi } from 'vitest'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DIRECT_CONTEXT_STORAGE_KEY, DirectItemStart } from './DirectItemStart'
import { assessmentStorageKey } from './accessStorage'
import * as api from './api'
import type { AnalysisRun, AssessmentSetup, DirectContext } from './types'

vi.mock('./api', async original => ({ ...await original<typeof import('./api')>(),
  getDirectSetup: vi.fn(), createDirectRun: vi.fn(), getRun: vi.fn(), classify: vi.fn(), cancelRun: vi.fn(), download: vi.fn(),
  getCatalog: vi.fn(), getAssessment: vi.fn(), createAssessmentRun: vi.fn(), searchSources: vi.fn(),
}))

const context: DirectContext = { benchmark: 'MathDial', deployment: 'Tutoring grade 5 students in India in English.',
  task_requirements: 'Multi-step arithmetic word problems.', answer_requirements: 'Ask guiding questions without revealing the answer.', validity_concerns: '' }
const assessment = { kind: 'direct' as const, id: 'direct-context-a', benchmark: context.benchmark, benchmark_name: context.benchmark,
  deployment: 'Deployment context:\nTutoring grade 5 students in India in English.\n\nTask requirements:\nMulti-step arithmetic word problems.\n\nAnswer requirements:\nAsk guiding questions without revealing the answer.',
  direct_context: context, assessment_status: 'not_run' as const, analysis_basis: 'deployment_requirements' as const }
const source = { id: 'databank:sha:mathdial', title: 'MathDial test', benchmark: 'mathdial', item_count: 4, available: true,
  source_label: 'Measurement Data Bank', source_revision: 'fixed-sha', source_url: 'https://huggingface.co/datasets/example/mathdial',
  match_reasons: ['Name matches MathDial'], conflicts: [], match_type: 'exact_name' as const, requires_confirmation: true as const }
const setup: AssessmentSetup = { assessment, sources: [source], checkpoint_size: 2,
  benchmark_identity: { name: 'MathDial', full_name: null, aliases: [], paper_urls: [], source_urls: [], year: null, languages: [], version: null, evidence: { name: 'User declared' } },
  catalog: { status: 'ready', message: 'Current catalog', repo: 'measurement-db', revision: 'fixed-sha', requires_confirmation: true },
  upload: { max_bytes: 1000000, max_items: 10000, formats: ['csv', 'json'] } }
const access = { run_id: 'direct-run-a', run_secret: 'private-direct-token' }
const tokenKey = assessmentStorageKey(assessment)
const ready: AnalysisRun = { run_id: access.run_id, assessment, status: 'ready', message: 'Ready to inspect.',
  example: { id: assessment.id, title: 'MathDial for tutoring', benchmark: 'MathDial', deployment: assessment.deployment, description: 'From deployment requirements.', item_count: 4, source_label: 'Measurement Data Bank', available: true },
  spec: { benchmark: 'MathDial', deployment: assessment.deployment, classifiers: [
    { id: 'IO.task_category', component: 'input_ontology', operation: 'assignment', applicable: true, criterion: 'Which task is requested?', category_set: ['arithmetic', 'other'] },
    { id: 'IF', component: 'input_form', operation: 'flag', applicable: false, criterion: '' },
  ] },
  summary: { total_items: 4, completed_items: 0, error_items: 0, pending_items: 4, complete_snapshot: false, classifiers: [] },
  processed: 0, complete: 0, errors: 0, total: 4, items: [{ item_id: 'item-1', content: 'Solve 2 + 2', reference_answer: '4', status: 'pending' }],
  pagination: { page: 1, total_pages: 1 }, usage: { input_tokens: 0, output_tokens: 0 }, can_continue: false, scope: null }

beforeEach(() => {
  vi.clearAllMocks()
  sessionStorage.clear()
  localStorage.clear()
  vi.mocked(api.getDirectSetup).mockResolvedValue(setup)
  vi.mocked(api.createDirectRun).mockResolvedValue({ ...ready, ...access })
  vi.mocked(api.getRun).mockResolvedValue(ready)
})

function fillContext(values = context) {
  fireEvent.change(screen.getByLabelText('Benchmark'), { target: { value: values.benchmark } })
  fireEvent.change(screen.getByLabelText('Deployment context'), { target: { value: values.deployment } })
  fireEvent.change(screen.getByLabelText('Task requirements'), { target: { value: values.task_requirements } })
  fireEvent.change(screen.getByLabelText('Answer requirements'), { target: { value: values.answer_requirements } })
}

async function confirmContext(user = userEvent.setup()) {
  fillContext()
  await user.click(screen.getByRole('button', { name: 'Find and confirm benchmark items' }))
  await user.click(await screen.findByRole('button', { name: 'Confirm benchmark' }))
  return user
}

function saveContext() {
  sessionStorage.setItem(DIRECT_CONTEXT_STORAGE_KEY, JSON.stringify({ version: 1, id: assessment.id, context }))
  sessionStorage.setItem(tokenKey, JSON.stringify(access))
}

it('requires declared context, dataset confirmation, explicit generation, and pilot review before completing only item analysis', async () => {
  render(<DirectItemStart />)
  expect(api.getDirectSetup).not.toHaveBeenCalled()
  expect(screen.queryByLabelText(/API key/i)).not.toBeInTheDocument()
  fillContext()
  expect(api.getDirectSetup).not.toHaveBeenCalled()
  const user = userEvent.setup()
  await user.click(screen.getByRole('button', { name: 'Find and confirm benchmark items' }))
  expect(api.getDirectSetup).toHaveBeenCalledExactlyOnceWith(context, '', expect.any(AbortSignal))
  expect(await screen.findByText('Benchmark you specified')).toBeVisible()
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  expect(api.createDirectRun).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-private-direct')
  expect(api.createDirectRun).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: /Generate item criteria/ }))
  await screen.findByRole('heading', { name: 'Your criteria are ready' })
  expect(api.createDirectRun).toHaveBeenCalledExactlyOnceWith(context, { benchmark_confirmed: true, source_id: source.id, source_revision: source.source_revision }, 'sk-private-direct')
  expect(api.classify).not.toHaveBeenCalled()
  expect(screen.getByText(/Input Form and Output Form are not assessed/)).toBeVisible()
  await user.click(screen.getByText('IF'))
  expect(screen.getByText('Not assessed in this item analysis.')).toBeVisible()
  expect(sessionStorage.getItem(tokenKey)).toBe(JSON.stringify(access))
  expect(JSON.stringify(sessionStorage)).not.toContain('sk-private-direct')
  expect(localStorage.length).toBe(0)

  const checkpoint: AnalysisRun = { ...ready, status: 'checkpoint', processed: 2, complete: 2, scope: 'pilot', can_continue: true }
  vi.mocked(api.classify).mockImplementationOnce(async () => { vi.mocked(api.getRun).mockResolvedValue(checkpoint); return checkpoint })
  await user.click(screen.getByRole('button', { name: 'Classify 2 items with GPT-6 Luna' }))
  expect(api.classify).toHaveBeenCalledExactlyOnceWith(access, 'pilot', 'sk-private-direct')
  await screen.findByRole('heading', { name: 'Pause here for a human review' })
  expect(screen.getByRole('button', { name: 'Continue through all items' })).toBeDisabled()
  await user.click(screen.getByRole('checkbox', { name: 'I have reviewed the pilot labels, evidence, and criteria' }))
  const complete: AnalysisRun = { ...checkpoint, status: 'complete', processed: 4, complete: 4, can_continue: false, scope: 'all',
    summary: { ...ready.summary!, completed_items: 4, pending_items: 0, complete_snapshot: true } }
  vi.mocked(api.classify).mockImplementationOnce(async () => { vi.mocked(api.getRun).mockResolvedValue(complete); return complete })
  await user.click(screen.getByRole('button', { name: 'Continue through all items' }))
  expect(api.classify).toHaveBeenLastCalledWith(access, 'all', 'sk-private-direct', true)
  expect(await screen.findByRole('heading', { name: 'Item analysis complete' })).toBeVisible()
  expect(screen.getAllByText('Benchmark assessment: Not run.').length).toBeGreaterThan(0)
  expect(screen.queryByText('Original six-dimension assessment')).not.toBeInTheDocument()
  expect(api.getAssessment).not.toHaveBeenCalled()
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
  expect(api.getCatalog).not.toHaveBeenCalled()
})

it('searches with the same direct requirements and resets benchmark confirmation when the search changes', async () => {
  const user = userEvent.setup()
  render(<DirectItemStart />)
  await confirmContext(user)
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-not-sent')
  await user.type(screen.getByLabelText('Search the Data Bank'), 'MathDial test')
  expect(screen.queryByRole('button', { name: /Generate item criteria/ })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Search Data Bank' }))
  expect(api.getDirectSetup).toHaveBeenLastCalledWith(context, 'MathDial test', expect.any(AbortSignal))
  await waitFor(() => expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeEnabled())
  expect(api.searchSources).not.toHaveBeenCalled()
  expect(api.createDirectRun).not.toHaveBeenCalled()
})

it('restores the exact direct run without a model call and clears its criteria when context is edited', async () => {
  saveContext()
  const galleryKey = 'item_analysis_run_v1:gallery:other'
  sessionStorage.setItem(galleryKey, JSON.stringify({ run_id: 'gallery-run', run_secret: 'gallery-token' }))
  const user = userEvent.setup()
  render(<DirectItemStart />)
  await screen.findByRole('heading', { name: 'Your criteria are ready' })
  expect(api.getRun).toHaveBeenCalledWith(access, 1, expect.any(AbortSignal))
  expect(api.getDirectSetup).not.toHaveBeenCalled()
  expect(screen.getByLabelText('OpenAI API key')).toHaveValue('')
  await user.click(screen.getByRole('button', { name: 'Edit context and start again' }))
  expect(screen.getByLabelText('Answer requirements')).toHaveValue(context.answer_requirements)
  expect(sessionStorage.getItem(tokenKey)).toBeNull()
  expect(sessionStorage.getItem(DIRECT_CONTEXT_STORAGE_KEY)).toBeNull()
  expect(sessionStorage.getItem(galleryKey)).toContain('gallery-token')
  expect(screen.queryByRole('heading', { name: 'Review the criteria' })).not.toBeInTheDocument()
  const changed = { ...context, answer_requirements: 'Give a brief final answer.' }
  fireEvent.change(screen.getByLabelText('Answer requirements'), { target: { value: changed.answer_requirements } })
  vi.mocked(api.getDirectSetup).mockResolvedValue({ ...setup, assessment: { ...assessment, id: 'direct-context-b', direct_context: changed } })
  await user.click(screen.getByRole('button', { name: 'Find and confirm benchmark items' }))
  expect(await screen.findByRole('button', { name: 'Confirm benchmark' })).toBeEnabled()
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  expect(api.createDirectRun).not.toHaveBeenCalled()
  expect(JSON.parse(sessionStorage.getItem(DIRECT_CONTEXT_STORAGE_KEY)!).id).toBe('direct-context-b')
})

it('ignores a stale discovery response after the form requirements change', async () => {
  let resolve!: (value: AssessmentSetup) => void
  vi.mocked(api.getDirectSetup).mockImplementationOnce(() => new Promise(done => { resolve = done }))
  const user = userEvent.setup()
  render(<DirectItemStart />)
  fillContext()
  await user.click(screen.getByRole('button', { name: 'Find and confirm benchmark items' }))
  const signal = vi.mocked(api.getDirectSetup).mock.calls[0][2]!
  fireEvent.change(screen.getByLabelText('Benchmark'), { target: { value: 'GSM8K' } })
  expect(signal.aborted).toBe(true)
  await act(async () => resolve(setup))
  expect(screen.getByLabelText('Benchmark')).toHaveValue('GSM8K')
  expect(screen.queryByRole('button', { name: 'Confirm benchmark' })).not.toBeInTheDocument()
  expect(sessionStorage.getItem(DIRECT_CONTEXT_STORAGE_KEY)).toBeNull()
  expect(api.createDirectRun).not.toHaveBeenCalled()
})

it.each(['mismatch', 'expired'])('does not reuse a %s restored run', async failure => {
  saveContext()
  if (failure === 'mismatch') vi.mocked(api.getRun).mockResolvedValue({ ...ready, assessment: { ...assessment, id: 'direct-another-context' } })
  else vi.mocked(api.getRun).mockRejectedValue(new api.AnalysisApiError('Expired', 410))
  render(<DirectItemStart />)
  expect(await screen.findByRole('alert')).toHaveTextContent('This run is no longer available')
  expect(screen.queryByRole('heading', { name: 'Review the criteria' })).not.toBeInTheDocument()
  expect(api.createDirectRun).not.toHaveBeenCalled()
  expect(api.classify).not.toHaveBeenCalled()
})

it('keeps an active run immutable until its phase ends', async () => {
  saveContext()
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'running' })
  render(<DirectItemStart />)
  await screen.findByRole('heading', { name: 'Reading the items' })
  expect(screen.getByRole('button', { name: 'Edit context and start again' })).toBeDisabled()
  expect(screen.queryByLabelText('Answer requirements')).not.toBeInTheDocument()
  expect(api.cancelRun).not.toHaveBeenCalled()
})

it('allows an unavailable catalog to proceed only through an explicitly confirmed upload', async () => {
  vi.mocked(api.getDirectSetup).mockResolvedValue({ ...setup, sources: [], catalog: { ...setup.catalog, status: 'unavailable', message: 'Try an upload.' } })
  render(<DirectItemStart />)
  const user = userEvent.setup()
  fillContext()
  await user.click(screen.getByRole('button', { name: 'Find and confirm benchmark items' }))
  const file = new File(['content,reference_answer\nWhat is 2+2?,4'], 'mathdial.csv', { type: 'text/csv' })
  await user.upload(await screen.findByLabelText('Benchmark items file'), file)
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-upload')
  await user.click(screen.getByRole('button', { name: /Generate item criteria/ }))
  await screen.findByRole('heading', { name: 'Your criteria are ready' })
  expect(api.createDirectRun).toHaveBeenCalledWith(context, { benchmark_confirmed: true, items_file: file }, 'sk-upload')
})
