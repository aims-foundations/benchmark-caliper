import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemAnalysis } from './ItemAnalysis'
import * as api from './api'
import type { AnalysisRun, Catalog } from './types'
import { DEMO_ITEM_ANALYSIS_SPEC } from '../demo/itemAnalysisFixture'

vi.mock('./api', async original => ({ ...await original<typeof import('./api')>(),
  getCatalog: vi.fn(), createRun: vi.fn(), getRun: vi.fn(), classify: vi.fn(), cancelRun: vi.fn(), download: vi.fn(), discardRun: vi.fn(), downloadPackage: vi.fn(),
}))

const example = { id: 'illustrative', title: 'Exam preparation example', description: 'Authored examples for demonstrating the workflow.', item_count: 10,
  benchmark: 'illustrative', deployment: 'Hindi-medium exam preparation.', source_label: 'Illustrative teaching items', available: true, supplied_spec_available: true }
const catalog: Catalog = { examples: [example], checkpoint_size: 100 }
const mmlu = { ...example, id: 'mmlu', title: 'MMLU · Hindi-medium exam preparation', item_count: 14015, benchmark: 'mmlu',
  description: 'MMLU items from measurement-db-pp.', source_label: 'measurement-db-pp · MMLU',
  source_revision: '1234567890abcdef1234567890abcdef12345678',
  source_url: 'https://huggingface.co/datasets/aims-foundations/measurement-db-pp/tree/1234567890abcdef1234567890abcdef12345678/mmlu' }
const gsm8k = { ...example, id: 'gsm8k', title: 'GSM8K · Math tutoring', benchmark: 'gsm8k', benchmark_title: 'GSM8K', assessment_title: 'Math tutoring',
  item_count: 1319, description: 'Grade-school math problems from GSM8K.', deployment: 'Support students learning multi-step arithmetic.',
  source_label: 'measurement-db-pp · GSM8K', supplied_spec_available: false, source_revision: 'abcdef1234567890abcdef1234567890abcdef12',
  source_url: 'https://huggingface.co/datasets/aims-foundations/measurement-db-pp/tree/abcdef1234567890abcdef1234567890abcdef12/gsm8k' }
const toxigenContexts = [
  { id: 'toxigen', assessment_title: 'Bangladesh clinical content moderation', deployment: 'Moderate content for a clinical service in Bangladesh.' },
  { id: 'toxigen-south-asia', assessment_title: 'South Asian academic toxicity research', deployment: 'Study toxicity in South Asian academic discourse.' },
].map(context => ({ ...example, ...context, title: `TOXIGEN · ${context.assessment_title}`, benchmark: 'toxigen', benchmark_title: 'TOXIGEN',
  item_count: 39011, description: 'TOXIGEN items paired with the original Caliper assessment for this use case.',
  source_label: 'aims-foundations/measurement-db-pp · toxigen/items.parquet · 39,011-item snapshot', supplied_spec_available: false,
  source_revision: '7a840c66f04393497c106289a1b8bbca8d107008',
  source_url: 'https://huggingface.co/datasets/aims-foundations/measurement-db-pp/blob/7a840c66f04393497c106289a1b8bbca8d107008/toxigen/items.parquet' }))
const access = { run_id: 'run-123', run_secret: 'private-run-token' }
const ready: AnalysisRun = {
  run_id: access.run_id, status: 'ready', message: 'Criteria are ready for inspection.', example,
  spec: { schema_version: 'caliper_item_spec_legacy_v1', fixed_catalog_version: 'caliper_induced_items_legacy_v1', benchmark: 'illustrative', deployment: example.deployment, classifiers: [{ id: 'IC.region_fit', component: 'input_content', operation: 'ordinal', applicable: true,
    criterion: 'Assess the item’s regional relevance.', ordinal_anchors: { '1': 'Region relevant', '2': 'Region neutral', '3': 'Region misaligned' } }] },
  summary: { total_items: 10, completed_items: 0, error_items: 0, pending_items: 10, complete_snapshot: false, classifiers: [] },
  processed: 0, total: 10, complete: 0, errors: 0, items: [{ item_id: 'example-1', content: 'What is 2 + 2?', reference_answer: '4', status: 'pending' }],
  pagination: { page: 1, total_pages: 1 }, usage: { input_tokens: 0, output_tokens: 0 }, can_continue: false, scope: null,
  model: { provider: 'openai', model_id: 'gpt-6-luna', reasoning_effort: 'low' },
}

