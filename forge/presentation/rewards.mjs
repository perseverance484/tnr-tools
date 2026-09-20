// Current reachable reward extraction (plan §5.3).
//
// THE FAILURE THIS REPLACES. A Godstorm poster showed per-floor cash-outs and chest items that had
// been removed from the quest before it went live. Nothing was lying: the numbers came from a
// planning table that had been correct once. The rule that makes that impossible is that a reward
// is whatever a REACHABLE objective node in the CURRENT captured record grants, and a presentation
// spec cannot state a reward amount at all (spec.mjs refuses the key).
//
// "Reachable" is doing real work here. A quest record keeps nodes the graph no longer walks to;
// reading rewards off every node in the array would resurrect exactly the cash-outs that were
// removed. structure.mjs walks the graph, and only the nodes it reached are read.

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
 * Every reward a player can actually reach, and which node grants it.
 *
 * @param {object} quest      the captured quest record
 * @param {object} structure  its extracted structure (supplies the reachable set)
 * @returns {object} the rewards block for the dossier
 */
export function extractRewards(quest, structure) {
  const content = quest.content || {};
  const objectives = Array.isArray(content.objectives) ? content.objectives : [];
  const reachable = new Set(structure.reachableIds);
  const terminal = new Set(structure.terminalIds);

  const nodes = [];
  for (const o of objectives) {
    const reward = rewardOf(o);
    if (!Object.keys(reward).length) continue;
    nodes.push({
      objectiveId: o.id,
      task: o.task,
      reachable: reachable.has(o.id),
      terminal: terminal.has(o.id),
      reward,
    });
  }

  const questLevel = rewardOf(content.reward || {});
  const live = nodes.filter((n) => n.reachable);

  // A "full clear" node is the last reachable reward node on the way to the win: for both Godstorm
  // pyramids that is the victory dialog, which is where the reward actually sits. Anything else
  // reachable and rewarding is an intermediate cash-out and is named as one rather than folded in.
  const order = structure.reachableIds;
  const rank = new Map(order.map((id, i) => [id, i]));
  const sorted = [...live].sort((a, b) => (rank.get(a.objectiveId) ?? 0) - (rank.get(b.objectiveId) ?? 0));
  const fullClear = sorted.length ? sorted[sorted.length - 1] : null;
  const intermediate = sorted.slice(0, Math.max(0, sorted.length - 1));

  const total = {};
  for (const n of sorted) {
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
    reachableRewardNodes: sorted.map((n) => n.objectiveId),
    unreachableRewardNodes: nodes.filter((n) => !n.reachable).map((n) => n.objectiveId),
    fullClear: fullClear ? { objectiveId: fullClear.objectiveId, reward: fullClear.reward } : null,
    intermediateCashOuts: intermediate.map((n) => ({ objectiveId: n.objectiveId, reward: n.reward })),
    rewardItems: sorted.flatMap((n) => (Array.isArray(n.reward.items) ? n.reward.items : [])),
    total,
    source: structure.source,
  };
}
