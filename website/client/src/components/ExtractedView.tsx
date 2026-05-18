import { useState } from 'react'

interface Props {
  paperSummary: string
  benchmarkYaml: string
  pageCount: number
  selectedExamples: string[]
  runId: string
  slug: string
  onStartOver: () => void
  onChangeKey: () => void
  onGenerateRegion: () => void
}

type Tab = 'summary' | 'yaml'

/**
 * Displays Step 3a's consolidated paper summary and Step 3b's synthesized
 * benchmark YAML side-by-side via a tab switch. Both are rendered as
 * preformatted text — model output is never run through an HTML
 * renderer per SECURITY.md.
 */
export function ExtractedView({
  paperSummary,
  benchmarkYaml,
  pageCount,
  selectedExamples,
  runId,
  slug,
  onStartOver,
  onChangeKey,
  onGenerateRegion,
}: Props) {
  const [tab, setTab] = useState<Tab>('summary')

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
    if (tab === 'summary') {
      downloadAs(
        paperSummary,
        `paper_summary_${slug || runId}.md`,
        'text/markdown',
      )
    } else {
      downloadAs(
        benchmarkYaml,
        `benchmark_${slug || runId}.yaml`,
        'application/yaml',
      )
    }
  }

  return (
    <section className="summary">
      <h2>Paper analyzed</h2>
      <p className="help">
        Step 3a produced a consolidated paper summary; Step 3b synthesized a
        per-paper benchmark YAML using {selectedExamples.length === 0
          ? 'no'
          : selectedExamples.join(' and ')}{' '}
        as reference{selectedExamples.length === 1 ? '' : 's'}. Downstream
        steps (region YAML, web search, scoring) will consume the YAML.
      </p>

      <div className="tab-bar" role="tablist">
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'summary'}
          className={tab === 'summary' ? 'tab active' : 'tab'}
          onClick={() => setTab('summary')}
        >
          Paper summary
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'yaml'}
          className={tab === 'yaml' ? 'tab active' : 'tab'}
          onClick={() => setTab('yaml')}
        >
          Benchmark YAML
        </button>
      </div>

      <pre className="summary-text" role="tabpanel">
        {tab === 'summary' ? paperSummary : benchmarkYaml}
      </pre>

      <dl className="run-meta">
        <dt>Slug</dt>
        <dd>
          <code>{slug}</code>
        </dd>
        <dt>Run ID</dt>
        <dd>
          <code>{runId}</code>
        </dd>
        <dt>Pages</dt>
        <dd>{pageCount}</dd>
        {selectedExamples.length > 0 && (
          <>
            <dt>References</dt>
            <dd>{selectedExamples.join(', ')}</dd>
          </>
        )}
      </dl>

      <div className="actions">
        <button type="button" className="link" onClick={onChangeKey}>
          Change key
        </button>
        <button type="button" className="link" onClick={handleDownload}>
          Download {tab === 'summary' ? '.md' : '.yaml'}
        </button>
        <button type="button" onClick={onStartOver}>
          Run another
        </button>
        <button type="button" onClick={onGenerateRegion}>
          Build region context →
        </button>
      </div>
    </section>
  )
}
