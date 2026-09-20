// The exact presentation asset registry (plan §4.3, P3).
//
// THE FAILURE THIS REPLACES. A named AI's portrait was redrawn by an image model and presented as
// the game art, and separately the real art was scattered across a final pack, a recovery ZIP,
// live captures and an old archive, so "use the real art" meant an afternoon of recovery. The
// registry answers one question per entity: which exact pixels does this character currently show,
// and what proves it.
//
// THE CHAIN. For an AI whose art was shipped from this repository there are three committed links,
// and the registry checks all three:
//
//   repository blob  --sha256-->  imagePack entry  --idmap-->  uploaded URL  ==  the avatar the
//   live record currently serves (from the newest capture of that AI).
//
// When every link holds, the entity is `exact-current-bytes`: the presentation can render the
// repository file and know it is byte-identical to what the game shows. That is the only status
// that supports deterministic offline rendering.
//
// WHY THE LAST LINK MATTERS MORE THAN IT LOOKS. Byte-verifying a repository file against its own
// pack digest proves the file has not changed; it does NOT prove the file is this character's art.
// Comparing the uploaded URL against the avatar the character currently serves is what makes a
// SWAP detectable - and it is why a wrong file of exactly the right size is caught too, because no
// step in this chain consults a byte count.
//
// WHAT IS NOT DONE HERE, deliberately: nothing is fetched. This task is zero-live-request, so an
// entity whose only current evidence is a remote URL resolves as `exact-current-remote` - correct
// and provenanced, but not yet materialised. Materialising those into a content-addressed cache
// (verifying the digest on arrival, exactly as repo-backed image packs do) is the renderer's job
// in P2, and lint says so rather than letting a renderer discover it.

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";
import { pathProblem } from "../src/runner/imgpack.mjs";
import { PresentationError } from "./errors.mjs";

export const STATUS = Object.freeze({
  EXACT_BYTES: "exact-current-bytes",
  EXACT_REMOTE: "exact-current-remote",
  HISTORICAL: "historical-only",
  MISSING: "missing",
  MISMATCH: "mismatch",
});

/** Statuses a factual, named-entity tile may be rendered from. */
export const RENDERABLE = Object.freeze([STATUS.EXACT_BYTES]);
/** Statuses that are current art, whether or not the bytes are here yet. */
export const CURRENT = Object.freeze([STATUS.EXACT_BYTES, STATUS.EXACT_REMOTE]);

/**
 * Resolve the art of every roster entity.
 *
 * @param {object}   o
 * @param {object[]} o.roster    roster entries (aiId, name, capturedAt, avatar via aiIndex)
 * @param {Map}      o.aiIndex   aiId -> {avatar, capturedAt, source} (roster.byId)
 * @param {object[]} o.packs     loaded imagePack evidence records
 * @param {object[]} o.uploads   loaded idmap evidence records
 * @param {object}   o.bindings  spec `assets`: {entityKey: "<repository path>"} - an EXPLICIT
 *                               author choice of which approved file is this entity's art
 * @param {object[]} o.observations  EVERY avatar observation across every selected record, not just
 *                               the newest per AI. Needed to tell "this is a different character's
 *                               art" (a swap) from "this is this character's art from before it was
 *                               replaced" (historical) - two different findings with two different
 *                               remedies, which a single equality check cannot separate.
 * @param {string}   o.root      repository root
 * @param {function} [o.blobAtRef]  (ref, path) => Buffer|null, the file's bytes AT THE PACK'S
 *   COMMIT. Injected so this module never shells out on its own and so a test can present a
 *   working tree that disagrees with the commit. See the note on rule 3 below for why comparing a
 *   file against its own pack entry is not enough.
 */
