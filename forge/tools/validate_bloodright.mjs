// JSON stdin bridge for repository Python tools. One validation implementation, no network.
import { readFileSync } from "node:fs";
import { bloodrightProblems } from "../src/bloodright/validate.mjs";
import { parseManifest, planOrder } from "../src/runner/manifest.mjs";
try {
  const value = JSON.parse(readFileSync(0, "utf8"));
  let problems = [];
  if (value.items) {
    const manifest = parseManifest(value);
    planOrder(manifest);
    problems = manifest.items.filter(it => ["skillTree", "skillTreeFolder"].includes(it.entity)).flatMap(it => bloodrightProblems(it.entity, it.data, null, { preCreate: it.op === "create" }).map(p => `${it.name}: ${p}`));
  } else {
    problems = bloodrightProblems(value.entity, value.data, null, { preCreate: value.slot === "create" });
    if (value.slot === "create" && (!value.srcId || value.data.hidden !== true)) problems.push("create needs srcId and hidden:true");
    if (!["create", "edit", "convert"].includes(value.slot)) problems.push("invalid slot");
    if (value.slot !== "create" && !value.targetId) problems.push("edit needs targetId");
  }
  process.stdout.write(JSON.stringify(problems));
} catch (e) { process.stdout.write(JSON.stringify([e.message])); }
