// The exact presentation asset registry (plan §4.3, P3).
//
// THE FAILURE THIS REPLACES. A named AI's portrait was redrawn by an image model and presented as
// the game art, and separately the real art was scattered across a final pack, a recovery ZIP,
// live captures and an old archive, so "use the real art" meant an afternoon of recovery. The
// registry answers one question per entity: which exact pixels does this entity currently show,
// and what proves it.
//
// TWO AXES, NOT ONE (independent review F1). The first version had a single `status` in which
// `exact-current-bytes` meant both "this is the right image" and "we have verified bytes for it".
// So when the immutable blob could not be read - an unavailable commit, a shallow clone - the
// registry recorded a note, kept going, and still promoted the asset to renderable. A wrong image
// of exactly the right size passed with the pack's ref set to an unavailable commit. An absent
// verifier must never imply verification, so the two questions are now separate fields:
//
//   status   WHICH art this is, in the plan's factual classes:
//            exact-current | approved-derivative | historical-only | mismatch | missing
//   bytes    WHETHER we hold and have verified those pixels:
//            {bound, path, ref, sha256, length, available, verified, reason}
//
// `renderable` is the conjunction, and it is the only thing a deterministic renderer may consume.
// Lint reads both: a binding that cannot be verified is fatal, not a note, because readiness counts
// and the future renderer both consume status.
//
// THE CHAIN. For an entity whose art was shipped from this repository there are four committed
// links, and the registry checks all four:
//
//   working-tree file --sha256--> equal to the BLOB AT THE PACK'S COMMIT --idmap--> uploaded URL
//   == the URL the live record currently serves (from the newest admissible capture).
//
// Comparing against the blob at the commit is what survives a working tree edited in the same
// breath as its pack entry. Comparing the uploaded URL against what the entity serves is what makes
// a SWAP detectable. No step reads a byte count, which is why a replacement of exactly the right
// size fails too.
//
// WHAT IS NOT DONE HERE, deliberately: nothing is fetched. An entity whose only current evidence is
// a remote URL is `exact-current` with `bytes.bound:false` - correct, provenanced and not
// renderable. Repository-side source-art archives can supply those bytes; wiring one is named in
// the README as the next step and is not this correction pass.

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";
import { pathProblem } from "../src/runner/imgpack.mjs";
import { PresentationError } from "./errors.mjs";

export const STATUS = Object.freeze({
  EXACT: "exact-current",
  DERIVATIVE: "approved-derivative",
  HISTORICAL: "historical-only",
  MISMATCH: "mismatch",
  MISSING: "missing",
});

/** Statuses that are the entity's current art, whether or not the bytes are here. */
export const CURRENT = Object.freeze([STATUS.EXACT]);
/** Statuses a factual, named-entity tile may be presented from at all. */
export const PRESENTABLE = Object.freeze([STATUS.EXACT, STATUS.DERIVATIVE]);

const NO_BYTES = Object.freeze({ bound: false, available: false, verified: false, reason: "no repository bytes are bound to this entity" });

/**
 * Resolve the art of every presentation entity.
 *
 * @param {object}   o
 * @param {object[]} o.entities  [{entity, name, field, liveUrl, source, capturedAt}] - the things
 *   that need art: every roster AI, every component quest's listing image, and anything the spec
 *   binds. Built by the dossier so this module does not have to know what a roster is.
 * @param {object[]} o.packs     loaded imagePack evidence records
 * @param {object[]} o.uploads   loaded idmap evidence records
 * @param {object}   o.bindings  spec `assets`: {entityKey: "<repository path>"}
 * @param {object[]} o.observations  EVERY url observation across every selected record, so stale
 *   art can be told from somebody else's art
 * @param {string}   o.root      repository root
 * @param {function} [o.blobAtRef]  (ref, path) => Buffer|null. Its ABSENCE is not verification:
 *   without it, no bound asset can reach verified bytes.
 */
