import { SCORE_DIMENSIONS } from './SixScoreTable'
import type { AnalysisRun, ClassifierSummary } from './types'

/** Use the run-wide summary, never the currently loaded or filtered item page. */
export function dimensionStatistics(dimension?: ClassifierSummary) {
  const counts = [1, 2, 3, 4, 5].map(score => dimension?.counts?.[String(score)] || 0)
  const known = dimension?.known ?? counts.reduce((total, count) => total + count, 0)
  const mean = dimension?.mean_score === undefined
    ? known ? counts.reduce((total, count, index) => total + count * (index + 1), 0) / known : null
    : dimension.mean_score
  return { known, unknown: dimension?.unknown || 0, mean }
}

export function benchmarkScoreLabel(run: AnalysisRun, id: string): string {
  if (run.assessment?.kind === 'direct' || run.spec?.assessment_status === 'not_run') return 'Not run'
  const assessment = run.summary?.original_assessment?.[id]
  if (assessment?.score === null) return 'Unknown'
  return typeof assessment?.score === 'number' ? `${assessment.score} / 5` : 'Not available'
}

export function dimensionAverages(run: AnalysisRun) {
  const dimensions = run.summary?.dimensions?.length ? run.summary.dimensions : run.summary?.classifiers || []
  return SCORE_DIMENSIONS.map(id => ({ id, ...dimensionStatistics(dimensions.find(dimension => dimension.id === id)), benchmark: benchmarkScoreLabel(run, id) }))
}
