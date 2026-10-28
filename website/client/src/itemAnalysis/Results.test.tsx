import { expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { buildDemoItemAnalysisRun } from '../demo/itemAnalysisFixture'
import { ItemJudgments, matchesItemFilter, ProcessingCounts, ResultExports, SummaryFindings } from './Results'
import type { Item } from './types'

it('keeps processing counts out of the scientific findings panel', () => {
  const run = buildDemoItemAnalysisRun('sample')
  const { unmount } = render(<SummaryFindings run={run} />)
  expect(screen.getByRole('heading', { name: 'What the items show' })).toBeInTheDocument()
  expect(screen.queryByText('Saved classifier judgments')).not.toBeInTheDocument()
  expect(screen.getByText(/No issue identified is a bounded finding/)).toBeInTheDocument()
  expect(screen.getAllByText('10 valid judgments')).toHaveLength(4)
  expect(screen.getByText('Which tasks, skills, or situations required by the deployment does each input represent?')).toBeInTheDocument()
  unmount()
  render(<ProcessingCounts run={run} />)
  expect(screen.getByText('Saved classifier judgments')).toBeInTheDocument()
  expect(screen.getByText(/do not measure scientific validity or human-review completion/)).toBeInTheDocument()
  expect(screen.queryByRole('heading', { name: 'What the items show' })).not.toBeInTheDocument()
})

it('opens the matching dimension filter from summary findings', async () => {
  const user = userEvent.setup()
  const run = buildDemoItemAnalysisRun('sample')
  const input = run.summary!.classifiers.find(classifier => classifier.id === 'input_content')!
  input.counts = { issue_identified: 2, no_issue_identified: 0, insufficient_evidence: 8 }
  input.insufficient_evidence = 8
  const onInspect = vi.fn()
  render(<SummaryFindings run={run} onInspect={onInspect} />)
  const dimension = screen.getByRole('heading', { name: 'Input Content' }).closest('article')!
  await user.click(within(dimension).getByRole('button', { name: 'Inspect flagged items (2)' }))
  expect(onInspect).toHaveBeenLastCalledWith({ kind: 'flagged', classifierId: 'input_content' })
  await user.click(within(dimension).getByRole('button', { name: 'Inspect uncertain items (8)' }))
  expect(onInspect).toHaveBeenLastCalledWith({ kind: 'uncertain', classifierId: 'input_content' })
})

it('uses live processing counters while a phase runs and keeps earlier summary findings separate', () => {
  const run = buildDemoItemAnalysisRun('pilot')
  run.status = 'running'
  run.scope = 'all'
  run.completed_judgments = 23
  run.remaining_judgments = { pilot: 0, all: 17 }
  run.complete = 5
  const { unmount } = render(<ProcessingCounts run={run} />)
  expect(screen.getByText('Saved classifier judgments').parentElement).toHaveTextContent('23Saved classifier judgmentsof 40 expected')
  expect(screen.getByText('Selected items').parentElement).toHaveTextContent('10Selected items')
  expect(screen.getByText('Missing classifier judgments').parentElement).toHaveTextContent('17Missing classifier judgments')
  unmount()
  render(<SummaryFindings run={run} />)
  expect(screen.getByText(/Summary statistics update when this classification phase finishes/)).toBeInTheDocument()
  expect(screen.queryByRole('heading', { name: 'What the items show' })).not.toBeInTheDocument()
})

it('distinguishes flags, uncertain judgments, and failures without treating pending items as uncertain', () => {
  const judgment = { justification: 'Explanation', evidence: ['Evidence'] }
  const item: Item = { item_id: 'one', content: 'Example', reference_answer: null, status: 'partial', labels: {
    input_ontology: { ...judgment, label: 'no_match' },
    input_content: { ...judgment, label: 'insufficient_evidence' },
    output_content: { ...judgment, label: 'no_issue_identified' },
  } }
  expect(matchesItemFilter(item, { kind: 'flagged' })).toBe(true)
  expect(matchesItemFilter(item, { kind: 'flagged', classifierId: 'output_content' })).toBe(false)
  expect(matchesItemFilter(item, { kind: 'uncertain', classifierId: 'input_content' })).toBe(true)
  expect(matchesItemFilter(item, { kind: 'uncertain', classifierId: 'output_ontology' })).toBe(false)
  expect(matchesItemFilter(item, { kind: 'retry' })).toBe(false)
  expect(matchesItemFilter({ ...item, classifier_errors: { output_ontology: 'Retry required' } }, { kind: 'retry', classifierId: 'output_ontology' })).toBe(true)
  expect(matchesItemFilter({ ...item, labels: undefined }, { kind: 'uncertain' })).toBe(false)
})

it('paginates cross-page filter matches and keeps evidence and identifiers collapsed', async () => {
  const user = userEvent.setup()
  const run = buildDemoItemAnalysisRun('sample')
  const matches = Array.from({ length: 23 }, (_, index) => ({ ...run.items[0], item_id: `saved-${index}`, content: `Matched item ${index + 1}` }))
  const setPage = vi.fn()
  const onFilterChange = vi.fn()
  render(<ItemJudgments run={run} page={2} setPage={setPage} pageLoading={false} filter={{ kind: 'uncertain', classifierId: 'input_content' }} filteredItems={matches} onFilterChange={onFilterChange} />)
  expect(document.querySelectorAll('details.ia-item')).toHaveLength(3)
  expect(screen.getByText(/23 matching items across selected items/)).toBeInTheDocument()
  expect(screen.getByText('Page 2 of 2')).toBeInTheDocument()
  expect(screen.queryByText('Matched item 1')).not.toBeInTheDocument()
  const card = document.querySelector('details.ia-item')!
  expect(card.querySelector('summary')!).not.toHaveTextContent('saved-20')
  await user.click(card.querySelector('summary')!)
  expect(within(card as HTMLElement).getAllByRole('heading', { level: 4 })).toHaveLength(4)
  expect((within(card as HTMLElement).getByText('Item identifier').closest('details') as HTMLDetailsElement).open).toBe(false)
  const disclosure = within(card as HTMLElement).getAllByText('Evidence and full explanation')[0].closest('details') as HTMLDetailsElement
  expect(disclosure.open).toBe(false)
  await user.click(disclosure.querySelector('summary')!)
  expect(disclosure.open).toBe(true)
  await user.click(screen.getByRole('button', { name: 'Previous' }))
  expect(setPage).toHaveBeenCalledWith(1)
  await user.click(screen.getByRole('button', { name: 'Clear filter' }))
  expect(onFilterChange).toHaveBeenCalledWith({ kind: 'all' })
})

it('keeps saved judgments inspectable while another dimension needs retry', () => {
  const run = buildDemoItemAnalysisRun('sample')
  const first = run.items[0]
  run.items = [{ ...first, status: 'error', labels: { input_ontology: first.labels!.input_ontology }, classifier_errors: { input_content: 'The request failed.' } }]
  render(<ItemJudgments run={run} page={1} setPage={vi.fn()} pageLoading={false} />)
  expect(screen.getAllByRole('heading', { level: 4 })).toHaveLength(4)
  expect(screen.getByText('match')).toBeInTheDocument()
  expect(screen.getByText('The request failed.')).toBeInTheDocument()
  expect(screen.getByText(/Completed classifier judgments are saved/)).toBeInTheDocument()
  expect(screen.getAllByText('Pending')).toHaveLength(2)
})

it('groups downloads and explains external human review without claiming completion', async () => {
  const user = userEvent.setup()
  const run = buildDemoItemAnalysisRun('sample')
  const onDownload = vi.fn()
  const onViewReport = vi.fn()
  const onDownloadPackage = vi.fn()
  render(<ResultExports run={run} onDownload={onDownload} onViewReport={onViewReport} onDownloadPackage={onDownloadPackage} downloading={null} />)
  expect(screen.getByText('Human review has not been recorded here.')).toBeInTheDocument()
  expect(screen.getByText(/website does not import completed worksheets/)).toBeInTheDocument()
  expect(within(screen.getByRole('region', { name: 'External human review' })).getAllByRole('listitem')).toHaveLength(4)
  await user.click(screen.getByRole('button', { name: /View report/ }))
  expect(onViewReport).toHaveBeenCalledOnce()
  await user.click(screen.getByRole('button', { name: /Download complete results package/ }))
  expect(onDownloadPackage).toHaveBeenCalledOnce()
  await user.click(screen.getByRole('button', { name: /Download blind review worksheet/ }))
  expect(onDownload).toHaveBeenCalledWith('review')
  expect((screen.getByText('Individual files').closest('details') as HTMLDetailsElement).open).toBe(false)
})

it('keeps the immutable specification downloadable while result exports await a running phase', async () => {
  const user = userEvent.setup()
  const run = buildDemoItemAnalysisRun('pilot')
  run.status = 'running'
  const onDownload = vi.fn()
  render(<ResultExports run={run} onDownload={onDownload} onDownloadPackage={vi.fn()} onViewReport={vi.fn()} downloading={null} />)
  await user.click(screen.getByText('Individual files'))
  expect(screen.getByRole('button', { name: /Criteria JSON/ })).toBeEnabled()
  expect(screen.getByRole('button', { name: /Item labels CSV/ })).toBeDisabled()
  expect(screen.getByRole('button', { name: /Download complete results package/ })).toBeDisabled()
  expect(screen.getByRole('button', { name: /View report/ })).toBeDisabled()
  await user.click(screen.getByRole('button', { name: /Criteria JSON/ }))
  expect(onDownload).toHaveBeenCalledWith('spec')
})