beforeEach(() => {
  vi.clearAllMocks()
  sessionStorage.clear()
  localStorage.clear()
  vi.mocked(api.getCatalog).mockResolvedValue(catalog)
  vi.mocked(api.createRun).mockResolvedValue({ ...ready, ...access })
  vi.mocked(api.getRun).mockResolvedValue(ready)
})

afterEach(() => vi.restoreAllMocks())

async function openStep(user: ReturnType<typeof userEvent.setup>, step: number) {
  const navigation = await screen.findByRole('navigation', { name: 'Item analysis steps' })
  const link = navigation.querySelector(`a[href="#ia-step-${step}"]`)!
  await user.click(link)
}

async function openExports(user: ReturnType<typeof userEvent.setup>) {
  await screen.findByRole('heading', { name: 'Python checks passed for the saved specification' })
  await openStep(user, 6)
}


it('returns to durable results without model calls and exposes readable report, package and blind worksheet actions', async () => {
  localStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await screen.findByRole('heading', { name: 'Python checks passed for the saved specification' })
  expect(api.getRun).toHaveBeenCalledWith(access, 1, expect.any(AbortSignal))
  expect(api.createRun).not.toHaveBeenCalled()
  expect(api.classify).not.toHaveBeenCalled()
  expect(screen.getByLabelText('OpenAI API key')).toHaveValue('')
  await openStep(user, 6)
  expect(screen.getByText(/No automatic expiry is configured for this run/)).toBeVisible()
  expect(screen.getByRole('button', { name: /View report/ })).toBeEnabled()
  expect(screen.getByRole('button', { name: /Download complete results package/ })).toBeEnabled()
  expect(screen.getByRole('button', { name: /Download blind review worksheet/ })).toBeEnabled()
  const files = screen.getByText('Individual files').closest('details')!
  expect(files.open).toBe(false)
  await user.click(screen.getByText('Individual files'))
  expect(files.open).toBe(true)
})

it('opens the report without an opener or secret URL and preserves the package filename', async () => {
  localStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  const tab = { opener: window, location: { replace: vi.fn() }, close: vi.fn() }
  vi.spyOn(window, 'open').mockReturnValue(tab as unknown as Window)
  vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:local-report')
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
  const filenames: string[] = []
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function (this: HTMLAnchorElement) { filenames.push(this.download) })
  vi.mocked(api.download).mockResolvedValue(new Blob(['<html>Saved report</html>'], { type: 'text/html' }))
  vi.mocked(api.downloadPackage).mockResolvedValue({ blob: new Blob(['ZIP fixture']), filename: 'MathDial-pilot-run-123.zip' })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await openExports(user)
  await user.click(screen.getByRole('button', { name: /View report/ }))
  expect(api.download).toHaveBeenCalledExactlyOnceWith(access, 'report')
  expect(window.open).toHaveBeenCalledWith('about:blank', '_blank')
  expect(tab.opener).toBeNull()
  expect(tab.location.replace).toHaveBeenCalledWith('blob:local-report')
  await user.click(screen.getByRole('button', { name: /Download complete results package/ }))
  expect(api.downloadPackage).toHaveBeenCalledExactlyOnceWith(access)
  expect(filenames).toEqual(['MathDial-pilot-run-123.zip'])
  await user.click(screen.getByRole('button', { name: /Download blind review worksheet/ }))
  expect(api.download).toHaveBeenLastCalledWith(access, 'review')
  expect(filenames).toEqual(['MathDial-pilot-run-123.zip', 'review.csv'])
  expect(api.classify).not.toHaveBeenCalled()
})

