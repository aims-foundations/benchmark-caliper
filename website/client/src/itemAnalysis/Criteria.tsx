import type { AnalysisSummary, Classifier, Specification } from './types'

export const CLASSIFIER_NAMES: Record<string, string> = {
  input_ontology: 'Input Ontology',
  input_content: 'Input Content',
  input_form: 'Input Form',
  output_form: 'Output Form',
  output_ontology: 'Output Ontology',
  output_content: 'Output Content',
  // Historical artifacts retain their original meanings.
  'IO.task_category': 'Task coverage',
  'OO.output_category': 'Expected answer categories',
  'OO.value_encoding': 'Regional conventions',
  'IC.region_fit': 'Regional relevance',
  'OC.label_contestability': 'Answer contestability',
}

export const readable = (value: string) => value.replaceAll('_', ' ')
export const classifierName = (id: string, names?: Record<string, string>) => names?.[id] || CLASSIFIER_NAMES[id] || readable(id)
export const classifierQuestion = (classifier: Classifier) => classifier.question || classifier.criterion || ''

export function labelName(classifier: Classifier, label: string | number | null): string {
  if (label === null) return 'Unknown'
  if (classifier.operation === 'flag') return String(label) === '1' ? 'Flagged' : 'Not flagged'
  if (classifier.operation === 'ordinal') return `${label} · ${classifier.ordinal_anchors?.[String(label)] || 'Unspecified'}`
  return readable(String(label))
}

export function SourceValue({ value }: { value: unknown }) {
  if (Array.isArray(value)) return <ul>{value.map((entry, index) => <li key={index}><SourceValue value={entry} /></li>)}</ul>
  if (value && typeof value === 'object') return <dl className="ia-source-fields">{Object.entries(value).map(([key, entry]) => <div key={key}><dt>{readable(key)}</dt><dd><SourceValue value={entry} /></dd></div>)}</dl>
  return <p className="ia-source-text">{value == null ? 'Not recorded' : String(value)}</p>
}

export function Criteria({ spec, metadata, classifierNames, direct = false }: { spec: Specification; metadata?: AnalysisSummary['specification']; classifierNames?: Record<string, string>; direct?: boolean }) {
  const generic = spec.fixed_catalog_version === 'caliper_generic_items_v1'
  const inventory = spec.input_category_inventory
  return <section className="ia-criteria" aria-label="Classification criteria">
    <div className="ia-section-heading"><div><p className="ia-eyebrow">The questions we ask</p>
      <h2>Review the criteria</h2></div><span>{spec.classifiers.filter(c => c.applicable).length} active classifiers</span></div>
    <p className="ia-muted">Open a criterion to see exactly how each item will be judged. {direct ? 'Input Form and Output Form are not assessed in this path.' : 'Input Form and Output Form stay in the original benchmark assessment.'}</p>
    <details className="ia-original"><summary>Criteria context and preparation notes</summary>
      <p><strong>Deployment used by these criteria</strong></p><p>{spec.deployment_description || spec.deployment}</p>
      <p className="ia-small">Catalog: {spec.fixed_catalog_version || 'caliper_induced_items_legacy_v1'} · Schema: {spec.schema_version || 'caliper_item_spec_legacy_v1'}</p>
      {generic && <p className="ia-small">Fixed rubric rules apply across benchmarks. Prepared context requires human source review; structural validation alone does not establish that its claims are supported.</p>}
      {!generic && <p className="ia-small">Historical classifier definitions and labels are shown with their original meanings.</p>}
      {metadata?.deployment_text_matches === false && <p className="ia-small">This supplied specification describes the deployment in different words. Compare it with the original deployment in “Context and usage” above.</p>}
      {metadata?.note && <p className="ia-small">{metadata.note}</p>}
      {!!metadata?.adjustments?.length && <><p className="ia-small">Preparation adjustments</p><ul className="ia-small">{metadata.adjustments.map((adjustment, i) => <li key={i}>{adjustment.reason || adjustment.field}</li>)}</ul></>}
      {spec.source_registry && <details><summary>Registered source contents</summary>{Object.entries(spec.source_registry).map(([id, source]) => <details className="ia-source-record" key={id}><summary>{id}</summary><SourceValue value={source} /></details>)}</details>}
    </details>
    <div className="ia-criteria-list">{spec.classifiers.map(classifier => {
      const context = spec.context_by_classifier?.[classifier.id]
      return <details key={classifier.id} className="ia-criterion">
        <summary><span><small>{readable(classifier.component)}</small><strong>{classifierName(classifier.id, classifierNames)}</strong></span>
          <span className={`ia-tag ${classifier.applicable ? '' : 'ia-tag-muted'}`}>{classifier.applicable ? { multilabel: 'Category matches', judgment: 'Evidence judgment', assignment: 'Category', ordinal: 'Regional fit', flag: 'Yes / no' }[classifier.operation] : 'Not applicable'}</span>
        </summary>
        <div className="ia-criterion-body">
          <p>{classifier.applicable ? classifierQuestion(classifier) : classifier.na_reason || (direct ? 'Not assessed in this item analysis.' : 'Assessed at benchmark level.')}</p>
          {classifier.applicable && <>
            {!!classifier.decision_rules?.length && <ul>{classifier.decision_rules.map(rule => <li key={rule}>{rule}</li>)}</ul>}
            {(classifier.labels || classifier.category_set) && <div className="ia-label-list">{(classifier.labels || classifier.category_set)!.map(label => <span key={label}>{readable(label)}</span>)}</div>}
            {classifier.ordinal_anchors && <dl className="ia-anchors">{Object.entries(classifier.ordinal_anchors).map(([label, anchor]) => <div key={label}><dt>{label}</dt><dd>{anchor}</dd></div>)}</dl>}
            {classifier.positive_class && <p className="ia-small">Flag means: {readable(classifier.positive_class)}.</p>}
            <p className="ia-small">{generic ? 'Insufficient evidence records an evidence gap. No issue identified is a bounded finding, not proof of benchmark validity.' : 'Unknown is allowed when the evidence is insufficient.'}</p>
          </>}
          {classifier.id === 'input_ontology' && inventory && <details className="ia-nested"><summary>Required categories · {inventory.completeness} inventory</summary>
            <p>A partial or unknown inventory does not make an unmatched item out of scope.</p>
            {!!inventory.completeness_source_ids.length && <p>Completeness evidence: {inventory.completeness_source_ids.join(', ')}</p>}
            <ul>{inventory.categories.map(category => <li key={category.id}><strong>{category.name} ({category.id})</strong>: {category.definition} <small>Sources: {category.source_ids.join(', ')}</small></li>)}</ul>
            {inventory.evidence_gaps.map(gap => <p key={gap}>Evidence gap: {gap}</p>)}
          </details>}
          {context && <details className="ia-nested"><summary>Sourced context and evidence gaps</summary>
            {(['deployment_requirements', 'benchmark_evidence', 'prior_hypotheses'] as const).map(field => <div key={field}><strong>{readable(field)}</strong><ul>{context[field].map((entry, i) => <li key={i}>{entry.statement} <small>Sources: {entry.source_ids.join(', ')}</small></li>)}</ul></div>)}
            {context.evidence_gaps.map(gap => <p key={gap}>Evidence gap: {gap}</p>)}
          </details>}
          {!!classifier.grounded_in?.length && <details className="ia-nested"><summary>{direct ? 'Source requirements' : 'Source findings'}</summary><ul>{classifier.grounded_in.map((source, i) => <li key={i}>{source}</li>)}</ul></details>}
        </div>
      </details>
    })}</div>
  </section>
}
