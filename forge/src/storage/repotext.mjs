// Repository text cache — manifest bodies and other repository files Forge has fetched.
//
// This is a SEPARATE IndexedDB database from the capture cache, deliberately.
//
// Repository text is not game capture data: it has a different lifetime, a different eviction
// story, and it is re-fetchable from the repository at any time, whereas a capture snapshot is
// evidence that cannot be recreated once the entity has moved on. Holding it in `tnr_forge` would
// mean bumping that database's version to add a store, and a version bump is a one-way door: an
// operator who rolls back to the previous released bundle would find a database newer than the
// code, and IndexedDB refuses to open it. The journal and the captures they still need would be
// unreachable because of a manifest cache.
//
// So: new database, version 1, nothing in `tnr_forge` touched. A rolled-back bundle never opens
// this database at all, and opens `tnr_forge` at exactly the version it already understands.

export const REPO_DB_NAME = "tnr_forge_repo";
export const REPO_DB_VERSION = 1;
const STORE = "text";

function reqToPromise(req) {
  return new Promise((resolve, reject) => {
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error || new Error("IndexedDB request failed"));
  });
}

export class RepoTextCache {
  constructor(idb, clock = () => Date.now()) {
    this.idb = idb;
    this.clock = clock;
    this._db = null;
  }

  async _open() {
    if (this._db) return this._db;
    this._db = await new Promise((resolve, reject) => {
      const req = this.idb.open(REPO_DB_NAME, REPO_DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE, { keyPath: "key" });
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error || new Error("could not open " + REPO_DB_NAME));
    });
    return this._db;
  }

  async _tx(mode, fn) {
    const db = await this._open();
    const tx = db.transaction(STORE, mode);
    const out = await fn(tx.objectStore(STORE));
    await new Promise((resolve, reject) => {
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error || new Error("repo text transaction failed"));
      tx.onabort = () => reject(tx.error || new Error("repo text transaction aborted"));
    });
    return out;
  }

  /** @param {{path: string, id: string, data: any}} rec */
  async put({ path, id, data }) {
    const key = `${path}\u0000${id}`;
    await this._tx("readwrite", (s) => reqToPromise(s.put({ key, path, id, data, at: this.clock() })));
    return key;
  }

  async get(path, id) {
    const rec = await this._tx("readonly", (s) => reqToPromise(s.get(`${path}\u0000${id}`)));
    return rec ?? null;
  }

  async clear() { await this._tx("readwrite", (s) => reqToPromise(s.clear())); }

  async size() {
    const recs = await this._tx("readonly", (s) => reqToPromise(s.getAll()));
    return { count: recs.length, bytes: recs.reduce((a, r) => a + JSON.stringify(r.data ?? null).length, 0) };
  }
}
