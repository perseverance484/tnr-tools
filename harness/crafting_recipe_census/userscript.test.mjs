// node --test harness/crafting_recipe_census/userscript.test.mjs
// Socket-free: runs the userscript in a vm with a minimal fake DOM and a stub census.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";
import vm from "node:vm";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = readFileSync(path.join(HERE, "crafting_recipe_census.user.js"), "utf8");
const CONSOLE_PATH = "harness/crafting_recipe_census/crafting_recipe_census.console.js";
const header = SRC.slice(0, SRC.indexOf("// ==/UserScript=="));
const meta = (k) => [...header.matchAll(new RegExp(`^// @${k}\\s+(.+)$`, "gm"))].map((m) => m[1].trim());

test("header: game origin only, no grants, census pinned to an immutable commit of the reviewed file", () => {
  assert.deepEqual(meta("match"), ["*://www.theninja-rpg.com/*", "*://theninja-rpg.com/*"]);
  assert.deepEqual(meta("grant"), ["none"]);
  assert.deepEqual(meta("connect"), []);
  const req = meta("require");
  assert.equal(req.length, 1);
  const m = req[0].match(/^https:\/\/cdn\.jsdelivr\.net\/gh\/perseverance484\/tnr-tools@([0-9a-f]{40})\/(.+)$/);
  assert.ok(m, req[0]);
  assert.equal(m[2], CONSOLE_PATH);
  const repo = path.resolve(HERE, "../..");
  const pinned = execFileSync("git", ["-C", repo, "show", `${m[1]}:${CONSOLE_PATH}`], { encoding: "utf8" });
  assert.equal(pinned, readFileSync(path.join(repo, CONSOLE_PATH), "utf8"), "pin is stale: re-pin @require");
});

test("the wrapper issues no request of its own", () => {
  assert.ok(!/\bfetch\s*\(|XMLHttpRequest|GM_|sendBeacon|WebSocket/.test(SRC));
});

class El {
  constructor(tag, doc) { this.tag = tag; this.doc = doc; this.children = []; this.parent = null; this.listeners = {}; this.attrs = {}; this.textContent = ""; }
  setAttribute(k, v) { this.attrs[k] = v; }
  append(...cs) { for (const c of cs) { c.parent = this; this.children.push(c); } }
  remove() { if (this.parent) { this.parent.children = this.parent.children.filter((c) => c !== this); this.parent = null; } }
  addEventListener(t, f) { (this.listeners[t] ||= []).push(f); }
  get isConnected() { let n = this; while (n.parent) n = n.parent; return n === this.doc.body; }
}

function harness(opts = {}) {
  const { hash = "", armed = false } = opts;
  const store = new Map(armed ? [["tnr_crafting_census_armed", "1"]] : []);
  const doc = { created: 0 };
  doc.body = new El("body", doc);
  doc.createElement = (t) => { doc.created++; return new El(t, doc); };
  const calls = [];
  const timers = [];
  const census = {
    run: async () => { calls.push("run"); if (opts.runError) throw new Error(opts.runError); return { status: "complete" }; },
    stop: () => calls.push("stop"),
    status: async () => ({ status: "not_started" }),
    logs: () => ["[census] hello"],
    RUNTIME: "1.0.1",
    download: async () => { calls.push("download"); return "f.json"; },
    reset: async () => calls.push("reset"),
  };
  const window = {
    location: { hash },
    sessionStorage: { getItem: (k) => store.get(k) ?? null, setItem: (k, v) => store.set(k, v), removeItem: (k) => store.delete(k) },
    document: doc,
    TNRCraftCensus: opts.noWindowCensus ? undefined : census,
    confirm: () => true,
  };
  const ctx = vm.createContext({ window, ...(opts.noWindowCensus ? { TNRCraftCensus: census } : {}), setInterval: (f) => { timers.push(f); return timers.length; }, clearInterval: () => { timers.length = 0; } });
  vm.runInContext(SRC, ctx);
  const panel = () => doc.body.children.find((c) => c.attrs && c.tag === "div");
  const click = async (label) => {
    const b = panel().children[1].children.find((x) => x.textContent === label);
    for (const f of b.listeners.click) await f();
    for (let i = 0; i < 5; i++) await new Promise((r) => setImmediate(r));
  };
  return { doc, store, calls, timers, panel, click };
}

test("unarmed tab: nothing is created and nothing runs", () => {
  const h = harness();
  assert.equal(h.doc.created, 0);
  assert.equal(h.timers.length, 0);
  assert.deepEqual(h.calls, []);
});

test("#craft-census arms the tab and shows the panel; buttons drive the census", async () => {
  const h = harness({ hash: "#craft-census" });
  assert.equal(h.store.get("tnr_crafting_census_armed"), "1");
  assert.ok(h.panel(), "panel attached");
  assert.deepEqual(h.calls, [], "arming alone runs nothing");
  await h.click("Run");
  await h.click("Stop");
  await h.click("Download");
  assert.match(h.panel().children[2].textContent, /Saved f\.json/);
  await h.click("Reset");
  assert.deepEqual(h.calls, ["run", "stop", "download", "reset"]);
});

test("armed tab re-attaches the panel after hydration clears body; Close disarms", async () => {
  const h = harness({ armed: true });
  const p = h.panel();
  h.doc.body.children = [];
  p.parent = null;
  assert.equal(p.isConnected, false);
  h.timers[0]();
  assert.equal(p.isConnected, true);
  await h.click("Close");
  assert.equal(h.store.has("tnr_crafting_census_armed"), false);
  assert.equal(p.isConnected, false);
});

test("a failing run() is shown on the panel, with the census log", async () => {
  const h = harness({ armed: true, runError: "indexedDB open blocked" });
  await h.click("Run");
  const [, , out, logView] = h.panel().children;
  assert.match(out.textContent, /Run error: indexedDB open blocked/);
  assert.match(logView.textContent, /\[census\] hello/);
});

test("a census published only on the sandbox global is still found", async () => {
  const h = harness({ armed: true, noWindowCensus: true });
  await h.click("Run");
  assert.deepEqual(h.calls, ["run"]);
});
