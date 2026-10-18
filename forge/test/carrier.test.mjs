// The carrier lifecycle (state/prompt_forge_disappearing_overlay.md), proven without a socket.
//
// Every test drives the SHIPPED boot() from src/main.mjs against a jsdom document whose framework
// is the fake in test/carrier.mjs: it hydrates when a test says so, claims a foreign host in the
// position the game's parser leaves it, clears body the way react-dom does, and stamps body the
// way react-dom does. carrier.react.test.mjs runs the decisive cases against react-dom@19.2.8
// itself; this file covers the moments a real reconciler cannot be paused at.

import { test } from "node:test";
import assert from "node:assert/strict";
import { JSDOM } from "jsdom";
import { IDBFactory } from "fake-indexeddb";
import { boot } from "../src/main.mjs";
import { App } from "../src/ui/app.mjs";
import { LAUNCHER_TAG, arm, disarm, isArmed, armHops, armFailure, mountHost, whenCarrierReady, carrierReadiness, carrierHydrated, alreadyMounted, ENTRY_PATH, CARRIER_PATH, MAX_HOPS, OVERLAY_CLASS } from "../src/hosts/userscript/takeover.mjs";
import { stampHydrated, isStamped, hydrateLikeReact, parseShell, clientNavigate, SHELL } from "./carrier.mjs";

const tick = (ms = 80) => new Promise((r) => setTimeout(r, ms));
const launcherButton = (el) => (el.shadowRoot || el).querySelector("button");
const hosts = (doc) => doc.querySelectorAll("." + OVERLAY_CLASS).length;

/** The carrier as the parser leaves it: the server-rendered shell, not yet hydrated. */
function dom(url = "https://www.theninja-rpg.com/", { shell = true } = {}) {
  const d = new JSDOM("<!doctype html><html lang=\"en\"><head></head><body class=\"h-full\"></body></html>", { url });
  const win = d.window;
  win.confirm = () => true;
  win.stop = () => {};
  win.navigator.clipboard = { writeText: async () => {} };
  win.fetch = async (u) => { throw new Error("no test may reach the network: " + u); };
  win.indexedDB = new IDBFactory();
  for (const [k, v] of Object.entries({ document: win.document, window: win, navigator: win.navigator, location: win.location, confirm: win.confirm, MutationObserver: win.MutationObserver, CSSStyleSheet: win.CSSStyleSheet, HTMLElement: win.HTMLElement })) {
    Object.defineProperty(globalThis, k, { value: v, configurable: true, writable: true });
  }
  if (shell) parseShell(win.document);
  return win;
}

/** document-start: <html> and <head> exist, <body> does not. */
function bodylessDom(url = "https://www.theninja-rpg.com/") {
  const win = dom(url, { shell: false });
  const doc = win.document;
  doc.documentElement.removeChild(doc.body);
  return { win, doc, insertBody() { const b = doc.createElement("body"); b.className = "h-full"; doc.documentElement.appendChild(b); return b; } };
}

// ------------------------------------------------------------------ the defect, pinned
test("control: a host mounted before hydration where the parser leaves it is reconciled away (the 0.4.0 defect)", () => {
  // The parser has produced <body> and the first <script>; the shell <div> has not arrived.
  const { win, doc, insertBody } = bodylessDom();
  const body = insertBody();
  parseShell(doc, body, SHELL.slice(0, 1));
  const host = mountHost(doc, win);                    // what bootHost() did at this moment in 0.4.0
  const [shellDiv, section] = parseShell(doc, body, SHELL.slice(1));   // the rest of the page arrives
  assert.deepEqual([...body.children].map((c) => c.tagName), ["SCRIPT", "DIV", "DIV", "SECTION"]);
  const errors = [];
  const { fallback } = hydrateLikeReact(doc, SHELL, { onRecoverableError: (e) => errors.push(e.message) });
  assert.equal(fallback, true, "React claimed the host as the shell and fell back to a client render");
  assert.equal(host.attached(), false, "the overlay is gone");
  assert.equal(doc.body.contains(shellDiv), false, "and the shell was re-rendered with a new identity");
  assert.equal(doc.body.contains(section), false);
  assert.ok(doc.getElementById("__next"), "the game is back, on its own");
  assert.equal(doc.body.style.overflow, "", "the scroll lock went with the body's attributes");
  assert.equal(doc.documentElement.style.overflow, "");
  assert.match(errors[0], /Hydration failed/);
  assert.equal(isStamped(doc), true, "and React now owns body");
});