it('deletes saved results only after the discard action is confirmed and then clears both access stores', async () => {
  localStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.discardRun).mockResolvedValue(undefined)
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await openExports(user)
  await user.click(screen.getByText('Manage this saved analysis'))
  await user.click(screen.getByRole('button', { name: 'Discard saved analysis' }))
  expect(api.discardRun).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Keep analysis' }))
  expect(localStorage.getItem('item_analysis_run_v1')).not.toBeNull()
  await user.click(screen.getByRole('button', { name: 'Discard saved analysis' }))
  await user.click(screen.getByRole('button', { name: 'Delete analysis permanently' }))
  expect(api.discardRun).toHaveBeenCalledExactlyOnceWith(access)
  expect(localStorage.getItem('item_analysis_run_v1')).toBeNull()
  expect(sessionStorage.getItem('item_analysis_run_v1')).toBeNull()
  expect(await screen.findByRole('combobox', { name: 'Benchmark and assessment context' })).toBeVisible()
})

it('defaults to real MMLU and exposes the pinned dataset source', async () => {
  // MMLU stays the default even if catalog ordering changes.
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, examples: [example, mmlu] })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  expect(await screen.findByRole('combobox', { name: 'Benchmark and assessment context' })).toHaveValue('mmlu')
  expect(screen.getByText('14,015 items')).toBeVisible()
  expect(screen.getByText('Optional pilot').nextElementSibling).toHaveTextContent('100 items')
  await user.click(screen.getByText('Dataset source and snapshot metadata'))
  expect(screen.getByRole('link', { name: /View dataset on Hugging Face/ })).toHaveAttribute('href', mmlu.source_url)
  expect(screen.getByText('1234567890ab')).toHaveAttribute('title', mmlu.source_revision)
  await user.click(screen.getByRole('button', { name: /Prepare shared context/ }))
  expect(api.createRun).toHaveBeenCalledWith('mmlu', 'generate', '')
})

it('keeps unavailable MMLU selected and explains server access instead of silently substituting teaching items', async () => {
  const unavailable_reason = 'The site maintainer must configure a Hugging Face token with access to measurement-db-pp.'
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, examples: [{ ...mmlu, available: false, unavailable_reason }, example] })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  const selector = await screen.findByRole('combobox', { name: 'Benchmark and assessment context' })
  expect(selector).toHaveValue('mmlu')
  expect(screen.getByText(unavailable_reason)).toBeVisible()
  expect(screen.queryByRole('button', { name: /Prepare shared context/ })).not.toBeInTheDocument()
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  expect(screen.getByText(/No Hugging Face key is needed from visitors/)).toBeVisible()
  expect(api.createRun).not.toHaveBeenCalled()
  await user.selectOptions(selector, 'illustrative')
  expect(screen.getByText('Full dataset size (prepared snapshot)').nextElementSibling).toHaveTextContent('10 items')
  await user.selectOptions(selector, 'mmlu')
  expect(screen.getByText(unavailable_reason)).toBeVisible()
})

it('preserves dataset provenance when restoring a prepared MMLU run', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, example: mmlu, total: mmlu.item_count })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await openExports(user)
  await user.click(screen.getByText('Run metadata and usage'))
  expect(screen.getByText(/Model: gpt-6-luna/)).toBeVisible()
  await openStep(user, 1)
  await user.click(screen.getByText('Dataset source and snapshot metadata'))
  expect(screen.getByRole('link', { name: /View dataset on Hugging Face/ })).toHaveAttribute('href', mmlu.source_url)
  expect(screen.getByText('1234567890ab')).toHaveAttribute('title', mmlu.source_revision)
})

