// The browser calls api.github.com cross-origin, so every header it sends must be one GitHub's CORS
// preflight allows; anything else makes the browser refuse the request unsent. The run lock read
// once sent cache-control, and no browser claim ever reached GitHub (2026-11-13).
import test from "node:test";
import assert from "node:assert/strict";
import { Github, GITHUB_CORS_HEADERS, readExact, writeExact } from "../src/github.mjs";
import { MemoryStorage } from "./shim.mjs";

function recording() {
  const sent = [];
  const fetchImpl = async (url, init = {}) => {
    sent.push(Object.keys(init.headers ?? {}).map((h) => h.toLowerCase()));
    if ((init.method ?? "GET") === "GET" && url.includes("/contents/state/")) return new Response(JSON.stringify({ content: btoa("{}"), sha: "abc" }), { status: 200 });
    if (init.method === "PUT") return new Response("{}", { status: 200 });
    return new Response("[]", { status: 200 });
  };
  const storage = new MemoryStorage();
  storage.setItem("tnr_bk_gh_v1", JSON.stringify({ pat: "github_pat_test_0000000000" }));
  return { gh: new Github({ fetchImpl, storage }), sent };
}

test("every GitHub request the browser makes uses only CORS-allowed headers", async () => {
  const { gh, sent } = recording();
  await readExact(gh, "state/run_lock.json");
  await writeExact(gh, "state/run_lock.json", "{}", "m", "abc");
  await gh.list();
  await gh.raw("push/x.json");
  await gh.put("harvests/inbox/x.json", "{}", "m");
  assert.ok(sent.length >= 5);
  for (const headers of sent) for (const h of headers) assert.ok(GITHUB_CORS_HEADERS.includes(h), `header ${h} is not allowed by api.github.com CORS`);
});
