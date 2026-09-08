// Derive the NESTED writable key surface from the PINNED game source (readiness brief section 6).
//
//   node tools/derive_nested.mjs /path/to/TheNinjaRPG [pin] > src/runner/nested.json
//
// No network. Reads the checked-out source only. Re-run whenever the pin moves.
//
// derive_fields.mjs covers the top level of each entity validator. Everything below it -
// an effect tag inside `effects[]`, a quest objective inside `content.objectives[]`, an AI rule's
// condition and action - is parsed by a zod object too, and zod objects STRIP unknown keys
// silently. So a misspelled key inside one of those is dropped by the server with no error and the
// mutation still reports success: exactly the failure mode the top-level check exists to prevent,
// one level down.
//
// Every family here is the same shape at source: `export const X = z.object({ ...groups, keys })`
// with a discriminator (`type` for tags and AI conditions/actions, `task` for objectives) given as
// z.literal("x") or z.enum([...]). This tool reads those object bodies, resolves the spread groups
// (across files: rewardFields lives in rewards.ts), and emits the allowed key set per discriminator
// value. It deliberately does NOT record types, bounds or enums: bounds are what the 45g power cap
// got wrong, and a key set is checkable without re-implementing zod.

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const root = process.argv[2];
const PIN = process.argv[3] || "345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9";
const FILES = {
  combat: "app/src/validators/combat.ts",
  objectives: "app/src/validators/objectives.ts",
  rewards: "app/src/validators/rewards.ts",
  ai: "app/src/validators/ai.ts",
  base: "app/src/validators/base.ts",
};
if (!root || !Object.values(FILES).every((f) => existsSync(join(root, f)))) {
  console.error("usage: derive_nested.mjs <TheNinjaRPG checkout> [pin]");
  process.exit(2);
}
const src = Object.fromEntries(Object.entries(FILES).map(([k, f]) => [k, readFileSync(join(root, f), "utf8")]));
const ALL = Object.values(src).join("\n");

/** Text inside the braces/brackets that open at `from` (index of the opening char + 1). */
function balanced(s, from) {
  let i = from, depth = 1;
  while (i < s.length && depth > 0) {
    const c = s[i], n = s[i + 1];
    if (c === "/" && n === "/") { i = s.indexOf("\n", i); continue; }
    if (c === "/" && n === "*") { i = s.indexOf("*/", i) + 2; continue; }
    if (c === '"' || c === "'" || c === "`") { const q = c; i++; while (i < s.length && s[i] !== q) { if (s[i] === "\\") i++; i++; } i++; continue; }
    if (c === "{" || c === "(" || c === "[") depth++;
    else if (c === "}" || c === ")" || c === "]") depth--;
    i++;
  }
  return s.slice(from, i - 1);
}

/** The body of `const NAME = z.object({...})` or `const NAME = {...}`, wherever it is declared. */
function bodyOf(name) {
  for (const text of Object.values(src)) {
    const re = new RegExp(`(?:export\\s+)?const\\s+${name}\\s*=\\s*(z\\.object\\(\\s*)?\\{`, "m");
    const m = re.exec(text);
    if (!m) continue;
    return balanced(text, m.index + m[0].length);
  }
  return null;
}

/** Top-level `key:` names and `...Spread` names of one object body. */
function shallow(body) {
  const keys = [], spreads = [];
  let i = 0, depth = 0;
  const atTop = () => depth === 0;
  while (i < body.length) {
    const c = body[i], n = body[i + 1];
    if (c === "/" && n === "/") { i = body.indexOf("\n", i) + 1 || body.length; continue; }
    if (c === "/" && n === "*") { i = body.indexOf("*/", i) + 2; continue; }
    if (c === '"' || c === "'" || c === "`") { const q = c; i++; while (i < body.length && body[i] !== q) { if (body[i] === "\\") i++; i++; } i++; continue; }
    if (c === "{" || c === "(" || c === "[") { depth++; i++; continue; }
    if (c === "}" || c === ")" || c === "]") { depth--; i++; continue; }
    if (atTop() && c === "." && body.slice(i, i + 3) === "...") {
      const m = /^\.\.\.([A-Za-z_$][\w$]*)/.exec(body.slice(i));
      if (m) { spreads.push(m[1]); i += m[0].length; continue; }
    }
    if (atTop() && /[A-Za-z_$"]/.test(c)) {
      const m = /^(?:"([^"]+)"|([A-Za-z_$][\w$]*))\s*:/.exec(body.slice(i));
      if (m) { keys.push(m[1] ?? m[2]); i += m[0].length; continue; }
    }
    i++;
  }
  return { keys, spreads };
}

/** `const NAME = z.object(OTHER)` - an alias, not an inline body. */
function aliasOf(name) {
  const m = new RegExp(`(?:export\\s+)?const\\s+${name}\\s*=\\s*z\\.object\\(\\s*([A-Za-z_$][\\w$]*)\\s*\\)`, "m").exec(ALL);
  return m ? m[1] : null;
}

