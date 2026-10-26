import type { AssessmentReference, RunAccess } from './types'

export function assessmentStorageKey(assessment?: AssessmentReference): string {
  const prefix = 'item_analysis_run_v1'
  return assessment ? `${prefix}:${assessment.kind}:${assessment.id}` : prefix
}

export function restoreAccess(storageKey: string): RunAccess | null {
  try {
    const saved = JSON.parse(restoreStoredValue(storageKey) || 'null')
    if (!saved || typeof saved.run_id !== 'string' || typeof saved.run_secret !== 'string') return null
    const access = { run_id: saved.run_id, run_secret: saved.run_secret }
    saveAccess(storageKey, access)
    return access
  } catch { return null }
}

/** Migrate old tab-scoped records without retaining provider credentials. */
export function restoreStoredValue(key: string): string | null {
  let value: string | null = null
  try { value = localStorage.getItem(key) } catch { /* Try tab storage. */ }
  if (value) return value
  try { return sessionStorage.getItem(key) } catch { return null }
}

export function saveStoredValue(key: string, value: string): void {
  try {
    localStorage.setItem(key, value)
    try { sessionStorage.removeItem(key) } catch { /* Durable copy is saved. */ }
  } catch {
    try { sessionStorage.setItem(key, value) } catch { /* Current view still works in memory. */ }
  }
}

export function clearStoredValue(key: string): void {
  try { localStorage.removeItem(key) } catch { /* Storage may be disabled. */ }
  try { sessionStorage.removeItem(key) } catch { /* Clear each store independently. */ }
}

export function saveAccess(key: string, access: RunAccess): void {
  saveStoredValue(key, JSON.stringify({ run_id: access.run_id, run_secret: access.run_secret }))
}
