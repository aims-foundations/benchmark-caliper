import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemReview } from './ItemReview'
import * as api from './api'

vi.mock('./api', async importOriginal => ({
  ...await importOriginal<typeof import('./api')>(),
  getCatalog: vi.fn(), startReview: vi.fn(), startGrounding: vi.fn(), startBenchmarkRetrieval: vi.fn(), startScreening: vi.fn(), startSelection: vi.fn(), getCandidates: vi.fn(), getReview: vi.fn(), cancelReview: vi.fn(), getReviewExport: vi.fn(),
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

const retrieved: api.BenchmarkRetrievalReview = {
  ...grounded, mode: 'retrieval', run_id: 'retrieve-run', source_run_id: 'ground-run', usage: {}, message: 'Benchmark retrieval complete.',
  retrieval: {
    policy: { method: 'dense_bm25_rrf', model: 'BAAI/bge-small-en-v1.5' },
    scope: { repo: 'benchmark-catalog', branches: { main: 'a' }, benchmarks: catalog.benchmarks.map(benchmark => benchmark.id), table_count: 4, source_rows: 1200, sample_only: false },
    stats: { source_rows: 1200, total_items: 1160, indexed_items: 1160, contentless_items: 0 },
    queries: [{ facet_id: 'management', query: 'Choose initial management. treatment options', onet_record_ids: ['dwa:treatment'], search_terms: ['treatment options'], refinements: grounded.grounding!.facets[0].mapping!.refinements, candidate_count: 750 }],
    queues: [{ queue_id: 'opaque/all', facet_id: 'management', source: null, item_count: 750 }, { queue_id: 'opaque/source', facet_id: 'management', source: 'matharena', item_count: 290 }],
  },
}
const candidates: api.CandidatePage = {
  queue_id: 'opaque/all', facet_id: 'management', page: 1, page_size: 20, total_pages: 38, total_items: 750,
  items: [{ item_id: 'item-1', evidence_hash: 'hash-1', question_text: 'What is the indicated first treatment?', search_text: '{"content":"What is the indicated first treatment?","grading_criterion":"Reference answer","item_id":"source-id","release":"2025"}', evidence: { item: { content: 'What is the indicated first treatment?', grading_criterion: 'Reference answer', item_id: 'source-id', release: '2025' } },
    sources: [{ benchmark: 'matharena', branch: 'main', commit: 'a', row: 12 }, { benchmark: 'coding', branch: 'main', commit: 'a', row: 23 }],
    rank: 1, dense_rank: 2, bm25_rank: 1, dense_score: 0.85, bm25_score: 4.5, rrf_score: 0.0325 }],
}

const rating = (score: number | null): api.ScreeningRating => ({ score, evidence: ['Reference answer'], justification: 'The supplied item evidence supports this rating.', information_gaps: score == null ? ['The response format is not established.'] : [] })
const assessment: api.ScreeningAssessment = {
  task: { status: 'matched', decision: 'Choose the indicated first treatment.', matched_facet_ids: ['management'], evidence: ['What is the indicated first treatment?'], justification: 'The item asks for a treatment decision.', information_gaps: [] },
  ratings: { input_ontology: rating(4), input_content: rating(4), input_form: rating(4), output_ontology: rating(4), output_content: rating(2), output_form: rating(null) },
  coverage: [{ requirement_index: 0, satisfied: true, evidence: ['Reference answer'], justification: 'The allergy requirement is met in this assessment fixture.', information_gaps: [] }],
}
const screeningItem: api.ScreenedItem = {
  ...candidates.items[0], acquisition: { queue_id: 'opaque/all', facet_id: 'management' }, status: 'complete', assessment,
  gate: { status: 'pass', reasons: ['A deployment task is matched and all four gate scores meet the threshold.'] }, screened_run_id: 'screen-run', usage: { input_tokens: 100, output_tokens: 200 },
}
const screened: api.ScreeningReview = {
  ...retrieved, mode: 'screening', run_id: 'screen-run', source_run_id: 'retrieve-run', message: 'Initial screening completed with one assessment error.', usage: { input_tokens: 400, output_tokens: 800 },
  screening: {
    policy: { version: 1, initial_budget: 50, gated_dimensions: ['input_ontology', 'input_content', 'input_form', 'output_ontology'], minimum_score: 3 },
    model: { version: 1, model: 'gpt-6-luna', reasoning_effort: 'high', max_output_tokens: 25000, prompt: 'Identify the tested task and rate all six dimensions.', output_schema: { title: 'ScreeningAssessment' } },
    allocation: { budget: 50, allocated: 4, shortfall: 46, allocations: [{ queue_id: 'opaque/all', facet_id: 'management', target: 50, allocated: 4 }],
      items: ['item-1', 'item-2', 'item-3', 'item-4'].map(item_id => ({ item_id, queue_id: 'opaque/all', facet_id: 'management' })) },
    items: [screeningItem,
      { ...screeningItem, item_id: 'item-2', assessment: { ...assessment, task: { ...assessment.task, status: 'no_match', decision: 'Recall an unrelated fact.', matched_facet_ids: [], justification: 'The tested task is outside the deployment.' },
        coverage: [{ ...assessment.coverage[0], satisfied: false, justification: 'This item does not test the required management task.' }] },
        gate: { status: 'fail', reasons: ['The actual task does not match a deployment task.'] } },
      { ...screeningItem, item_id: 'item-3', assessment: { ...assessment, ratings: { ...assessment.ratings, input_ontology: rating(null) }, coverage: [{ ...assessment.coverage[0], satisfied: null, information_gaps: ['No allergy evidence is supplied.'] }] },
        gate: { status: 'unresolved', reasons: ['Input ontology could not be established.'] } },
      { ...candidates.items[0], item_id: 'item-4', acquisition: { queue_id: 'opaque/all', facet_id: 'management' }, status: 'error', error: 'The response did not match the required schema.' },
    ],
  },
}

const selected: api.SelectionReview = {
  ...screened, mode: 'selection', run_id: 'select-run', source_run_id: 'screen-run', message: 'Collection selected with coverage gaps.', usage: {},
  selection_input: { allocated: 4, screened: 3, errors: 1, pending: 0 }, selection_run_id: 'select-run',
  selection: {
    policy: { version: 1, method: 'constrained_selection', quality: 'mean_four_gate_scores' }, limit: 30, eligible_count: 1, selected_count: 1, selected_item_ids: ['item-1'],
    items: [{ item_id: 'item-1', quality_score: 4, rating_sum: 16, matched_facet_ids: ['management'], coverage_requirement_indices: [0] }], total_quality: 4,
    task_coverage: [{ facet_id: 'management', minimum: 1, eligible_count: 1, selected_count: 1, shortfall: 0 }],
    quota_coverage: [{ requirement_index: 0, minimum_items: 3, eligible_count: 1, selected_count: 1, shortfall: 2 }],
    constraints_feasible: false, fully_satisfied: false, gaps: ['The allergy-constrained management requirement is short by 2 items.'], unresolved_requirement_indices: [],
    excluded_counts: { failed_gate: 1, unresolved_gate: 1, assessment_error: 1 }, solver: { status: 'optimal_partial' },
  },
}

beforeEach(() => {
  vi.clearAllMocks()
  sessionStorage.clear()
  localStorage.clear()
  vi.mocked(api.getCatalog).mockResolvedValue(catalog)
  vi.mocked(api.startReview).mockResolvedValue({ run_id: 'test-run', run_secret: 'temporary-access' })
  vi.mocked(api.startGrounding).mockResolvedValue({ run_id: 'ground-run', run_secret: 'ground-access' })
  vi.mocked(api.startBenchmarkRetrieval).mockResolvedValue({ run_id: 'retrieve-run', run_secret: 'retrieve-access' })
  vi.mocked(api.startScreening).mockResolvedValue({ run_id: 'screen-run', run_secret: 'screen-access' })
  vi.mocked(api.startSelection).mockResolvedValue({ run_id: 'select-run', run_secret: 'select-access' })
  vi.mocked(api.getCandidates).mockResolvedValue(candidates)
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

it('retrieves the whole main-branch bank after grounding without scope controls or another paid call', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'ground-run', run_secret: 'ground-access' }))
  vi.mocked(api.getReview).mockResolvedValueOnce(grounded).mockResolvedValue(retrieved)
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your O*NET grounding is ready' })
  expect(screen.getByText('3 benchmark collections · 1,200 source rows · whole bank')).toBeVisible()
  expect(screen.getByText(/Every field of every item row is included/)).toHaveTextContent('all benchmark collections and releases in scope')
  expect(screen.getByText(/Retrieval makes no paid model calls and needs no OpenAI key/)).toBeVisible()
  expect(screen.queryByRole('checkbox')).not.toBeInTheDocument()
  expect(screen.queryByRole('searchbox')).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Clear selection' })).not.toBeInTheDocument()
  await user.click(screen.getByText('Browse all 3 benchmark collections'))
  expect(screen.getByText('Customer Support')).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Retrieve benchmark items' }))
  await screen.findByRole('heading', { name: 'Your benchmark candidates are ready' })
  expect(api.startBenchmarkRetrieval).toHaveBeenCalledWith({ run_id: 'ground-run', run_secret: 'ground-access' })
  expect(api.startGrounding).not.toHaveBeenCalled()
  expect(api.startReview).not.toHaveBeenCalled()
  expect(screen.queryByLabelText('OpenAI API key for O*NET mapping')).not.toBeInTheDocument()
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(JSON.stringify({ run_id: 'retrieve-run', run_secret: 'retrieve-access' }))
  expect(localStorage.length).toBe(0)
  expect(screen.getByText(/1,160 searchable items/)).toHaveTextContent('0 items without searchable row data')
  expect(screen.getByText(/whole main-branch bank/)).toHaveTextContent('3 benchmark collections · 1,200 source rows')
  expect(screen.getByText(/These are retrieval ranks/)).toBeVisible()
  await user.click(screen.getByText('Task 1 · 750 candidates'))
  expect(screen.getByText('Choose initial management. treatment options')).toBeVisible()
  expect(screen.getByText('treatment options', { exact: true })).toBeVisible()
  expect(screen.getByText(/O\*NET records: dwa:treatment/)).toBeVisible()
})

it('browses private candidate pages and source queues with inspectable evidence and original ranking', async () => {
  const access = { run_id: 'retrieve-run', run_secret: 'retrieve-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  vi.mocked(api.getReview).mockResolvedValue(retrieved)
  vi.mocked(api.getCandidates).mockImplementation(async (_run, queueId, page = 1) => ({
    ...candidates, queue_id: queueId, page, items: candidates.items.map(item => ({ ...item, rank: page === 2 ? 21 : 1 })),
  }))
  const user = userEvent.setup()
  render(<ItemReview />)
  const first = await screen.findByRole('article', { name: 'Candidate 1' })
  expect(within(first).getByText('What is the indicated first treatment?')).toBeVisible()
  expect(within(first).getByText(/Sources:/).parentElement).toHaveTextContent('matharena, coding')
  expect(within(first).getByText(/Combined rank:/)).toHaveTextContent('Combined rank: 1 · Meaning search rank: 2 · Keyword rank: 1')
  await user.click(within(first).getByText('Inspect full item evidence and sources'))
  expect(within(first).getByText(/"grading_criterion": "Reference answer"/)).toBeVisible()
  expect(within(first).getByText(/"commit": "a"/)).toBeVisible()
  expect(within(first).getByRole('heading', { name: 'Full row text used for search' })).toBeVisible()
  expect(within(first).getByText(candidates.items[0].search_text)).toBeVisible()
  expect(screen.getByRole('button', { name: 'Previous candidates' })).toBeDisabled()
  await user.click(screen.getByRole('button', { name: 'Next candidates' }))
  await screen.findByRole('article', { name: 'Candidate 21' })
  expect(api.getCandidates).toHaveBeenLastCalledWith(access, 'opaque/all', 2, expect.any(AbortSignal))
  await user.selectOptions(screen.getByLabelText('Candidate queue'), 'opaque/source')
  await screen.findByRole('article', { name: 'Candidate 1' })
  expect(api.getCandidates).toHaveBeenLastCalledWith(access, 'opaque/source', 1, expect.any(AbortSignal))
  expect(screen.getByText('Page 1 of 38')).toBeVisible()
})

it('retains completed retrieval queues when stopped and retries the whole bank', async () => {
  const access = { run_id: 'retrieve-run', run_secret: 'retrieve-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  vi.mocked(api.getReview).mockResolvedValue({ ...retrieved, status: 'running', message: 'Searching remaining tasks.' })
  vi.mocked(api.cancelReview).mockResolvedValue({ ...retrieved, status: 'cancelled', message: 'Benchmark retrieval stopped.' })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Retrieving benchmark candidates' })
  expect(screen.getByRole('progressbar', { name: 'Task queries completed' })).toHaveAttribute('value', '1')
  expect(screen.queryByRole('button', { name: 'Retrieve benchmark items' })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Stop retrieval' }))
  await screen.findByRole('heading', { name: 'Retrieval stopped' })
  expect(api.cancelReview).toHaveBeenCalledWith(access)
  expect(screen.getByRole('article', { name: 'Candidate 1' })).toBeVisible()
  expect(screen.getByText('3 benchmark collections · 1,200 source rows · whole bank')).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Retrieve benchmark items' }))
  expect(api.startBenchmarkRetrieval).toHaveBeenCalledWith(access)
})

it('disables Step 4 when dataset access is unavailable and does not offer it for incomplete grounding', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'ground-run', run_secret: 'ground-access' }))
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, dataset_access_configured: false })
  vi.mocked(api.getReview).mockResolvedValue(grounded)
  const { unmount } = render(<ItemReview />)
  expect(await screen.findByRole('button', { name: 'Retrieve benchmark items' })).toBeDisabled()
  expect(screen.getByRole('alert')).toHaveTextContent('Dataset access is not configured')
  unmount()
  vi.mocked(api.getReview).mockResolvedValue({ ...grounded, status: 'cancelled' })
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Grounding stopped' })
  expect(screen.queryByRole('button', { name: 'Retrieve benchmark items' })).not.toBeInTheDocument()
})

