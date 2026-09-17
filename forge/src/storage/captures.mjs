// The capture cache. IndexedDB, because captures exceed the localStorage quota.
// DB tnr_forge. TWO stores, with deliberately different lifetimes:
//
//   captures           the READ CACHE. Two key shapes, because two kinds of read live here:
//                      `${path}:${idKey}` for a POINT read, where idKey is the record id or "" for
//                      an input-free name list; and `${path}?${canonicalJson}` for a QUERY read,
//                      where the key carries the exact canonical input that was sent. A query row's
//                      identity is its input, so two filters or two pages of one procedure can never
//                      share a slot (Phase 1 requirement 7.1). One slot per key, overwritten by the
//                      next read of that key and deleted by a write to that entity. Its job is to
//                      save budget, and a cache that did not go stale would be wrong.
//   capture_snapshots  IMMUTABLE EVIDENCE. One record per `persist: "full"` capture OCCURRENCE,
//                      keyed by job + phase + ordinal, holding the exact decoded body of that
//                      specific read.
//
// The two must not be confused, and the second exists because they were (independent review
// FFC-1). `path + id` identifies a mutable cache slot, never a capture event. A manifest may
// legally read the same record in capture.before, write it, and read it again in capture.after;
// keyed on path+id, the before body is first deleted by the write's invalidation and then
// replaced by the read-back's body, so exporting "the exact body of the before read" from that
// slot silently ships the AFTER record with a green persistence verdict. Repeated reads of one
// record have the same aliasing problem with no write involved at all. A snapshot is therefore
// written once, from the body that read returned, and nothing overwrites or invalidates it.
//
// Invalidation rule (spec section 6): any write to an entity drops every CACHE record for that
// entity, both the record's own get and the entity's list captures, because a rename changes
// what getAllNames returns. Invalidation never touches capture_snapshots: evidence of what was
// read is not made wrong by a later write, that is the whole point of keeping it.

import { PROCEDURES } from "../transport/procedures.mjs";
import { REPO_SAFE_PATHS } from "../research/registry.mjs";

export const DB_NAME = "tnr_forge";
export const STORE = "captures";
export const SNAPSHOT_STORE = "capture_snapshots";
// v2 adds capture_snapshots. The upgrade is additive: an existing v1 database keeps its captures
// store untouched and gains the new one, so a browser holding a v1 cache upgrades in place.
export const DB_VERSION = 2;

export function captureKey(path, id) { return `${path}:${id ?? ""}`; }

/**
 * The cache identity of a QUERY read: the path plus the exact canonical serialization of the input
 * that was sent (research/registry.mjs canonicalKey). `?` rather than `:` separates the two key
 * families, so no query key can ever be mistaken for — or collide with — a point read's record id.
 *
 * The whole serialization is in the key rather than a digest of it. A 32-bit hash of an unbounded
 * input space can collide, and a collision here would answer one filter's read with another's body
 * under a green provenance, which is the exact aliasing requirement 7.1 forbids.
 */
export function queryCaptureKey(path, queryKey) { return `${path}?${queryKey ?? ""}`; }

/**
 * The immutable identity of ONE full-capture occurrence. Job, phase and ordinal, because that is
 * what actually names the read: the nth capture of the before or after pass of this job. It is
 * deterministic, so a resumed pass that re-journals an entry addresses the same snapshot, and it
 * is unrelated to the record id, so two captures of one record never collide.
 */
export function snapshotKey(jobId, phase, ordinal) { return `${jobId}::${phase}::${ordinal}`; }

// ------------------------------------------------------------------ persistence tiers
// A capture declares the TIER its body is kept at (RUL-2026-09-17-001). The admission decision —
// which paths exist at all, and what each one's ceiling is — belongs to research/registry.mjs, so
// this file derives rather than restates it. The old FULL_PERSIST_PATHS name is kept because the
// manifest grammar, the screens and the existing tests all speak it, but it is now exactly "the
// rows the registry classifies repo-safe" rather than a second list that could drift from the first.
export const FULL_PERSIST_PATHS = REPO_SAFE_PATHS;

