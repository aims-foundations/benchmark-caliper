import { useEffect, useRef, useState } from 'react'
import { getDirectSetup, searchSources } from './api'
import type { AssessmentReference, AssessmentSetup, AssessmentSource, ConfirmedDataset, DirectContext } from './types'

interface Props {
  assessment: AssessmentReference
  setup: AssessmentSetup
  confirmed: ConfirmedDataset | null
  onConfirm: (dataset: ConfirmedDataset | null) => void
  directContext?: DirectContext
  onSelectionChange?: (source: AssessmentSource | null, file: File | null) => void
}

const MATCH_LABELS = { identifier: 'Identifier match', exact_name: 'Name match', related_name: 'Related name', search: 'Search result' }

function SourceDetails({ source }: { source: AssessmentSource }) {
  return <div className="ia-source-details">
    <p><strong>{MATCH_LABELS[source.match_type]}</strong></p>
    {source.match_reasons.length > 0 && <ul aria-label="Match evidence">{source.match_reasons.map(reason => <li key={reason}>{reason}</li>)}</ul>}
    {source.conflicts.length > 0 && <div className="ia-match-conflicts"><strong>Metadata differences to review</strong><ul>{source.conflicts.map(conflict => <li key={conflict}>{conflict}</li>)}</ul></div>}
    <dl className="ia-source-facts">
      <div><dt>Version</dt><dd>{source.version || 'Not recorded'}</dd></div>
      <div><dt>Testing scope</dt><dd>{source.testing_scope || 'Not recorded'}</dd></div>
      <div><dt>Split</dt><dd>{source.split || 'Not recorded'}</dd></div>
      <div><dt>Items</dt><dd>{source.item_count.toLocaleString()}</dd></div>
      <div><dt>Source</dt><dd>{source.source_label}</dd></div>
      <div><dt>Snapshot revision</dt><dd>{source.source_revision ? <code>{source.source_revision}</code> : 'Not recorded'}</dd></div>
    </dl>
    {source.source_url && <a href={source.source_url} target="_blank" rel="noreferrer">View dataset source ↗</a>}
    {(!source.available || !source.source_revision) && <p className="ia-error">{source.unavailable_reason || 'This snapshot is unavailable. Choose another result or upload the benchmark items.'}</p>}
  </div>
}

