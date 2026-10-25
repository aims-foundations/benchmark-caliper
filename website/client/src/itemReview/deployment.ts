import type { Deployment } from './api'

export const QUESTIONS: Array<{ id: keyof Deployment; title: string; hint: string }> = [
  { id: 'task', title: 'What will the AI system do?', hint: 'Describe its task, domain, and the setting where people will use it.' },
  { id: 'users', title: 'Who will use it?', hint: 'Include relevant users, languages, locations, and expertise. Say when a detail is unspecified.' },
  { id: 'inputs', title: 'What inputs will it receive?', hint: 'Describe text, images, audio, tools, and whether users can ask follow-up questions.' },
  { id: 'outputs', title: 'What should its responses look like?', hint: 'Describe the expected language, format, explanation, decision, or other output.' },
  { id: 'success', title: 'What counts as a successful response?', hint: 'What should an evaluation measure: correctness, helpfulness, safe refusal, or other outcomes?' },
  { id: 'constraints', title: 'What constraints or failures matter? (optional)', hint: 'Include situations the system must handle carefully, or capabilities outside its scope.' },
]
