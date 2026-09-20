// Explicit committed evidence loading (plan §4.1), with a real source lock.
//
// A dossier is built from sources somebody NAMED, at exact paths, at an exact commit, selecting
// exact captures. There is no scan of harvests/, no "most recent bundle wins", no fallback to a
// planning document, and - after independent review F2/F3 - no acceptance of a record merely
// because it is shaped like one.
//
// THREE THINGS THIS FILE REFUSES, each one a reproduced bypass of the first version:
//
//   1. ADMISSION (F2). The first version deep-searched the whole JSON document for any object
//      carrying {userId, username, avatar}. A failed capture, a capture whose input named a
//      different entity, and a stray object in a top-level `debugSnapshot` all satisfied a
//      "complete" 18/18 roster. A record is now admitted only when a SUPPORTED CAPTURE says so:
//      right procedure, ok, fully persisted, and the body's own identity equal to the identity
//      the request asked for. Nothing outside `captures[]` is evidence.
//
//   2. THE SOURCE LOCK (F3). The first version hashed whatever the working tree happened to hold
//      and called that provenance. Editing a reward in the working copy produced a passing dossier
//      with a fresh hash and no warning. A package now names `repoCommit`, every record names the
//      `sha256` its bytes must have, and both are checked: the file must hash to what the record
//      declares AND equal the blob at that commit. `draft: true` is the one way to build from
//      uncommitted bytes, and it marks the dossier rather than hiding the fact.
//
//   3. SELECTION (F3). The first version took the first matching capture in array order and ranked
//      AI freshness by the BUNDLE EXPORT timestamp. Prepending an older `before` capture therefore
//      won, and a 1-ryo draft reward became the current full clear. A record now selects by an
//      explicit capture identity, exactly one capture may match, and freshness uses the capture's
//      own `at`. Two candidates with the same timestamp and different content are a CONFLICT and
//      are refused rather than resolved by array order.
//
// FRESHNESS IS VISIBLE, NOT ASSUMED (plan P5). A capture from a run whose overall outcome failed is
// still evidence when that capture itself read back ok and persisted: the Marrow Vaults quest
// update landed and was captured in a run whose later image items errored. The run outcome is
// recorded and warned about; it is the per-capture check that decides.

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, isAbsolute } from "node:path";
import { PresentationError } from "./errors.mjs";
import { normalizeImagePack, pathProblem } from "../src/runner/imgpack.mjs";

export const EVIDENCE_SCHEMA = "tnr.presentation.evidence.v2";

const KINDS = new Set(["quest", "aiRecords", "assetRecords", "imagePack", "uploads"]);
const RECORD_KEYS = new Set(["id", "kind", "path", "sha256", "questId", "capture", "note"]);
const PACKAGE_KEYS = new Set(["schema", "repoCommit", "draft", "subject", "records", "note"]);
const SUBJECT_KEYS = new Set(["type", "title", "components"]);
const CAPTURE_KEYS = new Set(["proc", "phase", "at", "snapshotKey"]);

/** The procedure each record kind is allowed to read, so a selector cannot point at another. */
const KIND_PROC = { quest: "quests.get", aiRecords: "profile.getAi", assetRecords: "gameAsset.get" };
/** The request field that carries the entity identity, per procedure. */
const PROC_ID_FIELD = { "quests.get": "id", "profile.getAi": "userId", "gameAsset.get": "id" };
/** The body field that must equal it. A capture whose body is a different entity is not evidence. */
const PROC_BODY_ID = { "quests.get": "id", "profile.getAi": "userId", "gameAsset.get": "id" };

const COMMIT_RE = /^[0-9a-f]{40}$/;
const SHA256_RE = /^[0-9a-f]{64}$/;

const only = (obj, allowed, where) => {
  for (const k of Object.keys(obj)) {
    if (!allowed.has(k)) throw new PresentationError(`${where}: unknown key "${k}"`);
  }
};

/**
 * Parse and check an evidence package. Pure: no file is read here.
 * @param {object} raw
 * @returns {object} the frozen package
 */
