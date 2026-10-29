import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EvaluationSite } from '../EvaluationSite'
import { PIPELINE_RUN_STORAGE } from './accessStorage'
import { type AdaptiveReview, type ScreenedItem } from './api'
import { type ConstructionExample, type ConstructionSnapshot } from './ConstructionGallery'

vi.mock('../App', () => ({ App: () => null }))
vi.mock('../ItemAnalysisEntry', () => ({ ItemAnalysisEntry: () => null }))
vi.mock('./ItemReview', () => ({ ItemReview: () => { throw new Error('Private workflow must not mount on a public example page') } }))
const exampleId = 'clinical-exam-study'
const entry: ConstructionExample = {
  id: exampleId, title: 'Clinical exam study with management constraints', description: 'A completed construction run for clinical exam study questions.',
  run_id: 'original-run', result_state: 'frozen', assessed_count: 160, selected_count: 10, coverage_complete: false,
  artifacts: { report: { filename: 'report.html', bytes: 20 }, items: { filename: 'selected_items.csv', bytes: 10 }, results: { filename: 'results.json', bytes: 30 },
    package: { filename: 'complete-results.zip', bytes: 3, chunk_bytes: 1048576, package_id: 'fixed-zip' } },
}
const supported = (text: string) => ({ text, evidence: [{ answer_id: 'task' as const, quote: 'Clinical exam study.' }] })
const finding = { evidence: ['Original evidence — keep · punctuation.'], justification: 'The case supports this judgment.', information_gaps: [] }
const fullItem = (index: number): ScreenedItem => ({
  item_id: `item-${index}`, evidence_hash: `hash-${index}`, question_text: `Full original question ${index}.\n<script>source content</script> — keep · punctuation.`, search_text: `Complete search text ${index}`,
  evidence: { item: { question: `Original row ${index}`, source: 'Original source data.' } }, sources: [{ benchmark: 'clinical_questions', branch: 'main' }],
  rank: index + 1, dense_rank: 1, bm25_rank: 1, dense_score: 1, bm25_score: 1, rrf_score: 1,
  acquisition: { queue_id: 'queue', facet_id: 'management' }, status: 'complete', gate: { status: index >= 48 && index < 58 ? 'pass' : 'fail', reasons: ['Recorded screening decision.'] },
  assessment: { task: { ...finding, status: 'matched', decision: 'Choose initial management.', matched_facet_ids: ['management'] },
    ratings: { input_ontology: { ...finding, score: 4 }, input_content: { ...finding, score: 4 }, input_form: { ...finding, score: 4 }, output_ontology: { ...finding, score: 4 }, output_content: { ...finding, score: 4 }, output_form: { ...finding, score: 4 } }, coverage: [{ ...finding, requirement_index: 0, satisfied: false }] },
})
const selection = { policy: {}, limit: 30, eligible_count: 10, selected_count: 10, selected_item_ids: Array.from({ length: 10 }, (_, i) => `item-${i + 48}`),
  items: Array.from({ length: 10 }, (_, i) => ({ item_id: `item-${i + 48}`, quality_score: 4, rating_sum: 16, matched_facet_ids: ['management'], coverage_requirement_indices: [] })), total_quality: 40,
  task_coverage: [{ facet_id: 'management', minimum: 1, eligible_count: 10, selected_count: 10, shortfall: 0 }],
  quota_coverage: [{ requirement_index: 0, minimum_items: 3, eligible_count: 0, selected_count: 0, shortfall: 3 }], constraints_feasible: false, fully_satisfied: false,
  gaps: ['Three allergy cases are still needed.'], unresolved_requirement_indices: [], excluded_counts: {}, solver: {},
}
const snapshot: ConstructionSnapshot = {
  entry,
  review: {
    run_id: 'original-run', mode: 'adaptive', status: 'completed', message: 'Construction finished.', model: 'gpt-6-luna', reasoning_effort: 'high', source_run_id: 'prior', usage: {},
    deployment: { task: 'Clinical exam study.', users: 'Students.', inputs: 'Clinical cases.', outputs: 'Short answers.', success: 'Accurate management.', constraints: 'At least three allergy cases.' },
    extraction: null,
    requirements: { workflow: supported('Study assistance'), primary_user: supported('Students'), input_types: supported('Clinical cases'), output_types: supported('Short answers'), authority: { text: null, evidence: [] },
      task_facets: [{ facet_id: 'management', task: supported('Choose initial management'), required_input_evidence: supported('Clinical vignette'), required_output_behavior: supported('Explain treatment'), essential: true }],
      coverage_requirements: [{ facet_ids: ['management'], minimum_items: 3, requirement: supported('Include allergy cases.') }], unresolved_details: ['Oversight unspecified.'] },
    grounding: { retrieval: {}, mapping: { version: 1, model: 'gpt-6-luna', reasoning_effort: 'high', max_output_tokens: 25000, prompt: 'Map tasks.', output_schema: {} }, facets: [] },
    retrieval: { policy: {}, scope: { repo: 'measurement-db', branches: { main: 'abc' }, benchmarks: ['clinical_questions'], table_count: 281, source_rows: 8471422, sample_only: false }, stats: {}, queries: [{ facet_id: 'management', query: 'Clinical management', onet_record_ids: [], search_terms: [], refinements: [], candidate_count: 600 }], queues: [] },
    screening: { policy: { version: 1, initial_budget: 48, gated_dimensions: ['input_ontology', 'input_content', 'input_form', 'output_ontology'], minimum_score: 3 }, model: { version: 1, model: 'gpt-6-luna', reasoning_effort: 'high', max_output_tokens: 25000, prompt: 'Screen supplied evidence.', output_schema: {} },
      allocation: { budget: 48, allocated: 48, shortfall: 0, allocations: [], items: [] }, items: Array.from({ length: 10 }, (_, i) => fullItem(i + 48)) },
    selection_input: { allocated: 160, screened: 160, errors: 0, pending: 0 }, selection_run_id: 'original-run', selection,
    adaptive: { version: 1, policy: {}, settings: { seed: 0, max_cost_usd: null, input_price_per_million: null, cached_input_price_per_million: null, output_price_per_million: null, candidate_limit: 160, batch_size: 8, exploration_rate: .2 },
      initial_selection: { ...selection, selected_count: 0, selected_item_ids: [], items: [], total_quality: 0, task_coverage: [{ ...selection.task_coverage[0], selected_count: 0, shortfall: 1 }] }, initial_selection_run_id: 'initial-selection',
      batches: [], queue_statistics: [], attempts: [], cost: { spent_usd: null, reserved_usd: null, unknown_attempts: 0, scope: 'adaptive_screening' }, frozen: true, stop_reason: 'candidate_limit', screened_count: 160, acquired_count: 160 },
  } satisfies AdaptiveReview,
  items: Array.from({ length: 160 }, (_, index) => ({ item_id: `item-${index}`, index, question_preview: `Question preview ${index}`, status: 'complete', gate: index >= 48 && index < 58 ? 'pass' : 'fail', matched_facet_ids: ['management'], sources: ['clinical_questions'], selected: index >= 48 && index < 58, initial: index < 48, quality_score: 4 })),
}
let fetchMock: ReturnType<typeof vi.fn>
beforeEach(() => {
  localStorage.clear(); sessionStorage.clear()
  fetchMock = vi.fn(async (input: string) => {
    const path = new URL(input, window.location.origin).pathname
    if (path === '/nav.json') return new Response('{}')
    if (path === '/api/item-review/examples') return new Response(JSON.stringify({ examples: [entry] }))
    if (path === `/api/item-review/examples/${exampleId}`) return new Response(JSON.stringify(snapshot))
    const match = path.match(/\/items\/item-(\d+)$/)
    if (match) return new Response(JSON.stringify(fullItem(Number(match[1]))))
    if (path.endsWith('/package/chunk')) return new Response('zip', { headers: { 'X-Package-Id': 'fixed-zip', 'X-Package-Offset': '0', 'Content-Length': '3' } })
    return new Response('', { status: 404 })
  })
  vi.stubGlobal('fetch', fetchMock)
  window.history.replaceState(null, '', `/items?example=${exampleId}`)
})
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); window.history.replaceState(null, '', '/') })

