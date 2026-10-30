import { useId, useRef, useState } from 'react'

const CONTENT_LIMIT = 800

export function ItemContent({ text }: { text?: string | null }) {
  const [expanded, setExpanded] = useState(false)
  const contentId = useId()
  const headingId = useId()
  const section = useRef<HTMLElement>(null)
  const content = text || 'No separately labeled question is recorded. Inspect the full item record below.'
  const long = Boolean(text && text.length > CONTENT_LIMIT)
  const prefix = content.slice(0, CONTENT_LIMIT)
  const boundary = Math.max(prefix.lastIndexOf(' '), prefix.lastIndexOf('\n'), prefix.lastIndexOf('\t'))
  const excerpt = content.slice(0, boundary > CONTENT_LIMIT / 2 ? boundary : CONTENT_LIMIT)

  function toggle() {
    if (expanded && section.current && section.current.getBoundingClientRect().top < 0) {
      section.current.scrollIntoView({ block: 'start' })
    }
    setExpanded(value => !value)
  }

  return <section ref={section} className="construction-item-content" aria-labelledby={headingId}>
    <h4 id={headingId}>Item content</h4>
    <p id={contentId} className="review-preserve">{long && !expanded ? excerpt + '...' : content}</p>
    {long && <button type="button" className="secondary construction-content-toggle" aria-expanded={expanded} aria-controls={contentId} onClick={toggle}>
      {expanded ? 'Show less' : 'Show full content'}
    </button>}
  </section>
}
