// Regenerate the committed screen fixtures. Run via `npm run fixtures`.
import { writeFileSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { installDom, renderScenarios } from "../test/screen_scenarios.mjs";

const OUT = join(dirname(fileURLToPath(import.meta.url)), "..", "test", "fixtures", "screens");

installDom();
const scenarios = await renderScenarios();
mkdirSync(OUT, { recursive: true });
for (const f of readdirSync(OUT)) if (f.endsWith(".txt")) rmSync(join(OUT, f));
for (const { name, text } of scenarios) writeFileSync(join(OUT, `${name}.txt`), text, "utf8");
console.log(`wrote ${scenarios.length} screen fixtures to ${OUT}`);