/** Read-only discovery and explicit confirmation, before any model request. */
export function BenchmarkConfirmation({ assessment, setup, confirmed, onConfirm, directContext, onSelectionChange }: Props) {
  const initialSource = setup.sources.find(source => source.available && source.source_revision) || setup.sources[0]
  const [datasetMode, setDatasetMode] = useState<'source' | 'upload'>(initialSource ? 'source' : 'upload')
  const [sources, setSources] = useState(setup.sources)
  const [catalog, setCatalog] = useState(setup.catalog)
  const [sourceId, setSourceId] = useState(initialSource?.id || '')
  const [file, setFile] = useState<File | null>(null)
  const [query, setQuery] = useState('')
  const [searched, setSearched] = useState(false)
  const [searching, setSearching] = useState(false)
  const [searchError, setSearchError] = useState('')
  const [fileError, setFileError] = useState('')
  const request = useRef<AbortController | null>(null)
  const identity = setup.benchmark_identity
  const originalName = identity.full_name || identity.name || setup.assessment.benchmark_name || setup.assessment.benchmark
  const source = sources.find(candidate => candidate.id === sourceId)
  const canConfirm = !searching && (datasetMode === 'upload' ? !!file : !!source?.available && !!source.source_revision)
  const repositoryUrl = /^[A-Za-z0-9][A-Za-z0-9._-]*\/[A-Za-z0-9][A-Za-z0-9._-]*$/.test(catalog.repo)
    ? `https://huggingface.co/datasets/${catalog.repo}` : null

  useEffect(() => () => request.current?.abort(), [])
  useEffect(() => {
    onSelectionChange?.(datasetMode === 'source' ? source || null : null, datasetMode === 'upload' ? file : null)
  }, [datasetMode, source, file, onSelectionChange])

  function invalidate() {
    request.current?.abort()
    setSearching(false)
    onConfirm(null)
  }

  function changeMode(next: 'source' | 'upload') {
    invalidate()
    // Switching modes unmounts the browser's file input; do not retain an
    // invisible file selection that the user would then be confirming.
    setFile(null)
    setFileError('')
    setDatasetMode(next)
  }

  async function search() {
    invalidate()
    setSourceId('')
    setSources([])
    setSearchError('')
    setSearching(true)
    setSearched(true)
    const controller = new AbortController()
    request.current = controller
    try {
      const result = directContext
        ? await getDirectSetup(directContext, query.trim(), controller.signal)
        : await searchSources(assessment, query.trim(), controller.signal)
      if (controller.signal.aborted) return
      setSources(result.sources)
      setCatalog(result.catalog)
      setSourceId((result.sources.find(candidate => candidate.available && candidate.source_revision) || result.sources[0])?.id || '')
    } catch (problem) {
      if (!controller.signal.aborted) setSearchError(problem instanceof Error ? problem.message : 'Could not search the Data Bank. Try again or upload the benchmark items.')
    } finally {
      if (!controller.signal.aborted) setSearching(false)
    }
  }

  function confirm() {
    if (!canConfirm) return
    if (datasetMode === 'upload' && file) onConfirm({ benchmark_confirmed: true, items_file: file })
    else if (source?.source_revision) onConfirm({ benchmark_confirmed: true, source_id: source.id, source_revision: source.source_revision })
  }

  return <div className="ia-benchmark-confirmation">
    <h3>Confirm the benchmark and snapshot</h3>
    <p>We look for {directContext ? 'your benchmark' : 'the assessed benchmark'} in the Measurement Data Bank. Review the identity and snapshot before confirming, including when a match is exact.</p>
    <div className="ia-detected-benchmark">
      <p className="ia-eyebrow">{directContext ? 'Benchmark you specified' : 'Benchmark detected from the assessment'}</p><strong>{originalName}</strong>
      {identity.name !== originalName && <p className="ia-small">Short name: {identity.name}</p>}
      <dl className="ia-source-facts">
        <div><dt>Paper year</dt><dd>{identity.year || 'Not recorded'}</dd></div>
        <div><dt>Version</dt><dd>{identity.version || 'Not recorded'}</dd></div>
        <div><dt>Languages</dt><dd>{identity.languages.length > 0 ? identity.languages.join(', ') : 'Not recorded'}</dd></div>
      </dl>
      {identity.paper_urls.map(url => <a key={url} href={url} target="_blank" rel="noreferrer">View benchmark paper ↗</a>)}
      {identity.source_urls.map(url => <a key={url} href={url} target="_blank" rel="noreferrer">View benchmark's original source ↗</a>)}
    </div>
    <p className={`ia-small${catalog.status === 'unavailable' ? ' ia-catalog-unavailable' : ''}`} role="status">
      {catalog.status === 'unavailable' ? 'Data Bank catalog unavailable. ' : catalog.status === 'cached' ? 'Using cached Data Bank metadata. ' : 'Data Bank metadata loaded. '}{catalog.message}
    </p>
    {repositoryUrl && <p className="ia-small">Data Bank repository: <a href={repositoryUrl} target="_blank" rel="noreferrer">{catalog.repo} ↗</a></p>}
    <fieldset className="ia-mode"><legend>Find the matching items</legend>
      <label><input type="radio" name="dataset-source" checked={datasetMode === 'source'} onChange={() => changeMode('source')} /><span><strong>Choose from the Measurement Data Bank</strong><small>Review recommended matches or search for another benchmark.</small></span></label>
      <label><input type="radio" name="dataset-source" checked={datasetMode === 'upload'} onChange={() => changeMode('upload')} /><span><strong>Upload the benchmark’s items</strong><small>Use a CSV or JSON file when the matching snapshot is not available.</small></span></label>
    </fieldset>
    {datasetMode === 'source' ? <>
      <div className="ia-source-search">
        <label className="ia-field"><span>Search the Data Bank</span><input type="search" value={query} placeholder="Benchmark name, paper, or dataset identifier" maxLength={200} onChange={event => { invalidate(); setSourceId(''); setQuery(event.target.value); setSearchError('') }} onKeyDown={event => { if (event.key === 'Enter') { event.preventDefault(); void search() } }} /></label>
        <button className="ia-secondary" type="button" onClick={() => void search()}>{searching ? 'Search again' : 'Search Data Bank'}</button>
      </div>
      {searchError && <p className="ia-error" role="alert">{searchError}</p>}
      {searching && <p role="status">Searching the Data Bank…</p>}
      {!searching && !searchError && sources.length === 0 && <p role="status">No matching benchmark found. Try another name or identifier, or upload the benchmark’s items.</p>}
      {sources.length > 0 && <fieldset className="ia-source-candidates"><legend>{searched ? 'Search results' : 'Recommended matches'}</legend>
        {sources.map(candidate => <div key={candidate.id} className={`ia-source-candidate${candidate.id === sourceId ? ' ia-source-selected' : ''}`}>
          <label><input type="radio" name="benchmark-snapshot" checked={candidate.id === sourceId} onChange={() => { invalidate(); setSourceId(candidate.id) }} /><span><strong>{candidate.title}</strong><small>{candidate.benchmark} · {candidate.item_count.toLocaleString()} items{!candidate.available ? ' · unavailable' : ''}</small></span></label>
          {candidate.id === sourceId && <SourceDetails source={candidate} />}
        </div>)}
      </fieldset>}
    </> : <>
      {setup.sources.length === 0 && catalog.status !== 'unavailable' && <p className="ia-small">No matching benchmark was found automatically. Search the Data Bank above or upload the matching items below.</p>}
      <label className="ia-field"><span>Benchmark items file</span><input type="file" accept=".csv,.json,text/csv,application/json" aria-invalid={!!fileError} onChange={event => {
        invalidate()
        const nextFile = event.target.files?.[0] || null
        if (nextFile && (nextFile.size > setup.upload.max_bytes || !/\.(csv|json)$/i.test(nextFile.name))) {
          setFile(null)
          setFileError(`Choose a CSV or JSON file no larger than ${Math.round(setup.upload.max_bytes / 1024 / 1024)} MB.`)
        } else { setFile(nextFile); setFileError('') }
      }} /></label>
      {fileError && <p className="ia-error" role="alert">{fileError}</p>}
      <p className="ia-small">Include <code>content</code>, with <code>reference_answer</code> when available. Supply unique <code>item_id</code> values or let the website generate them. JSON must be an array of item objects. Up to {setup.upload.max_items.toLocaleString()} items and {Math.round(setup.upload.max_bytes / 1024 / 1024)} MB.</p>
      <details className="ia-upload-example"><summary>See an example file</summary><pre>{'item_id,content,reference_answer\nquestion-1,"What is 2 + 2?",4'}</pre></details>
    </>}
    <div className="ia-confirm-benchmark">
      {datasetMode === 'upload'
        ? <p>Confirm that <strong>{file?.name || 'your uploaded file'}</strong> contains items from <strong>{originalName}</strong> and the version and split you intend to analyze. Uploaded file metadata has not been verified against the Data Bank.</p>
        : <p>Confirm that <strong>{source?.title || 'the selected result'}</strong> is the benchmark {directContext ? 'you specified' : 'assessed above'} and that this is the snapshot you intend to analyze. Check the version, testing scope, and split; missing metadata is shown as “Not recorded.”</p>}
      <button type="button" className="ia-primary" disabled={!canConfirm || !!confirmed} onClick={confirm}>Confirm benchmark</button>
      <p className="ia-small">Searching and confirming do not make paid model calls.</p>
      {confirmed && <p className="ia-confirmed" role="status">Benchmark and {datasetMode === 'upload' ? 'uploaded file' : 'snapshot'} confirmed. Generate the item criteria below when ready.</p>}
    </div>
  </div>
}
