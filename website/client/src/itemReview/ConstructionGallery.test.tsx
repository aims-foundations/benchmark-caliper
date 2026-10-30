import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EvaluationSite } from '../EvaluationSite'
import { PIPELINE_RUN_STORAGE } from './accessStorage'
import { type AdaptiveReview, type ScreenedItem } from './api'
import { type ConstructionComposition, type ConstructionExample, type ConstructionSnapshot } from './ConstructionGallery'

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
    retrieval: { policy: {}, scope: { repo: 'measurement-db', branches: { main: 'abc' }, benchmarks: ['clinical_questions'], table_count: 281, source_rows: 8471422, sample_only: false }, stats: {}, queries: [{ facet_id: 'management', query: 'Clinical management', onet_record_ids: [], search_terms: [], refinements: [], candidate_count: 600 }], queues: [{ queue_id: 'management', facet_id: 'management', source: null, item_count: 600 }] },
    screening: { policy: { version: 1, initial_budget: 48, gated_dimensions: ['input_ontology', 'input_content', 'input_form', 'output_ontology'], minimum_score: 3 }, model: { version: 1, model: 'gpt-6-luna', reasoning_effort: 'high', max_output_tokens: 25000, prompt: 'Screen supplied evidence.', output_schema: {} },
      allocation: { budget: 48, allocated: 48, shortfall: 0, allocations: [], items: [] }, items: Array.from({ length: 10 }, (_, i) => fullItem(i + 48)) },
    selection_input: { allocated: 160, screened: 160, errors: 0, pending: 0 }, selection_run_id: 'original-run', selection,
    adaptive: { version: 1, policy: {}, settings: { seed: 0, max_cost_usd: null, input_price_per_million: null, cached_input_price_per_million: null, output_price_per_million: null, candidate_limit: 160, batch_size: 8, exploration_rate: .2 },
      initial_selection: { ...selection, selected_count: 0, selected_item_ids: [], items: [], total_quality: 0, task_coverage: [{ ...selection.task_coverage[0], selected_count: 0, shortfall: 1 }] }, initial_selection_run_id: 'initial-selection',
      batches: [], queue_statistics: [], attempts: [], cost: { spent_usd: null, reserved_usd: null, unknown_attempts: 0, scope: 'adaptive_screening' }, frozen: true, stop_reason: 'candidate_limit', screened_count: 160, acquired_count: 160 },
  } satisfies AdaptiveReview,
  items: Array.from({ length: 160 }, (_, index) => ({ item_id: `item-${index}`, index, question_preview: `Question preview ${index}`, preview_kind: 'question', status: 'complete', gate: index >= 48 && index < 58 ? 'pass' : 'fail', matched_facet_ids: ['management'], sources: ['clinical_questions'], selected: index >= 48 && index < 58, initial: index < 48, quality_score: 4 })),
}
const composition: ConstructionComposition = {
  selected_count: 10,
  sources: [{ name: 'AfriMedQA', count: 7, percentage: 70 }, { name: 'chatgpt_drift', count: 2, percentage: 20 }, { name: 'MMLU', count: 1, percentage: 10 }],
  unknown_source_count: 0,
  tasks: [{ facet_id: 'diagnosis', label: 'Choose a diagnosis', count: 5 }, { facet_id: 'investigation', label: 'Choose an investigation', count: 1 }, { facet_id: 'management', label: 'Choose initial management', count: 4 }],
  coverage: [{ requirement_index: 0, label: 'Include allergy cases.', minimum_items: 3, selected_count: 0, shortfall: 3 }],
  question_text: { available_count: 10, distinct_count: 9, missing_count: 0, overlaps: [{ item_ids: ['item-48', 'item-49'] }] },
  formats: { counts: [{ label: 'Text multiple choice questions', count: 10 }], unknown_count: 0, basis: 'Reviewed the original questions and answer choices in all selected rows.' },
}
let currentSnapshot: ConstructionSnapshot
let fetchMock: ReturnType<typeof vi.fn>
beforeEach(() => {
  currentSnapshot = structuredClone(snapshot)
  localStorage.clear(); sessionStorage.clear()
  fetchMock = vi.fn(async (input: string) => {
    const url = new URL(input, window.location.origin)
    const path = url.pathname
    if (path === '/nav.json') return new Response('{}')
    if (path === '/api/item-review/examples') return new Response(JSON.stringify({ examples: [entry] }))
    if (path === `/api/item-review/examples/${exampleId}`) return new Response(JSON.stringify(currentSnapshot))
    if (path.endsWith('/retrieved')) {
      const page = Number(url.searchParams.get('page') ?? 1)
      return new Response(JSON.stringify({ queue_id: 'management', facet_id: 'management', source: null,
        page, page_size: 10, total: 600, total_pages: 60, unique_candidate_count: 600,
        items: Array.from({ length: 10 }, (_, index) => ({ item_id: `retrieved-${(page - 1) * 10 + index}`,
          queue_rank: (page - 1) * 10 + index + 1, rank: index + 1, dense_rank: 1, bm25_rank: 2, dense_score: 1, bm25_score: 2, rrf_score: 1,
          question_preview: `Retrieved question ${(page - 1) * 10 + index}`, sources: ['clinical_questions'] })) }))
    }
    if (path.includes('/retrieved/')) return new Response(JSON.stringify({ ...fullItem(0), item_id: path.split('/').at(-1) }))
    const match = path.match(/\/items\/item-(\d+)$/)
    if (match) return new Response(JSON.stringify(fullItem(Number(match[1]))))
    if (path.endsWith('/package/chunk')) return new Response('zip', { headers: { 'X-Package-Id': 'fixed-zip', 'X-Package-Offset': '0', 'Content-Length': '3' } })
    return new Response('', { status: 404 })
  })
  vi.stubGlobal('fetch', fetchMock)
  window.history.replaceState(null, '', `/items?example=${exampleId}`)
})
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); window.history.replaceState(null, '', '/') })