// ------------------------------------------------------------------ brief tests 3, 4, 5, 6, 8
test("an armed carrier at document-start writes nothing until the framework owns body, then mounts exactly once", async () => {
  const { win, doc, insertBody } = bodylessDom();
  arm(win, { hops: 1 });
  const booting = boot(win, { establish: false });
  await tick();
  assert.equal(doc.body, null, "still waiting for a body");
  assert.equal(doc.documentElement.childElementCount, 1, "only <head>");

  const body = insertBody();
  parseShell(doc, body, SHELL.slice(0, 1));
  await tick();
  assert.equal(hosts(doc), 0, "a body is not a ready carrier: nothing was appended");
  assert.equal((doc.adoptedStyleSheets || []).length, 0, "not even a stylesheet");
  assert.equal(body.style.overflow, "", "no scroll lock on a page Forge has not mounted on");
  const [shellDiv] = parseShell(doc, body, SHELL.slice(1));
  await tick();
  assert.equal(hosts(doc), 0, "the whole page parsed is still not the framework owning it");
  assert.equal(armHops(win), 1, "the hop counter is left as the entry left it while waiting");

  const { fallback } = hydrateLikeReact(doc);
  assert.equal(fallback, false, "with nothing foreign in body the game hydrates cleanly");
  const app = await booting;
  assert.ok(app instanceof App, "Forge mounts once the carrier is ready");
  assert.equal(hosts(doc), 1, "exactly one overlay");
  assert.equal(doc.querySelector("." + OVERLAY_CLASS).parentElement, doc.body);
  assert.equal(doc.getElementById("__next"), shellDiv, "the game's shell keeps its identity");
  assert.equal(shellDiv.textContent, "the game", "and its content");
  assert.equal(armHops(win), 0, "the hop counter resets only now, at the stable-mounted condition");
  assert.equal(armFailure(win), null);
  assert.match(app.logs.map((l) => l.msg).join("\n"), /carrier ready via hydrated/);
  // the stamp is the only thing Forge read from the framework, and it was read by name
  assert.equal(carrierHydrated(doc), true);
});

test("the /forge entry still arms and hands off to the carrier without a second URL", async () => {
  const win = dom("https://www.theninja-rpg.com/forge");
  const went = [];
  assert.equal(await boot(win, { redirect: (u) => went.push(u) }), null);
  assert.deepEqual(went, [CARRIER_PATH]);
  assert.equal(isArmed(win), true);
  assert.equal(armHops(win), 1);
});

test("an unarmed page gets only the launcher button, and only after the game has hydrated", async () => {
  const win = dom("https://www.theninja-rpg.com/village");
  const before = win.document.body.innerHTML;
  assert.equal(await boot(win), null, "boot still returns at once on an unarmed page");
  await tick();
  assert.equal(win.document.body.innerHTML, before, "nothing is added before hydration (it could be claimed)");
  stampHydrated(win.document);
  await tick();
  const launchers = win.document.querySelectorAll(LAUNCHER_TAG);
  assert.equal(launchers.length, 1, "one launcher");
  assert.equal(win.document.body.lastElementChild, launchers[0], "appended after the game's own nodes");
  launchers[0].remove();
  assert.equal(win.document.body.innerHTML, before, "and nothing else in the page changed");
  assert.equal(hosts(win.document), 0);
  assert.equal((win.document.adoptedStyleSheets || []).length, 0, "no stylesheet is installed on the game document");
  assert.equal(isArmed(win), false, "showing the button does not arm the tab");
});

test("launcher: false keeps an unarmed page fully inert", async () => {
  const win = dom("https://www.theninja-rpg.com/village");
  const before = win.document.body.innerHTML;
  assert.equal(await boot(win, { launcher: false }), null);
  stampHydrated(win.document);
  await tick();
  assert.equal(win.document.body.innerHTML, before);
});

