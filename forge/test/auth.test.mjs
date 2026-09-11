// The protected-auth repair (state/prompt_forge_protected_auth.md), proven without a socket.
//
// Every test here drives the SHIPPED graph through composeForTest -> compose(), a FakeGame that
// answers UNAUTHORIZED for protectedProcedure exactly as enforceUserIsAuthed does at source, and
// a jsdom document. Nothing reaches the network, no Clerk package is installed, and no live
// session, cookie or token exists anywhere in this file: the page auth runtime is a two-boolean
// fake, which is all AuthState is allowed to read from the real one.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";
import { IDBFactory } from "fake-indexeddb";
import { AUTH, AuthState, AuthUnavailable, PROBE_PATH, PROBE_ID } from "../src/transport/auth.mjs";
import { isProtected, PROTECTED_PATHS, PROCEDURES } from "../src/transport/procedures.mjs";
import { parseRouterDecls, forgeTable } from "../tools/auth_pin_diff.mjs";
import { boot } from "../src/main.mjs";
import { CSS, CSS_DOC } from "../src/ui/styles.mjs";
import { App } from "../src/ui/app.mjs";
import { ARM_KEY, isArmed, arm, armHops, disarm, mountHost, whenBodyReady, alreadyMounted, pageAuthRuntime, CARRIER_PATH, ENTRY_PATH, OVERLAY_CLASS } from "../src/ui/takeover.mjs";
import { FakeGame, FakeClient, CrashSignal } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const SRC = join(dirname(fileURLToPath(import.meta.url)), "..", "src");
function walk(dir) { return readdirSync(dir, { withFileTypes: true }).flatMap((d) => d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)]); }

function dom(url = "https://www.theninja-rpg.com/") {
  const d = new JSDOM("<!doctype html><html><head></head><body><div id=\"__next\">the game</div></body></html>", { url });
  const win = d.window;
  win.confirm = () => true;
  win.stop = () => {};
  win.navigator.clipboard = { writeText: async () => {} };
  // jsdom ships neither; production has both, and boot() is the one place that reaches for them.
  // The fetch is a tripwire rather than a transport: no test here runs a job through boot(), so a
  // call to it means the composition root started talking to something.
  win.fetch = async (url) => { throw new Error("no test may reach the network: " + url); };
  win.indexedDB = new IDBFactory();
  for (const [k, v] of Object.entries({ document: win.document, window: win, navigator: win.navigator, location: win.location, confirm: win.confirm, MutationObserver: win.MutationObserver, CSSStyleSheet: win.CSSStyleSheet, HTMLElement: win.HTMLElement })) {
    Object.defineProperty(globalThis, k, { value: v, configurable: true, writable: true });
  }
  return win;
}

/**
 * The same window, rewound to document-start: the parser has produced <html> but not yet <body>.
 * jsdom always builds a body, so it is removed and handed back through insertBody(), which is
 * what the real parser does a moment later. This is the shape independent review FPA-1 is about.
 */
function bodylessDom(url = "https://www.theninja-rpg.com/") {
  const win = dom(url);
  const doc = win.document;
  doc.documentElement.removeChild(doc.body);
  return {
    win, doc,
    insertBody() {
      const body = doc.createElement("body");
      const gameRoot = doc.createElement("div");
      gameRoot.id = "__next";
      gameRoot.textContent = "the game";
      body.appendChild(gameRoot);
      doc.documentElement.appendChild(body);
      return body;
    },
  };
}

/** A fake clerk-js: the two booleans AuthState is permitted to read, and nothing else. */
const clerk = ({ loaded = true, signedIn = true } = {}) => () => ({ loaded, signedIn });

// Default READY: most tests here are about what happens when the SERVER disagrees with a client
// that believes it is signed in, which is the real-world failure. Pass authState explicitly to
// test the client-side gate instead.
function harness({ signedOut = false, authState = AUTH.READY, runtime = null } = {}) {
  const game = new FakeGame({ signedOut });
  return { game, ...composeForTest({ game, authState, runtime }) };
}

const AI = { userId: "ai-0000000000000000000", username: "Road Bandit", isAi: true, level: 10, rank: "GENIN", aiProfileId: null, jutsus: [], items: [] };
const ASSET = { id: "asset-000000000000000", name: "Pin", type: "STATIC", image: "i", url: "u", hidden: false };
const protectedCapture = (userId) => ({ proc: "profile.getAi", input: { userId }, id: userId, persist: "full" });
const publicCapture = (id) => ({ proc: "gameAsset.get", input: { id }, id, persist: "full" });
const writeManifest = () => ({ items: [{ entity: "jutsu", slot: "create", name: "Ember Step", srcId: "ember", data: { name: "Ember Step", description: "d", hidden: true } }] });

// ------------------------------------------------------------------ 1. the procedure table
test("the auth class of every audited procedure is transcribed from source, not derived from the limiter", () => {
  // client_contract.json crud_surface[].auth, each row carrying its own file/line/match at the
  // pinned SHA. protectedProcedure is recorded per procedure so a future limiter change cannot
  // silently move the auth gate.
  assert.equal(isProtected("profile.getAi"), true);      // routers/profile.ts:1121
  assert.equal(isProtected("profile.updateAi"), true);   // routers/profile.ts:1489
  assert.equal(isProtected("quests.update"), true);      // routers/quests.ts:700
  assert.equal(isProtected("gameAsset.get"), false);     // routers/asset.ts:147, publicProcedure
  assert.equal(isProtected("jutsu.getAllNames"), false); // routers/jutsu.ts:257, publicProcedure
  assert.equal(PROTECTED_PATHS.length, 27);
  assert.throws(() => isProtected("jutsu.nope"), /unknown procedure/);
});

