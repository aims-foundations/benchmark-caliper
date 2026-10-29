import { useEffect, useRef, useState } from 'react'
import { appPath } from '../paths'
import { SourceValue } from './Criteria'
import { DimensionAverages, ItemJudgments, SummaryFindings, matchesItemFilter, type ItemFilter } from './Results'
import { SharedScoringContext } from './SixScoreWorkflow'
import type { AnalysisRun, AnalysisSummary, Item, Specification } from './types'
import './itemAnalysis.css'
import './SavedItemAnalysis.css'

export type SavedItemAnalysisSnapshot = {
  items: Item[]
  spec: Specification
  summary: AnalysisSummary
  manifest: {
    run_id: string
    deployment: string
    updated_at?: string
    exported_at?: string
    model?: string | { model_id?: string; model?: string; reasoning_effort?: string }
  }
  dataset: { seed?: number; source?: Record<string, unknown> }
  originalAssessment: { scoring: Record<string, unknown> }
}

const PAGE_SIZE = 20

function SavedResults({ data, assessmentId, onRunOwnAnalysis }: {
  data: SavedItemAnalysisSnapshot; assessmentId: string; onRunOwnAnalysis: () => void
}) {
  const [page, setPage] = useState(1)
  const [filter, setFilter] = useState<ItemFilter>({ kind: 'all' })
  const itemsRef = useRef<HTMLDivElement>(null)
  const items = data.items.filter(item => item.status === 'complete')
  const count = items.length
  const matches = items.filter(item => matchesItemFilter(item, filter, data.spec.classifiers))
  const model = typeof data.manifest.model === 'string' ? data.manifest.model : data.manifest.model?.model_id || data.manifest.model?.model
  const selected = data.summary.experiment?.selected_items ?? count
  const sampleComplete = count === selected
  const run: AnalysisRun = {
    analysis_type: 'six_scores', run_id: data.manifest.run_id,
    status: sampleComplete ? 'checkpoint' : 'cancelled', scope: 'pilot',
    message: `Saved analysis of ${count} evaluated items`,
    assessment: { kind: 'gallery', id: assessmentId, benchmark: data.spec.benchmark, deployment: data.manifest.deployment },
    example: {
      id: assessmentId, title: data.spec.benchmark, benchmark: data.spec.benchmark,
      deployment: data.manifest.deployment, item_count: data.summary.total_items,
      description: 'Published item analysis', source_label: 'Saved dataset snapshot', available: true,
    },
    spec: data.spec, summary: data.summary,
    total: data.summary.total_items, complete: count, processed: count, errors: data.summary.error_items,
    items: items.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE),
    pagination: { page, total_pages: Math.max(1, Math.ceil(count / PAGE_SIZE)), page_size: PAGE_SIZE },
    usage: { input_tokens: 0, output_tokens: 0 }, can_continue: false,
  }
  const artifactPath = (artifact: 'spec' | 'items' | 'summary' | 'report' | 'package') => appPath(`/api/gallery/${encodeURIComponent(assessmentId)}/item-analysis/artifacts/${artifact}`)

  function changeFilter(next: ItemFilter) { setFilter(next); setPage(1) }
  function inspectDistribution(next: ItemFilter) {
    changeFilter(next)
    requestAnimationFrame(() => {
      itemsRef.current?.focus({ preventScroll: true })
      itemsRef.current?.scrollIntoView?.({ block: 'start' })
    })
  }

  return <>
    <div className="saved-ia-heading"><div><p className="ia-eyebrow">Item-level analysis</p><h2 id="saved-items-title">Saved item analysis</h2></div>
      <span className="ia-tag">{sampleComplete ? `${count.toLocaleString()}-item sample complete` : `${count.toLocaleString()} evaluated items`}</span>
    </div>
    <details className="saved-ia-context"><summary>Analysis details and scoring context</summary>
      <dl className="saved-ia-metadata">
        <div><dt>Model</dt><dd>{model || 'Not recorded'}</dd></div>
        <div><dt>Scoring rubric</dt><dd>{data.spec.rubric_version || 'Not recorded'}</dd></div>
        <div><dt>Sampling seed</dt><dd>{data.dataset.seed ?? 'Not recorded'}</dd></div>
        <div><dt>Run identifier</dt><dd>{data.manifest.run_id}</dd></div>
      </dl>
      <details><summary>Dataset source and revision</summary><SourceValue value={data.dataset.source} /></details>
      <SharedScoringContext spec={data.spec} />
    </details>
    <div ref={itemsRef} className="saved-ia-items" tabIndex={-1}>
      <ItemJudgments run={run} page={page} setPage={setPage} pageLoading={false} filter={filter} onFilterChange={changeFilter} filteredItems={matches} />
    </div>
    <details className="ia-original" id="score-distributions"><summary>Score distributions and original benchmark assessment</summary>
      <SummaryFindings run={run} onInspect={inspectDistribution} />
    </details>
    <DimensionAverages run={run} />
    <section className="ia-exports saved-ia-exports" aria-label="Save and share results">
      <h3>Save and share results</h3>
      <p className="ia-small">Keep a copy of the saved analysis. The complete package preserves the original export, including dataset provenance and the full prepared snapshot.</p>
      <div className="ia-primary-exports">
        <a className="ia-primary" href={artifactPath('report')} target="_blank" rel="noreferrer">View exported report <span aria-hidden="true">↗</span></a>
        <a className="ia-secondary" href={artifactPath('package')} download>Download complete results package <span aria-hidden="true">↓</span></a>
      </div>
      <p className="ia-small">This gallery view and the evaluated-item CSV show only the {count.toLocaleString()} evaluated items. The complete package includes all {data.summary.total_items.toLocaleString()} prepared items.</p>
      <details className="ia-individual-files"><summary>Individual files</summary><div>
        <a href={artifactPath('items')} download>Evaluated item scores CSV <span aria-hidden="true">↓</span></a>
        <a href={artifactPath('summary')} download>Summary JSON <span aria-hidden="true">↓</span></a>
        <a href={artifactPath('spec')} download>Shared context JSON <span aria-hidden="true">↓</span></a>
        <a href={artifactPath('report')} download>Original HTML report <span aria-hidden="true">↓</span></a>
      </div></details>
    </section>
    <section className="saved-ia-own-analysis">
      <div><h3>Run your own item analysis</h3><p className="ia-small">Analyze items using this assessment’s deployment context in your own run.</p></div>
      <button type="button" className="ia-secondary" onClick={onRunOwnAnalysis}>Run your own analysis</button>
    </section>
  </>
}

