import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemReview } from './ItemReview'
import * as api from './api'

vi.mock('./api', async importOriginal => ({
  ...await importOriginal<typeof import('./api')>(),
  getCatalog: vi.fn(), startReview: vi.fn(), startGrounding: vi.fn(), getReview: vi.fn(), cancelReview: vi.fn(), getReviewExport: vi.fn(),
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
const medicalDeployment: api.Deployment = {
  task: '  A medical study assistant.\n', users: 'Medical students.', inputs: 'Clinical vignettes.',
  outputs: 'A short answer.', success: 'Choose initial management.',
  constraints: 'Include at least three cases constrained by allergies.',
}
const supported = (text: string, answer_id: keyof api.Deployment, quote: string): api.SupportedText => ({ text, evidence: [{ answer_id, quote }] })
const extracted: api.RequirementsReview = {
  run_id: 'test-run', mode: 'requirements', status: 'completed', message: 'Requirements extracted and evidence checked.',
  model: 'gpt-6-luna', reasoning_effort: 'high', deployment: medicalDeployment, extraction: null, usage: {},
  requirements: {
    workflow: supported('Medical study assistance', 'task', 'A medical study assistant.'),
    primary_user: supported('Medical students', 'users', 'Medical students.'),
    input_types: supported('Clinical case text', 'inputs', 'Clinical vignettes.'),
    output_types: supported('Short answers', 'outputs', 'A short answer.'),
    authority: { text: null, evidence: [] },
    task_facets: [{ facet_id: 'management', task: supported('Choose the indicated initial management', 'success', 'Choose initial management.'),
      required_input_evidence: supported('Clinical vignette', 'inputs', 'Clinical vignettes.'),
      required_output_behavior: supported('A concise answer', 'outputs', 'A short answer.'), essential: true }],
    coverage_requirements: [{ facet_ids: ['management'], minimum_items: 3,
      requirement: supported('Management cases where allergies constrain the choice', 'constraints', 'Include at least three cases constrained by allergies.') }],
    unresolved_details: ['The level of human oversight is unspecified.'],
  },
}
const grounded: api.GroundingReview = {
  ...extracted, run_id: 'ground-run', mode: 'grounding', source_run_id: 'test-run', message: 'O*NET mappings completed and evidence checked.',
  grounding: {
    retrieval: { method: 'dense_bm25_rrf' },
    mapping: { version: 1, model: 'gpt-6-luna', reasoning_effort: 'high', max_output_tokens: 25000, prompt: 'Map applicable passages.', output_schema: {} },
    facets: [{ facet_id: 'management', query: 'Choose the indicated initial management', status: 'complete',
      candidates: [{ doc_id: 'dwa:treatment', name: 'Evaluate treatment options', text: 'Assess the risks and benefits of therapies.', kind: 'dwa', occupation_id: '29-1229.01', dense_rank: 1, bm25_rank: 2, rrf_score: 0.03 },
        { doc_id: 'dwa:staff', name: 'Manage clinical staff', text: 'Supervise staff.', kind: 'dwa', occupation_id: '29-1229.01', dense_rank: 2, bm25_rank: null, rrf_score: 0.016 }],
      mapping: { facet_id: 'management', records: [
        { record_id: 'dwa:treatment', supporting_passage: 'risks and benefits of therapies', applicability: 'partially_applicable', rationale: 'Useful treatment vocabulary within an educational task.', search_terms: ['treatment options', 'risks and benefits'] },
        { record_id: 'dwa:staff', supporting_passage: 'Supervise staff.', applicability: 'not_applicable', rationale: 'Staff supervision is outside the stated task.', search_terms: [] },
      ], refinements: [supported('Allergies constrain management choices', 'constraints', 'Include at least three cases constrained by allergies.')],
      unresolved_details: ['The catalog passage does not specify an educational level.'] },
    }],
  },
}

beforeEach(() => {
  vi.clearAllMocks()
  sessionStorage.clear()
  localStorage.clear()
  vi.mocked(api.getCatalog).mockResolvedValue(catalog)
  vi.mocked(api.startReview).mockResolvedValue({ run_id: 'test-run', run_secret: 'temporary-access' })
  vi.mocked(api.startGrounding).mockResolvedValue({ run_id: 'ground-run', run_secret: 'ground-access' })
  vi.mocked(api.getReview).mockResolvedValue(completed)
})
afterEach(() => vi.restoreAllMocks())

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

it('allows requirements extraction when dataset access is unavailable, while disabling item review', async () => {
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, dataset_access_configured: false })
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key'), 'sk-test-private')
  expect(screen.getByRole('alert')).toHaveTextContent('Dataset access is not configured on this server.')
  expect(screen.queryByLabelText('Hugging Face read token')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Continue to deployment' })).toBeEnabled()
  await user.click(screen.getByRole('button', { name: 'Continue to deployment' }))
  await user.click(screen.getByRole('button', { name: 'Use mathematics tutor example' }))
  expect(screen.getByRole('button', { name: 'Extract requirements' })).toBeEnabled()
  await user.click(screen.getByRole('button', { name: 'Review catalog and settings' }))
  expect(screen.getByRole('button', { name: 'Retrieve and assess shortlist' })).toBeDisabled()
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

it('extracts from the six answers without dataset access and displays evidence alongside read-only originals', async () => {
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, dataset_access_configured: false })
  vi.mocked(api.getReview).mockResolvedValue(extracted)
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key'), 'sk-test-private')
  await user.click(screen.getByRole('button', { name: 'Continue to deployment' }))
  for (const [field, answer] of Object.entries(medicalDeployment)) {
    await user.type(document.getElementById(`deployment-${field}`)!, answer)
  }
  expect(screen.getByText(/Extract requirements starts one paid GPT-6 Luna call/)).toBeVisible()
  expect(api.startReview).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Extract requirements' }))
  await screen.findByRole('heading', { name: 'Your extracted requirements are ready' })
  expect(api.startReview).toHaveBeenCalledWith({ deployment: medicalDeployment, mode: 'requirements' }, 'sk-test-private')
  expect(screen.queryByRole('heading', { name: 'Ranked shortlist items' })).not.toBeInTheDocument()
  expect(screen.queryByText(/no paid model calls yet/)).not.toBeInTheDocument()
  expect(screen.getByRole('heading', { name: 'Deployment summary' })).toBeVisible()
  expect(screen.getByText('Unknown — not specified in the answers.')).toBeVisible()
  const task = screen.getByRole('article', { name: 'Task 1' })
  expect(within(task).getByText('Essential')).toBeVisible()
  const sourceLink = within(task).getByRole('link', { name: 'Answer 5 · What counts as a successful response?' })
  expect(sourceLink).toHaveAttribute('href', '#original-answer-success')
  expect(within(task).getByText('Choose initial management.')).toBeVisible()
  const coverage = screen.getByRole('region', { name: 'Explicit coverage requirements' })
  expect(within(coverage).getByText(/Minimum items:/).parentElement).toHaveTextContent('Minimum items: 3')
  expect(within(coverage).getByRole('link', { name: 'Task 1' })).toHaveAttribute('href', '#facet-management')
  expect(screen.getByText('The level of human oversight is unspecified.')).toBeVisible()
  const original = document.getElementById('original-answer-task')!
  expect(original.querySelector('p')!.textContent).toBe(medicalDeployment.task)
  expect(screen.queryAllByRole('textbox')).toHaveLength(0)
  expect(sessionStorage.length).toBe(1)
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  expect(localStorage.length).toBe(0)
  await user.click(screen.getByRole('button', { name: 'Start another run' }))
  expect(await screen.findByLabelText('OpenAI API key')).toHaveValue('')
})

it('uses native required-field validation before starting extraction and keeps answers without length limits', async () => {
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key'), 'sk-test-private')
  await user.click(screen.getByRole('button', { name: 'Continue to deployment' }))
  await user.click(screen.getByRole('button', { name: 'Extract requirements' }))
  expect(api.startReview).not.toHaveBeenCalled()
  for (const input of screen.getAllByRole('textbox')) {
    expect(input).not.toHaveAttribute('minlength')
    expect(input).not.toHaveAttribute('maxlength')
  }
  expect(document.getElementById('deployment-success')).toBeRequired()
  expect(document.getElementById('deployment-constraints')).not.toBeRequired()
})

it('restores a running extraction and cancels it without displaying item-review progress', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...extracted, status: 'running', requirements: null, message: 'Extracting your deployment requirements.' })
  vi.mocked(api.cancelReview).mockResolvedValue({ ...extracted, status: 'cancelled', requirements: null, message: 'Extraction cancelled.' })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Extracting requirements' })
  expect(screen.getByRole('progressbar', { name: 'Requirements extraction in progress' })).toBeVisible()
  expect(screen.getByText(/This is one paid model call/)).toBeVisible()
  expect(screen.queryByText(/items shortlisted/)).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Stop extraction' }))
  await screen.findByRole('heading', { name: 'Extraction stopped' })
  expect(api.cancelReview).toHaveBeenCalledWith({ run_id: 'test-run', run_secret: 'temporary-access' })
  expect(screen.queryByRole('heading', { name: 'Deployment summary' })).not.toBeInTheDocument()
  expect(screen.getByRole('heading', { name: 'Original deployment answers' })).toBeVisible()
})

