import { beforeEach, expect, it, vi } from 'vitest'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemAnalysis } from './ItemAnalysis'
import * as api from './api'
import type { AnalysisRun, AssessmentReference, AssessmentSetup, SourceDiscovery } from './types'

vi.mock('./api', async original => ({ ...await original<typeof import('./api')>(),
  getAssessment: vi.fn(), createAssessmentRun: vi.fn(), getRun: vi.fn(), classify: vi.fn(), cancelRun: vi.fn(),
  getCatalog: vi.fn(), createRun: vi.fn(), searchSources: vi.fn(),
}))

const assessment: AssessmentReference = { kind: 'run', id: 'my-assessment' }
const storageKey = 'item_analysis_run_v1:run:my-assessment'
const access = { run_id: 'item-run', run_secret: 'private-token' }
const revision = 'a'.repeat(40)
const sourceId = `databank:${revision}:mmlu`
const setup: AssessmentSetup = {
  assessment: { ...assessment, benchmark: 'MMLU', deployment: 'A biology tutor for adult learners in Kenya.' },
  benchmark_identity: { name: 'MMLU', full_name: null, aliases: [], paper_urls: ['https://arxiv.org/abs/2009.03300'], source_urls: [], year: '2020', languages: ['English'], version: null, evidence: {} },
  catalog: { status: 'ready', message: 'Current catalog.', repo: 'aims-foundations/measurement-db-pp', revision, requires_confirmation: true },
  sources: [{ id: sourceId, benchmark: 'mmlu', title: 'MMLU', item_count: 14015, available: true, source_label: 'Data Bank MMLU snapshot',
    source_revision: revision, version: 'Original', split: 'test', testing_scope: '57 subjects', match_type: 'identifier',
    match_reasons: ['The paper identifier matches.'], conflicts: [], requires_confirmation: true }],
  checkpoint_size: 100, upload: { max_bytes: 10485760, max_items: 50000, formats: ['csv', 'json'] },
}
const ready: AnalysisRun = {
  run_id: access.run_id, assessment: setup.assessment, status: 'ready', message: 'Review the criteria.',
  example: { id: 'mmlu', title: 'MMLU', benchmark: 'mmlu', deployment: setup.assessment.deployment,
    item_count: 14015, available: true, description: 'This assessment’s items.', source_label: 'Pinned MMLU snapshot' },
  spec: { benchmark: 'mmlu', deployment: setup.assessment.deployment, classifiers: [] },
  summary: null, processed: 0, total: 14015, complete: 0, errors: 0, items: [],
  pagination: { page: 1, total_pages: 701 }, usage: { input_tokens: 0, output_tokens: 0 }, can_continue: false, scope: null,
}

beforeEach(() => {
  vi.resetAllMocks()
  sessionStorage.clear()
  vi.mocked(api.getAssessment).mockResolvedValue(setup)
  vi.mocked(api.createAssessmentRun).mockResolvedValue({ ...ready, ...access })
  vi.mocked(api.getRun).mockResolvedValue(ready)
  vi.mocked(api.searchSources).mockResolvedValue(setup)
})

it('continues the displayed assessment without choosing another deployment or starting calls automatically', async () => {
  const user = userEvent.setup()
  const onStatusChange = vi.fn()
  render(<ItemAnalysis assessment={assessment} onStatusChange={onStatusChange} />)
  expect(await screen.findByRole('heading', { name: 'Continue with MMLU' })).toBeVisible()
  expect(api.getCatalog).not.toHaveBeenCalled()
  expect(screen.queryByLabelText('Benchmark and assessment context')).not.toBeInTheDocument()
  expect(screen.queryByRole('radio', { name: /Use supplied criteria/ })).not.toBeInTheDocument()
  await user.click(screen.getByText('Deployment context carried forward'))
  expect(screen.getByText(setup.assessment.deployment)).toBeVisible()
  expect(onStatusChange).toHaveBeenLastCalledWith('pending')
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  expect(screen.getByText('The paper identifier matches.')).toBeVisible()
  expect(screen.getByRole('link', { name: /aims-foundations\/measurement-db-pp/ })).toHaveAttribute('href', 'https://huggingface.co/datasets/aims-foundations/measurement-db-pp')
  expect(screen.getByText('57 subjects')).toBeVisible()
  fireEvent.submit(screen.getByRole('heading', { name: 'Continue with MMLU' }).closest('form')!)
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-private')
  await user.click(screen.getByRole('button', { name: 'Generate item criteria' }))
  await screen.findByRole('heading', { name: 'Your criteria are ready' })
  expect(api.createAssessmentRun).toHaveBeenCalledWith(assessment, { source_id: sourceId, source_revision: revision, benchmark_confirmed: true }, 'sk-private')
  expect(api.classify).not.toHaveBeenCalled()
  expect(onStatusChange).toHaveBeenLastCalledWith('in_progress')
  expect(JSON.parse(sessionStorage.getItem(storageKey)!)).toEqual(access)
  expect(sessionStorage.getItem(storageKey)).not.toContain('sk-private')
})

