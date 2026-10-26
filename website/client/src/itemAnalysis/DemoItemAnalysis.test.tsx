import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DemoItemAnalysis } from './DemoItemAnalysis'
import { buildDemoExport } from './demoExports'
import { DEMO_ITEM_STORAGE_KEY } from '../demo/session'
import {
  buildDemoItemAnalysisRun,
  DEMO_ITEM_ANALYSIS_ITEMS,
  DEMO_ITEM_ANALYSIS_PILOT_SIZE,
  DEMO_ITEM_ANALYSIS_PROVENANCE,
} from '../demo/itemAnalysisFixture'

const liveStorageKey = 'item_analysis_run_v1:gallery:expert_1a429e941728__mathdial'
const liveAccess = JSON.stringify({ run_id: 'real-paid-run', run_secret: 'private-live-token' })
const sampleCount = DEMO_ITEM_ANALYSIS_ITEMS.length

beforeEach(() => {
  sessionStorage.clear()
  localStorage.clear()
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('The bundled demo must not request a server.')))
})

afterEach(() => {
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

async function showPilot(user = userEvent.setup()) {
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.click(screen.getByRole('button', { name: 'Show demo criteria' }))
  await user.click(screen.getByRole('button', { name: 'Show pilot results' }))
  return user
}

async function finishSample(user = userEvent.setup()) {
  await showPilot(user)
  await user.click(screen.getByRole('checkbox', { name: 'I have reviewed the pilot examples and criteria' }))
  await user.click(screen.getByRole('button', { name: 'Continue demo through remaining items' }))
  return user
}

it('requires benchmark confirmation and a human pilot checkpoint before completing the free sample', async () => {
  const onStatusChange = vi.fn()
  render(<DemoItemAnalysis onStatusChange={onStatusChange} />)
  expect(onStatusChange).toHaveBeenLastCalledWith('pending')
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeEnabled()
  expect(screen.queryByRole('button', { name: 'Show pilot results' })).not.toBeInTheDocument()
  expect(screen.queryByLabelText(/API key/i)).not.toBeInTheDocument()
  const user = userEvent.setup()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  expect(onStatusChange).toHaveBeenLastCalledWith('in_progress')
  await user.click(screen.getByRole('button', { name: 'Show demo criteria' }))
  expect(screen.getByRole('heading', { name: 'Review the criteria' })).toBeVisible()
  expect(screen.queryByRole('button', { name: 'Continue demo through remaining items' })).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Show pilot results' }))

  const results = screen.getByRole('region', { name: 'Analysis results' })
  expect(within(results).getAllByText('Example judgment shown')).toHaveLength(DEMO_ITEM_ANALYSIS_PILOT_SIZE)
  expect(within(results).getAllByText('Pending')).toHaveLength(sampleCount - DEMO_ITEM_ANALYSIS_PILOT_SIZE)
  expect(screen.getByText('Demo items complete').parentElement).toHaveTextContent(String(DEMO_ITEM_ANALYSIS_PILOT_SIZE))
  expect(screen.getByText('Selected items').parentElement).toHaveTextContent(String(sampleCount))
  expect(onStatusChange).toHaveBeenLastCalledWith('in_progress')
  expect(screen.getByRole('button', { name: 'Continue demo through remaining items' })).toBeDisabled()
  await user.click(screen.getByRole('checkbox', { name: 'I have reviewed the pilot examples and criteria' }))
  await user.click(screen.getByRole('button', { name: 'Continue demo through remaining items' }))

  expect(onStatusChange).toHaveBeenLastCalledWith('complete')
  expect(within(results).getAllByText('Example judgment shown')).toHaveLength(sampleCount)
  expect(within(results).queryByText('Pending')).not.toBeInTheDocument()
  expect(screen.getByText('Full demo sample')).toBeVisible()
  expect(screen.getByText('Demo items complete').parentElement).toHaveTextContent(String(sampleCount))
  expect(screen.queryByText('Full snapshot')).not.toBeInTheDocument()
  expect(screen.queryByText(/Percentages describe model judgments/)).not.toBeInTheDocument()
  expect(screen.getAllByText(/authored/i).length).toBeGreaterThan(0)
  expect(screen.queryByLabelText(/API key/i)).not.toBeInTheDocument()
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it('shows a real pinned source while identifying the judgments and sample as illustrative', async () => {
  render(<DemoItemAnalysis />)
  const sourceLinks = screen.getAllByRole('link').filter(link => link.getAttribute('href') === DEMO_ITEM_ANALYSIS_PROVENANCE.source_url)
  expect(sourceLinks.length).toBeGreaterThan(0)
  expect(screen.getAllByText(/authored/i).length).toBeGreaterThan(0)
  expect(screen.getAllByText(/sample/i).length).toBeGreaterThan(0)
  await finishSample()
  expect(screen.getAllByText(/not representative|not.*full MathDial|only.*(?:bundled|demo).*sample|(?:bundled|demo).*sample only/i).length).toBeGreaterThan(0)
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it('restores the demo checkpoint without reading or overwriting live item-run access', async () => {
  sessionStorage.setItem(liveStorageKey, liveAccess)
  const first = render(<DemoItemAnalysis />)
  await showPilot()
  expect(JSON.parse(sessionStorage.getItem(DEMO_ITEM_STORAGE_KEY)!)).toMatchObject({ version: 1, stage: 'pilot' })
  first.unmount()
  const onStatusChange = vi.fn()
  render(<DemoItemAnalysis onStatusChange={onStatusChange} />)
  expect(screen.getByRole('button', { name: 'Continue demo through remaining items' })).toBeDisabled()
  expect(screen.getByRole('checkbox', { name: 'I have reviewed the pilot examples and criteria' })).not.toBeChecked()
  expect(onStatusChange).toHaveBeenLastCalledWith('in_progress')
  expect(sessionStorage.getItem(liveStorageKey)).toBe(liveAccess)
  expect(localStorage.length).toBe(0)
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it('restores completion and resets only the free walkthrough', async () => {
  sessionStorage.setItem(liveStorageKey, liveAccess)
  const first = render(<DemoItemAnalysis />)
  await finishSample()
  first.unmount()
  const onStatusChange = vi.fn()
  render(<DemoItemAnalysis onStatusChange={onStatusChange} />)
  expect(onStatusChange).toHaveBeenLastCalledWith('complete')
  expect(screen.getByText('Full demo sample')).toBeVisible()
  const user = userEvent.setup()
  await user.click(screen.getByRole('button', { name: 'Restart item demo' }))
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeEnabled()
  expect(screen.queryByText('Full demo sample')).not.toBeInTheDocument()
  expect(onStatusChange).toHaveBeenLastCalledWith('pending')
  expect(sessionStorage.getItem(liveStorageKey)).toBe(liveAccess)
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it.each(['bad json', '{"version":99,"stage":"complete"}', '{"version":1,"stage":"unknown"}'])('starts with confirmation when saved demo state is invalid: %s', value => {
  sessionStorage.setItem(DEMO_ITEM_STORAGE_KEY, value)
  const onStatusChange = vi.fn()
  render(<DemoItemAnalysis onStatusChange={onStatusChange} />)
  expect(screen.getByRole('button', { name: 'Confirm benchmark' })).toBeEnabled()
  expect(onStatusChange).toHaveBeenLastCalledWith('pending')
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it('downloads demo artifacts locally with distinct filenames and sample provenance', async () => {
  const blobs: Blob[] = []
  const filenames: string[] = []
  vi.spyOn(URL, 'createObjectURL').mockImplementation(blob => { blobs.push(blob as Blob); return 'blob:demo-download' })
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function (this: HTMLAnchorElement) { filenames.push(this.download) })
  render(<DemoItemAnalysis />)
  const user = await finishSample()
  await user.click(screen.getByRole('button', { name: /Download.*criteria/i }))
  await user.click(screen.getByText('Individual files'))
  for (const name of ['Item labels CSV', 'Summary JSON', 'HTML report', 'Human review CSV']) {
    await user.click(screen.getByRole('button', { name: new RegExp(name) }))
  }
  expect(filenames).toEqual(['mathdial-demo-classifier_spec.json', 'mathdial-demo-items.csv', 'mathdial-demo-summary.json', 'mathdial-demo-report.html', 'mathdial-demo-review.csv'])
  expect(blobs).toHaveLength(5)
  for (const blob of blobs) {
    const content = await blob.text()
    expect(content).toContain(DEMO_ITEM_ANALYSIS_PROVENANCE.revision)
    expect(content).toMatch(/authored/i)
    expect(content).toMatch(/sample/i)
  }
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it('exports criteria before the pilot without claiming that any example judgments have been shown', async () => {
  let savedBlob: Blob | undefined
  vi.spyOn(URL, 'createObjectURL').mockImplementation(blob => { savedBlob = blob as Blob; return 'blob:demo-criteria' })
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
  render(<DemoItemAnalysis />)
  const user = userEvent.setup()
  await user.click(screen.getByRole('button', { name: 'Confirm benchmark' }))
  await user.click(screen.getByRole('button', { name: 'Show demo criteria' }))
  await user.click(screen.getByRole('button', { name: /Download.*criteria/i }))
  const artifact = JSON.parse(await savedBlob!.text())
  expect(artifact.demo).toMatchObject({ scope: 'criteria', shown_items: 0, sample_items: sampleCount, completed_demo_sample: false, model_calls: 0 })
  expect(artifact.specification.classifiers.length).toBeGreaterThan(0)
  expect(screen.queryByRole('region', { name: 'Analysis results' })).not.toBeInTheDocument()
  expect(globalThis.fetch).not.toHaveBeenCalled()
})

it('exports pilot versus complete-sample counts without claiming full MathDial coverage', () => {
  for (const phase of ['pilot', 'sample'] as const) {
    const run = buildDemoItemAnalysisRun(phase)
    const summary = JSON.parse(buildDemoExport('summary', run).content)
    const completed = phase === 'pilot' ? DEMO_ITEM_ANALYSIS_PILOT_SIZE : sampleCount
    expect(summary.total_items).toBe(sampleCount)
    expect(summary.completed_items).toBe(completed)
    expect(summary.pending_items).toBe(sampleCount - completed)
    expect(summary.demo).toMatchObject({ shown_items: completed, sample_items: sampleCount, completed_demo_sample: phase === 'sample' })
    expect(summary.demo.scope).toBe(phase)
    expect(summary.demo.dataset_scope).toMatch(/demo sample only/i)
  }
})

it('keeps the independent review worksheet free of supplied labels and escapes HTML items', () => {
  const run = buildDemoItemAnalysisRun('sample')
  const csv = buildDemoExport('review', run).content
  const header = csv.split(/\r?\n/, 1)[0]
  expect(header).toContain('human_label')
  expect(header).toContain('human_justification')
  expect(header).not.toMatch(/model_label|authored_label|prediction/)
  expect(header).toContain('human_matched_category_ids')
  expect(header).toContain('human_evidence')
  const dangerousContent = '<img src=x onerror=alert(1)>'
  const html = buildDemoExport('report', { ...run, items: [{ ...run.items[0], content: dangerousContent }] }).content
  expect(html).not.toContain(dangerousContent)
  expect(html).toContain('&lt;img')
})
