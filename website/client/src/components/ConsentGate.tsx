import { recordConsent } from '../consentStorage'

interface Props {
  onAccept: () => void
}

/**
 * First-visit consent screen. Explains what we log on every run, what we
 * only log with explicit per-run opt-in, and the user's data-subject
 * rights. Acknowledgment is recorded in localStorage so this only shows
 * once per browser profile.
 *
 * No "decline" path — the alternative is closing the tab. We keep the
 * decision granular: per-run opt-in (in the run form) covers the
 * "should we cache the prompt content?" choice separately.
 */
export function ConsentGate({ onAccept }: Props) {
  function handleAccept(): void {
    recordConsent()
    onAccept()
  }

  return (
    <section className="consent-gate" aria-labelledby="consent-heading">
      <h2 id="consent-heading">Before you start</h2>
      <p>
        This tool runs validity-analysis pipeline calls against the Anthropic
        API. Read this once, then you won't see it again on this device.
      </p>

      <h3>Your API key</h3>
      <ul>
        <li>Stays in your browser only.</li>
        <li>
          Sent only in a header on requests to our backend; never written to
          any server-side log, database, or file.
        </li>
        <li>You can revoke it at any time from your Anthropic console.</li>
      </ul>

      <h3>What we always log</h3>
      <ul>
        <li>Which pipeline steps ran, when, on which model.</li>
        <li>Token counts, costs, and step latency.</li>
        <li>SHA-256 hashes of your inputs (so we can dedupe identical papers).</li>
        <li>Whether each step succeeded or failed.</li>
      </ul>

      <h3>What we do NOT log by default</h3>
      <ul>
        <li>Your PDF, your deployment description, your elicitation answers.</li>
        <li>The prompts we send to the model or the responses it returns.</li>
        <li>Your IP address, beyond standard short-lived access logs.</li>
      </ul>
      <p className="help">
        For each run, you can opt in to also store the full prompts and
        responses for 90 days — used only for debugging and pipeline
        improvement. The default for that toggle is off.
      </p>

      <h3>Your rights</h3>
      <ul>
        <li>
          Export every record we have about a run with one click in the
          summary view.
        </li>
        <li>
          Delete every record about a run permanently with one click.
        </li>
      </ul>

      <div className="actions">
        <button type="button" onClick={handleAccept}>
          I understand — let me use the tool
        </button>
      </div>
    </section>
  )
}