it('shows extraction validation failures with the original answers and a JSON export', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  const failed: api.RequirementsReview = { ...extracted, status: 'failed', requirements: null, message: 'A source quotation was not found in the cited answer.' }
  vi.mocked(api.getReview).mockResolvedValue(failed)
  const blob = new Blob([JSON.stringify(failed)], { type: 'application/json' })
  vi.mocked(api.getReviewExport).mockResolvedValue(blob)
  const create = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:requirements')
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Extraction interrupted' })
  expect(screen.getByRole('alert')).toHaveTextContent('A source quotation was not found in the cited answer.')
  expect(screen.queryByRole('heading', { name: 'Deployment summary' })).not.toBeInTheDocument()
  expect(screen.getByRole('heading', { name: 'Original deployment answers' })).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Download requirements JSON' }))
  expect(api.getReviewExport).toHaveBeenCalledWith({ run_id: 'test-run', run_secret: 'temporary-access' })
  expect(create).toHaveBeenCalledWith(blob)
  expect(click.mock.instances[0]).toHaveAttribute('download', 'requirements-test-run.json')
})

it('keeps extraction results visible when the JSON download fails', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getReview).mockResolvedValue(extracted)
  vi.mocked(api.getReviewExport).mockRejectedValue(new Error('Download unavailable. Please retry.'))
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your extracted requirements are ready' })
  await user.click(screen.getByRole('button', { name: 'Download requirements JSON' }))
  expect(screen.getByRole('alert')).toHaveTextContent('Download unavailable. Please retry.')
  expect(screen.getByRole('heading', { name: 'Task facets' })).toBeVisible()
  expect(screen.getByRole('button', { name: 'Download requirements JSON' })).toBeEnabled()
})

