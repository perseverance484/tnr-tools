// Derive the top-level field set of every content validator from the PINNED game source.
// 45d_DATA_entity_schemas.json was generated from a 2026-08-26 drop and is stale against
// 345d18ac (item farm* keys, quest requiredFarmingLevel); the app validates against the pin.
//
//   node tools/derive_fields.mjs /path/to/TheNinjaRPG > src/runner/fields.json
//
// No network. Reads the checked-out source only. Re-run whenever the pin moves.
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

const root = process.argv[2];
if (!root || !existsSync(join(root, "app/src/validators/combat.ts")) || !existsSync(join(root, "app/drizzle/schema.ts"))) { console.error("usage: derive_fields.mjs <TheNinjaRPG checkout>"); process.exit(2); }
const PIN = process.argv[3] || "85cecaebf4ada2e265a18a1405f63c9637443275";

const TARGETS = {
  jutsu:     { file: "app/src/validators/combat.ts",     name: "JutsuValidatorRawSchema" },
  item:      { file: "app/src/validators/combat.ts",     name: "ItemValidatorRawSchema" },
  bloodline: { file: "app/src/validators/combat.ts",     name: "BloodlineValidator" },
  quest:     { file: "app/src/validators/objectives.ts", name: "QuestValidatorRawSchema" },
  gameAsset: { file: "app/src/validators/asset.ts",      name: "gameAssetValidator" },
};