export function parseEvidence(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) throw new PresentationError("evidence package is not an object");
  if (raw.schema !== EVIDENCE_SCHEMA) {
    throw new PresentationError(`evidence package schema must be "${EVIDENCE_SCHEMA}", found ${JSON.stringify(raw.schema)}`);
  }
  only(raw, PACKAGE_KEYS, "evidence package");

  const draft = raw.draft === true;
  if (!draft && (typeof raw.repoCommit !== "string" || !COMMIT_RE.test(raw.repoCommit))) {
    throw new PresentationError(
      "evidence package must name repoCommit as a 40-hex commit sha: the source lock is what makes the dossier a derivative of " +
      "known bytes rather than of whatever the working tree holds. Set draft:true to build from uncommitted evidence deliberately.",
    );
  }
  if (draft && raw.repoCommit != null) throw new PresentationError("a draft evidence package must not also claim a repoCommit");

  const subject = raw.subject;
  if (!subject || typeof subject !== "object") throw new PresentationError("evidence package has no subject");
  only(subject, SUBJECT_KEYS, "evidence subject");
  if (typeof subject.title !== "string" || !subject.title.trim()) throw new PresentationError("evidence subject needs a title");
  if (!Array.isArray(raw.records) || !raw.records.length) throw new PresentationError("evidence package selects no records");

  const seen = new Set();
  const records = raw.records.map((r, i) => {
    const where = `evidence record ${i}`;
    if (!r || typeof r !== "object") throw new PresentationError(`${where} is not an object`);
    only(r, RECORD_KEYS, where);
    if (typeof r.id !== "string" || !r.id) throw new PresentationError(`${where} has no id`);
    if (seen.has(r.id)) throw new PresentationError(`${where}: duplicate record id "${r.id}"`);
    seen.add(r.id);
    if (!KINDS.has(r.kind)) throw new PresentationError(`${where} (${r.id}): unknown kind ${JSON.stringify(r.kind)}`);
    // The same path rule the image-pack contract uses: repository-relative, plain segments, no
    // traversal, no scheme. An evidence package is data too.
    const bad = pathProblem(r.path);
    if (bad) throw new PresentationError(`${where} (${r.id}): path ${bad}`);
    if (!draft && (typeof r.sha256 !== "string" || !SHA256_RE.test(r.sha256))) {
      throw new PresentationError(`${where} (${r.id}): must declare the sha256 of the source file it selects (64 lowercase hex)`);
    }
    if (r.kind === "quest" && (typeof r.questId !== "string" || !r.questId)) {
      throw new PresentationError(`${where} (${r.id}): a quest record must name the questId it selects`);
    }
    if (r.kind !== "quest" && r.questId != null) {
      throw new PresentationError(`${where} (${r.id}): questId is only meaningful on a quest record`);
    }

    let capture = null;
    if (r.capture != null) {
      if (typeof r.capture !== "object" || Array.isArray(r.capture)) throw new PresentationError(`${where} (${r.id}): capture selector is not an object`);
      only(r.capture, CAPTURE_KEYS, `${where} (${r.id}) capture selector`);
      capture = { ...r.capture };
    }
    const expectedProc = KIND_PROC[r.kind];
    if (expectedProc) {
      if (!capture) capture = {};
      if (capture.proc != null && capture.proc !== expectedProc) {
        throw new PresentationError(`${where} (${r.id}): a ${r.kind} record reads ${expectedProc}, not ${JSON.stringify(capture.proc)}`);
      }
      capture.proc = expectedProc;
      // A record that selects ONE entity must pin the capture exactly. A record that gathers a set
      // (aiRecords, assetRecords) selects by procedure and phase; every member is validated below.
      if (r.kind === "quest" && !capture.at && !capture.snapshotKey) {
        throw new PresentationError(
          `${where} (${r.id}): a quest record must pin the capture it selects by "at" or "snapshotKey". ` +
          "Choosing the first capture that happens to match is how a stale before-read became the current record.",
        );
      }
    } else if (capture) {
      throw new PresentationError(`${where} (${r.id}): a ${r.kind} record reads a whole file, not a capture`);
    }

    return Object.freeze({ ...r, capture: capture ? Object.freeze(capture) : null });
  });
  return Object.freeze({ ...raw, draft, repoCommit: draft ? null : raw.repoCommit, records: Object.freeze(records) });
}

/** Does this capture match the selector? */
const matchesSelector = (c, sel) =>
  c.proc === sel.proc
  && (sel.phase == null || c.phase === sel.phase)
  && (sel.at == null || c.at === sel.at)
  && (sel.snapshotKey == null || c.snapshotKey === sel.snapshotKey);

