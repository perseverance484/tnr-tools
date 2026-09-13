import { build } from "esbuild";
import { mkdir, copyFile, cp, writeFile, rm } from "node:fs/promises";
const local = process.argv.includes("--local");
await rm("dist", { recursive: true, force: true });
await rm("dist-worker", { recursive: true, force: true });
await mkdir("dist", { recursive: true });
await mkdir("dist-worker", { recursive: true });
const origin = process.env.STUDIO_ORIGIN || "",
  publicJwk = process.env.APPROVAL_PUBLIC_JWK
    ? JSON.parse(process.env.APPROVAL_PUBLIC_JWK)
    : null;
if (publicJwk?.d)
  throw Error("Only a public approval JWK may enter the importer build");
const config = {
  turnstileSiteKey: process.env.TURNSTILE_SITE_KEY || "",
  localHarness: local,
};
await build({
  entryPoints: ["src/App.jsx"],
  bundle: true,
  format: "esm",
  outdir: "dist",
  minify: !local,
  metafile: true,
  write: true,
  define: {
    "process.env.NODE_ENV": JSON.stringify(
      local ? "development" : "production",
    ),
  },
}).then(async (r) =>
  writeFile("dist/build-meta.json", JSON.stringify(r.metafile, null, 2)),
);
await build({
  entryPoints: ["server/worker.mjs"],
  bundle: true,
  format: "esm",
  outfile: "dist-worker/worker.js",
  platform: "browser",
  target: "es2022",
  minify: !local,
});
await build({
  entryPoints: ["importer/panel.mjs"],
  bundle: true,
  format: "iife",
  outfile: "dist/tnr-guide-importer.user.js",
  minify: !local,
  define: {
    IMPORTER_TRUST: JSON.stringify({ studioOrigin: origin, publicJwk }),
  },
  banner: {
    js: "// ==UserScript==\n// @name TNR Guide Studio — approved draft importer\n// @namespace tnr-guide-studio\n// @version 1.0.0\n// @match https://www.theninja-rpg.com/guide*\n// @grant none\n// @run-at document-idle\n// ==/UserScript==",
  },
});
await writeFile(
  "dist/config.js",
  "window.STUDIO_CONFIG=" + JSON.stringify(config) + ";",
);
await writeFile(
  "dist/index.html",
  `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#14272a"><title>TNR Guide Studio</title><link rel="stylesheet" href="/App.css"><script src="/config.js" defer></script>${config.turnstileSiteKey ? '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" defer></script>' : ""}<script type="module" src="/App.js"></script></head><body><div id="root"></div></body></html>`,
);
await cp("public/assets", "dist/assets", { recursive: true });
await copyFile("public/_headers", "dist/_headers");
console.log(
  `Built public Studio, isolated Worker, and TNR-side importer. ${local ? "LOCAL HARNESS." : publicJwk && origin ? "Importer trust configured." : "Importer disabled until operator supplies public trust configuration."}`,
);