const openView = async (user: ReturnType<typeof userEvent.setup>, name: string) => {
  await user.click(screen.getByRole('tab', { name }))
}
const openStep = async (user: ReturnType<typeof userEvent.setup>, step: number) => {
  await openView(user, 'How it was built')
  await user.click(within(screen.getByRole('navigation', { name: 'Construction steps' })).getByRole('button', { name: new RegExp(`^Step ${step}`) }))
  return screen.getByRole('article', { name: new RegExp(`^Step ${step}:`) })
}
const openDownloads = async (user: ReturnType<typeof userEvent.setup>) => {
  await user.click(screen.getByText('Download results', { exact: true }))
}

it('opens a concise overview without mounting private runs or loading every assessment', async () => {
  const privateAccess = JSON.stringify({ run_id: 'private-run', run_secret: 'secret-access' })
  localStorage.setItem(PIPELINE_RUN_STORAGE, privateAccess)
  sessionStorage.setItem('item_review_run_v1', privateAccess)
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  expect(screen.getByRole('tab', { name: 'Overview', selected: true })).toBeVisible()
  expect(screen.getAllByRole('tab')).toHaveLength(3)
  expect(screen.queryByRole('heading', { name: /^Step [1-7]:/ })).not.toBeInTheDocument()
  expect(screen.queryByText('Screened item 1', { exact: true })).not.toBeInTheDocument()
  expect(document.querySelector('.construction-item')).toBeNull()
  expect(screen.queryByText('Full item record and sources')).not.toBeInTheDocument()
  expect(screen.queryByText(/human validation/i)).not.toBeInTheDocument()
  const summary = screen.getByRole('region', { name: 'Final collection summary' })
  expect(within(summary).getByText('Average quality Q').nextElementSibling).toHaveTextContent('4.00 / 5')
  expect(summary.compareDocumentPosition(screen.getByRole('tablist')) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/items/item-'))).toBe(false)
  expect(localStorage.getItem(PIPELINE_RUN_STORAGE)).toBe(privateAccess)
  expect(sessionStorage.getItem('item_review_run_v1')).toBe(privateAccess)
  expect(fetchMock.mock.calls.every(([url]) => url === '/nav.json' || String(url).startsWith('/api/item-review/examples'))).toBe(true)
  for (const [, options] of fetchMock.mock.calls) expect(options).not.toHaveProperty('headers.X-Review-Token')
  expect(screen.queryByLabelText(/OpenAI API key/i)).not.toBeInTheDocument()
})

it('supports keyboard navigation among the three views', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  const overview = await screen.findByRole('tab', { name: 'Overview' })
  overview.focus()
  await user.keyboard('{ArrowRight}')
  expect(screen.getByRole('tab', { name: 'How it was built', selected: true })).toHaveFocus()
  expect(screen.getByRole('heading', { name: /^Step 1:/ })).toBeVisible()
  await user.keyboard('{End}')
  expect(screen.getByRole('tab', { name: 'Browse items', selected: true })).toHaveFocus()
  await user.keyboard('{Home}')
  expect(screen.getByRole('tab', { name: 'Overview', selected: true })).toHaveFocus()
})