/**
 * Is this capture admissible as evidence at all? (F2.)
 *
 * Not "is it shaped right" - is it a SUPPORTED READ that actually happened, persisted, and came
 * back describing the entity it asked about. Every clause here corresponds to a reproduced bypass:
 * a capture with ok:false still resolved a keeper; a capture whose input named another entity
 * still resolved it; a capture with persist:"none" still supplied current structure.
 *
 * @returns {string|null} the reason it is inadmissible, or null when it is evidence
 */
export function captureProblem(c, { proc } = {}) {
  if (!c || typeof c !== "object") return "not an object";
  if (proc && c.proc !== proc) return `is a ${JSON.stringify(c.proc)} capture, not ${proc}`;
  if (c.ok !== true) return "did not read back ok";
  if (c.error != null) return `carries an error (${JSON.stringify(c.error)})`;
  if (c.persist !== "full") return `was persisted as ${JSON.stringify(c.persist)}, not "full"; a projected or dropped body is not a record`;
  if (c.persistOk !== true) return "was not persisted successfully, so its body is not the body that was read";
  if (!c.data || typeof c.data !== "object" || Array.isArray(c.data)) return "carries no record body";
  if (typeof c.at !== "string" || !c.at) return "carries no capture timestamp";
  const idField = PROC_ID_FIELD[c.proc];
  const bodyField = PROC_BODY_ID[c.proc];
  if (idField) {
    const asked = c.input && c.input[idField];
    if (typeof asked !== "string" || !asked) return `names no ${idField} in its request`;
    const answered = c.data[bodyField];
    if (typeof answered !== "string" || !answered) return `the body carries no ${bodyField}`;
    if (asked !== answered) return `asked for ${idField} ${JSON.stringify(asked)} but the body is ${JSON.stringify(answered)}`;
  }
  return null;
}

/** Admissible captures of one file matching a selector, with the reasons the others were refused. */
function selectCaptures(file, selector) {
  const all = Array.isArray(file.captures) ? file.captures : [];
  const matched = all.filter((c) => c && typeof c === "object" && matchesSelector(c, selector));
  const admitted = [];
  const refused = [];
  for (const c of matched) {
    const problem = captureProblem(c, { proc: selector.proc });
    if (problem) refused.push({ capture: c, problem });
    else admitted.push(c);
  }
  return { admitted, refused, matched };
}

/**
 * Required fields of a quest body. Missing is UNKNOWN, never false: dropping `hidden` used to
 * produce `hidden:false` and quietly lose the unpublished warning, which is the opposite of what
 * incomplete evidence should do.
 */
function questProblem(q) {
  if (typeof q.name !== "string" || !q.name) return "carries no name";
  if (!q.content || typeof q.content !== "object" || Array.isArray(q.content)) return "carries no content object";
  if (!Array.isArray(q.content.objectives) || !q.content.objectives.length) return "carries no objectives";
  if (typeof q.hidden !== "boolean") return 'carries no boolean "hidden"; publication state would have to be guessed';
  return null;
}

/**
 * Load every record an evidence package selects.
 *
 * @param {object} pkg    a parsed evidence package
 * @param {string} root   repository root; every path resolves under it
 * @param {function} [blobAtRef]  (commit, path) => Buffer|null, the source lock's verifier
 * @returns {{subject, records: Map<string, object>, sources: object[], warnings: string[]}}
 * @throws {PresentationError} when a selected source is missing, unpinned, unverified or ambiguous
 */