it('opens a public example without reading or changing private run access or making paid calls', async () => {
  const privateAccess = JSON.stringify({ run_id: 'private-run', run_secret: 'secret-access' })
  localStorage.setItem(PIPELINE_RUN_STORAGE, privateAccess)
  sessionStorage.setItem('item_review_run_v1', privateAccess)
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  expect(screen.getByRole('heading', { name: 'Selected items (10)' })).toBeVisible()
  expect(screen.getByRole('heading', { name: 'All screened items (160)' })).toBeVisible()
  expect(within(screen.getByRole('region', { name: 'The final collection' })).getByText('Coverage requirement 1 needs 3 more selected items.')).toBeVisible()
  expect(screen.getByText('Human validation is not included in this saved record.')).toBeVisible()
  expect(screen.getByText(/Construction stopped at the budget of 160 screened candidates/)).toBeVisible()
  expect(localStorage.getItem(PIPELINE_RUN_STORAGE)).toBe(privateAccess)
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(privateAccess)
  expect(fetchMock.mock.calls.every(([url]) => url === '/nav.json' || String(url).startsWith('/api/item-review/examples'))).toBe(true)
  for (const [, options] of fetchMock.mock.calls) expect(options).not.toHaveProperty('headers.X-Review-Token')
  expect(screen.queryByLabelText(/OpenAI API key/i)).not.toBeInTheDocument()
})

it('shows collapsible stages in reverse order and preserves the initial selection separately', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  const stages = screen.getAllByRole('heading', { name: /^Step [1-7]:/ })
  expect(stages.map(heading => heading.textContent?.match(/^Step (\d)/)?.[1])).toEqual(['7', '6', '5', '4', '3', '2', '1'])
  for (const heading of stages) expect(heading.closest('details')).not.toHaveAttribute('open')
  await user.click(screen.getByRole('heading', { name: 'Step 6: Initial collection selection' }))
  expect(screen.getByText('0 items were selected at this stage.')).toBeVisible()
  expect(screen.getByRole('heading', { name: 'Selected items (10)' })).toBeVisible()
})

