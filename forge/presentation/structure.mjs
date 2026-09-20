// Structure and encounter-sequence extraction (plan §5.1).
//
// Everything here is read off one captured quest record. Nothing is inferred from a scene
// background, a filename or a description: the Godstorm poster called Upper Court a "location"
// because an implementation asset name was allowed to become a semantic concept, and the rule that
// stops that is that structure comes from the objective graph and only from the objective graph.
//
// REACHABILITY, not enumeration. A quest record holds every objective node it has ever had; what
// a player can actually reach is the set the graph walks to from the entry node. The old Godstorm
// poster showed per-floor cash-outs that had already been removed, and a reward on an unreachable
// node is exactly that failure in the other direction - so the walk below is what decides which
// nodes count, and rewards.mjs reads only from it.

import { PresentationError } from "./errors.mjs";

const BATTLE_TASKS = new Set(["start_battle", "defeat_opponents"]);
const TERMINAL_TASKS = new Set(["win_quest", "fail_quest"]);

/** Every objective id an objective points at, whatever shape the pointer takes. */
export function successorsOf(objective) {
  const out = [];
  const push = (v) => { if (typeof v === "string" && v) out.push(v); };
  const n = objective.nextObjectiveId;
  if (Array.isArray(n)) {
    // dialog choices: [{text, nextObjectiveId}]
    for (const choice of n) {
      if (typeof choice === "string") push(choice);
      else if (choice && typeof choice === "object") push(choice.nextObjectiveId);
    }
  } else {
    push(n);
  }
  push(objective.failObjectiveId);
  push(objective.successObjectiveId);
  return out;
}

/** The AI ids a battle node fields. */
export function opponentsOf(objective) {
  const out = [];
  for (const key of ["opponentAIs", "attackers"]) {
    for (const entry of Array.isArray(objective[key]) ? objective[key] : []) {
      if (!entry || typeof entry !== "object") continue;
      for (const id of Array.isArray(entry.ids) ? entry.ids : []) if (typeof id === "string" && id) out.push(id);
    }
  }
  return out;
}

/**
 * Derive the structure of one captured quest record.
 *
 * @param {object} quest  a `quests.get` capture body
 * @param {string} recordId  the evidence record it came from, for provenance
 * @returns {object} the structure block for the dossier
 */
export function extractStructure(quest, recordId) {
  const content = quest && quest.content;
  if (!content || typeof content !== "object") throw new PresentationError(`quest ${quest && quest.id}: the capture carries no content`);
  const objectives = Array.isArray(content.objectives) ? content.objectives : [];
  if (!objectives.length) throw new PresentationError(`quest ${quest.id}: the capture carries no objectives`);

  const byId = new Map();
  for (const o of objectives) {
    if (!o || typeof o !== "object" || typeof o.id !== "string") throw new PresentationError(`quest ${quest.id}: an objective has no id`);
    if (byId.has(o.id)) throw new PresentationError(`quest ${quest.id}: duplicate objective id "${o.id}"`);
    byId.set(o.id, o);
  }

  // The entry node is the first objective as the record orders it: that is what the engine walks
  // and what `consecutiveObjectives` sequences. Choosing it by any other rule would be a guess.
  const entryId = objectives[0].id;
  const reachable = new Set();
  const danglingLinks = [];
  const stack = [entryId];
  while (stack.length) {
    const id = stack.pop();
    if (reachable.has(id)) continue;
    reachable.add(id);
    for (const next of successorsOf(byId.get(id))) {
      if (!byId.has(next)) { danglingLinks.push(`${id} -> ${next}`); continue; }
      if (!reachable.has(next)) stack.push(next);
    }
  }

  const reachableObjectives = objectives.filter((o) => reachable.has(o.id));
  const encounters = reachableObjectives
    .filter((o) => BATTLE_TASKS.has(o.task))
    .map((o, i) => ({
      index: i + 1,
      objectiveId: o.id,
      aiIds: opponentsOf(o),
      description: typeof o.description === "string" ? o.description : "",
    }));

  const dialog = reachableObjectives.filter((o) => o.task === "dialog");
  const terminals = reachableObjectives.filter((o) => TERMINAL_TASKS.has(o.task));

  return {
    questId: quest.id,
    name: quest.name,
    questType: quest.questType ?? null,
    questRank: quest.questRank ?? null,
    hidden: quest.hidden === true,
    consecutiveObjectives: quest.consecutiveObjectives === true,
    requiredLevel: quest.requiredLevel ?? null,
    prerequisiteQuestId: quest.prerequisiteQuestId ?? null,
    entryObjectiveId: entryId,
    counts: {
      objectives: objectives.length,
      reachableObjectives: reachableObjectives.length,
      battles: encounters.length,
      dialog: dialog.length,
      terminals: terminals.length,
      unreachable: objectives.length - reachableObjectives.length,
    },
    encounters,
    dialogIds: dialog.map((o) => o.id),
    terminalIds: terminals.map((o) => o.id),
    reachableIds: [...reachable],
    danglingLinks,
    // Scene assets are collected so the dossier can SAY they exist - and say that they are scene
    // art, not places. §5.5: a background variant is not a top-level location.
    sceneBackgroundIds: [...new Set(reachableObjectives.map((o) => o.sceneBackground).filter((v) => typeof v === "string" && v))],
    sceneCharacterIds: [...new Set(reachableObjectives.flatMap((o) => (Array.isArray(o.sceneCharacters) ? o.sceneCharacters : [])))],
    source: recordId,
  };
}

/**
 * The repeat pattern of a battle sequence, read through validated role annotations (plan §5.2).
 *
 * Derived, never annotated: given the role of each battle in order, this finds the shortest unit
 * that tiles the whole sequence exactly. Godstorm comes out as four recurring encounters then one
 * keeper, five times - which is the sentence the poster is supposed to be able to say without
 * anybody typing it.
 *
 * `exact` is false when the sequence does not tile cleanly; the caller reports the sequence rather
 * than a cadence, because a cadence that only nearly holds is the kind of claim this whole plan
 * exists to stop.
 *
 * @param {string[]} roles  one role per battle, in encounter order
 */
export function cadenceOf(roles) {
  const n = roles.length;
  if (!n) return { unit: [], repeats: 0, exact: false };
  for (let len = 1; len <= n; len++) {
    if (n % len) continue;
    let tiles = true;
    for (let i = len; i < n && tiles; i++) if (roles[i] !== roles[i % len]) tiles = false;
    if (!tiles) continue;
    const unit = [];
    for (const role of roles.slice(0, len)) {
      const last = unit[unit.length - 1];
      if (last && last.role === role) last.count += 1;
      else unit.push({ role, count: 1 });
    }
    return { unit, repeats: n / len, exact: true };
  }
  return { unit: [], repeats: 0, exact: false };
}

/** The cadence as one readable line, for a poster caption or a handoff. */
export function cadenceText(cadence) {
  if (!cadence.exact) return "no repeating pattern";
  const part = cadence.unit.map((u) => `${u.count} ${u.role} ${u.count === 1 ? "fight" : "fights"}`).join(" then ");
  return cadence.repeats === 1 ? part : `${part}, repeated ${cadence.repeats} times`;
}
