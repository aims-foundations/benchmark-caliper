import { beforeEach, expect, it, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ItemAnalysis } from './ItemAnalysis'
import { ITEM_STEPS } from './PipelineStages'
import { DEMO_ITEM_ANALYSIS_SPEC } from '../demo/itemAnalysisFixture'
import * as api from './api'
import type { AnalysisRun, ClassifierSummary, Item } from './types'

vi.mock('./api', async original => ({ ...await original<typeof import('./api')>(),
  getCatalog: vi.fn(), getRun: vi.fn(), createRun: vi.fn(), classify: vi.fn(), cancelRun: vi.fn(),
  download: vi.fn(), discardRun: vi.fn(), downloadPackage: vi.fn(),
}))

const access = { run_id: 'stage-test-run', run_secret: 'private-stage-test-token' }
const example = { id: 'mmlu', title: 'MMLU tutoring', item_count: 14015, benchmark: 'mmlu',
  deployment: 'Help students practise school-level mathematics.', description: 'A prepared test dataset.',
  source_label: 'Test dataset snapshot', available: true, supplied_spec_available: false }
const spec = { ...DEMO_ITEM_ANALYSIS_SPEC, benchmark: example.benchmark,
  deployment: example.deployment, deployment_description: example.deployment }

function distributions(count: number): ClassifierSummary[] {
  return spec.classifiers.map((classifier): ClassifierSummary => ({ ...classifier,
    counts: classifier.id === 'input_ontology' ? { match: count, no_match: 0, insufficient_evidence: 0 }
      : { no_issue_identified: count, issue_identified: 0, insufficient_evidence: 0 },
    valid_judgments: count, determinate_judgments: count, insufficient_evidence: 0,
    percentages_among_valid: classifier.id === 'input_ontology' ? { match: 100, no_match: 0, insufficient_evidence: 0 }
      : { no_issue_identified: 100, issue_identified: 0, insufficient_evidence: 0 },
  }))
}

function item(id: string, content: string, flagged = false): Item {
  return { item_id: id, content, reference_answer: '4', status: 'complete',
    labels: Object.fromEntries(spec.classifiers.map(classifier => [classifier.id, {
      label: classifier.id === 'input_ontology' ? 'match' : flagged && classifier.id === 'output_content' ? 'issue_identified' : 'no_issue_identified',
      justification: `A saved explanation for ${classifier.id}.`, evidence: ['Saved supporting evidence.'],
    }])),
  }
}

function savedRun(overrides: Partial<AnalysisRun> = {}): AnalysisRun {
  return { run_id: access.run_id, status: 'ready', message: 'Classifier context is ready.', example, spec,
    summary: { total_items: example.item_count, completed_items: 0, error_items: 0, pending_items: example.item_count,
      complete_snapshot: false, classifiers: distributions(0),
      experiment: { classifier_count: 4, selected_items: 0, completed_item_classifier_judgments: 0, expected_item_classifier_judgments: 0 },
      specification: { deployment_text_matches: true, note: 'Source identifiers checked; semantic grounding unreviewed.' },
    },
    processed: 0, total: example.item_count, complete: 0, errors: 0, completed_judgments: 0,
    items: [], pagination: { page: 1, total_pages: 701 }, usage: { input_tokens: 0, output_tokens: 0 },
    can_continue: false, scope: null, ...overrides,
  }
}

function checkpoint(): AnalysisRun {
  const run = savedRun()
  return { ...run, status: 'checkpoint', message: 'The pilot judgments are saved.', scope: 'pilot',
    processed: 100, complete: 100, completed_judgments: 400, can_continue: true,
    remaining_judgments: { pilot: 0, all: 55660 }, items: [item('first-item', 'A neutral item on the first page.')],
    summary: { ...run.summary!, completed_items: 100, pending_items: 13915, classifiers: distributions(100),
      experiment: { classifier_count: 4, selected_items: 100, completed_item_classifier_judgments: 400, expected_item_classifier_judgments: 400 },
    },
  }
}

function stage(number: number) {
  return screen.getByRole('region', { name: new RegExp(`^${number}\\. ${ITEM_STEPS[number - 1]}`) })
}

function navigation() { return screen.getByRole('navigation', { name: 'Item analysis steps' }) }

async function visit(number: number, user: ReturnType<typeof userEvent.setup>) {
  await user.click(within(navigation()).getByRole('link', { name: new RegExp(ITEM_STEPS[number - 1]) }))
  await waitFor(() => expect(within(navigation()).getByRole('link', { name: new RegExp(ITEM_STEPS[number - 1]) })).toHaveAttribute('aria-current', 'step'))
  await waitFor(() => expect(stage(number)).toHaveFocus())
}

beforeEach(() => {
  vi.clearAllMocks()
  localStorage.clear()
  sessionStorage.clear()
  localStorage.setItem('item_analysis_run_v1', JSON.stringify(access))
  vi.mocked(api.getCatalog).mockResolvedValue({ examples: [example], checkpoint_size: 100 })
  vi.mocked(api.getRun).mockResolvedValue(savedRun())
})