it('loads a full assessment only when opened, preserves source text, and keeps it cached across pages', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  const browser = await screen.findByRole('region', { name: 'All screened items (160)' })
  expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/items/item-'))).toBe(false)
  await user.click(within(browser).getByText('Screened item 1', { exact: true }))
  const question = await within(browser).findByText(/Full original question 0\./, { selector: 'p' })
  expect(question.textContent).toBe(fullItem(0).question_text)
  expect(browser.querySelector('script')).toBeNull()
  expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith('/items/item-0'))).toHaveLength(1)
  const item = question.closest('details')!
  await user.click(within(item).getByText('Complete original row and provenance'))
  expect(within(item).getAllByText(/Original row 0/)[0]).toBeVisible()
  await user.click(within(browser).getByRole('button', { name: 'Next items' }))
  expect(within(browser).getByText('Screened item 11', { exact: true })).toBeVisible()
  await user.click(within(browser).getByRole('button', { name: 'Previous items' }))
  await user.click(within(browser).getByText('Screened item 1', { exact: true }))
  expect(within(browser).getByText(/Full original question 0\./, { selector: 'p' })).toBeVisible()
  expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith('/items/item-0'))).toHaveLength(1)
})

it('filters all assessments by selection, screening decision, and initial or adaptive stage', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  const browser = await screen.findByRole('region', { name: 'All screened items (160)' })
  await user.selectOptions(within(browser).getByLabelText('Screening result'), 'selected')
  expect(within(browser).getByRole('status')).toHaveTextContent('10 matching items. Page 1 of 1.')
  await user.selectOptions(within(browser).getByLabelText('Screening stage'), 'initial')
  expect(within(browser).getByText('No items match these filters.')).toBeVisible()
  await user.selectOptions(within(browser).getByLabelText('Screening result'), 'fail')
  expect(within(browser).getByRole('status')).toHaveTextContent('48 matching items. Page 1 of 5.')
  await user.selectOptions(within(browser).getByLabelText('Screening stage'), 'adaptive')
  expect(within(browser).getByRole('status')).toHaveTextContent('102 matching items. Page 1 of 11.')
})

it('opens collapsed requirements and original answers when following evidence links', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  const outcome = screen.getByRole('region', { name: 'The final collection' })
  await user.click(within(outcome).getByRole('link', { name: 'Choose initial management' }))
  expect(document.getElementById('construction-step-2')).toHaveAttribute('open')
  const facet = document.getElementById('facet-management')!
  await user.click(within(facet).getAllByRole('link', { name: /^Answer 1:/ })[0])
  expect(document.getElementById('construction-step-1')).toHaveAttribute('open')
  expect(document.getElementById('original-answer-task')).toBeVisible()
})

it('publishes stable links and downloads the public package without private authentication or preparation calls', async () => {
  const user = userEvent.setup()
  const create = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:public-package')
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  expect(screen.getByRole('link', { name: 'Read the HTML report' })).toHaveAttribute('href', `/api/item-review/examples/${exampleId}/artifacts/report`)
  await user.click(screen.getByRole('button', { name: 'Download complete package' }))
  expect(create).toHaveBeenCalled()
  expect(click.mock.instances[0]).toHaveAttribute('download', 'complete-results.zip')
  const chunk = fetchMock.mock.calls.find(([url]) => String(url).includes('/package/chunk'))!
  expect(chunk[1]).toMatchObject({ headers: {} })
  expect(fetchMock.mock.calls.every(([, options]) => options?.method !== 'POST')).toBe(true)
})

it('lists published examples with dateless links', async () => {
  window.history.replaceState(null, '', '/items?gallery=1')
  render(<EvaluationSite />)
  const link = await screen.findByRole('link', { name: entry.title })
  expect(link).toHaveAttribute('href', '/items?example=clinical-exam-study')
  expect(screen.getByRole('link', { name: 'Explore this example' })).toHaveAttribute('href', '/items?example=clinical-exam-study')
  expect(screen.queryByRole('heading', { name: 'The final collection' })).not.toBeInTheDocument()
})

it('shows an unavailable public example without falling back to private results', async () => {
  fetchMock.mockImplementation(async (url: string) => new Response(url === '/nav.json' ? '{}' : '', { status: url === '/nav.json' ? 200 : 404 }))
  render(<EvaluationSite />)
  expect(await screen.findByRole('alert')).toHaveTextContent('This published example is unavailable.')
  expect(screen.queryByRole('heading', { name: 'The final collection' })).not.toBeInTheDocument()
})

it('copies the stable example address without private access or a date', async () => {
  const user = userEvent.setup()
  const write = vi.spyOn(navigator.clipboard, 'writeText').mockResolvedValue(undefined)
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  await user.click(screen.getByRole('button', { name: 'Copy example link' }))
  expect(write).toHaveBeenCalledWith(`${window.location.origin}/items?example=clinical-exam-study`)
  expect(screen.getByText('Link copied.')).toBeVisible()
})
