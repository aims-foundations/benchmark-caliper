import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { EvaluationSite } from './EvaluationSite'

vi.mock('./App', () => ({ App: ({ legacyItemAnalysis }: { legacyItemAnalysis?: boolean }) => <div>Unified Benchmark Caliper flow{legacyItemAnalysis && <p>Item analysis moved into benchmark analysis</p>}</div> }))
vi.mock('./itemReview/ItemReview', () => ({ ItemReview: () => <div>Item review flow</div> }))
vi.mock('./ItemAnalysisEntry', () => ({ ItemAnalysisEntry: () => <div>Choose an item analysis starting point</div> }))

afterEach(() => {
  window.history.replaceState(null, '', '/')
  vi.unstubAllEnvs()
})

describe('Evaluation routes', () => {
  it('offers two tools and includes item analysis in the benchmark workflow', () => {
    window.history.replaceState(null, '', '/')
    render(<EvaluationSite />)
    expect(screen.getByRole('link', { name: /analyze a benchmark/i })).toHaveAttribute('href', '/caliper')
    expect(screen.getByRole('link', { name: /assess evaluation items/i })).toHaveAttribute('href', '/items')
    expect(screen.getByRole('link', { name: /try the free demo/i })).toHaveAttribute('href', '/caliper?demo=mathdial')
    expect(screen.getByRole('link', { name: /start at item analysis/i })).toHaveAttribute('href', '/caliper?start=items')
    expect(screen.getAllByRole('article')).toHaveLength(2)
    expect(screen.queryByRole('link', { name: /explore item analysis/i })).not.toBeInTheDocument()
    expect(screen.getByText(/benchmark paper, deployment context, and matching dataset/i)).toBeInTheDocument()
    expect(screen.getByText(/issue prevalence with inspectable items/i)).toBeInTheDocument()
  })

  it.each(['/caliper', '/run/12345678-abcd-1234-abcd-123456789abc'])('preserves the existing workflow at %s', path => {
    window.history.replaceState(null, '', path)
    render(<EvaluationSite />)
    expect(screen.getByText('Unified Benchmark Caliper flow')).toBeInTheDocument()
  })

  it('routes item review separately', () => {
    window.history.replaceState(null, '', '/items')
    render(<EvaluationSite />)
    expect(screen.getByText('Item review flow')).toBeInTheDocument()
  })

  it('offers direct item entry within the Caliper route', () => {
    window.history.replaceState(null, '', '/caliper?start=items&mode=new')
    render(<EvaluationSite />)
    expect(screen.getByText('Choose an item analysis starting point')).toBeInTheDocument()
  })

  it.each(['/caliper?start=items&assessment=expert__mmlu', '/caliper?start=items&demo=mathdial', '/run/12345678-abcd?start=items'])('preserves report and demo route priority at %s', path => {
    window.history.replaceState(null, '', path)
    render(<EvaluationSite />)
    expect(screen.getByText('Unified Benchmark Caliper flow')).toBeInTheDocument()
  })

  it.each(['/item-analysis', '/item-analysis/'])('routes legacy item-analysis link %s to the unified flow', path => {
    window.history.replaceState(null, '', path)
    render(<EvaluationSite />)
    expect(screen.getByText('Unified Benchmark Caliper flow')).toBeInTheDocument()
    expect(screen.getByText('Item analysis moved into benchmark analysis')).toBeInTheDocument()
  })

  it('routes item analysis under the production base path', async () => {
    vi.stubEnv('BASE_URL', '/benchmark-caliper/')
    vi.resetModules()
    const { EvaluationSite: PrefixedEvaluationSite } = await import('./EvaluationSite')
    window.history.replaceState(null, '', '/benchmark-caliper/item-analysis')
    render(<PrefixedEvaluationSite />)
    expect(screen.getByText('Unified Benchmark Caliper flow')).toBeInTheDocument()
    expect(screen.getByText('Item analysis moved into benchmark analysis')).toBeInTheDocument()
  })
})
