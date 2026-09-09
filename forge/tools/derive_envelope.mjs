#!/usr/bin/env node
// Derive the tRPC 11 fetch-adapter wire format by RUNNING the adapter, not by reading
// builder_bundle.js (brief section 1: "Derive the batch envelope from the tRPC 11 fetch
// adapter, not from the existing bundle").
//
// Method: a real @trpc/client httpBatchLink with superjson, pointed at a fake fetch that
// records the outgoing request and forwards it to a real @trpc/server fetchRequestHandler
// hosting a miniature router whose procedures mirror the SHAPES the game uses:
//   - a publicProcedure-style query returning a row with Date and null fields
//   - a create mutation returning baseServerResponse {success, message: id}
//   - an update mutation that fails Zod validation, so data.zodError is populated
//   - a procedure that throws TOO_MANY_REQUESTS, mirroring ratelimitMiddleware
//   - a role-miss returning HTTP 200 with success:false
// The server is configured exactly as app/src/server/api/trpc.ts: transformer superjson,
// errorFormatter attaching zodError = issues or null.
//
// Output: test/fixtures/envelope/*.json, each holding the request (url, method, headers,
// body) and the raw response (status, body) plus what the client decoded. Zero network:
// fetch never leaves the process. Pinned: @trpc/* 11.18.0, superjson 2.2.6, zod 4.4.3.

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import superjson from "superjson";
import { z, ZodError } from "zod";
import { initTRPC, TRPCError } from "@trpc/server";
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { createTRPCClient, httpBatchLink } from "@trpc/client";

const here = dirname(fileURLToPath(import.meta.url));
const OUT = join(here, "..", "test", "fixtures", "envelope");
const LOCAL_FORGE_URL = pathToFileURL(join(here, "..")).href;
const FIXTURE_FORGE_URL = "file:///home/user/tnr-tools/forge";
const LOCAL_FRAME_RE = /file:\/\/\/home\/user\/tnr-tools\/forge\/tools\/derive_envelope\.mjs:\d+:\d+/g;
mkdirSync(OUT, { recursive: true });

const t = initTRPC.context().create({
  transformer: superjson,
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError: error.cause instanceof ZodError ? error.cause.issues : null,
      },
    };
  },
});

const baseServerResponse = z.object({ success: z.boolean(), message: z.string() });
const FIXED_DATE = new Date("2026-09-01T04:02:38.440Z");
const NEW_ID = "N3wId0000000000000000";

const router = t.router({
  jutsu: t.router({
    get: t.procedure.input(z.object({ id: z.string() })).query(({ input }) => ({
      id: input.id, name: "Row", hidden: true, createdAt: FIXED_DATE, updatedAt: FIXED_DATE,
      bloodlineId: null, effects: [{ type: "damage", power: 150 }],
    })),
    getAllNames: t.procedure.query(() => [
      { id: "a1", name: "Alpha", image: "", injectableInBattle: false },
      { id: "b2", name: `New Jutsu - b2`, image: "", injectableInBattle: false },
    ]),
    create: t.procedure.output(baseServerResponse).mutation(() => ({ success: true, message: NEW_ID })),
    createRoleMiss: t.procedure.output(baseServerResponse).mutation(() => ({ success: false, message: "Not allowed to create jutsu" })),
    update: t.procedure
      .input(z.object({ id: z.string(), data: z.object({ name: z.string(), power: z.number().min(0) }) }))
      .output(baseServerResponse)
      .mutation(({ input }) => ({ success: true, message: `Updated ${input.id}` })),
    limited: t.procedure.query(() => {
      throw new TRPCError({ code: "TOO_MANY_REQUESTS", message: "You are moving too fast! Incident logged for review" });
    }),
  }),
});

async function serve(req) {
  return fetchRequestHandler({ endpoint: "/api/trpc", req, router, createContext: () => ({}) });
}

const records = [];
async function recordingFetch(url, init = {}) {
  const u = String(url);
  const headers = {};
  new Headers(init.headers ?? {}).forEach((v, k) => { headers[k] = v; });
  const bodyText = init.body == null ? null : String(init.body);
  const req = new Request(u, { method: init.method ?? "GET", headers: init.headers, body: init.body });
  const res = await serve(req);
  const resText = await res.clone().text();
  records.push({
    request: { url: u, method: init.method ?? "GET", headers, body: bodyText,
               bodyJson: safeJson(bodyText) },
    response: { status: res.status, headers: Object.fromEntries(res.headers.entries()), body: resText,
                bodyJson: safeJson(resText) },
  });
  return res;
}
function safeJson(s) { try { return s == null ? null : JSON.parse(s); } catch { return null; } }

