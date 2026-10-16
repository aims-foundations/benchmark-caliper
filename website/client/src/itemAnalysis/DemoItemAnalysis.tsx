import { useEffect, useMemo, useRef, useState } from 'react'
import { DEMO_DEPLOYMENT_DESCRIPTION } from '../demo/fixture'
import { DEMO_ITEM_STORAGE_KEY, resetDemoItemProgress } from '../demo/session'
import {
  buildDemoItemAnalysisRun, DEMO_ITEM_ANALYSIS_PILOT_SIZE, DEMO_ITEM_ANALYSIS_PROVENANCE,
  DEMO_ITEM_ANALYSIS_SPEC, DEMO_ITEM_ANALYSIS_CLASSIFIER_NAMES,
} from '../demo/itemAnalysisFixture'
import { Criteria } from './Criteria'
import { Results } from './Results'
import { buildDemoExport } from './demoExports'
import type { Artifact } from './types'
import './itemAnalysis.css'
import './DemoItemAnalysis.css'

type Stage = 'identify' | 'confirmed' | 'criteria' | 'pilot' | 'complete'
const STAGES: Stage[] = ['identify', 'confirmed', 'criteria', 'pilot', 'complete']

function restoreStage(): Stage {
  try {
    const saved: unknown = JSON.parse(sessionStorage.getItem(DEMO_ITEM_STORAGE_KEY) || 'null')
    if (saved && typeof saved === 'object' && 'version' in saved && saved.version === 1 && 'stage' in saved && STAGES.includes(saved.stage as Stage)) return saved.stage as Stage
  } catch { /* Invalid or unavailable storage starts a fresh walkthrough. */ }
  return 'identify'
}

