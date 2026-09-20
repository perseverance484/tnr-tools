// The presentation dossier: one source-bound read model (plan §4.1).
//
// Everything a presentation is allowed to assert lives here, and every hard fact carries a pointer
// to the evidence record it came from, so an audit can answer "where did this number/name/image
// come from?" without reconstructing the session. The dossier is a DERIVATIVE (plan P7): it owns
// nothing, it restates nothing by hand, and rebuilding it from the same committed records produces
// the same document.
//
// IT ALSO CARRIES ITS SOURCE LOCK. `sources.repoCommit` is the commit every selected record was
// verified against; a draft build says so instead. A hash computed over whatever the working tree
// held was provenance-shaped and proved nothing (independent review F3).
//
// LOCATIONS ARE THE PART TO READ TWICE (plan §5.5). A top-level location is a subject the content
// model has - here, a quest that is a component of the event. A scene background is an IMAGE an
// objective shows. The Godstorm poster listed Upper Court, Binding Dais Active and Binding Dais
// Released as the event's locations; those are three asset records, two of which are the same room
// in two states. They are collected below under `sceneAssets`, with the objectives that use them,
// and the lint refuses to let one be named as a location.

import { createHash } from "node:crypto";
import { PresentationError } from "./errors.mjs";
import { ofKind, currentByEntity, allObservations } from "./evidence.mjs";
import { extractStructure, cadenceOf, cadenceText } from "./structure.mjs";
import { extractRewards } from "./rewards.mjs";
import { extractRoster, roleSequence, keepersOf } from "./roster.mjs";
import { buildAssetRegistry } from "./assets.mjs";
import { resolveNarrative } from "./narrative.mjs";

export const DOSSIER_SCHEMA = "tnr.presentation.dossier.v2";

/**
 * Build the dossier.
 *
 * @param {object} loaded  the result of loadEvidence()
 * @param {object} spec    a parsed presentation spec (supplies the annotations, never the facts)
 * @param {string} root    repository root
 * @param {function} [blobAtRef]  (ref, path) => Buffer|null; see assets.mjs
 */