it('shows one chronological step at a time and distinguishes initial selection from the final collection', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  await openView(user, 'How it was built')
  const steps = within(screen.getByRole('navigation', { name: 'Construction steps' })).getAllByRole('button')
  expect(steps.map(button => button.textContent?.match(/Step (\d)/)?.[1])).toEqual(['1', '2', '3', '4', '5', '6', '7'])
  expect(screen.getAllByRole('heading', { name: /^Step [1-7]:/ })).toHaveLength(1)
  expect(screen.getByRole('button', { name: 'Previous step' })).toBeDisabled()
  await user.click(screen.getByRole('button', { name: 'Next step' }))
  expect(screen.getByRole('heading', { name: /^Step 2:/ })).toBeVisible()
  await openStep(user, 6)
  expect(screen.getByRole('heading', { name: 'Initial selection' })).toBeVisible()
  expect(screen.getByText('0 items were selected at this stage.')).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Next step' }))
  expect(screen.getByText(/48 initial candidates \+ 112 additional candidates = 160 assessed in total/)).toBeVisible()
  expect(screen.getByText('Final selected items').nextElementSibling).toHaveTextContent('10')
  expect(screen.getByRole('button', { name: 'Next step' })).toBeDisabled()
})

it('shows retrieved candidates and screening results on their own step pages', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  let step = await openStep(user, 4)
  expect(within(step).getByText('These task lists overlap.')).toBeVisible()
  expect(await within(step).findByText('Retrieved question 0')).toBeVisible()
  expect(within(step).getByText('Step overview').closest('details')).not.toHaveAttribute('open')
  expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/retrieved/'))).toBe(false)
  await user.click(within(step).getByText('Retrieved item 1'))
  const retrieved = within(step).getByText('Retrieved item 1').closest('details')!
  const content = (await within(retrieved).findByRole('heading', { name: 'Item content' })).closest('section')!
  expect(content.parentElement?.firstElementChild).toBe(content)
  expect(content.querySelector('p')?.textContent).toBe(fullItem(0).question_text)
  expect(within(retrieved).getByText(/Task ranking: 1/)).toHaveTextContent('Meaning search rank: 1. Keyword search rank: 2.')
  await user.click(within(step).getByRole('button', { name: 'Next items' }))
  expect(await within(step).findByText('Retrieved item 11')).toBeVisible()
  expect(within(step).queryByText('Retrieved item 1', { exact: true })).not.toBeInTheDocument()
  step = await openStep(user, 5)
  expect(within(step).getByText('Valid assessments').nextElementSibling).toHaveTextContent('48')
  expect(within(step).getByText('Eligible items').nextElementSibling).toHaveTextContent('0')
  expect(within(step).getByRole('status')).toHaveTextContent('48 items. Showing 1 to 10.')
  expect(within(step).getByText('Screened item 1')).toBeVisible()
  expect(within(step).queryByText('Final collection:')).not.toBeInTheDocument()
  await user.click(within(step).getByRole('button', { name: 'Next items' }))
  expect(within(step).getByRole('status')).toHaveTextContent('48 items. Showing 11 to 20.')
  step = await openStep(user, 6)
  expect(within(step).getByText('No items were selected at Step 6.')).toBeVisible()
  expect(step.querySelector('.construction-browser-item')).toBeNull()
  step = await openStep(user, 7)
  expect(within(step).getByRole('status')).toHaveTextContent('10 items. Showing 1 to 10.')
  expect(Array.from(step.querySelectorAll('.construction-browser-item')).map(item => item.id)).toEqual(selection.selected_item_ids.map(id => `step-7-item-${id}`))
  await user.selectOptions(within(step).getByLabelText('Items to show'), 'adaptive')
  expect(within(step).getByRole('status')).toHaveTextContent('112 items. Showing 1 to 10.')
})

