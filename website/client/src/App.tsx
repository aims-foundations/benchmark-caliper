import { useState, useEffect } from 'react'
import { PrivacyNotice } from './components/PrivacyNotice'
import { GallerySidebar } from './components/GallerySidebar'
import { KeyForm } from './components/KeyForm'
import { RunForm } from './components/RunForm'
import {
  ProgressView,
  RUN_STEPS,
  SUMMARY_STEPS,
  EXTRACT_STEPS,
  REGION_STEPS,
  SCORE_STEPS,
  AUTO_STEPS,
} from './components/ProgressView'
import { AnswerForm } from './components/AnswerForm'
import { SummaryView } from './components/SummaryView'
import { ExtractedView } from './components/ExtractedView'
import { RegionView } from './components/RegionView'
import { ComposedPromptView } from './components/ComposedPromptView'
import { ScoringView } from './components/ScoringView'
import { ReportView } from './components/ReportView'
import { ConsentGate } from './components/ConsentGate'
import { MatrixBackdrop } from './components/MatrixBackdrop'
import { hasKey, getKey, clearKey } from './keyStorage'
import { hasConsent } from './consentStorage'
import {
  runPipeline,
  submitAnswers,
  extractPaper,
  generateRegion,
  composePrompt,
  scoreValidity,
  setRunEmail,
  startAutoRun,
  subscribeRunEvents,
  fetchGallery,
  fetchGalleryReport,
  ApiError,
  type PipelineEvent,
  type Question,
  type GalleryEntry,
  type GalleryReport,
} from './api'
import { appPath, stripBasePath } from './paths'

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

interface ComposedState {
  runId: string
  slug: string
  composedPrompt: string
  // Carried forward so "Send to Opus" can kick off scoring.
  regioned: RegionedState
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
  emailStatus?: {
    requested: boolean
    sent?: boolean
    fallback?: boolean
    error?: string | null
  }
}

interface AutoRunningState {
  runId: string
  slug: string
  events: PipelineEvent[]
}

type Phase =
  | { name: 'consent' }
  | { name: 'enter-key' }
  | { name: 'idle' }
  | { name: 'viewing-report'; runId: string }
  | { name: 'running'; state: RunningState }
  | { name: 'answering'; state: AnsweringState }
  | { name: 'submitting'; state: SubmittingState }
  | { name: 'summary'; state: SummaryState }
  | { name: 'auto-running'; state: AutoRunningState }
  | { name: 'extracting'; state: ExtractingState }
  | { name: 'extracted'; state: ExtractedState }
  | { name: 'regioning'; state: RegioningState }
  | { name: 'regioned'; state: RegionedState }
  | { name: 'composed'; state: ComposedState }
  | { name: 'scoring'; state: ScoringState; from: RegionedState }
  | { name: 'scored'; state: ScoredState }
  | { name: 'viewing-gallery'; state: { report: GalleryReport } }
  | { name: 'deleted' }
  | { name: 'error'; message: string }

// Phases where the gallery sidebar is navigable. During an active run
// (and its step-by-step pause points) the gallery is locked so the user
// can't navigate away and lose in-progress work.
const GALLERY_ENABLED_PHASES = new Set([
  'consent',
  'enter-key',
  'idle',
  'scored',
  'viewing-gallery',
  'viewing-report',
  'deleted',
  'error',
])

/**
 * If the page was loaded at /run/<uuid> (from the report-ready email link),
 * return that run_id so the app boots into the report view. Returns null
 * for anything else, including ill-formed paths.
 */
function initialReportRunId(): string | null {
  if (typeof window === 'undefined') return null
  const match = stripBasePath(window.location.pathname).match(
    /^\/run\/([0-9a-fA-F-]{8,64})\/?$/,
  )
  return match ? match[1] : null
}