export function buildDossier(loaded, spec, { root, blobAtRef = null } = {}) {
  const questRecords = ofKind(loaded, "quest");
  if (!questRecords.length) throw new PresentationError("the evidence package selects no quest record, so there is no structure to present");

  const provenance = {};
  const note = (path, recordId) => { provenance[path] = recordId; };
  const problems = [];

  const quests = {};
  const structures = [];
  for (const rec of questRecords) {
    quests[rec.questId] = rec.quest;
    const s = extractStructure(rec.quest, rec.id);
    structures.push(s);
    note(`structure.${s.questId}`, rec.id);
    note(`structure.${s.questId}.counts.battles`, rec.id);
    note(`structure.${s.questId}.counts.objectives`, rec.id);
    note(`structure.${s.questId}.hidden`, rec.id);
    note(`structure.${s.questId}.entryObjectiveId`, rec.id);
  }

  // Current art/name per entity, resolved by CAPTURE time with conflicts refused rather than
  // broken by array order (F3). aiRecords and assetRecords share one merge because the question
  // "which observation is current" has one answer regardless of entity class.
  const aiSources = ofKind(loaded, "aiRecords");
  const assetSources = ofKind(loaded, "assetRecords");
  const ai = currentByEntity(aiSources);
  const assets = currentByEntity(assetSources);
  problems.push(...ai.conflicts, ...assets.conflicts);

  const roster = extractRoster(structures, ai.best, spec.roles);
  problems.push(...roster.problems);
  for (const e of roster.entries) if (e.source) note(`roster.ai:${e.aiId}.name`, e.source);

  const encounters = structures.map((s) => {
    const roles = roleSequence(s, spec.roles);
    const cadence = s.successPathLinear ? cadenceOf(roles) : { unit: [], repeats: 0, exact: false };
    const keepers = keepersOf(s, spec.roles);
    note(`encounters.${s.questId}.sequence`, s.source);
    return {
      questId: s.questId,
      name: s.name,
      battles: s.encounters.length,
      keepers: keepers.length,
      keeperObjectiveIds: keepers.map((e) => e.objectiveId),
      sequence: s.encounters.map((e) => ({ index: e.index, objectiveId: e.objectiveId, aiIds: e.aiIds, role: spec.roles[e.aiIds[0]] ?? null, onSuccessPath: e.onSuccessPath })),
      cadence,
      cadenceText: cadenceText(cadence),
      successPathLinear: s.successPathLinear,
    };
  });

  const rewards = {};
  for (const rec of questRecords) {
    const s = structures.find((x) => x.questId === rec.questId);
    rewards[rec.questId] = extractRewards(rec.quest, s);
    note(`rewards.${rec.questId}`, rec.id);
    note(`rewards.${rec.questId}.fullClear`, rec.id);
  }

  // EVERY entity that needs art, not only the roster (F7): each AI, each component's listing image,
  // and each scene asset a selected record describes. A binding to anything else is reported by the
  // registry rather than ignored.
  const artEntities = [];
  for (const e of roster.entries) {
    const known = ai.best.get(e.aiId) || null;
    artEntities.push({
      entity: `ai:${e.aiId}`, entityId: e.aiId, kind: "ai", field: "avatar",
      name: e.name, liveUrl: known ? known.url : null,
      source: known ? known.source : null, capturedAt: known ? known.capturedAt : null,
    });
  }
  for (const s of structures) {
    artEntities.push({
      entity: `quest:${s.questId}`, entityId: s.questId, kind: "quest", field: "image",
      name: s.name, liveUrl: s.image,
      source: s.source, capturedAt: (loaded.sources.find((x) => x.id === s.source) || {}).capturedAt ?? null,
    });
  }
  // Scene assets belong to the registry only when this subject actually shows them. A selected
  // capture may cover assets from a neighbouring workstream; counting those would inflate art
  // readiness with images no tile will ever use.
  const usedAssetIds = new Set(structures.flatMap((s) => [...s.sceneBackgroundIds, ...s.sceneCharacterIds]));
  for (const [entityId, obs] of assets.best) {
    if (!usedAssetIds.has(entityId) && !Object.prototype.hasOwnProperty.call(spec.assets, `asset:${entityId}`)) continue;
    artEntities.push({
      entity: `asset:${entityId}`, entityId, kind: "asset", field: obs.field,
      name: obs.name, liveUrl: obs.url, source: obs.source, capturedAt: obs.capturedAt,
    });
  }

  const registry = buildAssetRegistry({
    entities: artEntities,
    packs: ofKind(loaded, "imagePack"),
    uploads: ofKind(loaded, "uploads"),
    bindings: spec.assets,
    observations: [...allObservations(aiSources), ...allObservations(assetSources)],
    root,
    blobAtRef,
  });
  for (const e of registry.entries) if (e.provenance.record) note(`assets.${e.entity}`, e.provenance.record);

  const knownNames = [
    ...structures.map((s) => s.name),
    ...roster.entries.map((e) => e.name).filter(Boolean),
    ...[...assets.best.values()].map((a) => a.name).filter(Boolean),
    loaded.subject.title,
    ...(loaded.subject.components ?? []),
  ];
  const narrative = resolveNarrative(structures, quests, spec.story, knownNames);
  problems.push(...narrative.problems);

  const locations = structures.map((s) => ({ key: `quest:${s.questId}`, name: s.name, kind: "component", source: s.source }));
  const sceneAssets = [];
  for (const s of structures) {
    const record = quests[s.questId];
    const reachable = new Set(s.reachableIds);
    for (const id of s.sceneBackgroundIds) {
      const usedBy = (record.content.objectives || [])
        .filter((o) => o.sceneBackground === id && reachable.has(o.id))
        .map((o) => o.id);
      sceneAssets.push({ key: `asset:${id}`, kind: "scene-background", component: s.questId, usedBy, source: s.source });
    }
    for (const id of s.sceneCharacterIds) {
      sceneAssets.push({ key: `asset:${id}`, kind: "scene-character", component: s.questId, usedBy: [], source: s.source });
    }
  }

  const dossier = {
    schema: DOSSIER_SCHEMA,
    subject: {
      type: loaded.subject.type ?? "event",
      title: loaded.subject.title,
      components: structures.map((s) => s.name),
    },
    sources: {
      repoCommit: loaded.repoCommit,
      draft: loaded.draft,
      records: loaded.sources,
    },
    structure: Object.fromEntries(structures.map((s) => [s.questId, s])),
    encounters,
    roster: roster.entries,
    rewards,
    dialogue: { byComponent: Object.fromEntries(structures.map((s) => [s.questId, s.dialogIds])) },
    narrative: narrative.blocks,
    locations,
    sceneAssets,
    assets: { entries: registry.entries, coverage: registry.coverage, packFiles: registry.packFiles },
    provenance,
    warnings: [...loaded.warnings, ...narrative.warnings],
    problems,
    totals: {
      components: structures.length,
      battles: encounters.reduce((n, e) => n + e.battles, 0),
      keepers: encounters.reduce((n, e) => n + e.keepers, 0),
      distinctAi: roster.entries.length,
    },
  };

  dossier.hash = createHash("sha256").update(stableJson(dossier)).digest("hex");
  return dossier;
}

/** Deterministic JSON: key order never depends on how the object happened to be built. */
export function stableJson(value) {
  const walk = (v) => {
    if (Array.isArray(v)) return v.map(walk);
    if (v instanceof Map) return Object.fromEntries([...v.entries()].sort().map(([k, x]) => [k, walk(x)]));
    if (v && typeof v === "object") {
      return Object.fromEntries(Object.keys(v).sort().filter((k) => v[k] !== undefined).map((k) => [k, walk(v[k])]));
    }
    return v;
  };
  return JSON.stringify(walk(value));
}
