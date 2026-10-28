import { classifierName, classifierQuestion, labelName, SourceValue } from './Criteria'
import type { AnalysisRun } from './types'

const VALIDATION_FAILURES = new Set(['invalid_json', 'schema', 'evidence', 'deployment', 'provenance', 'task_grounding'])

/** Explain checks performed by the server; never manufacture a per-check result log. */
export function ContextValidation({ run, onDownload, demo = false }: { run: AnalysisRun; onDownload?: () => void; demo?: boolean }) {
  const spec = run.spec
  const metadata = run.summary?.specification
  const generic = spec?.fixed_catalog_version === 'caliper_generic_items_v1'
  const failedChecks = !spec && run.failure?.stage === 'specification' && VALIDATION_FAILURES.has(run.failure.code)

  return <div className="ia-context-validation">
    <div className="ia-validation-result" role={failedChecks ? 'alert' : undefined}>
      <h3>{demo ? 'Bundled specification · no live validation run' : spec ? 'Python checks passed for the saved specification' : failedChecks ? 'Python checks did not pass' : 'Validation outcome not yet available'}</h3>
      {demo ? <p>This authored example illustrates how prepared context is combined with Caliper’s fixed classifier definitions. Opening the walkthrough does not run Python validation or generate a new specification.</p>
        : spec ? <p>The accepted specification combines the prepared context with {generic ? 'Caliper’s four fixed classifier definitions' : 'the saved historical classifier definitions'}. It is the specification used for this run’s item judgments.</p>
        : failedChecks ? <p>{run.failure!.message}</p>
          : <p>{run.status === 'failed' || run.status === 'cancelled'
            ? 'Preparation stopped before an accepted specification was saved. No failed Python check is reported here; the preparation message describes why the run stopped.'
            : 'Python runs these checks automatically after context preparation. No accepted specification is available yet.'}</p>}
    </div>

    {(generic || !spec) && <section className="ia-context-section" aria-label="Python validation checks">
      <h3>{demo ? 'Checks used in a live run' : spec ? 'What Python checked' : 'What Python checks'}</h3>
      <ul>
        <li><strong>Required structure:</strong> the required fields, four dimension-specific context blocks, permitted values, and unique category identifiers.</li>
        <li><strong>Source references and roles:</strong> cited identifiers exist in the saved source library, and requirements and category definitions cite deployment-requirement sources. Benchmark evidence uses permitted evidence roles.</li>
        <li><strong>Explicit evidence gaps:</strong> partial or unknown category inventories, and dimensions with no extracted requirements, record a gap. Known source-availability gaps are preserved.</li>
        <li><strong>Run consistency:</strong> benchmark and deployment text match the prepared inputs, and the resulting specification uses the prepared dataset profile and source registry.</li>
        <li><strong>Fixed classifier definitions:</strong> Python adds the code-owned questions, decision rules, response requirements, and allowed labels, then validates the assembled specification.</li>
      </ul>
      <p className="ia-small">{demo ? 'These checks describe the live pipeline. This static walkthrough does not produce a validation execution log.' : 'These checks run in Python on the server. This page does not contain a check-by-check execution log.'}</p>
    </section>}
    {spec && !generic && <p className="ia-small">This historical specification was accepted under its original validation rules. It does not provide the current four-dimension source-role validation record.</p>}

    <section className="ia-context-section" aria-label="Validation issues and adjustments">
      <h3>Issues and preparation notes</h3>
      {demo ? <p>No live validation findings were produced by this walkthrough. The bundled preparation note and context gaps remain available for inspection.</p>
        : failedChecks ? <p>The reported issue above blocked specification preparation. No item classification can use this rejected context.</p>
        : spec ? <p>The saved specification was accepted. Earlier repair attempts, if any, are not listed here.</p>
          : <p>No validation findings are available for this run yet.</p>}
      {!!metadata?.adjustments?.length && <><p>Recorded preparation adjustments:</p><ul>{metadata.adjustments.map((adjustment, index) => <li key={index}>{adjustment.reason || adjustment.field || 'A preparation adjustment was recorded.'}</li>)}</ul></>}
      {metadata?.note && <details className="ia-nested"><summary>Saved preparation note</summary><p>{metadata.note}</p></details>}
    </section>

    <div className="ia-validation-boundary">
      <h3>Scientific correctness remains unreviewed</h3>
      <p>Passing these checks does not establish scientific correctness. Python checks structure and source references; it does not determine whether a source supports a generated interpretation, whether stakeholders agree, or whether the benchmark is valid for your deployment.</p>
      <p className="ia-small">Review the source-grounded interpretation in step 2. External human review is a separate activity; this page does not record it as completed.</p>
    </div>

    {spec && <section className="ia-context-section" aria-label="Resulting classifier specification">
      <h3>Resulting classifier specification</h3>
      <p className="ia-small">{generic ? 'The same four definitions apply across benchmarks. The context in step 2 supplies the deployment-specific comparison standards.' : 'Historical definitions are preserved with their original labels.'} Open a dimension to inspect its exact rules and response requirements.</p>
      <div className="ia-criteria-list">{spec.classifiers.map(classifier => <details className="ia-criterion" key={classifier.id}>
        <summary><span><strong>{classifierName(classifier.id)}</strong></span><span className={`ia-tag ${classifier.applicable ? '' : 'ia-tag-muted'}`}>{classifier.applicable ? 'Rules and labels' : 'Not applicable'}</span></summary>
        <div className="ia-criterion-body">
          <p>{classifierQuestion(classifier)}</p>
          {!classifier.applicable && <p>{classifier.na_reason || 'This classifier is not active in the saved specification.'}</p>}
          {!!classifier.decision_rules?.length && <><h4>Decision rules</h4><ul>{classifier.decision_rules.map((rule, index) => <li key={index}>{rule}</li>)}</ul></>}
          <h4>Allowed labels</h4>
          <div className="ia-label-list">{(classifier.labels || classifier.category_set || Object.keys(classifier.ordinal_anchors || {}) || []).map(label => <span key={label}>{labelName(classifier, label)}</span>)}</div>
          {classifier.positive_class && <p className="ia-small">Flagged means: {classifier.positive_class}.</p>}
          {classifier.response_contract && <details className="ia-nested"><summary>Response fields and requirements</summary><SourceValue value={classifier.response_contract} /></details>}
          <details className="ia-nested"><summary>Classifier identifier</summary><code>{classifier.id}</code></details>
        </div>
      </details>)}</div>
      <details className="ia-original"><summary>Specification identifiers and recorded review status</summary>
        <dl className="ia-provenance"><div><dt>Catalog</dt><dd>{spec.fixed_catalog_version || 'Historical catalog'}</dd></div>
          <div><dt>Schema</dt><dd>{spec.schema_version || 'Historical schema'}</dd></div>
          <div><dt>Semantic review status</dt><dd>{spec.semantic_validation || 'Not recorded'}</dd></div></dl>
      </details>
      {onDownload && <button className="ia-text-button" onClick={onDownload}>Download classifier specification JSON</button>}
    </section>}
  </div>
}
