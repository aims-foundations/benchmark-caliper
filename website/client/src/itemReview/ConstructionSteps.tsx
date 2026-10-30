import type { ReactNode } from 'react'
import { DIMENSIONS, type SelectionReview } from './api'
import type { ConstructionSnapshot } from './constructionTypes'
import { DeploymentAnswers, RequirementsContent } from './RequirementsResults'
import { GroundingContent } from './GroundingResults'
import { RetrievedItems } from './RetrievedItems'
import { ConstructionStepItems } from './ConstructionStepItems'
import { PIPELINE_STEPS } from './StepSection'
import './ConstructionSteps.css'

type Props = {
  snapshot: ConstructionSnapshot
  step: number
  onStepChange: (step: number) => void
}

const dimensionDescriptions = {
  input_ontology: 'The requested task and type of case fit the deployment scope.',
  input_content: 'The facts are sufficiently complete, coherent, and suitable for the intended users.',
  input_form: 'The language, format, and available inputs fit the deployment requirements.',
  output_ontology: 'The source scoring measures the decision and success behavior the deployment needs.',
  output_content: 'The reference answer or expected judgment is appropriate and supported by the supplied evidence.',
  output_form: 'The requested response format agrees with the source scoring procedure.',
}

function Explanation({ label, children, result = false }: { label: string; children: ReactNode; result?: boolean }) {
  return <section className={`construction-step-explanation${result ? ' construction-step-result' : ''}`}>
    <h3>{label}</h3><div>{children}</div>
  </section>
}

function EvidenceDetails({ title, children }: { title: string; children: ReactNode }) {
  return <details className="construction-step-evidence"><summary>{title}</summary><div>{children}</div></details>
}

function SelectionCoverage({ selection, snapshot }: { selection: SelectionReview['selection']; snapshot: ConstructionSnapshot }) {
  if (!selection) return <p>No selection snapshot was saved for this stage.</p>
  const facets = snapshot.review.requirements?.task_facets ?? []
  return <>
    <div className="construction-table construction-coverage-desktop"><table><caption>Coverage at this stage</caption><thead><tr><th scope="col">Task</th><th scope="col">Minimum</th><th scope="col">Selected</th><th scope="col">Still needed</th></tr></thead><tbody>
      {selection.task_coverage.map(task => <tr key={task.facet_id}><th scope="row"><a href={`#facet-${task.facet_id}`}>{facets.find(facet => facet.facet_id === task.facet_id)?.task.text ?? task.facet_id}</a></th><td>{task.minimum}</td><td>{task.selected_count}</td><td>{task.shortfall}</td></tr>)}
    </tbody></table></div>
    <section className="construction-coverage-mobile" aria-label="Coverage at this stage">
      <p className="construction-coverage-caption">Coverage at this stage</p>
      <ul>{selection.task_coverage.map(task => <li key={task.facet_id}>
        <a className="construction-coverage-task" href={`#facet-${task.facet_id}`}>{facets.find(facet => facet.facet_id === task.facet_id)?.task.text ?? task.facet_id}</a>
        <dl>
          <div><dt>Minimum</dt><dd>{task.minimum}</dd></div>
          <div><dt>Selected</dt><dd>{task.selected_count}</dd></div>
          <div><dt>Still needed</dt><dd>{task.shortfall}</dd></div>
        </dl>
      </li>)}</ul>
    </section>
    {selection.quota_coverage.map(quota => <section key={quota.requirement_index}><h4>Additional requirement {quota.requirement_index + 1}</h4>
      <p>{snapshot.review.requirements?.coverage_requirements[quota.requirement_index]?.requirement.text}</p>
      <p>{quota.selected_count} qualifying items. {quota.minimum_items == null ? 'No numeric minimum was specified.' : `The minimum is ${quota.minimum_items}.`} {quota.shortfall == null ? 'Coverage remains unresolved.' : quota.shortfall > 0 ? `${quota.shortfall} more are needed.` : 'This requirement is met.'}</p>
    </section>)}
  </>
}