/** Whether a procedure path may have its response body durably persisted into a bundle. */
export function canPersistFull(path) { return FULL_PERSIST_PATHS.includes(path); }

/**
 * The tier a journaled capture record is to be read at, including records written before tiers
 * existed. This is the ONE place that decision is made, because it has to give the same answer to
 * the exporter, the outcome verdict and the screens - and in Phase 1 it briefly did not, which let a
 * Phase 0 `persist: "full"` entry be treated as a capture that had asked for nothing (independent
 * review FN1).
 *
 * The legacy mapping is deliberately narrow: ONLY `persist: "full"`, which is the exact shape
 * runner.mjs wrote before this contract, maps to repo-safe. Anything else with no tier is a summary
 * capture that kept no body. There is no blanket default, because a default would silently adopt
 * whatever an unrecognised or malformed record happens to contain.
 */
export function captureTier(capture) {
  if (!capture || typeof capture !== "object") return null;
  if (typeof capture.tier === "string" && capture.tier) return capture.tier;
  return capture.persist === "full" ? "repo-safe" : null;
}

/** True when this record predates tiers, so the caller knows to apply the conservative old rules. */
export function isLegacyCapture(capture) {
  return Boolean(capture && typeof capture === "object" && !capture.tier && capture.persist === "full");
}

/** The audited registry's opinion of a path, or null when it is not in the crud surface. */
export function persistProcedureKind(path) { return PROCEDURES[path] ? PROCEDURES[path].kind : null; }

// Defensive ceiling on ONE serialized full body. The largest content record observed in the
// repository's own committed captures is a 49-node quest at ~71 KB (harvests/inbox, quests.get),
// so 512 KiB is roughly seven times the worst real record and still small enough that a runaway
// body cannot quietly become a megabyte-scale commit. Exceeding it is an explicit persistence
// FAILURE, never a shortened body presented as full: nothing in this codebase truncates a body.
//
// "bytes" is JSON.stringify().length of the body - UTF-16
// code units, not encoded octets. That is the existing meaning of `bytes` throughout these stores
// and the Captures screen, so the ceiling keeps it rather than introducing a second unit; a body
// of non-ASCII text is measured slightly small, well inside the headroom above.
export const MAX_FULL_CAPTURE_BYTES = 512 * 1024;

// The same defensive idea for a LOCAL-ONLY body, at a different number because it bounds a
// different risk. Nothing local-only is ever committed, so the repository-commit argument above does
// not apply; what is left is an IndexedDB store one runaway response could fill. 8 MiB is roughly
// sixteen times the repo ceiling — comfortably above a 500-entry battle action log, which is the
// largest research body the committed manifests actually ask for — and still an amount a browser
// profile can hold without trouble. Exceeding it is an explicit persistence FAILURE, never a
// shortened body presented as whole: there is no truncation path here either.
export const MAX_LOCAL_CAPTURE_BYTES = 8 * 1024 * 1024;