it('grounds retained requirements without dataset access and hands off only a fresh in-memory key', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, dataset_access_configured: false })
  vi.mocked(api.getReview).mockResolvedValueOnce(extracted).mockResolvedValue(grounded)
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your extracted requirements are ready' })
  expect(screen.getByRole('button', { name: 'Ground with O*NET' })).toBeDisabled()
  const key = screen.getByLabelText('OpenAI API key for O*NET mapping')
  expect(key).toHaveValue('')
  expect(key).toHaveAttribute('type', 'password')
  await user.type(key, 'sk-mapping-private')
  expect(screen.getByText(/one paid GPT-6 Luna mapping call per task facet/)).toBeVisible()
  expect(api.startGrounding).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Ground with O*NET' }))
  await screen.findByRole('heading', { name: 'Your O*NET grounding is ready' })
  expect(api.startGrounding).toHaveBeenCalledWith({ run_id: 'test-run', run_secret: 'temporary-access' }, 'sk-mapping-private')
  expect(api.startReview).not.toHaveBeenCalled()
  expect(api.getReview).toHaveBeenLastCalledWith({ run_id: 'ground-run', run_secret: 'ground-access' }, 1, expect.any(AbortSignal))
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(JSON.stringify({ run_id: 'ground-run', run_secret: 'ground-access' }))
  expect(localStorage.length).toBe(0)
  expect(screen.getByLabelText('OpenAI API key for O*NET mapping')).toHaveValue('')
  const mapping = screen.getByRole('article', { name: 'Mapping for task 1' })
  expect(within(mapping).getByRole('heading', { name: 'Evaluate treatment options' })).toBeVisible()
  expect(within(mapping).getByText('Partially applicable', { exact: false })).toBeVisible()
  expect(within(mapping).getByText('risks and benefits of therapies')).toBeVisible()
  expect(within(mapping).getByText('treatment options', { exact: true })).toBeVisible()
  expect(within(mapping).getByText('The catalog passage does not specify an educational level.')).toBeVisible()
  expect(within(mapping).getByRole('link', { name: /Answer 6/ })).toHaveAttribute('href', '#original-answer-constraints')
  await user.click(within(mapping).getByText('Records considered but not adopted (1)'))
  expect(within(mapping).getByText('Staff supervision is outside the stated task.')).toBeVisible()
  await user.click(within(mapping).getByText('Inspect retrieval candidates (2)'))
  expect(within(mapping).getByText(/Keyword rank: 2/)).toHaveTextContent('Meaning search rank: 1 · Keyword rank: 2 · Combined ranking score: 0.0300')
  expect(document.getElementById('original-answer-task')!.querySelector('p')!.textContent).toBe(medicalDeployment.task)
})