export function loadEvidence(pkg, { root, blobAtRef = null } = {}) {
  if (!root || !isAbsolute(root)) throw new PresentationError("loadEvidence needs an absolute repository root");
  if (!pkg.draft && !blobAtRef) {
    throw new PresentationError("a pinned evidence package needs a blob reader to verify its source lock; pass blobAtRef or mark the package draft");
  }
  const records = new Map();
  const sources = [];
  const warnings = [];

  for (const r of pkg.records) {
    let bytes;
    try {
      bytes = readFileSync(join(root, r.path));
    } catch (e) {
      throw new PresentationError(`evidence "${r.id}": ${r.path} could not be read (${(e && e.code) || e})`, { recordId: r.id });
    }
    const sha256 = createHash("sha256").update(bytes).digest("hex");
    let file;
    try {
      file = JSON.parse(bytes.toString("utf8"));
    } catch (e) {
      throw new PresentationError(`evidence "${r.id}": ${r.path} is not JSON (${(e && e.message) || e})`, { recordId: r.id });
    }

    // ---- the source lock -----------------------------------------------------------------
    if (pkg.draft) {
      warnings.push(`evidence "${r.id}": DRAFT - ${r.path} was read from the working tree at ${sha256.slice(0, 12)} with no commit behind it; this dossier is not bound to committed bytes`);
    } else {
      if (sha256 !== r.sha256) {
        throw new PresentationError(
          `evidence "${r.id}": ${r.path} hashes ${sha256} but the package declares ${r.sha256}. ` +
          "The working tree does not hold the bytes this dossier was written against.",
          { recordId: r.id },
        );
      }
      const committed = blobAtRef(pkg.repoCommit, r.path);
      if (!committed) {
        throw new PresentationError(
          `evidence "${r.id}": ${r.path} could not be read at ${pkg.repoCommit.slice(0, 12)}, so its source lock cannot be verified. ` +
          "An unreadable commit is not a verified one.",
          { recordId: r.id },
        );
      }
      const committedSha = createHash("sha256").update(committed).digest("hex");
      if (committedSha !== sha256) {
        throw new PresentationError(
          `evidence "${r.id}": ${r.path} in the working tree hashes ${sha256} but at ${pkg.repoCommit.slice(0, 12)} it hashes ${committedSha}; ` +
          "the dossier would be built from uncommitted bytes.",
          { recordId: r.id },
        );
      }
    }

    const source = {
      id: r.id, kind: r.kind, path: r.path, sha256,
      repoCommit: pkg.draft ? null : pkg.repoCommit,
      draft: pkg.draft,
      bundleAt: typeof file.at === "string" ? file.at : null,
      outcome: file.outcome ?? null,
    };
    if (file.outcome && file.outcome !== "success") {
      // NOT fatal, and the distinction matters: push/53's predecessor failed on its image items
      // while its Marrow Vaults quest update landed and was read back ok and persisted in full.
      // Every capture it supplies is admitted on its own merits by captureProblem().
      warnings.push(`evidence "${r.id}": ${r.path} is from a run whose outcome was "${file.outcome}"; each capture it supplies is admitted on its own merits`);
    }

    if (r.kind === "quest") {
      const { admitted, refused, matched } = selectCaptures(file, { ...r.capture });
      const mine = admitted.filter((c) => c.input.id === r.questId);
      if (!mine.length) {
        const why = refused.filter((x) => x.capture.input && x.capture.input.id === r.questId).map((x) => x.problem);
        throw new PresentationError(
          `evidence "${r.id}": ${r.path} has no admissible ${r.capture.proc} capture for ${r.questId} matching the selector` +
          (why.length ? ` (${matched.length} matched the selector; refused because it ${why.join("; it ")})` : ""),
          { recordId: r.id },
        );
      }
      if (mine.length > 1) {
        throw new PresentationError(
          `evidence "${r.id}": the selector matches ${mine.length} admissible captures of ${r.questId} (${mine.map((c) => c.at).join(", ")}). ` +
          "Pin one by \"at\" or \"snapshotKey\"; choosing between them by array order is how a stale read wins.",
          { recordId: r.id },
        );
      }
      const cap = mine[0];
      const problem = questProblem(cap.data);
      if (problem) throw new PresentationError(`evidence "${r.id}": the quest record for ${r.questId} ${problem}`, { recordId: r.id });
      source.capturedAt = cap.at;
      source.entityId = r.questId;
      source.snapshotKey = cap.snapshotKey ?? null;
      records.set(r.id, { ...r, quest: cap.data, capturedAt: cap.at, source });
    } else if (r.kind === "aiRecords" || r.kind === "assetRecords") {
      const { admitted, refused } = selectCaptures(file, { ...r.capture });
      const wanted = r.kind === "aiRecords"
        ? admitted.filter((c) => typeof c.data.username === "string" && typeof c.data.avatar === "string")
        : admitted.filter((c) => typeof c.data.name === "string" && typeof c.data.image === "string");
      if (!wanted.length) {
        throw new PresentationError(
          `evidence "${r.id}": ${r.path} has no admissible ${r.capture.proc} capture carrying the fields a presentation needs` +
          (refused.length ? ` (${refused.length} matched and were refused: ${refused[0].problem})` : ""),
          { recordId: r.id },
        );
      }
      // Within one record the same entity may legitimately appear twice; the later capture wins and
      // an equal-timestamp disagreement is a conflict, the same rule used across records.
      const byEntity = new Map();
      for (const c of wanted) {
        const id = c.data[PROC_BODY_ID[c.proc]];
        const entry = r.kind === "aiRecords"
          ? { entityId: id, name: c.data.username, url: c.data.avatar, field: "avatar", capturedAt: c.at, snapshotKey: c.snapshotKey ?? null }
          : { entityId: id, name: c.data.name, url: c.data.image, field: "image", capturedAt: c.at, snapshotKey: c.snapshotKey ?? null };
        const prior = byEntity.get(id);
        if (!prior) { byEntity.set(id, entry); continue; }
        if (entry.capturedAt > prior.capturedAt) byEntity.set(id, entry);
        else if (entry.capturedAt === prior.capturedAt && entry.url !== prior.url) {
          throw new PresentationError(
            `evidence "${r.id}": two captures of ${id} at the same instant (${entry.capturedAt}) disagree about its ${entry.field}; ` +
            "nothing in the evidence decides which is current.",
            { recordId: r.id },
          );
        }
      }
      source.capturedAt = [...byEntity.values()].map((e) => e.capturedAt).sort().pop() ?? null;
      source.count = byEntity.size;
      source.refusedCaptures = refused.length;
      if (refused.length) {
        warnings.push(`evidence "${r.id}": ${refused.length} matching capture(s) were refused as inadmissible (first: ${refused[0].problem})`);
      }
      records.set(r.id, { ...r, entities: [...byEntity.values()], source });
    } else if (r.kind === "imagePack") {
      if (!file.imagePack) throw new PresentationError(`evidence "${r.id}": ${r.path} carries no imagePack block`, { recordId: r.id });
      // ONE OWNER for the pack contract: the runner's parser, not a second copy of its five rules.
      const { pack, errors } = normalizeImagePack(file.imagePack, {
        imgSizes: file.imgSizes || {},
        names: Object.keys(file.imagePack.files || {}),
      });
      if (!pack) throw new PresentationError(`evidence "${r.id}": ${r.path} imagePack is invalid - ${errors.join("; ")}`, { recordId: r.id });
      source.ref = pack.ref;
      source.count = Object.keys(pack.files).length;
      records.set(r.id, { ...r, pack, source });
    } else {
      const idmap = file.idmap;
      if (!idmap || typeof idmap !== "object" || Array.isArray(idmap)) throw new PresentationError(`evidence "${r.id}": ${r.path} carries no idmap`, { recordId: r.id });
      source.capturedAt = typeof file.at === "string" ? file.at : null;
      source.count = Object.keys(idmap).length;
      records.set(r.id, { ...r, idmap, source });
    }
    sources.push(source);
  }

  return { subject: pkg.subject, repoCommit: pkg.repoCommit, draft: pkg.draft, records, sources, warnings };
}

