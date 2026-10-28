import { useEffect, useState, type ReactNode } from 'react'
import { classifierName, SourceValue } from './Criteria'
import { DimensionAverages, ItemJudgments, ResultExports, SummaryFindings, type ItemFilter } from './Results'
import type { AnalysisRun, Artifact, Item, RunScope, Specification } from './types'

export const SIX_SCORE_STEPS = ['Context & items', 'Analyze', 'Results'] as const
export const isSixScoreRun = (run: AnalysisRun | null) => run?.analysis_type === 'six_scores' || run?.spec?.analysis_type === 'six_scores' || run?.spec?.schema_version === 'caliper_item_context_v1'

export function SharedScoringContext({ spec }: { spec: Specification }) {
  return <div className="ia-shared-context">
    <p>The same deployment context and fixed six-dimension rubric are used for every item. Earlier benchmark scores do not determine item scores.</p>
    <details className="ia-original"><summary>Shared context and sources</summary>
      <p><strong>Deployment:</strong> {spec.deployment_description || spec.deployment}</p>
      {Object.entries(spec.source_registry || {}).map(([id, value]) => <details key={id} className="ia-source-record"><summary>{id}</summary><SourceValue value={value} /></details>)}
      {spec.dataset_profile && <details><summary>Dataset profile</summary><SourceValue value={spec.dataset_profile} /></details>}
    </details>
    <details className="ia-original"><summary>Six-dimension scoring rubric</summary>
      <p>1 = fundamental mismatch · 2 = substantial mismatch · 3 = partial alignment · 4 = strong alignment with minor limitations · 5 = strong alignment supported by evidence.</p>
      <p>Unknown means the available evidence cannot support a score. It is separate from a processing failure or an item awaiting analysis.</p>
      {spec.classifiers.map(dimension => <details className="ia-source-record" key={dimension.id}><summary>{classifierName(dimension.id)}</summary>
        <p>{dimension.question}</p>{dimension.ordinal_anchors && <dl className="ia-anchors">{Object.entries(dimension.ordinal_anchors).map(([score, anchor]) => <div key={score}><dt>{score}</dt><dd>{anchor}</dd></div>)}</dl>}
      </details>)}
    </details>
  </div>
}

export function SixScoreNavigation({ current, onNavigate }: { current: number; onNavigate: (step: number) => void }) {
  return <nav className="ia-pipeline-navigation ia-three-steps" aria-label="Item analysis steps"><ol>{SIX_SCORE_STEPS.map((title, index) => <li key={title}>
    <a href={`#ia-score-step-${index + 1}`} aria-current={current === index + 1 ? 'step' : undefined} onClick={event => { event.preventDefault(); onNavigate(index + 1) }}>
      <span className="ia-step-number">{index + 1}</span><strong>{title}</strong>
    </a></li>)}</ol></nav>
}