it('keeps the grounding preview when retrieval cannot start', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'ground-run', run_secret: 'ground-access' }))
  vi.mocked(api.getReview).mockResolvedValue(grounded)
  vi.mocked(api.startBenchmarkRetrieval).mockRejectedValueOnce(new Error('The retrieval worker is busy.'))
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.click(await screen.findByRole('button', { name: 'Retrieve benchmark items' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('The retrieval worker is busy.')
  expect(screen.getByRole('heading', { name: 'Your O*NET grounding is ready' })).toBeVisible()
  expect(screen.getByRole('button', { name: 'Retrieve benchmark items' })).toBeEnabled()
  expect(sessionStorage.getItem('item_review_run_v1')).toContain('ground-access')
})

it('shows failures and exports the retained retrieval result without dropping original requirements', async () => {
  const access = { run_id: 'retrieve-run', run_secret: 'retrieve-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  vi.mocked(api.getReview).mockResolvedValue({ ...retrieved, status: 'failed', message: 'Index preparation failed.' })
  const blob = new Blob([JSON.stringify(retrieved)], { type: 'application/json' })
  vi.mocked(api.getReviewExport).mockResolvedValue(blob)
  vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:retrieval')
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Retrieval interrupted' })
  expect(screen.getByRole('alert')).toHaveTextContent('Index preparation failed.')
  expect(screen.getByRole('heading', { name: 'Original deployment answers' })).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Download retrieval JSON' }))
  expect(api.getReviewExport).toHaveBeenCalledWith(access)
  expect(click.mock.instances[0]).toHaveAttribute('download', 'benchmark-retrieval-retrieve-run.json')
})

it('retries a failed candidate page and explains an empty queue', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'retrieve-run', run_secret: 'retrieve-access' }))
  vi.mocked(api.getReview).mockResolvedValue(retrieved)
  vi.mocked(api.getCandidates).mockRejectedValueOnce(new Error('Candidate page unavailable.')).mockResolvedValueOnce({ ...candidates, items: [], total_items: 0, total_pages: 0 })
  const user = userEvent.setup()
  render(<ItemReview />)
  expect(await screen.findByRole('alert')).toHaveTextContent('Candidate page unavailable.')
  await user.click(screen.getByRole('button', { name: 'Retry loading candidates' }))
  expect(await screen.findByText('No candidates are available in this queue.')).toBeVisible()
  expect(screen.queryByRole('button', { name: 'Next candidates' })).not.toBeInTheDocument()
})