export function buildAssetRegistry({ entities, packs = [], uploads = [], bindings = {}, observations = [], root, blobAtRef = null }) {
  if (!root) throw new PresentationError("buildAssetRegistry needs a repository root");

  const history = new Map();
  for (const o of observations) {
    if (!history.has(o.entityId)) history.set(o.entityId, []);
    history.get(o.entityId).push(o);
  }

  const packFiles = new Map();
  for (const rec of packs) {
    for (const [name, f] of Object.entries(rec.pack.files)) {
      packFiles.set(name, { name, ...f, ref: rec.pack.ref, source: rec.id });
    }
  }
  const packByPath = new Map([...packFiles.values()].map((f) => [f.path, f]));

  const uploadedUrl = new Map();
  for (const rec of uploads) {
    for (const [name, url] of Object.entries(rec.idmap)) {
      if (typeof url === "string" && /^https?:\/\//.test(url)) uploadedUrl.set(name, { url, source: rec.id });
    }
  }

  const digests = new Map();
  const digestOf = (relPath) => {
    if (digests.has(relPath)) return digests.get(relPath);
    let d = null;
    try {
      const b = readFileSync(join(root, relPath));
      d = { sha256: createHash("sha256").update(b).digest("hex"), length: b.length };
    } catch { d = null; }
    digests.set(relPath, d);
    return d;
  };

  const boundKeys = new Set(Object.keys(bindings));
  const out = [];

  for (const e of entities) {
    boundKeys.delete(e.entity);
    const entry = {
      entity: e.entity,
      kind: e.kind,
      name: e.name ?? null,
      field: e.field,
      liveUrl: e.liveUrl ?? null,
      status: STATUS.MISSING,
      bytes: { ...NO_BYTES },
      renderable: false,
      provenance: { record: e.source ?? null, capturedAt: e.capturedAt ?? null },
      notes: [],
    };
    const boundPath = Object.prototype.hasOwnProperty.call(bindings, e.entity) ? bindings[e.entity] : null;
    resolveEntry(entry, { boundPath, entity: e, packByPath, uploadedUrl, digestOf, blobAtRef, history });
    entry.renderable = entry.status === STATUS.EXACT && entry.bytes.verified === true;
    out.push(entry);
  }

  // F7: a binding the registry never looked at is worse than a refused one - the spec advertised a
  // choice of art, lint passed, and a renderer would have received a selection nothing checked.
  for (const key of boundKeys) {
    out.push({
      entity: key,
      kind: key.split(":")[0],
      name: null,
      field: null,
      liveUrl: null,
      status: STATUS.MISSING,
      bytes: { bound: true, path: bindings[key], available: false, verified: false, reason: "the binding names an entity this subject's evidence does not describe" },
      renderable: false,
      provenance: { record: null, capturedAt: null },
      notes: [`spec.assets binds ${JSON.stringify(key)}, which is not an entity of this subject: no selected record describes it, so the art it names cannot be checked against anything`],
    });
  }

  return {
    entries: out,
    byEntity: new Map(out.map((x) => [x.entity, x])),
    packFiles: [...packFiles.values()],
    coverage: coverageOf(out),
  };
}

function coverageOf(entries) {
  const count = (p) => entries.filter(p).length;
  return {
    total: entries.length,
    exact: count((e) => e.status === STATUS.EXACT),
    derivative: count((e) => e.status === STATUS.DERIVATIVE),
    historical: count((e) => e.status === STATUS.HISTORICAL),
    mismatch: count((e) => e.status === STATUS.MISMATCH),
    missing: count((e) => e.status === STATUS.MISSING),
    renderable: count((e) => e.renderable),
    unverifiedBindings: count((e) => e.bytes.bound && !e.bytes.verified),
  };
}

function resolveEntry(entry, { boundPath, entity, packByPath, uploadedUrl, digestOf, blobAtRef, history }) {
  const liveUrl = entity.liveUrl ?? null;

  if (boundPath == null) {
    if (!liveUrl) {
      entry.notes.push("no selected evidence records any art for this entity");
      return;
    }
    // Current art, provenanced, no bytes here. A true statement about WHICH art, and an honest
    // "not yet" about whether it can be rendered.
    entry.status = STATUS.EXACT;
    entry.bytes = { ...NO_BYTES, reason: "current art is a remote URL from a committed capture; no repository bytes are bound" };
    return;
  }

  entry.bytes = { bound: true, path: boundPath, available: false, verified: false, reason: null };

  const bad = pathProblem(boundPath);
  if (bad) {
    entry.status = STATUS.MISMATCH;
    entry.bytes.reason = `bound repository path ${bad}`;
    entry.notes.push(entry.bytes.reason);
    return;
  }
  const packed = packByPath.get(boundPath);
  if (!packed) {
    entry.status = STATUS.MISMATCH;
    entry.bytes.reason = `${boundPath} is not bound by any selected image pack, so nothing states which bytes it is meant to be`;
    entry.notes.push(entry.bytes.reason);
    return;
  }
  entry.bytes.ref = packed.ref;
  entry.bytes.declaredSha256 = packed.sha256;
  entry.bytes.declaredLength = packed.bytes;
  entry.provenance.pack = packed.source;

  const actual = digestOf(boundPath);
  if (!actual) {
    entry.status = STATUS.MISSING;
    entry.bytes.reason = `${boundPath} is not in the working tree`;
    entry.notes.push(entry.bytes.reason);
    return;
  }
  entry.bytes.available = true;
  entry.bytes.sha256 = actual.sha256;
  entry.bytes.length = actual.length;
  if (actual.sha256 !== packed.sha256) {
    entry.status = STATUS.MISMATCH;
    entry.bytes.reason = `${boundPath} hashes ${actual.sha256} but the pack binds ${packed.sha256}; the art changed without the pack being regenerated`;
    entry.notes.push(entry.bytes.reason);
    return;
  }

  // THE IMMUTABLE BLOB. A pack entry and the file beside it can be edited in the same commit and
  // will then agree perfectly while no longer being the bytes that were uploaded. What the live
  // record serves was uploaded from the blob at the pack's commit, so that is the comparison - and
  // if it cannot be made, the answer is "unverified", never "fine".
  if (!blobAtRef) {
    entry.bytes.reason = "no blob reader was supplied, so the working-tree file could not be checked against the commit the pack names";
    entry.notes.push(entry.bytes.reason);
  } else {
    const committed = blobAtRef(packed.ref, boundPath);
    if (!committed) {
      entry.bytes.reason = `the blob for ${boundPath} at ${packed.ref.slice(0, 12)} could not be read, so these bytes are unverified; an unreadable commit is not a verified one`;
      entry.notes.push(entry.bytes.reason);
    } else {
      const committedSha = createHash("sha256").update(committed).digest("hex");
      if (committedSha !== actual.sha256) {
        entry.status = STATUS.MISMATCH;
        entry.bytes.reason = `${boundPath} in the working tree hashes ${actual.sha256}, but the blob at the commit the pack names (${packed.ref.slice(0, 12)}) hashes ${committedSha}; the bytes that were uploaded are the committed ones`;
        entry.notes.push(entry.bytes.reason);
        return;
      }
      entry.bytes.verified = true;
      entry.bytes.verifiedAgainst = packed.ref;
    }
  }

  const uploaded = uploadedUrl.get(packed.name) || null;
  entry.uploadedUrl = uploaded ? uploaded.url : null;
  if (uploaded) entry.provenance.upload = uploaded.source;

  if (!uploaded) {
    entry.status = STATUS.MISMATCH;
    entry.notes.push(`no selected upload record says what URL ${packed.name} became, so these bytes cannot be tied to what the game serves`);
    return;
  }
  if (!liveUrl) {
    entry.status = STATUS.MISMATCH;
    entry.notes.push("no selected capture records this entity's current art, so a binding cannot be checked against it");
    return;
  }
  if (uploaded.url === liveUrl) {
    entry.status = STATUS.EXACT;
    return;
  }
  // Two different findings hide behind one inequality, with different remedies: art this entity
  // USED to serve is stale and wants a re-bind, art it has never served is somebody else's.
  const wasOurs = (history.get(entity.entityId) || []).find((o) => o.url === uploaded.url);
  if (wasOurs) {
    entry.status = STATUS.HISTORICAL;
    entry.notes.push(`bound to ${packed.name}, which is the art ${entity.name ?? entity.entity} served at ${wasOurs.capturedAt ?? "an earlier capture"}; it now serves ${liveUrl}`);
  } else {
    entry.status = STATUS.MISMATCH;
    entry.notes.push(`bound to ${packed.name}, which was uploaded as ${uploaded.url}, but ${entity.name ?? entity.entity} currently serves ${liveUrl}; this is not this entity's art`);
  }
}
