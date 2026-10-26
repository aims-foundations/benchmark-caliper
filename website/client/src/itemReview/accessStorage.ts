import type { RunAccess } from './api'

export const TAB_RUN_STORAGE = 'item_review_run_v1'
export const PIPELINE_RUN_STORAGE = 'item_review_pipeline_run_v1'
type StorageKind = 'sessionStorage' | 'localStorage'

function readAccess(kind: StorageKind, key: string): RunAccess | null {
  try {
    const run = JSON.parse(window[kind].getItem(key) || 'null')
    return run && typeof run.run_id === 'string' && run.run_id
      && typeof run.run_secret === 'string' && run.run_secret
      ? { run_id: run.run_id, run_secret: run.run_secret } : null
  } catch { return null }
}

function writeAccess(kind: StorageKind, key: string, run: RunAccess): void {
  try {
    // Store access only, even if a response later includes more fields.
    window[kind].setItem(key, JSON.stringify({ run_id: run.run_id, run_secret: run.run_secret }))
  } catch { /* The current tab can still use its in-memory access. */ }
}

export function loadReviewAccess(): RunAccess | null {
  const tabRun = readAccess('sessionStorage', TAB_RUN_STORAGE)
  if (tabRun) return tabRun
  const saved = readAccess('localStorage', PIPELINE_RUN_STORAGE)
  // Pin this tab to its restored run if another tab later starts a new one.
  if (saved) writeAccess('sessionStorage', TAB_RUN_STORAGE, saved)
  return saved
}

export function saveReviewAccess(run: RunAccess, pipeline: boolean): void {
  writeAccess('sessionStorage', TAB_RUN_STORAGE, run)
  if (pipeline) writeAccess('localStorage', PIPELINE_RUN_STORAGE, run)
}

export function persistRestoredPipelineAccess(run: RunAccess): void {
  // Migrate existing tabs only after the server confirms their pipeline mode.
  // Polling an older tab must not replace another tab's latest saved review.
  if (!readAccess('localStorage', PIPELINE_RUN_STORAGE)) {
    writeAccess('localStorage', PIPELINE_RUN_STORAGE, run)
  }
}

export function forgetReviewAccess(run: RunAccess | null): void {
  try { sessionStorage.removeItem(TAB_RUN_STORAGE) } catch { /* Storage may be disabled. */ }
  const saved = readAccess('localStorage', PIPELINE_RUN_STORAGE)
  if (run && saved?.run_id === run.run_id && saved.run_secret === run.run_secret) {
    try { localStorage.removeItem(PIPELINE_RUN_STORAGE) } catch { /* Storage may be disabled. */ }
  }
}
