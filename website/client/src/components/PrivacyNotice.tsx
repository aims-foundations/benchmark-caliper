interface Props {
  onClose: () => void
}

/**
 * Stand-alone privacy notice reachable from the footer at any time.
 *
 * Mirrors the copy from the first-visit ConsentGate but stays available
 * after the user has acknowledged. SECURITY.md item 6.1 ("privacy
 * policy is live and matches actual practice") points here.
 */
export function PrivacyNotice({ onClose }: Props) {
  return (
    <section className="consent-gate" aria-labelledby="privacy-heading">
      <h2 id="privacy-heading">Privacy notice</h2>
      <p>
        This page describes what the validity-analyzer website does and does
        not log. Every claim here corresponds to a verifiable item in our
        public <code>SECURITY.md</code> checklist.
      </p>

      <h3>Your Anthropic API key</h3>
      <ul>
        <li>Stored on your device only (your browser's session/local storage).</li>
        <li>
          Sent to our backend in an <code>X-Anthropic-Key</code> HTTP header
          on each request. For step-by-step mode it is discarded from
          server memory the moment the request finishes; for auto mode
          (where the pipeline keeps running after you close the tab) it is
          held in process memory for the run's duration, typically 3–7
          minutes, and dropped when the run ends.
        </li>
        <li>
          Never written to any log, database, or filesystem on our servers.
          Never put in a URL, a cookie, or a response body.
        </li>
        <li>
          You can revoke it at any time from{' '}
          <a
            href="https://console.anthropic.com/"
            target="_blank"
            rel="noreferrer noopener"
          >
            console.anthropic.com
          </a>
          .
        </li>
      </ul>

      <h3>Your email address (auto mode)</h3>
      <ul>
        <li>
          Collected only when you ask us to email the report at the end of
          a run. You can leave the field blank to skip this.
        </li>
        <li>
          Stored on the run's row in our database (operational metadata),
          alongside a timestamp of when the email was sent.
        </li>
        <li>
          Used once: to send a single "your report is ready" message via
          our transactional-email provider (Resend). We never use it for
          marketing, never share it, and never combine it with data from
          other runs.
        </li>
        <li>
          Removed permanently when you delete the run via the Delete
          button on the report page.
        </li>
      </ul>

      <h3>What we always log</h3>
      <ul>
        <li>Run identifier (a random UUID), step name, model, timestamps.</li>
        <li>Token counts, computed cost in USD, step latency.</li>
        <li>SHA-256 hashes of your inputs (so identical papers can be deduplicated).</li>
        <li>Whether each step succeeded or failed, plus the exception class on failure.</li>
      </ul>
      <p className="help">
        These tier-1 and tier-2 records contain no personal identifiers and
        do not include your prompts or the model's responses. We keep them
        indefinitely so we can analyse cost and reliability over time.
      </p>

      <h3>What we log only with your explicit per-run opt-in</h3>
      <ul>
        <li>The full text of your deployment description.</li>
        <li>Your elicitation answers.</li>
        <li>The prompts we send to Anthropic and the responses they return.</li>
      </ul>
      <p className="help">
        The default for this is <strong>off</strong>. When you opt in, this
        content is held for 90 days and then auto-deleted by a daily
        retention job. Aggregated cost and error statistics derived from it
        do not identify your run and persist after the deletion.
      </p>

      <h3>Your rights</h3>
      <ul>
        <li>
          <strong>Export:</strong> from any run's summary or scoring view,
          download every record we have for that run as JSON.
        </li>
        <li>
          <strong>Delete:</strong> from the same view, hard-delete every
          record permanently. After this, the run no longer exists in our
          system; only aggregate cost statistics that don't identify it
          remain.
        </li>
        <li>
          <strong>Withdraw consent:</strong> clearing your browser's site
          data resets the consent acknowledgment so you'll see the
          first-visit notice again.
        </li>
      </ul>

      <h3>What we do not do</h3>
      <ul>
        <li>We do not run third-party analytics, advertising, or tracking on this site.</li>
        <li>We do not sell, rent, or share your data with anyone.</li>
        <li>
          We do not use your prompts or responses to train any model — they
          go to Anthropic via your key under their terms, and we keep our
          own copy only when you opt in for debugging purposes.
        </li>
      </ul>

      <h3>Hosting and security</h3>
      <p>
        TLS is enforced for all connections. Strict Content-Security-Policy
        and frame-ancestors headers are applied to every response. The full
        list of verifiable security commitments is in our public{' '}
        <code>SECURITY.md</code>.
      </p>

      <h3>Contact</h3>
      <p>
        Email <code>koyejolab@gmail.com</code> to report a vulnerability or
        request data deletion outside the in-app flow. We aim to confirm
        receipt within a few business days.
      </p>

      <div className="actions">
        <button type="button" onClick={onClose}>
          Close
        </button>
      </div>
    </section>
  )
}
