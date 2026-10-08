// Scoped projection: deliberately does not refresh the legacy entity contracts.
// Invoke with a checkout of the exact audited source pin; --check compares bytes.
import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
const pin = "1ccdaf078a58101872675e459c8e755b495d4c83";
const root = process.argv[2];
if (!root) throw new Error("usage: node tools/derive_bloodright.mjs GAME_CHECKOUT [--check]");
const actual = execFileSync("git", ["-C", root, "rev-parse", "HEAD"], { encoding: "utf8" }).trim();
if (actual !== pin) throw new Error(`expected audited ${pin}, got ${actual}`);
const paths = ["app/src/validators/combat.ts", "app/src/server/api/routers/skillTree.ts"];
const combat = readFileSync(`${root}/${paths[0]}`, "utf8");
const router = readFileSync(`${root}/${paths[1]}`, "utf8");
const block = (s, start, end) => { const a = s.indexOf(start); const b = s.indexOf(end, a + start.length); if (a < 0 || b < 0) throw new Error(`missing ${start}`); return s.slice(a, b); };
const keys = (s, indent) => [...s.matchAll(new RegExp(`^ {${indent}}(\\w+):`, "gm"))].map(m => m[1]);
const quoted = s => [...s.matchAll(/"([\w-]+)"/g)].map(m => m[1]);
const skillFields = keys(block(combat, "export const SkillTreeValidator", "  .superRefine"), 4);
const folderSource = readFileSync(`${root}/app/src/validators/skillTree.ts`, "utf8");
const folderFields = keys(block(folderSource, "const skillTreeFolderSchema", "});"), 2);
const effectFields = [...new Set([ ...keys(block(combat, "const BaseAttributes", "const PowerAttributes"), 2), ...keys(block(combat, "const PotencyAttributes", "export const IncreasePotencyTag"), 2), "type", "description" ])];
const tags = quoted(block(combat, "export const PotencyTagTypes", "] as const"));
// ElementNames is imported from the constants owner. Locate that owner mechanically.
const constantsPath = "app/drizzle/constants.ts";
const constants = readFileSync(`${root}/${constantsPath}`, "utf8");
const elements = [...quoted(block(constants, "export const BasicElementName =", "] as const")), ...quoted(block(constants, "export const ElementNames =", "] as const"))];
const names = ["get", "getAll", "getAllFolders", "create", "update", "createFolder", "updateFolder"];
const procedures = {};
for (const name of names) {
  const section = router.match(new RegExp(`^  ${name}: (public|protected)Procedure([\\s\\S]*?)(?=^  \\w+: (?:public|protected)Procedure|(?![\\s\\S]))`, "m"));
  if (!section) throw new Error(`missing procedure ${name}`);
  const auth = section[1];
  procedures[`skillTree.${name}`] = { kind: /\.mutation\(/.test(section[2]) ? "mutation" : "query", limited: auth === "public", mcp: /mcp:/.test(section[2]), auth };
}
const files = [paths[0], paths[1], constantsPath, "app/src/validators/skillTree.ts"];
for (const p of files) {
  const pinned = execFileSync("git", ["-C", root, "show", `${pin}:${p}`]);
  if (!pinned.equals(readFileSync(`${root}/${p}`))) throw new Error(`dirty source file: ${p}`);
}
const contract = { _meta: { pin, scope: "Bloodright potency import only; other effects intentionally refused", sources: Object.fromEntries(files.map(p => [p, createHash("sha256").update(readFileSync(`${root}/${p}`)).digest("hex")])) }, skillFields, folderFields, effectFields, tags, elements, procedures };
if (skillFields.length !== 14 || folderFields.length !== 5 || tags.length !== 10 || !elements.includes("Shadow")) throw new Error("audited extraction shape changed");
const out = fileURLToPath(new URL("../src/bloodright/contract.json", import.meta.url));
const text = JSON.stringify(contract, null, 2) + "\n";
if (process.argv.includes("--check")) { if (readFileSync(out, "utf8") !== text) throw new Error("Bloodright projection drift"); }
else writeFileSync(out, text);
console.log(`Bloodright contract: ${pin}; ${skillFields.length} skill fields, ${folderFields.length} folder fields, ${tags.length} potency targets`);
