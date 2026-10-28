import { classifierName, readable, SourceValue } from './Criteria'
import type { AnalysisSummary, ClassifierContext, SourcedStatement, Specification } from './types'

const SOURCE_ROLES: Record<string, string> = {
  deployment_requirement: 'Deployment requirements', benchmark_evidence: 'Benchmark documentation',
  domain_evidence: 'Domain evidence', stakeholder_evidence: 'Stakeholder evidence',
  prior_assessment: 'Earlier assessment', rubric: 'Assessment rubric', dataset_profile: 'Dataset profile',
  example_item: 'Example item', elicitation_question: 'Elicitation question', prior_hypothesis: 'Earlier hypothesis',
}

const DIMENSION_CONTEXT: Record<string, string> = {
  input_ontology: 'Required tasks, skills, scenarios, and the boundaries of deployment scope.',
  input_content: 'Deployment expectations and benchmark details used to judge assumptions within the input.',
  output_ontology: 'Expected output categories and the rules for interpreting or scoring answers.',
  output_content: 'Reference-answer documentation and supported domain or stakeholder standards.',
}

function sourceTitle(spec: Specification, id: string, index: number): string {
  const source = spec.source_registry?.[id]
  if (source && typeof source === 'object' && !Array.isArray(source)) {
    const record = source as Record<string, unknown>
    for (const field of ['title', 'source_title', 'name']) {
      if (typeof record[field] === 'string' && record[field]) return String(record[field])
    }
  }
  return `${SOURCE_ROLES[spec.source_roles?.[id] || ''] || 'Source'} ${index + 1}`
}

function SourceReferences({ ids, spec }: { ids: string[]; spec: Specification }) {
  const registryIds = Object.keys(spec.source_registry || {})
  if (!ids.length) return <p className="ia-small">No source reference was recorded.</p>
  return <details className="ia-nested ia-context-sources"><summary>{ids.length === 1 ? 'Supporting source' : `${ids.length} supporting sources`}</summary>
    <p className="ia-small">Read the saved content in the source library:</p>
    {ids.map(id => {
      const index = registryIds.indexOf(id)
      return <div className="ia-source-record" key={id}>{index < 0
        ? <p className="ia-small">This referenced source is not available in the saved library.</p>
        : <button className="ia-text-button" type="button" onClick={event => {
          const target = event.currentTarget.closest('.ia-prepared-context')?.querySelector<HTMLDetailsElement>(`[data-source-index="${index}"]`)
          if (!target) return
          target.open = true
          const library = target.parentElement?.closest('details')
          if (library) library.open = true
          target.querySelector('summary')?.focus()
          target.scrollIntoView?.({ block: 'nearest' })
        }}>{sourceTitle(spec, id, index)}</button>}</div>
    })}
  </details>
}

function Statements({ entries, spec, empty }: { entries: SourcedStatement[]; spec: Specification; empty: string }) {
  return entries.length ? <ul className="ia-context-statements">{entries.map((entry, index) => <li key={index}>
    <p>{entry.statement}</p><SourceReferences ids={entry.source_ids} spec={spec} />
  </li>)}</ul> : <p className="ia-small">{empty}</p>
}

function ContextBlock({ context, spec }: { context: ClassifierContext; spec: Specification }) {
  return <>
    <h4>Requirements used for this dimension</h4>
    <Statements entries={context.deployment_requirements} spec={spec} empty="No deployment requirement was extracted for this dimension. Review its evidence gaps before interpreting judgments." />
    <h4>Benchmark and comparison evidence</h4>
    <Statements entries={context.benchmark_evidence} spec={spec} empty="No benchmark or comparison evidence was recorded for this dimension." />
    <h4>Earlier hypotheses to examine</h4>
    <p className="ia-small">These are starting points for comparison, not established item findings.</p>
    <Statements entries={context.prior_hypotheses} spec={spec} empty="No earlier hypothesis was included for this dimension." />
    <h4>Evidence gaps</h4>
    {context.evidence_gaps.length ? <ul>{context.evidence_gaps.map((gap, index) => <li key={index}>{gap}</li>)}</ul>
      : <p className="ia-small">No gap was recorded for this dimension. This does not establish that the available evidence is complete.</p>}
  </>
}