it('supports a new benchmark through an uploaded dataset and carries the same assessment reference', async () => {
  vi.mocked(api.getAssessment).mockResolvedValue({ ...setup, assessment: { ...setup.assessment, benchmark: 'My new benchmark' }, sources: [] })
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  const file = new File(['[{"item_id":"q1","content":"Question","reference_answer":"Answer"}]'], 'items.json', { type: 'application/json' })
  await user.upload(await screen.findByLabelText('Benchmark items file'), file)
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-upload')
  await user.click(screen.getByRole('button', { name: 'Generate item criteria' }))
  await screen.findByRole('heading', { name: 'Your criteria are ready' })
  expect(api.createAssessmentRun).toHaveBeenCalledWith(assessment, { items_file: file, benchmark_confirmed: true }, 'sk-upload')
})

it('offers upload when the matching configured snapshot is unavailable', async () => {
  vi.mocked(api.getAssessment).mockResolvedValue({ ...setup, sources: [{ ...setup.sources[0], available: false, unavailable_reason: 'Server access is missing.' }] })
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  expect(await screen.findByText('Server access is missing.')).toBeVisible()
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeDisabled()
  await user.click(screen.getByRole('radio', { name: /Upload the benchmark/ }))
  expect(screen.getByLabelText('Benchmark items file')).toBeVisible()
  expect(screen.getByRole('radio', { name: /Upload the benchmark/ })).toBeChecked()
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeDisabled()
  expect(screen.queryByRole('button', { name: 'Generate item criteria' })).not.toBeInTheDocument()
})

it('requires selecting the uploaded dataset again after restarting the item stage', async () => {
  vi.mocked(api.getAssessment).mockResolvedValue({ ...setup, sources: [] })
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  await user.upload(await screen.findByLabelText('Benchmark items file'), new File(['[{"content":"Question"}]'], 'items.json', { type: 'application/json' }))
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-first')
  await user.click(screen.getByRole('button', { name: 'Generate item criteria' }))
  await user.click(await screen.findByRole('button', { name: 'Start a new analysis' }))
  expect(await screen.findByLabelText('Benchmark items file')).toHaveValue('')
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeDisabled()
  expect(api.createAssessmentRun).toHaveBeenCalledTimes(1)
})

it('restores the same assessment’s checkpoint and completes only after the full dataset is classified', async () => {
  sessionStorage.setItem(storageKey, JSON.stringify(access))
  const checkpoint: AnalysisRun = { ...ready, status: 'checkpoint', processed: 100, complete: 100, can_continue: true, scope: 'pilot' }
  vi.mocked(api.getRun).mockResolvedValue(checkpoint)
  const onStatusChange = vi.fn()
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} onStatusChange={onStatusChange} />)
  await screen.findByRole('heading', { name: 'Pause here for a human review' })
  expect(api.getAssessment).not.toHaveBeenCalled()
  expect(onStatusChange).toHaveBeenLastCalledWith('in_progress')
  expect(screen.getByLabelText('OpenAI API key')).toHaveValue('')
  const completed: AnalysisRun = { ...ready, status: 'complete', processed: ready.total, complete: ready.total, scope: 'all' }
  vi.mocked(api.classify).mockResolvedValue(completed)
  vi.mocked(api.getRun).mockResolvedValue(completed)
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-returned')
  await user.click(screen.getByRole('button', { name: 'Continue through all items' }))
  await waitFor(() => expect(onStatusChange).toHaveBeenLastCalledWith('complete'))
  expect(api.classify).toHaveBeenCalledWith(access, 'all', 'sk-returned')
})

it('keeps failed items incomplete even if the provider reports a completed run', async () => {
  sessionStorage.setItem(storageKey, JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'complete', processed: ready.total, complete: ready.total - 1, errors: 1 })
  const onStatusChange = vi.fn()
  render(<ItemAnalysis assessment={assessment} onStatusChange={onStatusChange} />)
  await screen.findByRole('heading', { name: 'Some items still need classification' })
  expect(onStatusChange).toHaveBeenLastCalledWith('in_progress')
})