export function DemoItemAnalysis({ onStatusChange }: {
  onStatusChange?: (status: 'pending' | 'in_progress' | 'complete') => void
}) {
  const [stage, setStage] = useState<Stage>(restoreStage)
  const [reviewed, setReviewed] = useState(false)
  const [page, setPage] = useState(1)
  const [downloadError, setDownloadError] = useState('')
  const resultHeading = useRef<HTMLHeadingElement>(null)
  const run = useMemo(() => buildDemoItemAnalysisRun(stage === 'complete' ? 'sample' : 'pilot'), [stage])
  const source = DEMO_ITEM_ANALYSIS_PROVENANCE
  const showingCriteria = ['criteria', 'pilot', 'complete'].includes(stage)
  const showingResults = stage === 'pilot' || stage === 'complete'
  const step = stage === 'identify' ? 0 : stage === 'confirmed' || stage === 'criteria' ? 1 : stage === 'pilot' ? 2 : 3

  useEffect(() => {
    try { sessionStorage.setItem(DEMO_ITEM_STORAGE_KEY, JSON.stringify({ version: 1, stage })) } catch { /* Progress still works in memory. */ }
    onStatusChange?.(stage === 'complete' ? 'complete' : stage === 'identify' ? 'pending' : 'in_progress')
  }, [stage, onStatusChange])

  useEffect(() => {
    if (stage === 'pilot' || stage === 'complete') resultHeading.current?.focus()
  }, [stage])

  function restart() {
    resetDemoItemProgress()
    setStage('identify')
    setReviewed(false)
    setPage(1)
    setDownloadError('')
  }

  function download(artifact: Artifact) {
    setDownloadError('')
    let url: string | undefined
    let link: HTMLAnchorElement | undefined
    try {
      const result = buildDemoExport(artifact, showingResults ? run : { ...run, status: 'ready', scope: null, complete: 0, processed: 0 })
      url = URL.createObjectURL(new Blob([result.content], { type: result.mimeType }))
      link = document.createElement('a')
      link.href = url
      link.download = result.filename
      document.body.appendChild(link)
      link.click()
    } catch {
      setDownloadError('The demo export could not be downloaded. Please try again.')
    } finally {
      link?.remove()
      if (url) { const downloadUrl = url; setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000) }
    }
  }

  return <div className="item-analysis-site ia-embedded ia-demo" aria-label="Free MathDial item analysis demo">
    <div className="ia-demo-intro"><div><p className="ia-eyebrow">MathDial walkthrough · item analysis</p>
      <h2>Follow the assessment into the items</h2>
      <p>This free demo uses {run.total} public MathDial examples and authored walkthrough judgments. No API key or model calls are needed.</p></div>
      <button type="button" className="ia-text-button" onClick={restart}>Restart item demo</button></div>

    <ol className="ia-steps ia-demo-steps" aria-label="Demo item analysis progress">
      {['Confirm benchmark', 'Review criteria', 'Review pilot', 'Complete demo sample'].map((label, index) => <li key={label}
        aria-current={index === step ? 'step' : undefined} data-done={index < step || stage === 'complete' ? true : undefined}>
        <span aria-hidden="true">{index < step || stage === 'complete' ? '✓' : index + 1}</span>{label}</li>)}
    </ol>

    <section className="ia-panel ia-demo-source" aria-label="Demo benchmark and source">
      <div className="ia-section-heading"><div><p className="ia-eyebrow">The benchmark in this assessment</p><h2>MathDial</h2></div>
        {stage !== 'identify' && <span className="ia-tag">Benchmark confirmed</span>}</div>
      <p>Continue the MathDial assessment for the India urban tutoring deployment with this fixed {run.total}-item demo sample.</p>
      <dl className="ia-demo-source-facts"><div><dt>Dataset</dt><dd>{source.title}</dd></div>
        <div><dt>Sample</dt><dd>{source.sample_description}</dd></div>
        <div><dt>License</dt><dd><a href={source.license_url} target="_blank" rel="noreferrer">{source.license}</a></dd></div>
        <div><dt>Source revision</dt><dd><code>{source.revision}</code></dd></div></dl>
      <a href={source.source_url} target="_blank" rel="noreferrer">View the pinned MathDial source ↗</a>
      <p className="ia-small ia-demo-attribution">{source.citation} <a href={source.paper_url} target="_blank" rel="noreferrer">Read the paper ↗</a></p>
      <p className="ia-small">{source.changes}</p>
      <p className="ia-small">{source.student_provenance}</p>
      <p className="ia-small">{source.source_route}</p>
      <p className="ia-demo-disclosure"><strong>Authored example judgments.</strong> {source.label_provenance} Results describe only this bundled sample, not the full MathDial benchmark.</p>
      <details className="ia-original"><summary>Deployment from the original assessment</summary><p className="ia-demo-deployment">{DEMO_DEPLOYMENT_DESCRIPTION}</p></details>
      {stage === 'identify' && <div className="ia-demo-next"><p>Confirm that this MathDial sample is the dataset you want to use for the walkthrough of the assessment above.</p>
        <button type="button" className="ia-primary" onClick={() => setStage('confirmed')}>Confirm benchmark</button></div>}
    </section>

    {stage === 'confirmed' && <section className="ia-demo-next ia-demo-stage" aria-label="Demo criteria preparation"><h3>Benchmark confirmed. Review the item criteria next.</h3>
      <p>The demo criteria were authored for the same deployment and benchmark findings shown above. Open them to see the questions applied to each example.</p>
      <button type="button" className="ia-primary" onClick={() => setStage('criteria')}>Show demo criteria</button></section>}

    {showingCriteria && <><Criteria spec={DEMO_ITEM_ANALYSIS_SPEC} metadata={run.summary?.specification} classifierNames={DEMO_ITEM_ANALYSIS_CLASSIFIER_NAMES} />
      <button type="button" className="ia-secondary" onClick={() => download('spec')}>Download demo criteria JSON <span aria-hidden="true">↓</span></button></>}

    {stage === 'criteria' && <section className="ia-demo-next ia-demo-stage" aria-label="Demo pilot preparation"><h3>Start with a small pilot</h3>
      <p>Inspect the authored judgments for {DEMO_ITEM_ANALYSIS_PILOT_SIZE} of the {run.total} bundled examples before continuing through the sample. Use the pilot to check how the criteria fit the item text.</p>
      <button type="button" className="ia-primary" onClick={() => setStage('pilot')}>Show pilot results</button></section>}

    {showingResults && <>
      <div className="ia-demo-status" role="status"><h3 ref={resultHeading} tabIndex={-1}>{stage === 'complete' ? 'Demo item analysis complete' : 'Pause for a human review'}</h3>
        <p>{stage === 'complete' ? `All ${run.total} bundled demo items are included below. This completes the walkthrough sample; it does not assess the full MathDial dataset.` : `${DEMO_ITEM_ANALYSIS_PILOT_SIZE} of ${run.total} demo items have example judgments. Open the items below, compare the evidence with the criteria, and review the pilot before continuing.`}</p></div>
      <Results run={run} page={page} setPage={setPage} onDownload={download} downloading={null} pageLoading={false} demo classifierNames={DEMO_ITEM_ANALYSIS_CLASSIFIER_NAMES} />
      {stage === 'pilot' && <section className="ia-demo-checkpoint" aria-label="Human review checkpoint"><h3>Check the pilot before continuing</h3>
        <p>Do the example labels and quoted evidence follow the criteria? For a real analysis, this is the point to catch ambiguous rules or misread items before applying them to the rest of the dataset.</p>
        <label><input type="checkbox" checked={reviewed} onChange={event => setReviewed(event.target.checked)} />
          <span>I have reviewed the pilot examples and criteria</span></label>
        <button type="button" className="ia-primary" disabled={!reviewed} onClick={() => { if (reviewed) setStage('complete') }}>Continue demo through remaining items</button>
        <p className="ia-small">This reveals the remaining authored example judgments. No model is run.</p></section>}
    </>}
    {downloadError && <p className="ia-error" role="alert">{downloadError}</p>}
  </div>
}
