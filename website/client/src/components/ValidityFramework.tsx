import './ValidityFramework.css'

// Shared overview for benchmark review and item selection. The output row uses
// terms that also apply to free-form responses, rather than only class labels.
const ROWS = [
  { name: 'Input', cells: ['Task & capability fit', 'Test case relevance', 'Input format'] },
  { name: 'Output', cells: ['Success criteria', 'Reference validity', 'Output format'] },
]

function FlowArrows() {
  return <div className="validity-flow-arrows" aria-hidden="true">
    {[0, 1].map(index => <svg key={index} viewBox="0 0 40 24" focusable="false">
      <path d="M1 12h30M24 5l11 7-11 7" />
    </svg>)}
  </div>
}

export function ValidityFramework() {
  return <figure className="validity-framework" aria-labelledby="validity-framework-title">
    <div className="validity-flow-stack validity-flow-sources">
      <div className="validity-flow-card"><h3>Source evaluation</h3><p>A benchmark or individual test items</p></div>
      <div className="validity-flow-card"><h3>Deployment context</h3><p>The AI system, task, users, and setting</p></div>
    </div>
    <FlowArrows />
    <div className="validity-matrix">
      <h2 id="validity-framework-title">Validity Analysis Framework</h2>
      <table aria-label="Six dimensions of validity">
        <thead><tr><td />{['Ontology', 'Content', 'Form'].map(name => <th key={name} scope="col">{name}</th>)}</tr></thead>
        <tbody>{ROWS.map(row => <tr key={row.name}>
          <th scope="row"><span>{row.name}</span></th>
          {row.cells.map(cell => <td key={cell}>{cell}</td>)}
        </tr>)}</tbody>
      </table>
    </div>
    <FlowArrows />
    <div className="validity-flow-stack validity-flow-outcomes">
      <div className="validity-flow-card"><h3>Validity report</h3><p>Benchmark Caliper</p></div>
      <div className="validity-flow-card"><h3>Ranked test items</h3><p>Goal-conditioned auditing</p></div>
    </div>
    <figcaption>Assess the fit between an evaluation and its intended deployment, across input and output.</figcaption>
  </figure>
}