it('defaults to selected items and loads full unselected assessments only when opened', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  await openView(user, 'Browse items')
  expect(screen.getByRole('button', { name: 'Selected items (10)' })).toHaveAttribute('aria-pressed', 'true')
  expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
  expect(screen.getByText('Selected item 1', { exact: true }).closest('details')).not.toHaveAttribute('open')
  expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/items/item-'))).toBe(false)
  await user.click(screen.getByRole('button', { name: 'All screened items (160)' }))
  await user.click(screen.getByText('Screened item 1', { exact: true }))
  await screen.findByText('Full item record and sources')
  const item = screen.getByText('Screened item 1', { exact: true }).closest('details')!
  const question = within(item).getByText(/Full original question 0\./, { selector: 'p' })
  expect(question.textContent).toBe(fullItem(0).question_text)
  expect(item.querySelector('script')).toBeNull()
  await user.click(within(item).getByText('Screening explanations and supporting evidence'))
  expect(within(item).getAllByText('Original evidence — keep · punctuation.', { exact: true })[0]).toBeVisible()
  await user.click(within(item).getByText('Full item record and sources'))
  expect(within(item).getAllByText(/Original row 0/)[0]).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Next items' }))
  expect(screen.getByText('Screened item 11', { exact: true })).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Previous items' }))
  await user.click(screen.getByText('Screened item 1', { exact: true }))
  await screen.findByText('Full item record and sources')
  expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith('/items/item-0'))).toHaveLength(1)
})

it('filters all assessments by eligibility and stage while keeping selected items complete', async () => {
  const user = userEvent.setup()
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  await openView(user, 'Browse items')
  await user.click(screen.getByRole('button', { name: 'All screened items (160)' }))
  await user.selectOptions(screen.getByLabelText('Screening stage'), 'initial')
  await user.selectOptions(screen.getByLabelText('Eligibility result'), 'fail')
  expect(screen.getByRole('status')).toHaveTextContent('48 matching items. Page 1 of 5.')
  await user.selectOptions(screen.getByLabelText('Screening stage'), 'adaptive')
  expect(screen.getByRole('status')).toHaveTextContent('102 matching items. Page 1 of 11.')
  await user.selectOptions(screen.getByLabelText('Eligibility result'), 'all')
  expect(screen.getByRole('status')).toHaveTextContent('112 matching items. Page 1 of 12.')
  await user.click(screen.getByRole('button', { name: 'Selected items (10)' }))
  expect(screen.getByRole('heading', { name: 'Selected items (10)' })).toBeVisible()
  expect(document.querySelectorAll('.construction-browser-item')).toHaveLength(10)
  expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
  expect(within(screen.getByRole('region', { name: 'Final collection summary' })).getByText('Average quality Q').nextElementSibling).toHaveTextContent('4.00 / 5')
})

