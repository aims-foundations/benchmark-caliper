import type { AnalysisSummary, Classifier, Specification } from './types'

export const CLASSIFIER_NAMES: Record<string, string> = {
  'IO.task_category': 'Task coverage',
  'OO.output_category': 'Expected answer categories',
  'OO.value_encoding': 'Regional conventions',
  'IC.region_fit': 'Regional relevance',
  'OC.label_contestability': 'Answer contestability',
}

export const readable = (value: string) => value.replaceAll('_', ' ')
export const classifierName = (id: string) => CLASSIFIER_NAMES[id] || readable(id)

export function labelName(classifier: Classifier, label: string | number | null): string {
  if (label === null) return 'Unknown'
  if (classifier.operation === 'flag') return String(label) === '1' ? 'Flagged' : 'Not flagged'
  if (classifier.operation === 'ordinal') return `${label} · ${classifier.ordinal_anchors?.[String(label)] || 'Unspecified'}`
  return readable(String(label))
}

export function Criteria({ spec, metadata }: { spec: Specification; metadata?: AnalysisSummary['specification'] }) {
  return <section className="ia-criteria" aria-label="Classification criteria">
    <div className="ia-section-heading"><div><p className="ia-eyebrow">The questions we ask</p>
      <h2>Review the criteria</h2></div><span>{spec.classifiers.filter(c => c.applicable).length} active classifiers</span></div>
    <p className="ia-muted">Open a criterion to see exactly how each item will be judged. Input Form and Output Form stay in the original benchmark assessment.</p>
    <details className="ia-original"><summary>Criteria context and preparation notes</summary>
      <p><strong>Deployment used by these criteria</strong></p><p>{spec.deployment}</p>
      {metadata?.deployment_text_matches === false && <p className="ia-small">This supplied specification describes the deployment in different words. Compare it with the original deployment in “Context and usage” above.</p>}
      {metadata?.note && <p className="ia-small">{metadata.note}</p>}
      {!!metadata?.adjustments?.length && <><p className="ia-small">Preparation adjustments</p><ul className="ia-small">{metadata.adjustments.map((adjustment, i) => <li key={i}>{adjustment.reason || adjustment.field}</li>)}</ul></>}
    </details>
    <div className="ia-criteria-list">{spec.classifiers.map(classifier => <details key={classifier.id} className="ia-criterion">
      <summary><span><small>{readable(classifier.component)}</small><strong>{classifierName(classifier.id)}</strong></span>
        <span className={`ia-tag ${classifier.applicable ? '' : 'ia-tag-muted'}`}>{classifier.applicable ? { assignment: 'Category', ordinal: 'Regional fit', flag: 'Yes / no' }[classifier.operation] : 'Not applicable'}</span>
      </summary>
      <div className="ia-criterion-body">
        <p>{classifier.applicable ? classifier.criterion : classifier.na_reason || 'Assessed at benchmark level.'}</p>
        {classifier.applicable && <>
          {classifier.category_set && <div className="ia-label-list">{classifier.category_set.map(category => <span key={category}>{readable(category)}</span>)}</div>}
          {classifier.ordinal_anchors && <dl className="ia-anchors">{Object.entries(classifier.ordinal_anchors).map(([label, anchor]) => <div key={label}><dt>{label}</dt><dd>{anchor}</dd></div>)}</dl>}
          {classifier.positive_class && <p className="ia-small">Flag means: {readable(classifier.positive_class)}.</p>}
          <p className="ia-small">Unknown is allowed when the evidence is insufficient.</p>
        </>}
        {!!classifier.grounded_in?.length && <details className="ia-nested"><summary>Source findings</summary><ul>{classifier.grounded_in.map((source, i) => <li key={i}>{source}</li>)}</ul></details>}
      </div>
    </details>)}</div>
  </section>
}
