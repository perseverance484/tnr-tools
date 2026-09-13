import { validateDraft } from "./schema.mjs";
import { stableStringify } from "./hash.mjs";
const key = "tnr-guide-studio:drafts:v2";
export function saveDraft(storage, draft) {
  const previous = storage.getItem(key),
    all = previous ? JSON.parse(previous) : {};
  all[draft.template.slug] = { savedAt: new Date().toISOString(), draft };
  storage.setItem(key, JSON.stringify(all));
  return true;
}
export function restoreDraft(storage, slug, registry) {
  try {
    const raw = storage.getItem(key);
    if (!raw) return { draft: null };
    const entry = JSON.parse(raw)[slug];
    if (!entry) return { draft: null };
    validateDraft(entry.draft, registry);
    return { ...entry, draft: entry.draft };
  } catch (error) {
    return {
      draft: null,
      error:
        "A saved draft needs recovery. Download the backup before starting again.",
      raw: storage.getItem(key),
    };
  }
}
export function clearDraft(storage, slug) {
  const all = JSON.parse(storage.getItem(key) || "{}");
  delete all[slug];
  storage.setItem(key, JSON.stringify(all));
}
export function draftFingerprint(d) {
  return stableStringify(d);
}
