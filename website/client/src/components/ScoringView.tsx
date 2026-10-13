import { useState, type FormEvent, type ReactNode } from 'react'
import {
  submitFeedback,
  ApiError,
  type FeedbackCategory,
} from '../api'
import { appPath } from '../paths'
import {
  calibrateConfidence,
  parsePriorityWeights,
  PRIORITY_LABEL,
  type Priority,
} from '../scoreInsights'

interface DimensionScore {
  score?: number
  // Opus's schema (opus_scoring_framing.md) uses `justification`; some
  // older test fixtures use `reasoning`. Accept both.
  justification?: string
  reasoning?: string
  evidence_quotes?: string[]
  evidence_web_sources?: string[]
  evidence_dataset?: string[]
  evidence_region_sources?: unknown[]
  confidence?: string
  strengths?: string[]
  [key: string]: unknown
}

// Render an evidence string, turning any bare URLs into clickable links so
// a reader can open a source and judge its quality (the Grokipedia lesson:
// the tool must show its sources inline).
const URL_RE = /(https?:\/\/[^\s)]+)/gi
function linkifyEvidence(text: string): ReactNode {
  const parts: ReactNode[] = []
  let lastIndex = 0
  let match: RegExpExecArray | null
  const re = new RegExp(URL_RE)
  while ((match = re.exec(text)) !== null) {
    const url = match[1]
    if (match.index > lastIndex) parts.push(text.slice(lastIndex, match.index))
    parts.push(
      <a key={match.index} href={url} target="_blank" rel="noreferrer noopener">
        {url}
      </a>,
    )
    lastIndex = match.index + url.length
  }
  if (lastIndex < text.length) parts.push(text.slice(lastIndex))
  return parts.length > 0 ? parts : text
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
  /**
   * The elicitation summary markdown, used to surface each dimension's
   * user-assigned priority weight beside its score. Optional — when absent
   * (e.g. some gallery entries) priority badges are simply omitted.
   */
  elicitationSummary?: string
  /** Report-email outcome from the run. Absent for the read-only gallery. */
  emailStatus?: {
    requested: boolean
    sent?: boolean
    fallback?: boolean
    error?: string | null
  }
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

const CONFIDENCE_LABEL: Record<string, string> = {
  high: 'High confidence',
  medium: 'Medium confidence',
  low: 'Low confidence',
}

// Short priority tag shown beside a dimension name.
const PRIORITY_TAG: Record<Priority, string> = {
  HIGH: 'High',
  MODERATE: 'Moderate',
  LOWER: 'Lower',
}

function PriorityBadge({ priority }: { priority: Priority }) {
  return (
    <span
      className="dim-priority"
      data-priority={priority}
      title={`${PRIORITY_LABEL[priority]} — assigned during elicitation`}
    >
      {PRIORITY_TAG[priority]} priority
    </span>
  )
}

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
  emailStatus,
  elicitationSummary,
}: Props) {
  const [tab, setTab] = useState<Tab>('table')
  const priorities = parsePriorityWeights(elicitationSummary)
  const hasPriorities = Object.keys(priorities).length > 0
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

      {emailStatus?.requested &&
        (emailStatus.sent && !emailStatus.fallback ? (
          <p className="email-status" role="status">
            📧 The report has been emailed to you, with Markdown and JSON
            copies attached.
          </p>
        ) : emailStatus.fallback ? (
          <p className="email-status warn" role="status">
            ✉️ Email delivery isn't configured on this deployment, so no
            email was sent. Use the <strong>Download</strong> buttons below
            to save the report.
          </p>
        ) : (
          <p className="email-status warn" role="status">
            ⚠️ We couldn't send the report email
            {emailStatus.error ? ` (${emailStatus.error})` : ''}. Use the{' '}
            <strong>Download</strong> buttons below to save the report.
          </p>
        ))}

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
          <p className="score-table-caveat">
            A structured opinion from Claude Opus, not a verdict — these
            scores can miss context. Read the reasoning, not just the number.
          </p>
          {!empty && hasPriorities && (
            <p className="priority-legend">
              The badge on each dimension is the priority you assigned during
              elicitation. A 5/5 on a <strong>Lower</strong>-priority
              dimension matters less than a low score on a{' '}
              <strong>High</strong>-priority one.
            </p>
          )}
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
                const priority = priorities[key]
                const conf = calibrateConfidence(dim)
                const webSources = Array.isArray(dim.evidence_web_sources)
                  ? dim.evidence_web_sources
                  : []
                const datasetEvidence = Array.isArray(dim.evidence_dataset)
                  ? dim.evidence_dataset
                  : []
                return (
                  <li
                    key={key}
                    className="score-row"
                    data-priority={priority ?? undefined}
                  >
                    <details>
                      <summary>
                        <span className="dim-name">
                          {DIMENSION_LABELS[key] ?? key}
                          {priority && <PriorityBadge priority={priority} />}
                        </span>
                        <span className="dim-tags">
                          <span
                            className="dim-confidence"
                            data-confidence={conf.calibrated}
                            title={
                              conf.downgraded
                                ? `Adjusted down from "${conf.reported}": only ${conf.streamCount} evidence ` +
                                  `stream${conf.streamCount === 1 ? '' : 's'} support this (high confidence needs at least two).`
                                : `${conf.streamCount} evidence stream${conf.streamCount === 1 ? '' : 's'} support this dimension.`
                            }
                          >
                            {CONFIDENCE_LABEL[conf.calibrated]}
                            {conf.downgraded && ' *'}
                          </span>
                          <span
                            className="dim-score"
                            data-score={dim.score ?? 0}
                          >
                            {dim.score ?? '?'} / 5
                          </span>
                        </span>
                      </summary>
                      {conf.downgraded && (
                        <p className="confidence-note">
                          Confidence shown as{' '}
                          <strong>{conf.calibrated}</strong>, adjusted down
                          from the model's <em>{conf.reported}</em>: this
                          dimension rests on {conf.streamCount} evidence
                          stream{conf.streamCount === 1 ? '' : 's'}, and the
                          framework reserves "high" for findings backed by at
                          least two.
                        </p>
                      )}
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
                            <h4>Paper quotes</h4>
                            <ul className="score-evidence">
                              {dim.evidence_quotes.map((q, i) => (
                                <li key={i}>{String(q)}</li>
                              ))}
                            </ul>
                          </>
                        )}
                      {webSources.length > 0 && (
                        <>
                          <h4>Web sources</h4>
                          <ul className="score-evidence">
                            {webSources.map((w, i) => (
                              <li key={i}>{linkifyEvidence(String(w))}</li>
                            ))}
                          </ul>
                        </>
                      )}
                      {datasetEvidence.length > 0 && (
                        <>
                          <h4>Dataset findings</h4>
                          <ul className="score-evidence">
                            {datasetEvidence.map((d, i) => (
                              <li key={i}>{String(d)}</li>
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
        <div className="output-doc" role="tabpanel">
          <div className="output-doc-bar">
            <span className="output-doc-name">scoring_raw_output.txt</span>
          </div>
          <pre className="summary-text">{rawText}</pre>
        </div>
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
          href={pdfUrl ?? appPath(`/api/runs/${runId}/review.pdf`)}
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