it('selects another benchmark and prepares shared context without a key', async () => {
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, examples: [gsm8k, mmlu, example] })
  const selectedRun = { ...ready, example: gsm8k, total: gsm8k.item_count }
  vi.mocked(api.createRun).mockResolvedValue({ ...selectedRun, ...access })
  vi.mocked(api.getRun).mockResolvedValue(selectedRun)
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  const selector = await screen.findByRole('combobox', { name: 'Benchmark and assessment context' })
  expect(selector).toHaveValue('mmlu')
  await user.selectOptions(selector, 'gsm8k')
  expect(screen.getByText('1,319 items')).toBeVisible()
  expect(selector).toHaveDisplayValue(gsm8k.title)
  expect(screen.getByRole('button', { name: /Prepare shared context/ })).toBeEnabled()
  await user.click(screen.getByText('Dataset source and snapshot metadata'))
  expect(screen.getByText(gsm8k.deployment)).toBeVisible()
  expect(screen.getByRole('link', { name: /View dataset on Hugging Face/ })).toHaveAttribute('href', gsm8k.source_url)
  await user.click(screen.getByRole('button', { name: /Prepare shared context/ }))
  await screen.findByRole('heading', { name: 'Python checks passed for the saved specification' })
  expect(api.createRun).toHaveBeenCalledWith('gsm8k', 'generate', '')
  await openStep(user, 1)
  expect(screen.getByText(gsm8k.title)).toBeVisible()
  expect(screen.getByText('Assessment context: Math tutoring')).toBeVisible()
  expect(api.classify).not.toHaveBeenCalled()
})

it('restores the selected benchmark and assessment metadata from the run even when absent from the current catalog', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, examples: [mmlu, example] })
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, example: gsm8k, total: gsm8k.item_count })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await screen.findByText(gsm8k.title)
  await openStep(user, 1)
  expect(screen.getByText(gsm8k.title)).toBeVisible()
  expect(screen.getByText('Assessment context: Math tutoring')).toBeVisible()
  expect(screen.getByText(gsm8k.source_label)).toBeVisible()
  expect(screen.getByText('1,319 items')).toBeVisible()
  await openStep(user, 1)
  await user.click(screen.getByText('Dataset source and snapshot metadata'))
  expect(screen.getByText(gsm8k.deployment)).toBeVisible()
  expect(screen.getByRole('link', { name: /View dataset on Hugging Face/ })).toHaveAttribute('href', gsm8k.source_url)
  expect(screen.getByText('abcdef123456')).toHaveAttribute('title', gsm8k.source_revision)
  expect(api.createRun).not.toHaveBeenCalled()
})

it.each(toxigenContexts)('uses the selected TOXIGEN assessment ID when starting $id', async selected => {
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, examples: [mmlu, ...toxigenContexts, example] })
  const selectedRun = { ...ready, example: selected, total: selected.item_count,
    spec: { ...ready.spec!, benchmark: selected.benchmark, deployment: selected.deployment } }
  vi.mocked(api.createRun).mockResolvedValue({ ...selectedRun, ...access })
  vi.mocked(api.getRun).mockResolvedValue(selectedRun)
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  const selector = await screen.findByRole('combobox', { name: 'Benchmark and assessment context' })
  const otherContext = toxigenContexts.find(context => context.id !== selected.id)!
  await user.selectOptions(selector, otherContext.id)
  expect(selector).toHaveDisplayValue(otherContext.title)
  await user.click(screen.getByText('Dataset source and snapshot metadata'))
  expect(screen.getByText(otherContext.deployment)).toBeVisible()
  await user.selectOptions(selector, selected.id)
  expect(selector).toHaveDisplayValue(selected.title)
  expect((selector as HTMLSelectElement).selectedOptions[0].textContent).toContain(selected.assessment_title)
  expect(screen.getByText(selected.deployment)).toBeVisible()
  expect(screen.queryByText(otherContext.deployment)).not.toBeInTheDocument()
  expect(screen.getByText('39,011 items')).toBeVisible()
  expect(screen.getByText(selected.source_label)).toBeVisible()
  expect(screen.getByRole('link', { name: /View dataset on Hugging Face/ })).toHaveAttribute('href', selected.source_url)
  expect(screen.getByText('7a840c66f043')).toHaveAttribute('title', selected.source_revision)
  expect(screen.getByRole('button', { name: /Prepare shared context/ })).toBeEnabled()
  await user.click(screen.getByRole('button', { name: /Prepare shared context/ }))
  await screen.findByRole('heading', { name: 'Python checks passed for the saved specification' })
  expect(api.createRun).toHaveBeenCalledExactlyOnceWith(selected.id, 'generate', '')
  await openStep(user, 1)
  expect(screen.getByText(selected.title)).toBeVisible()
  expect(screen.getByText(`Assessment context: ${selected.assessment_title}`)).toBeVisible()
  expect(api.classify).not.toHaveBeenCalled()
})

