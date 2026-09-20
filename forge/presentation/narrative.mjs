// Narrative source anchors (plan P2, §5.4).
//
// A story summary is editorial - it cannot be derived - so the rule is not "generate it" but
// "make it traceable". Every summary names the dialogue/objective ids it summarises, those ids
// must exist in the CURRENT captured records, and the summary may not introduce proper nouns that
// appear nowhere in the current evidence.
//
// THE FAILURE THIS REPLACES. A later Godstorm poster inherited stage language from an earlier
// draft - Tower, Dawnless - that the live dialogue no longer used, because planning prose and live
// captures were being blended by hand. An anchor check alone would not have caught it: stale prose
// can cite perfectly real objective ids. What catches it is the vocabulary check below, which asks
// where each distinctive name in the summary came from and fails when the answer is "nowhere in
// what was selected".
//
// THE VOCABULARY CHECK IS DELIBERATELY NARROW. It looks only at capitalised words that are not at
// the start of a sentence and not ordinary English, and it accepts any word that appears anywhere
// in the anchored objective text or in any name the dossier knows. It is a check on NAMES, not a
// judgement of prose: it cannot tell whether a summary is a good summary, and it does not try.

const SENTENCE_START = /(^|[.!?]["')\]]?\s+|\n\s*)$/;
// Capitalised words that carry no naming force: a summary may use them freely.
const ORDINARY = new Set([
  "A", "An", "The", "And", "But", "Or", "If", "When", "While", "After", "Before", "Then", "There",
  "This", "That", "These", "Those", "It", "Its", "They", "Their", "You", "Your", "He", "She", "His",
  "Her", "We", "Our", "One", "Two", "Three", "Four", "Five", "Each", "Every", "All", "No", "Not",
  "Player", "Players", "Battle", "Battles", "Boss", "Keeper", "Keepers", "Floor", "Floors",
]);

/** Lowercased, with a trailing possessive dropped, so "Thread" and "Thread's" are one word. */
const normalizeWord = (w) => String(w).toLowerCase().replace(/['\u2019]s$/, "").replace(/['\u2019]$/, "");
const words = (text) => (String(text ?? "").match(/[A-Za-z][A-Za-z'\u2019-]*/g) ?? []).map(normalizeWord);

/** Distinctive capitalised tokens of a summary: proper-noun candidates, sentence starts excluded. */
export function namesIn(text) {
  const out = [];
  const re = /[A-Z][A-Za-z'\u2019-]{2,}/g;
  let m;
  const s = String(text ?? "");
  while ((m = re.exec(s))) {
    if (SENTENCE_START.test(s.slice(0, m.index))) continue;
    if (ORDINARY.has(m[0])) continue;
    out.push(m[0]);
  }
  // deduplicated on the normalised form, reported in the spelling the summary used
  return [...new Set(out)];
}

/**
 * Check every story block against the selected current records.
 *
 * @param {object[]} structures  extracted structures, in component order
 * @param {object}   quests      questId -> the captured quest record
 * @param {object}   story       spec `story`: {key: {text, sourceObjectives: [ids], component?}}
 * @param {string[]} knownNames  every name the dossier already knows (quests, AIs, assets)
 */
export function resolveNarrative(structures, quests, story = {}, knownNames = []) {
  const problems = [];
  const warnings = [];
  const blocks = [];

  const objectiveIndex = new Map();
  for (const s of structures) {
    const record = quests[s.questId];
    for (const o of (record.content.objectives || [])) {
      if (!s.reachableIds.includes(o.id)) continue;
      objectiveIndex.set(`${s.questId}:${o.id}`, { questId: s.questId, ...o });
      // an id is also addressable bare when it is unambiguous across the selected structures
      if (!objectiveIndex.has(o.id)) objectiveIndex.set(o.id, { questId: s.questId, ...o });
      else if (objectiveIndex.get(o.id).questId !== s.questId) objectiveIndex.set(o.id, "AMBIGUOUS");
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
        problems.push(`${where}: objective id ${JSON.stringify(id)} does not exist in any selected current quest record`);
        continue;
      }
      if (hit === "AMBIGUOUS") {
        problems.push(`${where}: objective id ${JSON.stringify(id)} exists in more than one selected quest; qualify it as "<questId>:${id}"`);
        continue;
      }
      resolved.push(hit);
    }
    if (resolved.length !== ids.length) continue;

    const sourceText = resolved.map((o) => [o.description, o.successDescription, o.failDescription].filter(Boolean).join(" ")).join(" ");
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
      coverage: { anchored: covered, dialogNodes: available },
    });
  }

  return { blocks, problems, warnings };
}