it('shows planned queries while the first index is preparing and statistics are not yet available', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'retrieve-run', run_secret: 'retrieve-access' }))
  const { candidate_count: _count, ...query } = retrieved.retrieval!.queries[0]
  vi.mocked(api.getReview).mockResolvedValue({ ...retrieved, status: 'preparing', message: 'Preparing the local index.',
    retrieval: { ...retrieved.retrieval!, stats: {}, queries: [query], queues: [] } })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Retrieving benchmark candidates' })
  expect(screen.getByText(/0 source rows read/)).toBeVisible()
  expect(screen.getByText('0 of 1 task queries completed.')).toBeVisible()
  expect(screen.getByRole('progressbar', { name: 'Task queries completed' })).toHaveAttribute('value', '0')
  await user.click(screen.getByText('Task 1 · Awaiting retrieval'))
  expect(screen.getByText('Choose initial management. treatment options')).toBeVisible()
  expect(api.getCandidates).not.toHaveBeenCalled()
  expect(screen.queryByText('No searchable candidates were found in the bank.')).not.toBeInTheDocument()
})

it('keeps rows without a labeled question inspectable through their complete search text and evidence', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'retrieve-run', run_secret: 'retrieve-access' }))
  vi.mocked(api.getReview).mockResolvedValue(retrieved)
  const searchText = '{"item_id":"unlabeled-case","clinical_context":"Risk assessment","release":"older-release"}'
  vi.mocked(api.getCandidates).mockResolvedValue({ ...candidates, items: [{ ...candidates.items[0], question_text: '', search_text: searchText,
    evidence: { item: { item_id: 'unlabeled-case', clinical_context: 'Risk assessment', release: 'older-release' } } }] })
  const user = userEvent.setup()
  render(<ItemReview />)
  const candidate = await screen.findByRole('article', { name: 'Candidate 1' })
  expect(within(candidate).getByText(/This item has no separately labeled question/)).toBeVisible()
  await user.click(within(candidate).getByText('Inspect full item evidence and sources'))
  expect(within(candidate).getByText(searchText)).toBeVisible()
  expect(within(candidate).getByText(/"release": "older-release"/)).toBeVisible()
})

