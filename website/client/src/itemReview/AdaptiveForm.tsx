import { useState, type FormEvent } from 'react'
import type { AdaptiveRequest, AdaptiveSettings } from './api'

export function AdaptiveForm({ busy, onAdapt, settings }: {
  busy: boolean; onAdapt: (apiKey: string, body: AdaptiveRequest) => Promise<boolean>; settings?: AdaptiveSettings
}) {
  const [apiKey, setApiKey] = useState('')
  const [seed, setSeed] = useState('0')
  const [limited, setLimited] = useState(false)
  const [ceiling, setCeiling] = useState('')
  const [inputRate, setInputRate] = useState('')
  const [cachedRate, setCachedRate] = useState('')
  const [outputRate, setOutputRate] = useState('')
  const resuming = settings != null
  const validSeed = seed.trim() !== '' && Number.isSafeInteger(Number(seed)) && Number(seed) >= 0 && Number(seed) <= 2 ** 32 - 1
  const validPrice = (value: string, positive = false) => value.trim() !== '' && Number.isFinite(Number(value)) && (positive ? Number(value) > 0 : Number(value) >= 0)
  const validCost = !limited || (validPrice(ceiling, true) && validPrice(inputRate, true) && validPrice(cachedRate) && validPrice(outputRate, true) && Number(cachedRate) <= Number(inputRate))
  const valid = !!apiKey.trim() && (resuming || (validSeed && validCost))

  async function submit(event: FormEvent) {
    event.preventDefault()
    if (!busy && valid) {
      const body: AdaptiveRequest = resuming ? {} : {
        seed: Number(seed), max_cost_usd: limited ? Number(ceiling) : null,
        input_price_per_million: limited ? Number(inputRate) : null,
        cached_input_price_per_million: limited ? Number(cachedRate) : null,
        output_price_per_million: limited ? Number(outputRate) : null,
      }
      if (await onAdapt(apiKey.trim(), body)) setApiKey('')
    }
  }

  return <form className="review-panel" onSubmit={event => void submit(event)} aria-labelledby="adaptive-start-title">
    <p className="eyebrow">Step 7 · Adaptive screening</p>
    <h2 id="adaptive-start-title">{resuming ? 'Resume adaptive screening' : 'Improve the collection with adaptive screening'}</h2>
    <p>Screen up to 160 distinct candidates in total, including the initial screening. Each batch takes up to eight unseen items from the saved retrieval queues, then selects a collection of up to 30 items total.</p>
    <p>In 80% of decisions, choose the queue with the highest estimated selection yield adjusted for coverage gaps. In 20%, explore an available queue at random. Every completed batch preserves achieved coverage.</p>
    {resuming ? <p>Resume the pending batch and retain completed assessments, queue statistics, and the last accepted collection. The saved seed and cost settings stay unchanged.</p> : <>
      <label className="review-field"><span>Random seed</span><input type="number" min="0" step="1" max={2 ** 32 - 1} required value={seed} onChange={event => setSeed(event.target.value)} disabled={busy} /></label>
      <label className="adaptive-toggle"><input type="checkbox" checked={limited} onChange={event => setLimited(event.target.checked)} disabled={busy} /> Set an additional screening cost ceiling</label>
      {limited && <fieldset className="adaptive-cost-fields" disabled={busy}>
        <legend>Cost settings for this adaptive run</legend>
        <label className="review-field"><span>Additional screening cost ceiling (USD)</span><input type="number" min="0" step="any" required value={ceiling} onChange={event => setCeiling(event.target.value)} /></label>
        <p className="help">Enter GPT-6 Luna’s base prices for prompts up to 272,000 input tokens, using your account’s processing tier and regional rates. Input and output prices must be positive; the cached input price is for cache reads and can be zero but cannot exceed the input price.</p>
        <label className="review-field"><span>Input price per million tokens (USD)</span><input type="number" min="0" step="any" required value={inputRate} onChange={event => setInputRate(event.target.value)} /></label>
        <label className="review-field"><span>Cached input price per million tokens (USD)</span><input type="number" min="0" step="any" required value={cachedRate} onChange={event => setCachedRate(event.target.value)} /></label>
        <label className="review-field"><span>Output price per million tokens (USD)</span><input type="number" min="0" step="any" required value={outputRate} onChange={event => setOutputRate(event.target.value)} /></label>
        <p className="help">Cache writes use 1.25× the input price for 30 minutes or 2.5× for 12 hours. These replace the ordinary input charge for written tokens. Reservations include the default 30-minute write rate.</p>
        <p className="help">Above 272,000 input tokens, all input and cache rates double and the output rate increases by 1.5× for the whole request. Reservations apply this tier when the input estimate exceeds that threshold.</p>
        <p className="help">The ceiling applies only to Step 7 calls, including retries. Earlier calls are excluded. Reservations estimate the next call’s cost; they do not guarantee your final provider invoice.</p>
      </fieldset>}
    </>}
    {resuming && <p className="help">Saved seed: {settings.seed}. {settings.max_cost_usd == null ? 'No additional screening cost ceiling is set.' : `Additional screening cost ceiling: $${settings.max_cost_usd}. This applies only to Step 7 calls, including retries, and is an estimate rather than an invoice guarantee.`}</p>}
    <label className="review-field"><span>OpenAI API key for adaptive screening</span>
      <input type="password" autoComplete="off" spellCheck={false} required maxLength={512} placeholder="sk-…" value={apiKey} onChange={event => setApiKey(event.target.value)} disabled={busy} />
    </label>
    <p className="help">Your key stays in memory and is never saved to browser storage.</p>
    <p className="review-paid-note">{resuming ? 'Resuming' : 'Starting'} authorizes paid item assessments using the saved screening model and prompt. Screening stops at the candidate limit, queue exhaustion, or the configured cost ceiling. Coverage gaps may remain.</p>
    <button type="submit" disabled={busy || !valid}>{busy ? 'Starting…' : resuming ? 'Resume adaptive screening' : 'Start adaptive screening'}</button>
  </form>
}
