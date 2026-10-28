import { useEffect, useRef, useState, type FormEvent } from 'react'
import { getDirectSetup } from './api'
import { assessmentStorageKey, clearStoredValue, restoreStoredValue, saveStoredValue } from './accessStorage'
import { ItemAnalysis } from './ItemAnalysis'
import type { AssessmentReference, AssessmentSetup, DirectContext } from './types'
import './itemAnalysis.css'

export const DIRECT_CONTEXT_STORAGE_KEY = 'item_analysis_direct_context_v1'
const EMPTY_CONTEXT: DirectContext = { benchmark: '', deployment: '', task_requirements: '', answer_requirements: '', validity_concerns: '' }
const FIELDS = ['benchmark', 'deployment', 'task_requirements', 'answer_requirements', 'validity_concerns'] as const
interface AcceptedContext { context: DirectContext; assessment: AssessmentReference; setup?: AssessmentSetup }

function normalize(value: DirectContext): DirectContext {
  return Object.fromEntries(FIELDS.map(field => [field, (value[field] || '').trim()])) as unknown as DirectContext
}

function restore(): AcceptedContext | null {
  try {
    const saved = JSON.parse(restoreStoredValue(DIRECT_CONTEXT_STORAGE_KEY) || 'null')
    if (!saved || saved.version !== 1 || typeof saved.id !== 'string' || !saved.id.startsWith('direct-') || !saved.context) return null
    for (const field of FIELDS) {
      const value = saved.context[field] ?? (field === 'validity_concerns' ? '' : null)
      if (typeof value !== 'string' || value.length > (field === 'benchmark' ? 200 : 12000) || (field !== 'validity_concerns' && !value.trim())) return null
    }
    const context = normalize(saved.context)
    saveStoredValue(DIRECT_CONTEXT_STORAGE_KEY, JSON.stringify({ version: 1, id: saved.id, context }))
    return { assessment: { kind: 'direct', id: saved.id }, context }
  } catch { return null }
}

/** Start at the item stage using explicit requirements, without a paper assessment. */
export function DirectItemStart() {
  const [accepted, setAccepted] = useState<AcceptedContext | null>(restore)
  const [context, setContext] = useState<DirectContext>(() => accepted?.context || EMPTY_CONTEXT)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const request = useRef<AbortController | null>(null)
  useEffect(() => () => request.current?.abort(), [])

  function change(field: keyof DirectContext, value: string) {
    request.current?.abort()
    setBusy(false)
    setError('')
    setContext(previous => ({ ...previous, [field]: value }))
  }

  function editContext() {
    request.current?.abort()
    if (accepted) clearStoredValue(assessmentStorageKey(accepted.assessment))
    clearStoredValue(DIRECT_CONTEXT_STORAGE_KEY)
    setAccepted(null)
    setError('')
    setBusy(false)
  }

  async function continueToItems(event: FormEvent) {
    event.preventDefault()
    if (busy) return
    const normalized = normalize(context)
    if (FIELDS.some(field => field !== 'validity_concerns' && !normalized[field])) {
      setError('Describe the benchmark, deployment, task requirements, and answer requirements before continuing.')
      return
    }
    request.current?.abort()
    const controller = new AbortController()
    request.current = controller
    setBusy(true)
    setError('')
    try {
      const setup = await getDirectSetup(normalized, '', controller.signal)
      if (controller.signal.aborted) return
      if (setup.assessment.kind !== 'direct') throw new Error('The item context could not be prepared. Please try again.')
      const confirmedContext = normalize(setup.assessment.direct_context || normalized)
      const assessment: AssessmentReference = { kind: 'direct', id: setup.assessment.id }
      // Save only the declared context here; provider keys stay in memory.
      saveStoredValue(DIRECT_CONTEXT_STORAGE_KEY, JSON.stringify({ version: 1, id: assessment.id, context: confirmedContext }))
      setContext(confirmedContext)
      setAccepted({ context: confirmedContext, assessment, setup })
    } catch (problem) {
      if (!controller.signal.aborted) setError(problem instanceof Error ? problem.message : 'Could not find the benchmark. Please try again.')
    } finally {
      if (!controller.signal.aborted) setBusy(false)
    }
  }

  if (accepted) return <ItemAnalysis assessment={accepted.assessment} directContext={accepted.context} initialSetup={accepted.setup} onEditContext={editContext} />

  return <section className="item-analysis-site ia-direct-start" aria-label="New item analysis context">
    <form className="ia-panel ia-direct-form" onSubmit={event => void continueToItems(event)} aria-busy={busy}>
      <p className="ia-eyebrow">Start with your requirements</p><h2>Describe the context for the items</h2>
      <p>Specify what the system needs to do and what a suitable answer looks like. These requirements provide the shared context for each item’s six scores.</p>
      <p className="ia-assessment-not-run"><strong>Benchmark assessment: Not run.</strong> You can begin item analysis without a paper or benchmark-level scores.</p>
      <label className="ia-field"><span>Benchmark</span><input required maxLength={200} value={context.benchmark} onChange={event => change('benchmark', event.target.value)} placeholder="For example, MathDial" /></label>
      <label className="ia-field"><span>Deployment context</span><textarea required rows={4} maxLength={12000} value={context.deployment} onChange={event => change('deployment', event.target.value)} placeholder="Who will use the system, where, in which languages, and for what purpose?" /></label>
      <label className="ia-field"><span>Task requirements</span><textarea required rows={4} maxLength={12000} value={context.task_requirements} onChange={event => change('task_requirements', event.target.value)} placeholder="Which tasks, topics, or input categories should the items cover?" /></label>
      <label className="ia-field"><span>Answer requirements</span><textarea required rows={4} maxLength={12000} value={context.answer_requirements} onChange={event => change('answer_requirements', event.target.value)} placeholder="What should the system produce? Which answers are acceptable, and what constraints matter?" /></label>
      <label className="ia-field"><span>Validity concerns (optional)</span><textarea rows={3} maxLength={12000} value={context.validity_concerns} onChange={event => change('validity_concerns', event.target.value)} placeholder="Any suspected gaps, assumptions, or other issues to check in the items." /></label>
      {error && <p className="ia-error" role="alert">{error}</p>}
      <button type="submit" className="ia-primary" disabled={busy}>{busy ? 'Finding matching items…' : 'Find and confirm benchmark items'}</button>
      <p className="ia-small">This searches dataset metadata and makes no model calls. You will confirm the dataset and prepare shared context before entering an OpenAI key to score items.</p>
      <p className="ia-small">After you continue, this context is saved in this browser so you can return later. Editing it starts a new item analysis with updated shared context.</p>
    </form>
  </section>
}
