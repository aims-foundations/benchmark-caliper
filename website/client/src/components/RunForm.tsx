import { useState, type FormEvent } from 'react'

interface Props {
  onSubmit: (
    pdfFile: File,
    description: string,
    optedInFull: boolean,
  ) => void
  onChangeKey: () => void
}

export function RunForm({ onSubmit, onChangeKey }: Props) {
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [description, setDescription] = useState('')
  // Default OFF — we don't store prompts/responses unless the user opts in
  // for this run. See website/DESIGN.md section 6.
  const [optedInFull, setOptedInFull] = useState(false)
  const [fileError, setFileError] = useState<string | null>(null)

  function handleFile(file: File | null): void {
    setFileError(null)
    if (!file) {
      setPdfFile(null)
      return
    }
    if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
      setFileError('Please choose a PDF file.')
      setPdfFile(null)
      return
    }
    if (file.size > 32 * 1024 * 1024) {
      setFileError('PDF must be 32 MB or smaller.')
      setPdfFile(null)
      return
    }
    setPdfFile(file)
  }

  function handleSubmit(e: FormEvent<HTMLFormElement>): void {
    e.preventDefault()
    const trimmed = description.trim()
    if (!pdfFile || !trimmed) return
    onSubmit(pdfFile, trimmed, optedInFull)
  }

  const canSubmit = !!pdfFile && description.trim().length > 0

  return (
    <form onSubmit={handleSubmit} className="run-form">
      <h2>Describe your deployment</h2>
      <p className="help">
        Upload the benchmark paper as a PDF and describe the deployment context
        where you'd want to use it. Steps 0–2 of the pipeline run on submit;
        you'll see live progress and a few elicitation questions.
      </p>

      <label>
        <span className="label-text">Benchmark paper (PDF)</span>
        <input
          type="file"
          accept="application/pdf,.pdf"
          onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
          required
        />
      </label>
      {fileError && (
        <p role="alert" className="inline-error">
          {fileError}
        </p>
      )}

      <label>
        <span className="label-text">Deployment description</span>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={6}
          maxLength={10_000}
          placeholder="An Indonesian government chatbot answering citizen queries about KTP applications, tax filing, and business registration."
          required
        />
      </label>

      <label className="checkbox">
        <input
          type="checkbox"
          checked={optedInFull}
          onChange={(e) => setOptedInFull(e.target.checked)}
        />
        <span>
          <strong>Optional:</strong> store my prompts and responses for 90 days
          to help debug and improve the pipeline. Off by default. Token counts
          and costs are tracked either way.
        </span>
      </label>

      <div className="actions">
        <button type="button" className="link" onClick={onChangeKey}>
          Change key
        </button>
        <button type="submit" disabled={!canSubmit}>
          Run
        </button>
      </div>
    </form>
  )
}
