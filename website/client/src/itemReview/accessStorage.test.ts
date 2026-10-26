import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import {
  forgetReviewAccess, loadReviewAccess, persistRestoredPipelineAccess, saveReviewAccess,
  PIPELINE_RUN_STORAGE, TAB_RUN_STORAGE,
} from './accessStorage'

const access = { run_id: 'first-run', run_secret: 'first-secret' }
const other = { run_id: 'second-run', run_secret: 'second-secret' }

beforeEach(() => { sessionStorage.clear(); localStorage.clear() })
afterEach(() => vi.restoreAllMocks())

it('restores a pipeline after closing its tab without storing API keys or answers', () => {
  saveReviewAccess({ ...access, api_key: 'sk-private', deployment: 'Private goal' } as typeof access, true)
  expect(JSON.parse(localStorage.getItem(PIPELINE_RUN_STORAGE)!)).toEqual(access)
  expect(JSON.parse(sessionStorage.getItem(TAB_RUN_STORAGE)!)).toEqual(access)
  sessionStorage.clear()
  expect(loadReviewAccess()).toEqual(access)
  expect(JSON.parse(sessionStorage.getItem(TAB_RUN_STORAGE)!)).toEqual(access)
})

it('keeps an existing tab on its review and preserves another tab when forgetting it', () => {
  saveReviewAccess(access, true)
  localStorage.setItem(PIPELINE_RUN_STORAGE, JSON.stringify(other))
  expect(loadReviewAccess()).toEqual(access)
  persistRestoredPipelineAccess(access)
  forgetReviewAccess(access)
  expect(sessionStorage.getItem(TAB_RUN_STORAGE)).toBeNull()
  expect(JSON.parse(localStorage.getItem(PIPELINE_RUN_STORAGE)!)).toEqual(other)
})

it('removes both copies when forgetting the latest pipeline', () => {
  saveReviewAccess(access, true)
  forgetReviewAccess(access)
  expect(loadReviewAccess()).toBeNull()
})

it('does not remove a saved run with a different access token', () => {
  saveReviewAccess(access, true)
  forgetReviewAccess({ ...access, run_secret: 'different-secret' })
  expect(JSON.parse(localStorage.getItem(PIPELINE_RUN_STORAGE)!)).toEqual(access)
})

it('keeps legacy sampled review access in the tab only', () => {
  saveReviewAccess(access, false)
  expect(loadReviewAccess()).toEqual(access)
  expect(localStorage.length).toBe(0)
  sessionStorage.clear()
  expect(loadReviewAccess()).toBeNull()
})

it('migrates a confirmed pipeline from existing session storage', () => {
  sessionStorage.setItem(TAB_RUN_STORAGE, JSON.stringify(access))
  expect(loadReviewAccess()).toEqual(access)
  expect(localStorage.length).toBe(0)
  persistRestoredPipelineAccess(access)
  sessionStorage.clear()
  expect(loadReviewAccess()).toEqual(access)
})

it.each(['not json', '{}', 'null', '{"run_id":"","run_secret":"secret"}'])('recovers the saved pipeline when the tab record is invalid: %s', invalid => {
  sessionStorage.setItem(TAB_RUN_STORAGE, invalid)
  localStorage.setItem(PIPELINE_RUN_STORAGE, JSON.stringify(access))
  expect(loadReviewAccess()).toEqual(access)
})

it('still uses the tab when persistent storage is blocked', () => {
  vi.spyOn(localStorage, 'setItem').mockImplementation(() => { throw new Error('Storage disabled') })
  vi.spyOn(localStorage, 'getItem').mockImplementation(() => { throw new Error('Storage disabled') })
  expect(() => saveReviewAccess(access, true)).not.toThrow()
  expect(loadReviewAccess()).toEqual(access)
  expect(() => persistRestoredPipelineAccess(access)).not.toThrow()
  expect(() => forgetReviewAccess(access)).not.toThrow()
})
