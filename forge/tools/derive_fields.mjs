// Derive the top-level field set of every content validator from the PINNED game source.
// 45d_DATA_entity_schemas.json was generated from a 2026-08-26 drop and is stale against
// 345d18ac (item farm* keys, quest requiredFarmingLevel); the app validates against the pin.
//
//   node tools/derive_fields.mjs /path/to/TheNinjaRPG > src/runner/fields.json
//
// No network. Reads the checked-out source only. Re-run whenever the pin moves.
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const root = process.argv[2];
if (!root || !existsSync(join(root, "app/src/validators/combat.ts"))) { console.error("usage: derive_fields.mjs <TheNinjaRPG checkout>"); process.exit(2); }
const PIN = process.argv[3] || "345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9";

const TARGETS = {
  jutsu:     { file: "app/src/validators/combat.ts",     name: "JutsuValidatorRawSchema" },
  item:      { file: "app/src/validators/combat.ts",     name: "ItemValidatorRawSchema" },
  bloodline: { file: "app/src/validators/combat.ts",     name: "BloodlineValidator" },
  quest:     { file: "app/src/validators/objectives.ts", name: "QuestValidatorRawSchema" },
  gameAsset: { file: "app/src/validators/asset.ts",      name: "gameAssetValidator" },
};

/** Return the text between the braces of `NAME = z.object({ ... })`, and the line it starts on. */
function objectBody(src, name) {
  const m = new RegExp(`export const ${name}\\s*=\\s*z\\s*\\.object\\(\\{`).exec(src);
  if (!m) throw new Error("not found: " + name);
  let i = m.index + m[0].length, depth = 1;
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
  return { body: src.slice(start, i - 1), line: src.slice(0, m.index).split("\n").length };
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
    if (depth === 0 && lineStart) {
      const m = /^\s*([A-Za-z_$][\w$]*)\s*:/.exec(body.slice(i, i + 200));
      if (m) keys.push(m[1]);
      const s = /^\s*\.\.\.(.{0,80})/.exec(body.slice(i, i + 200));
      if (s) spreads.push(s[1].split("\n")[0].trim());
    }
    lineStart = c === "\n";
    if (c === "{" || c === "(" || c === "[") depth++;
    else if (c === "}" || c === ")" || c === "]") depth--;
    i++;
  }
  return { keys, spreads };
}

const out = { _provenance: { generator: "forge/tools/derive_fields.mjs", pin: PIN, note: "top-level keys of each entity validator at the pinned commit; spreads listed for manual review" }, entities: {} };
for (const [entity, t] of Object.entries(TARGETS)) {
  const src = readFileSync(join(root, t.file), "utf8");
  const { body, line } = objectBody(src, t.name);
  const { keys, spreads } = topLevelKeys(body);
  const fields = {}; for (const k of keys) fields[k] = true;
  out.entities[entity] = { source: `${t.file}:${line}`, validator: t.name, spreads, fields };
}
process.stdout.write(JSON.stringify(out, null, 1) + "\n");
