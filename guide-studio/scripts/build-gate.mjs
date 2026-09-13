import { readFile, access, readdir } from "node:fs/promises";
const metadata = JSON.parse(await readFile("dist/build-meta.json")),
  inputs = Object.keys(metadata.inputs);
if (
  inputs.some(
    (p) =>
      p.startsWith("server/") ||
      p.startsWith("importer/") ||
      p.startsWith("scripts/"),
  )
)
  throw Error("Public bundle crosses the credential/mutation boundary");
const config = await readFile("dist/config.js", "utf8");
if (!config.includes('"localHarness":false'))
  throw Error("Local harness leaked into production");
for (const file of await readdir("dist"))
  if (file.startsWith("local-"))
    throw Error("Local harness file leaked into production");
const worker = await readFile("dist-worker/worker.js", "utf8");
if (worker.includes("/api/trpc") || worker.includes("httpBatchLink"))
  throw Error("Worker must never mutate TNR");
for (const name of [
  "App.js",
  "App.css",
  "index.html",
  "tnr-guide-importer.user.js",
])
  await access("dist/" + name);
console.log(
  "Public authoring/Worker/importer bundles isolated; production harness absent.",
);
