import { useState, type FormEvent } from 'react'
import { setKey } from '../keyStorage'

interface Props {
  onSaved: () => void
}

export function KeyForm({ onSaved }: Props) {
  const [value, setValue] = useState('')
  const [persist, setPersist] = useState(false)

  function handleSubmit(e: FormEvent<HTMLFormElement>): void {
    e.preventDefault()
    const trimmed = value.trim()
    if (!trimmed) return
    setKey(trimmed, persist)
    setValue('') // clear React state — sessionStorage is the only home now
    onSaved()
  }

  return (
    <form onSubmit={handleSubmit} className="key-form">
      <h2>Enter your Anthropic API key</h2>
      <p className="help">
        Your key is stored on this device only. It is sent directly from
        your browser to our backend on each request and is never logged or
        persisted on our servers. Get a key at{' '}
        <a
          href="https://console.anthropic.com/"
          target="_blank"
          rel="noreferrer noopener"
        >
          console.anthropic.com
        </a>
        .
      </p>

      <label>
        <span className="visually-hidden">API key</span>
        <input
          type="password"
          autoComplete="off"
          spellCheck={false}
          placeholder="sk-ant-..."
          value={value}
          onChange={(e) => setValue(e.target.value)}
          required
        />
      </label>

      <label className="checkbox">
        <input
          type="checkbox"
          checked={persist}
          onChange={(e) => setPersist(e.target.checked)}
        />
        <span>
          Remember on this device. If unchecked, the key is forgotten when
          you close this tab.
        </span>
      </label>

      <button type="submit" disabled={!value.trim()}>
        Save key
      </button>
    </form>
  )
}