it('starts initial screening only after a fresh-key submission and preserves private run access', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'retrieve-run', run_secret: 'retrieve-access' }))
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, dataset_access_configured: false })
  vi.mocked(api.getReview).mockResolvedValueOnce(retrieved).mockResolvedValue(screened)
  const user = userEvent.setup()
  render(<ItemReview />)
  const key = await screen.findByLabelText('OpenAI API key for initial screening')
  expect(key).toHaveValue('')
  expect(key).toHaveAttribute('type', 'password')
  expect(screen.getByRole('button', { name: 'Screen initial candidates' })).toBeDisabled()
  expect(screen.getByText(/Up to 50 distinct candidates/)).toHaveTextContent('distributed as evenly as the available task queues allow')
  await user.type(key, 'sk-screen-private')
  expect(api.startScreening).not.toHaveBeenCalled()
  expect(screen.getByText(/Starting authorizes up to 50 paid/)).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Screen initial candidates' }))
  await screen.findByRole('heading', { name: 'Your initial screening is ready' })
  expect(api.startScreening).toHaveBeenCalledWith({ run_id: 'retrieve-run', run_secret: 'retrieve-access' }, 'sk-screen-private')
  expect(api.startBenchmarkRetrieval).not.toHaveBeenCalled()
  expect(api.startGrounding).not.toHaveBeenCalled()
  expect(api.startReview).not.toHaveBeenCalled()
  expect(screen.getByLabelText('OpenAI API key for initial screening')).toHaveValue('')
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(JSON.stringify({ run_id: 'screen-run', run_secret: 'screen-access' }))
  expect(localStorage.length).toBe(0)
  expect(api.getReview).toHaveBeenLastCalledWith({ run_id: 'screen-run', run_secret: 'screen-access' }, 1, expect.any(AbortSignal))
})

