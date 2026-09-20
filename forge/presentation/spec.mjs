// The versioned presentation spec parser (plan §4.2).
//
// A spec says HOW to present a dossier. It may not say WHAT is true. That single line is the whole
// design: the Godstorm poster carried 125,000 ryo and a five-enemy roster as authored text, so
// nothing could disagree with it when the content changed underneath.
//
// So the parser is fail-closed on a CLOSED key set, twice over:
//
//   1. unknown keys are refused, at every level, the same way the runner's pre-send validator
//      refuses an unknown key rather than letting the server drop it silently;
//   2. keys that would let a spec RESTATE a dossier fact are refused by name, with a message
//      saying which dossier key owns that number instead. Those are the ones that matter: a typo
//      is an accident, but a `rewards` block is a second content database starting.
//
// What a spec legitimately owns: titles, section order, labels, short narrative summaries and
// their source anchors, roster coverage, which approved file is an entity's art when more than one
// exists, and whether scene art may be captioned.

import { PresentationError } from "./errors.mjs";
import { ROLES } from "./roster.mjs";

export const SPEC_SCHEMA = "tnr.presentation.spec.v1";

const SPEC_KEYS = new Set([
  "schema", "evidence", "template", "title", "subtitle", "sections",
  "story", "roles", "roster", "locations", "sceneDetail", "assets", "labels", "note",
]);
const STORY_KEYS = new Set(["text", "sourceObjectives"]);
const ROSTER_KEYS = new Set(["coverage", "entries", "groupBy"]);
const TEMPLATES = new Set(["event-poster", "staff-brief"]);
const COVERAGE = new Set(["all", "selection"]);

// Keys a spec must never carry, each mapped to the dossier key that owns the fact. Refusing these
// BY NAME rather than as "unknown key" is the point: the message has to teach, because the author
// reaching for `rewards` is doing the exact thing that produced a poster full of removed cash-outs.
const OWNED_ELSEWHERE = new Map([
  ["rewards", "dossier.rewards - derived from the reachable reward nodes of the current capture"],
  ["reward", "dossier.rewards"],
  ["cashOuts", "dossier.rewards.intermediateCashOuts"],
  ["chests", "dossier.rewards.rewardItems"],
  ["battles", "dossier.structure[].counts.battles"],
  ["battleCount", "dossier.structure[].counts.battles"],
  ["keepers", "dossier.encounters[].keepers"],
  ["encounters", "dossier.encounters"],
  ["cadence", "dossier.encounters[].cadence - derived from the validated role annotations"],
  ["rosterNames", "dossier.roster[].name"],
  ["aiNames", "dossier.roster[].name"],
  ["structure", "dossier.structure"],
  ["counts", "dossier.structure[].counts"],
  ["hidden", "dossier.structure[].hidden"],
]);

const only = (obj, allowed, where) => {
  for (const k of Object.keys(obj)) {
    const owner = OWNED_ELSEWHERE.get(k);
    if (owner) {
      throw new PresentationError(
        `${where}: "${k}" is a dossier fact, not a presentation choice. It resolves from ${owner}. ` +
        "A spec that restates a hard number is a second content database and can go stale against the game.",
      );
    }
    if (!allowed.has(k)) throw new PresentationError(`${where}: unknown key "${k}"`);
  }
};

/**
 * Parse and check a presentation spec. Pure: reads nothing, resolves nothing against a dossier.
 * Cross-checks that need the dossier (do these objective ids exist? is this a real AI?) belong to
 * the extractors and the lint, which have one.
 */
