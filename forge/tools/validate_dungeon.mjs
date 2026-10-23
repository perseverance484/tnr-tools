// JSON stdin bridge for skills/building-tnr-content/scripts/validate.py: one manifest entry in,
// a problem list out. One validation implementation (src/dungeon/validate.mjs), no network.
import { readFileSync } from "node:fs";
import { dungeonProblems } from "../src/dungeon/validate.mjs";
try {
  const entry = JSON.parse(readFileSync(0, "utf8"));
  const create = entry.slot === "create";
  const problems = dungeonProblems(entry.data, null, { preCreate: create });
  if (!["create", "edit", "convert"].includes(entry.slot)) problems.push("invalid slot");
  if (create && !entry.srcId) problems.push("create needs a srcId");
  if (!create && !entry.targetId) problems.push("edit needs targetId");
  process.stdout.write(JSON.stringify(problems));
} catch (e) { process.stdout.write(JSON.stringify([e.message])); }
