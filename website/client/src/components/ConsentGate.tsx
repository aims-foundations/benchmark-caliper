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

      <h3>About the scores you'll see</h3>
      <p>
        The pipeline is still a work in progress, and we're improving it as
        we learn. Each validity score reflects Claude Opus's reading of the
        documents you share - a careful, structured opinion rather than the
        final word. Please treat the report as a useful starting point for
        thinking through your benchmark's fit, not a verdict. We'll share a
        fuller note alongside the scores themselves, and there's a feedback
        form on every report - that's how we make the next version better.
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

      <h3>What we logs (for future improvement) </h3>
      <ul>
        <li>Which pipeline steps ran, when, on which model.</li>
        <li>Token counts, costs, and step latency.</li>
        <li>SHA-256 hashes of your inputs (so we can dedupe identical papers).</li>
        <li>Whether each step succeeded or failed.</li>
      </ul>

      <h3>Your rights</h3>
      <ul>
        <li>
          Export every record we have about a run with one click in the
          summary view.
        </li>
      </ul>

      <div className="actions">
        <button type="button" onClick={handleAccept}>
          I understand - let me use the tool
        </button>
      </div>
    </section>
  )
}