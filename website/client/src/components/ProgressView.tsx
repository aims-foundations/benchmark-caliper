import type { PipelineEvent } from '../api'

export interface StepLabel {
  step: string
  label: string
}

interface Props {
  events: PipelineEvent[]
  steps: StepLabel[]
  heading?: string
}

export function ProgressView({ events, steps, heading = 'Running' }: Props) {
  // Build a map: step -> latest status, plus per-step progress for fan-outs.
  const statusByStep = new Map<string, 'started' | 'completed'>()
  const progressByStep = new Map<
    string,
    { completed: number; total: number }
  >()
  for (const e of events) {
    if (e.type === 'step-started') {
      statusByStep.set(e.step, 'started')
      if (typeof e.total === 'number') {
        progressByStep.set(e.step, { completed: 0, total: e.total })
      }
    } else if (e.type === 'step-progress') {
      progressByStep.set(e.step, {
        completed: e.completed,
        total: e.total,
      })
    } else if (e.type === 'step-completed') {
      statusByStep.set(e.step, 'completed')
    }
  }

  return (
    <section className="progress" role="status" aria-live="polite">
      <h2>{heading}</h2>
      <ol className="step-list">
        {steps.map(({ step, label }) => {
          const status = statusByStep.get(step)
          const progress = progressByStep.get(step)
          return (
            <li key={step} data-status={status ?? 'pending'}>
              <span className="step-icon" aria-hidden="true">
                {status === 'completed' ? '✓' : status === 'started' ? '…' : ' '}
              </span>
              <span className="step-label">
                {label}
                {progress && status !== 'completed' && (
                  <span className="step-progress">
                    {' '}
                    ({progress.completed}/{progress.total})
                  </span>
                )}
              </span>
            </li>
          )
        })}
      </ol>
    </section>
  )
}

export const RUN_STEPS: StepLabel[] = [
  { step: '0-slug', label: 'Deriving a slug for your run' },
  { step: '1-metadata', label: 'Extracting paper metadata (pages 1–2)' },
  { step: '2-questions', label: 'Generating elicitation questions' },
]

export const SUMMARY_STEPS: StepLabel[] = [
  { step: '2-summary', label: 'Synthesizing your answers into a summary' },
]

export const EXTRACT_STEPS: StepLabel[] = [
  { step: '3a-extract', label: 'Extracting quotes from each page' },
  { step: '3a-consolidate', label: 'Consolidating the extraction' },
  { step: '3b-select', label: 'Selecting reference examples' },
  { step: '3b-synthesize', label: 'Synthesizing the benchmark YAML' },
]

export const REGION_STEPS: StepLabel[] = [
  { step: '4a-template', label: 'Selecting region templates' },
  { step: '4b-synthesize', label: 'Building the region scaffold' },
  { step: '5-web-search', label: 'Enriching with web search' },
]

export const SCORE_STEPS: StepLabel[] = [
  { step: '7-score', label: 'Scoring with Opus across the 6 dimensions' },
]
