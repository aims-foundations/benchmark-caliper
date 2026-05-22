import { useState, type FormEvent } from 'react'
import { exportRun, deleteRun, ApiError } from '../api'

interface Props {
  summary: string
  runId: string
  slug: string
  onStartOver: () => void
  onChangeKey: () => void
  onDeleted: () => void
  /** Called when the user picks a mode and starts the rest of the run. */
  onStart: (input: { stepByStep: boolean }) => void
}

/**
 * Renders the elicitation summary as preformatted markdown text.
 *
 * We intentionally do NOT parse or render the markdown as HTML — model
 * output is treated as untrusted text per SECURITY.md. The user sees the
 * raw markdown; pretty rendering is a future-slice enhancement that
 * would require a vetted, sandboxed renderer.
 *
 * NOTE: the report-ready email collection is temporarily disabled — it
 * needs a configured Resend account (RESEND_API_KEY). Until that's set
 * up, the report is shown on-screen and downloadable instead.
 */
export function SummaryView({
  summary,
  runId,
  slug,
  onStartOver,
  onChangeKey,
  onDeleted,
  onStart,
}: Props) {
  const [busy, setBusy] = useState<null | 'export' | 'delete'>(null)
  const [error, setError] = useState<string | null>(null)
  const [stepByStep, setStepByStep] = useState(false)

  function handleStart(e: FormEvent<HTMLFormElement>): void {
    e.preventDefault()
    onStart({ stepByStep })
  }

  function downloadBlob(content: string, filename: string, type: string): void {
    const blob = new Blob([content], { type })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  function handleDownloadMd(): void {
    downloadBlob(summary, `elicitation_summary_${slug || runId}.md`, 'text/markdown')
  }

  async function handleExport(): Promise<void> {
    setError(null)
    setBusy('export')
    try {
      const data = await exportRun(runId)
      downloadBlob(
        JSON.stringify(data, null, 2),
        `validity_run_${slug || runId}.json`,
        'application/json',
      )
    } catch (e) {
      setError(
        e instanceof ApiError
          ? `Export failed (${e.status}).`
          : 'Export failed.',
      )
    } finally {
      setBusy(null)
    }
  }

  async function handleDelete(): Promise<void> {
    if (
      !window.confirm(
        'Delete this run from our servers? This cannot be undone. ' +
          'You will lose the prompts, responses, and metadata associated with it. ' +
          'Aggregate cost/error data we keep does not identify your run.',
      )
    ) {
      return
    }
    setError(null)
    setBusy('delete')
    try {
      await deleteRun(runId)
      onDeleted()
    } catch (e) {
      setError(
        e instanceof ApiError
          ? `Delete failed (${e.status}).`
          : 'Delete failed.',
      )
      setBusy(null)
    }
  }

  return (
    <section className="summary">
      <h2>Elicitation summary</h2>
      <p className="help">
        Step 2-summary's output. Downstream steps (region YAML, web search,
        Opus scoring) will consume this.
      </p>

      <div className="output-doc">
        <div className="output-doc-bar">
          <span className="output-doc-name">elicitation_summary.md</span>
        </div>
        <pre className="summary-text">{summary}</pre>
      </div>

      <dl className="run-meta">
        <dt>Slug</dt>
        <dd>
          <code>{slug}</code>
        </dd>
        <dt>Run ID</dt>
        <dd>
          <code>{runId}</code>
        </dd>
      </dl>

      {error && (
        <p role="alert" className="inline-error">
          {error}
        </p>
      )}

      <form onSubmit={handleStart} className="email-form">
        <h3>Run the validity scoring</h3>
        <p className="help">
          Scoring takes about 3–7 minutes on your Anthropic key. The
          finished report appears here when it's done, and you can download
          it as Markdown and JSON.
        </p>

        <label className="step-by-step">
          <input
            type="checkbox"
            checked={stepByStep}
            onChange={(e) => setStepByStep(e.target.checked)}
          />
          <span>
            Walk me through each step instead. I'd rather review the
            extracted paper and regional context before scoring.
          </span>
        </label>

        <div className="actions">
          <button type="button" className="link" onClick={onChangeKey}>
            Change key
          </button>
          <button type="button" className="link" onClick={handleDownloadMd}>
            Download .md
          </button>
          <button
            type="button"
            className="link"
            onClick={handleExport}
            disabled={busy !== null}
          >
            {busy === 'export' ? 'Exporting…' : 'Download all data'}
          </button>
          <button
            type="button"
            onClick={onStartOver}
            disabled={busy !== null}
          >
            Run another
          </button>
          <button type="submit" disabled={busy !== null}>
            {stepByStep ? 'Start step-by-step →' : 'Start scoring →'}
          </button>
        </div>
      </form>
    </section>
  )
}
