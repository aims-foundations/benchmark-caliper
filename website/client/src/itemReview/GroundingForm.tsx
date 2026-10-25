import { useState, type FormEvent } from 'react'

export function GroundingForm({ busy, onGround }: { busy: boolean; onGround: (apiKey: string) => Promise<boolean> }) {
  const [apiKey, setApiKey] = useState('')

  async function submit(event: FormEvent) {
    event.preventDefault()
    if (busy || !apiKey.trim()) return
    if (await onGround(apiKey.trim())) setApiKey('')
  }

  return <form className="review-panel" onSubmit={event => void submit(event)} aria-labelledby="grounding-start-title">
    <p className="eyebrow">Step 3 · O*NET grounding</p>
    <h2 id="grounding-start-title">Find supporting task vocabulary</h2>
    <p>Search the local healthcare O*NET catalog for descriptions related to each extracted task. GPT-6 Luna checks which passages apply and suggests supported vocabulary for a later benchmark search.</p>
    <p>Your original answers and extracted requirements carry forward unchanged. Tasks outside this catalog’s healthcare scope may have no suitable match.</p>
    <label className="review-field"><span>OpenAI API key for O*NET mapping</span>
      <input type="password" autoComplete="off" spellCheck={false} required maxLength={512} placeholder="sk-…"
        value={apiKey} onChange={event => setApiKey(event.target.value)} disabled={busy} /></label>
    <p className="help">Enter your key again because the earlier key was cleared. It stays in memory and is never saved to browser storage.</p>
    <p className="review-paid-note">Starting authorizes one paid GPT-6 Luna mapping call per task facet after local retrieval.</p>
    <button type="submit" disabled={busy || !apiKey.trim()}>{busy ? 'Starting…' : 'Ground with O*NET'}</button>
  </form>
}
