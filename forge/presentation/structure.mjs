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

  // The SUCCESS ROUTE. Membership is not order (independent review R3). The first correction
  // filtered the all-edge BFS order down to nodes that can reach a win, which gets the MEMBERSHIP
  // right and the SEQUENCE wrong: one `failObjectiveId` pointing across the quest pulled the
  // victory dialogue forward in the traversal, so the reward read off "the last node on the path"
  // became a mid-route payout while the real 125,000 victory was demoted to an intermediate. A
  // route the player walks is a walk over SUCCESS edges, so it is derived on that graph alone and
  // the all-edge order is never reused for it.
  const reachesWin = new Set();
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

  // Forward-reachable at all, win or not: the difference between an OPTIONAL branch the player can
  // choose and a node only a loss reaches. rewards.mjs needs both to classify a payout.
  const forwardOnly = new Set([entryId]);
  const fq = [entryId];
  while (fq.length) {
    for (const next of successEdges(byId.get(fq.shift()))) {
      if (!byId.has(next) || forwardOnly.has(next)) continue;
      forwardOnly.add(next);
      fq.push(next);
    }
  }

  // Walk forward from the entry over success edges, entering only nodes that still reach a win.
  // The result is both the membership and the order, from one traversal, so the two cannot drift.
  const successPath = [];
  const successSet = new Set();
  if (reachesWin.has(entryId)) {
    const sq = [entryId];
    successSet.add(entryId);
    while (sq.length) {
      const id = sq.shift();
      successPath.push(id);
      for (const next of successEdges(byId.get(id))) {
        if (!byId.has(next) || successSet.has(next) || !reachesWin.has(next)) continue;
        successSet.add(next);
        sq.push(next);
      }
    }
  }

  // CYCLES. A `failObjectiveId` pointing back up the quest makes a rooted cycle the entry check
  // cannot see: every node is still referenced and one start still exists. The pinned flow
  // validator rejects such a record, so it is worth reporting - but a loop that exists only through
  // a failure edge leaves the route a player walks perfectly well defined, so it is a WARNING.
  // A cycle through SUCCESS edges on the route is different: there is then no order in which the
  // route is walked, and inventing one is the thing this whole module exists not to do.
  const cyclesOver = (edgesOf) => {
    const found = new Set();
    const state = new Map();
    const visit = (id) => {
      state.set(id, 1);
      for (const next of edgesOf(byId.get(id))) {
        if (!byId.has(next) || !reachable.has(next)) continue;
        const st = state.get(next) ?? 0;
        if (st === 1) { found.add(next); found.add(id); continue; }
        if (st === 0) visit(next);
      }
      state.set(id, 2);
    };
    for (const id of order) if ((state.get(id) ?? 0) === 0) visit(id);
    return found;
  };
  const cycleNodes = cyclesOver(successorsOf);
  const routeCycles = [...cyclesOver(successEdges)].filter((id) => successSet.has(id)).sort();
  if (routeCycles.length) {
    throw new PresentationError(
      `quest ${quest.id}: the route to completion loops through ${routeCycles.join(", ")} along success edges, ` +
      "so there is no order in which a player walks it; a presentation must not invent one.",
    );
  }

  // Is the route a single unbranched chain? Only then may a cadence be claimed for it.
  let linear = true;
  let branchAt = null;
  for (const id of successPath) {
    const onward = [...new Set(successEdges(byId.get(id)).filter((n) => successSet.has(n)))];
    if (onward.length > 1) { linear = false; branchAt = branchAt ?? id; break; }
  }

  const reachableObjectives = order.map((id) => byId.get(id));
  // Encounters are ordered along the ROUTE, and battles that are not on it come after, unindexed
  // and marked. Numbering an optional battle into the sequence is what made a 4+1 cadence read as
  // five recurring fights before the first keeper, for a combined sequence no player can walk.
  const routeBattles = successPath.map((id) => byId.get(id)).filter((o) => BATTLE_TASKS.has(o.task));
  const offRouteBattles = reachableObjectives.filter((o) => BATTLE_TASKS.has(o.task) && !successSet.has(o.id));
  const encounters = [
    ...routeBattles.map((o, i) => ({
      index: i + 1,
      objectiveId: o.id,
      aiIds: opponentsOf(o),
      onSuccessPath: true,
      description: typeof o.description === "string" ? o.description : "",
    })),
    ...offRouteBattles.map((o) => ({
      index: null,
      objectiveId: o.id,
      aiIds: opponentsOf(o),
      onSuccessPath: false,
      description: typeof o.description === "string" ? o.description : "",
    })),
  ];

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
      routeBattles: routeBattles.length,
      offRouteBattles: offRouteBattles.length,
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
    cycles: [...cycleNodes].sort(),
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