test("the table's shape is an invariant: every mutation is protected, every public path is a read", () => {
  // Independent review FPA-3 made the table's completeness security-relevant, so its SHAPE is
  // pinned here rather than left to whoever regenerates it next. Both directions matter: a
  // mutation classified public would let the gate wave through a write the server will refuse,
  // and a public read classified protected would block work that would have succeeded.
  const PUBLIC_READ = /\.(get|getAll|getAllNames|getAllAiNames)$/;
  for (const [path, p] of Object.entries(PROCEDURES)) {
    if (p.kind === "mutation") assert.equal(p.auth, "protected", `${path} is a mutation and must be protected`);
    if (p.auth === "public") {
      assert.equal(p.kind, "query", `${path} is public and must therefore be a read`);
      assert.match(path, PUBLIC_READ, `${path} is public but is not one of the audited read families`);
    }
  }
  // `limited` is a statement about the rate limiter, not about auth. They are exact complements
  // across today's 43 rows, and that coincidence is exactly why auth is transcribed separately:
  // if this ever stops holding, it must be a deliberate edit rather than a silent gate move.
  for (const [path, p] of Object.entries(PROCEDURES)) assert.equal(p.limited, p.auth === "public", `${path}: limiter and auth class disagree`);
});

test("FPA-3: the auth classification is identical at the task pin and at Forge's global pin", () => {
  // The proof itself is docs/handoffs/FORGE_PROTECTED_AUTH_PIN_RECONCILIATION.md, produced by
  // tools/auth_pin_diff.mjs against a read-only checkout of both commits: 0 disagreements across
  // all 43 Forge paths, 0 reclassifications across the whole content surface. This test pins the
  // parsing half of that tool, which is the part that could rot, using a fixture in the exact
  // shape the routers use - the tool needs two game checkouts and so cannot run in this suite.
  const table = parseRouterDecls([
    "export const jutsuRouter = createTRPCRouter({",
    "  getAllNames: publicProcedure",
    "    .input(z.object({}))",
    "  update: protectedProcedure",
    "      nested: publicProcedure",   // deeper indentation is not a procedure declaration
    "});",
  ].join("\n"));
  assert.deepEqual(table, { getAllNames: "publicProcedure", update: "protectedProcedure" });
  // and the tool reads Forge's own table out of the shipped source, not a copy of it
  assert.deepEqual(forgeTable(), Object.fromEntries(Object.entries(PROCEDURES).map(([p, v]) => [p, v.auth])));
});


// ------------------------------------------------------------------ 2. the entry point (brief A, test 1)
test("/forge still works as the operator entry point and hands off to the authenticated host", async () => {
  const win = dom("https://www.theninja-rpg.com/forge");
  const went = [];
  const app = await boot(win, { redirect: (url) => went.push(url) });
  assert.equal(app, null, "the entry page mounts no app: it has no providers to mount one under");
  assert.deepEqual(went, [CARRIER_PATH], "the operator does not have to remember a second URL");
  assert.equal(isArmed(win), true, "the handoff is carried by a per-tab marker, not by the URL");
  assert.match(win.document.body.textContent, /signed-in session/);
});

test("the entry hands off at most twice, then says so instead of bouncing forever", async () => {
  const win = dom("https://www.theninja-rpg.com/forge");
  const went = [];
  await boot(win, { redirect: (url) => went.push(url) });
  await boot(win, { redirect: (url) => went.push(url) });
  await boot(win, { redirect: (url) => went.push(url) });
  assert.equal(went.length, 2);
  assert.equal(isArmed(win), false, "a tab that cannot reach a host is disarmed, not left armed");
  assert.match(win.document.body.textContent, /could not reach an authenticated page/);
});

test("an unarmed game page is untouched: no takeover, no app, no style, nothing removed", async () => {
  const win = dom("https://www.theninja-rpg.com/village");
  const before = win.document.body.innerHTML;
  const app = await boot(win);
  assert.equal(app, null);
  assert.equal(win.document.body.innerHTML, before, "@match now covers the origin; being inert is the contract");
  assert.equal((win.document.adoptedStyleSheets || []).length, 0);
});

// ------------------------------------------------------------------ 3. the carrier (brief B, test 8)
test("the carrier page keeps its provider/auth runtime alive while Forge is mounted", async () => {
  const win = dom("https://www.theninja-rpg.com/");
  arm(win, { hops: 1 });
  win.Clerk = { loaded: true, session: { id: "sess" } };  // stands in for the live ClerkProvider
  const gameRoot = win.document.getElementById("__next");
  const app = await boot(win, { establish: false });
  assert.ok(app instanceof App, "Forge mounts on the carrier");
  assert.equal(win.document.getElementById("__next"), gameRoot, "the game's React root is still mounted");
  assert.equal(gameRoot.textContent, "the game", "and untouched");
  assert.equal(win.Clerk.loaded, true, "the Clerk runtime that keeps the session alive is still there");
  assert.ok(win.document.querySelector(".f-host .f-app"), "Forge is an overlay inside the same document");
  assert.equal(win.document.querySelector(".f-host").parentElement, win.document.body);
  assert.equal(armHops(win), 0, "a successful mount resets the hop counter, so /forge stays reusable in this tab");
  // and closing it hands the page back exactly as it was
  app.close();
  assert.equal(win.document.querySelector(".f-host"), null);
  assert.equal(win.document.getElementById("__next"), gameRoot);
  assert.equal(isArmed(win), false);
});

// ---------------------------------------------------------------- FPA-1: document-start body
//
// The loader keeps @run-at document-start and matches the whole origin. On the carrier that means
// boot() can run before the parser has reached <body>. mountHost() reads doc.body, so calling it
// then throws, the top-level wrapper swallows the rejection, and the operator sees the game with
// the tab armed and Forge never mounted - a valid /forge handoff that silently does nothing.

