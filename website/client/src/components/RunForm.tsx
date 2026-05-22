import { useState, type FormEvent } from 'react'
import { fetchDatasetConfigs } from '../api'

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
  // null  → configs not probed yet for the current dataset id
  // []    → probed; 0–1 configs, no choice needed
  // [...] → probed; multiple configs, the user must pick one
  const [configChoices, setConfigChoices] = useState<string[] | null>(null)
  const [checkingConfigs, setCheckingConfigs] = useState(false)

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

  // A new dataset id invalidates any configs we probed for the old one.
  function handleDatasetIdChange(value: string): void {
    setHfDatasetId(value)
    setConfigChoices(null)
    setHfError(null)
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>): Promise<void> {
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

    // A dataset given without a config: make sure the repo isn't
    // multi-config before submitting. Step 5b profiles only one config,
    // so a multi-config repo needs an explicit choice — otherwise it
    // would silently analyze the default (likely wrong) subset.
    if (hfId && !hfCfg) {
      if (configChoices === null) {
        setCheckingConfigs(true)
        let choices: string[] = []
        try {
          const result = await fetchDatasetConfigs(hfId)
          choices = result.configs
        } catch {
          // Detection failed — don't block the run over it.
          choices = []
        }
        setConfigChoices(choices)
        setCheckingConfigs(false)
        if (choices.length > 1) return // show the picker, wait for a choice
      } else if (configChoices.length > 1) {
        setHfError(
          'This dataset has multiple configs — pick the one for this benchmark below.',
        )
        return
      }
    }

    onSubmit(pdfFile, trimmed, optedInFull, hfId || null, hfCfg || null)
  }

  const canSubmit =
    !!pdfFile && description.trim().length > 0 && !checkingConfigs
  const showConfigPicker = !!configChoices && configChoices.length > 1

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
            onChange={(e) => handleDatasetIdChange(e.target.value)}
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
        {showConfigPicker && (
          <div className="hf-config-picker">
            <p className="inline-error">
              <strong>“{hfDatasetId.trim()}”</strong> has{' '}
              {configChoices!.length} configurations. Step 5b profiles only
              one — pick the config that holds this benchmark's data:
            </p>
            <select
              className="hf-config-select"
              value={hfConfig}
              onChange={(e) => setHfConfig(e.target.value)}
            >
              <option value="">— select a config —</option>
              {configChoices!.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        )}
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
          {checkingConfigs ? 'Checking dataset…' : 'Run'}
        </button>
      </div>
    </form>
  )
}