export function SixScoreWorkflow({ run, context, canPrepare, onPrepare, onRestart, busy, starting, startDelayed, apiKey, onKeyChange, pilotSize, canAnalyze, onAnalyze, onStop,
  page, setPage, pageLoading, filter, onFilterChange, filteredItems, filterLoading, inspectionError, retryInspection,
  onDownload, onViewReport, onDownloadPackage, downloading, management, errors }: {
  run: AnalysisRun | null; context: ReactNode; canPrepare: boolean; onPrepare: () => void; onRestart: () => void; busy: boolean; starting: boolean; startDelayed?: boolean;
  apiKey: string; onKeyChange: (value: string) => void; pilotSize: number; canAnalyze: boolean; onAnalyze: (scope: RunScope) => void; onStop: () => void;
  page: number; setPage: (page: number) => void; pageLoading: boolean; filter: ItemFilter; onFilterChange: (filter: ItemFilter) => void;
  filteredItems?: Item[]; filterLoading: boolean; inspectionError: string; retryInspection: () => void;
  onDownload: (artifact: Artifact) => void; onViewReport: () => void; onDownloadPackage: () => void;
  downloading: Artifact | 'package' | 'view' | null; management: ReactNode; errors: ReactNode;
}) {
  const [viewedStep, setViewedStep] = useState<number | null>(null)
  const [scope, setScope] = useState<RunScope>('all')
  const active = !!run && ['preparing', 'generating', 'running'].includes(run.status)
  useEffect(() => { setViewedStep(null) }, [run?.status])
  useEffect(() => { if (run?.scope === 'all') setScope('all') }, [run?.scope])
  const current = viewedStep ?? (!run?.spec ? 1 : active || !run.processed ? 2 : 3)
  const selected = run?.scope === 'pilot' ? pilotSize : run?.total || 0
  const planned = scope === 'pilot' ? pilotSize : run?.total || 0
  const remaining = run?.remaining_requests?.[scope] ?? Math.ceil((run?.remaining_judgments?.[scope] ?? Math.max(0, planned - (run?.complete || 0)) * 6) / 6)
  function navigate(step: number) {
    setViewedStep(step)
    requestAnimationFrame(() => { const section = document.getElementById(`ia-score-step-${step}`); section?.focus({ preventScroll: true }); section?.scrollIntoView?.({ block: 'start' }) })
  }
  function inspect(next: ItemFilter) { onFilterChange(next); navigate(3) }
  return <>
    <SixScoreNavigation current={current} onNavigate={navigate} />
    {errors}
    <p className="ia-eyebrow">Current step {current} of 3</p>
    <section id="ia-score-step-1" className={`ia-stage${current === 1 ? ' ia-stage-current' : ''}`} tabIndex={-1} aria-labelledby="ia-score-context-title">
      <h2 id="ia-score-context-title">1. Context &amp; items</h2>
      <p>Confirm the deployment and dataset. Shared context is prepared once and reused for each item.</p>
      <details className="ia-stage-content" open={!run?.spec}><summary>{run?.spec ? 'Review confirmed context and items' : 'Choose context and items'}</summary>{context}</details>
      {!run && canPrepare && <form onSubmit={event => { event.preventDefault(); onPrepare() }}><button className="ia-primary" disabled={!canPrepare || busy}>{starting ? 'Preparing context…' : 'Prepare shared context'}</button><p className="ia-small">No API key or model call is needed to prepare context.</p></form>}
      {starting && <p role="status">{startDelayed ? 'Still waiting for the server to confirm this run. We’ll show progress here when it responds.' : 'Starting item analysis. Waiting for the server to confirm your run…'}</p>}
      {run && !run.spec && <p role="status">{run.failure?.message || run.error || run.message}</p>}
      {run && !run.spec && !active && <div className="ia-actions"><button type="button" className="ia-secondary" onClick={onRestart} disabled={busy}>Start a new analysis</button></div>}
      {run?.spec && <SharedScoringContext spec={run.spec} />}
    </section>
    <section id="ia-score-step-2" className={`ia-stage${current === 2 ? ' ia-stage-current' : ''}`} tabIndex={-1} aria-labelledby="ia-score-analyze-title">
      <h2 id="ia-score-analyze-title">2. Analyze</h2><p>One model call per item returns all six scores, with explanations, evidence, and missing information.</p>
      {!run?.spec && <p>Prepare the shared context to begin.</p>}
      {run?.spec && <>
        {active ? <><p role="status">{run.message}</p><progress max={selected || run.total} value={run.complete} aria-label="Item scoring progress" /><button className="ia-secondary" onClick={onStop} disabled={busy}>Stop analysis</button></>
          : run.processed > 0 && <p role="status">{run.complete} of {selected} selected items complete. {run.errors} needing retry. Completed items are saved.</p>}
        {run.status === 'failed' && <p role="alert" className="ia-error">{run.failure?.message || run.error || run.message}</p>}
        {canAnalyze && <form className="ia-classify-panel" onSubmit={event => { event.preventDefault(); onAnalyze(scope) }}>
          <div><fieldset className="ia-mode"><legend>Items to analyze</legend>
            <label><input type="radio" name="score-scope" checked={scope === 'all'} onChange={() => setScope('all')} /><span>All {run.total.toLocaleString()} items</span></label>
            <label><input type="radio" name="score-scope" disabled={run.scope === 'all'} checked={scope === 'pilot'} onChange={() => setScope('pilot')} /><span>First {pilotSize.toLocaleString()} items</span></label>
          </fieldset><p className="ia-small">{remaining.toLocaleString()} primary scoring {remaining === 1 ? 'call' : 'calls'} remaining. Retries may add calls. Completed items are reused when continuing.</p></div>
          <div><label className="ia-field"><span>OpenAI API key</span><input type="password" autoComplete="off" spellCheck={false} value={apiKey} onChange={event => onKeyChange(event.target.value)} required maxLength={512} placeholder="sk-…" /></label>
            <p className="ia-small">Used only for scoring. Kept in memory for this tab.</p>
            <button className="ia-primary" disabled={busy || !apiKey.trim() || !remaining}>{busy ? 'Starting…' : run.processed ? 'Continue analysis' : 'Analyze items'}</button></div>
        </form>}
      </>}
    </section>
    <section id="ia-score-step-3" className={`ia-stage${current === 3 ? ' ia-stage-current' : ''}`} tabIndex={-1} aria-labelledby="ia-score-results-title">
      <h2 id="ia-score-results-title">3. Results</h2>
      {run?.spec ? <>
        <p>Six scores per item. Select a score to inspect its explanation, evidence, and missing information.</p>
        {inspectionError ? <div role="alert"><p>{inspectionError}</p><button className="ia-secondary" onClick={retryInspection}>Retry item inspection</button></div> : <ItemJudgments run={run} page={page} setPage={setPage} pageLoading={pageLoading} filter={filter} onFilterChange={inspect} filteredItems={filteredItems} filterLoading={filterLoading} />}
        {run.processed > 0 && <details className="ia-original"><summary>Score distributions and original benchmark assessment</summary><SummaryFindings run={run} onInspect={inspect} /></details>}
        <DimensionAverages run={run} />
        <ResultExports run={run} onDownload={onDownload} onViewReport={onViewReport} onDownloadPackage={onDownloadPackage} downloading={downloading} />
        {management}
      </> : <p>Item scores will appear here as they are saved.</p>}
    </section>
  </>
}
