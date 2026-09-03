// Keys retained from builder_bundle.js as-is (spec section 3). The new app reads and writes
// them with the same shapes so both bundles can be installed side by side.

export const IDMAP_KEY = "tnr_bk_idmap_v1";   // { [srcId]: entityId, [imgName]: url }
export const GH_KEY = "tnr_bk_gh_v1";         // { on: boolean, pat: string }

function readJson(storage, key, fallback) {
  const raw = storage.getItem(key);
  if (raw == null || raw === "") return fallback;
  let v;
  try { v = JSON.parse(raw); } catch { v = undefined; }
  if (!v || typeof v !== "object" || Array.isArray(v)) {
    // never let the next write destroy something unreadable: park it under a sibling key
    try { storage.setItem(key + ".corrupt", raw); } catch { /* best effort */ }
    return fallback;
  }
  return v;
}

export function readIdmap(storage) { return readJson(storage, IDMAP_KEY, {}); }
export function writeIdmap(storage, idmap) { storage.setItem(IDMAP_KEY, JSON.stringify(idmap)); }

export function readGh(storage) { return readJson(storage, GH_KEY, {}); }
export function writeGh(storage, gh) { storage.setItem(GH_KEY, JSON.stringify(gh)); }
