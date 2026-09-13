// The disappearing overlay, reproduced against react-dom@19.2.8 - the version the production game
// pins (studie-tech/TheNinjaRPG@98d0eca5 app/package.json) - in jsdom, with no socket anywhere.
//
// The document is shaped like the game's: app/src/app/layout.tsx renders <html> and <body> as React
// elements (a <script> first, then the layout shell <div>, then trailing providers), so Next calls
// hydrateRoot(document, ...). The first test pins the 0.4.0 defect; the second proves the shipped
// boot() waits for React to own <body>, mounts once, survives the client navigation that
// HomeLanding.tsx performs, and closes cleanly. test/carrier.mjs's fake is calibrated to this file.

import { test } from "node:test";
import assert from "node:assert/strict";
import { JSDOM } from "jsdom";
import { IDBFactory } from "fake-indexeddb";
import React from "react";
import { renderToString } from "react-dom/server";
import { hydrateRoot } from "react-dom/client";
import { boot } from "../src/main.mjs";
import { App } from "../src/ui/app.mjs";
import { arm, isArmed, armHops, mountHost, carrierHydrated, OVERLAY_CLASS } from "../src/ui/takeover.mjs";

const e = React.createElement;
function Layout({ children }) {
  return e("html", { lang: "en", style: { "--font-scale": 1 }, suppressHydrationWarning: true },
    e("head", null, e("title", null, "TNR")),
    e("body", { className: "h-full" },
      e("script", { type: "application/ld+json", dangerouslySetInnerHTML: { __html: "{}" } }),
      e("div", { id: "layout" }, e("nav", null, "nav"), e("main", null, children)),
      e("section", { "aria-label": "toasts" })));
}
const landing = e(Layout, null, e("p", { id: "landing" }, "Forwarding to profile"));
const profile = e(Layout, null, e("p", { id: "profile" }, "the profile page"));
const SSR = "<!DOCTYPE html>" + renderToString(landing);
const settle = (ms = 60) => new Promise((r) => setTimeout(r, ms));

function carrier() {
  const d = new JSDOM(SSR, { url: "https://theninja-rpg.com/" });
  const win = d.window;
  win.confirm = () => true;
  win.stop = () => {};
  win.navigator.clipboard = { writeText: async () => {} };
  win.fetch = async (u) => { throw new Error("no test may reach the network: " + u); };
  win.indexedDB = new IDBFactory();
  for (const [k, v] of Object.entries({ document: win.document, window: win, navigator: win.navigator, location: win.location, confirm: win.confirm, MutationObserver: win.MutationObserver, CSSStyleSheet: win.CSSStyleSheet, HTMLElement: win.HTMLElement, Node: win.Node })) {
    Object.defineProperty(globalThis, k, { value: v, configurable: true, writable: true });
  }
  return win;
}

test("react-dom 19.2.8: a host appended before hydration, ahead of the layout shell, is cleared by the client-render fallback (0.4.0)", async () => {
  const win = carrier();
  const doc = win.document;
  const shell = doc.getElementById("layout");
  const host = mountHost(doc, win);
  doc.body.insertBefore(host.body, shell);    // where a document-start mount lands once the shell streams in after it
  assert.equal(carrierHydrated(doc), false, "React has not run yet");
  const errors = [];
  const root = hydrateRoot(doc, landing, { onRecoverableError: (err) => errors.push(err.message) });
  await settle();
  assert.equal(host.attached(), false, "the overlay is gone");
  assert.equal(doc.body.contains(shell), false, "the shell was re-rendered with a new identity: React client-rendered the root");
  assert.ok(doc.getElementById("layout") && doc.getElementById("landing"), "the game is back on its own");
  assert.equal(doc.body.style.overflow, "", "the scroll lock went with body's attributes");
  assert.equal(errors.length, 1);
  assert.match(errors[0], /Hydration failed/);
  assert.equal(carrierHydrated(doc), true, "and body now carries React's ownership stamp");
  root.unmount();
});

test("react-dom 19.2.8: a host appended where React skips it survives hydration, so timing alone decided 0.4.0's fate", async () => {
  const win = carrier();
  const doc = win.document;
  const host = mountHost(doc, win);
  doc.body.prepend(host.body);                // ahead of the <script>: a tag React does not expect here, so it is skipped
  const errors = [];
  const root = hydrateRoot(doc, landing, { onRecoverableError: (err) => errors.push(err.message) });
  await settle();
  assert.equal(host.attached(), true);
  assert.deepEqual(errors, []);
  root.unmount();
});

test("0.4.1: boot waits for React to own body, mounts once with the tree intact, survives the /profile navigation, and Close cleans up", async () => {
  const win = carrier();
  const doc = win.document;
  arm(win, { hops: 1 });
  const shell = doc.getElementById("layout");
  const booting = boot(win, { establish: false });
  await settle();
  assert.equal(doc.querySelector("." + OVERLAY_CLASS), null, "a parsed body React has not hydrated is not a ready carrier");
  assert.equal(doc.body.style.overflow, "");
  assert.equal(armHops(win), 1);

  const errors = [];
  const root = hydrateRoot(doc, landing, { onRecoverableError: (err) => errors.push(err.message) });
  const app = await booting;
  assert.ok(app instanceof App, "Forge mounted once React committed");
  assert.deepEqual(errors, [], "and hydration was clean: Forge was not in the way");
  assert.equal(doc.querySelectorAll("." + OVERLAY_CLASS).length, 1);
  assert.equal(doc.getElementById("layout"), shell, "the hydrated shell keeps its server-rendered identity");
  assert.equal(doc.body.style.overflow, "hidden");
  assert.equal(armHops(win), 0, "stable, so the hop counter resets");

  // HomeLanding: router.push("/profile") once user data resolves. A client render inside the root.
  win.history.pushState({}, "", "/profile");
  root.render(profile);
  await settle();
  assert.ok(doc.getElementById("profile") && !doc.getElementById("landing"), "the game navigated");
  assert.equal(doc.querySelectorAll("." + OVERLAY_CLASS).length, 1, "and Forge is still mounted");
  assert.equal(doc.querySelector("." + OVERLAY_CLASS).contains(app.root), true);
  assert.ok(!app.logs.some((l) => /host lost/.test(l.msg)));

  app.close();
  await settle();
  assert.equal(doc.querySelector("." + OVERLAY_CLASS), null);
  assert.equal(doc.body.style.overflow, "");
  assert.equal(isArmed(win), false);
  assert.equal(doc.getElementById("layout"), shell);
  root.unmount();
});