test("FPA-1: an armed carrier with no body yet mounts when the body arrives, exactly once", async () => {
  const { win, doc, insertBody } = bodylessDom();
  arm(win, { hops: 1 });
  win.Clerk = { loaded: true, session: { id: "sess" } };
  assert.equal(doc.body, null, "the test really is at document-start");

  const booting = boot(win, { establish: false });
  // Nothing may be written to a document Forge cannot mount into yet.
  await new Promise((r) => setTimeout(r, 20));
  assert.equal(doc.body, null);
  assert.equal(doc.documentElement.childElementCount, 1, "only <head>; Forge added nothing while waiting");
  assert.equal((doc.adoptedStyleSheets || []).length, 0, "not even a stylesheet before the body exists");

  const body = insertBody();
  const app = await booting;
  assert.ok(app instanceof App, "Forge mounts as soon as the body is there");
  assert.equal(doc.querySelectorAll("." + OVERLAY_CLASS).length, 1, "exactly one overlay");
  assert.equal(doc.querySelector("." + OVERLAY_CLASS).parentElement, body);
  assert.equal(doc.getElementById("__next").textContent, "the game", "the game's own tree is untouched");
});

test("FPA-1: a second boot on a page that already hosts Forge does not stack a second overlay", async () => {
  const win = dom("https://www.theninja-rpg.com/");
  arm(win, { hops: 1 });
  const first = await boot(win, { establish: false });
  assert.ok(first instanceof App);
  assert.equal(alreadyMounted(win.document), true);
  const second = await boot(win, { establish: false });
  assert.equal(second, null);
  assert.equal(win.document.querySelectorAll("." + OVERLAY_CLASS).length, 1);
});

test("FPA-1: an UNARMED page with no body is inert and never even watches for one", async () => {
  const { win, doc, insertBody } = bodylessDom("https://www.theninja-rpg.com/village");
  const app = await boot(win, { establish: false });
  assert.equal(app, null, "an unarmed page returns before the body wait is entered");
  insertBody();
  await new Promise((r) => setTimeout(r, 20));
  assert.equal(doc.querySelector("." + OVERLAY_CLASS), null, "and stays inert once the body arrives");
  assert.equal((doc.adoptedStyleSheets || []).length, 0);
});

test("FPA-1: mounting without the wait really does throw, which is what made this silent", () => {
  // The hazard, pinned directly: this is what bootHost() used to do first, outside its guard.
  const { doc, win } = bodylessDom();
  assert.throws(() => mountHost(doc, win), TypeError);
});

test("FPA-1: whenBodyReady resolves once, from whichever signal fires, and cleans up after itself", async () => {
  const { win, doc, insertBody } = bodylessDom();
  let resolved = 0;
  const p = whenBodyReady(doc, win).then((b) => { resolved++; return b; });
  insertBody();
  const body = await p;
  assert.equal(body, doc.body);
  // a later mutation must not re-resolve or leave an observer running against the live page
  doc.body.appendChild(doc.createElement("div"));
  await new Promise((r) => setTimeout(r, 20));
  assert.equal(resolved, 1);
  // and a document that already has a body resolves without waiting for anything
  assert.equal(await whenBodyReady(doc, win), doc.body);
});

test("the stylesheet cannot restyle the carrier page: every rule is scoped to the overlay", () => {
  // An adopted stylesheet outlives the overlay node, so ONE bare `body`, `*` or `button` rule
  // would restyle the game page and keep restyling it after Forge is closed.
  const selectors = CSS.split("\n").filter((line) => line.includes("{")).flatMap((line) =>
    line.split(/}\s*/).filter(Boolean).map((rule) => rule.slice(0, rule.indexOf("{")).trim()).filter(Boolean));
  assert.ok(selectors.length > 20, "the stylesheet was not parsed");
  for (const group of selectors) {
    for (const sel of group.split(",")) {
      assert.match(sel.trim(), /^\.f-(host|app|boot)\b/, `unscoped selector "${sel.trim()}" would reach the carrier page`);
    }
  }
  // and the only rules that touch the document itself live in the entry-only sheet
  assert.match(CSS_DOC, /^\s*html, body \{/m);
  assert.ok(!CSS.includes("html, body"));
});

test("boot on a carrier page swallows its own failure rather than breaking the game", async () => {
  const win = dom("https://www.theninja-rpg.com/");
  arm(win, { hops: 1 });
  Object.defineProperty(win, "localStorage", { get() { throw new Error("storage is disabled"); }, configurable: true });
  const app = await boot(win, { establish: false });
  assert.equal(app, null);
  assert.equal(win.document.getElementById("__next").textContent, "the game");
  assert.match(win.document.querySelector(".f-host").textContent, /failed to start/);
});

// ------------------------------------------------------------------ 4. readiness (brief B, test 2)
test("AuthState reads only booleans from the page runtime and never probes before it is loaded", async () => {
  let loaded = false;
  const calls = [];
  const auth = new AuthState({
    client: { call: async (path, input) => { calls.push({ path, input }); return { ok: true, data: null }; } },
    runtime: () => ({ loaded, signedIn: loaded ? true : null }),
    clock: () => Date.now(),
  });
  assert.equal(auth.state, AUTH.UNKNOWN);
  assert.equal(auth.ready, false, "protected mode is not offered before the runtime is ready");
  const establishing = auth.establish({ pollMs: 1, timeoutMs: 2000 });
  await new Promise((r) => setTimeout(r, 5));
  assert.deepEqual(calls, [], "nothing is sent while the page's auth runtime is still starting");
  loaded = true;
  assert.equal(await establishing, AUTH.READY);
  assert.deepEqual(calls, [{ path: PROBE_PATH, input: { userId: PROBE_ID } }], "exactly one probe");
});

test("a loaded runtime that reports nobody signed in is answered without a request at all", async () => {
  let called = 0;
  const auth = new AuthState({ client: { call: async () => { called++; return { ok: true, data: null }; } }, runtime: clerk({ signedIn: false }) });
  assert.equal(await auth.probe(), AUTH.SIGNED_OUT);
  assert.equal(called, 0);
  assert.match(auth.detail, /no signed-in session/);
});

test("a runtime that never appears does not hang the boot; the server probe decides", async () => {
  const auth = new AuthState({ client: { call: async () => ({ ok: true, data: null }) }, runtime: () => null });
  assert.equal(await auth.establish({ pollMs: 1, timeoutMs: 20 }), AUTH.READY);
});