const client = createTRPCClient({
  links: [httpBatchLink({ url: "https://game.invalid/api/trpc", transformer: superjson, fetch: recordingFetch })],
});

async function scenario(name, fn) {
  records.length = 0;
  let decoded, error = null;
  try { decoded = await fn(); } catch (e) {
    error = { name: e.name, message: e.message, code: e.data?.code ?? e.shape?.data?.code ?? null,
              httpStatus: e.data?.httpStatus ?? null, zodError: e.data?.zodError ?? null,
              shape: e.shape ?? null };
  }
  const out = { scenario: name, pins: { trpc: "11.18.0", superjson: "2.2.6", zod: "4.4.3" },
                exchanges: records.map((r) => r), decoded: reviveForFixture(decoded), error };
  writeFileSync(join(OUT, name + ".json"), JSON.stringify(stableFixture(out), null, 1) + "\n");
  console.log("wrote", name, `(${records.length} exchange${records.length === 1 ? "" : "s"})`);
}

function stableFixture(v) {
  if (typeof v === "string") {
    return v
      .replaceAll(LOCAL_FORGE_URL, FIXTURE_FORGE_URL)
      .replace(LOCAL_FRAME_RE, FIXTURE_FORGE_URL + "/tools/derive_envelope.mjs:0:0");
  }
  if (Array.isArray(v)) return v.map(stableFixture);
  if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, stableFixture(x)]));
  return v;
}

function reviveForFixture(v) {
  if (v instanceof Date) return { __date: v.toISOString() };
  if (Array.isArray(v)) return v.map(reviveForFixture);
  if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, reviveForFixture(x)]));
  return v;
}

await scenario("query_single_get", () => client.jutsu.get.query({ id: "abc" }));
await scenario("query_batched_two", () => Promise.all([client.jutsu.get.query({ id: "a1" }), client.jutsu.getAllNames.query()]));
await scenario("mutation_create_ok", () => client.jutsu.create.mutate());
await scenario("mutation_create_role_miss", () => client.jutsu.createRoleMiss.mutate());
await scenario("mutation_update_ok", () => client.jutsu.update.mutate({ id: "abc", data: { name: "Renamed", power: 150 } }));
await scenario("mutation_update_zod_fail", () => client.jutsu.update.mutate({ id: "abc", data: { name: "x", power: -1 } }));
await scenario("mutation_batched_create_and_update", () =>
  Promise.all([client.jutsu.create.mutate(), client.jutsu.update.mutate({ id: "zz", data: { name: "N", power: 1 } })]));
await scenario("query_too_many_requests", () => client.jutsu.limited.query());
// Mixed outcomes prove per-item status comes from decoded elements, never the shared HTTP status.
await scenario("mutation_batched_mixed_ok_and_zod_fail", () =>
  Promise.allSettled([client.jutsu.update.mutate({ id: "ok1", data: { name: "N", power: 1 } }),
                      client.jutsu.update.mutate({ id: "bad", data: { name: "x", power: -1 } })]));
await scenario("query_batched_one_limited_one_ok", () =>
  Promise.allSettled([client.jutsu.limited.query(), client.jutsu.get.query({ id: "fine" })]));
await scenario("get_on_mutation_path_rejected", async () => {
  const req = new Request("https://game.invalid/api/trpc/jutsu.create?batch=1&input=" + encodeURIComponent('{"0":{"json":null,"meta":{"values":["undefined"]}}}'), { method: "GET" });
  const res = await serve(req);
  const text = await res.text();
  records.push({ request: { url: req.url, method: "GET", headers: {}, body: null, bodyJson: null },
                 response: { status: res.status, headers: Object.fromEntries(res.headers.entries()), body: text, bodyJson: safeJson(text) } });
  const j = JSON.parse(text);
  const code = (Array.isArray(j) ? j[0] : j)?.error?.json?.data?.code ?? (Array.isArray(j) ? j[0] : j)?.error?.data?.code;
  if (code !== "METHOD_NOT_SUPPORTED") throw new Error("expected METHOD_NOT_SUPPORTED, got " + text.slice(0, 200));
  return { code };
});

console.log("fixtures in", OUT);