it('follows requirement evidence across views and reveals the original answer', async () => {
  currentSnapshot.composition = structuredClone(composition)
  const user = userEvent.setup()
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  await user.click(screen.getByRole('link', { name: 'Choose initial management' }))
  expect(screen.getByRole('tab', { name: 'How it was built', selected: true })).toBeVisible()
  const facet = await screen.findByText('Clinical vignette', { exact: true })
  expect(document.getElementById('facet-management')).toBeVisible()
  expect(facet).toBeVisible()
  await user.click(within(document.getElementById('facet-management')!).getAllByRole('link', { name: /^Answer 1:/ })[0])
  expect(screen.getByRole('heading', { name: /^Step 1:/ })).toBeVisible()
  expect(document.getElementById('original-answer-task')).toBeVisible()
})

it('reveals linked selected items from composition without preloading every assessment', async () => {
  currentSnapshot.composition = structuredClone(composition)
  const user = userEvent.setup()
  render(<EvaluationSite />)
  const summary = await screen.findByRole('region', { name: 'Composition of the selected items' })
  await user.click(within(summary).getByText('Inspect composition details', { exact: true }))
  const first = within(summary).getByRole('link', { name: 'Selected item 1' })
  expect(first).toHaveAttribute('href', '#selected-item-item-48')
  await user.click(first)
  expect(screen.getByRole('tab', { name: 'Browse items', selected: true })).toBeVisible()
  const card = document.getElementById('selected-item-item-48')!
  await waitFor(() => expect(card).toHaveAttribute('open'))
  expect(within(card).getByText(/Full original question 48\./, { selector: 'p' })).toBeVisible()
  expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/items/item-'))).toBe(false)
})

it('opens a screened item deep link outside the selected collection and tolerates malformed hashes', async () => {
  window.history.replaceState(null, '', `/items?example=${exampleId}#screened-item-item-159`)
  const user = userEvent.setup()
  const view = render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  expect(await screen.findByRole('tab', { name: 'Browse items', selected: true })).toBeVisible()
  const item = await screen.findByText('Screened item 160', { exact: true })
  await waitFor(() => expect(item.closest('details')).toHaveAttribute('open'))
  await screen.findByText('Full item record and sources')
  expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith('/items/item-159'))).toHaveLength(1)
  await openView(user, 'Overview')
  view.unmount()
  window.history.replaceState(null, '', `/items?example=${exampleId}#%E0%A4%A`)
  render(<EvaluationSite />)
  expect(await screen.findByRole('tab', { name: 'Overview', selected: true })).toBeVisible()
})

it('offers original downloads behind one disclosure and uses public package requests', async () => {
  const user = userEvent.setup()
  const create = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:public-package')
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  currentSnapshot.entry.artifacts.summary_report = { filename: 'report-with-composition.html', bytes: 40 }
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  expect(screen.getByRole('link', { name: 'Read the original HTML report' }).closest('details')).not.toHaveAttribute('open')
  await openDownloads(user)
  expect(screen.getByRole('link', { name: 'Read the original HTML report' })).toHaveAttribute('href', `/api/item-review/examples/${exampleId}/artifacts/report`)
  expect(screen.getByRole('link', { name: 'Read the report with composition summary' })).toHaveAttribute('href', `/api/item-review/examples/${exampleId}/artifacts/summary_report`)
  await user.click(screen.getByRole('button', { name: 'Download original results package' }))
  expect(create).toHaveBeenCalled()
  expect(click.mock.instances[0]).toHaveAttribute('download', 'complete-results.zip')
  const chunk = fetchMock.mock.calls.find(([url]) => String(url).includes('/package/chunk'))!
  expect(chunk[1]).toMatchObject({ headers: {} })
  expect(fetchMock.mock.calls.every(([, options]) => options?.method !== 'POST')).toBe(true)
})

