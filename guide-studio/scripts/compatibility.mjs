import { build } from "esbuild";
import { readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
const result = await build({
  write: false,
  entryPoints: [
    "compatibility/constants.ts",
    "compatibility/sanitize.ts",
    "compatibility/guide-html.ts",
    "compatibility/guide-validator.ts",
  ],
  outdir: "compatibility/runtime",
  outExtension: { ".js": ".mjs" },
  bundle: true,
  format: "esm",
  packages: "external",
  alias: {
    "@/drizzle/constants": "./compatibility/constants.ts",
    "@/utils/sanitize": "./compatibility/sanitize.ts",
    "@/libs/guide/html": "./compatibility/guide-html.ts",
  },
});
for (const file of result.outputFiles) {
  if (process.argv.includes("--check")) {
    if ((await readFile(file.path, "utf8")) !== file.text)
      throw Error("Stale compatibility runtime: " + file.path);
  } else await writeFile(file.path, file.contents);
}
const files = {};
for (const f of [
  "sanitize.ts",
  "guide-html.ts",
  "guide-validator.ts",
  "constants.ts",
])
  files[f] = createHash("sha256")
    .update(await readFile("compatibility/" + f))
    .digest("hex");
const manifest = JSON.parse(
  await readFile("compatibility/source-manifest.json"),
);
if (JSON.stringify(files) !== JSON.stringify(manifest.files))
  throw Error("Pinned source copies changed");
console.log("Pinned compatibility source and runtime verified.");