it('isolates saved analyses and state when switching between benchmark reports', async () => {
  sessionStorage.setItem(storageKey, JSON.stringify(access))
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify({ run_id: 'unrelated-legacy', run_secret: 'legacy-token' }))
  const view = render(<ItemAnalysis assessment={assessment} />)
  await screen.findByRole('heading', { name: 'Your criteria are ready' })
  const other = { kind: 'gallery' as const, id: 'another-report' }
  vi.mocked(api.getAssessment).mockResolvedValue({ ...setup, assessment: { ...setup.assessment, ...other, benchmark: 'Another benchmark' }, sources: [] })
  view.rerender(<ItemAnalysis assessment={other} />)
  await screen.findByRole('heading', { name: 'Continue with Another benchmark' })
  expect(screen.queryByRole('heading', { name: 'Your criteria are ready' })).not.toBeInTheDocument()
  expect(api.getRun).toHaveBeenCalledTimes(1)
})

it('rejects a saved token pointing to another assessment before displaying its items', async () => {
  sessionStorage.setItem(storageKey, JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, assessment: { ...setup.assessment, id: 'other-report' } })
  render(<ItemAnalysis assessment={assessment} />)
  expect(await screen.findByRole('alert')).toHaveTextContent('This run is no longer available')
  expect(screen.queryByRole('heading', { name: 'Your criteria are ready' })).not.toBeInTheDocument()
  expect(api.classify).not.toHaveBeenCalled()
})

