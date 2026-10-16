import type { AssessmentReference, RunAccess } from './types'

export function assessmentStorageKey(assessment?: AssessmentReference): string {
  const prefix = 'item_analysis_run_v1'
  return assessment ? `${prefix}:${assessment.kind}:${assessment.id}` : prefix
}

export function restoreAccess(storageKey: string): RunAccess | null {
  try {
    const saved = JSON.parse(sessionStorage.getItem(storageKey) || 'null')
    return saved && typeof saved.run_id === 'string' && typeof saved.run_secret === 'string'
      ? { run_id: saved.run_id, run_secret: saved.run_secret } : null
  } catch { return null }
}
