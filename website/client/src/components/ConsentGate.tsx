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
        This workflow uses your Anthropic API key for the benchmark assessment
        and your OpenAI API key for the required item analysis. You connect a
        matching dataset after the benchmark assessment: we search the
        Measurement Data Bank, then you confirm the benchmark and snapshot.
        You can also search for another match or upload the benchmark’s items.
        Each stage has an explicit action to start
        its paid model calls.
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

      <h3>Your API keys</h3>
      <ul>
        <li>Your Anthropic key is saved in your browser; your OpenAI key stays in the page's memory.</li>
        <li>
          Keys are sent to our backend in request headers and held in server
          memory while needed for model calls. They are never written to
          server logs, databases, or files.
        </li>
        <li>You can revoke either key at any time with its provider.</li>
      </ul>

      <h3>What we log (for future improvement)</h3>
      <ul>
        <li>Which pipeline steps ran, when, on which model.</li>
        <li>Token counts, costs, and step latency.</li>
        <li>SHA-256 hashes of your inputs (so we can dedupe identical papers).</li>
        <li>Whether each step succeeded or failed.</li>
      </ul>

      <p>
        The item-analysis stage sends assessment context and items to OpenAI.
        Its criteria and results are saved privately so you can pause and return
        later, with no automatic expiry by default. This browser keeps a run
        access token, but never your OpenAI key, for returning to saved results.
        You can download the complete results package or delete the saved run.
      </p>

      <h3>Your rights</h3>
      <ul>
        <li>
          Download the benchmark report and scoring JSON, and save the complete
          item-analysis results package for later review or sharing.
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
