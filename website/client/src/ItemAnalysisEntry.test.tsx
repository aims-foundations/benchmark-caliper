import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemAnalysisEntry, savedReportPath } from './ItemAnalysisEntry'

vi.mock('./itemAnalysis/DirectItemStart', () => ({ DirectItemStart: () => <div>Direct deployment form</div> }))

beforeEach(() => {
  window.history.replaceState(null, '', '/caliper?start=items')
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ benchmarks: [
    { id: 'expert__mmlu', benchmark_name: 'MMLU', slug: 'hindi_exam_preparation', deployment_description: 'Hindi-medium exam preparation in India.' },
  ] }), { status: 200 })))
})
afterEach(() => { vi.unstubAllGlobals(); window.history.replaceState(null, '', '/') })

it('requires selecting an existing context and links directly to its item stage without model requests', async () => {
  const user = userEvent.setup()
  render(<ItemAnalysisEntry />)
  expect(screen.queryByRole('link', { name: /continue to item analysis/i })).not.toBeInTheDocument()
  await user.selectOptions(await screen.findByLabelText('Benchmark and deployment'), 'expert__mmlu')
  expect(screen.getByText('Hindi-medium exam preparation in India.')).toBeVisible()
  expect(screen.getByRole('link', { name: /continue to item analysis/i })).toHaveAttribute('href', '/caliper?assessment=expert__mmlu#item-analysis-stage')
  expect(screen.queryByLabelText(/api key/i)).not.toBeInTheDocument()
  expect(vi.mocked(fetch).mock.calls.map(([url]) => url)).toEqual(['/api/gallery'])
})

it('switches starting points within the same workflow and restores the new-context route', async () => {
  const user = userEvent.setup()
  const first = render(<ItemAnalysisEntry />)
  await user.click(screen.getByRole('button', { name: /New deployment context/ }))
  expect(screen.getByText('Direct deployment form')).toBeVisible()
  expect(new URLSearchParams(location.search).get('mode')).toBe('new')
  first.unmount()
  render(<ItemAnalysisEntry />)
  expect(screen.getByText('Direct deployment form')).toBeVisible()
  expect(screen.getByRole('button', { name: /New deployment context/ })).toHaveAttribute('aria-pressed', 'true')
})

it('opens a saved report on the local site and does not navigate to an arbitrary pasted URL', async () => {
  const user = userEvent.setup()
  render(<ItemAnalysisEntry />)
  const field = screen.getByLabelText('Saved report link or run ID')
  await user.type(field, 'https://example.com/run/12345678-abcd')
  expect(screen.getByText(/enter a valid benchmark caliper report/i)).toBeVisible()
  expect(screen.queryByRole('link', { name: /continue from saved report/i })).not.toBeInTheDocument()
  await user.clear(field)
  await user.type(field, 'https://aims.stanford.edu/benchmark-caliper/run/12345678-abcd')
  expect(screen.getByRole('link', { name: /continue from saved report/i })).toHaveAttribute('href', '/run/12345678-abcd#item-analysis-stage')
  expect(savedReportPath('12345678-abcd')).toBe('/run/12345678-abcd#item-analysis-stage')
  expect(vi.mocked(fetch).mock.calls.map(([url]) => url)).toEqual(['/api/gallery'])
})

it('keeps saved-report entry available when the gallery cannot load', async () => {
  vi.mocked(fetch).mockRejectedValue(new Error('offline'))
  render(<ItemAnalysisEntry />)
  expect(await screen.findByRole('alert')).toHaveTextContent('Could not load existing assessments')
  expect(screen.getByLabelText('Saved report link or run ID')).toBeEnabled()
  expect(screen.getByRole('button', { name: 'Retry loading assessments' })).toBeEnabled()
})