it('shows actual task matching, six ratings, four-dimension gates, coverage, and assessment errors distinctly', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'screen-run', run_secret: 'screen-access' }))
  vi.mocked(api.getReview).mockResolvedValue(screened)
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your initial screening is ready' })
  expect(screen.getByText('Budget: 50 distinct items · Allocated: 4 · Shortfall: 46')).toBeVisible()
  expect(screen.getByText('Passed gate').parentElement).toHaveTextContent('1')
  expect(screen.getByText('Failed gate').parentElement).toHaveTextContent('1')
  expect(screen.getByText('Unresolved gate').parentElement).toHaveTextContent('1')
  expect(screen.getByText(/4 of 4 allocated items processed/)).toHaveTextContent('3 valid assessments · 1 assessment errors')
  const passed = screen.getByRole('article', { name: 'Screened item 1' })
  expect(within(passed).getByRole('heading', { name: 'Screening gate: Pass' })).toBeVisible()
  expect(within(passed).getByText('Output content').parentElement).toHaveTextContent('Reported dimension2 / 5')
  expect(within(passed).getByText('Output form').parentElement).toHaveTextContent('Reported dimensionUnknown')
  expect(within(passed).getAllByText('Gate dimension')).toHaveLength(4)
  expect(within(passed).getByText('Choose the indicated first treatment.')).toBeVisible()
  await user.click(within(passed).getByText('Inspect task interpretation and six validity ratings'))
  expect(within(passed).getByRole('heading', { name: 'Input ontology · 4 / 5' })).toBeVisible()
  expect(within(passed).getByRole('heading', { name: 'Output form · Unknown' })).toBeVisible()
  expect(within(passed).getByText('The response format is not established.')).toBeVisible()
  await user.click(within(passed).getByText('Inspect coverage requirements (1)'))
  expect(within(passed).getByRole('heading', { name: 'Coverage requirement 1 · Satisfied' })).toBeVisible()
  const failed = screen.getByRole('article', { name: 'Screened item 2' })
  expect(within(failed).getByText(/Acquired from:/).parentElement).toHaveTextContent('Task 1 queue')
  expect(within(failed).getByText(/Task match:/).parentElement).toHaveTextContent('No deployment task matched')
  expect(within(failed).getByRole('heading', { name: 'Screening gate: Fail' })).toBeVisible()
  const unresolved = screen.getByRole('article', { name: 'Screened item 3' })
  expect(within(unresolved).getByRole('heading', { name: 'Screening gate: Unresolved' })).toBeVisible()
  const errored = screen.getByRole('article', { name: 'Screened item 4' })
  expect(within(errored).getByRole('alert')).toHaveTextContent('The response did not match the required schema.')
  expect(within(errored).queryByRole('heading', { name: /Screening gate:/ })).not.toBeInTheDocument()
  expect(screen.queryByText(/confidence-adjusted/i)).not.toBeInTheDocument()
  expect(screen.getByText(/No final benchmark has been selected/)).toBeVisible()
})

it('retains completed screening assessments when stopped and continues only pending or errored items', async () => {
  const access = { run_id: 'screen-run', run_secret: 'screen-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  const partial: api.ScreeningReview = { ...screened, status: 'running', message: 'Screening initial items.', screening: { ...screened.screening!, items: [screeningItem] } }
  vi.mocked(api.getReview).mockResolvedValue(partial)
  vi.mocked(api.cancelReview).mockResolvedValue({ ...partial, status: 'cancelled', message: 'Initial screening stopped.' })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Screening initial candidates' })
  expect(screen.getByRole('progressbar', { name: 'Initial items processed' })).toHaveAttribute('value', '1')
  expect(screen.queryByRole('button', { name: 'Continue screening' })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Stop screening' }))
  await screen.findByRole('heading', { name: 'Screening stopped' })
  expect(api.cancelReview).toHaveBeenCalledWith(access)
  expect(screen.getByRole('article', { name: 'Screened item 1' })).toBeVisible()
  expect(screen.getByText(/1 completed assessments are retained/)).toHaveTextContent('up to 3 items')
  await user.type(screen.getByLabelText('OpenAI API key for initial screening'), 'sk-continue')
  await user.click(screen.getByRole('button', { name: 'Continue screening' }))
  expect(api.startScreening).toHaveBeenCalledWith(access, 'sk-continue')
})

it('does not offer another paid screening once every allocated item has a valid assessment', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'screen-run', run_secret: 'screen-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...screened, screening: { ...screened.screening!,
    allocation: { ...screened.screening!.allocation, allocated: 3, shortfall: 47 }, items: screened.screening!.items.slice(0, 3) } })
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your initial screening is ready' })
  expect(screen.getByRole('heading', { name: 'Screening gate: Fail' })).toBeVisible()
  expect(screen.getByRole('heading', { name: 'Screening gate: Unresolved' })).toBeVisible()
  expect(screen.queryByLabelText('OpenAI API key for initial screening')).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Continue screening' })).not.toBeInTheDocument()
})

