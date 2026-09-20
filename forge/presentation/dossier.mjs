// The presentation dossier: one source-bound read model (plan §4.1).
//
// Everything a presentation is allowed to assert lives here, and every hard fact carries a pointer
// to the evidence record it came from, so an audit can answer "where did this number/name/image
// come from?" without reconstructing the session. The dossier is a DERIVATIVE (plan P7): it owns
// nothing, it restates nothing by hand, and rebuilding it from the same committed records produces
// the same document.
//
// LOCATIONS ARE THE PART TO READ TWICE (plan §5.5). A top-level location is a subject the content
// model has - here, a quest that is a component of the event. A scene background is an IMAGE an
// objective shows. The Godstorm poster listed Upper Court, Binding Dais Active and Binding Dais
// Released as the event's locations; those are three asset records, two of which are the same room
// in two states. They are collected below under `sceneAssets`, with the objectives that use them,
// and the lint refuses to let one be named as a location.

import { createHash } from "node:crypto";
import { PresentationError } from "./errors.mjs";
import { ofKind } from "./evidence.mjs";
import { extractStructure, cadenceOf, cadenceText } from "./structure.mjs";
import { extractRewards } from "./rewards.mjs";
import { extractRoster, roleSequence, keepersOf } from "./roster.mjs";
import { buildAssetRegistry } from "./assets.mjs";
import { resolveNarrative } from "./narrative.mjs";

export const DOSSIER_SCHEMA = "tnr.presentation.dossier.v1";

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
  }

  const aiSources = ofKind(loaded, "aiRecords");
  const roster = extractRoster(structures, aiSources, spec.roles);
  for (const e of roster.entries) if (e.source) note(`roster.ai:${e.aiId}.name`, e.source);

  // Encounters: the sequence is evidence, the cadence is derived from it through the validated
  // role annotations. Neither is authored.
  const encounters = structures.map((s) => {
    const roles = roleSequence(s, spec.roles);
    const cadence = cadenceOf(roles);
    const keepers = keepersOf(s, spec.roles);
    note(`encounters.${s.questId}.sequence`, s.source);
    return {
      questId: s.questId,
      name: s.name,
      battles: s.encounters.length,
      keepers: keepers.length,
      keeperObjectiveIds: keepers.map((e) => e.objectiveId),
      sequence: s.encounters.map((e) => ({ index: e.index, objectiveId: e.objectiveId, aiIds: e.aiIds, role: spec.roles[e.aiIds[0]] ?? null })),
      cadence,
      cadenceText: cadenceText(cadence),
    };
  });

  const rewards = {};
  for (const rec of questRecords) {
    const s = structures.find((x) => x.questId === rec.questId);
    rewards[rec.questId] = extractRewards(rec.quest, s);
    note(`rewards.${rec.questId}`, rec.id);
    note(`rewards.${rec.questId}.fullClear`, rec.id);
  }

  // Every avatar observation, not just the newest, so the registry can tell a swap from stale art.
  const observations = aiSources.flatMap((rec) => rec.ai.map((a) => ({ ...a, capturedAt: rec.capturedAt, source: rec.id })));
  const registry = buildAssetRegistry({
    roster: roster.entries,
    aiIndex: roster.byId,
    packs: ofKind(loaded, "imagePack"),
    uploads: ofKind(loaded, "uploads"),
    bindings: spec.assets,
    observations,
    root,
    blobAtRef,
  });
  for (const e of registry.entries) if (e.provenance.record) note(`assets.${e.entity}`, e.provenance.record);

  const knownNames = [
    ...structures.map((s) => s.name),
    ...roster.entries.map((e) => e.name).filter(Boolean),
    loaded.subject.title,
    ...(loaded.subject.components ?? []),
  ];
  const narrative = resolveNarrative(structures, quests, spec.story, knownNames);

  // Top-level locations: the components themselves, and nothing that is merely drawn.
  const locations = structures.map((s) => ({ key: `quest:${s.questId}`, name: s.name, kind: "component", source: s.source }));
  const sceneAssets = [];
  for (const s of structures) {
    const record = quests[s.questId];
    for (const id of s.sceneBackgroundIds) {
      const usedBy = (record.content.objectives || [])
        .filter((o) => o.sceneBackground === id && s.reachableIds.includes(o.id))
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
      records: loaded.sources,
    },
    structure: Object.fromEntries(structures.map((s) => [s.questId, s])),
    encounters,
    roster: roster.entries,
    rewards,
    dialogue: {
      byComponent: Object.fromEntries(structures.map((s) => [s.questId, s.dialogIds])),
    },
    narrative: narrative.blocks,
    locations,
    sceneAssets,
    assets: {
      entries: registry.entries,
      coverage: registry.coverage,
      packFiles: registry.packFiles,
    },
    provenance,
    warnings: [...loaded.warnings, ...narrative.warnings],
    problems: [...roster.problems, ...narrative.problems],
    totals: {
      components: structures.length,
      battles: encounters.reduce((n, e) => n + e.battles, 0),
      keepers: encounters.reduce((n, e) => n + e.keepers, 0),
      distinctAi: roster.entries.length,
    },
  };

  // The dossier is content-addressed so a presentation can bind to the exact facts it was built
  // from: two builds of the same records give the same hash, and a changed record changes it.
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
