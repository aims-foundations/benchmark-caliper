import { expect, it, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { buildDemoItemAnalysisRun, DEMO_ITEM_ANALYSIS_SPEC } from '../demo/itemAnalysisFixture'
import { ContextValidation } from './ContextValidation'
import { PreparedContext } from './PreparedContext'

it('separates deployment-specific context from the fixed classifier rules', () => {
  render(<PreparedContext spec={DEMO_ITEM_ANALYSIS_SPEC} />)
  const requirements = screen.getByRole('region', { name: 'Prepared deployment requirements' })
  expect(requirements.querySelectorAll('.ia-context-statements > li')).toHaveLength(2)
  expect(requirements.querySelector('.ia-context-statements > li > p')?.textContent).toBe(DEMO_ITEM_ANALYSIS_SPEC.deployment_description)
  expect(screen.getByRole('heading', { name: 'Required input categories' })).toBeInTheDocument()
  expect(screen.getByText('partial inventory')).toBeInTheDocument()
  expect(screen.getByText(/A partial or unknown inventory does not make an unmatched item out of scope/)).toBeInTheDocument()
  const dimensions = screen.getByRole('region', { name: 'Dimension-specific context' })
  for (const name of ['Input Ontology', 'Input Content', 'Output Ontology', 'Output Content']) {
    expect(within(dimensions).getByText(name)).toBeVisible()
  }
  expect(screen.queryByText(DEMO_ITEM_ANALYSIS_SPEC.classifiers[0].decision_rules![0])).not.toBeInTheDocument()
  const gaps = screen.getByRole('region', { name: 'Prepared evidence gaps' })
  expect(within(gaps).getByText('No independent target-teacher item judgments or complete scoring and annotation documentation are bundled.')).toBeVisible()
})

it('keeps source and category identifiers collapsed while offering readable source contents', async () => {
  const user = userEvent.setup()
  const spec = structuredClone(DEMO_ITEM_ANALYSIS_SPEC)
  spec.source_registry!['elicitation_summary.md'] = { title: 'Math tutoring requirements', task: 'Offer hints before a solution.' }
  render(<PreparedContext spec={spec} direct />)
  const categories = screen.getByRole('region', { name: 'Required input categories' })
  const category = within(categories).getByText('Curriculum-agnostic mathematical errors').closest('details')!
  expect(category.open).toBe(false)
  await user.click(within(categories).getByText('Curriculum-agnostic mathematical errors'))
  expect(within(category).getByText(spec.input_category_inventory!.categories[0].definition)).toBeVisible()
  expect(within(category).getByText('required_001')).not.toBeVisible()
  await user.click(within(category).getByText('Supporting source'))
  await user.click(within(category).getByRole('button', { name: 'Math tutoring requirements' }))
  const source = screen.getByText('Math tutoring requirements', { selector: 'summary' })
  expect(within(source.closest('details')!).getByText('Offer hints before a solution.')).toBeVisible()
  expect(screen.getByText(/Input Form and Output Form are not assessed in this path/)).toBeInTheDocument()
})

it('distinguishes structural checks from scientific and human review, with fixed rules separate', async () => {
  const user = userEvent.setup()
  const run = buildDemoItemAnalysisRun('sample')
  run.summary!.specification = { adjustments: [{ field: 'evidence_gaps', reason: 'Preserve deterministic source availability gap' }] }
  render(<ContextValidation run={run} />)
  expect(screen.getByRole('heading', { name: 'Python checks passed for the saved specification' })).toBeInTheDocument()
  expect(screen.getByText(/Passing these checks does not establish scientific correctness/)).toBeInTheDocument()
  expect(screen.getByText(/External human review in step 6 is a separate activity/)).toBeInTheDocument()
  expect(screen.getByText('Preserve deterministic source availability gap')).toBeInTheDocument()
  expect(screen.queryByText(DEMO_ITEM_ANALYSIS_SPEC.deployment_description!)).not.toBeInTheDocument()
  const specification = screen.getByRole('region', { name: 'Resulting classifier specification' })
  const classifier = within(specification).getByText('Input Ontology').closest('details')!
  expect(classifier.open).toBe(false)
  await user.click(within(specification).getByText('Input Ontology'))
  expect(within(classifier).getByText(DEMO_ITEM_ANALYSIS_SPEC.classifiers[0].decision_rules![0])).toBeVisible()
  expect(within(classifier).getByText('match')).toBeVisible()
  expect(within(classifier).getByText('no match')).toBeVisible()
  expect(screen.queryByRole('button')).not.toBeInTheDocument()
})

it.each(['invalid_json', 'schema', 'evidence', 'deployment', 'task_grounding'])('shows a reported %s validation failure without an accepted specification', code => {
  const run = buildDemoItemAnalysisRun('sample')
  run.status = 'failed'
  run.spec = null
  run.failure = { stage: 'specification', code, message: 'The generated context failed its required checks after one repair.' }
  render(<ContextValidation run={run} />)
  expect(screen.getByRole('alert')).toHaveTextContent('Python checks did not pass')
  expect(screen.getByText(run.failure.message)).toBeInTheDocument()
  expect(screen.queryByRole('region', { name: 'Resulting classifier specification' })).not.toBeInTheDocument()
})

it('does not present provider failure during preparation as a failed Python check', () => {
  const run = buildDemoItemAnalysisRun('sample')
  run.status = 'failed'
  run.spec = null
  run.failure = { stage: 'specification', code: 'provider_authentication', message: 'The provider rejected this key.' }
  render(<ContextValidation run={run} />)
  expect(screen.getByRole('heading', { name: 'Validation outcome not yet available' })).toBeInTheDocument()
  expect(screen.getByText(/No failed Python check is reported here/)).toBeInTheDocument()
  expect(screen.queryByText('Python checks did not pass')).not.toBeInTheDocument()
})

it('preserves accepted context validation when a later item classification fails', () => {
  const run = buildDemoItemAnalysisRun('sample')
  run.status = 'failed'
  run.failure = { stage: 'classification', code: 'provider_unavailable', message: 'Retry classification later.' }
  render(<ContextValidation run={run} />)
  expect(screen.getByRole('heading', { name: 'Python checks passed for the saved specification' })).toBeInTheDocument()
  expect(screen.queryByText('Retry classification later.')).not.toBeInTheDocument()
})

it('can expose an explicit specification download when embedded outside the numbered page', async () => {
  const onDownload = vi.fn()
  const user = userEvent.setup()
  render(<ContextValidation run={buildDemoItemAnalysisRun('sample')} onDownload={onDownload} />)
  await user.click(screen.getByRole('button', { name: 'Download classifier specification JSON' }))
  expect(onDownload).toHaveBeenCalledOnce()
})
