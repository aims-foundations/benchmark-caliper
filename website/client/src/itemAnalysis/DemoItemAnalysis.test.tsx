import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DemoItemAnalysis } from './DemoItemAnalysis'
import { buildDemoExport } from './demoExports'
import { DEMO_ITEM_STORAGE_KEY } from '../demo/session'
import { buildSixScoreDemoRun } from '../demo/sixScoreItemFixture'
import { DEMO_ITEM_ANALYSIS_PROVENANCE } from '../demo/itemAnalysisFixture'
import { DEMO_SCORING } from '../demo/fixture'

beforeEach(() => { sessionStorage.clear(); localStorage.clear(); vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('The demo must stay local.'))) })
afterEach(() => { vi.restoreAllMocks(); vi.unstubAllGlobals() })

it('uses three stages and allows all items directly without a review gate or paid calls', async () => {
  const user = userEvent.setup()
  const onStatusChange = vi.fn()
  render(<DemoItemAnalysis onStatusChange={onStatusChange} />)
  expect(within(screen.getByRole('navigation', { name: 'Item analysis steps' })).getAllByRole('link')).toHaveLength(3)
  expect(onStatusChange).toHaveBeenLastCalledWith('pending')
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark and prepare context' }))
  expect(onStatusChange).toHaveBeenLastCalledWith('in_progress')
  await user.click(screen.getByRole('button', { name: 'Show all 10 items' }))
  expect(onStatusChange).toHaveBeenLastCalledWith('complete')
  expect(screen.getAllByRole('button', { name: /Input Ontology: 4/ })).toHaveLength(10)
  expect(screen.getAllByRole('button', { name: /Output Content: Unknown/ })).toHaveLength(10)
  expect(screen.queryByRole('checkbox')).not.toBeInTheDocument()
  expect(screen.queryByLabelText(/API key/)).not.toBeInTheDocument()
  await user.click(screen.getAllByRole('button', { name: /Output Content: Unknown/ })[0])
  const detail = screen.getByRole('region', { name: 'Selected score details' })
  expect(within(detail).getByRole('heading', { name: 'Missing information' })).toBeVisible()
  expect(detail).toHaveTextContent('Target-teacher judgments')
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it('supports an optional pilot, restores it, and does not disturb live access', async () => {
  const liveKey = 'item_analysis_run_v1:gallery:real'
  sessionStorage.setItem(liveKey, 'private-access')
  const first = render(<DemoItemAnalysis />)
  const user = userEvent.setup()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark and prepare context' }))
  await user.click(screen.getByRole('button', { name: 'Show first 4 items' }))
  expect(screen.getAllByRole('button', { name: /Input Ontology: 4/ })).toHaveLength(4)
  expect(screen.getAllByRole('button', { name: /Input Ontology: Pending/ })).toHaveLength(6)
  first.unmount()
  render(<DemoItemAnalysis />)
  expect(screen.getByRole('button', { name: 'Show remaining examples' })).toBeEnabled()
  await user.click(screen.getByRole('button', { name: 'Show remaining examples' }))
  expect(screen.getAllByRole('button', { name: /Input Ontology: 4/ })).toHaveLength(10)
  await user.click(screen.getByRole('button', { name: 'Restart item demo' }))
  expect(screen.getByRole('button', { name: 'Confirm benchmark and prepare context' })).toBeEnabled()
  expect(sessionStorage.getItem(liveKey)).toBe('private-access')
  expect(localStorage.length).toBe(0)
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it.each(['bad json', '{"version":99,"stage":"complete"}', '{"version":1,"stage":"pilot"}'])('starts fresh for invalid or old demo state: %s', value => {
  sessionStorage.setItem(DEMO_ITEM_STORAGE_KEY, value)
  render(<DemoItemAnalysis />)
  expect(screen.getByRole('button', { name: 'Confirm benchmark and prepare context' })).toBeEnabled()
})

it('exports six assessments and blind worksheets with provenance while preserving original benchmark scores', () => {
  const run = buildSixScoreDemoRun('sample')
  expect(run.summary?.original_assessment).toEqual(DEMO_SCORING.dimensions)
  expect(run.spec?.source_registry).not.toHaveProperty('scoring.json#/dimensions/input_ontology')
  for (const artifact of ['spec', 'items', 'summary', 'report', 'review'] as const) {
    const result = buildDemoExport(artifact, run)
    expect(result.content).toContain(DEMO_ITEM_ANALYSIS_PROVENANCE.revision)
    expect(result.content).toMatch(/authored/i)
  }
  const csv = buildDemoExport('items', run).content
  expect(csv).toContain('authored_example_scores')
  expect(csv).toContain('information_gaps')
  const review = buildDemoExport('review', run).content
  expect(review.split('\r\n')[0]).toContain('human_score')
  expect(review).not.toContain('Illustrative judgment:')
  const dangerous = '<img src=x onerror=alert(1)>'
  const html = buildDemoExport('report', { ...run, items: [{ ...run.items[0], content: dangerous }] }).content
  expect(html).not.toContain(dangerous)
  expect(html).toContain('&lt;img')
  expect(html).toContain('Missing information')
  expect(html).toContain('Input Form')
})
