import { useEffect, useRef, useState, type ReactNode } from 'react'

export const PIPELINE_STEPS = [
  { number: 1, mode: 'deployment', name: 'Deployment goal', description: 'Your original six answers describe the deployment this benchmark should support.' },
  { number: 2, mode: 'requirements', name: 'Extract requirements', description: 'Identify tasks, required inputs and outputs, and coverage requirements from your answers.' },
  { number: 3, mode: 'grounding', name: 'O*NET grounding', description: 'Connect extracted tasks to supporting O*NET records and search vocabulary.' },
  { number: 4, mode: 'retrieval', name: 'Retrieve benchmark items', description: 'Find relevant benchmark candidates and organize them into task queues.' },
  { number: 5, mode: 'screening', name: 'Initial screening', description: 'Assess the initial candidates and record their task matches, validity ratings, and eligibility.' },
  { number: 6, mode: 'selection', name: 'Initial collection selection', description: 'Select eligible items while meeting task and coverage requirements.' },
  { number: 7, mode: 'adaptive', name: 'Adaptive screening', description: 'Screen additional candidates, update the collection, and record why construction stopped.' },
] as const

export type StepNumber = typeof PIPELINE_STEPS[number]['number']

export function stepNumber(mode: string): StepNumber {
  return PIPELINE_STEPS.find(step => step.mode === mode)?.number ?? 1
}

export function StepSection({ step, current = false, status = 'Saved results', summary, children }: {
  step: StepNumber; current?: boolean; status?: string; summary?: string; children: ReactNode
}) {
  const [expanded, setExpanded] = useState(true)
  const section = useRef<HTMLElement>(null)
  const info = PIPELINE_STEPS[step - 1]
  const id = `pipeline-step-${step}`

  useEffect(() => {
    let frame: number | undefined
    function reveal(hash: string) {
      let targetId: string
      try { targetId = decodeURIComponent(hash.slice(1)) } catch { return }
      const target = document.getElementById(targetId)
      if (!target || !section.current?.contains(target)) return
      setExpanded(true)
      // Evidence links keep working when their containing step is collapsed.
      frame = requestAnimationFrame(() => target.scrollIntoView?.({ block: 'start' }))
    }
    function followLink(event: MouseEvent) {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return
      const link = event.target instanceof Element ? event.target.closest('a[href^="#"]') : null
      if (link) reveal(link.getAttribute('href') || '')
    }
    const followHash = () => reveal(window.location.hash)
    document.addEventListener('click', followLink)
    window.addEventListener('hashchange', followHash)
    followHash()
    return () => {
      document.removeEventListener('click', followLink)
      window.removeEventListener('hashchange', followHash)
      if (frame != null) cancelAnimationFrame(frame)
    }
  }, [])

  return <section ref={section} id={id} className={`pipeline-step${current ? ' pipeline-step-current' : ''}`} aria-labelledby={`${id}-title`}>
    <header className="pipeline-step-header">
      <div className="pipeline-step-heading">
        <div><p className="eyebrow">{current ? 'Current step' : 'Previous step'}</p>
          <h2 id={`${id}-title`}>Step {step}: {info.name}</h2></div>
        <span className="pipeline-step-status">{status}</span>
      </div>
      <p className="pipeline-step-description">{info.description}</p>
      <div className="pipeline-step-tools">
        {summary && <p>{summary}</p>}
        <button type="button" className="secondary" aria-expanded={expanded} aria-controls={`${id}-content`}
          onClick={() => setExpanded(value => !value)}>{expanded ? 'Collapse' : 'Expand'} Step {step}</button>
      </div>
    </header>
    <div id={`${id}-content`} className="pipeline-step-content" hidden={!expanded}>{children}</div>
  </section>
}
