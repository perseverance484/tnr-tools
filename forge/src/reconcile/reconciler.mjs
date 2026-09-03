// Reconciliation (spec section 5). Uniform across all six two-phase creates.
//
// Before the FIRST create of an entity type in a job, snapshot the current id set for that
// type via its getAllNames (the AI list keys on userId). The snapshot is written to
// localStorage synchronously BEFORE the create leaves, under a key recorded on the item.
//
// On resume, for an item left in SENT:
//   phase create (no entityId yet): re-fetch the list; new = now - snapshot - ids this job
//     already confirmed for the type. Exactly one new id and exactly one pending SENT create
//     of that type -> adopt. Anything else -> ORPHANED with the candidates listed. For jutsu,
//     item, bloodline, quest and ai the placeholder name embeds the id, which is an
//     independent cross-check; for gameAsset every orphan is named "Placeholder", so the
//     diff is the ONLY signal, which is why the snapshot is mandatory.
//   phase update (entityId known): read the record; if every asserted key already matches,
//     the update landed -> confirm with landed:true and the runner goes straight to verify.
//     Otherwise -> ORPHANED ("live differs"), and the user decides; never re-sent by itself.
//   phase rules-toggle: the profile row exists -> continue at rules; else ORPHANED.
//   phase rules: the profile's rules equal the asserted rules -> landed; else ORPHANED.
// Nothing is ever deleted.

import { recipe } from "../runner/recipes.mjs";
import { diffAsserted } from "../runner/validate.mjs";

export const SNAP_PREFIX = "tnr_forge_snap_v1:";

export class Reconciler {
  /**
   * @param {object} o
   * @param {Storage} o.storage
   * @param {import("../budget/reader.mjs").CachedReader} o.reader
   * @param {() => number} [o.clock]
   */
  constructor({ storage, reader, clock = () => Date.now() }) {
    this.storage = storage; this.reader = reader; this.clock = clock;
  }

  snapKey(jobId, entity) { return SNAP_PREFIX + jobId + ":" + entity; }

  readSnapshot(key) {
    try { return JSON.parse(this.storage.getItem(key) || "null"); } catch { return null; }
  }

  /** Called by the runner before every create; takes the snapshot once per (job, entity). */
  async beforeCreate(job, item, entity) {
    const key = this.snapKey(job.jobId, entity);
    if (this.storage.getItem(key)) return key;
    const rc = recipe(entity);
    const list = await this.reader.list(rc.names, { fresh: true }); // a limited read: one token
    if (!list.ok || !Array.isArray(list.data)) throw new Error(`snapshot failed: ${rc.names} ${list.ok ? "returned no list" : list.error.code}`);
    const ids = list.data.map((r) => r[rc.idKey]).filter(Boolean);
    this.storage.setItem(key, JSON.stringify({ entity, at: new Date(this.clock()).toISOString(), path: rc.names, count: ids.length, ids }));
    return key;
  }

  /** Drop a job's snapshots (after the job is DONE or removed). */
  forget(jobId) {
    const keys = [];
    for (let i = 0; i < this.storage.length; i++) { const k = this.storage.key(i); if (k && k.startsWith(SNAP_PREFIX + jobId + ":")) keys.push(k); }
    for (const k of keys) this.storage.removeItem(k);
    return keys.length;
  }

  /**
   * Decide what a SENT item became.
   * @param {object} job     journal job
   * @param {object} item    the SENT item
   * @param {object} ctx     {planned} the planned item (data with refs unresolved is fine here)
   * @returns {Promise<{action:"confirm", entityId?, phase?, landed?, note} | {action:"orphan", candidates, note}>}
   */
  async resolveSent(job, item, ctx = {}) {
    const rc = recipe(item.entity);
    if (item.phase === "create" || !item.entityId) return this._resolveCreate(job, item, rc);
    if (item.phase === "rules-toggle") return this._resolveToggle(item, rc);
    if (item.phase === "rules") return this._resolveRules(item, ctx);
    return this._resolveUpdate(item, rc, ctx);
  }

