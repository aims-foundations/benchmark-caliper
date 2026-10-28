import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SavedItemAnalysis, type SavedItemAnalysisSnapshot } from './SavedItemAnalysis'
import { SCORE_DIMENSIONS } from './SixScoreTable'
import type { ClassifierSummary, Item, Specification } from './types'

vi.mock('../paths', () => ({ appPath: (path: string) => `/benchmark-caliper${path}` }))

function snapshot(): SavedItemAnalysisSnapshot {
  const spec: Specification = {
    analysis_type: 'six_scores', schema_version: 'caliper_item_context_v1', rubric_version: 'caliper_item_rubric_v1',
    benchmark: 'GSM8K', deployment: 'Statistical analysis assistant', source_registry: { 'deployment.txt': 'Statistical analysis assistant' },
    classifiers: SCORE_DIMENSIONS.map(id => ({ id, component: id, operation: 'ordinal', applicable: true, question: `Assess ${id}`, ordinal_anchors: { '1': 'Fundamental mismatch', '5': 'Strong alignment' } })),
  }
  const items: Item[] = Array.from({ length: 25 }, (_, index) => ({
    item_id: `item-${index + 1}`, content: `Question ${index + 1}`, reference_answer: `Answer ${index + 1}`, status: 'complete', grading_criterion: 'Exact answer',
    dimensions: Object.fromEntries(SCORE_DIMENSIONS.map(id => [id, {
      score: id === 'input_ontology' && index >= 20 ? index === 24 ? null : 2 : 4,
      justification: `Reasoning for question ${index + 1}`, evidence: [`Evidence for question ${index + 1}`], information_gaps: index === 24 ? ['Missing deployment evidence'] : [],
    }])),
  }))
  const summaries: ClassifierSummary[] = spec.classifiers.map(classifier => {
    const scores = items.map(item => item.dimensions![classifier.id].score)
    const numeric = scores.filter((score): score is number => score !== null)
    return { ...classifier, known: numeric.length, unknown: scores.length - numeric.length, pending: 0, errors: 0,
      mean_score: numeric.reduce((total, score) => total + score, 0) / numeric.length,
      counts: Object.fromEntries([1, 2, 3, 4, 5].map(score => [String(score), numeric.filter(value => value === score).length])),
    }
  })
  return {
    items, spec,
    summary: {
      analysis_type: 'six_scores', total_items: 1319, completed_items: 25, error_items: 0, pending_items: 1294, complete_snapshot: false,
      classifiers: summaries, dimensions: summaries,
      experiment: { classifier_count: 6, selected_items: 25, selected_completed_items: 25, completed_item_classifier_judgments: 150, expected_item_classifier_judgments: 150 },
      original_assessment: Object.fromEntries(SCORE_DIMENSIONS.map(id => [id, { score: 1, justification: 'Original benchmark reasoning' }])),
    },
    manifest: { run_id: 'saved-run', deployment: spec.deployment, model: { model_id: 'saved-model' } },
    dataset: { seed: 42, source: { repo: 'dataset-repository', revision: 'immutable-revision' } },
    originalAssessment: { scoring: {} },
  }
}

const respond = (data = snapshot()) => ({ ok: true, json: async () => data })

beforeEach(() => {
  localStorage.clear()
  sessionStorage.clear()
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(respond()))
})
afterEach(() => { vi.restoreAllMocks(); vi.unstubAllGlobals() })

