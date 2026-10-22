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

import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

const root = process.argv[2];
const PIN = process.argv[3] || "107d7a86894f806a4c9cec89effef5992118a0ed";
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
// Validator files that only exist at later pins; read when present so earlier pins derive unchanged.
const OPTIONAL_FILES = {
  rewardPackages: "app/src/validators/rewardPackages.ts",
};
for (const [k, f] of Object.entries(OPTIONAL_FILES)) if (existsSync(join(root, f))) FILES[k] = f;
// Every other validator file is searched too, after the core ones: upstream moves shared field
// groups into new modules (mapLocationFields in validators/mapLocation.ts at 85cecae), and a group
// this tool cannot find is a hard error, never a silent omission. A name declared in more than one
// file is refused rather than guessed (bodyOf).
const SEARCHED = {};
for (const f of readdirSync(join(root, "app/src/validators")).filter((n) => n.endsWith(".ts")).sort()) {
  const rel = "app/src/validators/" + f;
  if (!Object.values(FILES).includes(rel)) SEARCHED[f.replace(/\.ts$/, "")] = rel;
}
const src = Object.fromEntries(Object.entries({ ...FILES, ...SEARCHED }).map(([k, f]) => [k, readFileSync(join(root, f), "utf8")]));
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
  const found = [];
  for (const [file, text] of Object.entries(src)) {
    // Upstream also writes \`z\n  .object({\` and z.strictObject/looseObject; whitespace before the dot is allowed.
    const re = new RegExp(`(?:export\\s+)?const\\s+${name}\\s*=\\s*(z\\s*\\.(?:object|strictObject|looseObject)\\(\\s*)?\\{`, "m");
    const m = re.exec(text);
    if (m) found.push([file, balanced(text, m.index + m[0].length)]);
  }
  if (found.length > 1) throw new Error(`${name} is declared in ${found.map((f) => f[0]).join(", ")}; cannot tell which one is meant`);
  return found.length ? found[0][1] : null;
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
  const m = new RegExp(`(?:export\\s+)?const\\s+${name}\\s*=\\s*z\\s*\\.(?:object|strictObject|looseObject)\\(\\s*([A-Za-z_$][\\w$]*)\\s*\\)`, "m").exec(ALL);
  return m ? m[1] : null;
}

/**
 * `const NAME = BASE.omit({ k: true }).extend({ ... })` - a schema derived from another by a chain
 * of .omit / .pick / .extend calls (ElementalDamageTag at 6524d0f). Returns {base, steps} or null.
 * Any other chained call (.merge, .partial, .refine, ...) is a hard error: its key set is not
 * something this tool can read, so it must not be guessed.
 */
