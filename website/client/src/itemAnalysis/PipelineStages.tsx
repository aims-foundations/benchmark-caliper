import { useEffect, useRef, useState, type ReactNode } from 'react'

export const ITEM_STEPS = [
  'Confirm data and deployment', 'Prepare classifier context', 'Validate context',
  'Classify items', 'Review summary findings', 'Export and human review',
] as const

export function PipelineNavigation({ current, statuses, onNavigate }: {
  current: number; statuses: string[]; onNavigate: (step: number) => void
}) {
  return <nav className="ia-pipeline-navigation" aria-label="Item analysis steps">
    <ol>{ITEM_STEPS.map((title, index) => <li key={title}>
      <a href={`#ia-step-${index + 1}`} aria-current={current === index + 1 ? 'step' : undefined}
        onClick={event => { event.preventDefault(); onNavigate(index + 1) }}>
        <span className="ia-step-number" aria-hidden="true">{index + 1}</span>
        <span><strong>{title}</strong><small>{statuses[index]}</small></span>
      </a>
    </li>)}</ol>
  </nav>
}

export function StageSection({ step, current, status, purpose, input, output, next, children, initiallyOpen = true }: {
  step: number; current: number; status: string; purpose: string; input: ReactNode; output: ReactNode;
  next: ReactNode; children: ReactNode; initiallyOpen?: boolean
}) {
  const [open, setOpen] = useState(initiallyOpen || current === step)
  const previousDefault = useRef(initiallyOpen)
  useEffect(() => {
    if (current === step) setOpen(true)
    else if (previousDefault.current && !initiallyOpen) setOpen(false)
    previousDefault.current = initiallyOpen
  }, [current, step, initiallyOpen])
  return <section id={`ia-step-${step}`} className={`ia-stage${current === step ? ' ia-stage-current' : ''}`}
    aria-labelledby={`ia-step-title-${step}`} tabIndex={-1}>
    <header className="ia-stage-heading"><h2 id={`ia-step-title-${step}`}>
      <span className="ia-step-number">{step}.</span> {ITEM_STEPS[step - 1]}</h2>
      <span className="ia-stage-status">{status}</span>
    </header>
    <p className="ia-stage-purpose">{purpose}</p>
    <dl className="ia-stage-contract"><div><dt>Input</dt><dd>{input}</dd></div><div><dt>Output</dt><dd>{output}</dd></div></dl>
    <details className="ia-stage-content" open={open} onToggle={event => setOpen(event.currentTarget.open)}>
      <summary>{open ? 'Hide step details' : 'Show step details and saved output'}</summary>
      <div>{children}</div>
    </details>
    <div className="ia-stage-next"><strong>Next action</strong><div>{next}</div></div>
  </section>
}
