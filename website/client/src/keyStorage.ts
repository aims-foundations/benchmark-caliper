/**
 * BYOK key storage.
 *
 * The key lives in the user's browser only. It is sent to our backend in
 * the X-Anthropic-Key header on each request and is never put in a cookie,
 * a URL, an analytics payload, or anywhere else it could leak.
 *
 * sessionStorage is the default (cleared when the tab closes); localStorage
 * is used only when the user explicitly opts in via the "remember on this
 * device" checkbox.
 *
 * See website/SECURITY.md item 1 for the verifiable claims this enforces.
 */

const KEY_NAME = 'anthropic_api_key'

export function getKey(): string | null {
  return (
    sessionStorage.getItem(KEY_NAME) ?? localStorage.getItem(KEY_NAME)
  )
}

export function setKey(key: string, persistOnDevice: boolean): void {
  if (persistOnDevice) {
    localStorage.setItem(KEY_NAME, key)
    sessionStorage.removeItem(KEY_NAME)
  } else {
    sessionStorage.setItem(KEY_NAME, key)
    localStorage.removeItem(KEY_NAME)
  }
}

export function clearKey(): void {
  sessionStorage.removeItem(KEY_NAME)
  localStorage.removeItem(KEY_NAME)
}

export function hasKey(): boolean {
  return getKey() !== null
}
