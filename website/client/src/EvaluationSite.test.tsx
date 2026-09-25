import { afterEach, describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { EvaluationSite } from './EvaluationSite'

vi.mock('./App', () => ({ App: () => <div>Existing Benchmark Caliper flow</div> }))
vi.mock('./itemReview/ItemReview', () => ({ ItemReview: () => <div>Item review flow</div> }))

afterEach(() => window.history.replaceState(null, '', '/'))

describe('Evaluation routes', () => {
  it('offers both workflows at the starting page', () => {
    window.history.replaceState(null, '', '/')
    render(<EvaluationSite />)
    expect(screen.getByRole('link', { name: /evaluate a benchmark/i })).toHaveAttribute('href', '/caliper')
    expect(screen.getByRole('link', { name: /find relevant tests/i })).toHaveAttribute('href', '/items')
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
})
