import { readFileSync } from "node:fs";
// For every naming-pass tree and bonus tag: how many kit effect rows the game's own
// resolvePotencyTags changes today, and after setting kit elementClassification to the element.
// Usage: node scripts/bloodright_engine/probe_coverage.mjs ENGINE.mjs   (ENGINE built by build_engine.mjs
// from an entry file containing: export { resolvePotencyTags } from "@/libs/combat/potency";)
const { resolvePotencyTags } = await import(new URL(process.argv[2], `file://${process.cwd()}/`).href);
const repo = new URL("../../", import.meta.url).pathname;
const kits = JSON.parse(readFileSync(`${repo}docs/design/bloodright/balance/kits_from_reference_captures.json`, "utf8"));
const root = `${repo}docs/design/bloodright/structural`;
let deadNow = 0, deadAfter = 0, pairs = 0, nodeDeadNow = 0, nodeDeadAfter = 0;
const eff = t => t.power + (t.powerPerLevel ?? 0) * 1;
const covered = (k, tag, cls) => {
  const mod = { id: "br", type: "increasepotency", creatorId: "me", targetId: "me", fromType: "bloodright", isNew: false, rounds: 99, power: 1, powerPerLevel: 0, level: 0, calculation: "static", affectedTag: tag, affectedElements: [...k.elements] };
  let n = 0;
  for (const j of k.jutsu) {
    const data = cls ? { ...j, elementClassification: cls } : j;
    const out = resolvePotencyTags({ type: "jutsu", effects: structuredClone(j.effects), level: 1, data }, [mod], "me");
    const ref = resolvePotencyTags({ type: "jutsu", effects: structuredClone(j.effects), level: 1, data }, [{ ...mod, power: 0 }], "me");
    out.forEach((t, i) => { if (t.type === tag && Math.abs(eff(t) - eff(ref[i])) > 1e-9) n++; });
  }
  return n;
};
for (const [slug, k] of Object.entries(kits)) {
  const d = JSON.parse(readFileSync(`${root}/${slug}.json`, "utf8"));
  const tags = [...new Set(d.nodes.flatMap(n => Object.keys(n.bonuses)))];
  const cls = k.elements.length === 1 && k.elements[0] !== "None" ? k.elements[0] : null;
  for (const tag of tags) {
    pairs++;
    const now = covered(k, tag, null), after = cls ? covered(k, tag, cls) : now;
    const nodes = d.nodes.filter(n => tag in n.bonuses).length;
    if (!now) { deadNow++; nodeDeadNow += nodes; }
    if (!after) { deadAfter++; nodeDeadAfter += nodes; console.log("still dead with classification:", slug, tag, cls ?? "(multi/None element)"); }
  }
}
console.log(`tag types: ${pairs}; dead now ${deadNow} (${nodeDeadNow} node bonuses); dead if kit elementClassification = bloodline element: ${deadAfter} (${nodeDeadAfter} node bonuses)`);
