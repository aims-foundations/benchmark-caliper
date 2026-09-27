import { expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Results } from './Results'
import { DIMENSIONS, getReviewExport, type DimensionScore, type Review } from './api'

vi.mock('./api', async importOriginal => ({
  ...await importOriginal<typeof import('./api')>(), getReviewExport: vi.fn(),
}))
const props = { run: { run_id: 'fixture', run_secret: 'private-access' }, onPageChange: vi.fn() }

const supported: DimensionScore = { score: 4, confidence: 0.93, confidence_rationale: 'The text directly supports this rating.',
  justification: 'This fits the deployment.', evidence: ['item.content'], information_gaps: [] }
const partial = Object.fromEntries(DIMENSIONS.map(([name]) => [name, supported]))
partial.output_content = { score: null, confidence: null, confidence_rationale: 'No reference answer was supplied.',
  justification: 'The reference cannot be judged.', evidence: [], information_gaps: ['Reference answer missing'] }
const review: Review = {
  run_id: 'fixture', status: 'completed', message: 'Ready', model: 'gpt-6-luna', reasoning_effort: 'high',
  deployment: { task: 'Tutor', users: 'Students', inputs: 'Text', outputs: 'Text', success: 'Correct', constraints: '' },
  scope: { benchmarks: ['matharena'], table_count: 1, source_rows: 1, branches: { main: 'a' }, sample_only: true,
    sampling: { version: 1, method: 'seeded_hash_with_branch_coverage', seed: 20260925, items_per_benchmark: 50 }, sample_max_items: 1 },
  sample_complete: true, prepared_benchmarks: 1, pagination: { page: 1, page_size: 20, total_pages: 1 },
  scoring_policy: { version: 5, formula: '1 + sum(confidence * (score - 1) for scored dimensions) / 6; no scored dimensions yields null' },
  source_rows: 1, total: 1, processed: 1, complete: 1, ranked: 1, unranked: 0, needs_review: 1, errors: 0, usage: {}, failed_items: [], unranked_items: [],
  ranked_items: [{ evidence_hash: 'fixture', rank: 1, status: 'complete', overall_score: 3.325, compatibility_score: 4,
    scored_dimensions: 5, needs_review: true, assessment: partial,
    evidence: { item: { content: 'Solve 2x + 3 = 7. Explain your reasoning.', grading_criterion: null } },
    sources: [{ benchmark: 'matharena', branch: 'main', commit: 'a', repo: 'fixture', items_path: 'items', item_id: '1', row: 0 }] }],
}

it('keeps a partial assessment ranked and exposes missing evidence alongside the original scores', async () => {
  render(<Results review={review} {...props} />)
  const item = screen.getByRole('article', { name: 'Item 1' })
  expect(within(item).getByRole('region', { name: 'Full evaluation item' })).toHaveTextContent('Solve 2x + 3 = 7.')
  expect(within(item).getByLabelText('Item score')).toHaveTextContent('Ranking score3.33 / 5')
  expect(within(item).getByLabelText('Item score')).toHaveTextContent('Compatibility mean4.00 / 5')
  expect(screen.queryByText('Unadjusted mean')).not.toBeInTheDocument()
  expect(screen.getByText('Adjusted for confidence')).toBeVisible()
  expect(within(item).getByLabelText('Item score')).toHaveTextContent('Dimensions scored5 / 6')
  expect(within(item).getAllByText('Insufficient evidence')[0]).toBeVisible()
  expect(within(item).getAllByText('Confidence 0.93')[0]).toBeVisible()
  expect(screen.queryByText('Unranked')).not.toBeInTheDocument()
  await userEvent.click(within(item).getByText('Assessment details'))
  expect(within(item).getByText('Reference answer missing')).toBeVisible()
  expect(within(item).getByText('No reference answer was supplied.', { exact: false })).toBeVisible()
})

it('retains an all-unknown assessment without a score or rank', () => {
  const unknown = Object.fromEntries(DIMENSIONS.map(([name]) => [name, partial.output_content]))
  render(<Results review={{ ...review, ranked: 0, unranked: 1, ranked_items: [],
    unranked_items: [{ ...review.ranked_items[0], rank: undefined, assessment: unknown,
      overall_score: null, compatibility_score: null, scored_dimensions: 0 }] }} {...props} />)
  expect(screen.getByRole('heading', { name: 'Items without scores' })).toBeVisible()
  expect(screen.getByRole('article', { name: 'Item without a score' })).toBeVisible()
  expect(screen.getByText('No scorable evidence')).toBeVisible()
  expect(screen.getByText('Items ranked').parentElement).toHaveTextContent('0')
  expect(screen.getByLabelText('Item score')).toHaveTextContent('Dimensions scored0 / 6')
  expect(screen.getByLabelText('Item score')).not.toHaveTextContent('/ 5')
  expect(screen.queryByText('Neutral baseline')).not.toBeInTheDocument()
})

it('explains the ranking adjustment and distinguishes missing evidence from mismatch', async () => {
  render(<Results review={review} {...props} />)
  await userEvent.click(screen.getByText('How to read these scores'))
  expect(screen.getByText('1 + confidence × (compatibility − 1)')).toBeVisible()
  expect(screen.getByText(/Missing dimensions contribute 1 to ranking only; their compatibility remains unknown/)).toBeVisible()
  expect(screen.getByText(/not a calibrated probability or statistical lower bound/)).toBeVisible()
  expect(screen.queryByText(/does not change the score/)).not.toBeInTheDocument()
})

