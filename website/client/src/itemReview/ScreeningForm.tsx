import { useState, type FormEvent } from 'react'

export function ScreeningForm({ busy, onScreen, remaining, retained = 0 }: {
  busy: boolean; onScreen: (apiKey: string) => Promise<boolean>; remaining?: number; retained?: number
}) {
  const [apiKey, setApiKey] = useState('')
  const continuing = remaining != null

  async function submit(event: FormEvent) {
    event.preventDefault()
    if (!busy && apiKey.trim() && await onScreen(apiKey.trim())) setApiKey('')
  }

  return <form className="review-panel" onSubmit={event => void submit(event)} aria-labelledby="screening-start-title">
    <p className="eyebrow">Step 5: Initial screening</p>
    <h2 id="screening-start-title">{continuing ? 'Continue the initial screening' : 'Assess the first 48 distinct candidates'}</h2>
    {continuing ? <p>{retained} completed assessments are retained. Continue with up to {remaining} items that are pending or had an assessment error, using the same initial allocation.</p>
      : <p>Up to 48 distinct candidates are distributed as evenly as the available task queues allow. Each item is assessed once, even when it appears in several queues. If fewer than 48 distinct candidates are available, the allocation shows the shortfall.</p>}
    <p>GPT-6 Luna identifies the task each item actually tests and rates all six validity dimensions with supporting evidence. Four dimensions determine the screening gate. Coverage requirements are checked separately.</p>
    <label className="review-field"><span>OpenAI API key for initial screening</span>
      <input type="password" autoComplete="off" spellCheck={false} required maxLength={512} placeholder="sk-…"
        value={apiKey} onChange={event => setApiKey(event.target.value)} disabled={busy} /></label>
    <p className="help">Enter your key again because the earlier key was cleared. It stays in memory and is never saved to browser storage.</p>
    <p className="review-paid-note">Starting authorizes up to {remaining ?? 48} paid GPT-6 Luna item assessments. This stage stops at the screening results; final benchmark selection is a later step.</p>
    <button type="submit" disabled={busy || !apiKey.trim() || remaining === 0}>{busy ? 'Starting…' : continuing ? 'Continue screening' : 'Screen initial candidates'}</button>
  </form>
}
