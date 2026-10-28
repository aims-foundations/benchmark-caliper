import type { ReactNode } from 'react'

export function ItemDetails({ question, children }: { question?: string | null; children: ReactNode }) {
  const preview = (question ?? '').replace(/\s+/g, ' ').trim()
  return <details className="review-item-details">
    <summary>
      Item details
      <span className="review-item-preview">{preview ? preview.length > 180 ? `${preview.slice(0, 180)}…` : preview : 'No separately labeled question'}</span>
    </summary>
    <div className="review-item-body">
      <p className="review-preserve">{question || 'This item has no separately labeled question. Its full source row is available below.'}</p>
      {children}
    </div>
  </details>
}