export function SavedItemAnalysis({ assessmentId, onRunOwnAnalysis }: { assessmentId: string; onRunOwnAnalysis: () => void }) {
  const [loaded, setLoaded] = useState<{ assessmentId: string; data: SavedItemAnalysisSnapshot } | null>(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const data = loaded?.assessmentId === assessmentId ? loaded.data : null

  useEffect(() => {
    const controller = new AbortController()
    setLoaded(null)
    setError('')
    fetch(appPath(`/api/gallery/${encodeURIComponent(assessmentId)}/item-analysis`), { signal: controller.signal })
      .then(response => {
        if (!response.ok) throw new Error(`Could not load the saved item analysis (${response.status}).`)
        return response.json() as Promise<SavedItemAnalysisSnapshot>
      })
      .then(snapshot => {
        if (!Array.isArray(snapshot.items) || !snapshot.spec?.classifiers || !snapshot.summary?.classifiers || !snapshot.manifest || !snapshot.dataset) {
          throw new Error('The saved item analysis is missing required results.')
        }
        if (!controller.signal.aborted) setLoaded({ assessmentId, data: snapshot })
      })
      .catch(reason => {
        if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : 'Could not load the saved item analysis.')
      })
    return () => controller.abort()
  }, [assessmentId, attempt])

  return <section id="item-analysis-stage" className="item-analysis-site saved-item-analysis" aria-labelledby="saved-items-title">
    {data ? <SavedResults key={assessmentId} data={data} assessmentId={assessmentId} onRunOwnAnalysis={onRunOwnAnalysis} /> : <>
      <h2 id="saved-items-title">Saved item analysis</h2>
      {error ? <div role="alert"><p>{error}</p><button type="button" className="ia-secondary" onClick={() => setAttempt(value => value + 1)}>Retry loading saved analysis</button></div>
        : <p role="status">Loading saved item analysis…</p>}
    </>}
  </section>
}