export function App() {
  const [phase, setPhase] = useState<Phase>(() => {
    const reportRun = initialReportRunId()
    if (reportRun) return { name: 'viewing-report', runId: reportRun }
    if (!hasConsent()) return { name: 'consent' }
    return hasKey() ? { name: 'idle' } : { name: 'enter-key' }
  })
  const [showPrivacy, setShowPrivacy] = useState(false)
  const [galleryEntries, setGalleryEntries] = useState<GalleryEntry[]>([])
  // The user's own finished run, kept for this session so they can
  // switch back to it from the sidebar. Cleared on restart / "Run another".
  const [sessionBenchmark, setSessionBenchmark] = useState<ScoredState | null>(
    null,
  )

  // Load the curated gallery once on mount.
  useEffect(() => {
    fetchGallery()
      .then(setGalleryEntries)
      .catch(() => setGalleryEntries([]))
  }, [])

  /** Enter the scored view and remember the run as this session's benchmark. */
  function enterScored(state: ScoredState): void {
    setSessionBenchmark(state)
    setPhase({ name: 'scored', state })
  }

  function handleConsent(): void {
    setPhase(hasKey() ? { name: 'idle' } : { name: 'enter-key' })
  }

  async function handleSelectCurated(id: string): Promise<void> {
    try {
      const report = await fetchGalleryReport(id)
      setPhase({ name: 'viewing-gallery', state: { report } })
    } catch {
      setPhase({ name: 'error', message: 'Could not load that benchmark.' })
    }
  }

  function handleSelectSession(): void {
    if (sessionBenchmark) {
      setPhase({ name: 'scored', state: sessionBenchmark })
    }
  }

  function handleAddBenchmark(): void {
    setPhase(hasKey() ? { name: 'idle' } : { name: 'enter-key' })
  }

  function handleRestartSession(): void {
    setSessionBenchmark(null)
    handleStartOver()
  }

  function handleKeySaved(): void {
    setPhase({ name: 'idle' })
  }

  function handleChangeKey(): void {
    clearKey()
    setPhase({ name: 'enter-key' })
  }

  function handleStartOver(): void {
    if (
      typeof window !== 'undefined' &&
      stripBasePath(window.location.pathname).startsWith('/run/')
    ) {
      window.history.replaceState(null, '', appPath('/'))
    }
    setPhase({ name: 'idle' })
  }

  async function handleRun(
    pdfFile: File,
    description: string,
    optedInFull: boolean,
    hfDatasetId: string | null,
    hfConfig: string | null,
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
        hfDatasetId,
        hfConfig,
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

  async function handleStart(args: {
    runId: string
    slug: string
    elicitationSummary: string
    email: string
    stepByStep: boolean
  }): Promise<void> {
    // The Anthropic key has to be available for both paths: auto-mode
    // needs the server to have already stashed it (it did on /api/runs),
    // and step-by-step still posts it as a header on each phase call.
    if (!getKey()) {
      setPhase({ name: 'enter-key' })
      return
    }
    try {
      await setRunEmail(args.runId, args.email)
    } catch (e) {
      const message =
        e instanceof ApiError
          ? `Could not save email (${e.status}). Try again.`
          : 'Could not save email. Try again.'
      setPhase({ name: 'error', message })
      return
    }

    if (args.stepByStep) {
      void handleExtract({
        runId: args.runId,
        slug: args.slug,
        elicitationSummary: args.elicitationSummary,
      })
      return
    }

    void handleAutoRun({
      runId: args.runId,
      slug: args.slug,
    })
  }

  async function handleAutoRun(args: {
    runId: string
    slug: string
  }): Promise<void> {
    const events: PipelineEvent[] = []
    setPhase({
      name: 'auto-running',
      state: { runId: args.runId, slug: args.slug, events },
    })
    try {
      await startAutoRun(args.runId)
    } catch (e) {
      setPhase({
        name: 'error',
        message:
          e instanceof ApiError
            ? `Could not start the pipeline (${e.status}).`
            : 'Could not start the pipeline.',
      })
      return
    }

    let scoring: Record<string, unknown> = {}
    let rawText = ''
    let emailStatus: ScoredState['emailStatus']
    let errored: PipelineEvent | null = null

    try {
      for await (const event of subscribeRunEvents(args.runId)) {
        events.push(event)
        setPhase({
          name: 'auto-running',
          state: {
            runId: args.runId,
            slug: args.slug,
            events: [...events],
          },
        })

        if (event.type === 'step-completed' && event.step === '7-score') {
          const out = event.output ?? {}
          if (out.scoring && typeof out.scoring === 'object') {
            scoring = out.scoring as Record<string, unknown>
          }
          if (typeof out.raw === 'string') rawText = out.raw
        } else if (event.type === 'run-complete') {
          emailStatus = event.email
        } else if (event.type === 'error') {
          errored = event
        }
      }
    } catch (e) {
      setPhase({
        name: 'error',
        message:
          e instanceof ApiError
            ? `Lost connection to the pipeline (${e.status}).`
            : 'Lost connection to the pipeline.',
      })
      return
    }

    if (errored) {
      setPhase({
        name: 'error',
        message: `Pipeline failed: ${
          errored.type === 'error' ? errored.errorClass : 'unknown'
        }`,
      })
      return
    }
    if (!rawText) {
      setPhase({ name: 'error', message: 'Pipeline returned no scoring.' })
      return
    }

    enterScored({
      runId: args.runId,
      slug: args.slug,
      scoring,
      rawText,
      emailStatus,
    })
  }

  async function handleExtract(args: {
    runId: string
    slug: string
    elicitationSummary: string
  }): Promise<void> {
    const apiKey = getKey()
    if (!apiKey) {
      setPhase({ name: 'enter-key' })
      return
    }
    const { runId, slug, elicitationSummary } = args
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

  async function handleCompose(): Promise<void> {
    if (phase.name !== 'regioned') return
    const base = phase.state
    try {
      const res = await composePrompt({
        runId: base.runId,
        benchmarkYaml: base.benchmarkYaml,
        regionYaml: base.regionYaml,
        elicitationSummary: base.elicitationSummary,
      })
      setPhase({
        name: 'composed',
        state: {
          runId: base.runId,
          slug: base.slug,
          composedPrompt: res.composed_prompt,
          regioned: base,
        },
      })
    } catch (e) {
      const message =
        e instanceof ApiError
          ? `Could not compose prompt (${e.status})`
          : 'Could not compose prompt'
      setPhase({ name: 'error', message })
    }
  }

  async function handleScore(fromState?: RegionedState): Promise<void> {
    const base =
      fromState ??
      (phase.name === 'regioned' ? phase.state : undefined) ??
      (phase.name === 'composed' ? phase.state.regioned : undefined)
    if (!base) return
    const apiKey = getKey()
    if (!apiKey) {
      setPhase({ name: 'enter-key' })
      return
    }
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

    enterScored({
      runId: base.runId,
      slug: base.slug,
      scoring,
      rawText,
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

  const sessionEntry = sessionBenchmark
    ? {
        benchmarkName:
          typeof sessionBenchmark.scoring.benchmark === 'string'
            ? sessionBenchmark.scoring.benchmark
            : '',
        slug: sessionBenchmark.slug,
      }
    : null
  const galleryActiveId =
    phase.name === 'viewing-gallery'
      ? phase.state.report.id
      : phase.name === 'scored'
        ? 'session'
        : null

  return (
    <div className="app-shell">
      <GallerySidebar
        entries={galleryEntries}
        sessionEntry={sessionEntry}
        activeId={galleryActiveId}
        enabled={GALLERY_ENABLED_PHASES.has(phase.name)}
        onSelectCurated={(id) => void handleSelectCurated(id)}
        onSelectSession={handleSelectSession}
        onAddBenchmark={handleAddBenchmark}
      />
      <main className="app">
      <div className="hero">
        <MatrixBackdrop />
        <header>
          <a
            className="brand"
            href="https://aimslab.stanford.edu"
            target="_blank"
            rel="noreferrer noopener"
          >
            <span className="brand-mark">AIMS</span>
            <span className="brand-tick" aria-hidden="true" />
            <span className="brand-label">AI Measurement Science</span>
          </a>
          <p className="eyebrow">Benchmark Caliper</p>
          <h1>Validity Analyzer</h1>
          <p className="tagline">
            Assess whether an AI benchmark applies to a different deployment
            context.
          </p>
        </header>
      </div>

      {phase.name === 'viewing-report' && (
        <ReportView
          runId={phase.runId}
          onStartOver={handleStartOver}
          onChangeKey={handleChangeKey}
        />
      )}

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
          onStart={(input) => {
            if (phase.name !== 'summary') return
            void handleStart({
              runId: phase.state.runId,
              slug: phase.state.slug,
              elicitationSummary: phase.state.summary,
              email: input.email,
              stepByStep: input.stepByStep,
            })
          }}
        />
      )}

      {phase.name === 'auto-running' && (
        <ProgressView
          events={phase.state.events}
          steps={AUTO_STEPS}
          heading="Running the full pipeline — you can close this tab"
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
          onScore={handleCompose}
        />
      )}

      {phase.name === 'composed' && (
        <ComposedPromptView
          composedPrompt={phase.state.composedPrompt}
          runId={phase.state.runId}
          slug={phase.state.slug}
          onBack={() =>
            setPhase({ name: 'regioned', state: phase.state.regioned })
          }
          onScore={() => handleScore(phase.state.regioned)}
          onChangeKey={handleChangeKey}
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

      {phase.name === 'viewing-gallery' && (
        <ScoringView
          scoring={phase.state.report.scoring}
          rawText={phase.state.report.raw}
          runId={phase.state.report.id}
          slug={phase.state.report.slug}
          pdfUrl={appPath(
            `/api/gallery/${encodeURIComponent(
              phase.state.report.id,
            )}/review.pdf`,
          )}
          readOnly
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

      {phase.name !== 'consent' && phase.name !== 'enter-key' && (
        <button
          type="button"
          className="restart-session"
          onClick={handleRestartSession}
          title="Clear this session and start fresh"
        >
          Restart session ↻
        </button>
      )}
      </main>
    </div>
  )
}