it('shows published scores and evidence without restoring private runs or requesting an API key', async () => {
  const user = userEvent.setup()
  const privateAccess = JSON.stringify({ run_id: 'private-run', run_secret: 'private-secret' })
  localStorage.setItem('item_analysis_run_v1:gallery:gsm8k', privateAccess)
  const onRunOwnAnalysis = vi.fn()
  render(<SavedItemAnalysis assessmentId="gsm8k" onRunOwnAnalysis={onRunOwnAnalysis} />)
  expect(screen.getByRole('status')).toHaveTextContent('Loading saved item analysis')
  expect(await screen.findByText('25-item sample complete')).toBeVisible()
  expect(screen.queryByLabelText(/API key/i)).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: /Prepare|Continue analysis|Stop analysis|Discard/i })).not.toBeInTheDocument()
  expect(screen.queryByText(/Explore the individual questions behind/)).not.toBeInTheDocument()
  expect(screen.queryByText('Human review')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'item-1 · Input Ontology: 4' }))
  const evidence = screen.getByRole('region', { name: 'Selected score details' })
  expect(evidence).toHaveTextContent('Reasoning for question 1')
  expect(evidence).toHaveTextContent('Evidence for question 1')
  expect(evidence).toHaveTextContent('Exact answer')
  expect(localStorage.getItem('item_analysis_run_v1:gallery:gsm8k')).toBe(privateAccess)
  expect(fetch).toHaveBeenCalledTimes(1)
  expect(fetch).toHaveBeenCalledWith('/benchmark-caliper/api/gallery/gsm8k/item-analysis', expect.objectContaining({ signal: expect.any(AbortSignal) }))
  expect(onRunOwnAnalysis).not.toHaveBeenCalled()
  await user.click(screen.getByRole('button', { name: 'Run your own analysis' }))
  expect(onRunOwnAnalysis).toHaveBeenCalledOnce()
  expect(screen.getByRole('heading', { name: 'Saved item analysis' })).toBeVisible()
  expect(fetch).toHaveBeenCalledTimes(1)
})

