// Current reachable reward extraction (plan §5.3).
//
// THE FAILURE THIS REPLACES. A Godstorm poster showed per-floor cash-outs and chest items that had
// been removed from the quest before it went live. Nothing was lying: the numbers came from a
// planning table that had been correct once. The rule that makes that impossible is that a reward
// is whatever a REACHABLE objective node in the CURRENT captured record grants, and a presentation
// spec cannot state a reward amount at all (spec.mjs refuses the key).
//
// REACHABLE IS NOT ENOUGH (independent review F5). The first version called the last reward a
// depth-first walk happened to visit the "full clear" and every earlier one an intermediate
// cash-out, then summed them. Adding an optional opening exit that pays 20,000 ryo and leads to
// `fall` therefore produced a 20,000-ryo "full clear", demoted the real 125,000 victory to a
// cash-out, and reported a 145,000 total across two mutually exclusive routes.
//
// So rewards are classified against the SUCCESS PATH - the nodes that lead from the entry to a
// `win_quest` along success edges - which structure.mjs derives from the graph:
//
//   full clear        the last reward on the success path. One unambiguous amount, or none.
//   intermediate      a reward on the success path before it. A real cash-out on the clear route.
//   optional          reachable, but cannot reach a win. An exit, a consolation, a side branch.
//   failure path      reached only by losing.
//   unreachable       still in the record, reached by nothing. Historical, and named as such.
//
// `total` carries the basis it was summed over, because a number without one is how two exclusive
// routes got added together.

const SCALARS = ["money", "tokens", "prestige", "exp", "reputation", "anbupoints", "clanpoints", "seichi_silver", "skillpoints", "village_membership", "rank"];
const LISTS = ["items", "jutsus", "badges", "bloodlines", "sage_modes", "hunter_items_ids", "gathering_items_ids"];

const zeroish = (v) => v === 0 || v === null || v === undefined || v === "" || v === "NONE" || v === false
  || (Array.isArray(v) && v.length === 0);

/** The non-empty reward fields of one objective (or of the quest-level reward block). */
export function rewardOf(node) {
  const out = {};
  for (const key of [...SCALARS, ...LISTS]) {
    const v = node[`reward_${key}`];
    if (!zeroish(v)) out[key] = v;
  }
  if (node.reward_hunter_items === true) out.hunter_items = true;
  if (node.reward_gathering_items === true) out.gathering_items = true;
  return out;
}

/**
 * Every reward a player can reach, which node grants it, and on which kind of path.
 *
 * @param {object} quest      the captured quest record
 * @param {object} structure  its extracted structure (supplies the graph-derived paths)
 * @returns {object} the rewards block for the dossier
 */
export function extractRewards(quest, structure) {
  const content = quest.content || {};
  const objectives = Array.isArray(content.objectives) ? content.objectives : [];
  const reachable = new Set(structure.reachableIds);
  const success = new Set(structure.successPath);
  const failureOnly = new Set(structure.reachedOnlyByFailure);

  const classify = (id) => {
    if (!reachable.has(id)) return "unreachable";
    if (success.has(id)) return "success-path";
    if (failureOnly.has(id)) return "failure-path";
    return "optional";
  };

  const nodes = [];
  for (const o of objectives) {
    const reward = rewardOf(o);
    if (!Object.keys(reward).length) continue;
    nodes.push({ objectiveId: o.id, task: o.task, path: classify(o.id), reward });
  }

  const questLevel = rewardOf(content.reward || {});

  // Order along the success path is the traversal order structure.mjs derived from the edges, not
  // the order the nodes happen to sit in the stored array.
  const rank = new Map(structure.successPath.map((id, i) => [id, i]));
  const onSuccess = nodes.filter((n) => n.path === "success-path").sort((a, b) => rank.get(a.objectiveId) - rank.get(b.objectiveId));

  // A full clear is only one number when the success path is one route. A branching success path
  // can pay differently down each branch, and picking whichever the traversal reached last is
  // exactly the guess this finding is about.
  const ambiguous = !structure.successPathLinear;
  const last = onSuccess.length ? onSuccess[onSuccess.length - 1] : null;
  const fullClear = ambiguous || !last ? null : { objectiveId: last.objectiveId, reward: last.reward };
  const intermediate = onSuccess.slice(0, Math.max(0, onSuccess.length - 1));

  const total = {};
  for (const n of onSuccess) {
    for (const [k, v] of Object.entries(n.reward)) {
      if (typeof v === "number") total[k] = (total[k] ?? 0) + v;
      else if (Array.isArray(v)) total[k] = [...(total[k] ?? []), ...v];
      else total[k] = v;
    }
  }

  return {
    questId: quest.id,
    questLevelReward: questLevel,
    nodes,
    successPathRewardNodes: onSuccess.map((n) => n.objectiveId),
    optionalRewardNodes: nodes.filter((n) => n.path === "optional").map((n) => ({ objectiveId: n.objectiveId, reward: n.reward })),
    failurePathRewardNodes: nodes.filter((n) => n.path === "failure-path").map((n) => ({ objectiveId: n.objectiveId, reward: n.reward })),
    unreachableRewardNodes: nodes.filter((n) => n.path === "unreachable").map((n) => n.objectiveId),
    fullClear,
    fullClearAmbiguous: ambiguous && onSuccess.length > 0,
    intermediateCashOuts: intermediate.map((n) => ({ objectiveId: n.objectiveId, reward: n.reward })),
    rewardItems: onSuccess.flatMap((n) => (Array.isArray(n.reward.items) ? n.reward.items : [])),
    total,
    totalBasis: ambiguous ? "none: the success path branches" : "the single success path from the entry to win_quest",
    source: structure.source,
  };
}
