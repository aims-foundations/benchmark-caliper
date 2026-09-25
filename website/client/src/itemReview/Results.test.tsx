import { expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Results } from './Results'
import { DIMENSIONS, type DimensionScore, type Review } from './api'

const supported: DimensionScore = { score: 4, confidence: 'high', confidence_rationale: 'The text directly supports this rating.',
  justification: 'This fits the deployment.', evidence: ['item.content'], information_gaps: [] }
const partial = Object.fromEntries(DIMENSIONS.map(([name]) => [name, supported]))
partial.output_content = { score: null, confidence: 'insufficient', confidence_rationale: 'No reference answer was supplied.',
  justification: 'The reference cannot be judged.', evidence: [], information_gaps: ['Reference answer missing'] }
const review: Review = {
  run_id: 'fixture', status: 'completed', message: 'Ready', model: 'gpt-6-luna', reasoning_effort: 'high',
  deployment: { task: 'Tutor', users: 'Students', inputs: 'Text', outputs: 'Text', success: 'Correct', constraints: '' },
  scope: { benchmarks: ['matharena'], items_per_table: 1, branches: { main: 'a' }, sample_only: true },
  scoring_policy: { version: 2, neutral_score: 3, confidence_weights: { high: 1, medium: .6, low: .3, insufficient: 0 }, formula: 'test policy' },
  source_rows: 1, total: 1, processed: 1, complete: 1, needs_review: 1, errors: 0, usage: {}, failed_items: [],
  ranked_items: [{ evidence_hash: 'fixture', rank: 1, status: 'complete', overall_score: 23 / 6, compatibility_score: 4,
    scored_dimensions: 5, needs_review: true, assessment: partial,
    evidence: { item: { content: 'Solve 2x + 3 = 7. Explain your reasoning.', grading_criterion: null } },
    sources: [{ benchmark: 'matharena', branch: 'main', commit: 'a', repo: 'fixture', items_path: 'items', item_id: '1', row: 0 }] }],
}

it('keeps a partial assessment ranked and exposes missing evidence alongside the original scores', async () => {
  render(<Results review={review} />)
  const item = screen.getByRole('article', { name: 'Item 1' })
  expect(within(item).getByRole('region', { name: 'Full evaluation item' })).toHaveTextContent('Solve 2x + 3 = 7.')
  expect(within(item).getByLabelText('Item score')).toHaveTextContent('3.83 / 5')
  expect(within(item).getByLabelText('Item score')).toHaveTextContent('Dimensions scored5 / 6')
  expect(within(item).getByText('Insufficient evidence')).toBeVisible()
  expect(screen.queryByText('Unranked')).not.toBeInTheDocument()
  await userEvent.click(within(item).getByText('Read the scores, confidence, and evidence'))
  expect(within(item).getByText('Reference answer missing')).toBeVisible()
  expect(within(item).getByText('No reference answer was supplied.', { exact: false })).toBeVisible()
})

it('labels an all-unknown score as a baseline rather than observed compatibility', () => {
  const unknown = Object.fromEntries(DIMENSIONS.map(([name]) => [name, partial.output_content]))
  render(<Results review={{ ...review, ranked_items: [{ ...review.ranked_items[0], assessment: unknown,
    overall_score: 3, compatibility_score: null, scored_dimensions: 0 }] }} />)
  expect(screen.getByText('No scorable evidence')).toBeVisible()
  expect(screen.getByText('Neutral baseline')).toBeVisible()
  expect(screen.getByText('Not evidence of compatibility')).toBeVisible()
})

it('downloads confidence, gaps, and the scoring policy with the report', async () => {
  let blob: Blob | undefined
  const create = vi.spyOn(URL, 'createObjectURL').mockImplementation(value => { blob = value as Blob; return 'blob:test' })
  const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  render(<Results review={review} />)
  await userEvent.click(screen.getByRole('button', { name: 'Download results' }))
  const exported = JSON.parse(await blob!.text())
  expect(exported.scoring_policy.version).toBe(2)
  expect(exported.ranked_items[0].assessment.output_content.confidence).toBe('insufficient')
  expect(exported.ranked_items[0].assessment.output_content.information_gaps).toEqual(['Reference answer missing'])
  create.mockRestore()
  click.mockRestore()
})
