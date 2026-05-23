import { DEMO_DEPLOYMENT_DESCRIPTION } from '../demo/fixture'

interface Props {
  onStart: () => void
  onExit: () => void
}

/**
 * Demo-mode replacement for the RunForm. Shows the very first step of the
 * pipeline — the upload / describe screen — but with every field already
 * populated from the cached MathDial / India urban tutoring assessment.
 * The user clicks "Run the demo" to begin the scripted replay.
 *
 * Visually it reuses .run-form / .hf-details classes so it sits in the
 * same panel layout as the real form.
 */
export function DemoIntro({ onStart, onExit }: Props) {
  return (
    <form
      className="run-form"
      onSubmit={(e) => {
        e.preventDefault()
        onStart()
      }}
    >
      <h2>Describe your deployment</h2>
      <p className="help">
        This is a <strong>demo run</strong>. Every field below is pre-filled
        with the actual inputs that produced our cached MathDial / India
        urban tutoring assessment. Click <em>Run the demo</em> to watch the
        pipeline replay end-to-end — no Anthropic key required, no API
        calls made.
      </p>

      <label>
        <span className="label-text">Benchmark paper (PDF)</span>
        <div className="demo-file-display" aria-readonly="true">
          <span className="demo-file-name">mathdial_2305.14536.pdf</span>
          <span className="demo-file-meta">cached example · 19 pages</span>
        </div>
      </label>

      <label>
        <span className="label-text">Deployment description</span>
        <textarea
          rows={6}
          readOnly
          value={DEMO_DEPLOYMENT_DESCRIPTION}
        />
      </label>

      <fieldset className="hf-details">
        <legend>
          <strong>HuggingFace dataset for this benchmark</strong>
        </legend>
        <p className="help">
          When provided, the pipeline profiles the actual dataset (Step 5b)
          and folds those findings into the scoring.
        </p>
        <label>
          <span className="label-text">HF dataset ID (e.g. org/dataset)</span>
          <input
            type="text"
            readOnly
            value="eth-nlped/mathdial"
            autoComplete="off"
            spellCheck={false}
          />
        </label>
        <label>
          <span className="label-text">HF config</span>
          <input
            type="text"
            readOnly
            value="(default)"
            autoComplete="off"
            spellCheck={false}
          />
        </label>
      </fieldset>

      <div className="actions">
        <button type="button" className="link" onClick={onExit}>
          Exit demo
        </button>
        <button type="submit">Run the demo →</button>
      </div>
    </form>
  )
}