export function ConstructionSteps({ snapshot, step, onStepChange }: Props) {
  const { review, items } = snapshot
  const currentStep = Math.min(7, Math.max(1, step))
  const info = PIPELINE_STEPS[currentStep - 1]
  const facets = review.requirements?.task_facets ?? []
  const requirements = review.requirements
  const initial = items.filter(item => item.initial)
  const additional = items.filter(item => !item.initial)
  const initialComplete = initial.filter(item => item.status === 'complete').length
  const initialErrors = initial.filter(item => item.status === 'error').length
  const initialPassed = initial.filter(item => item.gate === 'pass').length
  const initialFailed = initial.filter(item => item.gate === 'fail').length
  const initialUnresolved = initial.filter(item => item.status === 'complete' && item.gate !== 'pass' && item.gate !== 'fail').length
  const allocation = review.screening?.allocation
  const allocated = allocation?.allocated ?? initial.length
  const adaptive = review.adaptive
  const initialSelection = adaptive?.initial_selection ?? null
  const finalSelection = review.selection
  const completedBatches = adaptive?.batches.filter(batch => batch.kind === 'adaptive' && batch.status === 'committed') ?? []
  const adoptedMappings = review.grounding?.facets.flatMap(facet => facet.mapping?.records.filter(record => record.applicability !== 'not_applicable') ?? []) ?? []
  const distinctOnetRecords = new Set(adoptedMappings.map(record => record.record_id)).size
  const minimumScore = review.screening?.policy.minimum_score ?? 3
  const gatedDimensions = review.screening?.policy.gated_dimensions ?? ['input_ontology', 'input_content', 'input_form', 'output_ontology']
  const taskName = (id: string) => facets.find(facet => facet.facet_id === id)?.task.text ?? id
  const allocatedEqually = allocation && allocation.allocations.length > 0 && new Set(allocation.allocations.map(item => item.allocated)).size === 1
  const stoppingExplanation = adaptive?.stop_reason === 'candidate_limit'
    ? `Construction stopped at the limit of ${adaptive.settings.candidate_limit} assessed candidates, including the initial ${allocated}.`
    : adaptive?.stop_reason === 'queues_exhausted'
      ? 'Construction stopped because no unseen candidates remained in the saved queues.'
      : adaptive?.stop_reason === 'cost_limit'
        ? 'Construction stopped at the configured cost limit.'
        : review.message

  return <section className="construction-process" aria-labelledby="construction-process-title">
    <header className="construction-process-intro"><h2 id="construction-process-title">How this collection was built</h2>
      <p>Follow the results from the original answers to the final collection. Open Step overview for an explanation of each stage.</p>
    </header>
    <div className="construction-process-layout">
      <nav className="construction-step-nav" aria-label="Construction steps">
        <ol>{PIPELINE_STEPS.map(stage => <li key={stage.number}><button type="button" aria-label={`Step ${stage.number}: ${stage.name}`} aria-current={stage.number === currentStep ? 'step' : undefined} onClick={() => onStepChange(stage.number)}>
          <span className="construction-step-number" aria-hidden="true">{stage.number}</span><span><span className="construction-step-nav-label">Step {stage.number}</span>{stage.name}</span>
        </button></li>)}</ol>
      </nav>
      <article className="construction-step-panel" id={`construction-step-${currentStep}`} aria-labelledby={`construction-step-${currentStep}-title`}>
        <header><h2 id={`construction-step-${currentStep}-title`}>Step {currentStep}: {info.name}</h2></header>

        {currentStep === 1 && <>
          <EvidenceDetails title="Step overview">
            <Explanation label="What it received"><p>Six answers describing the intended task, users, inputs, outputs, success criteria, and constraints.</p></Explanation>
            <Explanation label="What happened"><p>The pipeline saved the original answers as the basis for the requirements, search queries, and screening decisions.</p></Explanation>
            <Explanation label="What happened next"><p>Step 2 translated these answers into structured tasks and requirements.</p></Explanation>
          </EvidenceDetails>
          <DeploymentAnswers deployment={review.deployment} />
        </>}

        {currentStep === 2 && <>
          <EvidenceDetails title="Step overview">
            <Explanation label="What it received"><p>The six original deployment answers from Step 1.</p></Explanation>
            <Explanation label="What happened"><p>{review.extraction?.model ?? review.model} extracted the requested tasks, expected inputs and outputs, and collection coverage requirements. Supporting quotations link the extracted requirements to the original answers.</p></Explanation>
            <Explanation label="What happened next"><p>Step 3 used the extracted tasks to find related O*NET descriptions and useful search wording.</p></Explanation>
          </EvidenceDetails>
          <Explanation label="Extracted requirements" result>
            {requirements ? <><p><strong>{facets.length} requested tasks</strong>, {requirements.coverage_requirements.length} additional coverage {requirements.coverage_requirements.length === 1 ? 'requirement' : 'requirements'}, and {requirements.unresolved_details.length} unresolved {requirements.unresolved_details.length === 1 ? 'detail' : 'details'}.</p>
            </> : <p>No extracted requirements are available in this saved record.</p>}
          </Explanation>
          <div className="construction-primary-results"><RequirementsContent requirements={requirements} /></div>
          <EvidenceDetails title="Inspect extraction settings and prompt"><pre>{JSON.stringify(review.extraction, null, 2)}</pre></EvidenceDetails>
        </>}

        {currentStep === 3 && <>
          <EvidenceDetails title="Step overview">
            <Explanation label="What it received"><p>The {facets.length} extracted tasks and their deployment requirements.</p></Explanation>
            <Explanation label="What happened"><p>The pipeline searched O*NET descriptions of occupations and work activities. {review.grounding?.mapping.model ?? review.model} chose relevant passages, recorded how they apply to the deployment, and proposed related search terms.</p></Explanation>
            <Explanation label="What happened next"><p>Step 4 combined the task requirements and adopted search terms into one benchmark search query per task.</p></Explanation>
          </EvidenceDetails>
          <Explanation label="Grounding results" result><p><strong>{distinctOnetRecords} distinct O*NET records</strong> supplied search wording across the task mappings.</p>
            <ul>{review.grounding?.facets.map(facet => <li key={facet.facet_id}>{taskName(facet.facet_id)}{' '}
              <strong>{facet.mapping?.records.filter(record => record.applicability !== 'not_applicable').length ?? 0} adopted records.</strong>{facet.status === 'error' && ' This mapping has an error.'}
            </li>)}</ul>
            {adoptedMappings.length > 0 && adoptedMappings.every(record => record.applicability === 'partially_applicable') && <p>All adopted records were marked partially applicable. Their search wording supplements the deployment answers; it does not replace the original requirements.</p>}
          </Explanation>
          <div className="construction-primary-results"><GroundingContent review={review} /></div>
        </>}

        {currentStep === 4 && <>
          <EvidenceDetails title="Step overview">
            <Explanation label="What it received"><p>One search query per task, using the requirements and the search wording from Step 3.</p></Explanation>
            <Explanation label="What happened"><p>BGE searched for similar meaning and BM25 searched for matching words across the item bank. The pipeline merged their rankings and organized candidates into task queues and source benchmark queues.</p>
            {review.retrieval && <p>The search covered {review.retrieval.scope.table_count.toLocaleString()} benchmark collections containing {review.retrieval.scope.source_rows.toLocaleString()} source rows.</p>}
          </Explanation>
            <Explanation label="What happened next"><p>Step 5 took {allocated} distinct candidates from these rankings for the initial screening. Remaining candidates stayed available for Step 7.</p></Explanation>
          </EvidenceDetails>
          <Explanation label="Retrieval results" result>
            <div className="construction-table"><table><caption>Retrieved candidates by task</caption><thead><tr><th scope="col">Task</th><th scope="col">Candidates</th></tr></thead><tbody>{review.retrieval?.queries.map(query => <tr key={query.facet_id}><th scope="row">{taskName(query.facet_id)}</th><td>{query.candidate_count?.toLocaleString() ?? 'Not recorded'}</td></tr>)}</tbody></table></div>
            <p><strong>These task lists overlap.</strong> A candidate can appear in several queues. The counts cannot be added to obtain a distinct item total, and retrieval alone does not establish eligibility.</p>
          </Explanation>
          <RetrievedItems snapshot={snapshot} />
          <section className="construction-primary-results construction-search-queries"><h3>Search queries</h3>{review.retrieval?.queries.map((query, index) => <section key={query.facet_id}><h4>Task {index + 1}: {taskName(query.facet_id)}</h4><p className="review-preserve">{query.query}</p></section>)}</section>
          <EvidenceDetails title="Inspect retrieval settings, bank snapshot, and saved queues"><pre>{JSON.stringify(review.retrieval, null, 2)}</pre></EvidenceDetails>
        </>}

        {currentStep === 5 && <>
          <EvidenceDetails title="Step overview">
            <Explanation label="What it received"><p><strong>{allocated} distinct candidates</strong> from the task rankings.{allocatedEqually ? ` The allocation was ${allocation.allocations[0].allocated} from each of ${allocation.allocations.length} tasks.` : ' The allocation across tasks is recorded below.'}</p></Explanation>
            <Explanation label="What happened"><p>{review.screening?.model.model ?? review.model} identified the decision each question actually requests and rated six dimensions of fit to the deployment. The eligibility rule required a task match and a score of at least {minimumScore} on each of the {gatedDimensions.length} required dimensions.</p></Explanation>
            <Explanation label="Eligibility conditions"><p>An item must request one of the deployment tasks and score at least {minimumScore} out of 5 on every required dimension:</p>
            <ul>{DIMENSIONS.filter(([key]) => gatedDimensions.includes(key)).map(([key, label]) => <li key={key}><strong>{label}:</strong> {dimensionDescriptions[key]}</li>)}</ul>
            <p>A higher score on another dimension cannot compensate for a score below the threshold. Unknown required scores cannot establish eligibility. The other rated dimensions are reported separately.</p>
            <p>Collection coverage requirements are checked separately during selection. Each item does not have to satisfy every coverage requirement.</p>
          </Explanation>
            <Explanation label="What happened next"><p>Step 6 received these assessments and considered only the {initialPassed} eligible items for the initial collection.</p></Explanation>
          </EvidenceDetails>
          <Explanation label="Screening results" result>
            <dl className="construction-step-counts"><div><dt>Valid assessments</dt><dd>{initialComplete}</dd></div><div><dt>Eligible items</dt><dd>{initialPassed}</dd></div><div><dt>Failed eligibility</dt><dd>{initialFailed}</dd></div><div><dt>Assessment errors</dt><dd>{initialErrors}</dd></div></dl>
            {initialUnresolved > 0 && <p>{initialUnresolved} eligibility decisions remain unresolved.</p>}
            {allocated > initial.length && <p>{allocated - initial.length} allocated items have no assessment record.</p>}
            <p>{initialPassed === 0 ? 'No assessed item met all the eligibility conditions.' : `${initialPassed} assessed items met all the eligibility conditions.`}{initialErrors === 0 && initialFailed > 0 ? ' A failed eligibility decision is a completed assessment, not a processing error.' : ''}</p>
          </Explanation>
          {allocation && allocation.allocations.length > 0 && <div className="construction-table"><table><caption>Initial candidates by task</caption><thead><tr><th scope="col">Task</th><th scope="col">Allocated items</th></tr></thead><tbody>{allocation.allocations.map(task => <tr key={task.queue_id}><th scope="row">{taskName(task.facet_id)}</th><td>{task.allocated}</td></tr>)}</tbody></table></div>}
          <ConstructionStepItems snapshot={snapshot} step={5} />
          <EvidenceDetails title="Inspect initial allocation, screening prompt, and settings"><pre>{JSON.stringify({ allocation, policy: review.screening?.policy, model: review.screening?.model }, null, 2)}</pre></EvidenceDetails>
        </>}

        {currentStep === 6 && <>
          <EvidenceDetails title="Step overview">
            <Explanation label="What it received"><p>The {initialComplete} valid assessments from the first {allocated} candidates, including {initialPassed} eligible items.</p></Explanation>
            <Explanation label="What happened"><p>The selector considered only items that passed screening. It sought a collection of up to {initialSelection?.limit ?? finalSelection?.limit ?? 30} items in total, covering the required tasks and additional requirements while preferring higher ratings. It did not lower the eligibility thresholds to fill a gap.</p></Explanation>
            <Explanation label="Selection quality"><p>Quality Q is the mean of the four required dimension scores for an item. The selector uses the recorded ratings; it does not make another model assessment.</p></Explanation>
            <Explanation label="What happened next"><p>Step 7 screened more candidates and repeated this selection process after each batch. The final collection therefore reflects more evidence than this initial selection.</p></Explanation>
          </EvidenceDetails>
          <Explanation label="Initial selection" result>
            <p>After the first {allocated} assessments:</p>
            {initialSelection ? <><p className="construction-step-outcome">{initialSelection.selected_count} {initialSelection.selected_count === 1 ? 'item was' : 'items were'} selected at this stage.</p>
              {initialSelection.selected_count === 0 && initialPassed === 0 && <p>There were no eligible items to select. The initial collection was empty, and the coverage gaps remained recorded.</p>}
              {initialSelection.selected_count > 0 && <p>{initialSelection.fully_satisfied ? 'All recorded coverage requirements were met at this stage.' : 'Some coverage requirements remained unmet at this stage.'}</p>}
              {initialSelection.selected_count > 0 && <p>Total quality Q: {initialSelection.total_quality.toFixed(2)}. Average Q: {(initialSelection.total_quality / initialSelection.selected_count).toFixed(2)} / 5.</p>}
            </> : <p>The initial selection snapshot is not available in this saved record.</p>}
          </Explanation>
          <section className="construction-primary-results"><h3>Initial coverage findings</h3><SelectionCoverage selection={initialSelection} snapshot={snapshot} /></section>
          <ConstructionStepItems snapshot={snapshot} step={6} />
          <EvidenceDetails title="Inspect the initial selection record"><pre>{JSON.stringify(initialSelection, null, 2)}</pre></EvidenceDetails>
        </>}

        {currentStep === 7 && <>
          <EvidenceDetails title="Step overview">
            <Explanation label="What it received"><p>The saved candidate queues from Step 4, the first {allocated} assessments, and the initial collection from Step 6.</p></Explanation>
            <Explanation label="What happened"><p>The policy chose a task or source benchmark queue using previous selection success and remaining coverage gaps, with some exploration of other queues. It took up to {adaptive?.settings.batch_size ?? 8} unseen candidates at a time and screened them using the same eligibility rules.</p><p>After each batch, selection ran again over all eligible items assessed so far. This stage reused the saved retrieval queues and skipped items already assessed in any queue.</p></Explanation>
            <Explanation label="What happens next"><p>{adaptive?.frozen ? 'The final collection is frozen for review.' : 'The current collection is saved for review.'} The saved record retains the selected items, assessments, and remaining coverage findings.</p></Explanation>
          </EvidenceDetails>
          <Explanation label="Adaptive screening results" result>
            <dl className="construction-step-counts"><div><dt>Additional candidates assessed</dt><dd>{additional.length}</dd></div><div><dt>Completed adaptive batches</dt><dd>{completedBatches.length}</dd></div><div><dt>Total candidates assessed</dt><dd>{items.length}</dd></div><div><dt>Final selected items</dt><dd>{finalSelection?.selected_count ?? snapshot.entry.selected_count}</dd></div></dl>
            <p><strong>{allocated} initial candidates + {additional.length} additional candidates = {items.length} assessed in total.</strong> The final selected items are a subset of these assessed candidates.</p>
            <p>{stoppingExplanation}</p>
            {finalSelection && <p>{finalSelection.fully_satisfied ? 'All recorded coverage requirements were met.' : 'Coverage remained incomplete. Stopping did not lower the original requirements.'}</p>}
            {finalSelection && finalSelection.selected_count > 0 && <p>Total quality Q: {finalSelection.total_quality.toFixed(2)}. Average Q: {(finalSelection.total_quality / finalSelection.selected_count).toFixed(2)} / 5.</p>}
          </Explanation>
          <section className="construction-primary-results"><h3>Final coverage findings</h3><SelectionCoverage selection={finalSelection} snapshot={snapshot} /></section>
          <ConstructionStepItems snapshot={snapshot} step={7} />
          <EvidenceDetails title="Inspect the final selection record"><pre>{JSON.stringify(finalSelection, null, 2)}</pre></EvidenceDetails>
          <EvidenceDetails title={`Inspect the ${adaptive?.batches.length ?? 0} screening batch records`}>
            <div className="construction-table"><table><caption>Screening and selection by batch</caption><thead><tr><th scope="col">Batch</th><th scope="col">Candidates acquired</th><th scope="col">Selected after batch</th></tr></thead><tbody>{adaptive?.batches.map(batch => <tr key={batch.number}><th scope="row">{batch.kind === 'initial' ? 'Initial screening' : `Adaptive batch ${batch.number}`}{batch.status === 'pending' && ' (pending)'}</th><td>{batch.item_ids.length}</td><td>{batch.selected_item_ids.length}</td></tr>)}</tbody></table></div>
          </EvidenceDetails>
          <EvidenceDetails title="Inspect adaptive settings, queue statistics, and full batch records"><pre>{JSON.stringify({ settings: adaptive?.settings, policy: adaptive?.policy, queue_statistics: adaptive?.queue_statistics, batches: adaptive?.batches }, null, 2)}</pre></EvidenceDetails>
        </>}

        <nav className="construction-step-pagination" aria-label="Move through construction steps"><button type="button" className="secondary" disabled={currentStep === 1} onClick={() => onStepChange(currentStep - 1)}>Previous step</button><span>Step {currentStep} of 7</span><button type="button" className="secondary" disabled={currentStep === 7} onClick={() => onStepChange(currentStep + 1)}>Next step</button></nav>
      </article>
    </div>
  </section>
}
