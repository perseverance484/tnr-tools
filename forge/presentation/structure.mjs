// Structure and encounter-sequence extraction (plan §5.1).
//
// Everything here is read off one captured quest record. Nothing is inferred from a scene
// background, a filename or a description: the Godstorm poster called Upper Court a "location"
// because an implementation asset name was allowed to become a semantic concept, and the rule that
// stops that is that structure comes from the objective graph and only from the objective graph.
//
// THE GRAPH, NOT THE ARRAY (independent review F4). The first version took `objectives[0]` as the
// entry and produced the encounter sequence by filtering the array in storage order, with a comment
// claiming that is how the engine walks it. The pinned source says otherwise: objectives.ts:153
// finds the objective nothing references and follows selected links, and quest.ts:1969 validates
// that exactly one such start exists. Swapping two array positions while changing no id and no edge
// therefore turned the cadence into "1 keeper then 8 recurring" and made a reachable opening
// dialogue look unreachable. Entry and order are now derived from the edges.
//
// SUCCESS EDGES ARE NOT FAILURE EDGES. A battle points forward on a win and at `fall` on a loss.
// Treating both as ordinary successors is what let an optional exit paying 20,000 ryo be read as
// the full clear (F5). The traversal below separates them, and rewards.mjs classifies against the
// paths that actually reach a `win_quest`.

import { PresentationError } from "./errors.mjs";

const BATTLE_TASKS = new Set(["start_battle", "defeat_opponents"]);
const WIN_TASKS = new Set(["win_quest"]);
const FAIL_TASKS = new Set(["fail_quest"]);
const TERMINAL_TASKS = new Set([...WIN_TASKS, ...FAIL_TASKS]);

/** Ids an objective points at on a SUCCESSFUL outcome, including each dialogue choice. */
export function successEdges(objective) {
  const out = [];
  const push = (v) => { if (typeof v === "string" && v) out.push(v); };
  const n = objective.nextObjectiveId;
  if (Array.isArray(n)) {
    for (const choice of n) {
      if (typeof choice === "string") push(choice);
      else if (choice && typeof choice === "object") push(choice.nextObjectiveId);
    }
  } else {
    push(n);
  }
  push(objective.successObjectiveId);
  return out;
}

/** Ids an objective points at on a FAILED outcome. */
export function failureEdges(objective) {
  const out = [];
  if (typeof objective.failObjectiveId === "string" && objective.failObjectiveId) out.push(objective.failObjectiveId);
  return out;
}