it('requires a completed retrieval with available candidates before offering initial screening', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'retrieve-run', run_secret: 'retrieve-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...retrieved, status: 'cancelled' })
  const { unmount } = render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Retrieval stopped' })
  expect(screen.queryByRole('button', { name: 'Screen initial candidates' })).not.toBeInTheDocument()
  unmount()
  vi.mocked(api.getReview).mockResolvedValue({ ...retrieved, retrieval: { ...retrieved.retrieval!, queues: [] } })
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your benchmark candidates are ready' })
  expect(screen.queryByLabelText('OpenAI API key for initial screening')).not.toBeInTheDocument()
})

it('exports retained screening results and makes prompt, schema, and complete item evidence inspectable', async () => {
  const access = { run_id: 'screen-run', run_secret: 'screen-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  vi.mocked(api.getReview).mockResolvedValue({ ...screened, status: 'failed', message: 'The provider interrupted screening.' })
  const blob = new Blob([JSON.stringify(screened)], { type: 'application/json' })
  vi.mocked(api.getReviewExport).mockResolvedValue(blob)
  vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:screening')
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Screening interrupted' })
  const first = screen.getByRole('article', { name: 'Screened item 1' })
  await user.click(within(first).getByText('Inspect original row and sources'))
  expect(within(first).getByText(/"release": "2025"/)).toBeVisible()
  expect(within(first).getByText(candidates.items[0].search_text)).toBeVisible()
  await user.click(screen.getByText('Inspect screening prompt and output schema'))
  expect(screen.getByText('Identify the tested task and rate all six dimensions.')).toBeVisible()
  expect(screen.getByText(/"title": "ScreeningAssessment"/)).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Download screening JSON' }))
  expect(api.getReviewExport).toHaveBeenCalledWith(access)
  expect(click.mock.instances[0]).toHaveAttribute('download', 'initial-screening-screen-run.json')
  expect(screen.getByRole('heading', { name: 'Original deployment answers' })).toBeVisible()
})

it('keeps retrieval visible on screening start errors and prevents competing starts while accepting a request', async () => {
  const access = { run_id: 'retrieve-run', run_secret: 'retrieve-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  vi.mocked(api.getReview).mockResolvedValue(retrieved)
  vi.mocked(api.startScreening).mockRejectedValueOnce(new Error('This key is already running a job.'))
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.type(await screen.findByLabelText('OpenAI API key for initial screening'), 'sk-private')
  await user.click(screen.getByRole('button', { name: 'Screen initial candidates' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('This key is already running a job.')
  expect(screen.getByRole('heading', { name: 'Your benchmark candidates are ready' })).toBeVisible()
  let accept!: (run: api.RunAccess) => void
  vi.mocked(api.startScreening).mockImplementationOnce(() => new Promise(resolve => { accept = resolve }))
  await user.click(screen.getByRole('button', { name: 'Screen initial candidates' }))
  expect(screen.getByLabelText('OpenAI API key for initial screening')).toBeDisabled()
  expect(screen.getByRole('button', { name: 'Start another run' })).toBeDisabled()
  expect(screen.getAllByRole('button', { name: 'Starting…' }).every(button => (button as HTMLButtonElement).disabled)).toBe(true)
  vi.mocked(api.getReview).mockResolvedValue(screened)
  accept({ run_id: 'screen-run', run_secret: 'screen-access' })
  await screen.findByRole('heading', { name: 'Your initial screening is ready' })
  expect(sessionStorage.getItem('item_review_run_v1')).not.toContain('sk-private')
})

it('renders model text as text and identifies reused assessments without changing allocation order', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'screen-run', run_secret: 'screen-access' }))
  const htmlText = '<img src=x onerror=alert(1)>'
  vi.mocked(api.getReview).mockResolvedValue({ ...screened, screening: { ...screened.screening!, items: [
    screened.screening!.items[1], { ...screeningItem, screened_run_id: 'earlier-run', assessment: { ...assessment, task: { ...assessment.task, decision: htmlText } } },
  ] } })
  render(<ItemReview />)
  const first = await screen.findByRole('article', { name: 'Screened item 1' })
  expect(within(first).getByText(htmlText)).toBeVisible()
  expect(first.querySelector('img')).toBeNull()
  expect(within(first).getByText('Retained assessment from an earlier screening run.')).toBeVisible()
  expect(within(first).getByRole('heading', { name: 'Screening gate: Pass' })).toBeVisible()
})

it('selects at most 30 items across the whole collection without a key or another screening call', async () => {
  const source = { run_id: 'screen-run', run_secret: 'screen-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(source))
  vi.mocked(api.getCatalog).mockResolvedValue({ ...catalog, dataset_access_configured: false })
  vi.mocked(api.getReview).mockResolvedValueOnce(screened).mockResolvedValue(selected)
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your initial screening is ready' })
  expect(screen.getByText(/one shared limit of 30 items across all tasks/)).toBeVisible()
  expect(screen.getByText(/Selection runs locally, makes no model calls, and needs no API key/)).toBeVisible()
  expect(screen.getByLabelText('OpenAI API key for initial screening')).toHaveValue('')
  expect(screen.queryByRole('spinbutton')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Select up to 30 items' })).toBeEnabled()
  expect(api.startSelection).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Select up to 30 items' }))
  await screen.findByRole('heading', { name: 'Selection has coverage gaps' })
  expect(api.startSelection).toHaveBeenCalledWith(source)
  expect(api.startScreening).not.toHaveBeenCalled()
  expect(api.startBenchmarkRetrieval).not.toHaveBeenCalled()
  expect(screen.getByText('Selected items').parentElement).toHaveTextContent('1 / 30')
  expect(screen.getByText('Eligible items').parentElement).toHaveTextContent('1')
  expect(screen.getByText('Total quality Q').parentElement).toHaveTextContent('4.00')
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(JSON.stringify({ run_id: 'select-run', run_secret: 'select-access' }))
  expect(localStorage.length).toBe(0)
})

it('shows task and quota shortfalls, unresolved quota minima, and the selected item rating evidence', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'select-run', run_secret: 'select-access' }))
  const originalRequirements = selected.requirements!
  const uncoveredTask = { ...originalRequirements.task_facets[0], facet_id: 'diagnosis', essential: false }
  vi.mocked(api.getReview).mockResolvedValue({ ...selected, requirements: { ...originalRequirements,
    task_facets: [...originalRequirements.task_facets, uncoveredTask],
    coverage_requirements: [...originalRequirements.coverage_requirements, { ...originalRequirements.coverage_requirements[0], minimum_items: null }],
  }, selection: { ...selected.selection!,
    task_coverage: [...selected.selection!.task_coverage, { facet_id: 'diagnosis', minimum: 1, eligible_count: 0, selected_count: 0, shortfall: 1 }],
    quota_coverage: [...selected.selection!.quota_coverage, { requirement_index: 1, minimum_items: null, eligible_count: 0, selected_count: 0, shortfall: null }],
    unresolved_requirement_indices: [1],
  } })
  const user = userEvent.setup()
  render(<ItemReview />)
  expect(await screen.findByText('Coverage remains incomplete.')).toBeVisible()
  expect(screen.getByText('The allergy-constrained management requirement is short by 2 items.')).toBeVisible()
  const taskCoverage = screen.getByRole('region', { name: 'Task coverage' })
  const rows = within(taskCoverage).getAllByRole('row')
  expect(within(rows[1]).getAllByRole('cell').map(cell => cell.textContent)).toEqual(['1', '1', '1', '0'])
  expect(within(rows[2]).getAllByRole('cell').map(cell => cell.textContent)).toEqual(['1', '0', '0', '1'])
  const quotaCoverage = screen.getByRole('region', { name: 'Coverage requirements in this collection' })
  expect(within(quotaCoverage).getByRole('heading', { name: 'Coverage requirement 1' }).parentElement).toHaveTextContent('Minimum items: 3 · Eligible: 1 · Selected: 1 · Shortfall: 2')
  expect(within(quotaCoverage).getByText('This requirement remains unresolved and cannot be claimed as satisfied.')).toBeVisible()
  expect(within(quotaCoverage).getByRole('heading', { name: 'Coverage requirement 2' }).parentElement).toHaveTextContent('Minimum items: Unresolved · Eligible: 0 · Selected: 0 · Shortfall: Unresolved')
  const item = screen.getByRole('article', { name: 'Selected item 1' })
  expect(within(item).getByText('Quality Q: 4.00 / 5')).toBeVisible()
  expect(within(item).getByText('Output content').parentElement).toHaveTextContent('2 / 5')
  expect(within(item).getByText('Output form').parentElement).toHaveTextContent('Unknown')
  expect(within(item).getAllByText('Gate dimension')).toHaveLength(4)
  expect(within(item).getByText('Choose the indicated first treatment.')).toBeVisible()
  await user.click(within(item).getByText('Inspect original row and sources'))
  expect(within(item).getByText(candidates.items[0].search_text)).toBeVisible()
  expect(within(item).getByText(/"grading_criterion": "Reference answer"/)).toBeVisible()
})