/** The byte ceiling that applies to a body kept at `tier`. */
export function tierCeiling(tier) { return tier === "repo-safe" ? MAX_FULL_CAPTURE_BYTES : MAX_LOCAL_CAPTURE_BYTES; }

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
          if (!db.objectStoreNames.contains(SNAPSHOT_STORE)) {
            const snaps = db.createObjectStore(SNAPSHOT_STORE, { keyPath: "key" });
            snaps.createIndex("jobId", "jobId", { unique: false });
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

  async _tx(mode, fn, storeName = STORE) {
    let db = await this._open();
    let tx;
    try { tx = db.transaction(storeName, mode); }
    catch (e) { if (e && e.name === "InvalidStateError") { this._db = null; db = await this._open(); tx = db.transaction(storeName, mode); } else throw e; }
    const store = tx.objectStore(storeName);
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

  /**
   * Store a decoded QUERY response under the exact input that produced it.
   *
   * `id` is deliberately null on these rows and the input lives in `query`. That is not cosmetic:
   * invalidateRecord() drops every row of an entity whose id is null, which is how list captures
   * already get invalidated by a write. A query row inherits that behaviour by being shaped like a
   * list row, so a write to an entity cannot leave a stale filtered read of it behind.
   */
  async putQuery({ path, queryKey, input, data }) {
    const rec = {
      key: queryCaptureKey(path, queryKey),
      path, id: null, query: queryKey ?? "",
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

  async getQuery(path, queryKey) {
    const rec = await this._tx("readonly", (s) => reqToPromise(s.get(queryCaptureKey(path, queryKey))));
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
    return recs.map(({ key, path, id, entity, at, bytes, query }) => ({ key, path, id, entity, at, bytes, query: query ?? null }));
  }

  async size() {
    const recs = await this.list();
    return { count: recs.length, bytes: recs.reduce((a, r) => a + (r.bytes || 0), 0) };
  }

  async clear() { await this._tx("readwrite", (s) => reqToPromise(s.clear())); }

  // ---------------------------------------------------------------- immutable capture snapshots
  /**
   * Store the exact decoded body of ONE full capture, under its occurrence key. Written once, from
   * the body that read returned, and never rewritten by a later read of the same record: this is
   * the copy the exported bundle is materialized from.
   *
   * Deliberately NOT reachable from invalidateEntity/invalidateRecord/clear, all of which operate
   * on the read cache only. A snapshot is deleted explicitly, by job or by key.
   */
  async putSnapshot({ key, jobId, phase, ordinal, path, id, input, data, tier = "repo-safe", projection = null, page = null, policy = null }) {
    const rec = {
      key, jobId, phase, ordinal, path,
      id: id == null || id === "" ? null : String(id),
      entity: entityOfPath(path),
      // The tier travels WITH the body. Export asks the snapshot what it is allowed to do with what
      // it just read, rather than re-deriving it from the path — so a registry edit that narrows a
      // tier cannot retroactively make an already-stored body exportable under the old rule, and a
      // snapshot separated from its journal entry still knows it is local-only.
      tier,
      // The policy that admitted the read travels WITH the body, so evidence and the contract that
      // allowed it cannot be separated by a journal edit or a later registry change (review FN4).
      policy,
      projection: projection ? [...projection] : null,
      page,
      input: input ?? null,
      data,
      at: new Date(this.clock()).toISOString(),
      bytes: JSON.stringify(data ?? null).length,
    };
    await this._tx("readwrite", (s) => reqToPromise(s.put(rec)), SNAPSHOT_STORE);
    return rec;
  }

  async getSnapshot(key) {
    const rec = await this._tx("readonly", (s) => reqToPromise(s.get(key)), SNAPSHOT_STORE);
    return rec ?? null;
  }

  async listSnapshots() {
    const recs = await this._tx("readonly", (s) => reqToPromise(s.getAll()), SNAPSHOT_STORE);
    return recs.map(({ key, jobId, phase, ordinal, path, id, entity, at, bytes, tier }) => ({ key, jobId, phase, ordinal, path, id, entity, at, bytes, tier: tier ?? "repo-safe" }));
  }

  async deleteSnapshot(key) {
    await this._tx("readwrite", (s) => reqToPromise(s.delete(key)), SNAPSHOT_STORE);
  }

  /** Drop every snapshot belonging to one job, for when that job's record is deleted. */
  async deleteSnapshotsForJob(jobId) {
    return this._tx("readwrite", async (s) => {
      const keys = await reqToPromise(s.index("jobId").getAllKeys(jobId));
      for (const k of keys) await reqToPromise(s.delete(k));
      return keys.length;
    }, SNAPSHOT_STORE);
  }

  async clearSnapshots() { await this._tx("readwrite", (s) => reqToPromise(s.clear()), SNAPSHOT_STORE); }

  close() { if (this._db) { this._db.close(); this._db = null; } }
}