test("clicking the launcher goes to /forge, exactly as typing the address does", async () => {
  const win = dom("https://www.theninja-rpg.com/village");
  hydrateLikeReact(win.document);
  const went = [];
  await boot(win, { establish: false, redirect: (u) => went.push(u) });
  await tick();
  const launcher = win.document.querySelector(LAUNCHER_TAG);
  assert.ok(launcher);
  const btn = launcherButton(launcher);
  const seen = [];
  for (const ev of ["mousedown", "pointerdown", "click"]) win.document.addEventListener(ev, () => seen.push(ev));
  btn.dispatchEvent(new win.MouseEvent("mousedown", { bubbles: true, composed: true }));
  btn.click();
  await tick();
  assert.deepEqual(went, [ENTRY_PATH]);
  assert.deepEqual(seen, [], "the game's own document handlers do not see the press or the click");
  assert.equal(hosts(win.document), 0, "nothing opens in place: the carrier is the entry's choice");
  assert.equal(isArmed(win), false, "/forge arms the tab, not the button");
  assert.equal(win.document.querySelector(LAUNCHER_TAG), null);
  btn.click();
  assert.deepEqual(went, [ENTRY_PATH], "a second click on the removed button does nothing");
});

test("no launcher on the /forge entry itself", async () => {
  const win = dom("https://www.theninja-rpg.com" + ENTRY_PATH);
  await boot(win, { redirect: () => {} });
  stampHydrated(win.document);
  await tick();
  assert.equal(win.document.querySelector(LAUNCHER_TAG), null);
});

test("an armed tab whose host never came up gets the launcher back, so /forge can show the diagnostic", async () => {
  const win = dom("https://www.theninja-rpg.com/village");
  hydrateLikeReact(win.document);
  arm(win, { hops: 1 });
  // mounting the overlay fails (bootHost returns null with nothing mounted)
  const real = win.document.body.appendChild;
  win.document.body.appendChild = function (n) { if (n && n.classList && n.classList.contains(OVERLAY_CLASS)) throw new Error("mount refused"); return real.call(this, n); };
  const again = await boot(win, { establish: false });
  win.document.body.appendChild = real;
  assert.equal(again, null);
  await tick();
  assert.equal(win.document.querySelectorAll(LAUNCHER_TAG).length, 1, "the operator has a way back in");
  assert.equal(isArmed(win), true, "the marker is left for /forge to report and clear");
});

test("an armed tab on a page that never became ready gets the launcher back without a second wait", async () => {
  const win = dom("https://www.theninja-rpg.com/village");   // parsed shell, never hydrates
  arm(win, { hops: 1 });
  const app = await boot(win, { establish: false, readiness: { graceMs: 30 } });
  assert.equal(app, null);
  assert.match(armFailure(win) || "", /never became ready/, "the diagnostic is recorded for /forge");
  await tick();
  assert.equal(win.document.querySelectorAll(LAUNCHER_TAG).length, 1, "the button is back at once");
  assert.equal(hosts(win.document), 0);
});

test("closing Forge brings the launcher back, disarmed", async () => {
  const win = dom();
  const doc = win.document;
  arm(win, { hops: 1 });
  hydrateLikeReact(doc);
  const app = await boot(win, { establish: false });
  assert.equal(doc.querySelector(LAUNCHER_TAG), null, "no launcher in an armed tab");
  app.close();
  assert.equal(hosts(doc), 0);
  assert.equal(isArmed(win), false);
  assert.equal(doc.querySelectorAll(LAUNCHER_TAG).length, 1, "the button is back");
});

test("the launcher survives the game's client navigation", async () => {
  const win = dom();
  hydrateLikeReact(win.document);
  await boot(win, { establish: false });
  await tick();
  const shell = clientNavigate(win, "/profile");
  await tick();
  assert.equal(shell.textContent, "profile page");
  assert.equal(win.document.querySelectorAll(LAUNCHER_TAG).length, 1);
});

// ------------------------------------------------------------------ brief test 7
test("the signed-in landing page's client navigation to /profile does not remove Forge", async () => {
  const win = dom();
  arm(win, { hops: 1 });
  hydrateLikeReact(win.document);
  const app = await boot(win, { establish: false });
  assert.ok(app instanceof App);
  const shell = clientNavigate(win, "/profile");
  await tick();
  assert.equal(win.location.pathname, "/profile");
  assert.equal(shell.textContent, "profile page", "the game navigated");
  assert.equal(hosts(win.document), 1, "and Forge is still there");
  assert.ok(win.document.querySelector("." + OVERLAY_CLASS + " .f-app"));
  assert.equal(armHops(win), 0);
});