function derivedOf(name) {
  for (const text of Object.values(src)) {
    const m = new RegExp(`(?:export\\s+)?const\\s+${name}\\s*=\\s*([A-Za-z_$][\\w$]*)\\s*\\.\\s*(?=[A-Za-z_$])`, "m").exec(text);
    if (!m || m[1] === "z") continue;
    const steps = [];
    let i = m.index + m[0].length;
    for (;;) {
      const cm = (steps.length ? /^\s*\.\s*([A-Za-z_$][\w$]*)\s*\(\s*\{/ : /^([A-Za-z_$][\w$]*)\s*\(\s*\{/).exec(text.slice(i));
      if (!cm) break;
      if (!["omit", "pick", "extend"].includes(cm[1])) {
        throw new Error(`${name}: unsupported schema derivation .${cm[1]}() on ${m[1]}`);
      }
      const open = i + cm[0].length;
      const body = balanced(text, open);
      steps.push({ op: cm[1], body });
      i = open + body.length + 1; // past the closing brace
      const close = /^\s*\)/.exec(text.slice(i));
      if (!close) throw new Error(`${name}: .${cm[1]}() takes more than one object argument`);
      i += close[0].length;
    }
    if (!steps.length) throw new Error(`${name}: derived from ${m[1]} by a call this tool cannot read`);
    const tail = /^\s*([;\n]|$)/.exec(text.slice(i));
    if (!tail) throw new Error(`${name}: unsupported call chained after .${steps.at(-1).op}()`);
    return { base: m[1], steps };
  }
  return null;
}

/** Every key of a schema, spreads resolved (across files), deduplicated. */
function keysOf(name, seen = new Set()) {
  if (seen.has(name)) return [];
  seen.add(name);
  const alias = aliasOf(name);
  if (alias) return keysOf(alias, seen);
  const derivation = derivedOf(name);
  if (derivation) {
    let out = new Set(keysOf(derivation.base, new Set(seen)));
    for (const { op, body } of derivation.steps) {
      const { keys, spreads } = shallow(body);
      if (op === "extend") {
        for (const k of keys) out.add(k);
        for (const s of spreads) for (const k of keysOf(s, new Set(seen))) out.add(k);
      } else {
        if (spreads.length) throw new Error(`${name}: spread inside .${op}()`);
        for (const k of keys) if (!out.has(k)) throw new Error(`${name}: .${op}() names ${k}, which ${derivation.base} does not have`);
        out = op === "omit" ? new Set([...out].filter((k) => !keys.includes(k))) : new Set(keys);
      }
    }
    return [...out];
  }
  const body = bodyOf(name);
  if (body == null) throw new Error("cannot find declaration for " + name);
  const { keys, spreads } = shallow(body);
  const out = new Set(keys);
  for (const s of spreads) for (const k of keysOf(s, seen)) out.add(k);
  return [...out];
}

/** The discriminator values a schema accepts on `field` (z.literal, z.enum([...]) or z.enum(CONST)). */
function discriminators(name, field) {
  let body = bodyOf(name);
  if (body == null) {
    // A derived schema must declare its own discriminator in an .extend(); inheriting the base's
    // would file the derived key set under the base's value and silently overwrite it.
    const derivation = derivedOf(name);
    if (!derivation) throw new Error("cannot find declaration for " + name);
    body = derivation.steps.filter((s) => s.op === "extend").map((s) => s.body).join("\n");
    if (!new RegExp(`\\b${field}\\s*:`).test(body)) {
      throw new Error(`${name}: derived schema does not redeclare its ${field} discriminator`);
    }
  }
  const re = new RegExp(`\\b${field}\\s*:\\s*z\\.(literal|enum)\\(`, "m");
  const m = re.exec(body);
  if (!m) return [];
  const inner = stripComments(balanced(body, m.index + m[0].length));
  const literals = [...inner.matchAll(/"([^"]+)"/g)].map((x) => x[1]);
  if (literals.length) return literals;
  const ref = /^\s*([A-Za-z_$][\w$]*)/.exec(inner);
  if (!ref) return [];
  const cm = new RegExp(`const\\s+${ref[1]}\\s*=\\s*\\[`, "m").exec(ALL);
  if (!cm) throw new Error(`cannot resolve enum source ${ref[1]} for ${name}.${field}`);
  // A commented-out member (SimpleTasks: // "anbu_kills") is not a member: the server's z.enum
  // refuses it, so Forge must not accept it as a discriminator.
  return [...stripComments(balanced(ALL, cm.index + cm[0].length)).matchAll(/"([^"]+)"/g)].map((x) => x[1]);
}

/** Source text with // and /* *\/ comments removed (string literals left intact). */
function stripComments(s) {
  let out = "", i = 0;
  while (i < s.length) {
    const c = s[i], n = s[i + 1];
    if (c === "/" && n === "/") { const j = s.indexOf("\n", i); i = j < 0 ? s.length : j; continue; }
    if (c === "/" && n === "*") { const j = s.indexOf("*/", i + 2); i = j < 0 ? s.length : j + 2; continue; }
    if (c === '"' || c === "'" || c === "`") { const q = c; let j = i + 1; while (j < s.length && s[j] !== q) { if (s[j] === "\\") j++; j++; } out += s.slice(i, j + 1); i = j + 1; continue; }
    out += c; i++;
  }
  return out;
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

/**
 * QuestValidatorRawSchema.content: its top-level keys (spread groups resolved, source order) and
 * the schema name its `reward` field references. Read from source, not hand-kept: a key missing
 * here is refused by Forge and reset to its default by the server on every shallow content merge.
 */
function questContentShape() {
  const body = bodyOf("QuestValidatorRawSchema");
  if (body == null) throw new Error("cannot find QuestValidatorRawSchema");
  const m = /\bcontent\s*:\s*z\s*\.\s*object\(\s*\{/.exec(body);
  if (!m) throw new Error("QuestValidatorRawSchema.content is not an inline z.object({...})");
  const inner = balanced(body, m.index + m[0].length);
  const { keys, spreads } = shallow(inner);
  const out = [...keys];
  for (const sp of spreads) for (const k of keysOf(sp)) if (!out.includes(k)) out.push(k);
  const r = /(?:^|[\s,{])reward\s*:\s*([A-Za-z_$][\w$]*)\s*[,\n]/.exec(inner);
  if (!r) throw new Error("QuestValidatorRawSchema.content.reward is not a named schema");
  return { keys: out, reward: r[1] };
}

const derived = {
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
  // content.reward is checked against the schema QuestValidatorRawSchema.content.reward names at
  // the pin (ObjectiveReward at 345d18ac; QuestReward, which adds reward_packages, at 94f9d84).
  objectiveReward: keysOf(questContentShape().reward).sort(),
  questContent: questContentShape().keys,
};

for (const [k, v] of Object.entries(derived)) {
  const n = Array.isArray(v) ? v.length : Object.keys(v).length;
  if (!n) throw new Error("derived nothing for " + k);
}

// SHARED KEY-SET TABLE. The 165 key sets at the pin are 53 distinct arrays: every effect tag that
// takes the same shape allows the same keys. Emitting each one once and naming it by index is a
// storage encoding of the same contract - forge/src/runner/validate.mjs expandNested() restores it,
// and a round-trip test asserts the restored surface byte-for-byte. It is done here, in the
// generator, so a re-derivation at this pin reproduces the committed file rather than reverting it.
//
// Allocation order is the traversal order below, which is deterministic, so the same source at the
// same pin emits the same indices.
const sets = [];
const index = new Map();
const ref = (keys) => {
  const k = JSON.stringify(keys);
  if (!index.has(k)) { index.set(k, sets.length); sets.push(keys); }
  return index.get(k);
};

const nested = {
  _meta: {
    generated_by: "forge/tools/derive_nested.mjs",
    pin: PIN,
    files: FILES,
    // the rest of app/src/validators/*.ts, searched for spread groups; counted, not listed (bundle size)
    searched: Object.keys(SEARCHED).length,
    note: "Allowed KEY SETS only, per discriminator value. No types, bounds or enums: a bound this "
      + "tool cannot see is the 45g.tag_power_max mistake, and a key set is checkable without zod.",
    format: "Shared key-set table. `sets` holds every distinct allowed key set once; each section "
      + "value is an index into it (or a map of discriminator value -> index). "
      + "forge/src/runner/validate.mjs expandNested() restores the per-discriminator key sets and "
      + "FAILS CLOSED on an index this file does not define.",
  },
  sets,
};
for (const [section, v] of Object.entries(derived)) {
  nested[section] = Array.isArray(v)
    ? ref(v)
    : Object.fromEntries(Object.entries(v).map(([discriminator, keys]) => [discriminator, ref(keys)]));
}
process.stdout.write(JSON.stringify(nested, null, 1) + "\n");
