/**
 * Tests for the BYOK browser-side storage discipline.
 *
 * Each test maps to a verifiable claim in website/SECURITY.md item 1.
 */

import { describe, it, expect, beforeEach } from 'vitest'
import { getKey, setKey, clearKey, hasKey } from './keyStorage'

describe('keyStorage', () => {
  beforeEach(() => {
    sessionStorage.clear()
    localStorage.clear()
    // Clear cookies just in case any other test wrote one.
    for (const c of document.cookie.split(';')) {
      const name = c.split('=')[0]?.trim()
      if (name) document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT`
    }
  })

  it('starts empty', () => {
    expect(hasKey()).toBe(false)
    expect(getKey()).toBeNull()
  })

  it('stores in sessionStorage by default (cleared when tab closes)', () => {
    setKey('sk-ant-test', false)
    expect(sessionStorage.getItem('anthropic_api_key')).toBe('sk-ant-test')
    expect(localStorage.getItem('anthropic_api_key')).toBeNull()
  })

  it('stores in localStorage only when persistent flag is set', () => {
    setKey('sk-ant-test', true)
    expect(localStorage.getItem('anthropic_api_key')).toBe('sk-ant-test')
    expect(sessionStorage.getItem('anthropic_api_key')).toBeNull()
  })

  it('clears both storage backends', () => {
    setKey('sk-ant-test', true)
    clearKey()
    expect(hasKey()).toBe(false)
    expect(sessionStorage.getItem('anthropic_api_key')).toBeNull()
    expect(localStorage.getItem('anthropic_api_key')).toBeNull()
  })

  it('switching from persistent to session-only moves the key', () => {
    setKey('sk-ant-A', true)
    setKey('sk-ant-B', false)
    expect(localStorage.getItem('anthropic_api_key')).toBeNull()
    expect(sessionStorage.getItem('anthropic_api_key')).toBe('sk-ant-B')
  })

  it('does not write the key into a cookie', () => {
    setKey('sk-ant-LEAK_TEST_xyz', false)
    expect(document.cookie).not.toContain('sk-ant')
    expect(document.cookie).not.toContain('LEAK_TEST')
    expect(document.cookie).not.toContain('anthropic_api_key')
  })
})