export function parseSpec(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) throw new PresentationError("presentation spec is not an object");
  if (raw.schema !== SPEC_SCHEMA) {
    throw new PresentationError(`presentation spec schema must be "${SPEC_SCHEMA}", found ${JSON.stringify(raw.schema)}`);
  }
  only(raw, SPEC_KEYS, "spec");

  if (typeof raw.evidence !== "string" || !raw.evidence) throw new PresentationError("spec must name the evidence package it presents");
  if (!TEMPLATES.has(raw.template)) {
    throw new PresentationError(`spec template must be one of ${[...TEMPLATES].join(", ")}, found ${JSON.stringify(raw.template)}`);
  }
  if (typeof raw.title !== "string" || !raw.title.trim()) throw new PresentationError("spec must carry a title");

  const story = {};
  for (const [key, block] of Object.entries(raw.story ?? {})) {
    const where = `spec.story.${key}`;
    if (!block || typeof block !== "object" || Array.isArray(block)) throw new PresentationError(`${where} is not an object`);
    only(block, STORY_KEYS, where);
    if (typeof block.text !== "string" || !block.text.trim()) throw new PresentationError(`${where} has no text`);
    if (!Array.isArray(block.sourceObjectives) || !block.sourceObjectives.length) {
      throw new PresentationError(`${where}: a summary must cite at least one source objective id (plan P2)`);
    }
    for (const id of block.sourceObjectives) {
      if (typeof id !== "string" || !id) throw new PresentationError(`${where}: a source objective id must be a non-empty string`);
    }
    story[key] = { text: block.text, sourceObjectives: [...block.sourceObjectives] };
  }

  const roles = {};
  for (const [aiId, role] of Object.entries(raw.roles ?? {})) {
    if (typeof role !== "string" || !ROLES.includes(role)) {
      throw new PresentationError(`spec.roles.${aiId}: role must be one of ${ROLES.join(", ")}, found ${JSON.stringify(role)}`);
    }
    roles[aiId] = role;
  }

  const rosterRaw = raw.roster ?? { coverage: "all" };
  if (!rosterRaw || typeof rosterRaw !== "object" || Array.isArray(rosterRaw)) throw new PresentationError("spec.roster is not an object");
  only(rosterRaw, ROSTER_KEYS, "spec.roster");
  if (!COVERAGE.has(rosterRaw.coverage)) {
    throw new PresentationError(`spec.roster.coverage must be "all" or "selection", found ${JSON.stringify(rosterRaw.coverage)}`);
  }
  if (rosterRaw.coverage === "selection" && (!Array.isArray(rosterRaw.entries) || !rosterRaw.entries.length)) {
    throw new PresentationError('spec.roster.coverage "selection" must list the entries it selects');
  }
  if (rosterRaw.coverage === "all" && rosterRaw.entries != null && !Array.isArray(rosterRaw.entries)) {
    throw new PresentationError("spec.roster.entries must be an array of ai ids");
  }

  const assets = {};
  for (const [entity, path] of Object.entries(raw.assets ?? {})) {
    if (!/^(ai|asset|quest):[A-Za-z0-9_-]+$/.test(entity)) {
      throw new PresentationError(`spec.assets: ${JSON.stringify(entity)} is not an entity key ("ai:<id>", "asset:<id>" or "quest:<id>")`);
    }
    if (typeof path !== "string" || !path) throw new PresentationError(`spec.assets["${entity}"] must be a repository path`);
    assets[entity] = path;
  }

  const locations = [];
  for (const loc of raw.locations ?? []) {
    if (typeof loc !== "string" || !loc) throw new PresentationError("spec.locations entries must be non-empty strings");
    locations.push(loc);
  }

  return Object.freeze({
    schema: SPEC_SCHEMA,
    evidence: raw.evidence,
    template: raw.template,
    title: raw.title,
    subtitle: typeof raw.subtitle === "string" ? raw.subtitle : null,
    sections: Array.isArray(raw.sections) ? [...raw.sections] : null,
    story,
    roles,
    roster: { coverage: rosterRaw.coverage, entries: rosterRaw.entries ? [...rosterRaw.entries] : null, groupBy: rosterRaw.groupBy ?? null },
    locations,
    sceneDetail: raw.sceneDetail === true,
    assets,
    labels: raw.labels && typeof raw.labels === "object" ? { ...raw.labels } : {},
  });
}