  async _resolveCreate(job, item, rc) {
    const key = item.snapshotKey || this.snapKey(job.jobId, item.entity);
    const snap = this.readSnapshot(key);
    if (!snap) return { action: "orphan", candidates: [], note: "no pre-create snapshot for this entity type; cannot tell which row is ours" };
    const list = await this.reader.list(rc.names, { fresh: true });
    if (!list.ok || !Array.isArray(list.data)) return { action: "orphan", candidates: [], note: `${rc.names} unavailable: ${list.ok ? "no list" : list.error.code}` };
    const before = new Set(snap.ids);
    const confirmedThisJob = new Set(job.items.filter((it) => it.entity === item.entity && it.entityId && it.idx !== item.idx).map((it) => it.entityId));
    const rows = list.data.filter((r) => !before.has(r[rc.idKey]) && !confirmedThisJob.has(r[rc.idKey]));
    const pending = job.items.filter((it) => it.entity === item.entity && it.state === "SENT" && (it.phase === "create" || !it.entityId));
    const candidates = rows.map((r) => ({ id: r[rc.idKey], name: r[rc.nameKey] ?? null, placeholderName: rc.placeholder ? rc.placeholder(r[rc.idKey]) === (r[rc.nameKey] ?? null) : null }));
    if (candidates.length === 1 && pending.length === 1) {
      const c = candidates[0];
      return { action: "confirm", entityId: c.id, phase: "update", note: `adopted the single new ${item.entity} ${c.id}` + (c.placeholderName === false ? " (name is not the placeholder pattern; check it)" : "") };
    }
    return { action: "orphan", candidates, note: `${candidates.length} new ${item.entity} row(s) since the snapshot, ${pending.length} create(s) pending: ambiguous` };
  }

  async _resolveUpdate(item, rc, ctx) {
    const planned = ctx.planned;
    if (!planned) return { action: "orphan", candidates: [], note: "no planned data to compare against" };
    const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
    if (!live.ok || !live.data) return { action: "orphan", candidates: [], note: `${rc.get} ${item.entityId}: ${live.ok ? "no record" : live.error.code}` };
    const data = stripRefs(planned.data);
    const diffs = diffAsserted(item.entity, data, live.data);
    if (!diffs.length) return { action: "confirm", entityId: item.entityId, phase: "verify", landed: true, note: "update already landed: asserted keys match live" };
    return { action: "orphan", candidates: [], note: "update may not have landed: live differs on " + diffs.map((d) => d.key).join(", "), diffs };
  }

  async _resolveToggle(item, rc) {
    const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
    if (live.ok && live.data && live.data.aiProfileId) return { action: "confirm", entityId: item.entityId, phase: "rules", note: "profile row exists; continue at rules" };
    return { action: "orphan", candidates: [], note: "no aiProfileId after a sent toggle" };
  }

  async _resolveRules(item, ctx) {
    if (!item.aiProfileId) return { action: "orphan", candidates: [], note: "rules sent but no aiProfileId recorded" };
    const prof = await this.reader.get("ai.getAiProfile", item.aiProfileId, { fresh: true });
    if (!prof.ok || !prof.data) return { action: "orphan", candidates: [], note: "ai.getAiProfile unavailable" };
    const want = ctx.planned ? ctx.planned.data.rules ?? [] : null;
    if (want && JSON.stringify(prof.data.rules ?? []) === JSON.stringify(want)) return { action: "confirm", entityId: item.entityId, phase: "verify", landed: true, note: "rules already landed" };
    return { action: "orphan", candidates: [], note: "rules may not have landed: profile rules differ" };
  }
}

// asserted keys whose values are still @refs cannot be compared; drop them from the diff
function stripRefs(data) {
  const out = {};
  for (const [k, v] of Object.entries(data)) if (!/@(jutsu|ai|scene|item|quest|bloodline|img):/.test(JSON.stringify(v) ?? "")) out[k] = v;
  return out;
}