it('prepares context without a key and keeps restored historical item labels readable', async () => {
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  expect(await screen.findByRole('button', { name: 'Prepare shared context' })).toBeEnabled()
  await user.click(screen.getByText('Dataset source and snapshot metadata'))
  expect(screen.getByText('Illustrative teaching items')).toBeVisible()
  expect(screen.queryByLabelText('OpenAI API key')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: /Prepare shared context/ }))
  await screen.findByRole('heading', { name: 'Python checks passed for the saved specification' })
  expect(api.createRun).toHaveBeenCalledWith('illustrative', 'generate', '')
  expect(api.classify).not.toHaveBeenCalled()
  expect(screen.getByRole('button', { name: 'Classify 10 items with GPT-6 Luna' })).toBeDisabled()
  expect(within(document.getElementById('ia-step-4')!).getAllByText('Pending').some(element => element.closest('summary'))).toBe(true)
  expect(screen.queryByRole('heading', { name: 'What the items show' })).not.toBeInTheDocument()
  await user.click(within(screen.getByRole('region', { name: 'Resulting classifier specification' })).getByText('Regional relevance'))
  expect(screen.getByText('Assess the item’s regional relevance.')).toBeVisible()
})

it('requires a key only for scoring and does not persist it', async () => {
  const user = userEvent.setup()
  vi.mocked(api.classify).mockResolvedValue({ ...ready, status: 'running', scope: 'pilot' })
  render(<ItemAnalysis />)
  await screen.findByRole('button', { name: 'Prepare shared context' })
  expect(screen.queryByText(/Claude|Sonnet|Haiku|Anthropic/)).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: /Prepare shared context/ }))
  await screen.findByRole('heading', { name: 'Python checks passed for the saved specification' })
  expect(api.createRun).toHaveBeenCalledWith('illustrative', 'generate', '')
  expect(api.classify).not.toHaveBeenCalled()
  expect(JSON.parse(localStorage.getItem('item_analysis_run_v1')!)).toEqual(access)
  expect(sessionStorage.getItem('item_analysis_run_v1')).toBeNull()
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-private')
  await user.click(screen.getByRole('button', { name: 'Classify 10 items with GPT-6 Luna' }))
  expect(api.classify).toHaveBeenCalledWith(access, 'pilot', 'sk-private')
  expect(localStorage.getItem('item_analysis_run_v1')).not.toContain('sk-private')
})

it('restores a checkpoint, requires key reentry, and continues through all remaining items', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  const checkpoint: AnalysisRun = { ...ready, status: 'checkpoint', processed: 100, complete: 100, total: 14015, can_continue: true, scope: 'pilot',
    spec: DEMO_ITEM_ANALYSIS_SPEC,
    summary: { ...ready.summary!, experiment: { classifier_count: 4, selected_items: 100,
      completed_item_classifier_judgments: 400, expected_item_classifier_judgments: 400 } },
    example: { ...example, item_count: 14015, source_label: 'measurement-db MMLU snapshot' } }
  vi.mocked(api.getRun).mockResolvedValue(checkpoint)
  vi.mocked(api.classify).mockResolvedValue({ ...checkpoint, status: 'running', scope: 'all', can_continue: false })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await screen.findByText('Pilot complete: 100/100 selected items classified.')
  await openStep(user, 4)
  expect(screen.getByText(/The remaining 13,915 items are outside this pilot/)).toHaveTextContent('Classifying them is optional.')
  expect(screen.getByRole('button', { name: /Download blind review worksheet/ })).toBeEnabled()
  expect(api.classify).not.toHaveBeenCalled()
  await openStep(user, 1)
  expect(screen.getByText('measurement-db MMLU snapshot')).toBeVisible()
  await openStep(user, 4)
  expect(screen.getByLabelText('OpenAI API key')).toHaveValue('')
  expect(screen.getByRole('button', { name: 'Continue through all items' })).toBeDisabled()
  expect(screen.getByText(/55,660 primary GPT-6 Luna classifier requests remain/)).toBeVisible()
  await user.type(screen.getByLabelText('OpenAI API key'), 'sk-returned')
  await user.click(screen.getByRole('button', { name: 'Continue through all items' }))
  expect(api.classify).toHaveBeenCalledWith(access, 'all', 'sk-returned')
  expect(api.createRun).not.toHaveBeenCalled()
})

