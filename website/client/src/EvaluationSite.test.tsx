import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { EvaluationSite } from './EvaluationSite'

vi.mock('./App', () => ({ App: () => <div>Existing Benchmark Caliper flow</div> }))
vi.mock('./itemReview/ItemReview', () => ({ ItemReview: () => <div>Item review flow</div> }))
vi.mock('./itemAnalysis/ItemAnalysis', () => ({ ItemAnalysis: () => <div>Item analysis flow</div> }))

afterEach(() => {
  window.history.replaceState(null, '', '/')
  vi.unstubAllEnvs()
})

describe('Evaluation routes', () => {
  it('offers all three workflows at the starting page', () => {
    window.history.replaceState(null, '', '/')
    render(<EvaluationSite />)
    expect(screen.getByRole('link', { name: /analyze a benchmark/i })).toHaveAttribute('href', '/caliper')
    expect(screen.getByRole('link', { name: /assess evaluation items/i })).toHaveAttribute('href', '/items')
    expect(screen.getByRole('link', { name: /explore item analysis/i })).toHaveAttribute('href', '/item-analysis')
  })

  it.each(['/caliper', '/run/12345678-abcd-1234-abcd-123456789abc'])('preserves the existing workflow at %s', path => {
    window.history.replaceState(null, '', path)
    render(<EvaluationSite />)
    expect(screen.getByText('Existing Benchmark Caliper flow')).toBeInTheDocument()
  })

  it('routes item review separately', () => {
    window.history.replaceState(null, '', '/items')
    render(<EvaluationSite />)
    expect(screen.getByText('Item review flow')).toBeInTheDocument()
  })

  it.each(['/item-analysis', '/item-analysis/'])('routes the item analysis demo at %s', path => {
    window.history.replaceState(null, '', path)
    render(<EvaluationSite />)
    expect(screen.getByText('Item analysis flow')).toBeInTheDocument()
  })

  it('routes item analysis under the production base path', async () => {
    vi.stubEnv('BASE_URL', '/benchmark-caliper/')
    vi.resetModules()
    const { EvaluationSite: PrefixedEvaluationSite } = await import('./EvaluationSite')
    window.history.replaceState(null, '', '/benchmark-caliper/item-analysis')
    render(<PrefixedEvaluationSite />)
    expect(screen.getByText('Item analysis flow')).toBeInTheDocument()
  })
})
