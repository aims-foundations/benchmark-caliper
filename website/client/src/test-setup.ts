import '@testing-library/jest-dom/vitest'

/**
 * Node 25 exposes a built-in `localStorage` global without the real Storage
 * methods (no .clear(), .setItem(), etc.) unless `--localstorage-file` is
 * passed. That stub overrides anything happy-dom/jsdom set up. We replace it
 * with a Map-backed Storage so tests behave like a real browser.
 */
class MapStorage implements Storage {
  private store = new Map<string, string>()
  get length(): number {
    return this.store.size
  }
  clear(): void {
    this.store.clear()
  }
  getItem(key: string): string | null {
    return this.store.get(key) ?? null
  }
  key(i: number): string | null {
    return Array.from(this.store.keys())[i] ?? null
  }
  removeItem(key: string): void {
    this.store.delete(key)
  }
  setItem(key: string, value: string): void {
    this.store.set(key, String(value))
  }
}

const ls = new MapStorage()
const ss = new MapStorage()

Object.defineProperty(globalThis, 'localStorage', {
  value: ls,
  configurable: true,
  writable: true,
})
Object.defineProperty(globalThis, 'sessionStorage', {
  value: ss,
  configurable: true,
  writable: true,
})

if (typeof window !== 'undefined') {
  Object.defineProperty(window, 'localStorage', {
    value: ls,
    configurable: true,
    writable: true,
  })
  Object.defineProperty(window, 'sessionStorage', {
    value: ss,
    configurable: true,
    writable: true,
  })
}
