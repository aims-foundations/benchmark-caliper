import { App } from './App'
import { ItemReview } from './itemReview/ItemReview'
import { SiteHeader } from './components/SiteHeader'
import { SiteFooter } from './components/SiteFooter'
import { appPath, stripBasePath } from './paths'

export function EvaluationSite() {
  const path = stripBasePath(window.location.pathname).replace(/\/+$/, '') || '/'
  if (path === '/items') return <ItemReview />
  if (path === '/caliper' || path.startsWith('/run/')) return <App />
  return (
    <div className="rd-root evaluation-site">
      <SiteHeader />
      <div className="rd-page-hero evaluation-hero">
        <header className="rd-container evaluation-intro">
          <div>
            <h1 className="rd-page-title">Find the Right Evaluation for Your Context.</h1>
            <p className="rd-lead">The framework characterizes benchmarks and individual test items with respect to the AI system, task, and deployment settings in which they are used.</p>
            <a className="rd-btn evaluation-hero-button" href="https://aimslab.stanford.edu/measurement-db">Explore the Measurement Data Bank</a>
          </div>
          <div className="evaluation-framework" aria-label="Six dimensions of validity">
            <p className="eyebrow">Validity Analysis Framework</p>
            <div className="evaluation-framework-flow">
              <div className="evaluation-framework-endpoint">Deployment Context</div>
              <svg className="evaluation-framework-arrow" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5" /></svg>
              <table className="evaluation-framework-grid" aria-label="Validity analysis framework">
                <colgroup><col className="evaluation-framework-axis" /><col /><col /><col /></colgroup>
                <thead>
                  <tr><td />{['Ontology', 'Content', 'Form'].map(dimension => <th key={dimension} scope="col">{dimension}</th>)}</tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="row"><span>Input</span></th>
                    <td>Test Case<br />Coverage</td>
                    <td>Test Case<br />Relevance</td>
                    <td>Signal<br />Format</td>
                  </tr>
                  <tr>
                    <th scope="row"><span>Label</span></th>
                    <td>Label<br />Taxonomy</td>
                    <td>Label<br />Agreement</td>
                    <td>Output<br />Format</td>
                  </tr>
                </tbody>
              </table>
              <svg className="evaluation-framework-arrow" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5" /></svg>
              <div className="evaluation-framework-endpoint evaluation-framework-assessment">Validity Assessment</div>
            </div>
          </div>
        </header>
      </div>
      <main className="rd-container evaluation-main" id="choose-workflow">
        <div className="evaluation-section-heading"><h2>Research tools</h2><p>Context-specific validity analysis at the benchmark and item levels.</p></div>
        <div className="evaluation-choices">
        <article className="evaluation-choice">
          <h3>Benchmark-level<br />validity analysis</h3>
          <p>Analyze benchmark documentation to assess applicability to a specified AI system, task, and deployment context across six dimensions of validity.</p>
          <dl className="evaluation-outcome"><div><dt>Input</dt><dd>Benchmark paper and deployment context</dd></div><div><dt>Output</dt><dd>Six-dimensional validity assessment</dd></div></dl>
          <a className="evaluation-choice-link" href={appPath('/caliper')}>Analyze a benchmark <span aria-hidden="true">→</span></a>
        </article>
        <article className="evaluation-choice">
          <h3>Goal-conditioned<br />item assessment <span className="review-badge">Demo</span></h3>
          <p>Assess and rank evaluation items from the Measurement Data Bank according to their compatibility with a specified deployment context, with supporting evidence and assessment confidence.</p>
          <dl className="evaluation-outcome"><div><dt>Input</dt><dd>Description of the AI system, task, and deployment context</dd></div><div><dt>Output</dt><dd>Ranked evaluation items with dimension-level assessments</dd></div></dl>
          <a className="evaluation-choice-link" href={appPath('/items')}>Assess evaluation items <span aria-hidden="true">→</span></a>
        </article>
        </div>
      </main>
      <SiteFooter />
    </div>
  )
}
