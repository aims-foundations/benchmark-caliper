import { useState, type FormEvent } from 'react'
import {
  submitFeedback,
  ApiError,
  type FeedbackCategory,
} from '../api'

interface DimensionScore {
  score?: number
  // Opus's schema (opus_scoring_framing.md) uses `justification`; some
  // older test fixtures use `reasoning`. Accept both.
  justification?: string
  reasoning?: string
  evidence_quotes?: string[]
  evidence_region_sources?: unknown[]
  strengths?: string[]
  [key: string]: unknown
}

interface Props {
  scoring: Record<string, unknown>
  rawText: string
  runId: string
  slug: string
  onStartOver: () => void
  onChangeKey: () => void
  /** Override the review.pdf URL (curated gallery entries live elsewhere). */
  pdfUrl?: string
  /** Curated/read-only view: hides the feedback form and key controls. */
  readOnly?: boolean
}

const DIMENSION_LABELS: Record<string, string> = {
  input_ontology: 'Input Ontology (IO)',
  input_content: 'Input Content (IC)',
  input_form: 'Input Form (IF)',
  output_ontology: 'Output Ontology (OO)',
  output_content: 'Output Content (OC)',
  output_form: 'Output Form (OF)',
}

const DIMENSION_ORDER = [
  'input_ontology',
  'input_content',
  'input_form',
  'output_ontology',
  'output_content',
  'output_form',
]

type Tab = 'table' | 'raw'

/**
 * Renders the validity scoring report. Default view is a per-dimension
 * score table; "raw" tab shows the JSON for transparency. Both
 * downloadable.
 */
const FEEDBACK_CATEGORIES: Array<{ value: FeedbackCategory; label: string }> = [
  { value: 'incorrect_score', label: 'A score seems incorrect' },
  { value: 'hallucination', label: 'Output contains hallucinated content' },
  {
    value: 'evidence_mismatch',
    label: "Evidence/quotes don't match the paper",
  },
  { value: 'other', label: 'Other issue' },
]