/** Every key of a schema, spreads resolved (across files), deduplicated. */
function keysOf(name, seen = new Set()) {
  if (seen.has(name)) return [];
  seen.add(name);
  const alias = aliasOf(name);
  if (alias) return keysOf(alias, seen);
  const body = bodyOf(name);
  if (body == null) throw new Error("cannot find declaration for " + name);
  const { keys, spreads } = shallow(body);
  const out = new Set(keys);
  for (const s of spreads) for (const k of keysOf(s, seen)) out.add(k);
  return [...out];
}

/** The discriminator values a schema accepts on `field` (z.literal, z.enum([...]) or z.enum(CONST)). */
function discriminators(name, field) {
  const body = bodyOf(name);
  const re = new RegExp(`\\b${field}\\s*:\\s*z\\.(literal|enum)\\(`, "m");
  const m = re.exec(body);
  if (!m) return [];
  const inner = balanced(body, m.index + m[0].length);
  const literals = [...inner.matchAll(/"([^"]+)"/g)].map((x) => x[1]);
  if (literals.length) return literals;
  const ref = /^\s*([A-Za-z_$][\w$]*)/.exec(inner);
  if (!ref) return [];
  const cm = new RegExp(`const\\s+${ref[1]}\\s*=\\s*\\[`, "m").exec(ALL);
  if (!cm) throw new Error(`cannot resolve enum source ${ref[1]} for ${name}.${field}`);
  return [...balanced(ALL, cm.index + cm[0].length).matchAll(/"([^"]+)"/g)].map((x) => x[1]);
}

/** Members of a z.union / z.discriminatedUnion, by name. */
function unionMembers(name) {
  const m = new RegExp(`const\\s+${name}\\s*=\\s*z\\.(?:discriminatedUnion\\(\\s*"[^"]+"\\s*,\\s*)?(?:union\\()?\\[`, "m").exec(ALL);
  if (!m) throw new Error("cannot find union " + name);
  const body = balanced(ALL, m.index + m[0].length);
  return [...body.matchAll(/([A-Za-z_$][\w$]*)\s*(?:\.prefault\([^)]*\))?\s*,/g)].map((x) => x[1]);
}

/** {discriminatorValue: [keys]} for every member of a union. */
function family(unionName, field) {
  const out = {};
  for (const member of unionMembers(unionName)) {
    const keys = keysOf(member).sort();
    for (const v of discriminators(member, field)) out[v] = keys;
  }
  return out;
}

/** Keys of an inline `z.array(z.object({...}))`, either at `field` of a schema or of a bare const. */
function inlineArrayObjectKeys(name, field) {
  const hay = field ? bodyOf(name) : (() => {
    const m = new RegExp(`(?:export\\s+)?const\\s+${name}\\s*=`, "m").exec(ALL);
    if (!m) throw new Error("cannot find " + name);
    return ALL.slice(m.index, m.index + 800);
  })();
  const start = field ? new RegExp(`\\b${field}\\s*:[\\s\\S]{0,40}?z\\s*\\.\\s*array\\(`, "m") : /z\s*\.\s*array\(/;
  const m = start.exec(hay);
  if (!m) throw new Error(`no z.array for ${name}${field ? "." + field : ""}`);
  const arr = balanced(hay, m.index + m[0].length);
  const om = /z\.object\(\s*\{/.exec(arr);
  if (!om) throw new Error(`no z.object inside the array for ${name}${field ? "." + field : ""}`);
  const { keys, spreads } = shallow(balanced(arr, om.index + om[0].length));
  const out = new Set(keys);
  for (const sp of spreads) for (const k of keysOf(sp)) out.add(k);
  return [...out].sort();
}

const nested = {
  _meta: {
    generated_by: "forge/tools/derive_nested.mjs",
    pin: PIN,
    files: FILES,
    note: "Allowed KEY SETS only, per discriminator value. No types, bounds or enums: a bound this "
      + "tool cannot see is the 45g.tag_power_max mistake, and a key set is checkable without zod.",
  },
  effects: family("AllTags", "type"),
  objectives: family("AllObjectives", "task"),
  aiConditions: family("ZodAllAiConditions", "type"),
  aiActions: family("ZodAllAiActions", "type"),
  aiRule: keysOf("AiRule").sort(),
  // Two typed sub-objects one level below an objective, both inline at source:
  //   DialogObjective.nextObjectiveId: z.array(z.object({text, nextObjectiveId}))
  //   idsWithNumberField (attackers, opponentAIs): z.array(z.object({ids, number, quantity}))
  objectiveChoice: inlineArrayObjectKeys("DialogObjective", "nextObjectiveId"),
  idsWithNumber: inlineArrayObjectKeys("idsWithNumberField", null),
  objectiveReward: keysOf("ObjectiveReward").sort(),
  questContent: ["objectives", "reward", "sceneBackground", "sceneCharacters"], // QuestValidatorRawSchema.content
};

for (const [k, v] of Object.entries(nested)) {
  if (k === "_meta") continue;
  const n = Array.isArray(v) ? v.length : Object.keys(v).length;
  if (!n) throw new Error("derived nothing for " + k);
}
process.stdout.write(JSON.stringify(nested, null, 1) + "\n");
