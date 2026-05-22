interface Props {
  composedPrompt: string
  runId: string
  slug: string
  onBack: () => void
  onScore: () => void
  onChangeKey: () => void
}

/**
 * Step 6 inspection view: shows the assembled Opus user message for the
 * user to review before authorizing the Opus call. Step-by-step mode
 * only — auto mode bypasses this screen.
 */
export function ComposedPromptView({
  composedPrompt,
  runId,
  slug,
  onBack,
  onScore,
  onChangeKey,
}: Props) {
  function handleDownload(): void {
    const blob = new Blob([composedPrompt], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `composed_prompt_${slug || runId}.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  const charCount = composedPrompt.length
  const approxTokens = Math.round(charCount / 4)

  return (
    <section className="summary">
      <h2>Review the scoring prompt</h2>
      <p className="help">
        This is the exact message that will be sent to Claude Opus for
        the validity scoring. It bundles the framework, your benchmark
        YAML, the regional context, your elicitation answers, and any
        dataset analysis findings. Opus's reply (the 6-dimension scores)
        is conditioned on everything below — review it before authorizing
        the call. Opus is the only paid step that hasn't run yet.
      </p>

      <dl className="run-meta">
        <dt>Length</dt>
        <dd>
          {charCount.toLocaleString()} characters (~
          {approxTokens.toLocaleString()} tokens)
        </dd>
        <dt>Slug</dt>
        <dd>
          <code>{slug}</code>
        </dd>
        <dt>Run ID</dt>
        <dd>
          <code>{runId}</code>
        </dd>
      </dl>

      <div className="output-doc" role="region">
        <div className="output-doc-bar">
          <span className="output-doc-name">scoring_prompt.txt</span>
        </div>
        <pre className="summary-text composed-prompt">{composedPrompt}</pre>
      </div>

      <div className="actions">
        <button type="button" className="link" onClick={onChangeKey}>
          Change key
        </button>
        <button type="button" className="link" onClick={handleDownload}>
          Download .md
        </button>
        <button type="button" className="link" onClick={onBack}>
          ← Back to region
        </button>
        <button type="button" onClick={onScore}>
          Send to Opus (score) →
        </button>
      </div>
    </section>
  )
}