it('allows selection from stopped partial screening and can later continue the same initial allocation', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'screen-run', run_secret: 'screen-access' }))
  vi.mocked(api.getReview).mockResolvedValueOnce({ ...screened, status: 'cancelled', screening: { ...screened.screening!, items: [screeningItem] } })
    .mockResolvedValue({ ...selected, selection_input: { allocated: 4, screened: 1, errors: 0, pending: 3 } })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Screening stopped' })
  expect(screen.getByText(/Initial screening is incomplete/)).toHaveTextContent('available so far')
  expect(screen.getByText(/1 valid assessments · 0 assessment errors · 3 pending items/)).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Select up to 30 items' }))
  await screen.findByRole('heading', { name: 'Selection has coverage gaps' })
  expect(screen.getByText(/This selection uses the valid assessments available so far/)).toBeVisible()
  expect(screen.getByText(/1 completed assessments are retained/)).toHaveTextContent('up to 3 items')
  await user.type(screen.getByLabelText('OpenAI API key for initial screening'), 'sk-continue')
  await user.click(screen.getByRole('button', { name: 'Continue screening' }))
  expect(api.startScreening).toHaveBeenCalledWith({ run_id: 'select-run', run_secret: 'select-access' }, 'sk-continue')
})

it('shows a fully covered collection without offering to reassess valid items', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'select-run', run_secret: 'select-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...selected,
    selection_input: { allocated: 1, screened: 1, errors: 0, pending: 0 },
    selection: { ...selected.selection!, constraints_feasible: true, fully_satisfied: true, gaps: [], quota_coverage: [] },
  })
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Your candidate collection is ready' })
  expect(screen.queryByText('Coverage remains incomplete.')).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: 'Continue screening' })).not.toBeInTheDocument()
  expect(screen.queryByLabelText('OpenAI API key for initial screening')).not.toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Select up to 30 items' })).toBeEnabled()
})