export function ScoringView({
  scoring,
  rawText,
  runId,
  slug,
  onStartOver,
  onChangeKey,
  pdfUrl,
  readOnly = false,
}: Props) {
  const [tab, setTab] = useState<Tab>('table')
  const [feedbackOpen, setFeedbackOpen] = useState(false)
  const [feedbackCategory, setFeedbackCategory] =
    useState<FeedbackCategory>('incorrect_score')
  const [feedbackMessage, setFeedbackMessage] = useState('')
  const [feedbackEmail, setFeedbackEmail] = useState('')
  const [feedbackStatus, setFeedbackStatus] = useState<
    'idle' | 'sending' | 'sent' | 'error'
  >('idle')
  const [feedbackError, setFeedbackError] = useState('')

  async function handleFeedbackSubmit(
    e: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    e.preventDefault()
    const message = feedbackMessage.trim()
    if (!message) return
    setFeedbackStatus('sending')
    setFeedbackError('')
    try {
      await submitFeedback({
        runId,
        category: feedbackCategory,
        message,
        contactEmail: feedbackEmail.trim() || null,
      })
      setFeedbackStatus('sent')
      setFeedbackMessage('')
      setFeedbackEmail('')
    } catch (err) {
      setFeedbackStatus('error')
      setFeedbackError(
        err instanceof ApiError
          ? `Could not submit (${err.status}). Please try again.`
          : 'Could not submit feedback. Please try again.',
      )
    }
  }

  function downloadAs(content: string, filename: string, type: string): void {
    const blob = new Blob([content], { type })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  function handleDownload(): void {
    if (tab === 'table') {
      const formatted = JSON.stringify(scoring, null, 2)
      downloadAs(formatted, `scoring_${slug || runId}.json`, 'application/json')
    } else {
      downloadAs(rawText, `scoring_raw_${slug || runId}.txt`, 'text/plain')
    }
  }

  // Opus's schema nests dimensions under `dimensions`; older test fixtures
  // put them at the top level. Prefer nested, fall back to flat.
  const dimBag: Record<string, unknown> =
    scoring.dimensions && typeof scoring.dimensions === 'object'
      ? (scoring.dimensions as Record<string, unknown>)
      : scoring
  const dimensions = DIMENSION_ORDER.filter((k) => dimBag[k] !== undefined)
  const empty = dimensions.length === 0

  return (
    <section className="summary">
      <h2>Validity scoring</h2>
      <p className="help">
        Step 7's output: an Opus-scored validity assessment across the six
        dimensions, conditioned on your deployment context. Scores are 1–5;
        higher is better. Click a dimension to expand its reasoning.
      </p>

      <div className="tab-bar" role="tablist">
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'table'}
          className={tab === 'table' ? 'tab active' : 'tab'}
          onClick={() => setTab('table')}
        >
          Score table
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'raw'}
          className={tab === 'raw' ? 'tab active' : 'tab'}
          onClick={() => setTab('raw')}
        >
          Raw output
        </button>
      </div>

      {tab === 'table' && (
        <div className="score-table" role="tabpanel">
          {empty ? (
            <p className="inline-error">
              Opus output couldn't be parsed as a scoring object. Switch to
              "Raw output" to see what was returned.
            </p>
          ) : (
            <ol className="score-list">
              {dimensions.map((key) => {
                const dim = dimBag[key] as DimensionScore
                const reasoning = dim.justification ?? dim.reasoning
                return (
                  <li key={key} className="score-row">
                    <details>
                      <summary>
                        <span className="dim-name">
                          {DIMENSION_LABELS[key] ?? key}
                        </span>
                        <span
                          className="dim-score"
                          data-score={dim.score ?? 0}
                        >
                          {dim.score ?? '?'} / 5
                        </span>
                      </summary>
                      {reasoning && (
                        <p className="score-reasoning">{reasoning}</p>
                      )}
                      {Array.isArray(dim.strengths) &&
                        dim.strengths.length > 0 && (
                          <>
                            <h4>Strengths</h4>
                            <ul className="score-evidence">
                              {dim.strengths.map((s, i) => (
                                <li key={i}>{String(s)}</li>
                              ))}
                            </ul>
                          </>
                        )}
                      {Array.isArray(dim.evidence_quotes) &&
                        dim.evidence_quotes.length > 0 && (
                          <>
                            <h4>Evidence quotes</h4>
                            <ul className="score-evidence">
                              {dim.evidence_quotes.map((q, i) => (
                                <li key={i}>{String(q)}</li>
                              ))}
                            </ul>
                          </>
                        )}
                    </details>
                  </li>
                )
              })}
            </ol>
          )}
        </div>
      )}

      {tab === 'raw' && (
        <pre className="summary-text" role="tabpanel">
          {rawText}
        </pre>
      )}

      <dl className="run-meta">
        <dt>Slug</dt>
        <dd>
          <code>{slug}</code>
        </dd>
        <dt>Run ID</dt>
        <dd>
          <code>{runId}</code>
        </dd>
      </dl>

      <div className="actions">
        {!readOnly && (
          <button type="button" className="link" onClick={onChangeKey}>
            Change key
          </button>
        )}
        <button type="button" className="link" onClick={handleDownload}>
          Download {tab === 'table' ? '.json' : '.txt'}
        </button>
        <a
          className="link"
          href={pdfUrl ?? `/api/runs/${runId}/review.pdf`}
          download={`validity_report_${slug || runId}.pdf`}
          target="_blank"
          rel="noreferrer"
        >
          Download report PDF
        </a>
        <button type="button" onClick={onStartOver}>
          Run another
        </button>
      </div>

      <aside className="score-disclaimer">
        <strong>A note on these scores.</strong> This pipeline is still a
        work in progress, and we're improving it as we learn. Each score
        reflects Claude Opus's reading of the documents shared. It's
        a careful, structured opinion, but not the final word - the model can
        miss context or weigh things differently than you would. Please
        treat this report as a useful starting point for thinking through
        the benchmark's fit.
        {!readOnly &&
          " If something looks off, we'd love to hear about it through the form below - that's how we make the next version better."}
      </aside>

      {!readOnly && (
      <details
        className="feedback-section"
        open={feedbackOpen}
        onToggle={(e) =>
          setFeedbackOpen((e.target as HTMLDetailsElement).open)
        }
      >
        <summary>Report an issue with this assessment</summary>
        <p className="help">
          Spotted a wrong score, a hallucinated claim, or a quote that
          doesn't match the paper? Let us know. We use feedback to improve
          the pipeline. Your run ID is attached automatically.
        </p>
        {feedbackStatus === 'sent' ? (
          <p className="success-message">
            Thanks — we received your report.{' '}
            <button
              type="button"
              className="link"
              onClick={() => setFeedbackStatus('idle')}
            >
              Send another
            </button>
          </p>
        ) : (
          <form onSubmit={handleFeedbackSubmit} className="feedback-form">
            <label>
              What's the issue?
              <select
                value={feedbackCategory}
                onChange={(e) =>
                  setFeedbackCategory(e.target.value as FeedbackCategory)
                }
                disabled={feedbackStatus === 'sending'}
              >
                {FEEDBACK_CATEGORIES.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Details
              <textarea
                value={feedbackMessage}
                onChange={(e) => setFeedbackMessage(e.target.value)}
                rows={5}
                maxLength={5000}
                required
                placeholder="Which dimension or claim looks wrong? What were you expecting instead?"
                disabled={feedbackStatus === 'sending'}
              />
            </label>
            <label>
              Email (optional, so we can follow up)
              <input
                type="email"
                value={feedbackEmail}
                onChange={(e) => setFeedbackEmail(e.target.value)}
                placeholder="you@example.com"
                disabled={feedbackStatus === 'sending'}
              />
            </label>
            {feedbackStatus === 'error' && (
              <p className="inline-error">{feedbackError}</p>
            )}
            <button
              type="submit"
              disabled={
                feedbackStatus === 'sending' || !feedbackMessage.trim()
              }
            >
              {feedbackStatus === 'sending' ? 'Sending…' : 'Send report'}
            </button>
          </form>
        )}
      </details>
      )}
    </section>
  )
}
