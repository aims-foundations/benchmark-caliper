import { useState } from 'react'

interface DimensionScore {
  score?: number
  reasoning?: string
  evidence_quotes?: string[]
  evidence_region_sources?: unknown[]
  [key: string]: unknown
}

interface Props {
  scoring: Record<string, unknown>
  rawText: string
  runId: string
  slug: string
  onStartOver: () => void
  onChangeKey: () => void
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
export function ScoringView({
  scoring,
  rawText,
  runId,
  slug,
  onStartOver,
  onChangeKey,
}: Props) {
  const [tab, setTab] = useState<Tab>('table')

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

  const dimensions = DIMENSION_ORDER.filter((k) => scoring[k] !== undefined)
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
                const dim = scoring[key] as DimensionScore
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
                      {dim.reasoning && (
                        <p className="score-reasoning">{dim.reasoning}</p>
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
        <button type="button" className="link" onClick={onChangeKey}>
          Change key
        </button>
        <button type="button" className="link" onClick={handleDownload}>
          Download {tab === 'table' ? '.json' : '.txt'}
        </button>
        <button type="button" onClick={onStartOver}>
          Run another
        </button>
      </div>
    </section>
  )
}