it('presents all six steps with contracts and keeps accepted context accessible without paid work', async () => {
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await screen.findByRole('heading', { name: 'Python checks passed for the saved specification' })
  for (let number = 1; number <= 6; number += 1) {
    const panel = stage(number)
    expect(within(panel).getByText('Input', { selector: 'dt' })).toBeVisible()
    expect(within(panel).getByText('Output', { selector: 'dt' })).toBeVisible()
    expect(within(panel).getByText('Next action', { selector: 'strong' })).toBeVisible()
  }
  expect(within(navigation()).getAllByRole('link')).toHaveLength(6)
  expect(within(navigation()).getByRole('link', { name: /Validate context/ })).toHaveAttribute('aria-current', 'step')
  expect(within(stage(3)).getByRole('heading', { name: 'Scientific correctness remains unreviewed' })).toBeVisible()
  await visit(2, user)
  expect(within(stage(2)).getByRole('heading', { name: 'Deployment requirements' })).toBeVisible()
  expect(within(stage(2)).getByRole('heading', { name: 'Required input categories' })).toBeVisible()
  expect(within(stage(2)).getByRole('heading', { name: 'Context for each dimension' })).toBeVisible()
  await visit(3, user)
  expect(within(stage(3)).getByRole('heading', { name: 'Resulting classifier specification' })).toBeVisible()
  expect(api.createRun).not.toHaveBeenCalled()
  expect(api.classify).not.toHaveBeenCalled()
})

it('separates a completed 100-item pilot from optional dataset coverage and exports', async () => {
  vi.mocked(api.getRun).mockResolvedValue(checkpoint())
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await waitFor(() => expect(within(navigation()).getByRole('link', { name: /Review summary findings/ })).toHaveAttribute('aria-current', 'step'))
  await visit(4, user)
  expect(stage(4)).toHaveTextContent(/Pilot complete: 100\/100 selected items classified/)
  expect(stage(4)).toHaveTextContent(/optional/i)
  expect(stage(1)).toHaveTextContent('14,015')
  expect(within(stage(4)).getByRole('button', { name: 'Continue through all items' })).toBeDisabled()
  await visit(6, user)
  expect(within(stage(6)).queryByText('Independent human review')).not.toBeInTheDocument()
  expect(within(stage(6)).queryByRole('button', { name: /Download blind review worksheet/ })).not.toBeInTheDocument()
  for (const label of [/View report/, /Download complete results package/]) {
    expect(within(stage(6)).getByRole('button', { name: label })).toBeEnabled()
  }
  expect(within(stage(4)).queryByRole('button', { name: /Download/ })).not.toBeInTheDocument()
  expect(api.classify).not.toHaveBeenCalled()
})

it('keeps live processing separate from stale findings and prevents export during classification', async () => {
  const run = checkpoint()
  vi.mocked(api.getRun).mockResolvedValue({ ...run, status: 'running', scope: 'all', can_continue: false,
    processed: 101, complete: 100, completed_judgments: 403 })
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  const progress = await screen.findByRole('progressbar', { name: 'Classification progress' })
  expect(progress).toHaveAttribute('value', '403')
  expect(progress).toHaveAttribute('max', '56060')
  expect(within(navigation()).getByRole('link', { name: /Classify items/ })).toHaveAttribute('aria-current', 'step')
  await visit(5, user)
  expect(within(stage(5)).queryByRole('heading', { name: 'What the items show' })).not.toBeInTheDocument()
  await visit(6, user)
  expect(within(stage(6)).getByRole('button', { name: /Download complete results package/ })).toBeDisabled()
  expect(api.classify).not.toHaveBeenCalled()
})

it('places rejected context in validation without offering item classification', async () => {
  const message = 'Generated context cited an unavailable source after one repair.'
  vi.mocked(api.getRun).mockResolvedValue(savedRun({ status: 'failed', spec: null, summary: null, message,
    failure: { stage: 'specification', code: 'evidence', message } }))
  render(<ItemAnalysis />)
  await screen.findByRole('heading', { name: 'Python checks did not pass' })
  expect(within(navigation()).getByRole('link', { name: /Validate context/ })).toHaveAttribute('aria-current', 'step')
  expect(within(stage(3)).getByRole('alert')).toHaveTextContent(message)
  expect(within(stage(3)).queryByRole('heading', { name: 'Resulting classifier specification' })).not.toBeInTheDocument()
  expect(within(stage(4)).queryByRole('button', { name: /Classify|Resume/ })).not.toBeInTheDocument()
  expect(api.classify).not.toHaveBeenCalled()
})

it('inspects a flagged result from another saved page without starting classifier requests', async () => {
  const run = checkpoint()
  run.summary!.classifiers = distributions(100).map(classifier => classifier.id === 'output_content'
    ? { ...classifier, counts: { no_issue_identified: 99, issue_identified: 1, insufficient_evidence: 0 },
      percentages_among_valid: { no_issue_identified: 99, issue_identified: 1, insufficient_evidence: 0 } } : classifier)
  vi.mocked(api.getRun).mockImplementation(async (_access, page) => ({ ...run,
    items: page === 2 ? [item('later-flagged-item', 'A flagged result saved on page two.', true)] : page === 1 ? run.items : [],
    pagination: { page, total_pages: 701 },
  }))
  const user = userEvent.setup()
  render(<ItemAnalysis />)
  await user.click(await screen.findByRole('button', { name: 'Inspect flagged items (1)' }))
  expect(await screen.findByText('A flagged result saved on page two.', { selector: 'strong' })).toBeVisible()
  expect(within(navigation()).getByRole('link', { name: /Classify items/ })).toHaveAttribute('aria-current', 'step')
  expect(screen.queryByText('A neutral item on the first page.', { selector: 'strong' })).not.toBeInTheDocument()
  expect(api.getRun).toHaveBeenCalledWith(access, 2, expect.any(AbortSignal))
  expect(api.getRun).not.toHaveBeenCalledWith(access, 6, expect.any(AbortSignal))
  expect(api.classify).not.toHaveBeenCalled()
  expect(api.createRun).not.toHaveBeenCalled()
})
