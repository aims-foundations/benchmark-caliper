import { useState } from 'react'
import { PrivacyNotice } from './components/PrivacyNotice'
import { KeyForm } from './components/KeyForm'
import { RunForm } from './components/RunForm'
import {
  ProgressView,
  RUN_STEPS,
  SUMMARY_STEPS,
  EXTRACT_STEPS,
  REGION_STEPS,
  SCORE_STEPS,
} from './components/ProgressView'
import { AnswerForm } from './components/AnswerForm'
import { SummaryView } from './components/SummaryView'
import { ExtractForm } from './components/ExtractForm'
import { ExtractedView } from './components/ExtractedView'
import { RegionView } from './components/RegionView'
import { ScoringView } from './components/ScoringView'
import { ConsentGate } from './components/ConsentGate'
import { hasKey, getKey, clearKey } from './keyStorage'
import { hasConsent } from './consentStorage'
import {
  runPipeline,
  submitAnswers,
  extractPaper,
  generateRegion,
  scoreValidity,
  ApiError,
  type PipelineEvent,
  type Question,
} from './api'

interface RunningState {
  events: PipelineEvent[]
  description: string
  optedInFull: boolean
}

interface AnsweringState extends RunningState {
  runId: string
  slug: string
  metadata: string
  questions: Question[]
}

interface SubmittingState extends AnsweringState {
  events: PipelineEvent[]
}

interface SummaryState {
  runId: string
  slug: string
  summary: string
}

interface ExtractingState {
  runId: string
  slug: string
  events: PipelineEvent[]
  elicitationSummary: string
}

interface ExtractedState {
  runId: string
  slug: string
  paperSummary: string
  benchmarkYaml: string
  pageCount: number
  selectedExamples: string[]
  elicitationSummary: string
}

interface RegioningState {
  runId: string
  slug: string
  events: PipelineEvent[]
  elicitationSummary: string
  benchmarkYaml: string
  paperSummary: string
}

interface RegionedState {
  runId: string
  slug: string
  regionYaml: string
  scaffoldYaml: string
  selectedTemplates: string[]
  webSearchUsed: boolean
  // Carried forward for the scoring step:
  paperSummary: string
  benchmarkYaml: string
  elicitationSummary: string
}

interface ScoringState {
  runId: string
  slug: string
  events: PipelineEvent[]
}

interface ScoredState {
  runId: string
  slug: string
  scoring: Record<string, unknown>
  rawText: string
}

type Phase =
  | { name: 'consent' }
  | { name: 'enter-key' }
  | { name: 'idle' }
  | { name: 'running'; state: RunningState }
  | { name: 'answering'; state: AnsweringState }
  | { name: 'submitting'; state: SubmittingState }
  | { name: 'summary'; state: SummaryState }
  | {
      name: 'extract-prompt'
      runId: string
      slug: string
      elicitationSummary: string
    }
  | { name: 'extracting'; state: ExtractingState }
  | { name: 'extracted'; state: ExtractedState }
  | { name: 'regioning'; state: RegioningState }
  | { name: 'regioned'; state: RegionedState }
  | { name: 'scoring'; state: ScoringState; from: RegionedState }
  | { name: 'scored'; state: ScoredState }
  | { name: 'deleted' }
  | { name: 'error'; message: string }

