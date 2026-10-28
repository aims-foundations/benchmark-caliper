import { useEffect, useMemo, useState } from 'react'
import { DEMO_ITEM_STORAGE_KEY, resetDemoItemProgress } from '../demo/session'
import { DEMO_ITEM_ANALYSIS_PILOT_SIZE, DEMO_ITEM_ANALYSIS_PROVENANCE } from '../demo/itemAnalysisFixture'
import { buildSixScoreDemoRun, DEMO_SIX_SCORE_SPEC } from '../demo/sixScoreItemFixture'
import { SharedScoringContext, SixScoreNavigation } from './SixScoreWorkflow'
import { ItemJudgments, ResultExports, SummaryFindings, type ItemFilter } from './Results'
import { buildDemoExport } from './demoExports'
import { saveBlob, viewReport } from './downloads'
import type { Artifact } from './types'
import './itemAnalysis.css'
import './DemoItemAnalysis.css'

type Stage = 'identify' | 'ready' | 'pilot' | 'complete'
function restoreStage(): Stage {
  try { const saved = JSON.parse(sessionStorage.getItem(DEMO_ITEM_STORAGE_KEY) || 'null'); if (saved?.version === 2 && ['identify', 'ready', 'pilot', 'complete'].includes(saved.stage)) return saved.stage } catch { /* Start a fresh walkthrough. */ }
  return 'identify'
}
export function DemoItemAnalysis({ onStatusChange }: { onStatusChange?: (status: 'pending' | 'in_progress' | 'complete') => void }) {
  const [stage, setStage] = useState<Stage>(restoreStage)
  const [viewed, setViewed] = useState<number | null>(null)
  const [page, setPage] = useState(1)
  const [filter, setFilter] = useState<ItemFilter>({ kind: 'all' })
  const [error, setError] = useState('')
  const run = useMemo(() => buildSixScoreDemoRun(stage === 'complete' ? 'sample' : 'pilot'), [stage])
  const showing = stage === 'pilot' || stage === 'complete'
  const source = DEMO_ITEM_ANALYSIS_PROVENANCE
  const current = viewed ?? (stage === 'identify' ? 1 : stage === 'ready' ? 2 : 3)
  useEffect(() => {
    try { sessionStorage.setItem(DEMO_ITEM_STORAGE_KEY, JSON.stringify({ version: 2, stage })) } catch { /* Keep progress in memory. */ }
    onStatusChange?.(stage === 'complete' ? 'complete' : stage === 'identify' ? 'pending' : 'in_progress')
  }, [stage, onStatusChange])
  function advance(next: Stage) { setStage(next); setViewed(null); setPage(1); setFilter({ kind: 'all' }) }
  function navigate(step: number) {
    setViewed(step)
    requestAnimationFrame(() => { const section = document.getElementById(`ia-score-step-${step}`); section?.focus({ preventScroll: true }); section?.scrollIntoView?.({ block: 'start' }) })
  }
  function download(artifact: Artifact) {
    try { const result = buildDemoExport(artifact, showing ? run : { ...run, status: 'ready', scope: null, complete: 0, processed: 0 }); saveBlob(new Blob([result.content], { type: result.mimeType }), result.filename); setError('') }
    catch { setError('The demo export could not be downloaded. Please try again.') }
  }
  async function report() {
    try { const result = buildDemoExport('report', run); await viewReport(async () => new Blob([result.content], { type: result.mimeType })); setError('') }
    catch { setError('The demo report could not be opened. Please try again.') }
  }
  return <div className="item-analysis-site ia-embedded ia-demo" aria-label="Free MathDial item analysis demo">
    <div className="ia-demo-intro"><div><p className="ia-eyebrow">MathDial walkthrough · item analysis</p><h2>Six scores for every item</h2>
      <p>This free demo uses {run.total} public MathDial examples and authored illustrative scores. No API key or model calls are needed.</p></div>
      <button className="ia-text-button" onClick={() => { resetDemoItemProgress(); advance('identify'); setError('') }}>Restart item demo</button></div>
    <SixScoreNavigation current={current} onNavigate={navigate} />
    <section id="ia-score-step-1" className="ia-stage" tabIndex={-1} aria-labelledby="demo-context-title"><h2 id="demo-context-title">1. Context &amp; items</h2>
      <p><strong>MathDial</strong> · {run.total} bundled dialogues from {source.source_split_count} published test dialogues.</p><p>{source.sample_description}</p>
      <p>Deployment: one-on-one tutoring for English-fluent professional teachers in Indian metropolitan cities.</p>
      <a href={source.source_url} target="_blank" rel="noreferrer">View the pinned MathDial source ↗</a>
      <p className="ia-demo-disclosure"><strong>Authored illustrative scores.</strong> {source.label_provenance}</p>
      <details className="ia-original"><summary>Source provenance and attribution</summary><p>{source.citation}</p><p>{source.student_provenance}</p><p>{source.changes}</p><p>Revision: {source.revision}</p><a href={source.license_url}>{source.license}</a></details>
      {stage === 'identify' ? <button className="ia-primary" onClick={() => advance('ready')}>Confirm benchmark and prepare context</button> : <SharedScoringContext spec={DEMO_SIX_SCORE_SPEC} />}
    </section>
    <section id="ia-score-step-2" className="ia-stage" tabIndex={-1} aria-labelledby="demo-analyze-title"><h2 id="demo-analyze-title">2. Analyze</h2>
      <p>A live analysis uses one model call per item to return all six assessments together. This walkthrough reveals bundled examples.</p>
      {stage === 'identify' ? <p>Confirm the context and items first.</p> : <div className="ia-actions">
        {!showing && <button className="ia-secondary" onClick={() => advance('pilot')}>Show first {DEMO_ITEM_ANALYSIS_PILOT_SIZE} items</button>}
        {stage !== 'complete' && <button className="ia-primary" onClick={() => advance('complete')}>{stage === 'pilot' ? 'Show remaining examples' : `Show all ${run.total} items`}</button>}
        {stage === 'complete' && <p>All {run.total} bundled examples are available.</p>}
      </div>}
    </section>
    <section id="ia-score-step-3" className="ia-stage" tabIndex={-1} aria-labelledby="demo-results-title"><h2 id="demo-results-title">3. Results</h2>
      {showing ? <><p role="status">{run.complete} of {run.total} bundled items shown. These scores illustrate the workflow; they are not model outputs or findings about the full MathDial benchmark.</p>
        <ItemJudgments run={run} page={page} setPage={setPage} pageLoading={false} demo filter={filter} onFilterChange={value => { setFilter(value); setPage(1) }} />
        <details className="ia-original"><summary>Illustrative score distributions and original benchmark assessment</summary><SummaryFindings run={run} demo onInspect={value => { setFilter(value); setPage(1); navigate(3) }} /></details>
        <ResultExports run={run} onDownload={download} onViewReport={() => void report()} downloading={null} demo />
      </> : <><p>Six scores per item will appear here. Select a score to read the explanation, evidence, and missing information.</p>{stage === 'ready' && <button className="ia-secondary" onClick={() => download('spec')}>Download demo context JSON</button>}</>}
      {error && <p className="ia-error" role="alert">{error}</p>}
    </section>
  </div>
}