it('clears the earlier preview while connecting to the new grounding run', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getReview).mockResolvedValueOnce(extracted).mockImplementation(() => new Promise(() => {}))
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key for O*NET mapping'), 'sk-mapping-private')
  await user.click(screen.getByRole('button', { name: 'Ground with O*NET' }))
  await screen.findByRole('heading', { name: 'Connecting to your run' })
  expect(screen.queryByRole('heading', { name: 'Your extracted requirements are ready' })).not.toBeInTheDocument()
})

it('prevents restarting the workflow while a grounding request is being accepted', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getReview).mockResolvedValueOnce(extracted).mockResolvedValue(grounded)
  let accept!: (run: api.RunAccess) => void
  vi.mocked(api.startGrounding).mockImplementationOnce(() => new Promise(resolve => { accept = resolve }))
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key for O*NET mapping'), 'sk-mapping-private')
  await user.click(screen.getByRole('button', { name: 'Ground with O*NET' }))
  const restart = screen.getByRole('button', { name: 'Start another run' })
  expect(restart).toBeDisabled()
  expect(screen.getByLabelText('OpenAI API key for O*NET mapping')).toBeDisabled()
  await user.click(restart)
  expect(screen.getByRole('heading', { name: 'Your extracted requirements are ready' })).toBeVisible()
  expect(sessionStorage.getItem('item_review_run_v1')).toContain('test-run')
  accept({ run_id: 'ground-run', run_secret: 'ground-access' })
  await screen.findByRole('heading', { name: 'Your O*NET grounding is ready' })
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(JSON.stringify({ run_id: 'ground-run', run_secret: 'ground-access' }))
  expect(screen.getByRole('button', { name: 'Start another run' })).toBeEnabled()
})