test("pageAuthRuntime reports presence only, and survives a page with no Clerk at all", () => {
  assert.equal(pageAuthRuntime({})(), null);
  assert.deepEqual(pageAuthRuntime({ Clerk: { loaded: false } })(), { loaded: false, signedIn: null });
  assert.deepEqual(pageAuthRuntime({ Clerk: { loaded: true } })(), { loaded: true, signedIn: false });
  assert.deepEqual(pageAuthRuntime({ Clerk: { loaded: true, session: { id: "s" } } })(), { loaded: true, signedIn: true });
});

test("the probe reads the game's answer, persists nothing, and fails closed when it cannot ask", async () => {
  const h = harness({ signedOut: true });
  const auth = h.auth;
  assert.equal(await auth.probe(), AUTH.SIGNED_OUT);
  h.game.signIn();
  assert.equal(await auth.probe(), AUTH.READY);
  // one call per probe, on the protected probe path, for the sentinel id, and never cached
  assert.deepEqual(h.game.calls.map((c) => c.path), [PROBE_PATH, PROBE_PATH]);
  assert.equal(await h.cache.get(PROBE_PATH, PROBE_ID), null, "the probe body is never written to the capture cache");
  const broken = new AuthState({ client: { call: async () => { throw new Error("offline"); } } });
  assert.equal(await broken.probe(), AUTH.UNKNOWN);
  assert.equal(broken.ready, false, "UNKNOWN is not permission");
});

test("the gate refuses protected paths unless READY, and never blocks a public one", () => {
  for (const state of [AUTH.UNKNOWN, AUTH.PROBING, AUTH.SIGNED_OUT]) {
    const auth = new AuthState({ state });
    assert.throws(() => auth.assert("profile.updateAi"), AuthUnavailable);
    assert.doesNotThrow(() => auth.assert("gameAsset.get"));
    assert.equal(auth.allows("quests.update"), false);
    assert.equal(auth.allows("jutsu.getAllNames"), true);
  }
  const ready = new AuthState({ state: AUTH.READY });
  assert.doesNotThrow(() => ready.assert("profile.updateAi"));
});

// ------------------------------------------------------------------ 5. writes (brief E, tests 3 and 6)
test("a signed-out job sends NO protected mutation: the gate refuses before anything is journaled", async () => {
  const h = harness({ signedOut: true, authState: AUTH.SIGNED_OUT });
  h.runner.plan(writeManifest(), { jobId: "w" });
  const s = await h.runner.run("w");
  assert.equal(s.state, "PAUSED");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(h.game.calls.length, 0, "not one request left the device");
  assert.equal(h.game.count("jutsu"), 0, "and nothing was created");
  assert.equal(s.items[0].state, "PLANNED", "the item is untouched, not SENT");
  assert.equal(s.outcome, "open");
});

test("a session that dies mid-job stops the NEXT send instead of discovering it by sending", async () => {
  const h = harness();
  h.runner.plan({ items: [
    { entity: "jutsu", slot: "create", name: "One", srcId: "one", data: { name: "One", description: "d", hidden: true } },
    { entity: "jutsu", slot: "create", name: "Two", srcId: "two", data: { name: "Two", description: "d", hidden: true } },
  ] }, { jobId: "mid" });
  const realHandle = h.game.handle.bind(h.game);
  h.game.handle = (path, input) => { const r = realHandle(path, input); if (path === "jutsu.create") h.auth.state = AUTH.SIGNED_OUT; return r; };
  const s = await h.runner.run("mid");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(h.game.count("jutsu"), 1, "the first item ran; the second was never sent");
  assert.equal(s.items[1].state, "PLANNED");
  assert.ok(!s.items.some((i) => i.state === "SENT"), "a refusal never leaves an item in the ambiguous state");
});

test("UNAUTHORIZED on a protected mutation is a clean refusal, never an ambiguous SENT or a retry", async () => {
  // The gate is bypassed on purpose: this is the case where the session dies between the check
  // and the send, so the mutation really is sent and the server really refuses it.
  const h = harness();
  h.runner.plan(writeManifest(), { jobId: "refuse" });
  h.auth.assert = () => {};
  h.game.signOut();
  const s = await h.runner.run("refuse");
  assert.equal(s.state, "PAUSED");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(s.pause.authRefused, true);
  const item = h.journal.get("refuse").items[0];
  assert.equal(item.state, "FAILED", "the server answered, so the write did not happen: refused, not uncertain");
  assert.equal(item.authRefused, true);
  assert.match(item.error, /SESSION/);
  assert.equal(h.game.calls.filter((c) => c.path === "jutsu.create").length, 1, "no automatic retry");
  // and resume must not treat it as reconcilable work
  assert.ok(!h.journal.get("refuse").items.some((i) => i.state === "SENT"));
});

test("existing SENT semantics for real transport ambiguity are unchanged", async () => {
  // A crash inside the send still leaves the item SENT and pauses ambiguously: the auth work must
  // not have quietly turned every failure into a clean refusal.
  const game = new FakeGame({ crashAt: 2 });   // 1 is the reconciler's pre-create name snapshot
  const h = { game, ...composeForTest({ game }) };
  h.runner.plan(writeManifest(), { jobId: "crash" });
  const s = await h.runner.run("crash");
  assert.equal(s.state, "PAUSED");
  assert.notEqual(s.pause.reason, "SESSION");
  assert.equal(h.journal.get("crash").items[0].state, "SENT");
});

test("reconciliation is not started against a dead session, so nothing is orphaned by a sign-out", async () => {
  const game = new FakeGame({ crashAt: 2 });   // 1 is the reconciler's pre-create name snapshot
  const h = { game, ...composeForTest({ game }) };
  h.runner.plan(writeManifest(), { jobId: "rec" });
  await h.runner.run("rec");
  assert.equal(h.journal.get("rec").items[0].state, "SENT");
  h.auth.state = AUTH.SIGNED_OUT;
  const before = game.calls.length;
  const s = await h.runner.resume("rec");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(game.calls.length, before, "reconciliation issued no reads");
  assert.equal(h.journal.get("rec").items[0].state, "SENT", "still SENT, NOT orphaned: this is a sign-in problem");
});