/** Records of one kind, in package order. */
export const ofKind = (loaded, kind) => [...loaded.records.values()].filter((r) => r.kind === kind);

/**
 * Merge entity observations across records: the newest capture per entity wins, and two records
 * that observe the same entity at the same instant with different content are a conflict.
 *
 * The bundle EXPORT time is deliberately not consulted. Ranking by it is what let an older
 * `before` read of a keeper beat the newer `after` read sitting in the same file.
 */
export function currentByEntity(records) {
  const best = new Map();
  const conflicts = [];
  for (const rec of records) {
    for (const e of rec.entities) {
      const entry = { ...e, source: rec.id };
      const prior = best.get(e.entityId);
      if (!prior) { best.set(e.entityId, entry); continue; }
      if (entry.capturedAt > prior.capturedAt) best.set(e.entityId, entry);
      else if (entry.capturedAt === prior.capturedAt && entry.url !== prior.url) {
        conflicts.push(
          `${e.entityId}: records "${prior.source}" and "${rec.id}" both observe it at ${entry.capturedAt} but disagree about its ${e.field}; ` +
          "nothing in the evidence decides which is current",
        );
      }
    }
  }
  return { best, conflicts };
}

/** Every observation across every record, for telling stale art from somebody else's art. */
export function allObservations(records) {
  return records.flatMap((rec) => rec.entities.map((e) => ({ ...e, source: rec.id })));
}
