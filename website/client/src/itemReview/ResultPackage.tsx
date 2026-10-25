import { useState } from 'react'
import { getReviewPackage, type Review, type RunAccess, type RunResult } from './api'

type PipelineReview = Exclude<RunResult, Review>

export function ResultPackage({ review, run }: { review: PipelineReview; run: RunAccess }) {
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState('')
  const state = review.metadata?.result_state || (review.status !== 'completed' ? 'partial'
    : review.mode === 'adaptive' && review.adaptive?.frozen ? 'frozen' : 'stage_complete')

  async function download() {
    setDownloading(true)
    setError('')
    let url: string | undefined
    try {
      const result = await getReviewPackage(run)
      url = URL.createObjectURL(result.blob)
      const link = document.createElement('a')
      link.href = url
      link.download = result.filename
      link.click()
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Could not download the results package. Please try again.')
    } finally {
      if (url) {
        const downloadUrl = url
        setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000)
      }
      setDownloading(false)
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
    <button type="button" disabled={downloading} onClick={() => void download()}>{downloading ? 'Downloading package…' : 'Download results package'}</button>
    <p className="help">Download before results expire one hour after this run ends. Server restarts also discard results. Keep the package for future review; it cannot be reopened as a website run.</p>
    {error && <p className="review-error" role="alert">{error}</p>}
  </section>
}