it('requires confirmation again when choosing another benchmark snapshot', async () => {
  const other = { ...setup.sources[0], id: 'databank:other:mmlu-v2', title: 'MMLU updated', source_revision: 'b'.repeat(40), version: 'Updated',
    match_type: 'related_name' as const, match_reasons: ['A related benchmark name.'], conflicts: ['The version differs from the paper.'] }
  vi.mocked(api.getAssessment).mockResolvedValue({ ...setup, sources: [...setup.sources, other] })
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  await user.click(await screen.findByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-confirmed')
  await user.click(screen.getByRole('radio', { name: /MMLU updated/ }))
  expect(screen.queryByRole('button', { name: 'Generate item criteria' })).not.toBeInTheDocument()
  expect(screen.getByText('The version differs from the paper.')).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.click(screen.getByRole('button', { name: 'Generate item criteria' }))
  await waitFor(() => expect(api.createAssessmentRun).toHaveBeenCalledWith(assessment, { source_id: other.id, source_revision: other.source_revision, benchmark_confirmed: true }, 'sk-confirmed'))
})

it('clears confirmation when editing a search and requires confirmation of the manual result', async () => {
  const found = { ...setup.sources[0], id: 'databank:manual:mmlu', title: 'Manually found MMLU', match_type: 'search' as const, version: null, split: null, testing_scope: null }
  vi.mocked(api.searchSources).mockResolvedValue({ ...setup, sources: [found] })
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  await user.click(await screen.findByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('Search the Data Bank'), 'mmlu revised')
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeDisabled()
  await user.keyboard('{Enter}')
  expect(await screen.findByRole('radio', { name: /Manually found MMLU/ })).toBeChecked()
  expect(api.searchSources).toHaveBeenCalledWith(assessment, 'mmlu revised', expect.any(AbortSignal))
  expect(screen.getAllByText('Not recorded').length).toBeGreaterThanOrEqual(3)
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-manual')
  await user.click(screen.getByRole('button', { name: 'Generate item criteria' }))
  await waitFor(() => expect(api.createAssessmentRun).toHaveBeenCalledWith(assessment, { source_id: found.id, source_revision: found.source_revision, benchmark_confirmed: true }, 'sk-manual'))
})

it('requires reconfirming an uploaded file when it is replaced', async () => {
  vi.mocked(api.getAssessment).mockResolvedValue({ ...setup, sources: [] })
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  const first = new File(['[{"content":"First"}]'], 'first.json', { type: 'application/json' })
  const second = new File(['[{"content":"Second"}]'], 'second.json', { type: 'application/json' })
  await user.upload(await screen.findByLabelText('Benchmark items file'), first)
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-upload')
  await user.upload(screen.getByLabelText('Benchmark items file'), second)
  expect(screen.queryByRole('button', { name: 'Generate item criteria' })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.click(screen.getByRole('button', { name: 'Generate item criteria' }))
  await waitFor(() => expect(api.createAssessmentRun).toHaveBeenCalledWith(assessment, { items_file: second, benchmark_confirmed: true }, 'sk-upload'))
})

it('drops a hidden upload selection when changing between Data Bank and upload modes', async () => {
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  await user.click(await screen.findByRole('radio', { name: /Upload the benchmark/ }))
  await user.upload(screen.getByLabelText('Benchmark items file'), new File(['[{"content":"Question"}]'], 'items.json', { type: 'application/json' }))
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.click(screen.getByRole('radio', { name: /Choose from the Measurement Data Bank/ }))
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  await user.click(screen.getByRole('radio', { name: /Upload the benchmark/ }))
  expect(screen.getByLabelText('Benchmark items file')).toHaveValue('')
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeDisabled()
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
})

it.each(['ready', 'unavailable'] as const)('keeps upload and search available when the catalog is %s with no matches', async status => {
  vi.mocked(api.getAssessment).mockResolvedValue({ ...setup, sources: [], catalog: { ...setup.catalog, status, message: status === 'unavailable' ? 'Connection unavailable.' : 'No name matched.' } })
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  expect(await screen.findByLabelText('Benchmark items file')).toBeVisible()
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeDisabled()
  await user.click(screen.getByRole('radio', { name: /Choose from the Measurement Data Bank/ }))
  expect(screen.getByText(/No matching benchmark found/)).toBeVisible()
  await user.type(screen.getByLabelText('Search the Data Bank'), 'MMLU')
  await user.click(screen.getByRole('button', { name: 'Search Data Bank' }))
  expect(await screen.findByRole('radio', { name: /MMLU.*14,015 items/ })).toBeChecked()
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
})

it.each(['resolve', 'reject'])('ignores a stale search %s after a newer search has finished', async outcome => {
  let resolveOld!: (result: SourceDiscovery) => void
  let rejectOld!: (error: Error) => void
  const oldSearch = new Promise<SourceDiscovery>((resolve, reject) => { resolveOld = resolve; rejectOld = reject })
  const oldSource = { ...setup.sources[0], id: 'old', title: 'Old result' }
  const newSource = { ...setup.sources[0], id: 'new', title: 'Newest result' }
  vi.mocked(api.searchSources).mockReturnValueOnce(oldSearch).mockResolvedValueOnce({ ...setup, sources: [newSource] })
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  await user.type(await screen.findByLabelText('Search the Data Bank'), 'old')
  await user.click(screen.getByRole('button', { name: 'Search Data Bank' }))
  await user.clear(screen.getByLabelText('Search the Data Bank'))
  await user.type(screen.getByLabelText('Search the Data Bank'), 'new')
  await user.click(screen.getByRole('button', { name: 'Search Data Bank' }))
  expect(await screen.findByRole('radio', { name: /Newest result/ })).toBeChecked()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await act(async () => { if (outcome === 'resolve') resolveOld({ ...setup, sources: [oldSource] }); else rejectOld(new Error('Old request failed')); await Promise.resolve() })
  expect(screen.getByRole('radio', { name: /Newest result/ })).toBeChecked()
  expect(screen.queryByRole('radio', { name: /Old result/ })).not.toBeInTheDocument()
  expect(screen.queryByText('Old request failed')).not.toBeInTheDocument()
  expect(screen.getByLabelText('OpenAI API key')).toBeVisible()
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
})

it('can retry a failed search without creating a run', async () => {
  vi.mocked(api.searchSources).mockRejectedValueOnce(new Error('Search connection interrupted.')).mockResolvedValueOnce(setup)
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  await user.type(await screen.findByLabelText('Search the Data Bank'), 'MMLU')
  await user.click(screen.getByRole('button', { name: 'Search Data Bank' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Search connection interrupted.')
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeDisabled()
  await user.click(screen.getByRole('button', { name: 'Search Data Bank' }))
  expect(await screen.findByRole('radio', { name: /MMLU.*14,015 items/ })).toBeChecked()
  expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  expect(api.createAssessmentRun).not.toHaveBeenCalled()
})

it('refreshes and requires new confirmation when the server rejects a stale snapshot', async () => {
  const updatedSource = { ...setup.sources[0], id: 'databank:new:mmlu', source_revision: 'c'.repeat(40) }
  vi.mocked(api.getAssessment).mockResolvedValueOnce(setup).mockResolvedValueOnce({ ...setup, sources: [updatedSource] })
  vi.mocked(api.createAssessmentRun).mockRejectedValueOnce(new api.AnalysisApiError('The snapshot changed. Confirm the current snapshot.', 409))
  const user = userEvent.setup()
  render(<ItemAnalysis assessment={assessment} />)
  await user.click(await screen.findByRole('button', { name: 'Confirm benchmark' }))
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-stale')
  await user.click(screen.getByRole('button', { name: 'Generate item criteria' }))
  expect(await screen.findByText(updatedSource.source_revision)).toBeVisible()
  expect(screen.getByRole('alert')).toHaveTextContent('The snapshot changed.')
  expect(screen.queryByRole('button', { name: 'Generate item criteria' })).not.toBeInTheDocument()
  expect(api.createAssessmentRun).toHaveBeenCalledTimes(1)
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Generate item criteria' })).toBeEnabled()
})
