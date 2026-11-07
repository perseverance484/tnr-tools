// IndexedDB that survives the process, for the game-connection host.
//
// In the browser, Forge's capture cache and its immutable capture snapshots live in the tab's
// IndexedDB, which outlives a crash of the page. On this host Node has no IndexedDB, and an
// in-memory fake-indexeddb loses every snapshot when the process dies: a job resumed after a
// crash then exports its full captures as "snapshot is gone" (results.mjs materialize), because
// it will never re-read them. That is the gap this file closes.
//
// HOW: a real fake-indexeddb does the work, and a mirror of every database is kept on disk in one
// file (v8 structured serialization, so Dates and binary survive). Every readwrite transaction
// records the puts, deletes and clears it makes; when the transaction COMMITS, the ops are applied
// to the mirror and the file is rewritten atomically, inside the "complete" dispatch and before
// the caller's own oncomplete runs. So by the time any Forge code learns that a snapshot was
// stored, it is on disk. An aborted transaction changes nothing, as in IndexedDB.
//
// On start the file is replayed into a fresh fake-indexeddb, schemas (keyPath, indexes) included,
// so the caches open the same databases at the same versions they left.
//
// Scope: the operations Forge's caches use (put, add, delete by key or key range, clear) on
// object stores. Anything written inside a versionchange (upgrade) transaction is not mirrored;
// Forge only creates stores and indexes there. A damaged mirror file is an error, never an empty
// cache: losing evidence silently is the failure this exists to prevent.

import { existsSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { serialize, deserialize } from "node:v8";
import { IDBFactory } from "fake-indexeddb";

const WRAPPED = Symbol("forge.idbfile.wrapped");
const clone = (v) => deserialize(serialize(v));

function keyId(k) {
  if (typeof k === "string") return "s" + k;
  if (typeof k === "number") return "n" + k;
  return "x" + serialize(k).toString("base64");
}

function writeAtomic(path, buf) {
  const tmp = path + ".tmp-" + process.pid;
  writeFileSync(tmp, buf);
  renameSync(tmp, path);
}

function readSchema(db, mirrorDb) {
  const names = Array.from(db.objectStoreNames);
  for (const n of Object.keys(mirrorDb.stores)) if (!names.includes(n)) delete mirrorDb.stores[n];
  if (!names.length) return;
  const tx = db.transaction(names, "readonly");
  for (const n of names) {
    const os = tx.objectStore(n);
    const schema = {
      keyPath: os.keyPath, autoIncrement: os.autoIncrement,
      indexes: Array.from(os.indexNames).map((i) => { const ix = os.index(i); return { name: i, keyPath: ix.keyPath, unique: ix.unique, multiEntry: ix.multiEntry }; }),
    };
    const prev = mirrorDb.stores[n];
    mirrorDb.stores[n] = { ...schema, records: prev ? prev.records : new Map() };
  }
}

export class FileIDB {
  /** Use FileIDB.open(path): the replay is asynchronous. */
  constructor(path) {
    this.path = path;
    this.real = new IDBFactory();
    this.mirror = { format: 1, dbs: {} };
    if (existsSync(path)) {
      let m;
      try { m = deserialize(readFileSync(path)); }
      catch (e) { throw new Error(`the capture store ${path} could not be read (${e.message}); refusing to start with an empty one`); }
      if (!m || m.format !== 1 || typeof m.dbs !== "object") throw new Error(`the capture store ${path} is not a Forge mirror file`);
      this.mirror = m;
    }
    // What Forge's caches are handed: an IDBFactory whose connections are mirrored.
    this.factory = {
      open: (name, version) => this._open(name, version),
      deleteDatabase: (name) => {
        const req = this.real.deleteDatabase(name);
        req.addEventListener("success", () => { delete this.mirror.dbs[name]; this._flush(); });
        return req;
      },
      cmp: (a, b) => this.real.cmp(a, b),
      databases: () => this.real.databases(),
    };
  }

  static async open(path) {
    const f = new FileIDB(path);
    await f._replay();
    return f;
  }

  /** Bytes of the mirror file, for diagnostics. */
  size() { return existsSync(this.path) ? readFileSync(this.path).length : 0; }

  async _replay() {
    for (const [name, mdb] of Object.entries(this.mirror.dbs)) {
      const req = this.real.open(name, mdb.version);
      req.onupgradeneeded = () => {
        const db = req.result;
        for (const [sn, s] of Object.entries(mdb.stores)) {
          const os = db.createObjectStore(sn, { keyPath: s.keyPath ?? undefined, autoIncrement: !!s.autoIncrement });
          for (const ix of s.indexes) os.createIndex(ix.name, ix.keyPath, { unique: ix.unique, multiEntry: ix.multiEntry });
        }
      };
      const db = await new Promise((resolve, reject) => { req.onsuccess = () => resolve(req.result); req.onerror = () => reject(req.error); });
      const stores = Object.keys(mdb.stores);
      if (stores.length) {
        const tx = db.transaction(stores, "readwrite");
        for (const sn of stores) {
          const os = tx.objectStore(sn);
          const inline = mdb.stores[sn].keyPath != null;
          for (const [key, value] of mdb.stores[sn].records.values()) inline ? os.put(value) : os.put(value, key);
        }
        await new Promise((resolve, reject) => { tx.oncomplete = () => resolve(); tx.onerror = () => reject(tx.error); tx.onabort = () => reject(tx.error); });
      }
      db.close();
    }
  }

  _open(name, version) {
    const req = version === undefined ? this.real.open(name) : this.real.open(name, version);
    // Registered before the caller's onsuccess, so the connection is mirrored before Forge sees it.
    req.addEventListener("success", () => this._adopt(name, req.result));
    return req;
  }

  _adopt(name, db) {
    const mdb = this.mirror.dbs[name] ?? (this.mirror.dbs[name] = { version: db.version, stores: {} });
    mdb.version = db.version;
    readSchema(db, mdb);
    this._flush();
    const transaction = db.transaction.bind(db);
    db.transaction = (names, mode, opts) => {
      const tx = transaction(names, mode, opts);
      if (mode === "readwrite") this._watch(name, tx);
      return tx;
    };
  }

  _watch(dbName, tx) {
    const ops = [];
    const objectStore = tx.objectStore.bind(tx);
    tx.objectStore = (sn) => this._wrapStore(objectStore(sn), sn, ops);
    tx.addEventListener("complete", () => {
      const mdb = this.mirror.dbs[dbName];
      for (const [sn, op, key, value] of ops) {
        const recs = mdb.stores[sn].records;
        if (op === "put") recs.set(keyId(key), [key, value]);
        else if (op === "delete") recs.delete(keyId(key));
        else if (op === "deleteRange") { for (const [id, [k]] of recs) if (key.includes(k)) recs.delete(id); }
        else if (op === "clear") recs.clear();
      }
      if (ops.length) this._flush();
    });
  }

  _wrapStore(os, sn, ops) {
    if (os[WRAPPED]) return os;
    const put = os.put.bind(os), add = os.add.bind(os), del = os.delete.bind(os), clear = os.clear.bind(os);
    const record = (req, entry) => { req.addEventListener("success", () => ops.push(entry(req))); return req; };
    os.put = (value, key) => { const v = clone(value); return record(key === undefined ? put(value) : put(value, key), (r) => [sn, "put", r.result, v]); };
    os.add = (value, key) => { const v = clone(value); return record(key === undefined ? add(value) : add(value, key), (r) => [sn, "put", r.result, v]); };
    os.delete = (key) => {
      const range = key && typeof key === "object" && typeof key.includes === "function";
      return record(del(key), () => [sn, range ? "deleteRange" : "delete", key, null]);
    };
    os.clear = () => record(clear(), () => [sn, "clear", null, null]);
    os[WRAPPED] = true;
    return os;
  }

  _flush() { writeAtomic(this.path, serialize(this.mirror)); }
}
