/**
 * Per-browser consent acknowledgment.
 *
 * Stored in localStorage so the user only sees the consent gate once per
 * device. Clearing browser data resets it. We bump the version suffix
 * (`consent_v2`, etc.) when the privacy notice changes materially —
 * everyone sees the new gate again.
 *
 * No server-side state. The gate is purely a UX nudge; the actual
 * privacy guarantees come from the backend defaults and the redaction
 * gate, not from the user clicking a button.
 */

const KEY = 'consent_v1'

export function hasConsent(): boolean {
  return localStorage.getItem(KEY) === 'yes'
}

export function recordConsent(): void {
  localStorage.setItem(KEY, 'yes')
}

export function clearConsent(): void {
  localStorage.removeItem(KEY)
}