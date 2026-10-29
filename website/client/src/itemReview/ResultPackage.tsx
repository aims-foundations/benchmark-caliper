import { useEffect, useRef, useState } from 'react'
import { getReviewPackage, type PackageDownloadProgress, type Review, type RunAccess, type RunResult } from './api'

type PipelineReview = Exclude<RunResult, Review>

export function ResultPackage({ review, run }: { review: PipelineReview; run: RunAccess }) {
  const [downloading, setDownloading] = useState<PackageDownloadProgress | null>(null)
  const controllerRef = useRef<AbortController | null>(null)
  const [error, setError] = useState('')
  const state = review.metadata?.result_state || (review.status !== 'completed' ? 'partial'
    : review.mode === 'adaptive' && review.adaptive?.frozen ? 'frozen' : 'stage_complete')

  useEffect(() => {
    setDownloading(null)
    setError('')
    return () => {
      controllerRef.current?.abort()
      controllerRef.current = null
    }
  }, [run.run_id, run.run_secret])

  async function download() {
    if (controllerRef.current) return
    const controller = new AbortController()
    controllerRef.current = controller
    setDownloading('preparing')
    setError('')
    let url: string | undefined
    try {
      const result = await getReviewPackage(run, progress => {
        if (!controller.signal.aborted) setDownloading(progress)
      }, controller.signal)
      if (controller.signal.aborted) return
      url = URL.createObjectURL(result.blob)
      const link = document.createElement('a')
      link.href = url
      link.download = result.filename
      link.click()
    } catch (error) {
      if (!controller.signal.aborted) setError(error instanceof Error ? error.message : 'Could not download the results package. Your saved results are unchanged. Please try downloading again.')
    } finally {
      if (url) {
        const downloadUrl = url
        setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000)
      }
      if (controllerRef.current === controller) {
        controllerRef.current = null
        if (!controller.signal.aborted) setDownloading(null)
      }
    }
  }

  return <section className="review-panel" aria-label="Save and share results">
    <h2>Save and share results</h2>
    {review.metadata?.run_name && <p><strong>Run name:</strong> {review.metadata.run_name}</p>}
    <p><strong>{state === 'partial' ? 'Partial snapshot' : state === 'frozen' ? 'Frozen collection' : 'Stage complete'}</strong>
      {' · '}{state === 'partial' ? 'The package contains the results available so far, including any previously accepted collection.'
        : state === 'frozen' ? 'Adaptive screening has ended. The package includes the accepted collection and any remaining coverage gaps.'
          : 'This stage has finished. The package records progress through this stage; later stages may still remain.'}</p>
    <p>Download a ZIP with an HTML report for reading and sharing, a CSV of the selected items, and the complete JSON record. Before collection selection, the CSV has no selected items.</p>
    <button type="button" disabled={downloading !== null} onClick={() => void download()}><span aria-live="polite">{downloading === 'preparing' ? 'Preparing package…' : downloading === 'downloading' ? 'Downloading package…' : 'Download results package'}</span></button>
    <p className="help">Completed progress is saved without a time limit. Return in this browser to continue, even after closing the tab. If a server restart interrupts a stage, its saved results remain available; paid calls do not restart automatically. Keep the package for sharing or a separate copy; it cannot be imported as a website run.</p>
    {error && <p className="review-error" role="alert">{error}</p>}
  </section>
}
