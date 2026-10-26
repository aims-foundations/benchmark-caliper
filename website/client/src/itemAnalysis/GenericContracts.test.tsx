import { expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
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
  expect(screen.getByRole('button', { name: /Human review CSV/ })).toBeDisabled()
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
