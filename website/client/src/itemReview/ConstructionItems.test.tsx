import { useCallback, useState } from 'react'
import { afterEach, expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ConstructionItems } from './ConstructionItems'
import { type ScreenedItem } from './api'
import type { ConstructionSnapshot } from './constructionTypes'

const summaries = Array.from({ length: 73 }, (_, index) => ({
  item_id: `record-${index}`, index, question_preview: `Which action fits case ${index}?`, preview_kind: 'question' as const,
  status: 'complete' as const, gate: index === 2 || index === 3 ? 'pass' as const : 'fail' as const,
  matched_facet_ids: ['management'], sources: ['exam_bank'], selected: index === 2, initial: index < 48, quality_score: 4,
}))
const snapshot = {
  entry: { id: 'example' }, items: summaries,
  review: { selection: { selected_item_ids: ['record-2'] }, requirements: { task_facets: [{ facet_id: 'management', task: { text: 'Choose management' } }], coverage_requirements: [] }, screening: { policy: { minimum_score: 3 }, items: [] } },
} as unknown as ConstructionSnapshot
const finding = { justification: 'Recorded reason.', evidence: ['Keep original — and · punctuation.'], information_gaps: [] }
const rating = { ...finding, score: 4 }
const fullItem = (index: number): ScreenedItem => ({
  item_id: `record-${index}`, status: 'complete', question_text: `Full original question ${index}.\n<script>Keep literal source content.</script>`,
  search_text: 'Search data', rank: 1, dense_rank: 1, bm25_rank: 1, dense_score: 1, bm25_score: 1, rrf_score: 1,
  evidence: { item: { original: index } }, sources: [{ benchmark: 'exam_bank', branch: 'main' }], acquisition: { queue_id: 'management:exam_bank', facet_id: 'management' }, evidence_hash: `hash-${index}`,
  gate: { status: index === 2 || index === 3 ? 'pass' : 'fail', reasons: ['The recorded gate explanation.'] },
  assessment: { task: { ...finding, status: 'matched', decision: 'Choose the appropriate action.', matched_facet_ids: ['management'] }, ratings: { input_ontology: rating, input_content: rating, input_form: rating, output_ontology: rating, output_content: rating, output_form: rating }, coverage: [] },
})

function Browser({ focusedItemId, initialPhase = null }: { focusedItemId?: string; initialPhase?: 'all' | 'initial' | 'adaptive' | null }) {
  const [loaded, setLoaded] = useState(() => new Map<string, ScreenedItem>())
  const onLoad = useCallback((item: ScreenedItem) => setLoaded(previous => new Map(previous).set(item.item_id, item)), [])
  return <ConstructionItems snapshot={snapshot} loadedItems={loaded} onLoad={onLoad} initialPhase={initialPhase} focusedItemId={focusedItemId} />
}

afterEach(() => { vi.unstubAllGlobals() })

it('keeps selected items complete when returning from filtered and paginated assessments', async () => {
  const user = userEvent.setup()
  const fetch = vi.fn()
  vi.stubGlobal('fetch', fetch)
  render(<Browser />)
  expect(screen.getByRole('heading', { name: 'Selected items (1)' })).toBeVisible()
  expect(screen.getByRole('button', { name: 'Selected items (1)' })).toHaveAttribute('aria-pressed', 'true')
  expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
  expect(screen.getByText('Which action fits case 2?')).toBeVisible()
  expect(screen.getByText('Quality Q:').parentElement).toHaveTextContent('4.00 / 5')
  expect(screen.queryByText('Which action fits case 3?')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'All screened items (73)' }))
  await user.click(screen.getByRole('button', { name: 'Next items' }))
  expect(screen.getByRole('status')).toHaveTextContent('Page 2 of 8.')
  await user.selectOptions(screen.getByLabelText('Screening stage'), 'adaptive')
  await user.selectOptions(screen.getByLabelText('Eligibility result'), 'fail')
  expect(screen.getByRole('status')).toHaveTextContent('25 matching items. Page 1 of 3.')
  await user.click(screen.getByRole('button', { name: 'Selected items (1)' }))
  expect(screen.getByText('Which action fits case 2?')).toBeVisible()
  expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'All screened items (73)' }))
  expect(screen.getByLabelText('Screening stage')).toHaveValue('all')
  expect(screen.getByLabelText('Eligibility result')).toHaveValue('all')
  expect(screen.getByRole('status')).toHaveTextContent('73 matching items. Page 1 of 8.')
  expect(fetch).not.toHaveBeenCalled()
})

it('loads only an opened item, shows its exact content first, and caches the assessment', async () => {
  const user = userEvent.setup()
  const fetch = vi.fn(async (_path: string) => new Response(JSON.stringify(fullItem(0))))
  vi.stubGlobal('fetch', fetch)
  render(<Browser />)
  await user.click(screen.getByRole('button', { name: 'All screened items (73)' }))
  await user.click(screen.getByText('Screened item 1'))
  await screen.findByRole('heading', { name: 'Eligibility result' })
  expect(fetch).toHaveBeenCalledTimes(1)
  expect(fetch.mock.calls[0][0]).toBe('/api/item-review/examples/example/items/record-0')
  const content = screen.getByRole('heading', { name: 'Item content' }).closest('section')!
  expect(content.parentElement?.firstElementChild).toBe(content)
  expect(within(content).queryByRole('button')).not.toBeInTheDocument()
  expect(screen.getByText(/Full original question 0/, { selector: 'p' }).textContent).toBe(fullItem(0).question_text)
  expect(document.querySelector('script')).toBeNull()
  await user.click(screen.getByText('Screening explanations and supporting evidence'))
  expect(screen.getAllByText('Keep original — and · punctuation.')[0]).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Next items' }))
  await user.click(screen.getByRole('button', { name: 'Previous items' }))
  await user.click(screen.getByText('Screened item 1'))
  expect(screen.getByRole('heading', { name: 'Eligibility result' })).toBeVisible()
  expect(fetch).toHaveBeenCalledTimes(1)
})

