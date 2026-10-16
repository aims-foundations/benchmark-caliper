/** Walkthrough state is isolated from real item-run credentials. */
export const DEMO_ITEM_STORAGE_KEY = 'caliper_demo_mathdial_items_v1'

export function resetDemoItemProgress(): void {
  try { sessionStorage.removeItem(DEMO_ITEM_STORAGE_KEY) } catch { /* The demo still works without storage. */ }
}
