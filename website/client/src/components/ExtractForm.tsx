import { useState, type FormEvent } from 'react'

interface Props {
  onSubmit: (pdfFile: File) => void
  onSkip: () => void
  onChangeKey: () => void
}

/**
 * Re-upload prompt for the extract step. The original PDF was discarded
 * after the elicitation leg (we don't keep user content longer than a
 * single request needs); the user re-uploads the same paper to run the
 * full per-page extraction.
 */
export function ExtractForm({ onSubmit, onSkip, onChangeKey }: Props) {
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [fileError, setFileError] = useState<string | null>(null)

  function handleFile(file: File | null): void {
    setFileError(null)
    if (!file) {
      setPdfFile(null)
      return
    }
    if (
      file.type !== 'application/pdf' &&
      !file.name.toLowerCase().endsWith('.pdf')
    ) {
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
    if (!pdfFile) return
    onSubmit(pdfFile)
  }

  return (
    <form onSubmit={handleSubmit} className="extract-form">
      <h2>Extract the full paper</h2>
      <p className="help">
        We didn't keep the PDF you uploaded earlier — re-upload it now and we'll
        run the full per-page extraction (Step 3a). Each page is processed in
        parallel; for a 30-page paper this typically takes 1–2 minutes.
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

      <div className="actions">
        <button type="button" className="link" onClick={onChangeKey}>
          Change key
        </button>
        <button type="button" className="link" onClick={onSkip}>
          Skip extraction
        </button>
        <button type="submit" disabled={!pdfFile}>
          Extract
        </button>
      </div>
    </form>
  )
}
