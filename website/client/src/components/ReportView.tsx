import { useEffect, useState } from 'react'
import { fetchReport, ApiError, type ReportResponse } from '../api'
import { ScoringView } from './ScoringView'

interface Props {
  runId: string
  onStartOver: () => void
  onChangeKey: () => void
}

/**
 * Landing page reached from the report-ready email link
 * (/run/:runId). Fetches the stored scoring from the server and hands
 * it to ScoringView for rendering.
 *
 * The run_id in the URL is the only credential, matching the same
 * posture as /api/runs/{run_id}/export.
 */
export function ReportView({ runId, onStartOver, onChangeKey }: Props) {
  const [data, setData] = useState<ReportResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    fetchReport(runId)
      .then((r) => {
        if (!cancelled) setData(r)
      })
      .catch((e) => {
        if (cancelled) return
        setError(
          e instanceof ApiError
            ? e.status === 404
              ? 'This run has already been deleted, or never finished scoring.'
              : `Could not load report (${e.status}).`
            : 'Could not load report.',
        )
      })
    return () => {
      cancelled = true
    }
  }, [runId])

  if (error) {
    return (
      <section className="error" role="alert">
        <h2>Report unavailable</h2>
        <p>{error}</p>
        <button type="button" onClick={onStartOver}>
          Start a new run
        </button>
      </section>
    )
  }

  if (!data) {
    return (
      <section className="progress" role="status" aria-live="polite">
        <h2>Loading your report…</h2>
      </section>
    )
  }

  return (
    <ScoringView
      scoring={data.scoring}
      rawText={data.raw}
      runId={data.runId}
      slug={data.slug}
      onStartOver={onStartOver}
      onChangeKey={onChangeKey}
    />
  )
}
