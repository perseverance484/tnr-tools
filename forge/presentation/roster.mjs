// Roster extraction and validated role annotations (plan §5.2).
//
// The first Godstorm poster showed five enemies for an eighteen-enemy event, and nothing in the
// pipeline could tell that it had. There was no statement anywhere of whether a roster block meant
// "a sample" or "everybody", so a sample could not be wrong. Here the roster is DERIVED - it is
// exactly the set of AI ids the reachable battle nodes field - and the presentation spec says
// whether it is showing all of them or a named selection. Under coverage:"all" an omission is a
// lint failure rather than an editorial choice.
//
// ROLES ARE ANNOTATIONS, NOT FACTS. Nothing in a quest record says "keeper". The spec supplies the
// role of each AI id and this file validates it against the battle nodes: an annotated id that
// fights in no battle is refused, and a battle AI with no annotation is refused, so an annotation
// can never quietly invent, rename or drop an enemy. What roles BUY is the cadence - four
// recurring encounters then a keeper - which is derived from the annotated sequence, not typed.

export const ROLES = Object.freeze(["recurring", "ascendant", "keeper", "finalBoss"]);
/** Roles that count as a "keeper fight" for the encounter cadence and the keeper tally. */
export const KEEPER_ROLES = Object.freeze(["keeper", "finalBoss"]);

/**
 * Build the roster from the structures and whatever AI records the evidence supplies.
 *
 * @param {object[]} structures  extracted structures, in component order
 * @param {Map}      currentById  entityId -> the CURRENT observation, already resolved by capture
 *   time with conflicts refused (evidence.mjs currentByEntity). Ranking used to happen here, off
 *   the bundle export timestamp, which is how an older before-read of a keeper won (review F3).
 * @param {object}   roles       {aiId: role} from the presentation spec, already key-checked
 * @returns {{entries, problems, unannotated, unknownAnnotations}}
 */
export function extractRoster(structures, currentById, roles = {}) {
  const appearances = new Map();
  const firstSeen = new Map();
  structures.forEach((s, componentIndex) => {
    for (const e of s.encounters) {
      for (const aiId of e.aiIds) {
        if (!appearances.has(aiId)) {
          appearances.set(aiId, []);
          firstSeen.set(aiId, componentIndex * 1e6 + e.index);
        }
        appearances.get(aiId).push({ component: s.questId, objectiveId: e.objectiveId, index: e.index });
      }
    }
  });

  const problems = [];
  const unannotated = [];
  const entries = [];
  for (const [aiId, where] of appearances) {
    const known = currentById.get(aiId);
    const role = Object.prototype.hasOwnProperty.call(roles, aiId) ? roles[aiId] : null;
    if (!role) unannotated.push(aiId);
    entries.push({
      aiId,
      name: known ? known.name : null,
      role,
      components: [...new Set(where.map((w) => w.component))],
      appearances: where.length,
      battles: where.map((w) => w.objectiveId),
      // An AI that fights but that no ADMISSIBLE capture names cannot be presented: the poster
      // would have to invent a name or show a blank tile, and both are the original defect.
      resolved: Boolean(known),
      source: known ? known.source : null,
      capturedAt: known ? known.capturedAt : null,
    });
    if (!known) problems.push(`ai ${aiId} fights in ${where.length} battle(s) but no admissible capture in the selected evidence names it`);
  }

  const unknownAnnotations = Object.keys(roles).filter((id) => !appearances.has(id));
  for (const id of unknownAnnotations) {
    problems.push(`role annotation names ai ${id}, which fights in no reachable battle of the selected structures`);
  }
  for (const [id, role] of Object.entries(roles)) {
    if (!ROLES.includes(role)) problems.push(`role annotation for ai ${id} is ${JSON.stringify(role)}; expected one of ${ROLES.join(", ")}`);
  }

  // Deterministic and meaningful: the order a player meets them in, along the graph traversal
  // structure.mjs derived - not the order the objectives happen to sit in the stored array.
  entries.sort((a, b) => (firstSeen.get(a.aiId) ?? 0) - (firstSeen.get(b.aiId) ?? 0));

  return { entries, problems, unannotated, unknownAnnotations };
}

/** The role sequence of one structure's battles, for cadenceOf(). */
export function roleSequence(structure, roles) {
  return structure.encounters.map((e) => {
    const ids = e.aiIds;
    if (ids.length !== 1) return "mixed";
    const role = roles[ids[0]];
    if (!role) return "unannotated";
    // finalBoss collapses to keeper for the CADENCE only: Stormcourt's fifth keeper is its final
    // boss, and a pattern that treated it as a different shape would not tile although the player
    // meets exactly the same rhythm five times. The roster keeps the two roles apart.
    return KEEPER_ROLES.includes(role) ? "keeper" : role;
  });
}

/** Keeper-role battles of one structure. */
export function keepersOf(structure, roles) {
  return structure.encounters.filter((e) => e.aiIds.length === 1 && KEEPER_ROLES.includes(roles[e.aiIds[0]]));
}