// ------------------------------------------------------------------ brief test 8: host loss
test("a host lost after mounting is remounted once, the same app, without a second overlay", async () => {
  const win = dom();
  const doc = win.document;
  arm(win, { hops: 1 });
  hydrateLikeReact(doc);
  const app = await boot(win, { establish: false });
  assert.ok(app instanceof App);
  const first = doc.querySelector("." + OVERLAY_CLASS);
  assert.equal(armHops(win), 0);
  // The page reconciles body anyway (a readiness signal that was early, say): the host is
  // claimed and cleared exactly as in the control test.
  doc.body.insertBefore(first, doc.getElementById("__next"));
  const { fallback } = hydrateLikeReact(doc);
  assert.equal(fallback, true);
  assert.equal(doc.body.contains(first), false);
  await tick();
  assert.equal(hosts(doc), 1, "remounted, exactly one overlay");
  const second = doc.querySelector("." + OVERLAY_CLASS);
  assert.notEqual(second, first);
  assert.equal(second.querySelector(".f-app"), app.root, "the same app, with its state, re-homed rather than rebuilt");
  assert.equal(doc.body.style.overflow, "hidden", "the scroll lock is re-applied");
  assert.equal(isArmed(win), true);
  assert.match(app.logs.map((l) => l.msg).join("\n"), /host lost \(1\)[\s\S]*host remounted after loss/);

  // A second loss stops Forge: no third host, no fight, and the reason is recorded where the
  // next /forge will show it.
  second.remove();
  await tick();
  assert.equal(hosts(doc), 0, "no third overlay");
  assert.equal(armHops(win), MAX_HOPS, "the hop counter is at its limit, not reset to success");
  assert.match(armFailure(win), /removed the Forge overlay 2 times/);
  assert.match(app.logs.map((l) => l.msg).join("\n"), /giving up on this page/);
  // and the game page was not written to again
  assert.deepEqual([...doc.body.children].map((c) => c.tagName), ["SCRIPT", "DIV", "SECTION"]);

  // The next /forge in this tab shows the diagnostic instead of bouncing, then starts clean.
  const entry = dom("https://www.theninja-rpg.com/forge");
  entry.sessionStorage.setItem("tnr_forge_armed_v1", win.sessionStorage.getItem("tnr_forge_armed_v1"));
  const went = [];
  assert.equal(await boot(entry, { redirect: (u) => went.push(u) }), null);
  assert.deepEqual(went, [], "no redirect: the operator is told, not bounced");
  assert.match(entry.document.body.textContent, /could not stay on the game page/);
  assert.match(entry.document.body.textContent, /removed the Forge overlay 2 times/);
  assert.equal(isArmed(entry), false, "disarmed, so the next attempt starts clean");
});

test("a carrier that never becomes ready is never written to; the reason surfaces at /forge after the hop limit", async () => {
  const win = dom();
  const doc = win.document;
  arm(win, { hops: 1 });
  const app = await boot(win, { establish: false, readiness: { graceMs: 30 } });
  assert.equal(app, null);
  assert.equal(hosts(doc), 0);
  assert.equal((doc.adoptedStyleSheets || []).length, 0);
  assert.equal(doc.body.style.overflow, "");
  assert.equal(armHops(win), 1, "the counter was not reset: nothing succeeded");
  assert.match(armFailure(win), /never became ready to host an overlay/);
  assert.equal(isArmed(win), true, "still armed: /forge decides, with the reason in hand");

  const went = [];
  const entry = () => { const e = dom("https://www.theninja-rpg.com/forge"); e.sessionStorage.setItem("tnr_forge_armed_v1", win.sessionStorage.getItem("tnr_forge_armed_v1")); return e; };
  let e = entry();
  await boot(e, { redirect: (u) => went.push(u) });
  assert.deepEqual(went, [CARRIER_PATH], "one more try is allowed");
  assert.equal(armHops(e), 2);
  assert.match(armFailure(e), /never became ready/, "the diagnostic rides along with the re-arm");
  win.sessionStorage.setItem("tnr_forge_armed_v1", e.sessionStorage.getItem("tnr_forge_armed_v1"));
  e = entry();
  await boot(e, { redirect: (u) => went.push(u) });
  assert.equal(went.length, 1, "at the limit, no further redirect");
  assert.match(e.document.body.textContent, /could not stay on the game page/);
  assert.match(e.document.body.textContent, /never became ready to host an overlay/);
  assert.equal(isArmed(e), false);
});