// ---------------------------------------------------------------- FPA-2: server refusal invalidates
//
// A probe is a snapshot; a session can die a minute later. Before this, a server UNAUTHORIZED
// paused the job but left AuthState READY, so the banner said "TNR session active" while the run
// screen said authentication was unavailable, and Resume would send the next protected request
// against a session the server had already refused.

test("FPA-2: a protected READ refused by the server drives the shared auth state to signed out", async () => {
  const h = harness({ signedOut: true, authState: AUTH.READY });
  h.runner.plan({ items: [], capture: { after: [protectedCapture(AI.userId)] } }, { jobId: "r" });
  assert.equal(h.auth.state, AUTH.READY, "the client starts out believing it is signed in");
  const s = await h.runner.run("r");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(h.auth.state, AUTH.SIGNED_OUT, "the server's answer beats the last probe");
  assert.equal(h.auth.ready, false);
  assert.match(h.auth.detail, /profile\.getAi: UNAUTHORIZED/);
});

test("FPA-2: a protected MUTATION refused by the server drives the shared auth state to signed out", async () => {
  const h = harness({ authState: AUTH.READY });
  h.runner.plan(writeManifest(), { jobId: "m" });
  h.auth.assert = () => {};        // the session dies between the gate and the send
  h.game.signOut();
  const s = await h.runner.run("m");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(h.journal.get("m").items[0].state, "FAILED", "still a clean refusal, not an ambiguous SENT");
  assert.equal(h.auth.state, AUTH.SIGNED_OUT);
});

test("FPA-2: after a refusal, resuming without a successful re-check sends zero protected requests", async () => {
  const h = harness({ signedOut: true, authState: AUTH.READY });
  h.runner.plan({ items: [], capture: { after: [1, 2, 3].map((n) => protectedCapture(`ai-000000000000000000${n}`)) } }, { jobId: "again" });
  await h.runner.run("again");
  assert.equal(h.auth.state, AUTH.SIGNED_OUT);
  const spent = h.game.calls.length;
  assert.equal(spent, 1, "one request proved it; the other two captures were not attempted");
  // a second run() is now stopped by the preflight, before any request
  const s2 = await h.runner.run("again");
  assert.equal(s2.pause.reason, "SESSION");
  assert.equal(h.game.calls.length, spent, "resuming spent nothing");
  // and once the operator signs in and re-checks, the same job completes
  h.game.signIn();
  assert.equal(await h.auth.probe(), AUTH.READY);
  const s3 = await h.runner.run("again");
  assert.equal(s3.state, "DONE");
});

test("FPA-2: a multi-item write job cannot advance to the next protected item after a refusal", async () => {
  const h = harness({ authState: AUTH.READY });
  h.runner.plan({ items: [
    { entity: "jutsu", slot: "create", name: "One", srcId: "one", data: { name: "One", description: "d", hidden: true } },
    { entity: "jutsu", slot: "create", name: "Two", srcId: "two", data: { name: "Two", description: "d", hidden: true } },
  ] }, { jobId: "two" });
  h.auth.assert = () => {};
  h.game.signOut();
  await h.runner.run("two");
  assert.equal(h.auth.state, AUTH.SIGNED_OUT);
  h.auth.assert = AuthState.prototype.assert.bind(h.auth);   // the gate is live again
  const spent = h.game.calls.length;
  const s = await h.runner.run("two");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(h.game.calls.length, spent, "item two was never attempted against the refused session");
  assert.equal(h.journal.get("two").items[1].state, "PLANNED");
  assert.equal(h.game.count("jutsu"), 0, "and nothing was created");
});

// ---------------------------------------------------------------- FPA-2 round 2: AI-rules and
// reconciliation. Round 2 centralised SESSION handling for capture reads, fill reads, verify
// reads, dedupNames and decoded mutation refusals - but _rules()'s two protected profile.getAi
// reads and the reconciler's AI reads were still converted into ordinary content failures and
// orphans. These are the paths One Perfect Crop's enemy AI work actually runs through.

/**
 * An `aiProfile` edit: the profile.getAi -> (toggle) -> ai.updateAiProfile path, and nothing else.
 * `aiProfile` rather than `ai` on purpose - an `ai` item runs _fill() first, whose profile.getAi
 * read is one of the sites round 2 already covered, so it would mask the _rules() reads these
 * tests exist for.
 */
const rulesManifest = (userId) => ({ items: [{
  entity: "aiProfile", slot: "edit", targetId: userId, name: "Road Bandit",
  data: { rules: [{ conditions: [], action: { type: "end_turn" } }], includeDefaultRules: false },
}] });

test("FPA-2b: profile.getAi refused BEFORE the toggle pauses for auth and does not fail the item", async () => {
  const h = harness({ authState: AUTH.READY });
  h.game.seed("ai", { ...AI });
  h.runner.plan(rulesManifest(AI.userId), { jobId: "pre" });
  // the session dies after the preflight gate, on the first protected read inside _rules()
  const real = h.game.handle.bind(h.game);
  h.game.handle = (path, input) => (path === "profile.getAi" ? h.game.signOut() && real(path, input) : real(path, input));

  const s = await h.runner.run("pre");
  assert.equal(s.state, "PAUSED");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(s.pause.path, "profile.getAi");
  assert.equal(h.auth.state, AUTH.SIGNED_OUT, "the shared auth state is invalidated, not left READY");
  const item = h.journal.get("pre").items[0];
  assert.notEqual(item.state, "FAILED", "a sign-in problem is not a terminal content failure");
  assert.equal(h.journal.get("pre").items[0].error ?? null, null);

  // and nothing further is sent until a probe succeeds
  const spent = h.game.calls.length;
  assert.equal((await h.runner.run("pre")).pause.reason, "SESSION");
  assert.equal(h.game.calls.length, spent, "the preflight gate stops the re-run before any request");

  h.game.handle = real;
  h.game.signIn();
  assert.equal(await h.auth.probe(), AUTH.READY);
  const s2 = await h.runner.run("pre");
  assert.equal(s2.state, "DONE", "the same item finishes once the session is back");
  assert.equal(s2.outcome, "success");
});