it('preserves the unadjusted numerical scoring of version 4 reports', async () => {
  render(<Results review={{ ...review,
    scoring_policy: { version: 4, formula: 'mean(available dimension scores); no scored dimensions yields null' },
    ranked_items: [{ ...review.ranked_items[0], overall_score: 4 }] }} {...props} />)
  expect(screen.getByLabelText('Item score')).toHaveTextContent('Compatibility score4.00 / 5')
  expect(screen.queryByText('Compatibility mean')).not.toBeInTheDocument()
  expect(screen.queryByText('Adjusted for confidence')).not.toBeInTheDocument()
  expect(screen.getAllByText('Confidence 0.93')[0]).toBeVisible()
  await userEvent.click(screen.getByText('How to read these scores'))
  expect(screen.getByText(/Confidence describes evidence support and does not change the score/)).toBeVisible()
  expect(screen.getByText(/Missing dimensions are excluded/)).toBeVisible()
  expect(screen.queryByText('1 + confidence × (compatibility − 1)')).not.toBeInTheDocument()
})

it.each([2, 3])('preserves categorical confidence in version %i reports', async version => {
  const categorical = Object.fromEntries(Object.entries(partial).map(([name, dimension]) => [name, {
    ...dimension, confidence: dimension.score == null ? 'insufficient' : 'high',
  } satisfies DimensionScore]))
  render(<Results review={{ ...review,
    scoring_policy: { version, neutral_score: 3, confidence_weights: { high: 1, medium: .6, low: .3, insufficient: 0 }, formula: 'legacy' },
    ranked_items: [{ ...review.ranked_items[0], assessment: categorical, overall_score: version === 2 ? 23 / 6 : 4 }] }} {...props} />)
  expect(screen.getByLabelText('Item score')).toHaveTextContent(version === 2 ? '3.83 / 5' : '4.00 / 5')
  expect(screen.getAllByText('High confidence')[0]).toBeVisible()
  expect(screen.getAllByText('Insufficient evidence')[0]).toBeVisible()
  expect(screen.queryByText('Confidence 0.93')).not.toBeInTheDocument()
  expect(screen.queryByText('Compatibility mean')).not.toBeInTheDocument()
  await userEvent.click(screen.getByText('How to read these scores'))
  if (version === 2) expect(screen.getByText(/This report uses an earlier scoring policy/)).toBeVisible()
  expect(screen.queryByText(/The model reports it from 0 to 1/)).not.toBeInTheDocument()
})

it.each([0, 0.7, 1])('displays numerical confidence %s without converting it to a category', confidence => {
  const assessment = { ...partial, input_form: { ...supported, confidence } }
  render(<Results review={{ ...review, ranked_items: [{ ...review.ranked_items[0], assessment }] }} {...props} />)
  expect(screen.getAllByText(`Confidence ${confidence.toFixed(2)}`)[0]).toBeVisible()
  expect(screen.queryByText('High confidence')).not.toBeInTheDocument()
  expect(screen.getByLabelText('Item score')).toHaveTextContent('Compatibility mean4.00 / 5')
})

it('downloads confidence, gaps, and the scoring policy with the report', async () => {
  let blob: Blob | undefined
  const create = vi.spyOn(URL, 'createObjectURL').mockImplementation(value => { blob = value as Blob; return 'blob:test' })
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  vi.mocked(getReviewExport).mockResolvedValue(new Blob([JSON.stringify(review)], { type: 'application/json' }))
  render(<Results review={review} {...props} />)
  await userEvent.click(screen.getByRole('button', { name: 'Download all results' }))
  expect(getReviewExport).toHaveBeenCalledWith(props.run)
  const exported = JSON.parse(await blob!.text())
  expect(exported.scoring_policy.version).toBe(5)
  expect(exported.scoring_policy.confidence_weights).toBeUndefined()
  expect(exported.ranked_items[0].overall_score).toBe(3.325)
  expect(exported.ranked_items[0].compatibility_score).toBe(4)
  expect(exported.ranked_items[0].assessment.input_form.confidence).toBe(0.93)
  expect(exported.ranked_items[0].assessment.output_content.confidence).toBeNull()
  expect(exported.ranked_items[0].assessment.output_content.information_gaps).toEqual(['Reference answer missing'])
  create.mockRestore()
  click.mockRestore()
})

it('navigates result pages and returns directly to the highest scores', async () => {
  const { rerender } = render(<Results review={{ ...review, status: 'running', sample_complete: false, pagination: { page: 1, page_size: 20, total_pages: 3 } }} {...props} />)
  expect(screen.getByText('Highest score first · Updating as items finish')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Previous page' })).toBeDisabled()
  await userEvent.click(screen.getByRole('button', { name: 'Next page' }))
  expect(props.onPageChange).toHaveBeenCalledWith(2)
  rerender(<Results review={{ ...review, pagination: { page: 2, page_size: 20, total_pages: 3 } }} {...props} />)
  await userEvent.click(screen.getByRole('button', { name: 'Back to top scores' }))
  expect(props.onPageChange).toHaveBeenLastCalledWith(1)
})
