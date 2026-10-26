export function saveBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

/** Open during the click event, then fill the tab with the authenticated report. */
export async function viewReport(load: () => Promise<Blob>): Promise<void> {
  const tab = window.open('about:blank', '_blank')
  if (!tab) throw new Error('Allow a new tab to view the report, or download the HTML report from Individual files.')
  tab.opener = null
  try {
    const blob = await load()
    const url = URL.createObjectURL(blob)
    tab.location.replace(url)
    setTimeout(() => URL.revokeObjectURL(url), 60000)
  } catch (error) {
    tab.close()
    throw error
  }
}
