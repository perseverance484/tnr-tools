import { readFile, access, readdir } from "node:fs/promises";
import { gzipSync } from "node:zlib";
const metadata = JSON.parse(await readFile("dist/build-meta.json")),
  inputs = Object.keys(metadata.inputs);
if (
  inputs.some(
    (p) =>
      p.startsWith("server/") ||
      p.startsWith("importer/") ||
      p.startsWith("scripts/") ||
      p === "catalog/catalog.v1.json",
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
const html = await readFile("dist/index.html", "utf8");
const [appScript, appOutput] = Object.entries(metadata.outputs).find(
  ([, output]) => output.entryPoint === "src/App.jsx",
);
for (const file of [appScript, appOutput.cssBundle]) {
  if (!/^dist\/static\/App-[A-Z0-9]+\.(js|css)$/.test(file))
    throw Error("Public entry points must have content-hashed filenames");
  await access(file);
  if (!html.includes('"/' + file.slice(5) + '"'))
    throw Error("HTML does not reference the current public bundle");
}
let gzipBytes = 0;
for (const file of Object.keys(metadata.outputs).filter((f) =>
  f.endsWith(".js"),
)) {
  const bytes = await readFile(file);
  if (/data:image\/webp;base64,[A-Za-z0-9+/]{100,}/.test(bytes.toString()))
    throw Error("Official image bytes leaked into public JavaScript");
  const compressed = gzipSync(bytes).length;
  gzipBytes += compressed;
  console.log(`${file}: ${bytes.length} bytes; ${compressed} bytes gzip`);
}
// Measured two-template application: ~230 KB gzip. Keep less than 10% room for
// growth, across all public chunks rather than just the entry point.
if (gzipBytes > 250_000)
  throw Error(
    `Public JavaScript exceeds 250000-byte gzip budget: ${gzipBytes}`,
  );
for (const name of ["index.html", "tnr-guide-importer.user.js"])
  await access("dist/" + name);
await import("./install-smoke.mjs");
console.log(
  "Public authoring/Worker/importer bundles isolated; production harness absent; mobile size budget passed.",
);
