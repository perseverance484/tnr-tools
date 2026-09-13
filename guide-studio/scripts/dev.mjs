import { createServer } from "node:http";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import { resolve, extname } from "node:path";
import { generateKeyPair, exportJWK } from "jose";
import registry from "../catalog/catalog.v1.json" with { type: "json" };
import { createService } from "../server/service.mjs";
import { MemoryStore, MemoryBucket } from "../server/store.mjs";
import { approvalSigner } from "../server/auth.mjs";
import { build } from "esbuild";
const port = Number(process.env.PORT || 4173),
  origin = `http://localhost:${port}`;
const { privateKey, publicKey } = await generateKeyPair("EdDSA", {
  extractable: true,
});
const publicJwk = await exportJWK(publicKey),
  privateJwk = await exportJWK(privateKey);
privateJwk.kid = "local-only";
process.env.APPROVAL_PUBLIC_JWK = JSON.stringify(publicJwk);
process.env.STUDIO_ORIGIN = origin;
process.argv.push("--local");
await import("./build.mjs");
const store = new MemoryStore(),
  bucket = new MemoryBucket();
const service = createService({
  store,
  bucket,
  registry,
  origin,
  authenticate: async () => ({ id: "local-staff-harness" }),
  verifyTurnstile: async (token) => {
    if (token !== "local-harness") throw Error("Local harness token required");
  },
  signApproval: approvalSigner(JSON.stringify(privateJwk)),
});
// These mocks are served only by this localhost development process, never included in production.
await build({
  entryPoints: ["test/browser-importer.mjs"],
  bundle: true,
  format: "iife",
  outfile: "dist/local-importer.js",
  define: {
    IMPORTER_TRUST: JSON.stringify({ studioOrigin: origin, publicJwk }),
  },
});
await writeFile(
  "dist/local-importer.html",
  '<!doctype html><html><meta charset="utf-8"><title>Local TNR importer harness</title><h1>Native guide importer · local mocks only</h1><script src="/local-importer.js"></script></html>',
);
const types = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".webp": "image/webp",
};
createServer(async (req, res) => {
  try {
    if (req.headers.host !== `localhost:${port}`) {
      res.writeHead(403);
      return res.end("Local harness only");
    }
    if (req.url.startsWith("/api/") || req.url.startsWith("/guide-assets/")) {
      const request = new Request(origin + req.url, {
        method: req.method,
        headers: req.headers,
        ...(!["GET", "HEAD"].includes(req.method)
          ? { body: req, duplex: "half" }
          : {}),
      });
      const response = await service(request);
      res.writeHead(response.status, Object.fromEntries(response.headers));
      return res.end(Buffer.from(await response.arrayBuffer()));
    }
    const pathname = new URL(req.url, origin).pathname;
    const file = resolve(
      "dist",
      "." +
        (pathname === "/" || pathname === "/staff" ? "/index.html" : pathname),
    );
    if (!file.startsWith(resolve("dist") + "/"))
      throw Error("Path not allowed");
    const bytes = await readFile(file);
    res.writeHead(200, {
      "Content-Type": types[extname(file)] || "application/octet-stream",
      "Cache-Control": "no-store",
    });
    res.end(bytes);
  } catch {
    res.writeHead(404);
    res.end("Not found");
  }
}).listen(port, "0.0.0.0", () =>
  console.log(
    `LOCAL ONLY ${origin} — memory review queue, fake Turnstile/staff, ephemeral signing key. No TNR requests.`,
  ),
);
