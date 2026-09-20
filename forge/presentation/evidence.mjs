// Explicit committed evidence loading (plan §4.1).
//
// A dossier is built from sources somebody NAMED, at paths inside this repository, and from
// nothing else. There is no scan of harvests/, no "most recent bundle wins", no fallback to a
// planning document: the Godstorm posters went wrong because facts arrived from whatever was
// nearest in the conversation, and the fix is that an evidence package is a committed list of
// exact records with exact selectors.
//
// An evidence package selects sources. It does NOT carry facts - no reward numbers, no roster
// names, no battle counts. Those are read out of the records it points at, which is the whole
// difference between a derivative and a second content database (plan P7).
//
// Four record kinds, deliberately few and each with one explicit selector:
//
//   quest       a `quests.get` capture inside a results bundle, named by its quest id.
//   aiRecords   every record in a results bundle carrying a userId and an avatar. No id list:
//               which AIs matter is decided by the quest's own battle nodes, so listing them here
//               would be the evidence package starting to own the roster.
//   imagePack   a committed manifest's `imagePack` block - repository path, commit, SHA-256 per
//               logical image name. Parsed by the runner's own contract, not a second copy of it.
//   uploads     a results bundle's `idmap`, which records the URL each uploaded image became.
//
// FRESHNESS IS VISIBLE, NOT ASSUMED (plan P5). Every loaded record carries the bundle timestamp,
// the capture timestamp where there is one, the file's SHA-256 and whether the run that produced
// it succeeded. A capture from a FAILED run is still evidence when the capture itself read back
// ok - the Marrow Vaults quest update landed and was captured in a run whose later items errored -
// so the run outcome is recorded and warned about rather than used to discard a good read.

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, isAbsolute } from "node:path";
import { PresentationError } from "./errors.mjs";
import { normalizeImagePack, pathProblem } from "../src/runner/imgpack.mjs";

export const EVIDENCE_SCHEMA = "tnr.presentation.evidence.v1";

const KINDS = new Set(["quest", "aiRecords", "imagePack", "uploads"]);
const RECORD_KEYS = new Set(["id", "kind", "path", "questId", "note"]);
const PACKAGE_KEYS = new Set(["schema", "subject", "records", "note"]);
const SUBJECT_KEYS = new Set(["type", "title", "components"]);

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
    if (r.kind === "quest" && (typeof r.questId !== "string" || !r.questId)) {
      throw new PresentationError(`${where} (${r.id}): a quest record must name the questId it selects`);
    }
    if (r.kind !== "quest" && r.questId != null) {
      throw new PresentationError(`${where} (${r.id}): questId is only meaningful on a quest record`);
    }
    return Object.freeze({ ...r });
  });
  return Object.freeze({ ...raw, records: Object.freeze(records) });
}

/** Deep-collect every object carrying a userId and an avatar. */
function collectAiRecords(node, into) {
  if (Array.isArray(node)) {
    for (const v of node) collectAiRecords(v, into);
    return;
  }
  if (!node || typeof node !== "object") return;
  if (typeof node.userId === "string" && typeof node.avatar === "string" && typeof node.username === "string") {
    into.push({ aiId: node.userId, name: node.username, avatar: node.avatar });
  }
  for (const v of Object.values(node)) collectAiRecords(v, into);
}

/**
 * Load every record an evidence package selects.
 *
 * @param {object} pkg    a parsed evidence package
 * @param {string} root   repository root; every path resolves under it
 * @returns {{subject, records: Map<string, object>, sources: object[], warnings: string[]}}
 * @throws {PresentationError} when a selected source is missing, unparseable or unverified
 */
export function loadEvidence(pkg, { root } = {}) {
  if (!root || !isAbsolute(root)) throw new PresentationError("loadEvidence needs an absolute repository root");
  const records = new Map();
  const sources = [];
  const warnings = [];

  for (const r of pkg.records) {
    let text;
    try {
      text = readFileSync(join(root, r.path), "utf8");
    } catch (e) {
      throw new PresentationError(`evidence "${r.id}": ${r.path} could not be read (${(e && e.code) || e})`, { recordId: r.id });
    }
    let file;
    try {
      file = JSON.parse(text);
    } catch (e) {
      throw new PresentationError(`evidence "${r.id}": ${r.path} is not JSON (${(e && e.message) || e})`, { recordId: r.id });
    }
    const sha256 = createHash("sha256").update(text).digest("hex");
    const source = { id: r.id, kind: r.kind, path: r.path, sha256, bundleAt: file.at ?? null, outcome: file.outcome ?? null };

    if (file.outcome && file.outcome !== "success") {
      // NOT fatal, and the distinction matters: push/53's predecessor failed on its image items
      // while its Marrow Vaults quest update landed and was read back. A per-capture check is the
      // honest gate; the run outcome is provenance the reviewer should see.
      warnings.push(`evidence "${r.id}": ${r.path} is from a run whose outcome was "${file.outcome}"; each capture it supplies is checked individually`);
    }

    if (r.kind === "quest") {
      const cap = (file.captures || []).find(
        (c) => c && (c.proc === "quests.get" || c.proc === "quest.get") && c.input && c.input.id === r.questId,
      );
      if (!cap) throw new PresentationError(`evidence "${r.id}": ${r.path} carries no quests.get capture for ${r.questId}`, { recordId: r.id });
      if (cap.ok !== true) throw new PresentationError(`evidence "${r.id}": the quests.get capture for ${r.questId} did not read back ok`, { recordId: r.id });
      if (!cap.data || typeof cap.data !== "object") throw new PresentationError(`evidence "${r.id}": the quests.get capture for ${r.questId} carries no record`, { recordId: r.id });
      if (cap.data.id !== r.questId) {
        throw new PresentationError(`evidence "${r.id}": the capture for ${r.questId} holds quest ${JSON.stringify(cap.data.id)}`, { recordId: r.id });
      }
      source.capturedAt = cap.at ?? file.at ?? null;
      source.entityId = r.questId;
      records.set(r.id, { ...r, quest: cap.data, capturedAt: source.capturedAt, source });
    } else if (r.kind === "aiRecords") {
      const found = [];
      collectAiRecords(file, found);
      if (!found.length) throw new PresentationError(`evidence "${r.id}": ${r.path} carries no AI records (a userId, username and avatar together)`, { recordId: r.id });
      source.capturedAt = file.at ?? null;
      source.count = found.length;
      records.set(r.id, { ...r, ai: found, capturedAt: source.capturedAt, source });
    } else if (r.kind === "imagePack") {
      if (!file.imagePack) throw new PresentationError(`evidence "${r.id}": ${r.path} carries no imagePack block`, { recordId: r.id });
      // ONE OWNER for the pack contract: the runner's parser, not a second copy of its five rules.
      // imgSizes is passed so rule 4 (the two ledgers must agree) is checked here too.
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
      if (!idmap || typeof idmap !== "object") throw new PresentationError(`evidence "${r.id}": ${r.path} carries no idmap`, { recordId: r.id });
      source.capturedAt = file.at ?? null;
      source.count = Object.keys(idmap).length;
      records.set(r.id, { ...r, idmap, capturedAt: source.capturedAt, source });
    }
    sources.push(source);
  }

  return { subject: pkg.subject, records, sources, warnings };
}

/** Records of one kind, in package order. */
export const ofKind = (loaded, kind) => [...loaded.records.values()].filter((r) => r.kind === kind);
