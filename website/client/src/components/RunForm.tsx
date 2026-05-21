import { useState, type FormEvent } from 'react'

interface Props {
  onSubmit: (
    pdfFile: File,
    description: string,
    optedInFull: boolean,
    hfDatasetId: string | null,
    hfConfig: string | null,
  ) => void
  onChangeKey: () => void
}

// Loose shape check for `org/dataset` (HF requires non-empty namespace and
// name; we don't validate against the live registry). Empty string is fine
// — that just means the user is opting out of dataset analysis.
const HF_ID_RE = /^[A-Za-z0-9._-]+\/[A-Za-z0-9._-]+$/

export function RunForm({ onSubmit, onChangeKey }: Props) {
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [description, setDescription] = useState('')
  // Default OFF — we don't store prompts/responses unless the user opts in
  // for this run. See website/DESIGN.md section 6.
  const [optedInFull, setOptedInFull] = useState(false)
  const [hfDatasetId, setHfDatasetId] = useState('')
  const [hfConfig, setHfConfig] = useState('')
  const [fileError, setFileError] = useState<string | null>(null)
  const [hfError, setHfError] = useState<string | null>(null)

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
    const hfId = hfDatasetId.trim()
    const hfCfg = hfConfig.trim()
    if (!pdfFile || !trimmed) return
    if (hfId && !HF_ID_RE.test(hfId)) {
      setHfError('HF dataset ID must look like "org/dataset".')
      return
    }
    setHfError(null)
    onSubmit(
      pdfFile,
      trimmed,
      optedInFull,
      hfId || null,
      hfCfg || null,
    )
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

      <fieldset className="hf-details">
        <legend>
          <strong>Optional:</strong> HuggingFace dataset for this benchmark
        </legend>
        <p className="help">
          If the benchmark's data is published on HuggingFace and you know
          the dataset ID, paste it here. The pipeline will profile a sample
          of the actual data and include those findings in the validity
          scoring (Step 5b). Leave blank to skip — scoring still runs.
        </p>
        <label>
          <span className="label-text">HF dataset ID (e.g. org/dataset)</span>
          <input
            type="text"
            value={hfDatasetId}
            onChange={(e) => setHfDatasetId(e.target.value)}
            placeholder="eth-nlped/mathdial"
            maxLength={200}
            autoComplete="off"
            spellCheck={false}
          />
        </label>
        <label>
          <span className="label-text">HF config</span>
          <input
            type="text"
            value={hfConfig}
            onChange={(e) => setHfConfig(e.target.value)}
            placeholder="default"
            maxLength={100}
            autoComplete="off"
            spellCheck={false}
          />
        </label>
        {hfError && (
          <p role="alert" className="inline-error">
            {hfError}
          </p>
        )}
      </fieldset>

      <label className="checkbox">
        <input
          type="checkbox"
          checked={optedInFull}
          onChange={(e) => setOptedInFull(e.target.checked)}
        />
        <span>
          <strong>Optional:</strong> store my prompts and responses for 90 days
          to help debug and improve the pipeline.
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
