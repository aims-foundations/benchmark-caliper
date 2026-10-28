import type { FormEvent } from 'react'
import type { SelectionInput } from './api'

export function SelectionForm({ input, busy, onSelect }: {
  input: SelectionInput; busy: boolean; onSelect: () => Promise<boolean>
}) {
  function submit(event: FormEvent) {
    event.preventDefault()
    if (!busy) void onSelect()
  }

  return <form className="review-panel" onSubmit={submit} aria-labelledby="selection-start-title">
    <p className="eyebrow">Step 6: Select a collection</p>
    <h2 id="selection-start-title">Choose up to 30 items in total</h2>
    <p>The collection has one shared limit of 30 items across all tasks. Selection uses items that pass the screening gate, covers every task with at least one item, and checks your explicit coverage requirements.</p>
    <p>Each item’s quality Q is the mean of its input ontology, input content, input form, and output ontology scores. The selector maximizes total Q while respecting the collection limit and available coverage.</p>
    <p>{input.screened} valid assessments · {input.errors} assessment errors · {input.pending} pending items from the initial {input.allocated} allocated items</p>
    {(input.errors > 0 || input.pending > 0) && <p className="selection-notice">Initial screening is incomplete. Selection will use the valid assessments available so far; you can continue screening and select again later. <a href="#initial-screening-continuation">Continue screening in Step 5</a>.</p>}
    <p>If the available items cannot satisfy every requirement, the result identifies the coverage gaps. Selection runs locally, makes no model calls, and needs no API key.</p>
    <button type="submit" disabled={busy}>{busy ? 'Starting…' : 'Select up to 30 items'}</button>
  </form>
}