test("FPA-2b: profile.getAi refused AFTER a landed toggle keeps the item CONFIRMED at rules", async () => {
  const h = harness({ authState: AUTH.READY });
  h.game.seed("ai", { ...AI, aiProfileId: null });
  h.runner.plan(rulesManifest(AI.userId), { jobId: "post" });
  // let the first read and the toggle through; refuse the read that follows the toggle
  const real = h.game.handle.bind(h.game);
  let toggled = false;
  h.game.handle = (path, input) => {
    if (toggled && path === "profile.getAi") h.game.signOut();
    const r = real(path, input);
    if (path === "ai.toggleAiProfile") toggled = true;
    return r;
  };

  const s = await h.runner.run("post");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(h.auth.state, AUTH.SIGNED_OUT);
  assert.ok(h.game.calls.some((c) => c.path === "ai.toggleAiProfile"), "the toggle really did land");
  assert.equal(h.game.rows("ai")[0].aiProfileId != null, true, "the profile row exists server-side");

  const item = h.journal.get("post").items[0];
  assert.equal(item.state, "CONFIRMED", "not FAILED: resume() would skip a terminal item and strand the AI");
  assert.equal(item.phase, "rules", "and it is parked at exactly the step that still owes a write");

  // the rules write was never sent against the dead session
  assert.equal(h.game.calls.filter((c) => c.path === "ai.updateAiProfile").length, 0);
  const spent = h.game.calls.length;
  assert.equal((await h.runner.run("post")).pause.reason, "SESSION");
  assert.equal(h.game.calls.length, spent, "nothing further is sent before a successful re-check");

  // after signing back in the item continues from "rules" and the profile is finished
  h.game.handle = real;
  h.game.signIn();
  assert.equal(await h.auth.probe(), AUTH.READY);
  const s2 = await h.runner.run("post");
  assert.equal(s2.state, "DONE");
  assert.equal(s2.outcome, "success");
  const profile = h.game.rows("aiProfile")[0];
  assert.deepEqual(profile.rules, [{ conditions: [], action: { type: "end_turn" } }], "the rules write finished after re-auth");
  assert.equal(profile.includeDefaultRules, false);
});

test("FPA-2b: a SESSION during AI reconciliation pauses for auth and never orphans the SENT item", async () => {
  // resume() gates before reconciling, but the session can expire between that gate and the
  // reconciler's own protected reads. The reconciler's honest answer to an unreadable record is
  // ORPHANED, which would turn a sign-in prompt into an adopt-or-skip decision about a write that
  // is very likely fine.
  const h = harness({ authState: AUTH.READY });
  h.game.seed("ai", { ...AI });
  h.runner.plan(rulesManifest(AI.userId), { jobId: "rec" });
  // crash inside the toggle send, so the item is left SENT with a real ambiguity to reconcile
  const real = h.game.handle.bind(h.game);
  h.game.handle = (path, input) => {
    const r = real(path, input);
    if (path === "ai.toggleAiProfile") throw new CrashSignal(h.game.calls.length);
    return r;
  };
  await h.runner.run("rec");
  const sent = h.journal.get("rec").items[0];
  assert.equal(sent.state, "SENT");
  assert.equal(sent.phase, "rules-toggle");

  // now the session dies AFTER resume()'s preflight gate, on the reconciler's read
  h.game.handle = real;
  let gated = false;
  h.auth.assert = (path) => { if (!gated) { gated = true; return; } h.game.signOut(); };
  const s = await h.runner.resume("rec");

  assert.equal(s.state, "PAUSED");
  assert.equal(s.pause.reason, "SESSION", "not a generic reconciliation failure");
  assert.equal(h.auth.state, AUTH.SIGNED_OUT, "reconciliation surfaced SESSION to the runner");
  const after = h.journal.get("rec").items[0];
  assert.equal(after.state, "SENT", "still SENT, NOT orphaned: nothing is owed to the operator yet");
  assert.notEqual(after.state, "ORPHANED");
  assert.deepEqual(after.candidates ?? [], []);
});

test("FPA-2: the banner stops claiming a live session, and Resume is withheld until a re-check", async () => {
  const win = dom("https://www.theninja-rpg.com/");
  const game = new FakeGame({ signedOut: true });
  const d = composeForTest({ game, authState: AUTH.READY });
  d.github = { list: async () => [], text: async () => "{}", put: async () => ({ sha: "s" }) };
  const app = new App({ version: "test", storage: d.storage, now: d.clock, ...d });
  app.mount(win.document.body, win.document);
  assert.match(win.document.querySelector(".f-authbar").textContent, /TNR session active/);

  d.runner.plan({ items: [], capture: { after: [protectedCapture(AI.userId)] } }, { jobId: "j" });
  await d.runner.run("j");
  app.go("run", { jobId: "j" });

  const bar = win.document.querySelector(".f-authbar").textContent;
  assert.ok(!/TNR session active/.test(bar), "the banner cannot say the session is live after the server refused it");
  assert.match(bar, /TNR authentication unavailable/);

  const main = win.document.querySelector(".f-main").textContent;
  assert.match(main, /Paused: TNR authentication unavailable/);
  assert.match(main, /re-check the session/i);
  const resume = [...win.document.querySelectorAll(".f-main button")].find((b) => /Resume/.test(b.textContent));
  assert.equal(resume.disabled, true, "a doomed Resume is not offered");

  // tapping it anyway (or from the Jobs list) issues nothing
  const spent = game.calls.length;
  await app.resumeJob("j");
  assert.equal(game.calls.length, spent);

  // after a successful re-check the button comes back
  game.signIn();
  await app.recheckAuth();
  assert.equal(d.auth.state, AUTH.READY);
  app.go("run", { jobId: "j" });
  const resume2 = [...win.document.querySelectorAll(".f-main button")].find((b) => /Resume/.test(b.textContent));
  assert.equal(resume2.disabled, false);
});

