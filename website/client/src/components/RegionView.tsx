interface Props {
  regionYaml: string
  scaffoldYaml: string
  selectedTemplates: string[]
  webSearchUsed: boolean
  runId: string
  slug: string
  onStartOver: () => void
  onChangeKey: () => void
  onScore: () => void
}

/**
 * Displays the region YAML produced by Step 4 + 5. Shows the final
 * (web-search-enriched) version with a toggle to view the scaffold
 * (pre-search) for transparency. Both rendered as preformatted text.
 */
import { useState } from 'react'

type Tab = 'final' | 'scaffold'

export function RegionView({
  regionYaml,
  scaffoldYaml,
  selectedTemplates,
  webSearchUsed,
  runId,
  slug,
  onStartOver,
  onChangeKey,
  onScore,
}: Props) {
  const [tab, setTab] = useState<Tab>('final')

  function downloadAs(content: string, filename: string): void {
    const blob = new Blob([content], { type: 'application/yaml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  function handleDownload(): void {
    if (tab === 'final') {
      downloadAs(regionYaml, `region_${slug || runId}.yaml`)
    } else {
      downloadAs(scaffoldYaml, `region_scaffold_${slug || runId}.yaml`)
    }
  }

  return (
    <section className="summary">
      <h2>Region context built</h2>
      <p className="help">
        Step 4 produced a region YAML scoped to your deployment using{' '}
        {selectedTemplates.length === 0
          ? 'no templates'
          : selectedTemplates.join(' and ')}{' '}
        as starting point
        {selectedTemplates.length === 1 ? '' : 's'}.
        {webSearchUsed
          ? ' Step 5 enriched it with web search to resolve [NEEDS VERIFICATION] tags.'
          : ' Web search was skipped; the scaffold is the final output.'}
      </p>

      {webSearchUsed && (
        <div className="tab-bar" role="tablist">
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'final'}
            className={tab === 'final' ? 'tab active' : 'tab'}
            onClick={() => setTab('final')}
          >
            Final (enriched)
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'scaffold'}
            className={tab === 'scaffold' ? 'tab active' : 'tab'}
            onClick={() => setTab('scaffold')}
          >
            Scaffold (pre-search)
          </button>
        </div>
      )}

      <div className="output-doc" role="tabpanel">
        <div className="output-doc-bar">
          <span className="output-doc-name">
            {tab === 'final' || !webSearchUsed
              ? 'region.yaml'
              : 'region_scaffold.yaml'}
          </span>
        </div>
        <pre className="summary-text">
          {tab === 'final' || !webSearchUsed ? regionYaml : scaffoldYaml}
        </pre>
      </div>

      <dl className="run-meta">
        <dt>Slug</dt>
        <dd>
          <code>{slug}</code>
        </dd>
        <dt>Run ID</dt>
        <dd>
          <code>{runId}</code>
        </dd>
        {selectedTemplates.length > 0 && (
          <>
            <dt>Templates</dt>
            <dd>{selectedTemplates.join(', ')}</dd>
          </>
        )}
      </dl>

      <div className="actions">
        <button type="button" className="link" onClick={onChangeKey}>
          Change key
        </button>
        <button type="button" className="link" onClick={handleDownload}>
          Download .yaml
        </button>
        <button type="button" onClick={onStartOver}>
          Run another
        </button>
        <button type="button" onClick={onScore}>
          Preview scoring prompt →
        </button>
      </div>
    </section>
  )
}