/** Text between a brace opened just before `from`, and its match. */
function balancedFrom(src, from) {
  let i = from, depth = 1;
  const start = i;
  while (i < src.length && depth > 0) {
    const c = src[i], n = src[i + 1];
    if (c === "/" && n === "/") { i = src.indexOf("\n", i); continue; }
    if (c === "/" && n === "*") { i = src.indexOf("*/", i) + 2; continue; }
    if (c === '"' || c === "'" || c === "`") { const q = c; i++; while (i < src.length && src[i] !== q) { if (src[i] === "\\") i++; i++; } i++; continue; }
    if (c === "/" && /[(,=:\s]/.test(src.slice(0, i).trimEnd().slice(-1))) { i++; while (i < src.length && src[i] !== "/") { if (src[i] === "\\") i++; if (src[i] === "\n") break; i++; } i++; continue; } // regex literal
    if (c === "{" || c === "(" || c === "[") depth++;
    else if (c === "}" || c === ")" || c === "]") depth--;
    i++;
  }
  return src.slice(start, i - 1);
}

/** Return the text between the braces of `NAME = z.object({ ... })`, and the line it starts on. */
function objectBody(src, name) {
  const m = new RegExp(`export const ${name}\\s*=\\s*z\\s*\\.object\\(\\{`).exec(src);
  if (!m) throw new Error("not found: " + name);
  return { body: balancedFrom(src, m.index + m[0].length), line: src.slice(0, m.index).split("\n").length };
}

/**
 * The AI record has no content validator: profile.updateAi takes insertAiSchema, which is
 * createInsertSchema(userData).omit({...}).extend(z.object({...})). The userData table is in
 * drizzle/schema.ts; insertAiSchema itself was there until TheNinjaRPG 8d14dbe moved it to
 * validators/aiInput.ts. Both locations are searched, and exactly one must declare it.
 * Derive its effective top-level key set from the table columns so an AI create can be validated
 * BEFORE the placeholder is minted; waiting for a live row means a typo costs a live row.
 */
const AI_SCHEMA_FILES = ["app/drizzle/schema.ts", "app/src/validators/aiInput.ts"];
const AI_SCHEMA_RE = /export const insertAiSchema\s*=\s*createInsertSchema\(\s*userData\s*\)/;
function insertAiSchemaFields(schemaSrc) {
  const t = /export const userData = mysqlTable\(\s*"[^"]*"\s*,\s*\{/.exec(schemaSrc);
  if (!t) throw new Error("not found: userData mysqlTable");
  const columns = topLevelKeys(balancedFrom(schemaSrc, t.index + t[0].length)).keys;
  const hits = AI_SCHEMA_FILES.filter((f) => existsSync(join(root, f)))
    .map((f) => { const src = readFileSync(join(root, f), "utf8"); return { f, src, a: AI_SCHEMA_RE.exec(src) }; })
    .filter((h) => h.a);
  if (hits.length !== 1) throw new Error(hits.length ? `insertAiSchema is declared in ${hits.map((h) => h.f).join(" and ")}; cannot tell which one the server uses` : "not found: insertAiSchema");
  const { f: aiFile, src: aiSrc, a } = hits[0];
  const tail = aiSrc.slice(a.index);
  const om = /\.omit\(\s*\{/.exec(tail);
  const omit = om ? topLevelKeys(balancedFrom(tail, om.index + om[0].length)).keys : [];
  const ex = /\.extend\(\s*(?:z\s*\.object\(\s*)?\{/.exec(tail);
  const extend = ex ? topLevelKeys(balancedFrom(tail, ex.index + ex[0].length)).keys : [];
  if (!columns.length || !omit.length || !extend.length) throw new Error("insertAiSchema extraction produced an empty part");
  const set = new Set(columns.filter((k) => !omit.includes(k)));
  for (const k of extend) set.add(k);
  const fields = {}; for (const k of [...set].sort()) fields[k] = true;
  return { source: `${aiFile}:` + aiSrc.slice(0, a.index).split("\n").length, validator: "insertAiSchema",
           spreads: [], columns: columns.length, omitted: omit.sort(), extended: extend.sort(), fields };
}

/** Top-level `key:` entries of an object body (depth 0 relative to the body). */
function topLevelKeys(body) {
  const keys = [], spreads = [];
  let depth = 0, i = 0, lineStart = true;
  while (i < body.length) {
    const c = body[i], n = body[i + 1];
    if (c === "/" && n === "/") { i = body.indexOf("\n", i); continue; }
    if (c === "/" && n === "*") { i = body.indexOf("*/", i) + 2; continue; }
    if (c === '"' || c === "'" || c === "`") { const q = c; i++; while (i < body.length && body[i] !== q) { if (body[i] === "\\") i++; i++; } i++; continue; }
    if (c === "/" && /[(,=:\s]/.test(body.slice(0, i).trimEnd().slice(-1))) { i++; while (i < body.length && body[i] !== "/" && body[i] !== "\n") { if (body[i] === "\\") i++; i++; } i++; continue; }
    if (depth === 0 && lineStart && c !== "\n") {
      // horizontal whitespace only: a leading \n would let the first key of a body match twice
      const m = /^[^\S\n]*([A-Za-z_$][\w$]*)\s*:/.exec(body.slice(i, i + 200));
      if (m && !keys.includes(m[1])) keys.push(m[1]);
      const s = /^[^\S\n]*\.\.\.(.{0,80})/.exec(body.slice(i, i + 200));
      if (s) spreads.push(s[1].split("\n")[0].trim().replace(/,$/, ""));
    }
    lineStart = c === "\n";
    if (c === "{" || c === "(" || c === "[") depth++;
    else if (c === "}" || c === ")" || c === "]") depth--;
    i++;
  }
  return { keys, spreads };
}

// Spreads (`...name` or `...name.shape`) are resolved against every validator file, so their keys
// are part of the entity's field set. An unresolved spread would mean its fields are silently
// dropped by every fetch-merge update, so it is a hard error, not a review note.
const VALIDATOR_DIR = join(root, "app/src/validators");
const validatorSrc = readdirSync(VALIDATOR_DIR).filter((f) => f.endsWith(".ts")).sort()
  .map((f) => readFileSync(join(VALIDATOR_DIR, f), "utf8")).join("\n");
function spreadKeys(spread, seen = new Set()) {
  const name = /^([A-Za-z_$][\w$]*)(?:\.shape)?\s*,?\s*$/.exec(spread)?.[1];
  if (!name) throw new Error("unresolvable spread: " + spread);
  if (seen.has(name)) return [];
  seen.add(name);
  const decls = [...validatorSrc.matchAll(new RegExp(`(?:export\\s+)?const\\s+${name}\\s*=`, "g"))];
  if (decls.length > 1) throw new Error(`spread ${name} is declared ${decls.length} times across validators/; cannot tell which one is spread`);
  const m = new RegExp(`(?:export\\s+)?const\\s+${name}\\s*=\\s*(?:z\\s*\\.(?:object|strictObject|looseObject)\\(\\s*)?\\{`).exec(validatorSrc);
  if (!m) throw new Error("spread declaration not found: " + name);
  // `z.object({...}).extend({...})` (or .merge/.and) would hide keys after the first body: refuse it.
  const tail = validatorSrc.slice(m.index + m[0].length + balancedFrom(validatorSrc, m.index + m[0].length).length + 1).match(/^\s*\)?\s*\.(\w+)/);
  if (tail && /^(extend|merge|and|safeExtend)$/.test(tail[1])) throw new Error(`spread ${name} uses .${tail[1]}(); resolve it by hand`);
  const { keys, spreads } = topLevelKeys(balancedFrom(validatorSrc, m.index + m[0].length));
  return [...keys, ...spreads.flatMap((s) => spreadKeys(s, seen))];
}

const out = { _provenance: { generator: "forge/tools/derive_fields.mjs", pin: PIN, note: "top-level keys of each entity validator at the pinned commit; spreads are resolved into fields" }, entities: {} };
for (const [entity, t] of Object.entries(TARGETS)) {
  const src = readFileSync(join(root, t.file), "utf8");
  const { body, line } = objectBody(src, t.name);
  const { keys, spreads } = topLevelKeys(body);
  const fields = {}; for (const k of [...keys, ...spreads.flatMap((sp) => spreadKeys(sp))]) fields[k] = true;
  out.entities[entity] = { source: `${t.file}:${line}`, validator: t.name, spreads, fields };
}
out.entities.ai = insertAiSchemaFields(readFileSync(join(root, "app/drizzle/schema.ts"), "utf8"));
process.stdout.write(JSON.stringify(out, null, 1) + "\n");
