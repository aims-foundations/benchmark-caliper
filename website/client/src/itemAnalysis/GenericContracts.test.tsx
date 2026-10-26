import { expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { buildDemoItemAnalysisRun, DEMO_ITEM_ANALYSIS_SPEC } from '../demo/itemAnalysisFixture'
import { Criteria } from './Criteria'
import { Results } from './Results'

it('shows immutable rules, partial inventory boundaries and cited context for all four classifiers', () => {
  render(<Criteria spec={DEMO_ITEM_ANALYSIS_SPEC} />)
  expect(screen.getByText('4 active classifiers')).toBeInTheDocument()
  expect(screen.getByText(/caliper_generic_items_v1/)).toBeInTheDocument()
  expect(screen.getByText('Required categories · partial inventory')).toBeInTheDocument()
  expect(screen.getByText('A partial or unknown inventory does not make an unmatched item out of scope.')).toBeInTheDocument()
  expect(screen.getByText(/Uniform multiple-choice representation/)).toBeInTheDocument()
  expect(screen.getAllByText('Sourced context and evidence gaps')).toHaveLength(4)
})

it('renders actual generic summary fields and includes insufficient evidence in percentage denominators', () => {
  const run = buildDemoItemAnalysisRun('sample')
  // The API uses these modern fields; legacy known/unknown values are absent.
  expect(run.summary!.classifiers.every(classifier => classifier.known === undefined)).toBe(true)
  run.summary!.experiment!.completed_item_classifier_judgments = 39
  render(<Results run={run} page={1} setPage={vi.fn()} onDownload={vi.fn()} downloading={null} pageLoading={false} />)
  expect(screen.getByText('39 completed item-classifier judgments across 4 classifiers.')).toBeInTheDocument()
  const heading = screen.getByRole('heading', { name: 'Input Content', level: 3 })
  const distribution = heading.closest('article')!
  expect(within(distribution).getByText(/0 sufficient evidence · 10 insufficient evidence/)).toBeInTheDocument()
  expect(within(distribution).getByText('100.0%')).toBeInTheDocument()
  expect(screen.getAllByText('Matched categories: required_001')).toHaveLength(10)
})

it('does not offer a review worksheet before a run selects items', () => {
  const run = buildDemoItemAnalysisRun('sample')
  run.status = 'ready'
  run.processed = 0
  run.summary!.experiment!.selected_items = 0
  render(<Results run={run} page={1} setPage={vi.fn()} onDownload={vi.fn()} downloading={null} pageLoading={false} />)
  expect(screen.getByRole('button', { name: /Download blind review worksheet/ })).toBeDisabled()
})

it('shows saved dimensions on a partially failed item and identifies the dimension to retry', () => {
  const run = buildDemoItemAnalysisRun('sample')
  run.status = 'failed'
  run.complete = 9
  run.errors = 1
  const partial = { ...run.items[0], status: 'error', labels: { ...run.items[0].labels },
    classifier_errors: { input_content: 'No valid judgment was saved. Retry this phase.' },
    error: 'Some classifiers need a retry. Saved judgments are retained.' }
  delete partial.labels.input_content
  run.items = [partial]
  render(<Results run={run} page={1} setPage={vi.fn()} onDownload={vi.fn()} downloading={null} pageLoading={false} />)
  const content = screen.getByRole('heading', { name: 'Input Content', level: 4 }).closest('section')!
  expect(within(content).getByText('Needs retry')).toBeInTheDocument()
  expect(within(content).getByText('No valid judgment was saved. Retry this phase.')).toBeInTheDocument()
  const ontology = screen.getByRole('heading', { name: 'Input Ontology', level: 4 }).closest('section')!
  expect(within(ontology).getByText('match')).toBeInTheDocument()
  expect(within(ontology).getByText('Matched categories: required_001')).toBeInTheDocument()
  expect(screen.getByText(/Completed classifier judgments are saved/)).toBeInTheDocument()
})

it('keeps unattempted dimensions pending after a partial item is stopped', () => {
  const run = buildDemoItemAnalysisRun('sample')
  run.status = 'cancelled'
  run.items = [{ ...run.items[0], status: 'partial', labels: {
    input_ontology: run.items[0].labels!.input_ontology,
  } }]
  render(<Results run={run} page={1} setPage={vi.fn()} onDownload={vi.fn()} downloading={null} pageLoading={false} />)
  expect(screen.getByText('Partly classified')).toBeInTheDocument()
  expect(screen.getAllByText('Pending')).toHaveLength(3)
  expect(screen.queryByText('Needs retry')).not.toBeInTheDocument()
})

it('distinguishes selected items from the dataset and counts saved and missing dimensions after a partial pilot', () => {
  const run = buildDemoItemAnalysisRun('pilot')
  run.status = 'cancelled'
  run.complete = 1
  run.errors = 1
  run.summary!.experiment = { classifier_count: 4, selected_items: 2, completed_item_classifier_judgments: 5, expected_item_classifier_judgments: 8 }
  render(<Results run={run} page={1} setPage={vi.fn()} onDownload={vi.fn()} downloading={null} pageLoading={false} />)
  expect(screen.getByText('Selected items').parentElement).toHaveTextContent(`2Selected itemsof ${run.total} in the snapshot`)
  expect(screen.getByText('Saved classifier judgments').parentElement).toHaveTextContent('5Saved classifier judgmentsof 8 expected')
  expect(screen.getByText('Missing classifier judgments').parentElement).toHaveTextContent('3Missing classifier judgments')
  expect(screen.getByText('Items fully classified').parentElement).toHaveTextContent('1 item needing retry')
  expect(screen.getByText('Pilot results')).toBeInTheDocument()
})

it('keeps full long item text behind an accessible disclosure while preserving its judgments', async () => {
  const run = buildDemoItemAnalysisRun('sample')
  run.items = [{ ...run.items[0], content: 'Long source passage. '.repeat(60) }]
  const user = userEvent.setup()
  render(<Results run={run} page={1} setPage={vi.fn()} onDownload={vi.fn()} downloading={null} pageLoading={false} />)
  const item = document.querySelector('details.ia-item') as HTMLDetailsElement
  await user.click(item.querySelector('summary')!)
  const full = screen.getByText('Read full item text').closest('details')!
  expect(full.open).toBe(false)
  await user.click(screen.getByText('Read full item text'))
  expect(full.open).toBe(true)
  expect(full.querySelector('p')?.textContent).toBe(run.items[0].content)
  expect(screen.getByRole('heading', { name: 'Input Ontology', level: 4 })).toBeVisible()
})

it('presents registered sources as individually expandable readable fields', async () => {
  const spec = { ...DEMO_ITEM_ANALYSIS_SPEC, source_registry: { 'source-a': { source_title: 'Deployment requirements', requirements: ['Use English', 'Offer hints'] } } }
  const user = userEvent.setup()
  render(<Criteria spec={spec} />)
  await user.click(screen.getByText('Criteria context and preparation notes'))
  await user.click(screen.getByText('Registered source contents'))
  const source = screen.getByText('source-a').closest('details')!
  expect(source.open).toBe(false)
  await user.click(screen.getByText('source-a'))
  expect(screen.getByText('Deployment requirements')).toBeVisible()
  expect(screen.getByText('Offer hints')).toBeVisible()
  expect(source.querySelector('pre')).toBeNull()
})