it('uses the saved per-classifier progress to estimate retry calls', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'failed', spec: DEMO_ITEM_ANALYSIS_SPEC,
    processed: 10, complete: 9, errors: 1, completed_judgments: 39,
    remaining_judgments: { pilot: 1, all: 1 } })
  render(<ItemAnalysis />)
  expect(await screen.findByText(/1 primary GPT-6 Luna classifier requests remain/)).toBeVisible()
  expect(screen.getByText(/Each item uses 4 separate requests/)).toBeVisible()
  expect(screen.getByText(/Classification pauses after this selection/)).toHaveTextContent('Saved judgments are reused.')
  expect(screen.getByRole('button', { name: 'Resume classification' })).toBeDisabled()
})

it('measures progress by saved judgments while the last item is still being classified', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'running', spec: DEMO_ITEM_ANALYSIS_SPEC,
    scope: 'pilot', processed: 10, complete: 9, completed_judgments: 39 })
  render(<ItemAnalysis />)
  const progress = await screen.findByRole('progressbar', { name: 'Classification progress' })
  expect(progress).toHaveAttribute('max', '40')
  expect(progress).toHaveAttribute('value', '39')
  expect(screen.getByText('Saved classifier judgments').parentElement).toHaveTextContent('39Saved classifier judgments')
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
  await screen.findByText(/Classification paused: 0\/10 selected items fully classified/)
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
  await screen.findByRole('combobox', { name: 'Benchmark and assessment context' })
  expect(sessionStorage.getItem('item_analysis_run_v1')).toBeNull()
  expect(api.createRun).not.toHaveBeenCalled()
  expect(api.classify).not.toHaveBeenCalled()
})

it('shows one safe initialization error and its reference without retrying paid work automatically', async () => {
  vi.useFakeTimers()
  try {
    const message = 'The criteria could not be generated from the available evidence. Start a new analysis to retry.'
    const olderError = 'Older provider error detail.'
    sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
    vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'failed', spec: null, summary: null, message, error: olderError,
      failure: { stage: 'specification', code: 'evidence', message } })
    render(<ItemAnalysis />)
    await act(async () => {})
    expect(screen.getByRole('heading', { name: 'Python checks did not pass' })).toBeVisible()
    expect(screen.getAllByText(message)).toHaveLength(1)
    expect(screen.queryByText(olderError)).not.toBeInTheDocument()
    expect(screen.getByText('specification/evidence').closest('details')).toHaveTextContent('Preparation error referencespecification/evidence')
    expect(screen.getByRole('button', { name: 'Start a new analysis', hidden: true })).toBeEnabled()
    expect(screen.queryByRole('button', { name: 'Resume classification' })).not.toBeInTheDocument()
    await act(async () => { await vi.advanceTimersByTimeAsync(30000) })
    expect(api.getRun).toHaveBeenCalledTimes(1)
    expect(api.createRun).not.toHaveBeenCalled()
    expect(api.classify).not.toHaveBeenCalled()
  } finally { vi.useRealTimers() }
})

