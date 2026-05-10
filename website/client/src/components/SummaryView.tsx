import { useState } from 'react'
import { exportRun, deleteRun, ApiError } from '../api'

interface Props {
  summary: string
  runId: string
  slug: string
  onStartOver: () => void
  onChangeKey: () => void
  onDeleted: () => void
  onExtract: () => void
}

/**
 * Renders the elicitation summary as preformatted markdown text.
 *
 * We intentionally do NOT parse or render the markdown as HTML — model
 * output is treated as untrusted text per SECURITY.md. The user sees the
 * raw markdown; pretty rendering is a future-slice enhancement that
 * would require a vetted, sandboxed renderer.
 */
export function SummaryView({
  summary,
  runId,
  slug,
  onStartOver,
  onChangeKey,
  onDeleted,
  onExtract,
}: Props) {
  const [busy, setBusy] = useState<null | 'export' | 'delete'>(null)
  const [error, setError] = useState<string | null>(null)

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
        Opus scoring) will consume this. We hold prompts and responses for
        at most 90 days, then auto-delete; you can export or delete sooner
        below.
      </p>

      <pre className="summary-text">{summary}</pre>

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
          className="link danger"
          onClick={handleDelete}
          disabled={busy !== null}
        >
          {busy === 'delete' ? 'Deleting…' : 'Delete from server'}
        </button>
        <button type="button" onClick={onStartOver} disabled={busy !== null}>
          Run another
        </button>
        <button
          type="button"
          onClick={onExtract}
          disabled={busy !== null}
        >
          Extract paper →
        </button>
      </div>
    </section>
  )
}
