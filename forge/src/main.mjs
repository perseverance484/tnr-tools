// Composition root. The only file that touches window.*; every layer is constructed here
// with the real localStorage, indexedDB and fetch, and nothing else in src/ reaches for them.
// Build: node build.mjs -> ../forge_bundle.js (IIFE), loaded by forge_loader_user.js.

import { Journal } from "./storage/journal.mjs";
import { CaptureCache } from "./storage/captures.mjs";
import { CookieSession } from "./transport/session.mjs";
import { TrpcClient } from "./transport/client.mjs";
import { Uploader } from "./transport/upload.mjs";
import { Budget } from "./budget/bucket.mjs";
import { CachedReader } from "./budget/reader.mjs";
import { Validator } from "./runner/validate.mjs";
import { Runner } from "./runner/runner.mjs";
import { Reconciler } from "./reconcile/reconciler.mjs";
import { Github } from "./github.mjs";
import { App } from "./ui/app.mjs";
import { takeover, onHostPath } from "./ui/takeover.mjs";
import { h } from "./ui/dom.mjs";
import FIELDS from "./runner/fields.json" with { type: "json" };
import NESTED from "./runner/nested.json" with { type: "json" };

export const VERSION = "forge 0.3.0";
// Field sets for pre-send validation are bundled from src/runner/fields.json, derived from the
// PINNED validators by tools/derive_fields.mjs. 45d (2026-08-26) is stale against the pin, so it
// is not fetched at boot: the bundle validates against exactly the commit it was audited on.

/**
 * Build the whole dependency graph. THIS is the composition under test: every harness calls it,
 * so a wiring mistake here (a missing journal on the Reconciler, say) fails the suite instead of
 * shipping behind a safer test-only graph. Only the environment primitives and the transport
 * client are injectable; every wiring decision lives here and nowhere else.
 */
export function compose({ storage, indexedDB, fetchImpl, clock = () => Date.now(), tabId,
                          log = () => {}, client = null, sleep } = {}) {
  const deps = {};
  deps.journal = new Journal(storage, clock);
  deps.cache = new CaptureCache(indexedDB, clock);
  deps.session = new CookieSession({ fetchImpl, origin: "" });
  deps.client = client ?? new TrpcClient(deps.session, { onExchange: (r) => log(`${r.kind} ${r.paths.join(",")} -> ${r.status ?? r.error}`) });
  deps.budget = new Budget({ storage, clock, ...(sleep ? { sleep } : {}) });
  deps.reader = new CachedReader({ client: deps.client, cache: deps.cache, budget: deps.budget });
  deps.reconciler = new Reconciler({ storage, reader: deps.reader, clock, journal: deps.journal });
  deps.github = new Github({ fetchImpl, storage });
  deps.uploader = new Uploader({ session: deps.session, fetchImpl });
  deps.validator = new Validator(FIELDS, NESTED);
  deps.runner = new Runner({
    journal: deps.journal, client: deps.client, reader: deps.reader, cache: deps.cache,
    budget: deps.budget, validator: deps.validator, uploader: deps.uploader,
    reconciler: deps.reconciler, storage, clock, tabId, log,
  });
  return deps;
}

export async function boot(win = window) {
  if (!onHostPath(win.location)) return null;
  const { body } = takeover(win.document, win);
  const status = h("div", { style: { padding: "16px", fontFamily: "system-ui", color: "#e8eaf0", background: "#0f1115", minHeight: "100vh" } }, "TNR forge: starting…");
  body.appendChild(status);

  const clock = () => Date.now();
  // the job lease is keyed by tab; sessionStorage survives a reload or a restored tab, not a new one
  let tabId;
  try { tabId = win.sessionStorage.getItem("tnr_forge_tab") || null; if (!tabId) { tabId = Math.random().toString(36).slice(2, 12); win.sessionStorage.setItem("tnr_forge_tab", tabId); } } catch { tabId = undefined; }
  let deps = {};
  try {
    deps = compose({
      storage: win.localStorage, indexedDB: win.indexedDB, fetchImpl: win.fetch.bind(win),
      clock, tabId, log: (m) => deps.app && deps.app.log(m),
    });
    deps.app = new App({ version: VERSION, storage: win.localStorage, now: clock, ...deps });
    status.remove();
    deps.app.mount(body, win.document);
    return deps.app;
  } catch (e) {
    status.textContent = "";
    status.append(h("div", {}, h("b", {}, "TNR forge failed to start")), h("pre", { style: { whiteSpace: "pre-wrap", fontSize: "12px" } }, String(e && e.stack || e)));
    return null;
  }
}

if (typeof window !== "undefined" && typeof document !== "undefined") boot(window);