/** Every id an objective points at, either way. */
export const successorsOf = (objective) => [...successEdges(objective), ...failureEdges(objective)];

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

  // ENTRY: the objective nothing references, as the engine finds it (objectives.ts:153) and as the
  // editor validates it (quest.ts:1969). Zero or several is a structure this tool must not flatten
  // into a single sequence, so it says so instead of picking one.
  const referenced = new Set();
  const danglingLinks = [];
  for (const o of objectives) {
    for (const next of successorsOf(o)) {
      if (!byId.has(next)) { danglingLinks.push(`${o.id} -> ${next}`); continue; }
      referenced.add(next);
    }
  }
  const starts = objectives.filter((o) => !referenced.has(o.id)).map((o) => o.id);

  // A record can hold a DETACHED REMNANT: a node removed from the route whose edges were never
  // cleaned up. That is not a second entry, and refusing the whole record for it would turn "there
  // is a stale reward node here" - exactly the thing the rewards check exists to report - into a
  // build failure. So when several nodes are unreferenced, the entry is the one that can still
  // reach a win; the others are reported as orphans. Genuine ambiguity, where two of them reach a
  // win or none does, is still refused rather than guessed.
  const reachesWinFrom = (startId) => {
    const seen = new Set([startId]);
    const q = [startId];
    while (q.length) {
      const o = byId.get(q.shift());
      if (WIN_TASKS.has(o.task)) return true;
      for (const n of successEdges(o)) {
        if (!byId.has(n) || seen.has(n)) continue;
        seen.add(n);
        q.push(n);
      }
    }
    return false;
  };
  // A terminal is never an entry. Severing the last edge into `win` leaves it unreferenced, and a
  // rule that only asked "does it reach a win" would happily start the quest at its own ending.
  const candidates = starts.filter((id) => !TERMINAL_TASKS.has(byId.get(id).task));
  let entryId;
  let orphanStarts = [];
  if (candidates.length === 1) {
    entryId = candidates[0];
    orphanStarts = starts.filter((id) => id !== entryId);
  } else {
    const live = candidates.filter(reachesWinFrom);
    if (live.length !== 1) {
      throw new PresentationError(
        `quest ${quest.id}: expected exactly one entry objective that reaches a win (one that nothing points at), found ${live.length}` +
        ` among ${starts.length} unreferenced objective(s)${starts.length ? ` (${starts.join(", ")})` : ""}` +
        ". The engine walks from the unreferenced start; a presentation must not guess which one it is.",
      );
    }
    entryId = live[0];
    orphanStarts = starts.filter((id) => id !== entryId);
  }

  // ORDER: breadth-first along the edges from the entry, success edges before failure edges, each
  // node's own edge order preserved. Deterministic, and independent of where a node sits in the
  // stored array.
  const order = [];
  const reachable = new Set();
  const viaFailure = new Set();
  const queue = [entryId];
  reachable.add(entryId);
  while (queue.length) {
    const id = queue.shift();
    order.push(id);
    const o = byId.get(id);
    for (const next of successEdges(o)) {
      if (!byId.has(next) || reachable.has(next)) continue;
      reachable.add(next);
      queue.push(next);
    }
    for (const next of failureEdges(o)) {
      if (!byId.has(next)) continue;
      viaFailure.add(next);
      if (reachable.has(next)) continue;
      reachable.add(next);
      queue.push(next);
    }
  }

  // The SUCCESS PATH: nodes reachable from the entry along success edges only, that can also still
  // reach a win_quest along success edges. Anything reachable but outside it is optional or a
  // failure branch, and rewards.mjs must not read a full clear off it.
  const forwardOnly = new Set();
  const fq = [entryId];
  forwardOnly.add(entryId);
  while (fq.length) {
    const o = byId.get(fq.shift());
    for (const next of successEdges(o)) {
      if (!byId.has(next) || forwardOnly.has(next)) continue;
      forwardOnly.add(next);
      fq.push(next);
    }
  }
  const reachesWin = new Set();
  // reverse closure over success edges from every win terminal
  const predecessors = new Map();
  for (const o of objectives) {
    for (const next of successEdges(o)) {
      if (!byId.has(next)) continue;
      if (!predecessors.has(next)) predecessors.set(next, []);
      predecessors.get(next).push(o.id);
    }
  }
  const wq = objectives.filter((o) => WIN_TASKS.has(o.task)).map((o) => o.id);
  for (const id of wq) reachesWin.add(id);
  while (wq.length) {
    const id = wq.shift();
    for (const prev of predecessors.get(id) ?? []) {
      if (reachesWin.has(prev)) continue;
      reachesWin.add(prev);
      wq.push(prev);
    }
  }
  const successPath = order.filter((id) => forwardOnly.has(id) && reachesWin.has(id));
  const successSet = new Set(successPath);

  // Is the success path a single unbranched chain? Only then may a cadence be claimed for it.
  let linear = true;
  let branchAt = null;
  for (const id of successPath) {
    const onward = [...new Set(successEdges(byId.get(id)).filter((n) => successSet.has(n)))];
    if (onward.length > 1) { linear = false; branchAt = branchAt ?? id; break; }
  }

  const reachableObjectives = order.map((id) => byId.get(id));
  const encounters = reachableObjectives
    .filter((o) => BATTLE_TASKS.has(o.task))
    .map((o, i) => ({
      index: i + 1,
      objectiveId: o.id,
      aiIds: opponentsOf(o),
      onSuccessPath: successSet.has(o.id),
      description: typeof o.description === "string" ? o.description : "",
    }));

  const dialog = reachableObjectives.filter((o) => o.task === "dialog");
  const terminals = reachableObjectives.filter((o) => TERMINAL_TASKS.has(o.task));

  return {
    questId: quest.id,
    name: quest.name,
    questType: quest.questType ?? null,
    questRank: quest.questRank ?? null,
    hidden: quest.hidden,
    image: typeof quest.image === "string" && quest.image ? quest.image : null,
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
    winIds: reachableObjectives.filter((o) => WIN_TASKS.has(o.task)).map((o) => o.id),
    failIds: reachableObjectives.filter((o) => FAIL_TASKS.has(o.task)).map((o) => o.id),
    reachableIds: order,
    successPath,
    successPathLinear: linear,
    successPathBranchAt: branchAt,
    orphanStarts,
    reachedOnlyByFailure: [...viaFailure].filter((id) => !forwardOnly.has(id)),
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
 * that tiles the whole sequence exactly. Godstorm comes out as four ordinary encounters then one
 * keeper, five times - which is the sentence the poster is supposed to be able to say without
 * anybody typing it.
 *
 * `exact` is false when the sequence does not tile cleanly; the caller reports the sequence rather
 * than a cadence, because a cadence that only nearly holds is the kind of claim this whole plan
 * exists to stop.
 *
 * @param {string[]} roles  one role per battle, in traversal order
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
