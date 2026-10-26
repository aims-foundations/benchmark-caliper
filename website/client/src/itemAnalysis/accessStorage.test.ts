import { beforeEach, expect, it } from 'vitest'
import { assessmentStorageKey, clearStoredValue, restoreAccess, saveAccess } from './accessStorage'

const key = assessmentStorageKey({ kind: 'direct', id: 'direct-test' })
const access = { run_id: 'run-test', run_secret: 'private-access' }

beforeEach(() => { localStorage.clear(); sessionStorage.clear() })

it('migrates a tab record and restores it after the tab storage is cleared', () => {
  sessionStorage.setItem(key, JSON.stringify({ ...access, api_key: 'sk-never-save' }))
  expect(restoreAccess(key)).toEqual(access)
  expect(JSON.parse(localStorage.getItem(key)!)).toEqual(access)
  expect(sessionStorage.getItem(key)).toBeNull()
  sessionStorage.clear()
  expect(restoreAccess(key)).toEqual(access)
})

it('stores only access fields and clears both old and durable records for this assessment', () => {
  saveAccess(key, { ...access, api_key: 'sk-never-save' } as typeof access)
  sessionStorage.setItem(key, JSON.stringify(access))
  localStorage.setItem('another-context', 'keep')
  clearStoredValue(key)
  expect(localStorage.getItem(key)).toBeNull()
  expect(sessionStorage.getItem(key)).toBeNull()
  expect(localStorage.getItem('another-context')).toBe('keep')
})

it('does not accept malformed or incomplete saved access', () => {
  localStorage.setItem(key, '{broken')
  expect(restoreAccess(key)).toBeNull()
  localStorage.setItem(key, JSON.stringify({ run_id: access.run_id }))
  expect(restoreAccess(key)).toBeNull()
})
