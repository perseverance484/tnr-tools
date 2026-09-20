// Narrative source anchors (plan P2, §5.4).
//
// A story summary is editorial - it cannot be derived - so the rule is not "generate it" but
// "make it traceable". Every summary names the dialogue/objective ids it summarises, those ids must
// exist and be reachable in the CURRENT captured records, the summary may not introduce proper
// nouns that appear nowhere in the current evidence, and - after independent review F6 - it is
// bound to the VERSION of the text it was written against.
//
// TWO BYPASSES THIS CLOSES.
//
//   Sentence starts. The first version exempted every capitalised word at the start of a sentence,
//   so `Dawnless awaits below. Tower rises above.` passed with the real anchors attached. There is
//   no reason a proper noun is more trustworthy for sitting after a full stop. Every capitalised
//   word is now checked; ordinary English is exempted by vocabulary, not by position.
//
//   Changed text under an unchanged id. Anchors proved the ids existed, never that the prose still
//   summarised them. Rewriting `d5_victory` so the stair stays CLOSED left a summary claiming it
//   stands open, passing cleanly. Each block therefore carries `sourceDigest`, a hash of the exact
//   fields it summarises; when the dialogue moves, the digest moves and the build stops until a
//   human has re-read it. That is a re-review prompt, not a semantic judgement - this file does not
//   decide whether prose is a good summary and does not try.

import { createHash } from "node:crypto";

// The objective fields a summary is written against. Fixed, so a digest means the same thing in
// every build, and narrow, so an unrelated field edit does not cry wolf.
export const ANCHOR_FIELDS = Object.freeze(["description", "successDescription", "failDescription", "drawDescription", "fleeDescription"]);

// Capitalised words that carry no naming force: a summary may use them freely wherever they sit.
//
// This list is the price of checking sentence starts. Ordinary English words legitimately begin
// sentences in a summary, so they have to be exempt somewhere, and a stoplist of FUNCTION and
// common descriptive words is the narrowest place to put it. The residual risk is a proper noun
// that is also an ordinary English word - a character actually called "Further" would pass - which
// is why the source fingerprint below is the second line of defence rather than the only one.
// Nothing here is a place, a character, an item or a faction.
const ORDINARY = new Set([
  "a", "an", "the", "and", "but", "or", "nor", "so", "yet", "if", "when", "while", "as", "because",
  "after", "before", "then", "there", "here", "this", "that", "these", "those", "it", "its",
  "they", "their", "them", "you", "your", "he", "she", "his", "her", "we", "our", "us", "who",
  "what", "which", "where", "how", "one", "two", "three", "four", "five", "each", "every", "all",
  "both", "either", "neither", "some", "any", "no", "not", "now", "only", "still", "again",
  "with", "without", "from", "into", "onto", "over", "under", "above", "below", "beneath",
  "beyond", "past", "across", "through", "between", "among", "along", "around", "toward",
  "towards", "within", "inside", "outside", "up", "down", "out", "off", "on", "at", "by", "for",
  "deep", "deeper", "deepest", "far", "farther", "further", "near", "nearer", "high", "higher",
  "low", "lower", "first", "last", "next", "later", "earlier", "soon", "finally", "eventually",
  "meanwhile", "instead", "together", "once", "twice", "until", "since", "always", "never",
  "player", "players", "battle", "battles", "boss", "keeper", "keepers", "floor", "floors",
  "enemy", "enemies", "fight", "fights", "reward", "rewards", "story", "event", "quest",
]);