it('explains how to proceed when extraction produced no task facets', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...extracted, requirements: { ...extracted.requirements!, task_facets: [], coverage_requirements: [] } })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your extracted requirements are ready' })
  expect(screen.queryByRole('button', { name: 'Ground with O*NET' })).not.toBeInTheDocument()
  expect(screen.queryByLabelText('OpenAI API key for O*NET mapping')).not.toBeInTheDocument()
  expect(screen.getByText(/No task facets were extracted to ground with O\*NET/)).toHaveTextContent('clarify the tasks in your deployment answers')
  await user.click(screen.getByRole('button', { name: 'Start another run' }))
  expect(await screen.findByLabelText('OpenAI API key')).toHaveValue('')
  expect(api.startGrounding).not.toHaveBeenCalled()
})

it('keeps extracted requirements available if grounding cannot start', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'test-run', run_secret: 'temporary-access' }))
  vi.mocked(api.getReview).mockResolvedValue(extracted)
  vi.mocked(api.startGrounding).mockRejectedValueOnce(new Error('This key is already running a job.'))
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key for O*NET mapping'), 'sk-mapping-private')
  await user.click(screen.getByRole('button', { name: 'Ground with O*NET' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('This key is already running a job.')
  expect(screen.getByRole('heading', { name: 'Your extracted requirements are ready' })).toBeVisible()
  expect(screen.getByRole('button', { name: 'Ground with O*NET' })).toBeEnabled()
  expect(sessionStorage.getItem('item_review_run_v1')).not.toContain('sk-mapping-private')
})

it('restores an active grounding run and preserves completed mappings when stopped', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'ground-run', run_secret: 'ground-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...grounded, status: 'running', message: 'Mapping task facets.' })
  vi.mocked(api.cancelReview).mockResolvedValue({ ...grounded, status: 'cancelled', message: 'O*NET grounding stopped.' })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Finding supporting O*NET passages' })
  expect(screen.getByRole('progressbar', { name: 'Task facets mapped' })).toHaveAttribute('value', '1')
  expect(screen.queryByRole('button', { name: 'Ground with O*NET' })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Stop grounding' }))
  await screen.findByRole('heading', { name: 'Grounding stopped' })
  expect(api.cancelReview).toHaveBeenCalledWith({ run_id: 'ground-run', run_secret: 'ground-access' })
  expect(screen.getByRole('article', { name: 'Mapping for task 1' })).toBeVisible()
  expect(screen.getByRole('button', { name: 'Ground with O*NET' })).toBeDisabled()
})

it('shows a failed grounding run and exports retained requirements with partial mappings', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'ground-run', run_secret: 'ground-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...grounded, status: 'failed', message: 'A supporting passage could not be verified.' })
  const blob = new Blob([JSON.stringify(grounded)], { type: 'application/json' })
  vi.mocked(api.getReviewExport).mockResolvedValue(blob)
  vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:grounding')
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Grounding interrupted' })
  expect(screen.getByRole('alert')).toHaveTextContent('A supporting passage could not be verified.')
  expect(screen.getByRole('heading', { name: 'Original deployment answers' })).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Download grounding JSON' }))
  expect(api.getReviewExport).toHaveBeenCalledWith({ run_id: 'ground-run', run_secret: 'ground-access' })
  expect(click.mock.instances[0]).toHaveAttribute('download', 'onet-grounding-ground-run.json')
  await user.type(screen.getByLabelText('OpenAI API key for O*NET mapping'), 'sk-retry')
  await user.click(screen.getByRole('button', { name: 'Ground with O*NET' }))
  expect(api.startGrounding).toHaveBeenCalledWith({ run_id: 'ground-run', run_secret: 'ground-access' }, 'sk-retry')
})

it('explicitly shows no adopted match while keeping the original task', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'ground-run', run_secret: 'ground-access' }))
  const facet = grounded.grounding!.facets[0]
  vi.mocked(api.getReview).mockResolvedValue({ ...grounded, grounding: { ...grounded.grounding!, facets: [
    { ...facet, mapping: { ...facet.mapping!, records: [], refinements: [] } },
  ] } })
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your O*NET grounding is ready' })
  expect(screen.getByText(/No applicable O\*NET record was adopted/)).toBeVisible()
  expect(screen.getByRole('article', { name: 'Task 1' })).toHaveTextContent('Choose the indicated initial management')
})