it.each([undefined, null])('renders older failed runs without failure metadata (%s) once', async failure => {
  const message = 'Criteria generation failed. Start a new analysis to retry.'
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'failed', spec: null, summary: null, message, error: message, failure })
  render(<ItemAnalysis />)
  await screen.findByRole('heading', { name: 'Validation outcome not yet available' })
  expect(screen.getAllByText(message)).toHaveLength(1)
  expect(screen.queryByText(/Error reference:/)).not.toBeInTheDocument()
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
  await openStep(user, 5)
  expect(screen.getByText('7 known labels · 2 unknown · 0 invalid')).toBeVisible()
  expect(screen.getByText('71.4%')).toBeVisible()
  await user.click(screen.getByText('Excluded processing counts'))
  expect(screen.getByText('1 failed · 0 invalid · 0 pending')).toBeVisible()
  await user.click(screen.getByText('What is 2 + 2?', { selector: 'strong' }))
  expect(screen.getByText('Arithmetic does not require regional knowledge.')).toBeVisible()
  await user.click(screen.getByText('Evidence and full explanation'))
  expect(screen.getByText('2 + 2')).toBeVisible()
  await waitFor(() => expect(screen.queryByRole('button', { name: 'Continue through all items' })).not.toBeInTheDocument())
})

it('withholds stale aggregate statistics and exports while item classification is running', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'running', processed: 2, complete: 2 })
  render(<ItemAnalysis />)
  await screen.findByText(/Classifying the selected pilot/)
  expect(screen.queryByRole('heading', { name: 'What the items show' })).not.toBeInTheDocument()
  const user = userEvent.setup()
  await openStep(user, 5)
  expect(screen.getByText(/Summary findings update when the current phase pauses or finishes/)).toBeVisible()
  await openStep(user, 6)
  await user.click(screen.getByText('Individual files'))
  expect(screen.getByRole('button', { name: /Item labels CSV/ })).toBeDisabled()
  expect(screen.getByRole('button', { name: /Criteria JSON/ })).toBeEnabled()
})

it('renders structured benchmark conversations and objects with live item judgments', async () => {
  sessionStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  const question = { question: 'Which response is appropriate?', options: ['Offer help', 'Ignore the request'] }
  vi.mocked(api.getRun).mockResolvedValue({ ...ready, status: 'running', processed: 2, complete: 2,
    items: [
      { ...ready.items[0], item_id: 'toxigen-chat', content: [
        { role: 'system', content: 'Assess the message for toxicity.' },
        { role: 'user', content: 'Thank you for your help.' },
      ], status: 'complete', labels: { 'IC.region_fit': { label: 2, justification: 'This conversation is region neutral.', evidence: ['Thank you for your help.'] } } },
      { ...ready.items[0], item_id: 'structured-question', content: question, status: 'complete' },
      { ...ready.items[0], item_id: 'plain-text', content: 'An ordinary text item.' },
    ] })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await screen.findByText(/Classifying the selected pilot/)
  const chat = screen.getByText('toxigen-chat').closest<HTMLDetailsElement>('details.ia-item')!
  await user.click(within(chat).getByText(/system:/, { selector: 'strong' }))
  expect(chat.querySelector('.ia-item-text')).toHaveTextContent('system: Assess the message for toxicity. user: Thank you for your help.')
  expect(within(chat).getByText('2 · Region neutral')).toBeVisible()
  expect(within(chat).getByText('This conversation is region neutral.')).toBeVisible()
  await user.click(within(chat).getByText('Evidence and full explanation'))
  expect(within(chat).getByText('Thank you for your help.', { selector: 'li' })).toBeVisible()
  const structured = screen.getByText('structured-question').closest<HTMLDetailsElement>('details.ia-item')!
  await user.click(within(structured).getByText(/Which response is appropriate/, { selector: 'strong' }))
  expect(structured.querySelector('.ia-item-text')?.textContent).toBe(JSON.stringify(question, null, 2))
  expect(screen.getByText('An ordinary text item.', { selector: 'strong' })).toBeVisible()
  expect(screen.getByRole('progressbar', { name: 'Classification progress' })).toHaveAttribute('value', '2')
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
