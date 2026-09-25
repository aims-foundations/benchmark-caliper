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
          </div>
          <div className="evaluation-framework" aria-label="Six dimensions of validity">
            <p className="eyebrow">Six perspectives on evaluation</p>
            <div className="evaluation-framework-grid">
              {['Input', 'Output'].map(side => <div key={side} className="evaluation-framework-row"><strong>{side}</strong>
                {['Ontology', 'Content', 'Form'].map(dimension => <span key={dimension}>{dimension}</span>)}
              </div>)}
            </div>
            <p>The task. The context. The format.<br />Considered on both sides of an interaction.</p>
          </div>
        </header>
      </div>
      <main className="rd-container evaluation-main" id="choose-workflow">
        <div className="evaluation-section-heading"><h2>Where would you like to start?</h2><p>Choose the question you want to answer.</p></div>
        <div className="evaluation-choices">
        <article className="evaluation-choice">
          <div className="evaluation-choice-top"><p className="eyebrow">Benchmark Caliper</p><span aria-hidden="true">01</span></div>
          <h3>I have a benchmark.<br />Does it fit?</h3>
          <p>Bring a benchmark paper and your deployment context. Examine what the benchmark measures and where its conclusions apply.</p>
          <dl className="evaluation-outcome"><div><dt>You bring</dt><dd>A benchmark paper</dd></div><div><dt>You get</dt><dd>A six-dimension validity report</dd></div></dl>
          <a className="rd-btn rd-btn--primary" href={appPath('/caliper')}>Evaluate a benchmark <span aria-hidden="true">↗</span></a>
          <p className="evaluation-provider">Uses your Anthropic API key. A recorded demo is also available.</p>
        </article>
        <article className="evaluation-choice evaluation-choice-items">
          <div className="evaluation-choice-top"><p className="eyebrow">Goal-conditioned auditing <span className="review-badge">Demo</span></p><span aria-hidden="true">02</span></div>
          <h3>I need relevant tests.<br />Where do I look?</h3>
          <p>Describe your AI deployment. Explore individual evaluation items, ranked by compatibility with confidence and evidence you can inspect.</p>
          <dl className="evaluation-outcome"><div><dt>You bring</dt><dd>An AI deployment in mind</dd></div><div><dt>You get</dt><dd>Ranked items with supporting evidence</dd></div></dl>
          <a className="rd-btn rd-btn--primary" href={appPath('/items')}>Find relevant tests <span aria-hidden="true">↗</span></a>
          <p className="evaluation-provider">Uses your OpenAI API key. First demo: a small measurement-db sample.</p>
        </article>
        </div>
      </main>
      <section className="rd-container evaluation-note">
        <p>Built on the six-dimensional validity framework.</p>
        <a href="https://aimslab.stanford.edu/measurement-db">Explore the Measurement Data Bank <span aria-hidden="true">↗</span></a>
      </section>
      <SiteFooter />
    </div>
  )
}