it('filters across all published pages and keeps averages independent of the visible items', async () => {
  const user = userEvent.setup()
  render(<SavedItemAnalysis assessmentId="gsm8k" onRunOwnAnalysis={vi.fn()} />)
  const table = await screen.findByRole('table', { name: /Item scores/ })
  const averages = screen.getByRole('table', { name: 'Dimension averages and benchmark scores' })
  const originalAverages = averages.textContent
  expect(within(averages).getByText('3.67 / 5')).toBeVisible()
  expect(within(table).getAllByRole('row')).toHaveLength(22)
  expect(within(table).queryByText('item-21')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Next' }))
  expect(screen.getByText('Page 2 of 2')).toBeVisible()
  expect(within(table).getByText('item-21')).toBeVisible()
  expect(within(table).getAllByRole('row')).toHaveLength(7)
  await user.click(screen.getByRole('button', { name: 'Low scores (1–2)' }))
  expect(screen.getByRole('status')).toHaveTextContent('4 matching items across selected items')
  expect(within(table).getByText('item-21')).toBeVisible()
  expect(within(table).queryByText('item-1')).not.toBeInTheDocument()
  expect(within(table).getAllByRole('row')).toHaveLength(6)
  expect(averages.textContent).toBe(originalAverages)
  await user.click(screen.getByRole('button', { name: 'Unknown scores' }))
  expect(screen.getByRole('status')).toHaveTextContent('1 matching item across selected items')
  expect(within(table).getByText('item-25')).toBeVisible()
  expect(averages.textContent).toBe(originalAverages)
  await user.click(screen.getByRole('button', { name: 'Clear filter' }))
  expect(screen.getByText('Page 1 of 2')).toBeVisible()
  expect(within(table).getByText('item-1')).toBeVisible()
  expect(averages.textContent).toBe(originalAverages)
})

it('keeps distributions collapsed above averages and inspects a dimension across all pages', async () => {
  const user = userEvent.setup()
  const scroll = vi.fn()
  vi.spyOn(Element.prototype, 'scrollIntoView').mockImplementation(scroll)
  render(<SavedItemAnalysis assessmentId="gsm8k" onRunOwnAnalysis={vi.fn()} />)
  await screen.findByText('25-item sample complete')
  const distributionToggle = screen.getByText('Score distributions and original benchmark assessment')
  expect(distributionToggle.closest('details')).not.toHaveAttribute('open')
  const averages = screen.getByRole('region', { name: 'Average item scores' })
  expect(distributionToggle.compareDocumentPosition(averages) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  expect(averages.nextElementSibling).toBe(screen.getByRole('region', { name: 'Save and share results' }))
  await user.click(screen.getByRole('button', { name: 'Next' }))
  await user.click(distributionToggle)
  await user.click(screen.getByRole('button', { name: 'Inspect low scores (4)' }))
  expect(screen.getByRole('status')).toHaveTextContent('4 matching items across selected items. Dimension: Input Ontology')
  expect(screen.getByRole('button', { name: 'item-21 · Input Ontology: 2' })).toBeVisible()
  await waitFor(() => expect(scroll).toHaveBeenCalledWith({ block: 'start' }))
  expect(document.activeElement).toHaveClass('saved-ia-items')
  await user.click(screen.getByText('Original six-dimension assessment'))
  expect(screen.getAllByText('Original benchmark reasoning')).toHaveLength(6)
})

it('offers public prefixed downloads and preserves the full-snapshot scope in explanatory text', async () => {
  const user = userEvent.setup()
  render(<SavedItemAnalysis assessmentId="saved entry" onRunOwnAnalysis={vi.fn()} />)
  await screen.findByText('25-item sample complete')
  const exports = screen.getByRole('region', { name: 'Save and share results' })
  expect(exports).toHaveTextContent('all 1,319 prepared rows')
  expect(exports).toHaveTextContent('only the 25 evaluated items')
  await user.click(within(exports).getByText('Individual files'))
  for (const [name, artifact] of [
    ['View exported report', 'report'], ['Download complete results package', 'package'],
    ['Evaluated item scores CSV', 'items'], ['Summary JSON', 'summary'], ['Shared context JSON', 'spec'], ['Original HTML report', 'report'],
  ]) {
    expect(within(exports).getByRole('link', { name })).toHaveAttribute('href', `/benchmark-caliper/api/gallery/saved%20entry/item-analysis/artifacts/${artifact}`)
  }
  expect(within(exports).getByRole('link', { name: 'Download complete results package' })).toHaveAttribute('download')
})

it('recovers from loading failure through an explicit retry', async () => {
  const user = userEvent.setup()
  vi.mocked(fetch).mockResolvedValueOnce({ ok: false, status: 503 } as Response)
  render(<SavedItemAnalysis assessmentId="gsm8k" onRunOwnAnalysis={vi.fn()} />)
  expect(await screen.findByRole('alert')).toHaveTextContent('Could not load the saved item analysis (503)')
  await user.click(screen.getByRole('button', { name: 'Retry loading saved analysis' }))
  expect(await screen.findByText('25-item sample complete')).toBeVisible()
  expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  expect(fetch).toHaveBeenCalledTimes(2)
})

it('does not show an earlier assessment when an outdated request finishes after navigation', async () => {
  let resolveFirst!: (value: Response) => void
  vi.mocked(fetch).mockReturnValueOnce(new Promise<Response>(resolve => { resolveFirst = resolve }))
  const view = render(<SavedItemAnalysis assessmentId="first" onRunOwnAnalysis={vi.fn()} />)
  view.rerender(<SavedItemAnalysis assessmentId="second" onRunOwnAnalysis={vi.fn()} />)
  await screen.findByText('25-item sample complete')
  const outdated = snapshot()
  outdated.items = outdated.items.slice(0, 1)
  outdated.summary.experiment!.selected_items = 1
  resolveFirst(respond(outdated) as Response)
  await waitFor(() => expect(vi.mocked(fetch).mock.calls[0][1]?.signal?.aborted).toBe(true))
  expect(screen.getByText('25-item sample complete')).toBeVisible()
  expect(screen.queryByText('1-item sample complete')).not.toBeInTheDocument()
})
