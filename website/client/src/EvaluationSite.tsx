import { App } from './App'
import { ItemReview } from './itemReview/ItemReview'
import { SiteHeader } from './components/SiteHeader'
import { SiteFooter } from './components/SiteFooter'
import { MatrixBackdrop } from './components/MatrixBackdrop'
import { appPath, stripBasePath } from './paths'

export function EvaluationSite() {
  const path = stripBasePath(window.location.pathname).replace(/\/+$/, '') || '/'
  if (path === '/items') return <ItemReview />
  if (path === '/caliper' || path.startsWith('/run/')) return <App />
  return (
    <div className="rd-root">
      <SiteHeader />
      <div className="rd-page-hero evaluation-hero">
        <MatrixBackdrop />
        <header className="rd-container">
          <p className="eyebrow">AIMS · Evaluation tools</p>
          <h1 className="rd-page-title">What would you<br />like to evaluate?</h1>
          <p className="rd-lead">Start with a benchmark you know, or find tests that fit the AI system you want to deploy.</p>
        </header>
      </div>
      <main className="rd-container evaluation-choices">
        <article className="evaluation-choice">
          <p className="eyebrow">01 · Benchmark validity</p>
          <h2>Benchmark Caliper</h2>
          <p>Does an existing benchmark fit your deployment context? Bring a benchmark paper and review its validity across six dimensions.</p>
          <p className="help">Benchmark paper · Deployment questions · Validity report</p>
          <a className="rd-btn rd-btn--primary" href={appPath('/caliper')}>Evaluate a benchmark <span aria-hidden="true">↗</span></a>
          <p className="evaluation-provider">Uses your Anthropic API key. A recorded demo is also available.</p>
        </article>
        <article className="evaluation-choice evaluation-choice-items">
          <p className="eyebrow">02 · Find relevant tests <span className="review-badge">Demo</span></p>
          <h2>Goal-conditioned auditing</h2>
          <p>Which evaluation items fit your AI deployment? Describe the setting and review tests ranked by six-dimensional validity assessments.</p>
          <p className="help">Deployment questions · Item assessment · Ranked tests</p>
          <a className="rd-btn rd-btn--primary" href={appPath('/items')}>Find relevant tests <span aria-hidden="true">↗</span></a>
          <p className="evaluation-provider">Uses your OpenAI API key. First demo: a small measurement-db sample.</p>
        </article>
      </main>
      <section className="rd-container evaluation-note">
        <p>Both workflows use Input / Output × Ontology / Content / Form to examine whether an evaluation fits its intended setting.</p>
      </section>
      <SiteFooter />
    </div>
  )
}