test("a stable mount clears an older diagnostic along with the hop count", async () => {
  const win = dom();
  arm(win, { hops: 1, failure: "an earlier attempt" });
  assert.equal(armFailure(win), "an earlier attempt");
  hydrateLikeReact(win.document);
  const app = await boot(win, { establish: false });
  assert.ok(app instanceof App);
  assert.equal(armHops(win), 0);
  assert.equal(armFailure(win), null);
  assert.deepEqual(JSON.parse(win.sessionStorage.getItem("tnr_forge_armed_v1")), { armed: true, hops: 0 }, "a boolean and a hop count, nothing else");
});

// ------------------------------------------------------------------ brief test 9: Close
test("Close disconnects the loss watchers before removing the host, restores scrolling and disarms", async () => {
  const win = dom();
  const doc = win.document;
  arm(win, { hops: 1 });
  hydrateLikeReact(doc);
  const app = await boot(win, { establish: false });
  const shell = doc.getElementById("__next");
  app.close();
  assert.equal(hosts(doc), 0);
  assert.equal(doc.body.style.overflow, "");
  assert.equal(doc.documentElement.style.overflow, "");
  assert.equal(isArmed(win), false);
  assert.equal(doc.getElementById("__next"), shell, "the game is untouched");
  // Nothing is watching any more: body can change however it likes and Forge stays closed.
  doc.body.appendChild(doc.createElement("div")).remove();
  doc.documentElement.appendChild(doc.body);
  await tick();
  assert.equal(hosts(doc), 0, "Close is never mistaken for a loss");
  assert.ok(!app.logs.some((l) => /host lost/.test(l.msg)));
});

// ------------------------------------------------------------------ readiness signals
test("the fallback readiness signal: the page's own runtime settled on a complete document, only when no stamp appears", async () => {
  const win = dom();
  const doc = win.document;
  arm(win, { hops: 1 });
  win.Clerk = { loaded: false };
  const booting = boot(win, { establish: false });
  await tick();
  assert.equal(hosts(doc), 0, "a runtime that has not finished loading is not readiness");
  win.Clerk.loaded = true;
  const app = await booting;
  assert.ok(app instanceof App);
  assert.equal(doc.readyState, "complete");
  assert.match(app.logs.map((l) => l.msg).join("\n"), /carrier ready via runtime/);
  assert.equal(armHops(win), 0);
});

test("carrierReadiness reads names, not internals, and whenCarrierReady resolves once and tears down", async () => {
  const win = dom();
  const doc = win.document;
  assert.equal(carrierReadiness(doc, win), null);
  assert.equal(carrierHydrated(doc), false);
  doc.body.__reactFiber$anything = { do: "not read me" };
  assert.equal(carrierHydrated(doc), true);
  assert.equal(carrierReadiness(doc, win), "hydrated");
  delete doc.body.__reactFiber$anything;
  doc.body.__reactProps$other = {};
  assert.equal(carrierReadiness(doc, win), "hydrated", "either stamp will do");
  delete doc.body.__reactProps$other;
  let resolved = 0;
  const p = whenCarrierReady(doc, win, { pollMs: 5 }).then((v) => { resolved++; return v; });
  await tick(20);
  stampHydrated(doc);
  assert.equal(await p, "hydrated");
  stampHydrated(doc);
  doc.body.appendChild(doc.createElement("div"));
  await tick(30);
  assert.equal(resolved, 1);
  // a document with no body is never ready; one that never becomes ready resolves null after the grace
  assert.equal(carrierReadiness({ body: null, readyState: "complete" }, win), null);
  const fresh = dom();
  assert.equal(await whenCarrierReady(fresh.document, fresh, { graceMs: 20, pollMs: 5 }), null);
  assert.equal(hosts(fresh.document), 0);
});

test("a second boot on a hosted page does not stack, and alreadyMounted stays true across a client navigation", async () => {
  const win = dom();
  arm(win, { hops: 1 });
  hydrateLikeReact(win.document);
  assert.ok((await boot(win, { establish: false })) instanceof App);
  assert.equal(await boot(win, { establish: false }), null);
  clientNavigate(win);
  assert.equal(alreadyMounted(win.document), true);
  assert.equal(hosts(win.document), 1);
  assert.equal(ENTRY_PATH, "/forge");
  disarm(win);
});