it('copies a stable example address without a date or navigation hash', async () => {
  const user = userEvent.setup()
  const write = vi.spyOn(navigator.clipboard, 'writeText').mockResolvedValue(undefined)
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  await user.click(screen.getByRole('button', { name: 'Copy link' }))
  expect(write).toHaveBeenCalledWith(`${window.location.origin}/items?example=clinical-exam-study`)
  expect(screen.getByText('Link copied.')).toBeVisible()
})

it('lists published examples and does not expose workflow controls for an unavailable example', async () => {
  window.history.replaceState(null, '', '/items?gallery=1')
  const view = render(<EvaluationSite />)
  const link = await screen.findByRole('link', { name: entry.title })
  expect(link).toHaveAttribute('href', '/items?example=clinical-exam-study')
  expect(screen.getByRole('link', { name: 'View results' })).toHaveAttribute('href', '/items?example=clinical-exam-study')
  view.unmount()
  window.history.replaceState(null, '', `/items?example=${exampleId}`)
  fetchMock.mockImplementation(async (url: string) => new Response(url === '/nav.json' ? '{}' : '', { status: url === '/nav.json' ? 200 : 404 }))
  render(<EvaluationSite />)
  expect(await screen.findByRole('alert')).toHaveTextContent('These saved results are unavailable.')
  expect(screen.queryByRole('tab')).not.toBeInTheDocument()
})

it('retains missing source and question-text findings without displaying format annotations', async () => {
  const user = userEvent.setup()
  currentSnapshot.composition = {
    ...structuredClone(composition),
    sources: [{ name: 'AfriMedQA', count: 7, percentage: 70 }], unknown_source_count: 3,
    formats: { counts: [], unknown_count: 10, basis: null },
    question_text: { available_count: 8, distinct_count: 8, missing_count: 2, overlaps: [] },
    coverage: [{ requirement_index: 0, label: 'Include allergy cases.', minimum_items: null, selected_count: 0, shortfall: null }],
  }
  render(<EvaluationSite />)
  const summary = await screen.findByRole('region', { name: 'Composition of the selected items' })
  await user.click(within(summary).getByText('Inspect composition details', { exact: true }))
  expect(within(summary).getByRole('row', { name: 'Benchmark not recorded 3 30%' })).toBeVisible()
  expect(within(summary).queryByText(/format annotation/i)).not.toBeInTheDocument()
  expect(within(summary).queryByRole('heading', { name: 'Question formats' })).not.toBeInTheDocument()
  expect(within(summary).queryByText(/^Text multiple choice questions:/)).not.toBeInTheDocument()
  expect(within(summary).queryByText(/^Format review:/)).not.toBeInTheDocument()
  expect(within(summary).getByText(/8 of 10 selected rows have question text available/)).toHaveTextContent('2 rows could not be compared.')
  expect(within(summary).getByText(/No numeric minimum was specified/)).toHaveTextContent('The coverage finding remains unresolved.')
})

it('explains counts when selected rows have multiple source or task assignments', async () => {
  const user = userEvent.setup()
  currentSnapshot.composition = {
    ...structuredClone(composition),
    sources: [...composition.sources, { name: 'Additional source', count: 1, percentage: 10 }],
  }
  render(<EvaluationSite />)
  const summary = await screen.findByRole('region', { name: 'Composition of the selected items' })
  await user.click(within(summary).getByText('Inspect composition details', { exact: true }))
  expect(within(summary).getByText(/An item can belong to more than one source benchmark or deployment task/)).toHaveTextContent('Source shares use all 10 selected items as the denominator.')
})