it('reveals a linked off-page candidate even when the browser defaults to selected items', async () => {
  const fetch = vi.fn(async () => new Response(JSON.stringify(fullItem(67))))
  vi.stubGlobal('fetch', fetch)
  render(<Browser focusedItemId="record-67" />)
  const heading = await screen.findByRole('heading', { name: 'Eligibility result' })
  expect(screen.getByRole('button', { name: 'All screened items (73)' })).toHaveAttribute('aria-pressed', 'true')
  expect(screen.getByRole('status')).toHaveTextContent('73 matching items. Page 7 of 8.')
  expect(heading.closest('details')).toHaveAttribute('id', 'screened-item-record-67')
  expect(heading.closest('details')).toHaveAttribute('open')
  expect(fetch).toHaveBeenCalledTimes(1)
})

it('returns to the same linked item after filters hide it and the route moves away and back', async () => {
  const user = userEvent.setup()
  const fetch = vi.fn(async () => new Response(JSON.stringify(fullItem(67))))
  vi.stubGlobal('fetch', fetch)
  const { rerender } = render(<Browser focusedItemId="record-67" />)
  await screen.findByRole('heading', { name: 'Eligibility result' })
  await user.selectOptions(screen.getByLabelText('Screening stage'), 'initial')
  expect(screen.queryByText('Screened item 68')).not.toBeInTheDocument()
  rerender(<Browser />)
  rerender(<Browser focusedItemId="record-67" />)
  expect(await screen.findByRole('heading', { name: 'Eligibility result' })).toBeVisible()
  expect(screen.getByLabelText('Screening stage')).toHaveValue('all')
  expect(screen.getByRole('status')).toHaveTextContent('Page 7 of 8.')
  expect(document.getElementById('screened-item-record-67')).toHaveAttribute('open')
  expect(fetch).toHaveBeenCalledTimes(1)
})

it('labels a saved decision instead of displaying unclassified old instruction prefixes', () => {
  const legacy = structuredClone(snapshot)
  delete legacy.items[2].preview_kind
  legacy.items[2].question_preview = 'You are a skilled doctor. Follow these instructions.'
  render(<ConstructionItems snapshot={legacy} loadedItems={new Map([['record-2', fullItem(2)]])} onLoad={() => {}} initialPhase={null} />)
  expect(screen.getByText('Task identified during screening')).toBeVisible()
  expect(screen.getByText('Choose the appropriate action.')).toBeVisible()
  expect(screen.queryByText(/You are a skilled doctor/)).not.toBeInTheDocument()
})

it('expands long item content exactly without collapsing the inspection or moving ratings above it', async () => {
  const user = userEvent.setup()
  const item = fullItem(2)
  item.question_text = 'Keep spacing, punctuation — and · intact.\n  '.repeat(40)
  render(<ConstructionItems snapshot={snapshot} loadedItems={new Map([[item.item_id, item]])} onLoad={() => {}} initialPhase={null} />)
  await user.click(screen.getByText('Selected item 1'))
  const card = screen.getByText('Selected item 1').closest('details')!
  const heading = await within(card).findByRole('heading', { name: 'Item content' })
  const content = heading.closest('section')!
  expect(content.parentElement?.firstElementChild).toBe(content)
  expect(within(card).getByText('Quality Q:').parentElement).toHaveTextContent('4.00 / 5')
  const paragraph = content.querySelector('p')!
  expect(paragraph.textContent).toMatch(/\.\.\.$/)
  expect(item.question_text.startsWith(paragraph.textContent!.slice(0, -3))).toBe(true)
  const expand = within(content).getByRole('button', { name: 'Show full content' })
  expect(expand).toHaveAttribute('aria-expanded', 'false')
  expect(expand).toHaveAttribute('aria-controls', paragraph.id)
  await user.click(expand)
  expect(paragraph.textContent).toBe(item.question_text)
  expect(card).toHaveAttribute('open')
  await user.click(within(content).getByRole('button', { name: 'Show less' }))
  expect(paragraph.textContent).toMatch(/\.\.\.$/)
  expect(card).toHaveAttribute('open')
})

it('honors initial and adaptive phase routes without restricting a later selected view', async () => {
  const user = userEvent.setup()
  const { rerender } = render(<Browser initialPhase="initial" />)
  expect(screen.getByLabelText('Screening stage')).toHaveValue('initial')
  expect(screen.getByRole('status')).toHaveTextContent('48 matching items.')
  rerender(<Browser initialPhase="adaptive" />)
  expect(screen.getByLabelText('Screening stage')).toHaveValue('adaptive')
  expect(screen.getByRole('status')).toHaveTextContent('25 matching items.')
  await user.click(screen.getByRole('button', { name: 'Selected items (1)' }))
  expect(screen.getByText('Which action fits case 2?')).toBeVisible()
})
