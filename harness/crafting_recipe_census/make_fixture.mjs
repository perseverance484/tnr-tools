// node harness/crafting_recipe_census/make_fixture.mjs [--check]
// Writes fixtures/raw_complete.json: a full census of the fake world (fake_server.mjs) run by the
// real console script on a virtual clock. Deterministic; --check fails if the committed copy differs.
import { createRequire } from "node:module";
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { seedWorld, fakeFetch, fakeEnv } from "./fake_server.mjs";

const require = createRequire(import.meta.url);
const C = require("./crafting_recipe_census.console.js");
const out = fileURLToPath(new URL("./fixtures/raw_complete.json", import.meta.url));

const fe = fakeEnv(fakeFetch(seedWorld()).fetch);
const census = C.create(fe.env);
const s = await census.run({ limit: 3 });
if (s.status !== "complete") throw new Error(`fixture run ${s.status}`);
await census.download();
const text = fe.downloads[0].text + "\n";
if (process.argv.includes("--check")) {
  if (readFileSync(out, "utf8") !== text) {
    console.error("fixtures/raw_complete.json is stale; rerun make_fixture.mjs");
    process.exit(1);
  }
  console.log("fixture current");
} else {
  writeFileSync(out, text);
  console.log(`wrote ${out}`);
}
