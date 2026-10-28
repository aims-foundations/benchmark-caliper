import { expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import { buildSixScoreDemoRun } from '../demo/sixScoreItemFixture'
import { buildDemoItemAnalysisRun } from '../demo/itemAnalysisFixture'
import { DimensionAverages, ItemJudgments } from './Results'
import { buildDemoExport } from './demoExports'
import type { AnalysisRun } from './types'

function mixedRun(): AnalysisRun {
  const run = buildSixScoreDemoRun('sample')
  const dimension = run.summary!.classifiers[0]
  Object.assign(dimension, { counts: { '1': 1, '2': 0, '3': 0, '4': 0, '5': 2 }, known: 3, unknown: 2, errors: 1, pending: 4, mean_score: 11 / 3 })
  run.summary!.completed_items = 5
  run.summary!.complete_snapshot = false
  run.summary!.experiment!.selected_completed_items = 5
  run.summary!.original_assessment = { input_ontology: { score: 2 }, input_content: { score: null } }
  return run
}

function averageRow(name: string) {
  const table = screen.getByRole('table', { name: 'Dimension averages and benchmark scores' })
  return within(within(table).getByRole('rowheader', { name }).closest('tr')!)
}

it('shows six arithmetic means alongside benchmark scores with numeric denominators and selection scope', () => {
  render(<DimensionAverages run={mixedRun()} />)
  expect(screen.getByRole('heading', { name: 'Average item scores' })).toBeVisible()
  expect(screen.getByText(/5 of 10 selected items evaluated, from 10 items/)).toBeVisible()
  expect(screen.getByText('Partial results')).toBeVisible()
  expect(screen.getAllByRole('rowheader')).toHaveLength(6)
  const input = averageRow('Input Ontology')
  expect(input.getByText('3.67 / 5')).toBeVisible()
  expect(input.getByText('3 numeric')).toBeVisible()
  expect(input.getByText('2 Unknown')).toBeVisible()
  expect(input.getByText('2 / 5')).toBeVisible()
  expect(screen.getByText(/Unknown, failed, and pending items are excluded/)).toBeVisible()
})

it('computes older summary means from numeric counts while keeping all-Unknown dimensions unscored', () => {
  const run = mixedRun()
  delete run.summary!.classifiers[0].mean_score
  delete run.summary!.dimensions
  render(<DimensionAverages run={run} />)
  expect(averageRow('Input Ontology').getByText('3.67 / 5')).toBeVisible()
  const content = averageRow('Input Content')
  expect(content.getByText('No numeric scores')).toBeVisible()
  expect(content.getByText('0 numeric')).toBeVisible()
  expect(content.getByText('10 Unknown')).toBeVisible()
  expect(content.getAllByText('Unknown')).toHaveLength(2)
  expect(averageRow('Input Form').getByText('Not available')).toBeVisible()
})

it('labels a direct-context benchmark as Not run even if stale benchmark values are present', () => {
  const run = mixedRun()
  run.assessment = { kind: 'direct', id: 'direct', benchmark: 'Example', deployment: 'Deployment' }
  render(<DimensionAverages run={run} />)
  expect(screen.getAllByText('Not run')).toHaveLength(6)
  expect(averageRow('Input Ontology').queryByText('2 / 5')).not.toBeInTheDocument()
})

it('keeps run-wide means unchanged when a page or filter shows a different subset of items', () => {
  const run = mixedRun()
  run.pagination = { ...run.pagination, page: 1, total_pages: 2 }
  run.items = [run.items[0]]
  const { rerender } = render(<><DimensionAverages run={run} /><ItemJudgments run={run} page={1} setPage={vi.fn()} pageLoading={false} /></>)
  expect(averageRow('Input Ontology').getByText('3.67 / 5')).toBeVisible()
  const lowItem = { ...run.items[0], item_id: 'low-item', dimensions: { input_ontology: { score: 1, justification: 'A mismatch.', evidence: [], information_gaps: [] } } }
  rerender(<><DimensionAverages run={{ ...run, items: [lowItem] }} /><ItemJudgments run={{ ...run, items: [lowItem] }} page={1} setPage={vi.fn()} pageLoading={false} filter={{ kind: 'flagged' }} filteredItems={[lowItem]} /></>)
  expect(screen.getByRole('button', { name: 'low-item · Input Ontology: 1' })).toBeVisible()
  expect(averageRow('Input Ontology').getByText('3.67 / 5')).toBeVisible()
  expect(averageRow('Input Ontology').getByText('3 numeric')).toBeVisible()
  rerender(<><DimensionAverages run={{ ...run, items: [] }} /><ItemJudgments run={{ ...run, items: [] }} page={2} setPage={vi.fn()} pageLoading={false} /></>)
  expect(screen.getByText('Page 2 of 2')).toBeVisible()
  expect(averageRow('Input Ontology').getByText('3.67 / 5')).toBeVisible()
})

it('describes a selected batch and keeps categorical historical reports unchanged', () => {
  const { rerender } = render(<DimensionAverages run={buildSixScoreDemoRun('pilot')} />)
  expect(screen.getByText('Selected items')).toBeVisible()
  expect(screen.getByText(/4 of 4 selected items evaluated, from 10 items/)).toBeVisible()
  expect(averageRow('Input Ontology').getByText('4 numeric')).toBeVisible()
  rerender(<DimensionAverages run={buildDemoItemAnalysisRun('sample')} />)
  expect(screen.queryByRole('table')).not.toBeInTheDocument()
})

it('exports unrounded means in demo JSON and a readable comparison in HTML without changing original scores', () => {
  const run = mixedRun()
  delete run.summary!.classifiers[0].mean_score
  const summary = JSON.parse(buildDemoExport('summary', run).content)
  expect(summary.dimensions[0].mean_score).toBe(11 / 3)
  expect(summary.classifiers[0].mean_score).toBe(11 / 3)
  expect(summary.dimensions[1].mean_score).toBeNull()
  expect(summary.original_assessment.input_ontology.score).toBe(2)
  const report = buildDemoExport('report', run).content
  expect(report).toContain('<h2>Average item scores</h2>')
  expect(report).toContain('3.67 / 5')
  expect(report).toContain('3 numeric · 2 Unknown')
  expect(report).toContain('Unknown (no numeric scores)')
  expect(report.indexOf('<h2>Average item scores</h2>')).toBeLessThan(report.indexOf('<h2>Example judgments</h2>'))
  expect(buildSixScoreDemoRun('pilot').summary!.dimensions![0].mean_score).toBe(4)
})
