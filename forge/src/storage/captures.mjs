// The capture cache. IndexedDB, because captures exceed the localStorage quota.
// DB tnr_forge, store captures. Key is `${path}:${idKey}` where idKey is the record id for
// a get, or "" for a list procedure (getAll, getAllNames).
//
// Invalidation rule (spec section 6): any write to an entity drops every capture for that
// entity, both the record's own get and the entity's list captures, because a rename
// changes what getAllNames returns.

export const DB_NAME = "tnr_forge";
export const STORE = "captures";
export const DB_VERSION = 1;

export function captureKey(path, id) { return `${path}:${id ?? ""}`; }

// Which router prefix belongs to which entity. profile.* and ai.* both belong to "ai".
export const ENTITY_OF_PATH = Object.freeze({
  jutsu: "jutsu", item: "item", bloodline: "bloodline", gameAsset: "asset",
  quests: "quest", profile: "ai", ai: "ai",
});

export function entityOfPath(path) {
  const router = String(path).split(".")[0];
  return ENTITY_OF_PATH[router] ?? router;
}

function reqToPromise(req) {
  return new Promise((resolve, reject) => {
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export class CaptureCache {
  /**
   * @param {IDBFactory} idb  window.indexedDB or fake-indexeddb
   * @param {() => number} clock
   */
  constructor(idb, clock = () => Date.now()) {
    if (!idb || typeof idb.open !== "function") throw new Error("CaptureCache needs an IDBFactory");
    this.idb = idb;
    this.clock = clock;
    this._db = null;
  }

  async _open() {
    if (this._db) return this._db;
    if (!this._opening) {
      this._opening = (async () => {
        const req = this.idb.open(DB_NAME, DB_VERSION);
        req.onupgradeneeded = () => {
          const db = req.result;
          if (!db.objectStoreNames.contains(STORE)) {
            const store = db.createObjectStore(STORE, { keyPath: "key" });
            store.createIndex("entity", "entity", { unique: false });
            store.createIndex("path", "path", { unique: false });
          }
        };
        const db = await new Promise((resolve, reject) => {
          req.onsuccess = () => resolve(req.result);
          req.onerror = () => reject(req.error);
          req.onblocked = () => reject(new Error("tnr_forge open blocked by another connection"));
        });
        db.onversionchange = () => { db.close(); if (this._db === db) this._db = null; };
        db.onclose = () => { if (this._db === db) this._db = null; };
        this._db = db;
        return db;
      })().finally(() => { this._opening = null; });
    }
    return this._opening;
  }

  async _tx(mode, fn) {
    let db = await this._open();
    let tx;
    try { tx = db.transaction(STORE, mode); }
    catch (e) { if (e && e.name === "InvalidStateError") { this._db = null; db = await this._open(); tx = db.transaction(STORE, mode); } else throw e; }
    const store = tx.objectStore(STORE);
    const result = await fn(store);
    await new Promise((resolve, reject) => {
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
      tx.onabort = () => reject(tx.error);
    });
    return result;
  }

  /** Store a decoded response. */
  async put({ path, id, input, data }) {
    id = id == null || id === "" ? "" : String(id);
    const rec = {
      key: captureKey(path, id),
      path,
      id: id === "" ? null : id,
      entity: entityOfPath(path),
      input: input ?? null,
      data,
      at: new Date(this.clock()).toISOString(),
      bytes: JSON.stringify(data ?? null).length,
    };
    await this._tx("readwrite", (s) => reqToPromise(s.put(rec)));
    return rec;
  }

  async get(path, id) {
    const rec = await this._tx("readonly", (s) => reqToPromise(s.get(captureKey(path, id))));
    return rec ?? null;
  }

  async has(path, id) { return (await this.get(path, id)) != null; }

  async delete(path, id) {
    await this._tx("readwrite", (s) => reqToPromise(s.delete(captureKey(path, id))));
  }

  /** Drop every capture belonging to an entity type (all paths, all ids). */
  async invalidateEntity(entity) {
    return this._tx("readwrite", async (s) => {
      const idx = s.index("entity");
      const keys = await reqToPromise(idx.getAllKeys(entity));
      for (const k of keys) await reqToPromise(s.delete(k));
      return keys.length;
    });
  }

  /**
   * Drop captures affected by a write to one record: that record's own gets on every path,
   * plus every list capture for the entity (getAll, getAllNames), since lists carry names.
   */
  async invalidateRecord(entity, id) {
    return this._tx("readwrite", async (s) => {
      const idx = s.index("entity");
      const recs = await reqToPromise(idx.getAll(entity));
      let n = 0;
      const want = id == null ? "" : String(id);
      for (const r of recs) {
        if (String(r.id ?? "") === want || r.id === null || r.id === "") { await reqToPromise(s.delete(r.key)); n++; }
      }
      return n;
    });
  }

  async list() {
    const recs = await this._tx("readonly", (s) => reqToPromise(s.getAll()));
    return recs.map(({ key, path, id, entity, at, bytes }) => ({ key, path, id, entity, at, bytes }));
  }

  async size() {
    const recs = await this.list();
    return { count: recs.length, bytes: recs.reduce((a, r) => a + (r.bytes || 0), 0) };
  }

  async clear() { await this._tx("readwrite", (s) => reqToPromise(s.clear())); }

  close() { if (this._db) { this._db.close(); this._db = null; } }
}