/** Prepared, deployment-specific content only. Code-owned rules belong in validation. */
export function PreparedContext({ spec, metadata, classifierNames, direct = false }: {
  spec: Specification; metadata?: AnalysisSummary['specification']; classifierNames?: Record<string, string>; direct?: boolean
}) {
  const inventory = spec.input_category_inventory
  const contexts = Object.entries(spec.context_by_classifier || {})
  const requirements = [...new Map(contexts.flatMap(([, context]) => context.deployment_requirements)
    .map(entry => [JSON.stringify([entry.statement, [...entry.source_ids].sort()]), entry])).values()]
  const gaps = [...new Set([...(inventory?.evidence_gaps || []), ...contexts.flatMap(([, context]) => context.evidence_gaps)])]
  const sources = Object.entries(spec.source_registry || {})

  return <div className="ia-prepared-context">
    <p className="ia-muted">This prepared context connects your deployment requirements and available sources to each classifier. Review the interpretation and missing evidence before classifying items.</p>
    <p className="ia-small">{direct ? 'Input Form and Output Form are not assessed in this path.' : 'Input Form and Output Form remain in the original benchmark assessment.'} Fixed classifier rules appear in step 3.</p>

    <section className="ia-context-section" aria-label="Prepared deployment requirements">
      <h3>Deployment requirements</h3>
      <p className="ia-small">Requirements shared across dimensions appear once here; each dimension below shows which requirements it uses.</p>
      <Statements entries={requirements} spec={spec} empty="No sourced deployment requirements are available in this saved context." />
      {metadata?.deployment_text_matches === false && <p className="ia-error">This saved specification describes the deployment in different words. Compare it with the deployment confirmed in step 1.</p>}
    </section>

    <section className="ia-context-section" aria-label="Required input categories">
      <div className="ia-section-heading"><h3>Required input categories</h3>{inventory && <span className="ia-tag ia-tag-muted">{readable(inventory.completeness)} inventory</span>}</div>
      {inventory ? <>
        <p className="ia-small">These definitions describe the tasks or situations that Input Ontology will look for. {inventory.completeness === 'complete'
          ? 'The prepared context marks this inventory as complete; review its cited support before accepting that interpretation.'
          : 'A partial or unknown inventory does not make an unmatched item out of scope.'}</p>
        {inventory.categories.length ? <div className="ia-criteria-list">{inventory.categories.map(category => <details className="ia-criterion" key={category.id}>
          <summary><span><strong>{category.name}</strong></span></summary>
          <div className="ia-criterion-body"><p>{category.definition}</p><SourceReferences ids={category.source_ids} spec={spec} />
            <details className="ia-nested"><summary>Category identifier</summary><code>{category.id}</code></details>
          </div>
        </details>)}</div> : <p>No required categories were identified from the available context.</p>}
        {!!inventory.completeness_source_ids.length && <details className="ia-nested"><summary>Support for inventory completeness</summary><SourceReferences ids={inventory.completeness_source_ids} spec={spec} /></details>}
      </> : <p className="ia-small">This historical specification does not record a sourced category inventory.</p>}
    </section>

    <section className="ia-context-section" aria-label="Dimension-specific context">
      <h3>Context for each dimension</h3>
      <p className="ia-small">Open a dimension to inspect its requirements, comparison evidence, earlier hypotheses, and evidence gaps.</p>
      <div className="ia-criteria-list">{spec.classifiers.map(classifier => {
        const context = spec.context_by_classifier?.[classifier.id]
        return <details className="ia-criterion" key={classifier.id}>
          <summary><span><strong>{classifierName(classifier.id, classifierNames)}</strong>{DIMENSION_CONTEXT[classifier.id] && <small>{DIMENSION_CONTEXT[classifier.id]}</small>}</span>
            <span className="ia-tag ia-tag-muted">{context ? `${context.evidence_gaps.length} evidence gap${context.evidence_gaps.length === 1 ? '' : 's'}` : 'Historical context'}</span>
          </summary>
          <div className="ia-criterion-body">{context ? <ContextBlock context={context} spec={spec} />
            : <><p>No separate sourced context block was recorded for this classifier.</p>{!!classifier.grounded_in?.length && <ul>{classifier.grounded_in.map((source, index) => <li key={index}>{source}</li>)}</ul>}</>}</div>
        </details>
      })}</div>
    </section>

    <section className="ia-context-section" aria-label="Prepared evidence gaps">
      <h3>Evidence gaps to keep in view</h3>
      {gaps.length ? <ul>{gaps.map(gap => <li key={gap}>{gap}</li>)}</ul>
        : <p className="ia-small">No evidence gaps were recorded. This is not a finding that all necessary evidence is available.</p>}
      <p className="ia-small">Missing evidence may lead to an “insufficient evidence” judgment. It does not by itself establish an incompatibility.</p>
    </section>

    <details className="ia-original"><summary>Source library · {sources.length} registered source{sources.length === 1 ? '' : 's'}</summary>
      <p className="ia-small">Source roles distinguish deployment requirements, benchmark evidence, and earlier assessments. Open a source to read its saved content and reference identifier.</p>
      {sources.length ? sources.map(([id, source], index) => <details className="ia-source-record" key={id} data-source-index={index}>
        <summary>{sourceTitle(spec, id, index)}</summary>
        <p className="ia-small">Role: {SOURCE_ROLES[spec.source_roles?.[id] || ''] || 'Not recorded'} · Reference: <code>{id}</code></p>
        <SourceValue value={source} />
      </details>) : <p>No source library was recorded in this historical specification.</p>}
    </details>
  </div>
}