// ------------------------------------------------------------------ 6. reads and captures (brief D, tests 4 and 5)
test("public capture-only work still runs while signed out, exactly as the procedure guards allow", async () => {
  const h = harness({ signedOut: true, authState: AUTH.SIGNED_OUT });
  h.game.seed("asset", { ...ASSET });
  h.runner.plan({ items: [], capture: { after: [publicCapture(ASSET.id)] } }, { jobId: "pub" });
  const s = await h.runner.run("pub");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success");
  const job = h.journal.get("pub");
  assert.equal(job.capturesAfter[0].ok, true);
  assert.equal(job.capturesAfter[0].persistOk, true, "the full body is there; no session was needed for it");
});

test("a protected capture pass is refused before the first read when the session is known bad", async () => {
  const h = harness({ signedOut: true, authState: AUTH.SIGNED_OUT });
  h.runner.plan({ items: [], capture: { after: [1, 2, 3, 4, 5].map((n) => protectedCapture(`ai-000000000000000000${n}`)) } }, { jobId: "probe" });
  const s = await h.runner.run("probe");
  assert.equal(s.state, "PAUSED");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(s.pause.path, "profile.getAi");
  assert.equal(h.game.calls.length, 0, "five doomed reads are not spent proving the same thing");
  assert.equal(s.outcome, "open", "and it is not reported as a finished capture job of any kind");
});

test("UNAUTHORIZED from a protected read is an auth failure, not '0 bodies persisted'", async () => {
  // This is the exact shape of harvests/inbox/tnr_results_1789067111434.json: five profile.getAi
  // full captures, all UNAUTHORIZED. 0.3.0 finished DONE/failed and reported a capture problem.
  const h = harness({ signedOut: true, authState: AUTH.READY });   // the client believes it is signed in; the server disagrees
  const ids = [1, 2, 3, 4, 5].map((n) => `ai-000000000000000000${n}`);
  h.runner.plan({ items: [], capture: { after: ids.map(protectedCapture) } }, { jobId: "getai" });
  const s = await h.runner.run("getai");
  assert.equal(s.state, "PAUSED", "0.3.0 said DONE here");
  assert.equal(s.pause.reason, "SESSION");
  assert.equal(s.pause.path, "profile.getAi");
  assert.equal(s.outcome, "open");
  assert.notEqual(s.outcome, "success", "an auth failure is never presented as a successful capture");
  assert.equal(h.game.calls.length, 1, "it stops on the first refusal instead of repeating it five times");
  const job = h.journal.get("getai");
  assert.ok(!(job.capturesAfter || []).length, "no capture entry claims a read that the session was never allowed to make");
});

test("a signed-out job that pauses resumes and completes once the session is back", async () => {
  const h = harness({ signedOut: true, authState: AUTH.SIGNED_OUT });
  h.game.seed("ai", { ...AI });
  h.runner.plan({ items: [], capture: { after: [protectedCapture(AI.userId)] } }, { jobId: "again" });
  assert.equal((await h.runner.run("again")).pause.reason, "SESSION");
  h.game.signIn();
  assert.equal(await h.auth.probe(), AUTH.READY);
  const s = await h.runner.run("again");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success");
  assert.equal(h.journal.get("again").capturesAfter[0].persistOk, true);
});

test("an expired session during read-back is reported as auth, not as an unreadable write", async () => {
  const h = harness();
  h.game.seed("jutsu", { id: "jutsu-00000000000000", name: "Ember Step", description: "d", hidden: true, effects: [] });
  h.runner.plan({ items: [{ entity: "jutsu", slot: "edit", targetId: "jutsu-00000000000000", name: "Ember Step", data: { description: "new" } }] }, { jobId: "verify" });
  const realGet = h.game.handle.bind(h.game);
  let updated = false;
  h.game.handle = (path, input) => {
    if (path === "jutsu.update") updated = true;
    if (updated && path === "jutsu.get") return { ok: false, error: { code: "UNAUTHORIZED", httpStatus: 401, message: "UNAUTHORIZED", path, zodError: null } };
    return realGet(path, input);
  };
  const s = await h.runner.run("verify");
  assert.equal(s.pause.reason, "SESSION");
  const item = h.journal.get("verify").items[0];
  assert.notEqual(item.verify, "unread", "'we could not read it back' hides which problem this is");
});

// ------------------------------------------------------------------ 7. no credential material (brief C, test 7)
test("no credential extraction path exists anywhere in src/", () => {
  // The forbidden list is brief section C, expressed as identifiers. github.mjs is exempt from
  // the Authorization check alone: its bearer goes to api.github.com and never to the game, which
  // CookieSession enforces independently (see the header allowlist test below).
  const banned = [/document\s*\.\s*cookie/, /__session/, /__clerk/, /getToken/, /sessionClaims/, /lastActiveToken/, /\bBearer\b/i];
  for (const file of walk(SRC)) {
    const raw = readFileSync(file, "utf8");
    const code = raw.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^\s*\/\/[^\n]*$/gm, "");
    for (const re of banned) {
      if (re.source.includes("Bearer") && file.endsWith("github.mjs")) continue;
      assert.ok(!re.test(code), `${file} matches forbidden auth pattern ${re}`);
    }
  }
});

test("CookieSession's game-request header allowlist is not widened by the auth work", async () => {
  const { CookieSession, SessionRefused } = await import("../src/transport/session.mjs");
  const s = new CookieSession({ fetchImpl: async () => ({ ok: true }) });
  await assert.rejects(() => s.fetch("/api/trpc/x", { headers: { authorization: "Bearer x" } }), SessionRefused);
  await assert.rejects(() => s.fetch("/api/trpc/x", { headers: { cookie: "a=b" } }), SessionRefused);
  assert.deepEqual([...CookieSession.ALLOWED_HEADERS].sort(), ["accept", "content-type", "x-uploadthing-version"]);
});