export function buildAssetRegistry({ roster, aiIndex, packs = [], uploads = [], bindings = {}, observations = [], root, blobAtRef = null }) {
  if (!root) throw new PresentationError("buildAssetRegistry needs a repository root");

  // aiId -> every avatar it has been observed serving, with when
  const history = new Map();
  for (const o of observations) {
    if (!history.has(o.aiId)) history.set(o.aiId, []);
    history.get(o.aiId).push(o);
  }

  // logical image name -> {path, sha256, bytes, ref, source}
  const packFiles = new Map();
  for (const rec of packs) {
    for (const [name, f] of Object.entries(rec.pack.files)) {
      packFiles.set(name, { name, ...f, ref: rec.pack.ref, source: rec.id });
    }
  }
  // repository path -> the pack entry that binds it (a spec binds by path, humans read paths)
  const packByPath = new Map([...packFiles.values()].map((f) => [f.path, f]));

  // uploaded URL for each logical image name, newest record wins
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
      const bytes = readFileSync(join(root, relPath));
      d = { sha256: createHash("sha256").update(bytes).digest("hex"), bytes: bytes.length };
    } catch { d = null; }
    digests.set(relPath, d);
    return d;
  };

  const entries = [];
  for (const entity of roster) {
    const key = `ai:${entity.aiId}`;
    const known = aiIndex.get(entity.aiId) || null;
    const liveUrl = known ? known.avatar : null;
    const entry = {
      entity: key,
      name: entity.name,
      field: "avatar",
      liveUrl,
      status: STATUS.MISSING,
      provenance: {
        record: known ? known.source : null,
        capturedAt: known ? known.capturedAt : null,
      },
      notes: [],
    };

    const boundPath = Object.prototype.hasOwnProperty.call(bindings, key) ? bindings[key] : null;
    if (boundPath != null) {
      const bad = pathProblem(boundPath);
      if (bad) {
        entry.status = STATUS.MISMATCH;
        entry.notes.push(`bound repository path ${bad}`);
        entries.push(entry);
        continue;
      }
      entry.repoPath = boundPath;
      const packed = packByPath.get(boundPath);
      if (!packed) {
        entry.status = STATUS.MISMATCH;
        entry.notes.push(`${boundPath} is not bound by any selected image pack, so nothing states which bytes it is meant to be`);
        entries.push(entry);
        continue;
      }
      entry.ref = packed.ref;
      entry.declaredSha256 = packed.sha256;
      entry.declaredBytes = packed.bytes;
      entry.provenance.pack = packed.source;
      const actual = digestOf(boundPath);
      if (!actual) {
        entry.status = STATUS.MISSING;
        entry.notes.push(`${boundPath} is not in the working tree`);
        entries.push(entry);
        continue;
      }
      entry.sha256 = actual.sha256;
      entry.bytes = actual.bytes;
      if (actual.sha256 !== packed.sha256) {
        entry.status = STATUS.MISMATCH;
        entry.notes.push(`${boundPath} hashes ${actual.sha256} but the pack binds ${packed.sha256}; the art changed without the pack being regenerated`);
        entries.push(entry);
        continue;
      }
      // THE WORKING TREE IS NOT THE BINDING. A pack entry and the file beside it can be edited in
      // the same commit and will then agree with each other perfectly while no longer being the
      // bytes that were uploaded. What the live record actually serves was uploaded from the blob
      // at the pack's IMMUTABLE commit, so that is what a presentation must render. Comparing
      // against it is also the only check that survives a replacement file of exactly the right
      // size: nothing here looks at a byte count.
      if (blobAtRef) {
        const committed = blobAtRef(packed.ref, boundPath);
        if (!committed) {
          entry.notes.push(`the blob for ${boundPath} at ${packed.ref.slice(0, 12)} could not be read, so the working-tree file could not be checked against the commit the pack names`);
          entry.refVerified = false;
        } else {
          const committedSha = createHash("sha256").update(committed).digest("hex");
          entry.refVerified = committedSha === actual.sha256;
          if (!entry.refVerified) {
            entry.status = STATUS.MISMATCH;
            entry.notes.push(`${boundPath} in the working tree hashes ${actual.sha256}, but the blob at the commit the pack names (${packed.ref.slice(0, 12)}) hashes ${committedSha}; the bytes that were uploaded are the committed ones, so the working-tree file is not this entity's art`);
            entries.push(entry);
            continue;
          }
        }
      }
      const uploaded = uploadedUrl.get(packed.name) || null;
      entry.uploadedUrl = uploaded ? uploaded.url : null;
      if (uploaded) entry.provenance.upload = uploaded.source;
      if (!uploaded) {
        entry.status = STATUS.MISMATCH;
        entry.notes.push(`no selected upload record says what URL ${packed.name} became, so these bytes cannot be tied to what the game serves`);
      } else if (!liveUrl) {
        entry.status = STATUS.MISMATCH;
        entry.notes.push("no selected capture records this entity's current avatar, so a binding cannot be checked against it");
      } else if (uploaded.url !== liveUrl) {
        // THE SWAP DETECTOR. Byte count never enters this comparison, which is why a wrong file of
        // exactly the right size fails here too.
        //
        // Two different findings hide behind one inequality, and the remedies differ: art this
        // entity USED to serve is stale and wants a re-bind to the current file, while art it has
        // never served is somebody else's and wants the binding corrected. Saying which is why the
        // observation history is passed in.
        const wasOurs = (history.get(entity.aiId) || []).find((o) => o.avatar === uploaded.url);
        if (wasOurs) {
          entry.status = STATUS.HISTORICAL;
          entry.notes.push(`bound to ${packed.name}, which is the art ${entity.name ?? key} served at ${wasOurs.capturedAt ?? "an earlier capture"}; it now serves ${liveUrl}`);
        } else {
          entry.status = STATUS.MISMATCH;
          entry.notes.push(`bound to ${packed.name}, which was uploaded as ${uploaded.url}, but ${entity.name ?? key} currently serves ${liveUrl}; this is not this entity's art`);
        }
      } else {
        entry.status = STATUS.EXACT_BYTES;
      }
      entries.push(entry);
      continue;
    }

    if (!liveUrl) {
      entry.notes.push("no selected evidence records any art for this entity");
      entries.push(entry);
      continue;
    }
    // No explicit binding. The current avatar from the newest capture is exact-current art; it is
    // simply not here as bytes, so a deterministic renderer must materialise and verify it first.
    entry.status = STATUS.EXACT_REMOTE;
    entry.notes.push("current art is a remote URL from a committed capture; no repository bytes are bound, so a deterministic render must materialise and hash it first");
    entries.push(entry);
  }

  return {
    entries,
    byEntity: new Map(entries.map((e) => [e.entity, e])),
    packFiles: [...packFiles.values()],
    coverage: {
      total: entries.length,
      exactBytes: entries.filter((e) => e.status === STATUS.EXACT_BYTES).length,
      exactRemote: entries.filter((e) => e.status === STATUS.EXACT_REMOTE).length,
      historical: entries.filter((e) => e.status === STATUS.HISTORICAL).length,
      missing: entries.filter((e) => e.status === STATUS.MISSING).length,
      mismatch: entries.filter((e) => e.status === STATUS.MISMATCH).length,
    },
  };
}
