import { useEffect, useState } from 'react'
import { fetchReport, ApiError, type ReportResponse } from '../api'
import { ScoringView } from './ScoringView'
import { getRun as getItemRun } from '../itemAnalysis/api'
import { assessmentStorageKey, restoreAccess } from '../itemAnalysis/accessStorage'

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
  const [data, setData] = useState<(ReportResponse & { recoveredFromItems?: boolean; deploymentContext?: string }) | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    const controller = new AbortController()
    setData(null)
    setError(null)
    fetchReport(runId)
      .then((r) => {
        if (!cancelled) setData(r)
      })
      .catch(async (e) => {
        if (cancelled) return
        // The item run retains the exact parent assessment. It can outlive the
        // original report artifacts, so recover it using this tab's scoped token.
        const access = restoreAccess(assessmentStorageKey({ kind: 'run', id: runId }))
        if (access) {
          try {
            const itemRun = await getItemRun(access, 1, controller.signal)
            if (cancelled) return
            const context = itemRun.assessment
            if (itemRun.run_id === access.run_id && context?.kind === 'run' && context.id === runId &&
                context.scoring && typeof context.scoring === 'object' && !Array.isArray(context.scoring) && Object.keys(context.scoring).length > 0) {
              setData({
                runId, slug: '', scoring: context.scoring,
                raw: JSON.stringify(context.scoring, null, 2),
                elicitationSummary: context.elicitation_summary,
                deploymentContext: context.deployment,
                recoveredFromItems: true,
              })
              return
            }
          } catch { /* Keep the original report error if the item run cannot recover it. */ }
        }
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
      controller.abort()
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
    <>
    {data.recoveredFromItems && <p className="pipeline-stage-status" role="status">Restored the benchmark assessment saved with your item analysis. You can continue that item analysis below.</p>}
    <ScoringView
      scoring={data.scoring}
      rawText={data.raw}
      runId={data.runId}
      assessment={{ kind: 'run', id: data.runId }}
      elicitationSummary={data.elicitationSummary}
      deploymentContext={data.deploymentContext}
      readOnly={data.recoveredFromItems}
      pdfAvailable={!data.recoveredFromItems}
      slug={data.slug}
      onStartOver={onStartOver}
      onChangeKey={onChangeKey}
    />
    </>
  )
}