test("nothing auth-derived is written to storage or to an exported bundle", async () => {
  const win = dom("https://www.theninja-rpg.com/");
  const storage = new MemoryStorage();
  const game = new FakeGame({ signedOut: true });
  const d = composeForTest({ game, storage, authState: AUTH.UNKNOWN, runtime: clerk({ signedIn: true }) });
  d.github = { list: async () => [], text: async () => "{}", put: async () => ({ sha: "s" }) };
  const app = new App({ version: "test", storage, now: d.clock, ...d });
  app.mount(win.document.body, win.document);
  await app.establishAuth();
  assert.equal(d.auth.state, AUTH.SIGNED_OUT);

  d.runner.plan({ items: [], capture: { after: [protectedCapture(AI.userId)] } }, { jobId: "x" });
  await d.runner.run("x");
  let text = JSON.stringify(storage.snapshot());
  try { text += JSON.stringify(win.sessionStorage.length ? { s: win.sessionStorage.getItem(ARM_KEY) } : {}); } catch { /* jsdom */ }
  let bundle = null;
  app.showExport = (exported) => { bundle = exported; };
  await app.exportJob("x");
  for (const needle of ["__session", "Bearer", "authorization", "Clerk", "clerk", "jwt", "token"]) {
    assert.ok(!text.toLowerCase().includes(needle.toLowerCase()), `${needle} reached persistent storage`);
    assert.ok(!bundle.toLowerCase().includes(needle.toLowerCase()), `${needle} reached the exported bundle`);
  }
  assert.match(bundle, /"pause"/, "the bundle really was produced");
  // The arming marker is the only key this repair adds to persistent storage, and it holds a
  // boolean and a hop count. Nothing about who is signed in, or how, is written down anywhere.
  arm(win, { hops: 1 });
  assert.deepEqual(JSON.parse(win.sessionStorage.getItem(ARM_KEY)), { armed: true, hops: 1 });
  disarm(win);
  assert.equal(win.sessionStorage.getItem(ARM_KEY), null);
});

test("AuthState.describe cannot leak: it is a state string, a sentence and a timestamp", () => {
  const auth = new AuthState({ state: AUTH.READY });
  assert.deepEqual(Object.keys(auth.describe()).sort(), ["at", "detail", "state"]);
});

// ------------------------------------------------------------------ 8. the operator sees it (brief D)
test("the auth banner names the problem and offers a re-check; the run button is blocked with a reason", async () => {
  const win = dom("https://www.theninja-rpg.com/");
  const game = new FakeGame({ signedOut: true });
  const d = composeForTest({ game, authState: AUTH.SIGNED_OUT });
  const manifest = { items: [], capture: { after: [protectedCapture(AI.userId)] } };
  d.github = { list: async () => [{ name: "04_probe.json", path: "push/04_probe.json", sha: "s", size: 1, type: "file" }], text: async () => JSON.stringify(manifest), put: async () => ({ sha: "s" }) };
  const app = new App({ version: "test", storage: d.storage, now: d.clock, ...d });
  app.mount(win.document.body, win.document);

  const bar = win.document.querySelector(".f-authbar").textContent;
  assert.match(bar, /TNR authentication unavailable/);
  assert.match(bar, /Sign in to The Ninja RPG/);
  assert.match(bar, /Public capture-only manifests can still run/);
  assert.ok([...win.document.querySelectorAll(".f-authbar button")].some((b) => /Re-check/.test(b.textContent)));

  await app.selectManifest({ name: "04_probe.json", path: "push/04_probe.json", sha: "s" });
  app.go("manifests");
  const main = win.document.querySelector(".f-main").textContent;
  assert.match(main, /Blocked: TNR authentication is unavailable/);
  assert.match(main, /profile\.getAi/);
  const run = [...win.document.querySelectorAll(".f-main button")].find((b) => /Run captures|Start job/.test(b.textContent));
  assert.equal(run.disabled, true, "a job that cannot authenticate is not offered");

  // a public manifest is still offered while signed out
  d.github.text = async () => JSON.stringify({ items: [], capture: { after: [publicCapture(ASSET.id)] } });
  await app.selectManifest({ name: "05_pub.json", path: "push/05_pub.json", sha: "s2" });
  const run2 = [...win.document.querySelectorAll(".f-main button")].find((b) => /Run captures/.test(b.textContent));
  assert.equal(run2.disabled, false);
});

test("a SESSION pause reads as an authentication problem on the run screen", async () => {
  const win = dom("https://www.theninja-rpg.com/");
  const game = new FakeGame({ signedOut: true });
  const d = composeForTest({ game, authState: AUTH.SIGNED_OUT });
  d.github = { list: async () => [], text: async () => "{}", put: async () => ({ sha: "s" }) };
  const app = new App({ version: "test", storage: d.storage, now: d.clock, ...d });
  app.mount(win.document.body, win.document);
  d.runner.plan({ items: [], capture: { after: [protectedCapture(AI.userId)] } }, { jobId: "j" });
  await d.runner.run("j");
  app.go("run", { jobId: "j" });
  const text = win.document.querySelector(".f-main").textContent;
  assert.match(text, /Paused: TNR authentication unavailable/);
  assert.match(text, /Nothing further was sent/);
  assert.ok(!/0 of 1 reads failed/.test(text), "the capture wording must not stand in for the auth wording");
});

test("a ready session says so, and the banner does not block public work", () => {
  const win = dom("https://www.theninja-rpg.com/");
  const d = composeForTest({ authState: AUTH.READY });
  d.github = { list: async () => [], text: async () => "{}", put: async () => ({ sha: "s" }) };
  const app = new App({ version: "test", storage: d.storage, now: d.clock, ...d });
  app.mount(win.document.body, win.document);
  assert.match(win.document.querySelector(".f-authbar").textContent, /TNR session active/);
});