it('labels retained selection results as previous when a new selection is stopped', async () => {
  const access = { run_id: 'select-retry', run_secret: 'retry-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  const retry: api.SelectionReview = { ...selected, run_id: 'select-retry', status: 'running', selection_run_id: 'select-run', message: 'Selecting again.' }
  vi.mocked(api.getReview).mockResolvedValue(retry)
  vi.mocked(api.cancelReview).mockResolvedValue({ ...retry, status: 'cancelled', message: 'Selection stopped.' })
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Selecting the benchmark collection' })
  expect(screen.getByText(/This run has not produced a new completed selection/)).toBeVisible()
  expect(screen.getByRole('heading', { name: 'Previously selected collection' })).toBeVisible()
  expect(screen.getByRole('article', { name: 'Selected item 1' })).toBeVisible()
  expect(screen.queryByRole('button', { name: 'Select up to 30 items' })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Stop selection' }))
  await screen.findByRole('heading', { name: 'Selection stopped' })
  expect(api.cancelReview).toHaveBeenCalledWith(access)
  expect(screen.getByText(/This run has not produced a new completed selection/)).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Select up to 30 items' }))
  expect(api.startSelection).toHaveBeenCalledWith(access)
})

it('exports selection evidence and preserves a previous collection after a solver failure', async () => {
  const access = { run_id: 'select-failed', run_secret: 'failed-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  vi.mocked(api.getReview).mockResolvedValue({ ...selected, run_id: 'select-failed', status: 'failed', message: 'Selection could not complete.', selection_run_id: 'select-run' })
  vi.mocked(api.getReviewExport).mockResolvedValue(new Blob([JSON.stringify(selected)], { type: 'application/json' }))
  vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:selection')
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  const user = userEvent.setup()
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Selection interrupted' })
  expect(screen.getByRole('alert')).toHaveTextContent('Selection could not complete.')
  expect(screen.getByRole('heading', { name: 'Previously selected collection' })).toBeVisible()
  await user.click(screen.getByText('Inspect selection policy, exclusions, and solver result'))
  expect(screen.getByText(/"selection_run_id": "select-run"/)).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Download selection JSON' }))
  expect(api.getReviewExport).toHaveBeenCalledWith(access)
  expect(click.mock.instances[0]).toHaveAttribute('download', 'benchmark-selection-select-failed.json')
})

it('keeps the screening report available if collection selection cannot start', async () => {
  const access = { run_id: 'screen-run', run_secret: 'screen-access' }
  sessionStorage.setItem('item_review_run_v1', JSON.stringify(access))
  vi.mocked(api.getReview).mockResolvedValue({ ...screened, screening: { ...screened.screening!, items: [screeningItem] } })
  vi.mocked(api.startSelection).mockRejectedValueOnce(new Error('The selection worker is busy.'))
  const user = userEvent.setup()
  render(<ItemReview />)
  await user.click(await screen.findByRole('button', { name: 'Select up to 30 items' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('The selection worker is busy.')
  expect(screen.getByRole('article', { name: 'Screened item 1' })).toBeVisible()
  expect(screen.getByRole('button', { name: 'Select up to 30 items' })).toBeEnabled()
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(JSON.stringify(access))
})

it('renders an initial selection without a result and keeps selection unavailable during active screening', async () => {
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'screen-run', run_secret: 'screen-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...screened, status: 'running' })
  const { unmount } = render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Screening initial candidates' })
  expect(screen.queryByRole('button', { name: 'Select up to 30 items' })).not.toBeInTheDocument()
  unmount()
  sessionStorage.setItem('item_review_run_v1', JSON.stringify({ run_id: 'select-run', run_secret: 'select-access' }))
  vi.mocked(api.getReview).mockResolvedValue({ ...selected, status: 'preparing', selection: null, selection_run_id: null })
  render(<ItemReview />)
  await screen.findByRole('heading', { name: 'Selecting the benchmark collection' })
  expect(screen.getByRole('progressbar', { name: 'Collection selection in progress' })).toBeVisible()
  expect(screen.queryByRole('article', { name: 'Selected item 1' })).not.toBeInTheDocument()
})