it('handles a single selected item and an empty selected collection', async () => {
  const user = userEvent.setup()
  currentSnapshot.composition = {
    selected_count: 1, sources: [{ name: 'One source', count: 1, percentage: 100 }], unknown_source_count: 0,
    tasks: [{ facet_id: 'management', label: 'Choose initial management', count: 1 }], coverage: [],
    question_text: { available_count: 1, distinct_count: 1, missing_count: 0, overlaps: [] },
    formats: { counts: [], unknown_count: 1, basis: null },
  }
  currentSnapshot.review.selection = { ...selection, selected_count: 1, selected_item_ids: ['item-48'] }
  const view = render(<EvaluationSite />)
  let summary = await screen.findByRole('region', { name: 'Composition of the selected items' })
  await user.click(within(summary).getByText('Inspect composition details', { exact: true }))
  expect(within(summary).getByText(/1 recorded source benchmark across 1 deployment task/)).toBeVisible()
  expect(within(summary).getByText('1 selected row contains 1 distinct question text after normalizing whitespace.')).toBeVisible()
  expect(within(summary).getByText('No additional coverage requirements were recorded.')).toBeVisible()
  view.unmount()
  currentSnapshot.composition = {
    selected_count: 0, sources: [], unknown_source_count: 0, tasks: [], coverage: [],
    question_text: { available_count: 0, distinct_count: 0, missing_count: 0, overlaps: [] },
    formats: { counts: [], unknown_count: 0, basis: null },
  }
  currentSnapshot.review.selection = { ...selection, selected_count: 0, selected_item_ids: [], total_quality: 0 }
  render(<EvaluationSite />)
  summary = await screen.findByRole('region', { name: 'Composition of the selected items' })
  expect(within(summary).getByText('No items were selected, so there is no selected collection to summarize.')).toBeVisible()
  expect(within(summary).queryByRole('table')).not.toBeInTheDocument()
  expect(within(screen.getByRole('region', { name: 'Final collection summary' })).getByText('Average quality Q').nextElementSibling).toHaveTextContent('Not available')
})

it('shows original answers and extracted results while keeping general explanations optional', async () => {
  const user = userEvent.setup()
  currentSnapshot.review.grounding!.facets = [{ facet_id: 'management', query: 'Clinical work', status: 'complete',
    candidates: [{ doc_id: 'onet-1', kind: 'task', name: 'Clinical activity', text: 'Explain treatment plans.', occupation_id: null, dense_rank: 1, bm25_rank: 1, rrf_score: 1 }],
    mapping: { facet_id: 'management', records: [{ record_id: 'onet-1', supporting_passage: 'Explain treatment plans.', applicability: 'partially_applicable', rationale: 'Shared treatment terminology.', search_terms: ['treatment plans'] }], refinements: [], unresolved_details: [] } }]
  render(<EvaluationSite />)
  await screen.findByRole('heading', { name: entry.title })
  let step = await openStep(user, 1)
  const overview = within(step).getByText('Step overview').closest('details')!
  expect(overview).not.toHaveAttribute('open')
  const answers = within(step).getByRole('region', { name: 'Original deployment answers' })
  expect(answers).toBeVisible()
  expect(answers.closest('details')).toBeNull()
  expect(within(answers).getAllByRole('heading', { level: 3 })).toHaveLength(6)
  expect(overview.compareDocumentPosition(answers) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  for (const value of Object.values(currentSnapshot.review.deployment)) expect(within(answers).getByText(value, { exact: true })).toBeVisible()
  step = await openStep(user, 2)
  expect(within(step).getByText('Clinical vignette', { exact: true })).toBeVisible()
  expect(within(step).getByText('Oversight unspecified.', { exact: true })).toBeVisible()
  expect(within(step).getByText('Step overview').closest('details')).not.toHaveAttribute('open')
  step = await openStep(user, 3)
  expect(within(step).getByRole('heading', { name: 'O*NET mappings' })).toBeVisible()
  expect(within(step).getByText('Explain treatment plans.', { exact: true, selector: 'blockquote' })).toBeVisible()
  expect(within(step).getByText('Shared treatment terminology.')).toBeVisible()
})