export function App() {
  const [phase, setPhase] = useState<Phase>(() => {
    if (!hasConsent()) return { name: 'consent' }
    return hasKey() ? { name: 'idle' } : { name: 'enter-key' }
  })
  const [showPrivacy, setShowPrivacy] = useState(false)

  function handleConsent(): void {
    setPhase(hasKey() ? { name: 'idle' } : { name: 'enter-key' })
  }

  function handleKeySaved(): void {
    setPhase({ name: 'idle' })
  }

  function handleChangeKey(): void {
    clearKey()
    setPhase({ name: 'enter-key' })
  }

  function handleStartOver(): void {
    setPhase({ name: 'idle' })
  }

  async function handleRun(
    pdfFile: File,
    description: string,
    optedInFull: boolean,
  ): Promise<void> {
    const apiKey = getKey()
    if (!apiKey) {
      setPhase({ name: 'enter-key' })
      return
    }

    const events: PipelineEvent[] = []
    setPhase({
      name: 'running',
      state: { events, description, optedInFull },
    })

    let questions: Question[] = []
    let metadata = ''
    let runId = ''
    let slug = ''
    let errored: PipelineEvent | null = null

    try {
      for await (const event of runPipeline({
        apiKey,
        pdfFile,
        deploymentDescription: description,
        optedInFull,
      })) {
        events.push(event)
        setPhase({
          name: 'running',
          state: { events: [...events], description, optedInFull },
        })

        if (
          event.type === 'step-completed' &&
          event.step === '2-questions'
        ) {
          const out = event.output ?? {}
          if (Array.isArray(out.questions)) questions = out.questions as Question[]
          if (typeof out.metadata === 'string') metadata = out.metadata
          if (typeof out.slug === 'string') slug = out.slug
          if (typeof out.run_id === 'string') runId = out.run_id
        } else if (event.type === 'awaiting-answers') {
          runId = event.runId
          slug = event.slug
        } else if (event.type === 'error') {
          errored = event
        }
      }
    } catch (e) {
      const message =
        e instanceof ApiError
          ? `Request failed (${e.status})`
          : 'Request failed'
      setPhase({ name: 'error', message })
      return
    }

    if (errored) {
      setPhase({
        name: 'error',
        message: `Pipeline failed: ${errored.type === 'error' ? errored.errorClass : 'unknown'}`,
      })
      return
    }

    if (!runId || questions.length === 0) {
      setPhase({ name: 'error', message: 'Run completed without questions.' })
      return
    }

    setPhase({
      name: 'answering',
      state: {
        events,
        description,
        optedInFull,
        runId,
        slug,
        metadata,
        questions,
      },
    })
  }

  async function handleExtract(pdfFile: File): Promise<void> {
    if (phase.name !== 'extract-prompt') return
    const apiKey = getKey()
    if (!apiKey) {
      setPhase({ name: 'enter-key' })
      return
    }
    const { runId, slug, elicitationSummary } = phase
    const events: PipelineEvent[] = []
    setPhase({
      name: 'extracting',
      state: { runId, slug, events, elicitationSummary },
    })

    let paperSummary = ''
    let benchmarkYaml = ''
    let pageCount = 0
    let selectedExamples: string[] = []
    let errored: PipelineEvent | null = null

    try {
      for await (const event of extractPaper({
        apiKey,
        runId,
        pdfFile,
        elicitationSummary,
      })) {
        events.push(event)
        setPhase({
          name: 'extracting',
          state: { runId, slug, events: [...events], elicitationSummary },
        })

        if (event.type === 'step-completed') {
          const out = event.output ?? {}
          if (
            event.step === '3a-consolidate' &&
            typeof out.paper_summary === 'string'
          ) {
            paperSummary = out.paper_summary
          } else if (
            event.step === '3b-synthesize' &&
            typeof out.benchmark_yaml === 'string'
          ) {
            benchmarkYaml = out.benchmark_yaml
          }
        } else if (event.type === 'extract-complete') {
          pageCount = event.pageCount
          selectedExamples = event.selectedExamples
        } else if (event.type === 'error') {
          errored = event
        }
      }
    } catch (e) {
      const message =
        e instanceof ApiError
          ? `Request failed (${e.status})`
          : 'Request failed'
      setPhase({ name: 'error', message })
      return
    }

    if (errored) {
      setPhase({
        name: 'error',
        message: `Extraction failed: ${errored.type === 'error' ? errored.errorClass : 'unknown'}`,
      })
      return
    }
    if (!paperSummary || !benchmarkYaml) {
      setPhase({
        name: 'error',
        message: 'Extraction returned incomplete output.',
      })
      return
    }

    setPhase({
      name: 'extracted',
      state: {
        runId,
        slug,
        paperSummary,
        benchmarkYaml,
        pageCount,
        selectedExamples,
        elicitationSummary,
      },
    })
  }

  async function handleGenerateRegion(): Promise<void> {
    if (phase.name !== 'extracted') return
    const apiKey = getKey()
    if (!apiKey) {
      setPhase({ name: 'enter-key' })
      return
    }
    const base = phase.state
    const events: PipelineEvent[] = []
    setPhase({
      name: 'regioning',
      state: {
        runId: base.runId,
        slug: base.slug,
        events,
        elicitationSummary: base.elicitationSummary,
        benchmarkYaml: base.benchmarkYaml,
        paperSummary: base.paperSummary,
      },
    })

    let scaffoldYaml = ''
    let regionYaml = ''
    let selectedTemplates: string[] = []
    let webSearchUsed = false
    let errored: PipelineEvent | null = null

    try {
      for await (const event of generateRegion({
        apiKey,
        runId: base.runId,
        elicitationSummary: base.elicitationSummary,
        benchmarkYaml: base.benchmarkYaml,
      })) {
        events.push(event)
        setPhase({
          name: 'regioning',
          state: {
            runId: base.runId,
            slug: base.slug,
            events: [...events],
            elicitationSummary: base.elicitationSummary,
            benchmarkYaml: base.benchmarkYaml,
            paperSummary: base.paperSummary,
          },
        })

        if (event.type === 'step-completed') {
          const out = event.output ?? {}
          if (
            event.step === '4b-synthesize' &&
            typeof out.region_scaffold === 'string'
          ) {
            scaffoldYaml = out.region_scaffold
          } else if (
            event.step === '5-web-search' &&
            typeof out.region_yaml === 'string'
          ) {
            regionYaml = out.region_yaml
          }
        } else if (event.type === 'region-complete') {
          selectedTemplates = event.selectedTemplates
          webSearchUsed = event.webSearchUsed
        } else if (event.type === 'error') {
          errored = event
        }
      }
    } catch (e) {
      const message =
        e instanceof ApiError
          ? `Request failed (${e.status})`
          : 'Request failed'
      setPhase({ name: 'error', message })
      return
    }

    if (errored) {
      setPhase({
        name: 'error',
        message: `Region generation failed: ${errored.type === 'error' ? errored.errorClass : 'unknown'}`,
      })
      return
    }
    // If web search was skipped, the final region YAML is the scaffold.
    if (!regionYaml) regionYaml = scaffoldYaml
    if (!regionYaml) {
      setPhase({ name: 'error', message: 'Region generation produced no YAML.' })
      return
    }

    setPhase({
      name: 'regioned',
      state: {
        runId: base.runId,
        slug: base.slug,
        regionYaml,
        scaffoldYaml: scaffoldYaml || regionYaml,
        selectedTemplates,
        webSearchUsed,
        // Carry artifacts forward for the scoring step.
        paperSummary: base.paperSummary,
        benchmarkYaml: base.benchmarkYaml,
        elicitationSummary: base.elicitationSummary,
      },
    })
  }

  async function handleScore(): Promise<void> {
    if (phase.name !== 'regioned') return
    const apiKey = getKey()
    if (!apiKey) {
      setPhase({ name: 'enter-key' })
      return
    }
    const base = phase.state
    const events: PipelineEvent[] = []
    setPhase({
      name: 'scoring',
      state: { runId: base.runId, slug: base.slug, events },
      from: base,
    })

    let scoring: Record<string, unknown> = {}
    let rawText = ''
    let errored: PipelineEvent | null = null

    try {
      for await (const event of scoreValidity({
        apiKey,
        runId: base.runId,
        paperSummary: base.paperSummary,
        benchmarkYaml: base.benchmarkYaml,
        regionYaml: base.regionYaml,
        elicitationSummary: base.elicitationSummary,
      })) {
        events.push(event)
        setPhase({
          name: 'scoring',
          state: {
            runId: base.runId,
            slug: base.slug,
            events: [...events],
          },
          from: base,
        })

        if (
          event.type === 'step-completed' &&
          event.step === '7-score'
        ) {
          const out = event.output ?? {}
          if (out.scoring && typeof out.scoring === 'object') {
            scoring = out.scoring as Record<string, unknown>
          }
          if (typeof out.raw === 'string') {
            rawText = out.raw
          }
        } else if (event.type === 'error') {
          errored = event
        }
      }
    } catch (e) {
      const message =
        e instanceof ApiError
          ? `Request failed (${e.status})`
          : 'Request failed'
      setPhase({ name: 'error', message })
      return
    }

    if (errored) {
      setPhase({
        name: 'error',
        message: `Scoring failed: ${errored.type === 'error' ? errored.errorClass : 'unknown'}`,
      })
      return
    }
    if (!rawText) {
      setPhase({ name: 'error', message: 'Scoring returned no output.' })
      return
    }

    setPhase({
      name: 'scored',
      state: {
        runId: base.runId,
        slug: base.slug,
        scoring,
        rawText,
      },
    })
  }

  async function handleAnswers(
    answers: Array<{ id: string; answer: string }>,
  ): Promise<void> {
    if (phase.name !== 'answering') return
    const apiKey = getKey()
    if (!apiKey) {
      setPhase({ name: 'enter-key' })
      return
    }

    const base = phase.state
    const events: PipelineEvent[] = []
    setPhase({ name: 'submitting', state: { ...base, events } })

    let summary = ''
    let errored: PipelineEvent | null = null

    try {
      for await (const event of submitAnswers({
        apiKey,
        runId: base.runId,
        deploymentDescription: base.description,
        metadata: base.metadata,
        questions: base.questions,
        answers,
        optedInFull: base.optedInFull,
      })) {
        events.push(event)
        setPhase({
          name: 'submitting',
          state: { ...base, events: [...events] },
        })

        if (
          event.type === 'step-completed' &&
          event.step === '2-summary'
        ) {
          const out = event.output ?? {}
          if (typeof out.summary === 'string') summary = out.summary
        } else if (event.type === 'error') {
          errored = event
        }
      }
    } catch (e) {
      const message =
        e instanceof ApiError
          ? `Request failed (${e.status})`
          : 'Request failed'
      setPhase({ name: 'error', message })
      return
    }

    if (errored) {
      setPhase({
        name: 'error',
        message: `Pipeline failed: ${errored.type === 'error' ? errored.errorClass : 'unknown'}`,
      })
      return
    }

    if (!summary) {
      setPhase({ name: 'error', message: 'Summary call returned no content.' })
      return
    }

    setPhase({
      name: 'summary',
      state: { runId: base.runId, slug: base.slug, summary },
    })
  }

  return (
    <main className="app">
      <header>
        <h1>Validity Analyzer</h1>
        <p className="tagline">
          Assess whether an AI benchmark applies to a different deployment
          context.
        </p>
      </header>

      {phase.name === 'consent' && <ConsentGate onAccept={handleConsent} />}

      {phase.name === 'enter-key' && <KeyForm onSaved={handleKeySaved} />}

      {phase.name === 'idle' && (
        <RunForm onSubmit={handleRun} onChangeKey={handleChangeKey} />
      )}

      {phase.name === 'running' && (
        <ProgressView events={phase.state.events} steps={RUN_STEPS} />
      )}

      {phase.name === 'answering' && (
        <AnswerForm
          questions={phase.state.questions}
          onSubmit={handleAnswers}
          onChangeKey={handleChangeKey}
        />
      )}

      {phase.name === 'submitting' && (
        <ProgressView
          events={phase.state.events}
          steps={SUMMARY_STEPS}
          heading="Building your summary"
        />
      )}

      {phase.name === 'summary' && (
        <SummaryView
          summary={phase.state.summary}
          runId={phase.state.runId}
          slug={phase.state.slug}
          onStartOver={handleStartOver}
          onChangeKey={handleChangeKey}
          onDeleted={() => setPhase({ name: 'deleted' })}
          onExtract={() =>
            setPhase({
              name: 'extract-prompt',
              runId: phase.state.runId,
              slug: phase.state.slug,
              elicitationSummary: phase.state.summary,
            })
          }
        />
      )}

      {phase.name === 'extract-prompt' && (
        <ExtractForm
          onSubmit={handleExtract}
          onSkip={handleStartOver}
          onChangeKey={handleChangeKey}
        />
      )}

      {phase.name === 'extracting' && (
        <ProgressView
          events={phase.state.events}
          steps={EXTRACT_STEPS}
          heading="Extracting the paper"
        />
      )}

      {phase.name === 'extracted' && (
        <ExtractedView
          paperSummary={phase.state.paperSummary}
          benchmarkYaml={phase.state.benchmarkYaml}
          pageCount={phase.state.pageCount}
          selectedExamples={phase.state.selectedExamples}
          runId={phase.state.runId}
          slug={phase.state.slug}
          onStartOver={handleStartOver}
          onChangeKey={handleChangeKey}
          onGenerateRegion={handleGenerateRegion}
        />
      )}

      {phase.name === 'regioning' && (
        <ProgressView
          events={phase.state.events}
          steps={REGION_STEPS}
          heading="Building region context"
        />
      )}

      {phase.name === 'regioned' && (
        <RegionView
          regionYaml={phase.state.regionYaml}
          scaffoldYaml={phase.state.scaffoldYaml}
          selectedTemplates={phase.state.selectedTemplates}
          webSearchUsed={phase.state.webSearchUsed}
          runId={phase.state.runId}
          slug={phase.state.slug}
          onStartOver={handleStartOver}
          onChangeKey={handleChangeKey}
          onScore={handleScore}
        />
      )}

      {phase.name === 'scoring' && (
        <ProgressView
          events={phase.state.events}
          steps={SCORE_STEPS}
          heading="Scoring with Opus (this can take a minute)"
        />
      )}

      {phase.name === 'scored' && (
        <ScoringView
          scoring={phase.state.scoring}
          rawText={phase.state.rawText}
          runId={phase.state.runId}
          slug={phase.state.slug}
          onStartOver={handleStartOver}
          onChangeKey={handleChangeKey}
        />
      )}

      {phase.name === 'deleted' && (
        <section className="result" role="status">
          <h2>Run deleted</h2>
          <p className="help">
            All prompts, responses, and metadata for that run have been
            removed from our servers. Aggregate cost and error counts that
            do not identify your run remain in our long-term store.
          </p>
          <div className="actions">
            <button type="button" className="link" onClick={handleChangeKey}>
              Change key
            </button>
            <button type="button" onClick={handleStartOver}>
              Run another
            </button>
          </div>
        </section>
      )}

      {phase.name === 'error' && (
        <div role="alert" className="error">
          <p>{phase.message}</p>
          <button type="button" onClick={handleStartOver}>
            Try again
          </button>
        </div>
      )}

      <footer>
        <p>
          Your API key stays on this device. We never store it on our servers.
          {' '}
          <button
            type="button"
            className="link"
            onClick={() => setShowPrivacy(true)}
          >
            Privacy notice
          </button>
        </p>
      </footer>

      {showPrivacy && (
        <div className="modal-overlay" role="dialog" aria-modal="true">
          <div className="modal-body">
            <PrivacyNotice onClose={() => setShowPrivacy(false)} />
          </div>
        </div>
      )}
    </main>
  )
}