/** Lowercased, with a trailing possessive dropped, so "Thread" and "Thread's" are one word. */
const normalizeWord = (w) => String(w).toLowerCase().replace(/['’]s$/, "").replace(/['’]$/, "");
const words = (text) => (String(text ?? "").match(/[A-Za-z][A-Za-z'’-]*/g) ?? []).map(normalizeWord);

/**
 * Distinctive capitalised tokens of a summary: proper-noun candidates.
 *
 * Position is deliberately NOT consulted. A capitalised word at the start of a sentence is exactly
 * as much of a name as the same word in the middle of one, and treating it as safe is what let
 * "Dawnless awaits below." through.
 */
export function namesIn(text) {
  const out = [];
  const re = /[A-Z][A-Za-z'’-]{2,}/g;
  let m;
  const s = String(text ?? "");
  while ((m = re.exec(s))) {
    if (ORDINARY.has(normalizeWord(m[0]))) continue;
    out.push(m[0]);
  }
  return [...new Set(out)];
}

/** The exact source text one anchor contributes, in a fixed field order. */
function anchorText(objective) {
  return ANCHOR_FIELDS.map((f) => (typeof objective[f] === "string" ? objective[f] : "")).join("\u0000");
}

/**
 * The fingerprint of the exact source fields a set of anchors summarises.
 *
 * Over the anchors IN THE ORDER THE SUMMARY CITES THEM, each as questId, objectiveId, task and the
 * fixed field list. Reordering the citation changes it, because a summary of the same three nodes
 * read in a different order is a different claim.
 */
export function sourceDigest(resolved) {
  const h = createHash("sha256");
  for (const o of resolved) h.update(`${o.questId}\u0000${o.id}\u0000${o.task}\u0000${anchorText(o)}\u0001`);
  return h.digest("hex");
}

/**
 * Check every story block against the selected current records.
 *
 * @param {object[]} structures  extracted structures, in component order
 * @param {object}   quests      questId -> the captured quest record
 * @param {object}   story       spec `story`: {key: {text, sourceObjectives, sourceDigest}}
 * @param {string[]} knownNames  every name the dossier already knows (quests, AIs, assets)
 */
export function resolveNarrative(structures, quests, story = {}, knownNames = []) {
  const problems = [];
  const warnings = [];
  const blocks = [];

  const objectiveIndex = new Map();
  for (const s of structures) {
    const record = quests[s.questId];
    const reachable = new Set(s.reachableIds);
    for (const o of (record.content.objectives || [])) {
      if (!reachable.has(o.id)) continue;
      objectiveIndex.set(`${s.questId}:${o.id}`, { questId: s.questId, ...o });
      if (!objectiveIndex.has(o.id)) objectiveIndex.set(o.id, { questId: s.questId, ...o });
      else if (objectiveIndex.get(o.id) !== "AMBIGUOUS" && objectiveIndex.get(o.id).questId !== s.questId) objectiveIndex.set(o.id, "AMBIGUOUS");
    }
  }

  const vocabulary = new Set();
  for (const n of knownNames) for (const w of words(n)) vocabulary.add(w);

  for (const [key, block] of Object.entries(story)) {
    const where = `story.${key}`;
    const ids = Array.isArray(block.sourceObjectives) ? block.sourceObjectives : [];
    if (!ids.length) {
      problems.push(`${where}: a narrative summary must cite the objective ids it summarises`);
      continue;
    }
    const resolved = [];
    for (const id of ids) {
      const hit = objectiveIndex.get(id);
      if (!hit) {
        problems.push(`${where}: objective id ${JSON.stringify(id)} does not exist, or is not reachable, in any selected current quest record`);
        continue;
      }
      if (hit === "AMBIGUOUS") {
        problems.push(`${where}: objective id ${JSON.stringify(id)} exists in more than one selected quest; qualify it as "<questId>:${id}"`);
        continue;
      }
      resolved.push(hit);
    }
    if (resolved.length !== ids.length) continue;

    // THE SOURCE VERSION. An id that still exists is not evidence that the prose behind it is the
    // prose this summary was written from.
    const digest = sourceDigest(resolved);
    if (typeof block.sourceDigest !== "string" || !block.sourceDigest) {
      problems.push(
        `${where}: no sourceDigest. A summary must be bound to the version of the dialogue it was reviewed against, ` +
        `or a later edit to the same objective ids changes what it claims without changing the spec. Current digest: ${digest}`,
      );
    } else if (block.sourceDigest !== digest) {
      problems.push(
        `${where}: the dialogue behind its anchors has changed since this summary was reviewed ` +
        `(reviewed against ${block.sourceDigest.slice(0, 12)}, current ${digest.slice(0, 12)}). ` +
        "Re-read the current text and update the summary and its sourceDigest together.",
      );
    }

    const sourceText = resolved.map(anchorText).join(" ");
    const anchored = new Set(words(sourceText));
    const unsupported = namesIn(block.text).filter((n) => !anchored.has(normalizeWord(n)) && !vocabulary.has(normalizeWord(n)));
    for (const n of unsupported) {
      problems.push(`${where}: names ${JSON.stringify(n)}, which appears in none of its source objectives and in no current record of this subject; a summary may not introduce wording the current evidence does not carry`);
    }

    const component = resolved[0].questId;
    const structure = structures.find((s) => s.questId === component);
    const covered = resolved.filter((o) => o.questId === component).length;
    const available = structure ? structure.dialogIds.length : 0;
    if (available && covered / available < 0.05) {
      warnings.push(`${where}: anchored to ${covered} of ${available} dialogue nodes in ${component}; a summary this thinly sourced is hard to audit`);
    }
    if (resolved.some((o) => o.questId !== component)) {
      warnings.push(`${where}: anchors span more than one component (${[...new Set(resolved.map((o) => o.questId))].join(", ")})`);
    }

    blocks.push({
      key,
      component,
      text: block.text,
      sourceObjectives: resolved.map((o) => ({ questId: o.questId, objectiveId: o.id, task: o.task })),
      sourceDigest: digest,
      reviewedAgainst: block.sourceDigest ?? null,
      coverage: { anchored: covered, dialogNodes: available },
    });
  }

  return { blocks, problems, warnings };
}
