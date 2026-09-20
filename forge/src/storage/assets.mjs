// Verified asset bytes, addressed by CONTENT.
//
// A third IndexedDB database, for the same reason repotext.mjs is a second one: a version bump on
// `tnr_forge` is a one-way door that would make a rolled-back bundle unable to open the journal at
// all. A rolled-back bundle simply never opens this database.
//
// THE KEY IS THE SHA-256 AND NOTHING ELSE. That is the cache-identity property this whole feature
// rests on. A cache keyed by repository path, or by path@ref, or by logical filename, can serve
// bytes that are not the bytes the manifest named: the same path holds different content at
// different commits, and the same logical name meant different files across two manifests. Keyed by
// digest, a hit is either the exact content the manifest asked for or it is not a hit. The path and
// commit that produced the entry ride along as provenance for reporting, and are deliberately NOT
// part of the key, so two manifests binding the same blob share one cached copy.
//
// The digest is re-verified on every read as well as on every fetch (see core/imagepack.mjs). A
// content-addressed store cannot be poisoned by a wrong path, but it can be corrupted, and an entry
// that fails its own key is dropped rather than trusted.

export const ASSET_DB_NAME = "tnr_forge_assets";
export const ASSET_DB_VERSION = 1;
const STORE = "bytes";

// Every upload slug's ceiling is at most 512 KB (transport/upload.mjs SLUGS), so an entry larger
// than this could never be uploaded and is refused before it reaches the store. Bounds the database
// against a manifest that binds something enormous.
export const MAX_ASSET_BYTES = 2 * 1024 * 1024;

// Repo-backed uploads already performed, keyed by CONTENT, so a resumed or re-run job does not
// re-upload bytes the game already holds - and, just as importantly, so a stale idmap entry under a
// logical filename can never stand in for different bytes carrying the same name. The idmap
// (tnr_bk_idmap_v1) is keyed by name and shared with the builder; it is left exactly as it is.
export const ASSET_UPLOADS_KEY = "tnr_forge_asset_uploads_v1";

function reqToPromise(req) {
  return new Promise((resolve, reject) => {
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error || new Error("IndexedDB request failed"));
  });
}

export class AssetCache {
  constructor(idb, clock = () => Date.now()) {
    this.idb = idb;
    this.clock = clock;
    this._db = null;
  }

  async _open() {
    if (this._db) return this._db;
    this._db = await new Promise((resolve, reject) => {
      const req = this.idb.open(ASSET_DB_NAME, ASSET_DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE, { keyPath: "sha256" });
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error || new Error("could not open " + ASSET_DB_NAME));
    });
    return this._db;
  }

  async _tx(mode, fn) {
    const db = await this._open();
    const tx = db.transaction(STORE, mode);
    const out = await fn(tx.objectStore(STORE));
    await new Promise((resolve, reject) => {
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error || new Error("asset transaction failed"));
      tx.onabort = () => reject(tx.error || new Error("asset transaction aborted"));
    });
    return out;
  }

  /**
   * @param {{sha256: string, bytes: ArrayBuffer, path?: string, ref?: string}} rec
   * The caller has already verified that digest(bytes) === sha256; this store does not digest.
   */
  async put({ sha256, bytes, path = null, ref = null }) {
    const size = bytes.byteLength ?? bytes.length ?? 0;
    if (size > MAX_ASSET_BYTES) throw new Error(`asset ${sha256.slice(0, 12)} is ${size} bytes, over the ${MAX_ASSET_BYTES}-byte cache limit`);
    await this._tx("readwrite", (s) => reqToPromise(s.put({ sha256, bytes, size, path, ref, at: this.clock() })));
    return sha256;
  }

  async get(sha256) {
    const rec = await this._tx("readonly", (s) => reqToPromise(s.get(sha256)));
    return rec ?? null;
  }

  async delete(sha256) { await this._tx("readwrite", (s) => reqToPromise(s.delete(sha256))); }

  async clear() { await this._tx("readwrite", (s) => reqToPromise(s.clear())); }

  async size() {
    const recs = await this._tx("readonly", (s) => reqToPromise(s.getAll()));
    return { count: recs.length, bytes: recs.reduce((a, r) => a + (r.size || 0), 0) };
  }
}

function readJson(storage, key) {
  const raw = storage.getItem(key);
  if (raw == null || raw === "") return {};
  let v;
  try { v = JSON.parse(raw); } catch { v = undefined; }
  if (!v || typeof v !== "object" || Array.isArray(v)) return {};
  return v;
}

/** { [sha256]: {url, at, path, ref} } - uploads of repo-backed bytes, keyed by content. */
export function readAssetUploads(storage) { return readJson(storage, ASSET_UPLOADS_KEY); }

export function recordAssetUpload(storage, sha256, url, { path = null, ref = null, at = Date.now() } = {}) {
  const map = readAssetUploads(storage);
  map[sha256] = { url, at, path, ref };
  storage.setItem(ASSET_UPLOADS_KEY, JSON.stringify(map));
  return map;
}
