import { useState } from 'react'
import { classifierName, SourceValue } from './Criteria'
import type { Item, Specification } from './types'

export const SCORE_DIMENSIONS = ['input_ontology', 'input_content', 'input_form', 'output_ontology', 'output_content', 'output_form'] as const
function display(value: unknown): string { return typeof value === 'string' ? value : value == null ? 'Not supplied' : JSON.stringify(value, null, 2) }

export function SixScoreTable({ items, spec, loading }: { items: Item[]; spec: Specification; loading: boolean }) {
  const [selected, setSelected] = useState<{ itemId: string; dimension: string } | null>(null)
  const item = items.find(candidate => candidate.item_id === selected?.itemId)
  const dimension = selected?.dimension
  const judgment = dimension ? item?.dimensions?.[dimension] : undefined
  return <>
    <div className="ia-score-table-scroll" aria-busy={loading}><table className="ia-score-table"><caption>Item scores · 1 to 5, or Unknown when evidence is insufficient</caption>
      <thead><tr><th rowSpan={2} scope="col">Item</th><th colSpan={3} scope="colgroup">Input</th><th colSpan={3} scope="colgroup">Output</th></tr>
        <tr>{SCORE_DIMENSIONS.map(id => <th scope="col" key={id}>{classifierName(id).replace(/^(Input|Output) /, '')}</th>)}</tr></thead>
      <tbody>{items.map(item => <tr key={item.item_id}><th scope="row"><span className="ia-score-item-id">{item.item_id}</span><span className="ia-score-preview">{display(item.content)}</span></th>
        {SCORE_DIMENSIONS.map(id => {
          const assessment = item.dimensions?.[id]
          const value = assessment ? assessment.score === null ? 'Unknown' : String(assessment.score) : item.status === 'error' ? 'Needs retry' : 'Pending'
          return <td key={id}><button type="button" className={`ia-score-cell ia-score-${assessment?.score ?? 'unknown'}`} aria-label={`${item.item_id} · ${classifierName(id)}: ${value}`} aria-pressed={selected?.itemId === item.item_id && dimension === id}
            onClick={() => setSelected({ itemId: item.item_id, dimension: id })}>{value}</button></td>
        })}</tr>)}</tbody>
    </table></div>
    {item && dimension && <section className="ia-score-inspection" aria-label="Selected score details" aria-live="polite">
      <div className="ia-section-heading"><h3>{classifierName(dimension)} · {judgment ? judgment.score === null ? 'Unknown' : `${judgment.score} / 5` : item.status === 'error' ? 'Needs retry' : 'Pending'}</h3><button className="ia-text-button" onClick={() => setSelected(null)}>Close details</button></div>
      <p className="ia-small">Item: {item.item_id}</p>
      {judgment ? <><h4>Explanation</h4><p>{judgment.justification}</p><h4>Evidence</h4>{judgment.evidence.length ? <ul>{judgment.evidence.map((evidence, index) => <li key={index}>{evidence}</li>)}</ul> : <p>No supporting evidence recorded.</p>}
        <h4>Missing information</h4>{judgment.information_gaps.length ? <ul>{judgment.information_gaps.map((gap, index) => <li key={index}>{gap}</li>)}</ul> : <p>No material gaps recorded.</p>}
      </> : item.status === 'error' ? <p className="ia-error">{item.error || 'Scoring failed for this item. Continue analysis to retry it.'}</p> : <p>This item has not been scored yet.</p>}
      <details className="ia-original" open><summary>Complete item and reference answer</summary><pre className="ia-item-text">{display(item.content)}</pre><h4>Reference answer</h4><pre className="ia-item-text">{display(item.reference_answer)}</pre>
        <h4>Grading criteria</h4><SourceValue value={item.grading_criterion} />
        {item.item_features != null && <><h4>Item metadata</h4><SourceValue value={item.item_features} /></>}
        {item.asset_manifest != null && <><h4>Media and availability</h4><SourceValue value={item.asset_manifest} /><p className="ia-small">A media reference alone does not establish that the scorer inspected its content.</p></>}
        {item.verifier != null && <><h4>Verifier</h4><SourceValue value={item.verifier} /></>}
      </details>
      <details className="ia-original"><summary>Shared source references</summary>{Object.entries(spec.source_registry || {}).map(([id, source]) => <details key={id}><summary>{id}</summary><SourceValue value={source} /></details>)}</details>
    </section>}
  </>
}
